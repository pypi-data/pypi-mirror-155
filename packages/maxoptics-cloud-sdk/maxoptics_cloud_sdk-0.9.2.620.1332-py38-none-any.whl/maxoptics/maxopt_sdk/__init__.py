# flake8:noqa
"""The `maxopt_sdk` package performs as an instruction converter when executing offline scripts.
"""
import json
import os
from functools import wraps
from itertools import count
from pathlib import Path
from typing import Callable, Dict
from uuid import uuid4

from matplotlib import pyplot as plt

from maxoptics.config import Config
from maxoptics.core.base.BaseContainer import WaveformShell
from maxoptics.core.component.base.Component import ProjectComponent, Solver
from maxoptics.core.logger import info_print, warn_print
from maxoptics.core.plot.heatmap import heatmap
from maxoptics.core.project.Project import dynamic_add
from maxoptics.core.project.ProjectBase import yield_components_with_class
from maxoptics.core.TaskFile import TaskFile
from maxoptics.core.base import (
    Material as CoreMaterial,
    Waveform as CoreWaveform,
)

# %%utils
from maxoptics.macros import (
    Simu_FDTD_Mode_Expansion,
    X_Normal,
    Y_Normal,
    Z_Normal,
)
from .utils import Workspace, TinyTaskInfo
from maxoptics.var.models.meta.PowerMonitor import (
    PowerMonitor,
)
from maxoptics.var.models.MitM import (
    EME,
    FDE,
    FDTD,
    FDTDPortGroup,
)
from maxoptics.var.MosIO.Network.WhaleClient import WhaleClients
from maxoptics.var.project import MosProject

Config.runtime.offline_compat = True


def __sdk__():
    """Get the cached client instance.

    Returns:
        MaxOptics
    """
    from maxoptics.sdk import MaxOptics

    if not hasattr(Config, "__Global_MOS_Instance__"):
        from maxoptics import MosLibraryCloud

        Config.runtime.offline_compat = False
        MosLibraryCloud()
        Config.runtime.offline_compat = True
    ret: MaxOptics = Config.__Global_MOS_Instance__
    return ret


def __pname__():
    """Get default project name. The output depends on value of
    **templates**.**project_name_template** in configuration file.

    Returns:
        str: The default project name.
    """
    template = Config.templates.file.project_name_template
    ret = Config.templates.format(template, {}, __sdk__().config)
    return ret


def __not_implemented__(*args, **kwargs):
    """A template of NotImplemented functions. Just print "Ignored"."""
    print("Ignored")


mc = count(0)


def style_trans(func: Callable):
    """Add support to plotX="x" type writing."""

    @wraps(func)
    def wrapper(target, pub, option, *args, **kwargs):
        new_option = {}
        for key, value in option.items():
            if key in ["plotX", "plotY"]:
                new_option[value] = key
            else:
                new_option[key] = value

        return func(target, pub, new_option, *args, **kwargs)

    return wrapper


# %% Models


class GdsModel:
    """A gds operation recorder.
    Records all the gds_import operations and post-assignments.
    """

    def __init__(self, file):
        self.file = file
        self.storef = []

    def gds_import(self, cellname, layer, material, zmin, zmax):
        """
        Stores `gds_import` action.
        `add_structure`_ will get all stored actions and apply them on the solver.

        Args:
            cellname (str): The cell's name.

            layer (tuple(int, int)): A 2-elements tuple.

            material (MaterialShell): A material repr object returned by ``find_material``.

            zmin (float): The minimum on z axis direction.

            zmax (float): The maximum on z axis direction.

        Returns:
            dict[str, Any]: A dict acts as an assignment-operation recorder.
        """
        if isinstance(layer, tuple):
            layer = "{0}/{1}".format(*layer)

        operation_recorder = {}

        def functor(solver):
            objs = solver.gds_import(
                self.file, cellname, layer, material.name, zmin, zmax
            )
            assert objs is not None, "gds import failed!"
            for obj in objs:
                if "mesh_order" in operation_recorder.keys():
                    operation_recorder["meshOrder"] = operation_recorder.pop(
                        "mesh_order"
                    )

                obj.update(**operation_recorder)

        self.storef.append(functor)
        return operation_recorder

    def add_rectangle(self, *args):
        """
        Stores `add_rectangle` action.
        `add_structure`_ will get all stored actions and apply them on the solver.
        """

        def _(p):
            add_rectangle(p, *args)

        self.storef.append(_)

    @property
    def structures(self):
        return self

    def show(self, *args, **kwargs):
        print("Not Implemented")


