import inspect
import json
import os
from abc import ABC
from pathlib import Path
from shutil import rmtree

import requests

from maxoptics.core.logger import error_print
from maxoptics.core.project.utils import Index
from .BaseClient import BaseClient


class WhaleClients(BaseClient, ABC):
    def __init__(
        self, task_id, project=None, config=None, status=0, tarsrc_name=None
    ):
        super().__init__("whale_url_template")
        self.task_id = int(task_id)
        self.monitor_num = 0
        self.id = task_id
        self.status = status
        self.project = project
        self.task_type = ""
        self.tarsrc_name = tarsrc_name
        self.error = Exception("Unknown Error")
        self.file_dirs = []

        if config:
            self.config = config

    def rm_files(self):
        """Remove relative files.
        File/dir paths are stored in self.file_dirs.
        """
        for file_dir_raw in self.file_dirs:
            fd = Path(file_dir_raw)
            try:
                if fd.is_dir():
                    rmtree(fd)
                elif fd.is_file():
                    os.remove(fd)
                else:
                    error_print("Unknown object to remove" + str(fd))
            except (FileNotFoundError, PermissionError):
                error_print(f"Fail to delete {fd}")

        self.file_dirs = []

    def post(self, url="", json_params="", **kwargs):
        """Partial method of HttpIo.post. Token is a fixed parameter."""
        return super().post(url, {"token": self.token}, json_params, **kwargs)

    @property
    def Index(self):
        """Get an `Index` instance of current project.

        Returns:
            Index
        """
        return Index(self.project, self.task_type, self.tarsrc_name)

    def check_status(self, quiet=False):
        """Print and return using status.

        Args:
            quiet (bool): If True, no print will be shown.

        Returns:
            Optional[bool]: False for unintended termination. True for success. None for still running/waiting.
        """
        if self.status == -2:
            print(f"Task {self.task_id} is stopped.")
            return False
        if self.status == -1:
            print(f"Task {self.task_id} is paused.")
            return False
        if self.status == 0:
            if not quiet:
                print(f"Task {self.task_id} is waiting.")
        if self.status == 1:
            if not quiet:
                print(f"Task {self.task_id} is running.")
        if self.status == 2:
            return True

    def update_status(self):
        """Update status of current task.

        Returns:
            None
        """
        url_template = self.config.templates.http.dragon_url_template
        try:
            api_address = self.config.host
        except AttributeError:
            error_print("Library is not fully initialized: host is not set.")
            exit(1)
        port = self.config.port
        api_url = url_template.format(api_address, port)  # Dragon url
        res = requests.post(
            api_url % ("get_tasks_status"),
            data=json.dumps({"token": self.token, "ids": [self.id]}),
            headers={
                "Content-Type": "application/json",
                "Connection": "close",
            },
        )
        self.status = json.loads(res.text)["result"][str(self.id)]


def fillargs(f, args, kws):
    """Distribute incoming arguments and key-word arguments."""
    spec = inspect.getargspec(f)
    __args = spec.args[1:]
    print(spec.args)  # RM
    __defaults = spec.defaults
    result = dict().fromkeys(__args)
    # Default values
    __values = __args[::-1]
    __defaults = __defaults[::-1] if __defaults else []
    for i in range(len(__defaults)):
        result[__values[i]] = __defaults[i]

    for i in range(len(args)):
        result[__args[i]] = args[i]

    for k in result:
        if k in kws:
            result[k] = kws[k]

    return result, __args
