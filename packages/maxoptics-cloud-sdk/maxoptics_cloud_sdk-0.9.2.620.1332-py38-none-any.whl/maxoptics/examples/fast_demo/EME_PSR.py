import glob
from importlib.resources import path
import json
from matplotlib import pyplot as plt
import os
from pprint import pprint
import time
from pathlib import Path

import maxoptics.maxopt_sdk as sdk
from maxoptics.maxopt_sdk import (
    EME,
    TaskResult,
    json_save,
    passive_eme_fd_result_chart,
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
    plot_path = str(Path(__file__).parent.as_posix()) + '/plots/PSR/'
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)
    # -----------1 eme config
    eme_config_private = {
        'dy'        : grid,
        'dz'        : grid,
        'wavelength': wavelength,
        'name'      : 'EME_PSR'
    }
    eme_config.update(eme_config_private)
    eme = EME(eme_config)
    eme.set_geometry(y=0, z=0.09, y_span=8, z_span=6)
    eme.set_cell_group(
        x_min=-30.5,  # x_min of simulation region, x_max is decided by x_min + sum of cells' span
        cell_group=[
            {
                "cell_num": 1,
                "number_of_modes": number_of_modes,
                "sc": 0,
                "span": 1
            },
            {
                "cell_num": 6,
                "number_of_modes": number_of_modes,
                "sc": 1,
                "span": 6
            },
            {
                "cell_num": 6,
                "number_of_modes": number_of_modes,
                "sc": 1,
                "span": 30
            },
            {
                "cell_num": 6,
                "number_of_modes": number_of_modes,
                "sc": 1,
                "span": 12
            },
            {
                "cell_num": 1,
                "number_of_modes": number_of_modes,
                "sc": 0,
                "span": 8.9
            },
            {
                "cell_num": 40,
                "number_of_modes": number_of_modes,
                "sc": 1,
                "span": 5
            },
            {
                "cell_num": 1,
                "number_of_modes": number_of_modes,
                "sc": 0,
                "span": 5.2
            },
            {
                "cell_num": 1,
                "number_of_modes": number_of_modes,
                "sc": 0,
                "span": 5
            }
        ]
    )

    # --------2.set project and structure     -----------------
    project = sdk.GdsModel(gds_file)
    # project.add_rectangle((0, 0), 6, monitor_w, 0, -0.1, 0.1, Si)     # add
    # rectangle((center_x,center_y),x_span,y_span,rotation_angle,z_min,z_max,material)
    project.gds_import(gds_topcell, (1, 0), SiO2, -4, 0)
    project.gds_import(gds_topcell, (2, 0), Si, 0, 0.22)
    # struct_si = project.gds_import(gds_topcell, (2, 0), Si, 0, 0.22)
    # struct_si["mesh_order"] = 3  # default mesh_order is 2
    # view_index_eme(project=project, eme_config=eme_config, view_axis='x',
    # view_location=25, z_span=6, y_span=6, x_span=0.2)  # source
    eme.add_structure(project.structures)

    # --------3.set waveform and source    -----------------
    portLeft = eme.add('EMEPort')
    portLeft.set_geometry(x=-30.5, y=0, z=0, y_span=2, z_span=2)
    # set ModeSource's mode_selection [0:fundamental mode, 1:fundamental TE mode, 2:fundamental TM mode, 3:user select]
    portLeft['mode_selection'] = 1
    # portLeft['mode_index'] = 1 # mode_index calculatored in mode_selection
    # which rank by refractive index.You don't have to write this when
    # mode_selection is not 'user select'
    eme['source_port'] = portLeft

    # --------4.set monitor    -----------------------------------
    # port_localtion: 0 for left port. port_localtion: 1 for right port. default: 0
    portTM = eme.add('EMEPort', {'port_location': 1})
    portTM.set_geometry(x=42.6, y=2.673, z=0.11, y_span=2, z_span=2)
    portTM['mode_selection'] = 1

    # port_localtion: 0 for left port. port_localtion: 1 for right port. default: 0
    portTE = eme.add('EMEPort', {'port_location': 1})
    portTE.set_geometry(x=42.6, y=0, z=0.11, y_span=2, z_span=2)
    portTE['mode_selection'] = 1

    # port_localtion: 0 for left port. port_localtion: 1 for right port. default: 0
    portTM2 = eme.add('EMEPort', {'port_location': 1})
    portTM2.set_geometry(x=42.6, y=2.673, z=0.11, y_span=2, z_span=2)
    portTM2['mode_selection'] = 2

    # port_localtion: 0 for left port. port_localtion: 1 for right port. default: 0
    portTE2 = eme.add('EMEPort', {'port_location': 1})
    portTE2.set_geometry(x=42.6, y=0, z=0.11, y_span=2, z_span=2)
    portTE2['mode_selection'] = 2

    z_normal = eme.add('ProfileMonitor')
    z_normal['monitor_type'] = 2  # 0:x-normal, 1:y-normal, 2:z-normal
    z_normal['x_resolution'] = 100  # grid numbers in x direction, only works for profile monitor
    z_normal.set_geometry(x=6, y=0, z=0.11, x_span=73, y_span=8)

    project.show(savepath=Path(plot_path), show=False, config=eme)

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
                monitor=portLeft,
                attribute="E",
                operation="ABS",
                taskPath=Path(result.workspace).parent / Path(result.workspace).name),
            # mode= 0, 1, 2, 3. Index of modes users want to check. ranked by refractive from high to low
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
            dict(y="plotX", z="plotY", mode=1),
        )
        tf = TaskResult(df, "intensity")
        x, y, Z = tf.raw_data["horizontal"], tf.raw_data["vertical"], tf.raw_data["data"]
        sdk.heatmap(x, y, Z)
        plt.xlabel("x (μm)")
        plt.ylabel("y (μm)")
        plt.title("source_mode_profile")
        plt.savefig(plot_path + "01_source_modeprofile_fdeonly.jpg")
        plt.clf()
        print('=========================== generated source profile from FDE-only =================================')

    if extract:
        # =============   see results from eme
        if not run:
            result = EmptyClass()
            result.workspace = project_address                                          # for power monitor

        # ========================   see mode profile at output ports
        df = passive_eme_fd_result_chart(
            "intensity",
            dict(
                log=False,
                monitor=z_normal,
                attribute="E",
                operation="ABS",
                taskPath=Path(result.workspace)),
            dict(x='plotX', y='plotY'),
        )
        tf = TaskResult(df, "intensity")
        x, y, Z = tf.raw_data["horizontal"], tf.raw_data["vertical"], tf.raw_data["data"]
        sdk.heatmap(x, y, Z)
        plt.xlabel("x (μm)")
        plt.ylabel("y (μm)")
        plt.title("z_normal profile")
        plt.savefig(plot_path + f"{wavelength}z_normal_eme.jpg")
        plt.clf()

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
        TM_outTE = (tf.DataFrame[0][1])  # column:1, row 2
        TE_outTE = (tf.DataFrame[0][2])  # column:1, row 3
        TM_outTM = (tf.DataFrame[0][3])  # column:1, row 4
        TE_outTM = (tf.DataFrame[0][4])  # column:1, row 5
        print("TM_outTE=", TM_outTE)
        print("TE_outTE=", TE_outTE)
        print("TM_outTM=", TM_outTM)
        print("TE_outTM=", TE_outTM)
        json_save(os.path.join(plot_path, f"{wavelength}TM_outTE.json"), TM_outTE)
        json_save(os.path.join(plot_path, f"{wavelength}TE_outTE.json"), TE_outTE)
        json_save(os.path.join(plot_path, f"{wavelength}TM_outTM.json"), TM_outTM)
        json_save(os.path.join(plot_path, f"{wavelength}TE_outTM.json"), TE_outTM)


if __name__ == '__main__':
    start = time.time()
    # -----------------------------
    path = str(Path(__file__).parent.as_posix())
    gds_file = path + '/gds/' + 'PSR.gds'
    project_address = path + '/project/'
    simulation(extract=True, source_view=False, run=True, gds_file=gds_file, gds_topcell="PSR",
               number_of_modes=10, grid=0.01, wavelength=1.54, project_address=project_address)
    # ----------------------------
    print('\x1b[6;30;42m' + '[Finished in %(t)s mins]' % {'t': round((time.time() - start) / 60, 2)} + '\x1b[0m')