# To compat mesh_order to meshOrder
# from maxoptics.var.models.meta.GdsPolygon import GdsPolygonAttrs
# GdsPolygonAttrs.mesh_order = ShadowAttr("meshOrder")


# %% Component


def set_geometry(self: MosProject, **kwargs):
    for key, val in kwargs.items():
        if key in [
            "x",
            "x_span",
            "x_min",
            "x_max",
            "y",
            "y_span",
            "y_min",
            "y_max",
            "z",
            "z_span",
            "z_min",
            "z_max",
        ]:
            self[key] = val


ProjectComponent.set_geometry = set_geometry

# %% Project & Solver

c = count()


def add_rectangle(
    self, center, width, height, rotation, z_min, z_max, material
):
    """
    A compat method for the offline method with same name.

    Leave relative sentences as is.
    """
    return self.create_rectangle(
        name=f"add_rectangle_{next(c)}",
        x=center[0],
        y=center[1],
        x_span=width,
        y_span=height,
        rotate_z=rotation,
        z_min=z_min,
        z_max=z_max,
        materialId=material,
    )


MosProject.add_rectangle = add_rectangle


def add(self, klass, dikt: Dict = {}):
    """
    A compat method for the offline method with same name.

    Leave relative sentences as is.
    """
    component = dynamic_add(klass, "", self)

    # filtered_dict = {key: val for key, val in dikt.items() if key in component}
    filtered_dict = dikt

    return component.update(**filtered_dict)


MosProject.add = add


def add_structure(self, gds_model: GdsModel):
    """
    .. _add_structure:

    A compat method for the offline method with same name.

    Leave relative sentences as is.
    """
    for f in gds_model.storef:
        f(self)


MosProject.add_structure = add_structure


# %% Solver


def run_meshgen(*args, **kwargs):
    """This is an offline exclusive method, not supported in cloud version."""
    print("run_meshgen is not needed")

    class G:
        workspace = "run_meshgen"

    return G()


Solver.run_meshgen = run_meshgen


def fde_run(self, *args):
    """
    A compat method for the offline method with same name.

    Leave relative sentences as is.
    """
    self: FDE
    project = self.__parent__

    ret = project.run_fde()
    return ret


FDE.run = fde_run


def eme_run(self, only_fde=False, *args):
    """
    A compat method for the offline method with same name.

    Leave relative sentences as is.
    """
    self: EME
    project: MosProject = self.__parent__
    if only_fde:
        ret = EMEResultHandler(0, project, None, status=-1)
    else:
        _ = project.run_eme_fde()
        ret = project.run_eme_eme(dep_task=_.id)

    wok = Workspace().load(ret.workspace)

    source_modes = wok.others["source_modes"] = {}

    for port in project.ports:
        port_mode = project.run_calculate_modes(port)
        source_modes[port.name] = TinyTaskInfo(
            port_mode.id, port_mode.__class__
        )

    wok.dump(ret.workspace)

    return ret


EME.run = eme_run


def set_cell_group(self, x_min, cell_group):
    """
    A compat method for the offline method with same name.

    Leave relative sentences as is.
    """
    self: EME
    self.attrs.x_min = x_min
    for cell in cell_group:
        self.append_cell(**cell, fix="x_min")


EME.set_cell_group = set_cell_group


def fdtd_run(self, only_fde=False, *args):
    """
    A compat method for the offline method with same name.

    Leave relative sentences as is.
    """
    self: FDTD
    project: MosProject = self.__parent__

    if only_fde:
        ret = FDTDResultHandler(0, project, None, status=-1)
    else:
        ret = project.run_fdtd()

    _ws = ret.workspace

    wok = Workspace().load(_ws)

    source_modes = wok.others["source_modes"] = {}

    for poso in project.ports + project.sources:
        _mode = project.run_calculate_modes(poso)
        source_modes[poso.name] = TinyTaskInfo(_mode.id, _mode.__class__)

    wok.dump(_ws)

    return ret


FDTD.run = fdtd_run


