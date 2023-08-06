"""
The `maxoptics` module implements `MosLibraryCloud`_, provides shortcut for
`Macros`_ and other information.
"""
import warnings
from time import sleep

from maxoptics.core.utils import package_initialization, removesuffix
from maxoptics.macros import (
    X_Linear,
    Y_Linear,
    Z_Linear,
    Point,
    PortLeftAttach,
    PortRightAttach,
    X_Normal,
    Y_Normal,
    Z_Normal,
)

__all__ = (
    "X_Normal",
    "Y_Normal",
    "Z_Normal",
    "X_Linear",
    "Y_Linear",
    "Z_Linear",
    "Point",
    "PortLeftAttach",
    "PortRightAttach",
    "MosLibraryCloud",
    "__MainPath__",
    "__MainName__",
    "__ConfigPath__",
    "__version__",
)

__MainPath__, __ConfigPath__ = package_initialization()
__MainName__ = removesuffix(__MainPath__.name or "unnamed", ".py")

# Version Number
__version__ = "0.9.2"


class MosLibraryCloud:
    """
    .. _MosLibraryCloud:

    Entrance of cloud sdk.
    """

    def __new__(cls, **kws):
        """Everytime this class is called, config will be reloaded."""
        from maxoptics.config import Config
        from maxoptics.sdk import MaxOptics

        # print("Using Config From", __ConfigPath__)
        if Config.runtime.offline_compat and hasattr(
            Config, "__from_MosLibrary__"
        ):
            warnings.warn(
                UserWarning(
                    "You have triggered 'local Script Compat Mode' "
                    "and still using MosLibraryCloud() to create new MaxOptics Instance.\n"
                    "The created Instance may not share projects, materials, tasks "
                    "and any operations you have done on other Maxoptics instance(s).\n"
                    "\n"
                    "If you want to access the object and methods hidden by "
                    "your script(s), you can do:\n"
                    "1. `project = solver.__parent__`, and\n"
                    "2. `client = project.__parent__`\n"
                    "\n"
                    "to access these instances.\n"
                )
            )
            sleep(3)
        Config.runtime.__from_MosLibrary__ = True
        mos_instance = MaxOptics()
        Config.runtime.__from_MosLibrary__ = False

        if kws:
            mos_instance.config = Config.reflected(**kws)
        else:
            mos_instance.config = Config.reflected()

        if Config.develop.login:
            mos_instance.login()

        mos_instance.search_projects()

        Config.__Global_MOS_Instance__ = mos_instance

        return mos_instance


class MosLibrary:
    """Deprecated. Please user MosLibraryCloud instead."""

    def __new__(cls, **kws):
        warnings.warn(
            FutureWarning(
                "\nThe usage of MosLibrary is planned to be deprecated in 0.10.0, please use MosLibraryCloud instead."
            )
        )
        return MosLibraryCloud(**kws)
