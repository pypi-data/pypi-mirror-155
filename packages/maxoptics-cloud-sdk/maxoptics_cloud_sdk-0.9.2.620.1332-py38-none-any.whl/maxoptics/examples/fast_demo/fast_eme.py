import glob
from importlib.resources import path
import os
import json
from matplotlib import pyplot as plt
from pprint import pprint
import time
from pathlib import Path

import maxoptics.maxopt_sdk as sdk
from maxoptics.maxopt_sdk import (
    EME,
    TaskResult,
    json_save,
    passive_eme_smatrix_chart,
    passive_source_fde_result_chart,
)

from case_alias import Si, SiO2, view_index_eme, eme_config, EmptyClass


def simulation(
        gds_file,
        gds_topcell,
        project_address,
        wavelength,
        grid,
        number_of_modes,
        run=False,
        source_view=False,
        extract=False):
    # -------general parameter
    port_files = glob.glob(os.path.join(path, 'port*.json'))
    if len(port_files) > 0:
        with open(port_files[0]) as json_file:
            ports = json.load(json_file)
    plot_path = str(Path(__file__).parent.as_posix()) + '/plots/emefast/'
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)
    # -----------1 eme config
    eme_config_private = {
        'dy'        : grid,
        'dz'        : grid,
        'wavelength': wavelength,
        'name'      : 'fast_eme'
    }
    eme_config.update(eme_config_private)
    eme = EME(eme_config)
    eme.set_geometry(y=0, z=0, y_span=3, z_span=3)
    eme.set_cell_group(
        x_min=-1,  # x_min of simulation region, x_max is decided by x_min + sum of cells' span
        cell_group=[
            {
                "cell_num": 3,
                "number_of_modes": number_of_modes,
                "sc": 1,
                "span": 2
            }
        ]
    )
    # --------2.set project and structure     -----------------
    project = sdk.GdsModel(gds_file)
    # project.add_rectangle((0, 0), 6, monitor_w, 0, -0.1, 0.1, Si)["meshorder"] = 1
    # add rectangle((center_x,center_y),x_span,y_span,rotation_angle,z_min,z_max,material)
    project.add_rectangle((0, 0), 2, 2, 0, -0.1, 0.1, Si)
    project.gds_import(gds_topcell, (3, 0), SiO2, 0, 0.1)
    # view_index_eme(project=project, eme_config=eme_config, view_axis='x', view_location=-1, z_span=3, y_span=3, x_span=0.2)  # source
    # view_index_eme(project=project, eme_config=eme_config, view_axis='y', view_location=0, z_span=6, y_span=0.2, x_span=200)  # source
    # view_index_eme(project=project, eme_config=eme_config, view_axis='z',
    # view_location=0.1, z_span=0.2, y_span=6, x_span=206)  # monitorT
    eme.add_structure(project.structures)

    # --------3.set waveform and source     -----------------
    portLeft = eme.add('EMEPort')
    # portLeft.set_geometry(x=-103, x_span=0, y=0, z=0.5, y_span=5.5, z_span=7)
    portLeft.set_geometry(x=-1, y=0, z=0, y_span=3, z_span=3)
    # set ModeSource's mode_selection [0:fundamental mode, 1:fundamental TE mode, 2:fundamental TM mode, 3:user select]
    portLeft['mode_selection'] = 1
    # portLeft['mode_index'] = 1  # mode_index calculatored in mode_selection
    # which rank by refractive index. You don't have to write this when
    # mode_selection is not 'user select'

    # --------4.set monitor    -----------------------------------
    portRight = eme.add('EMEPort', {'port_location': 1})
    # portRight.set_geometry(x=103, x_span=0, y=0, z=0.5, y_span=5.5, z_span=7)
    portRight.set_geometry(x=1, y=0, z=0, y_span=3, z_span=3)
    portRight['mode_selection'] = 1
    eme['source_port'] = portRight
    # y_normal = eme.add('ProfileMonitor')
    # y_normal['monitor_type'] = 1
    # y_normal['x_resolution'] = 400
    # y_normal.set_geometry(x=0, y=0, z=0, x_span=206, z_span=7, y_span=0)

    project.show(savepath=Path(plot_path), show=False, celldisplay=True, config=eme)

    if run:
        start = time.time()
        print('\x1b[6;30;42m' + '-------starting eme now !!!!------------- ' + '\x1b[0m')
        result = eme.run()
        print('\x1b[6;30;42m' + '[Finished in %(t)s mins for eme]' %
              {'t': round((time.time() - start) / 60, 2)} + '\x1b[0m')

    if source_view:
        # =============   jpg mode source, now only after eme
        result = eme.run(only_fde=True)
        df = passive_source_fde_result_chart(
            "intensity",
            dict(
                monitor=portRight,
                attribute="E",
                operation="ABS",
                taskPath=Path(result.workspace).parent / Path(result.workspace).name),
            dict(y="plotX", z="plotY", mode=0),
        )
        tf = TaskResult(df, "intensity")
        x, y, Z = tf.raw_data["horizontal"], tf.raw_data["vertical"], tf.raw_data["data"]
        sdk.heatmap(x, y, Z)
        plt.xlabel("x (μm)")
        plt.ylabel("y (μm)")
        plt.title("source_mode_profile")
        plt.savefig(plot_path + "00_source_modeprofile_fdeonly.jpg")
        plt.clf()

        df = passive_source_fde_result_chart(
            "intensity",
            dict(
                monitor=portLeft,
                attribute="E",
                operation="ABS",
                taskPath=Path(result.workspace).parent / Path(result.workspace).name),
            dict(y="plotX", z="plotY", mode=0),
        )
        tf = TaskResult(df, "intensity")
        x, y, Z = tf.raw_data["horizontal"], tf.raw_data["vertical"], tf.raw_data["data"]
        sdk.heatmap(x, y, Z)
        plt.xlabel("x (μm)")
        plt.ylabel("y (μm)")
        plt.title("source_mode_profile")
        plt.savefig(plot_path + "01_output_modeprofile_fdeonly.jpg")
        plt.clf()

        print('=========================== generated source profile from FDE-only =================================')

    if extract:
        # =============   see results from eme
        if not run:
            result = EmptyClass()
            result.workspace = project_address                                          # for power monitor

        """RESULT - Smatrix"""
        df = passive_eme_smatrix_chart(
            "table",
            dict(
                operation="ABS^2",  # ABS or ABS^2
                taskPath=Path(result.workspace),
            ),
            dict(),
        )

        plt.clf()
        tf = TaskResult(df, "table")
        pprint(tf.raw_data["data"])
        pprint(tf.DataFrame)
        T = (tf.DataFrame[0][1])  # column:1,row 2
        R = (tf.DataFrame[0][0])  # column:1,row 1
        print("Transmission=", T)
        print("Reflection=", R)
        json_save(os.path.join(plot_path, "Transmission.json"), T)
        json_save(os.path.join(plot_path, "Reflection.json"), R)


if __name__ == '__main__':
    start = time.time()
    # -----------------------------
    path = str(Path(__file__).parent.as_posix())
    gds_file = path + '/gds/' + 'fast_test.gds'
    project_address = path + '/project/'
    simulation(
        extract=True,
        source_view=False,
        run=True,
        gds_file=gds_file,
        gds_topcell="EXTEND_1",
        number_of_modes=10,
        grid=0.02,
        wavelength=1.5,
        project_address=project_address)
    # ----------------------------
    print('\x1b[6;30;42m' + '[Finished in %(t)s mins]' % {'t': round((time.time() - start) / 60, 2)} + '\x1b[0m')
