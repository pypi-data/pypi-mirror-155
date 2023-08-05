
import json
import logging
import shutil
import json
import os
import os.path
import shutil
import tempfile
import typing
from xml.dom.expatbuilder import parseString

from .commands.proc import Proc
from .commands.netstat import Netstat
from collections import defaultdict
from ..m2m.packets import PacketType

if typing.TYPE_CHECKING:
    from typing import Callable, Text


log = logging.getLogger("agent")


DISABLED = 0
DISCOVERY_MODE = 1
ALERT_MODE = 2


class SecurityExtensions:
    """Manages security extensions."""

    def __init__(self, client):
        self.client = client

        # 'seen data' won't trigger an immediate send.
        self._seen_data = defaultdict(set)

        # pending to be sent to server
        self._pending = defaultdict(lambda: defaultdict(lambda: 0))
        self._counter = 0

        self.mode = DISCOVERY_MODE

    @classmethod
    def init(cls, client): #, remote_directory, m2m_url=None):
        #url = m2m_url or constants.M2M_URL
        sec_ext = cls(client) #, url, remote_directory)
        return sec_ext

    def _reset_pending(self):
        # pending to be sent to server
        self._pending = defaultdict(lambda: defaultdict(lambda: 0))
        self._counter = 0

    def get_data_model(self, kind):
        if kind == "proc":
            return Proc().get_data_model()
        elif kind == "netstat":
            return Netstat().get_data_model()

    def __repr__(self):
        # type: () -> Text
        return "SecurityExtensions(enabled=%r)" % self.enabled

    def poll(self):
        commands = [Proc(), Netstat()]
        if not self._seen_data:
            self.load_ids_data()

        self._counter += 1
        for cmd in commands:
            data = cmd.execute()

            not_seen_data = data.difference(self._seen_data[cmd.kind])
            for item in data:
                self._pending[cmd.kind][item] += 1

            if not_seen_data:
                log.warning(
                    "Found %s data not seen before: %s", 
                    len(not_seen_data), not_seen_data
                    )
                self.append_ids_data(cmd.kind, list(not_seen_data))
            else:
                log.warning("No new data")
            self._seen_data[cmd.kind].update(data)

            if self.mode == DISCOVERY_MODE:
                pass
            if self.mode == ALERT_MODE:
                pass  # raise alert

        if self._counter == 5:
            log.warning("Sending pending data: %s", len(self._pending.keys()))
            for kind in self._pending.keys():
                self.append_ids_data(kind, list(self._pending[kind].keys()))
            self._reset_pending()


    def load_ids_data(self):
        # type: () -> None
        log.debug("Starting initial load IDS data")

        with self.client.remote.batch() as batch:
            batch.call_with_id(
                "authenticate_result",
                "device.check_auth",
                device_class="tuxtunnel",
                serial=self.client.serial,
                auth_token=self.client.auth_token,
            )
            batch.call_with_id(
                "ids_data",
                "ids.get_ids_deviceclass_data"
            )
        batch.get_result("authenticate_result")
        batch.check("ids_data")

        ids_data = batch.get_result("ids_data")
        for key, values in ids_data.items():
            _model = self.get_data_model(key)
            self._seen_data[key].update(
                set(_model(*row) for row in values)
                )
            log.warning("Loaded %s items for %s", key, len(self._seen_data[key]))

    def _parse_data(self, kind, data):
        result = []
        for row in data:
            _data = row._asdict()
            _data["seen"] = self._pending[kind][row]
            result.append(_data)
        return result

    def append_ids_data(self, kind, data):
        # type: (bytes, bytes) -> None

        parsed_data = self._parse_data(kind, data)

        with self.client.remote.batch() as batch:
            batch.call_with_id(
                "authenticate_result",
                "device.check_auth",
                device_class="tuxtunnel",
                serial=self.client.serial,
                auth_token=self.client.auth_token,
            )
            batch.call(
                "ids.add_ids_data",
                kind=kind,
                counter=self._counter,
                data=parsed_data
            )