def fdtd_run_mode_expansion(self, fdtd_path, **kwargs):
    """
    A compat method for the offline method with same name.

    Leave relative sentences as is.
    """
    wok = Workspace().load(fdtd_path)

    fdtd_task_id = wok.main.id
    project: MosProject = self.__parent__

    me_results = wok.others[Simu_FDTD_Mode_Expansion] = {}
    me_mode_results = wok.others["source_modes"] = {}
    project.save()

    mes = list(yield_components_with_class(ModeExpansion, project))
    for _, me in mes:
        ret = project.run_fdtd_mode_expansion(me, dep_task=fdtd_task_id)

        pm_ids = [_["id"] for _ in me.attrs.monitors_for_expansion]
        assert pm_ids, f"{me.name} binds no monitor."

        the_pm = None
        for pm_id in pm_ids:
            pm: PowerMonitor = [_ for _ in project.monitors if _.id == pm_id][
                0
            ]
            if pm.attrs.mode_expansion.get("__used__") in [None, me.name]:
                the_pm = pm

        assert the_pm, "Host PowerMonitor Not Found!"

        me_results[the_pm.name] = TinyTaskInfo(ret.id, ret.__class__)

        # mode_expansion.attrs.mode_selection = 3
        cmret = project.run_calculate_modes(me)
        me_mode_results[the_pm.name] = TinyTaskInfo(cmret.id, cmret.__class__)
        wok.dump(fdtd_path)

    class Empty:
        def __init__(self):
            self.workspace = fdtd_path

    return Empty()


FDTD.run_mode_expansion = fdtd_run_mode_expansion


def __solver_add(self, *args, **kwargs):
    """Bind ``solver.add`` to ``project.add``"""
    return add(self.__parent__, *args, **kwargs)


EME.add = FDE.add = FDTD.add = FDTDPortGroup.add = __solver_add


def __solver_add_structure(self, *args, **kwargs):
    """Bind ``solver.add_structure`` to ``project.add_structure``"""
    return add_structure(self.__parent__, *args, **kwargs)


EME.add_structure = (
    FDE.add_structure
) = FDTD.add_structure = __solver_add_structure


def __calc_mem(self, *args, **kwargs):
    """This is an offline exclusive method, not supported in cloud version."""
    print("Not Implemented")


FDE.calc_mem = EME.calc_mem = FDTD.calc_mem = __calc_mem


def __create_project(kwargs) -> MosProject:
    """
    Create project with the global client.
    """
    instance = Config.__Global_MOS_Instance__
    if "name" in kwargs:
        name = kwargs.pop("name")
    else:
        name = __pname__()

    project = instance.create_project_as(name=name)
    return project


def FDE(kwargs={}):
    """
    A compat class for offline package's ``FDE``.

    Preparation will be executed in the background.
    """
    project = __create_project(kwargs)

    fde = project.create_fde(**kwargs)
    # Add to __parent__ to avoid gc
    fde.__parent__ = project
    return fde


def EME(kwargs={}):
    """
    A compat class for offline package's ``EME``.

    Preparation will be executed in the background.
    """
    project = __create_project(kwargs)
    eme = project.create_eme(**kwargs)
    # Add to __parent__ to avoid gc
    eme.__parent__ = project
    return eme


def FDTD(kwargs={}):
    """
    A compat class for offline package's ``FDTD``.

    Preparation will be executed in the background.
    """
    project = __create_project(kwargs)

    fdtd = project.create_fdtd(**kwargs)
    # Add to __parent__ to avoid gc
    fdtd.__parent__ = project
    fdtd.__dict__["waveforms"] = []
    return fdtd


# %%Visual

from maxoptics.var.visualizer.main import *


@style_trans
def passive_any(target, pub, options, functor_name):
    """Common part for some result retrieval methods."""
    pubs = dict(
        attribute=pub.get("attribute"),
        operation=pub.get("operation"),
        monitor=pub.get("monitor") or pub.get("monitorIndex"),
    )
    monitor = pubs["monitor"]

    for key, val in list(pubs.items()):
        if val is None:
            pubs.pop(key)

    task_path = pub.get("taskPath")
    wok = Workspace().load(task_path)
    wokt = wok.main

    task = wokt.get_task(monitor, __sdk__().config)
    functor = getattr(task, functor_name)

    return functor(target=target, **pubs, **options)


