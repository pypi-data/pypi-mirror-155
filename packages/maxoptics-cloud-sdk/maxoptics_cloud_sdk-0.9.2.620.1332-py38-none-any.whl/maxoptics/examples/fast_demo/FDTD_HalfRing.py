import glob
import json
from matplotlib import pyplot as plt
import os
from pathlib import Path
import time

from importlib.resources import path
import maxoptics.maxopt_sdk as sdk
from maxoptics.maxopt_sdk import (
    FDTD,
    TaskResult,
    json_save,
    passive_fdtd_fd_result_chart,
    passive_source_fde_result_chart,
    passive_fdtd_mode_expansion_chart,
)
import seaborn

from case_alias import Si, SiO2, fdtd_config, source_config, view_index_fdtd, EmptyClass


def simulation(
        gds_file,
        gds_topcell,
        project_address,
        run=False,
        source_view=False,
        extract=False,
        grids_per_lambda=15):
    # -------general parameter
    monitor_w = 3
    monitor_h = 2
    port_files = glob.glob(os.path.join(path, 'port*.json'))
    if len(port_files) > 0:
        with open(port_files[0]) as json_file:
            ports = json.load(json_file)
    plot_path = str(Path(__file__).parent.as_posix()) + '/plots/HalfRing/'
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)
    # -----------1. FDTD config
    fdtd_config_private = {
        'x'                   : 0,
        'y'                   : 0,
        'z'                   : 0,
        'x_span'              : 11,
        'y_span'              : 12,
        'z_span'              : 8,
        'cells_per_wavelength': grids_per_lambda,  # set FDTD's cells_per_wavelength = 2 + LumMesh*4
        'name'                : 'FDTD_HalfRing'
    }
    fdtd_config.update(fdtd_config_private)
    fdtd = FDTD(fdtd_config)
    fdtd.set_geometry(**fdtd_config)

    # --------2.set project and structure     -----------------
    project = sdk.GdsModel(gds_file)
    # project.add_rectangle((0, 0), 6, monitor_w, 0, -0.1, 0.1, Si)     # add
    # rectangle((center_x,center_y),x_span,y_span,rotation_angle,z_min,z_max,material)
    project.gds_import(gds_topcell, (1, 0), SiO2, -4, 0)
    project.gds_import(gds_topcell, (2, 0), Si, 0, 0.18)
    view_index_fdtd(
        project=project,
        fdtd_config=fdtd_config,
        view_axis='x',
        plot_path=plot_path,
        view_location=-4,
        z_span=3,
        y_span=12,
        x_span=0.2)  # source
    # view_index_fdtd(project=project, fdtd_config=fdtd_config, view_axis='x',
    # view_location=ports['op_1']['position'][0], z_span=monitor_h,
    # y_span=monitor_w, x_span=0.2)  # monitorT
    fdtd.add_structure(project.structures)

    # --------3.set waveform and source     -----------------
    sdk.init_waveforms('./case_waveforms.json')
    waveform = sdk.Waveform.find('Waveform_1550_100')
    source_config_private = {
        'x'     : -4,
        'y'     : 3.6,
        'z'     : 0,
        'x_span': 0,
        'y_span': monitor_w,
        'z_span': monitor_h
    }
    source_config.update(source_config_private)
    source_config["waveform_id"] = waveform.id
    src = fdtd.add("ModeSource", source_config)
    src.set_geometry(**source_config)
    fdtd.add("GlobalMonitor", {
        "frequency_points" : 11,
        "wavelength_center": waveform.data['center_wavelength'],
        "wavelength_span"  : waveform.data['wavelength_span']}
    )
    fdtd.update(waveforms=[waveform])

    # --------4.set monitor    -----------------------------------

    z_normal = {
        'x'                     : fdtd_config["x"],
        'y'                     : fdtd_config["y"],
        'z'                     : fdtd_config["z"],
        'x_span'                : fdtd_config["x_span"],
        'y_span'                : fdtd_config["y_span"],
        'z_span'                : 0,
        'use_wavelength_spacing': 1,  # use wavelength_spacing [1:on, 0:off]
        'use_source_limits'     : 0,  # source_limits [1:on, 0:off]
        'frequency_points'      : 3,
        "wavelength_center"     : waveform.data['center_wavelength'],
        "wavelength_span"       : waveform.data['wavelength_span'],
        "spacing_type"          : 0,  # [0:wavelength, 1:frequency]
        "spacing_limit"         : 0   # [0:min/max, 1:center/span]
    }
    monitor_T = {
        'x'                     : 4,
        'y'                     : 3.6,
        'z'                     : 0.09,
        'x_span'                : 0,
        'y_span'                : monitor_w,
        'z_span'                : monitor_h,
        'use_wavelength_spacing': 1,  # use wavelength_spacing [1:on, 0:off]
        'use_source_limits'     : 0,  # source_limits [1:on, 0:off]
        "spacing_type"          : 0,  # [0:wavelength, 1:frequency]
        "spacing_limit"         : 0,  # [0:min/max, 1:center/span]
        "mode_expansion"        : {"mode_list": [1, 2, 3, 4]}
    }
    monitor_C = {
        'x'                     : 3.1,
        'y'                     : -3,
        'z'                     : 0.09,
        'x_span'                : monitor_w,
        'y_span'                : 0,
        'z_span'                : monitor_h,
        'use_wavelength_spacing': 1,  # use wavelength_spacing [1:on, 0:off]
        'use_source_limits'     : 0,  # source_limits [1:on, 0:off]
        "spacing_type"          : 0,  # [0:wavelength, 1:frequency]
        "spacing_limit"         : 0,  # [0:min/max, 1:center/span]
        "mode_expansion"        : {"mode_list": [1, 2, 3, 4]}
    }
    monitor_R = {
        'x'                     : -4.21,
        'y'                     : 3.6,
        'z'                     : 0.09,
        'x_span'                : 0,
        'y_span'                : monitor_w,
        'z_span'                : monitor_h,
        'use_wavelength_spacing': 1,  # use wavelength_spacing [1:on, 0:off]
        'use_source_limits'     : 0,  # source_limits [1:on, 0:off]
        "spacing_type"          : 0,  # [0:wavelength, 1:frequency]
        "spacing_limit"         : 0,  # [0:min/max, 1:center/span]
        "mode_expansion"        : {"mode_list": [1, 2, 3, 4]}
    }

    z_normal_mon = fdtd.add("PowerMonitor", z_normal)
    z_normal_mon.set_geometry(**z_normal)

    monitor_T_mon = fdtd.add("PowerMonitor", monitor_T)
    monitor_T_mon.set_geometry(**monitor_T)

    monitor_C_mon = fdtd.add("PowerMonitor", monitor_C)
    monitor_C_mon.set_geometry(**monitor_C)

    monitor_R_mon = fdtd.add("PowerMonitor", monitor_R)
    monitor_R_mon.set_geometry(**monitor_R)

    project.show(savepath=Path(plot_path), show=False, config=fdtd)

    if run:
        start = time.time()
        print('\x1b[6;30;42m' + '-------starting FDTD now !!!!------------- ' + '\x1b[0m')
        result = fdtd.run()
        fdtd.run_mode_expansion(fdtd_path=result.workspace)             # for mode monitor
        print('\x1b[6;30;42m' + '[Finished in %(t)s mins for FDTD]' %
              {'t': round((time.time() - start) / 60, 2)} + '\x1b[0m')

    if source_view:
        # =============   jpg mode source, now only after FDTD
        result = fdtd.run(only_fde=True)
        df = passive_source_fde_result_chart("intensity",
                                             dict(monitor=src,
                                                  attribute="E",
                                                  operation="ABS",
                                                  taskPath=Path(result.workspace).parent / Path(result.workspace).name),
                                             dict(x=0,
                                                  y="plotX",
                                                  z="plotY",
                                                  mode=0),
                                             )
        tf = TaskResult(df, "intensity")
        x, y, Z = tf.raw_data["horizontal"], tf.raw_data["vertical"], tf.raw_data["data"]
        sdk.heatmap(x, y, Z)
        plt.xlabel("x (μm)")
        plt.ylabel("y (μm)")
        plt.title("source_mode_profile")
        plt.savefig(plot_path + "00_source_modeprofile_fdeonly.jpg")
        plt.clf()
        print('=========================== generated source profile from FDE-only =================================')

    if extract:
        # =============   see results from FDTD
        if not run:
            result = EmptyClass()
            result.workspace = project_address                                          # for power monitor

        df = passive_fdtd_fd_result_chart("line",
                                          dict(log=False,
                                               monitor=monitor_T_mon,
                                               attribute="T",
                                               operation="Real",
                                               taskPath=Path(result.workspace)),
                                          dict(wavelength="plotX"),
                                          )
        tf = TaskResult(df, "line")
        # --------
        # seaborn.lineplot(x=tf.DataFrame.index, y=10 * np.log10(tf.DataFrame['data'].values), markers=True)
        seaborn.lineplot(data=tf.DataFrame)
        plt.xlabel("wavelength (μm)")
        plt.ylabel("Transmission_Through")
        plt.title("Through_mon Real(T) line")
        plt.savefig(plot_path + "02_Trans_ThroughVsLambda_power.jpg")
        plt.clf()
        json_save(os.path.join(plot_path, "hfr_Through009.json"), tf.raw_data)  # save data as .json file

        df = passive_fdtd_mode_expansion_chart("line",
                                               dict(log=False,
                                                    monitor=monitor_T_mon,
                                                    attribute="t_forward",
                                                    operation="Real",
                                                    taskPath=Path(result.workspace)),
                                               dict(mode="1",
                                                    wavelength="plotX")
                                               )
        tf = TaskResult(df, "line")
        # --------
        seaborn.lineplot(data=tf.DataFrame)
        # seaborn.lineplot(x=tf.DataFrame.index, y=10 * np.log10(tf.DataFrame['data'].values), markers=True)
        plt.xlabel("wavelength (μm)")
        plt.ylabel("Transmission Forward")
        plt.title("Through_mon Real(t_forward) line")
        plt.savefig(plot_path + "021_ME_ThroughVsLambda_mode.jpg")
        plt.clf()
        json_save(os.path.join(plot_path, "hfr_ME_Through.json"), tf.raw_data)  # save data as .json file

        df = passive_fdtd_fd_result_chart("line",
                                          dict(log=False,
                                               monitor=monitor_C_mon,
                                               attribute="T",
                                               operation="Real",
                                               taskPath=Path(result.workspace)),
                                          dict(wavelength="plotX"),
                                          )
        tf = TaskResult(df, "line")
        # ---------
        # seaborn.lineplot(x=tf.DataFrame.index, y=10 * np.log10(-tf.DataFrame['data'].values), markers=True)
        seaborn.lineplot(data=-tf.DataFrame)
        plt.xlabel("wavelength (μm)")
        plt.ylabel("Transmission_Cross")
        plt.title("Cross_mon Real(T) line")
        plt.savefig(plot_path + "03_Trans_CrossVsLambda_power.jpg")
        plt.clf()
        json_save(os.path.join(plot_path, "hfr_Cross009.json"), tf.raw_data)  # save data as .json file

        df = passive_fdtd_mode_expansion_chart("line",
                                               dict(log=False,
                                                    monitor=monitor_C_mon,
                                                    attribute="t_backward",
                                                    operation="Real",
                                                    taskPath=Path(result.workspace)),
                                               dict(mode="1", wavelength="plotX")
                                               )
        tf = TaskResult(df, "line")
        # # --------
        seaborn.lineplot(data=tf.DataFrame)
        # seaborn.lineplot(x=tf.DataFrame.index, y=10 * np.log10(tf.DataFrame['data'].values), markers=True)
        plt.xlabel("wavelength (μm)")
        plt.ylabel("Transmission Backward")
        plt.title("Cross_mon Real(t_backward) line")
        plt.savefig(plot_path + "031_ME_CrossVsLambda_mode.jpg")
        plt.clf()
        json_save(os.path.join(plot_path, "hfr_ME_cross.json"), tf.raw_data)  # save data as .json file

        # ========================   jpg Return loss, power monitor
        df = passive_fdtd_fd_result_chart("line",
                                          dict(log=False,
                                               monitor=monitor_R_mon,
                                               attribute="T",
                                               operation="Real",
                                               taskPath=Path(result.workspace)),
                                          dict(wavelength="plotX"),
                                          )
        tf = TaskResult(df, "line")
        # ---------
        # seaborn.lineplot(x=tf.DataFrame.index, y=10 * np.log10(-tf.DataFrame['data'].values), markers=True)
        seaborn.lineplot(data=-tf.DataFrame)
        plt.xlabel("wavelength (μm)")
        plt.ylabel("Reflection")
        plt.title("Rel_mon Real(T) line")
        plt.savefig(plot_path + "04_ReflVsLambda_power.jpg")
        plt.clf()
        json_save(os.path.join(plot_path, "hfr_Refl009.json"), tf.raw_data)  # save data as .json file

        df = passive_fdtd_mode_expansion_chart("line",
                                               dict(log=False,
                                                    monitor=monitor_R_mon,
                                                    attribute="t_backward",
                                                    operation="ABS",
                                                    taskPath=Path(result.workspace)),
                                               dict(mode="1",
                                                    wavelength="plotX")
                                               )
        tf = TaskResult(df, "line")
        # --------
        seaborn.lineplot(data=tf.DataFrame)
        # seaborn.lineplot(x=tf.DataFrame.index, y=10 * np.log10(tf.DataFrame['data'].values), markers=True)
        plt.xlabel("wavelength (μm)")
        plt.ylabel("Transmission Backward")
        plt.title("Rel_mon ABS(t_backward) lien")
        plt.savefig(plot_path + "041_ME_ReflVsLambda_mode.jpg")
        plt.clf()
        json_save(os.path.join(plot_path, "hfr_ME_Refl.json"), tf.raw_data)  # save data as .json file


if __name__ == '__main__':
    start = time.time()
    # -----------------------------
    path = str(Path(__file__).parent.as_posix())
    gds_file = path + '/gds/' + 'hfr.gds'
    project_address = path + '/project/'
    simulation(extract=True, source_view=False, run=True,
               gds_file=gds_file, gds_topcell="HalfRing", grids_per_lambda=15, project_address=project_address)
    print('\x1b[6;30;42m' + '[Finished in %(t)s mins]' % {'t': round((time.time() - start) / 60, 2)} + '\x1b[0m')
