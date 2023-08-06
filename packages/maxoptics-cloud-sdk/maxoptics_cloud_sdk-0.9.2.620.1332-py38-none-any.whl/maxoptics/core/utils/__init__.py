# coding=utf-8
"""This module provides utilities used frequently by other modules."""
import inspect
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Union, List, Dict, Callable


class ShadowAttr:
    def __new__(cls, _key="", *args):
        def getter(self):
            key = _key
            return self.get(key)

        def setter(self, value):
            key = _key
            return self.set(key, value)

        def deleter(self):
            key = _key
            exec(f"del self.{key}")

        return property(fget=getter, fset=setter)


def damerau_levenshtein_distance(s1, s2):
    # From jellyfish
    len1 = len(s1)
    len2 = len(s2)
    infinite = len1 + len2

    # character array
    da = defaultdict(int)

    # distance matrix
    score = [[0] * (len2 + 2) for x in range(len1 + 2)]

    score[0][0] = infinite
    for i in range(0, len1 + 1):
        score[i + 1][0] = infinite
        score[i + 1][1] = i
    for i in range(0, len2 + 1):
        score[0][i + 1] = infinite
        score[1][i + 1] = i

    for i in range(1, len1 + 1):
        db = 0
        for j in range(1, len2 + 1):
            i1 = da[s2[j - 1]]
            j1 = db
            cost = 1
            if s1[i - 1] == s2[j - 1]:
                cost = 0
                db = j

            score[i + 1][j + 1] = min(
                score[i][j] + cost,
                score[i + 1][j] + 1,
                score[i][j + 1] + 1,
                score[i1][j1] + (i - i1 - 1) + 1 + (j - j1 - 1),
            )
        da[s1[i - 1]] = i

    return score[len1 + 1][len2 + 1]


def nearest_words_with_damerau_levenshtein_distance(dic, name):
    def extract_dict(mapping: Dict, list_of_name: List):
        for key_name in mapping:
            if key_name not in list_of_name:
                list_of_name.append(key_name)
            if isinstance(mapping[key_name], dict):
                extract_dict(mapping[key_name], list_of_name)
        return list_of_name

    if isinstance(dic, dict):
        name_list = extract_dict(dic, [])
    elif isinstance(dic, list):
        name_list = dic
    else:
        raise SystemError("SDK down.")

    dis_list = []
    result_list = []
    for n in name_list:
        dis = damerau_levenshtein_distance(n, name)
        dis_list.append(dis)
        result_list.append(n)

    sorted_zipped = sorted(zip(dis_list, result_list))
    sorted_unzipped = tuple(zip(*sorted_zipped))[1][:5]
    return sorted_unzipped