def passive_fde_result_chart(target, pub, options):
    """
    A compat method for the offline method with same name.

    Leave relative sentences as is.
    """
    return passive_any(target, pub, options, "passive_fde_result_chart")


def passive_eme_fd_result_chart(target, pub, options):
    """
    A compat method for the offline method with same name.

    Leave relative sentences as is.
    """
    return passive_any(target, pub, options, "passive_eme_monitor_chart")


def passive_eme_smatrix_chart(target, pub, options):
    """
    A compat method for the offline method with same name.

    Leave relative sentences as is.
    """
    pub.update(attribute="S")
    target = "intensity"
    return passive_any(target, pub, options, "passive_eme_smatrix_chart")


def passive_fdtd_fd_result_chart(target, pub, options):
    """
    A compat method for the offline method with same name.

    Leave relative sentences as is.
    """
    return passive_any(target, pub, options, "passive_fdtd_fd_result_chart")


def passive_fdtd_td_result_chart(target, pub, options):
    """
    A compat method for the offline method with same name.

    Leave relative sentences as is.
    """
    return passive_any(target, pub, options, "passive_fdtd_td_result_chart")


@style_trans
def passive_fdtd_mode_expansion_chart(target, pub, options):
    """
    A compat method for the offline method with same name.

    Leave relative sentences as is.
    """
    functor_name = "passive_fdtd_mode_expansion_chart"

    pubs = dict(
        log=pub.get("log"),
        attribute=pub.get("attribute"),
        operation=pub.get("operation"),
        monitor=pub.get("monitor"),
    )

    for key, val in list(pubs.items()):
        if val is None:
            pubs.pop(key)

    task_path = pub.get("taskPath")
    wok = Workspace().load(task_path)

    monitor = pubs["monitor"]

    me_results = wok.others[Simu_FDTD_Mode_Expansion]

    assert monitor.name in me_results, "result not found!"

    wokt = me_results[monitor.name]
    config = __sdk__().config
    task = wokt.get_task(monitor, config)
    functor = getattr(task, functor_name)
    return functor(target=target, **pubs, **options)


@style_trans
def passive_fdtd_mode_expansion_fde_result_chart(target, pub, options):
    """
    A compat method for the offline method with same name.

    Leave relative sentences as is.
    """
    functor_name = "passive_fde_result_chart"

    pubs = dict(
        log=pub.get("log"),
        attribute=pub.get("attribute"),
        operation=pub.get("operation"),
    )

    for key, val in list(pubs.items()):
        if val is None:
            pubs.pop(key)

    task_path = pub.get("taskPath")
    wok = Workspace().load(task_path)

    monitor = pub["monitor"]

    me_result = wok.others["source_modes"]
    assert monitor.name in me_result, ""

    task = me_result[monitor.name].get_task(monitor, __sdk__().config)

    functor = getattr(task, functor_name)
    return functor(target=target, **pubs, **options)


@style_trans
def passive_source_fde_result_chart(target, pub, options):
    """
    A compat method for the offline method with same name.

    Leave relative sentences as is.
    """
    functor_name = "passive_fde_result_chart"

    pubs = dict(
        log=pub.get("log"),
        attribute=pub.get("attribute"),
        operation=pub.get("operation"),
    )

    monitor = pub["monitor"]

    for key, val in list(pubs.items()):
        if val is None:
            pubs.pop(key)

    task_path = pub.get("taskPath")
    wok = Workspace().load(task_path)

    source_modes_result = wok.others["source_modes"]
    assert monitor.name in source_modes_result, "Can't find matching result"
    config = __sdk__().config
    if source_modes_result[monitor.name].id == 0:
        warn_print(
            f"FDE solving of {monitor.name} is omitted, therefore result fetch will be omitted."
        )
        return passive_fake(target, None, None)

    task = source_modes_result[monitor.name].get_task(monitor, config)

    functor = getattr(task, functor_name)
    return functor(target=target, **pubs, **options)


