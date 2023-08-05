from subprocess import Popen, PIPE
from re import split
from sys import stdout

from .base import CommandBase
from sh import ps



class Proc(CommandBase):
    enabled_attrs = ["user", "cmd"]
    kind = "proc"

    def to_dict(self):
        return { label: str.strip(getattr(self, label).encode()) for label in self.enabled_attrs}

    @staticmethod
    def _get_cmd():
        return ps("-afwwo", "user cmd", _iter=True)

    @staticmethod
    def _clean_cmd(cmd):
        return cmd.replace("\_ ", "")

    def parse_params(self, data):
        data = data.split()
        cmd = self._trim_sensitive_data(
            " ".join(data[1:]), 
            ["auth", "password", "serial", "pass"]
            )
        return {
            "user": data[0],
            "cmd": self._clean_cmd(cmd)
            }

    def execute(self):
        """
            USER     COMMAND
            root     bash
            root      \_ ps -afwwo user,command
            root     bash
            root      \_ python -m dataplicity.app -s http://api:8001 --remote-dir /tmp --auth <hidden> --serial <hidden>
        """
        result = set()
        data_class = self.get_data_model()
        for e, proc_row in enumerate(self._get_cmd()):
            if e == 0:  # skip header
                continue
            result.add(data_class(**self.parse_params(proc_row)))
        return result


if __name__ == "__main__":
    proc_list = Proc().execute()
    stdout.write("Process list: \n")
    for proc in proc_list:
        stdout.write("\t" + str(proc) + "\n")