def is_float(value: Any) -> Union[float, None]:
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def camel_to_snake(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def package_initialization():
    def find_config(directory: Path, fn, depth=3):
        if depth == 0:
            return None

        try:
            # if os.path.isfile(directory):
            #     if (
            #         directory.name.endswith(".yml") or
            #         directory.name.endswith(".toml")
            #     ):
            #         file = directory
            #     else:
            #         file = directory.parent/fn
            # else:

            file = directory / fn

            if os.path.exists(file):
                return file
            else:
                if directory.parent == directory:
                    return None
                else:
                    dirp = directory.parent
                    return find_config(dirp, fn, depth - 1)

        except PermissionError:
            return None

    def get_main():
        def get_non_test_main():
            try:
                ret = Path(inspect.getfile(sys.modules.get("__main__")))
                if ret.name not in ["_jb_pytest_runner.py"]:
                    return ret
            except (AttributeError, TypeError):
                return None

        def get_current_test():
            raw_ret = os.getenv("PYTEST_CURRENT_TEST")
            if raw_ret:
                ret = Path(raw_ret.split("::")[0])
                if ret.exists():
                    return ret

        def get_last_stack():
            files_from_stack = (
                stack[1]
                for stack in inspect.stack()
                if "maxoptics" in (stack[4] or [""])[0]
            )

            for stack_file in files_from_stack:
                if Path(stack_file).name not in [
                    "__init__.py",
                    "_jb_pytest_runner.py",
                ]:
                    return Path(stack_file)

        ret_0 = (
            get_current_test()
            or get_last_stack()
            or get_non_test_main()
            or Path(".")
        )

        return ret_0.absolute()

    def get_root():
        # TODO: use Path.home() instead of fetch it from env vars.
        if sys.platform == "darwin" or sys.platform == "linux":
            ret = Path(os.getenv("HOME"))
            if (ret / "maxoptics.toml").exists():
                return ret
            else:
                ret = Path("/")
                if (ret / "maxoptics.toml").exists():
                    return ret

        elif sys.platform == "win32" or sys.platform == "win64":
            ret = Path(os.getenv("USERPROFILE") or os.getenv("HOMEPATH"))
            if (ret / "maxoptics.toml").exists():
                return ret
            else:
                ret = Path(os.getenv("SYSTEMDRIVE"))
                if (ret / "maxoptics.toml").exists():
                    return ret

    def get_env():
        ret = os.getenv("MAXOPTICS_SDK_CONFIG")
        if ret:
            return Path(ret).absolute()

    def yield_config():
        root = get_root()
        main = get_main()
        env = get_env()

        for dear, *fns, max_dep in [
            (root, "maxoptics.toml", 1),
            (main, "pyproject.toml", 10),
            (main, "maxoptics.conf", "maxoptics.yml", "maxoptics.toml", 4),
            (env, "maxoptics.toml", "maxoptics.yml", 2),
        ]:
            if not dear:
                continue
            else:
                for filename in fns:
                    ret = find_config(dear, filename, max_dep)
                    if ret:
                        yield ret

    __MainPath__ = get_main() or Path(".")
    __ConfigPath__ = list(yield_config())

    return __MainPath__, __ConfigPath__


def read_config(files):
    def compat_keys(config_key: str):
        mapping = {
            "SERVERAPI": "host",
            "SERVERPORT": "port",
            "OUTPUTDIR": "output_dir",
            "DEFAULTUSER": "user",
            "DEFAULTPASSWORD": "password",
        }
        if config_key.upper() == config_key:
            if config_key in mapping:
                return mapping[config_key]
            elif len(config_key) > 1:
                return config_key[0] + (config_key[1:]).lower()
            else:
                return config_key
        else:
            return config_key

    def yaml_config_reader(fi):
        import yaml

        with open(fi, "r", encoding="utf-8") as fio:
            try:
                ret = yaml.load(fio, yaml.SafeLoader)
                return {compat_keys(key): val for key, val in ret.items()}

            except yaml.YAMLError as e:
                print(f"{fi} is corrupted! Please check it.")
                print(e)
                exit(1)

    def toml_config_reader(fi):
        import toml

        with open(fi, "r", encoding="utf-8") as fio:
            try:
                return toml.load(fio)

            except toml.TomlDecodeError as e:
                print(f"{fi} is corrupted! Please check it.")
                print(e)
                exit(1)

    if not isinstance(files, list):
        files = [files]

    for file in files:
        file = Path(file)
        if file.name:
            try:
                yield {
                    "yml": yaml_config_reader,
                    "yaml": yaml_config_reader,
                    "conf": yaml_config_reader,
                    "toml": toml_config_reader,
                }[file.name.split(".")[-1]](file)
            except UnicodeDecodeError as e:
                print(file, " is corrupted! Please check it.")
                raise e


def decohints(decorator: Callable) -> Callable:
    """To fix the strange problem of Pycharm"""
    return decorator


if sys.version_info.minor >= 9:
    # 3.9 python added these methods.
    fdict = dict
    fstr = str

else:

    class fdict(dict):
        """A dict class with __or__ method."""

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def __or__(self, incoming):
            # assert isinstance(incoming, self.__class__)
            # for arg in args:
            # assert isinstance(arg, self.__class__)
            self.update(incoming)
            return self

    class fstr(str):
        """A string class with removesuffix and removeprefix."""

        def __init__(self, obj):
            self.__str__ = obj
            super().__init__()

        def removesuffix(self, suffix):
            len_of_suffix = len(suffix)
            if len(self) < len_of_suffix:
                return self
            else:
                if self[-len_of_suffix:] == suffix:
                    return fstr(self[:-len_of_suffix])
                else:
                    return self

        def removeprefix(self, prefix: str):
            len_of_prefix = len(prefix)
            if len(self) < len_of_prefix:
                return self
            else:
                if self[:len_of_prefix] == prefix:
                    return fstr(self[len_of_prefix:])
                else:
                    return self


def removeprefix(self: str, prefix: str):
    """Remove the prefix if the str starts with the prefix."""
    assert isinstance(prefix, str)
    len_of_prefix = len(prefix)
    if len(self) < len_of_prefix:
        return self
    else:
        if self[:len_of_prefix] == prefix:
            return self[len_of_prefix:]
        else:
            return self


def removesuffix(self: str, suffix: str):
    """Remove the suffix if the str ends with the suffix."""
    assert isinstance(suffix, str)
    len_of_suffix = len(suffix)
    if len(self) < len_of_suffix:
        return self
    else:
        if self[-len_of_suffix:] == suffix:
            return self[:-len_of_suffix]
        else:
            return self
