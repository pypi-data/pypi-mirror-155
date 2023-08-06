# coding=utf-8
"""
The `config` module provide easy control on behaviors of program.
This module holds 2 important global objects/variables and 1 factory class.

ConfigFactory is a factory dataclass.

Config is an instance of ConfigFactory. It's also a runtime global variable container that helps modules communicate.

BASEDIR records the location of package.
"""
from __future__ import annotations

import os
import time
from pathlib import Path

from attr import define, field, asdict

from maxoptics import __MainPath__, __ConfigPath__, __MainName__
from maxoptics.core.utils import read_config

BASEDIR = Path(os.path.dirname(os.path.abspath(__file__))).parent


class _ConfigFactoryMethodBase:
    def reflected(self, **kwargs):
        new_attributes = {**self.__dict__, **kwargs}
        return self.__class__().update(new_attributes)

    def asdict(self):
        return asdict(self)

    def update(self, dikt):
        """
        Update attrs. 'aaa-bbb' will be turned to 'aaa_bbb'.

        Args:
            dikt (dict[str, str | dict]): A config mapping.

        Returns:
            _ConfigFactoryMethodBase: return self.
        """
        for key, val in dikt.items():
            key = key.replace("-", "_")

            if isinstance(val, _ConfigFactoryMethodBase):
                val = asdict(val)

            if isinstance(val, dict):
                getattr(self, key).update(val)
            else:
                object.__setattr__(self, key, val)
        return self

    def reload(self, file=None):
        if file is None:
            file = __ConfigPath__
        confs = read_config(file)

        for conf in confs:
            if "maxoptics" in conf:
                conf = conf["maxoptics"]["cloud-sdk"]
            elif "SERVERAPI" in conf:
                ...
            else:
                continue

            self.update(conf)
        return self


@define(slots=False, frozen=False)
class ConfigFactory(_ConfigFactoryMethodBase):
    """An `attrs` dataclass and a factory of config.

    host: The host of server.

    Every MaxOptics Instance holds a ConfigFactory instance.
    """

    host: str = None
    port: int = 80
    output_dir: Path = field(
        validator=lambda instance, attribute, value: value or ".",
        converter=Path,
        default=__MainPath__.parent / "outputs",
    )
    user: str = ""
    password: str = field(converter=str, default="")
    socket_port: int = 80

    @define(slots=True, frozen=False)
    class PreferenceClass(_ConfigFactoryMethodBase):
        color: bool = False
        verbose: bool = False

    @define(slots=True, frozen=False)
    class DevelopClass(_ConfigFactoryMethodBase):
        debug: bool = False
        test_octopus_refactor: bool = False
        listen_socket: bool = True
        login: bool = True
        disable_constraints: bool = False

    @define(slots=True, frozen=False)
    class TemplateClass(_ConfigFactoryMethodBase):
        @define(slots=True, frozen=False)
        class Http(_ConfigFactoryMethodBase):
            dragon_url_template: str = "http://{host}:{port}/api/%s/"
            whale_url_template: str = "http://{host}:{port}/whale/api/%s/"
            octopus_sio_template: str = "http://{host}:{socket_port}"

        @define(slots=True, frozen=False)
        class File(_ConfigFactoryMethodBase):
            project_name_template: str = "{__MainName__}-%d-%H-%M"
            log_folder_template: str = (
                "{__MainPath__.parent}/{user}'s_output/{project.name}"
            )
            task_log_file_template: str = (
                "{project.log_folder}/{task.task_type}_{task.id}/.log"
            )
            # local
            task_yaml_template: str = "{project.log_folder}/month%mday%d/{task.task_type}_{task.task_id}.yml"

        http: Http = field(default=Http())
        file: File = field(default=File())

        @staticmethod
        def format(
            fstring: str,
            extra_locals,
            extra_config: ConfigFactory = None,
            time_strf=True,
        ):
            dikt = {
                "__MainPath__": __MainPath__,
                "__MainName__": __MainName__,
                "__ConfigPath__": __ConfigPath__,
                **Config.__dict__,
                **extra_locals,
            }
            if extra_config:
                dikt.update(extra_config.__dict__)

            fstring = fstring.format(**dikt)

            if time_strf:
                fstring = time.strftime(fstring, time.localtime())

            return fstring

    @define(slots=True, frozen=False)
    class RuntimeClass(_ConfigFactoryMethodBase):
        token: str = ""
        offline_compat: bool = False
        __from_MosLibrary__ = False
        __print_level__ = 0

    preferences: PreferenceClass = field(default=PreferenceClass())
    develop: DevelopClass = field(default=DevelopClass())
    templates: TemplateClass = field(default=TemplateClass())
    runtime: RuntimeClass = field(default=RuntimeClass())


Config = ConfigFactory().reload()