# Fake methods
def passive_fake(target, pub, options):
    """
    A fake result retrieval method that returns blank data.

    Prevent the running program from raising error when an action is not-implemented/skipped.
    """
    data = {
        "data": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        "columns": [1, 2, 3],
        "header": [1, 2, 3],
        "index": [1, 2, 3],
        "horizontal": [1, 2, 3],
        "vertical": [1, 2, 3],
        "dWidth": [1, 2, 3],
        "dHeight": [1, 2, 3],
    }

    class Task:
        task_id = 0

    info_print("Not Implemented")
    return TaskFile(data, task=Task(), target=target)


class View:
    def __init__(self, pth, solver):
        """
        The mesh file is imported during initialization, and the actual coordinates of the corresponding mesh
        are obtained according to the user-defined project such as eme, etc.

        Args:
            pth(path): The workspace。

            solver(Simulation): User-created project to get the actual coordinates of the
            corresponding mesh file.
        """
        self.file = str(pth)

        self.project = solver.__parent__

    def plot2D(
        self,
        savepath="",
        grid="on",
        show=True,
        ptitle="meshview",
        index="",
        mapping=None,
        **slicer,
    ):
        """View the mesh result of a slice of the structure by adding index monitor.

        Args:
            savepath (str): Path of files to save mesh heatmap(s).

            grid (bool): Local exclusive functionality. Makes no difference in this method.

            show (bool): If true, pop out a window and show the picture(s). If false, save the picture(s).

            ptitle (str): The title of picture(s).

            index (str): Local exclusive parameter. Makes no difference in this method.

            mapping (None): Local exclusive parameter. Makes no difference in this method.

            slicer: Denote the slice with a single key-word argument. Such as ``x=1``.

        Returns:
            list[str, ...]: A list of visualized attributes (nx, ny, ...).
        """
        assert len(slicer) < 2, "too many dimensions!!"
        solver = self.project.solver

        key = list(slicer.keys())[0]
        val = list(slicer.values())[0]

        _3d = {
            "x": X_Normal,
            "y": Y_Normal,
            "z": Z_Normal,
        }
        monitor_type = _3d[key]

        plot_axis = set(_3d).difference(set(slicer))

        i1, i2 = sorted(tuple(plot_axis))

        overwrite = {key: val, f"{key}_span": 0, "monitor_type": monitor_type}

        im = self.project.create_index_monitor()
        im.sync_spatial(solver)
        im.update(**overwrite)

        task = self.project.run_index_monitor(im)

        attribute_selection_set = task.passive_fdtd_index_monitor_option(
            "intensity", im
        )["attributes"]
        if "n" in attribute_selection_set:
            attribute_selection_set = ["n"]
        num_count = len(attribute_selection_set)

        for attr in attribute_selection_set:
            df = task.passive_fdtd_index_monitor_chart(
                "intensity", im, attr, **{i1: "plotX", i2: "plotY"}
            )

            x, y, Z = (
                df.raw_data["horizontal"],
                df.raw_data["vertical"],
                df.raw_data["data"],
            )
            fig, ax = heatmap(x, y, Z)

            ax.set_xlabel(f"{i1} (μm)")
            ax.set_ylabel(f"{i2} (μm)")
            ax.set_title(f"{ptitle}")
            fig.canvas.mpl_connect("button_press_event", self.__on_press)

            def managePng(field):
                if not show:
                    png_name = f"{Path(self.file).name.split('.')[0]}_count{next(mc)}_{field}.png"
                    path = str(savepath)

                    if len(path) == 0:

                        png_path = (
                            (os.path.dirname(self.file) or ".")
                            + "/"
                            + png_name
                        )
                    elif os.path.isdir(path):
                        png_path = os.path.join(path, png_name)
                    else:
                        dirname = os.path.dirname(path)
                        filename = (
                            os.path.basename(path).split(".")[0]
                            + "_"
                            + field
                            + "."
                            + os.path.basename(path).split(".")[1]
                        )

                        png_path = os.path.join(dirname, filename)
                    plt.savefig(png_path, dpi=100, bbox_inches="tight")
                    # except Exception:
                    #     print("please input the correct savepath ")

                elif show:
                    ax = plt.gca()

                    def format_coord(x, y):
                        return "%s=%0.3f, %s=%0.3f" % (i1, x, i2, y)

                    ax.format_coord = format_coord
                    plt.show()

            if grid == "on":
                print("grid not supported")
                # ax.set_xticks(self.xx)
                # ax.set_yticks(self.yy)
                # plt.grid(lw=0.15)
                # plt.xticks(rotation=45)
                # # managePng(fields[i])
                managePng(attr)

            elif grid == "off":
                # managePng(fields[i])
                managePng(attr)

            plt.close()
        return attribute_selection_set

    def __on_press(self, event):
        if event.inaxes:
            pointx = "%.4e" % event.xdata
            pointy = "%.4e" % event.ydata

            devx = [abs(_ - float(pointx)) for _ in self.xx]
            devy = [abs(_ - float(pointy)) for _ in self.yy]
            mindevx = min(devx)
            mindevy = min(devy)
            inx, iny = [0, 0]
            for i, value in enumerate(devx):
                if value == mindevx:
                    inx = i
            for i, value in enumerate(devy):
                if value == mindevy:
                    iny = i
            eps = self.eps[self.indx][inx, iny]
            print((pointx, pointy, eps))

    def rm_files(self, *args, **kwargs):
        pass


# %%Material and Waveform
class Material:
    """A compat class for offline package's ``maxopt_ofl.Material``."""

    @property
    def materials(self):
        return __sdk__().user_materials.all()

    @staticmethod
    def find(name):
        inst = __sdk__()
        return inst.user_materials[name]


class Waveform:
    """A compat class for offline package's ``maxopt_ofl.Waveform``."""

    @property
    def waveforms(self):
        return __sdk__().user_waveforms.all()

    @staticmethod
    def find(name):
        inst = __sdk__()
        return inst.user_waveforms[name]


def init_materials(fp=None, replace=False):
    """A compat method for the offline method with same name.

    Leave relative sentences as is.

    Args:
        fp (str | Path): The file path.

        replace (bool): This parameter will be passed to ensure_material method.

    Returns:
        None
    """

    class FakeMaterialType(CoreMaterial):
        def __init__(self, data):
            self.data = data
            self.name = data.get("name", "unnamed_" + str(uuid4()))

        def to_dict(self):
            return self.data

    if fp:
        with open(fp, "r", encoding="utf-8") as f:
            __sdk__().ensure_materials(
                [FakeMaterialType(_) for _ in json.load(f)],
                "passive",
                replace=replace,
            )


def init_waveforms(fp, replace=False):
    """A compat method for the offline method with same name.

    Leave relative sentences as is.

    Args:
        fp (str | Path): The file path.
        replace (bool): This parameter will be passed to ensure_waveform method.

    Returns:
        None
    """

    class FakeWaveformType(CoreWaveform):
        def __init__(self, data):
            self.__data = data
            self.name = data.get("name", "unnamed_" + str(uuid4()))

        def to_dict(self):
            return self.__data

    with open(fp, "r", encoding="utf-8") as f:
        __sdk__().ensure_waveforms(
            [
                FakeWaveformType(WaveformShell(_).to_dict())
                for _ in json.load(f)
            ],
            replace=replace,
        )


# %% Other
def workspace(self: WhaleClients):
    """A compat property."""
    if not hasattr(self, "__workspace__"):
        template = Config.templates.file.task_yaml_template
        __workspace = Config.templates.format(
            template,
            dict(
                task=self,
                project=self.project,
            ),
            __sdk__().config,
        )

        os.makedirs(Path(__workspace).parent, exist_ok=True)

        self.__workspace__ = __workspace
        Ws = Workspace()
        Ws.main = TinyTaskInfo(self.id, self.__class__)
        Ws.dump(self.__workspace__)
        self.file_dirs.append(self.__workspace__)

    return self.__workspace__


WhaleClients.workspace = property(workspace)


def TaskResult(_, *args, **kwargs):
    """Return the first inputted parameter."""
    return _


def main():
    pass


def json_save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)


from maxoptics.var.models.MitM import ModeExpansion


# from maxoptics.var.models.meta.ModeExpansion import ModeExpansionAttrs

# ModeExpansionAttrs.monitor = property(lambda *_: None)


def mode_expansion_set(self, name, value, *args, **kwargs):
    """Allow ModeExpansion object task append a result monitor like assigning a value."""
    if name == "monitor":
        return self.append_monitor_for_mode_expansion(value)
    else:
        return super(ModeExpansion, self).set(name, value, *args, **kwargs)


ModeExpansion.set = mode_expansion_set

heatmap

# %%
