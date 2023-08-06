import json
import os
import time
from pathlib import Path
import maxoptics.maxopt_sdk as sdk
from matplotlib import pyplot as plt
import maxoptics
from maxoptics.core import heatmap, lineplot
from maxoptics.macros import X_Normal, Y_Normal, Z_Normal

client = maxoptics.MosLibraryCloud()

SiO2 = client.public_materials["SiO2 (Glass) - Palik"]
Si = client.public_materials["Si (Silicon) - Palik"]


def json_save(path, data):
    with open(path, "w") as f:
        json.dump(data, f)


def simulation(project_name, run_parameter_sweep=False, source_view=False, extract=False,
               mesh_type=0, grids_per_lambda=6):
    # <editor-folder desc="--- 0. general parameter ---">
    gapConfig = {"start": 0.1, "stop": 0.3, "points": 3}
    plotPath = str(Path(__file__).parent.as_posix()) + "/plots/FDTD_HALFRING_PARAMETER_SWEEP/"
    meshPath = plotPath + "mesh"
    if not os.path.exists(plotPath):
        os.makedirs(plotPath)
    if not os.path.exists(meshPath):
        os.makedirs(meshPath)
    # </editor-folder>

    # <editor-folder desc="--- 1. create project & FDTD ---">
    # <editor-folder desc="--- 1.1 project---">
    project = client.create_project_as(project_name)

    # set global param
    project.DOCUMENT.append_global_param("wg_width", "", 0.4, "waveguide width")
    project.DOCUMENT.append_global_param("wg_height", "", 0.18, "waveguide height")
    project.DOCUMENT.append_global_param("gap", "", 0.1, "coupler gap")
    project.DOCUMENT.append_global_param("r_inner", "", 2.9, "ring inner radius")
    project.DOCUMENT.append_global_param("r_outer", "r_inner+wg_width", 3.3, "ring outer radius")
    project.DOCUMENT.append_global_param("in_y", "r_inner+wg_width*3/2+gap", 3.6, "injection waveguide Y position")
    project.DOCUMENT.append_global_param("out_x", "r_inner+wg_width/2", 3.1, "cross output waveguide X position")
    project.DOCUMENT.append_global_param("sour_x", "-(r_outer)-0.7", -4, "mode source X position")
    project.DOCUMENT.append_global_param("in_x_span", "-2*(sour_x)+3", 11, "injection waveguide X length")
    project.DOCUMENT.append_global_param("out_y_span", "", 6, "cross output waveguide Y length")
    project.DOCUMENT.append_global_param("y_min", "-out_y_span", -6, "full region Y min")
    project.DOCUMENT.append_global_param("y_max", "in_y+2.4", 6, "full region Y max")
    project.DOCUMENT.append_global_param("y_center", "((y_min)+(y_max))/2", 0, "full region Y center")
    project.DOCUMENT.append_global_param("y_span_full", "y_max-(y_min)", 12, "full region Y span")
    project.DOCUMENT.append_global_param("sub_height", "", 4, "substrate height")
    project.DOCUMENT.append_global_param("sour_width", "", 3, "source and monitor width")
    project.DOCUMENT.append_global_param("sour_height", "", 2, "source and monitor height")
    project.DOCUMENT.append_global_param("pos_ratio", "", 0, "index monitor position ratio")
    # </editor-folder>

    # <editor-folder desc="--- 1.2 FDTD ---">
    fdtd_config = {"simulation_time"     : 10000,
                   "background_material" : client.public_materials["Air"],
                   "x"                   : 0,
                   "y"                   : 0,
                   "z"                   : 0,
                   "x_span"              : 11,
                   "y_span"              : 12,
                   "z_span"              : 8,
                   "refinement_type"     : mesh_type,
                   "cells_per_wavelength": grids_per_lambda}
    fdtd = project.create_fdtd(**fdtd_config)

    fdtdAttrs = fdtd.attrs
    fdtdAttrs.__expre__.x_span = "in_x_span"
    fdtdAttrs.__expre__.y = "y_center"
    fdtdAttrs.__expre__.y_span = "y_span_full"
    fdtdAttrs.__expre__.y_min = "y_min"
    fdtdAttrs.__expre__.y_max = "y_max"
    # </editor-folder>
    # </editor-folder>

    # <editor-folder desc="--- 2. structure ---">
    # <editor-folder desc="--- 2.1 sub ---">
    sub = project.create_rectangle(name="sub",
                                   x=0,
                                   x_span=11,
                                   y=0,
                                   y_span=12,
                                   z=-2,
                                   z_span=4,
                                   materialId=client.public_materials["SiO2 (Glass) - Palik"],
                                   overrideMeshOrder=1,  # [0:use material mesh order,1:set mesh order by user]
                                   meshOrder=1
                                   )
    subAttrs = sub.attrs
    subAttrs.__expre__.x_span = "in_x_span"
    subAttrs.__expre__.y = "y_center"
    subAttrs.__expre__.y_span = "y_span_full"
    subAttrs.__expre__.y_min = "y_min"
    subAttrs.__expre__.y_max = "y_max"
    subAttrs.__expre__.z = "-(sub_height)/2"
    subAttrs.__expre__.z_span = "sub_height"
    subAttrs.__expre__.z_span = "sub_height"
    # </editor-folder>

    # <editor-folder desc="--- 2.2 in ---">
    wgIn = project.create_rectangle(name="in",
                                    x=0,
                                    x_span=11,
                                    y=3.6,
                                    y_span=0.4,
                                    z=0.09,
                                    z_span=0.18,
                                    materialId=client.public_materials["Si (Silicon) - Palik"],
                                    overrideMeshOrder=1,  # [0:use material mesh order,1:set mesh order by user]
                                    meshOrder=2
                                    )
    wgInAttrs = wgIn.attrs
    wgInAttrs.__expre__.x_span = "in_x_span"
    wgInAttrs.__expre__.y = "in_y"
    wgInAttrs.__expre__.y_span = "wg_width"
    wgInAttrs.__expre__.z = "wg_height/2"
    wgInAttrs.__expre__.z_span = "wg_height"
    # </editor-folder>

    # <editor-folder desc="--- 2.3 halfRing ---">
    halfRing = project.create_arc_waveguide(name="half_ring",
                                            x=0,
                                            y=0,
                                            z=0,
                                            z_span=0.18,
                                            innerRadius=2.9,
                                            outerRadius=3.3,
                                            angle=180,
                                            rotate_z=180,
                                            materialId=client.public_materials["Si (Silicon) - Palik"],
                                            overrideMeshOrder=1,  # [0:use material mesh order,1:set mesh order by user]
                                            meshOrder=2
                                            )
    halfRingAttrs = halfRing.attrs
    halfRingAttrs.__expre__.z = "wg_height/2"
    halfRingAttrs.__expre__.z_span = "wg_height"
    halfRingAttrs.__expre__.innerRadius = "r_inner"
    halfRingAttrs.__expre__.outerRadius = "r_outer"
    # </editor-folder>

    # <editor-folder desc="--- 2.4 outLeft ---">
    outLeft = project.create_rectangle(name="out_left",
                                       x=-3.1,
                                       x_span=0.4,
                                       y=-3,
                                       y_span=6,
                                       z=0.09,
                                       z_span=0.18,
                                       materialId=client.public_materials["Si (Silicon) - Palik"],
                                       overrideMeshOrder=1,  # [0:use material mesh order,1:set mesh order by user]
                                       meshOrder=2
                                       )
    outLeftAttrs = outLeft.attrs
    outLeftAttrs.__expre__.x = "-out_x"
    outLeftAttrs.__expre__.x_span = "wg_width"
    outLeftAttrs.__expre__.y = "-out_y_span/2"
    outLeftAttrs.__expre__.y_span = "out_y_span"
    outLeftAttrs.__expre__.z = "wg_height/2"
    outLeftAttrs.__expre__.z_span = "wg_height"
    # </editor-folder>

    # <editor-folder desc="--- 2.5 outRight ---">
    outRight = project.create_rectangle(name="out_right",
                                        x=3.1,
                                        x_span=0.4,
                                        y=-3,
                                        y_span=6,
                                        z=0.09,
                                        z_span=0.18,
                                        materialId=client.public_materials["Si (Silicon) - Palik"],
                                        overrideMeshOrder=1,  # [0:use material mesh order,1:set mesh order by user]
                                        meshOrder=2
                                        )
    outRightAttrs = outRight.attrs
    outRightAttrs.__expre__.x = "out_x"
    outRightAttrs.__expre__.x_span = "wg_width"
    outRightAttrs.__expre__.y = "-out_y_span/2"
    outRightAttrs.__expre__.y_span = "out_y_span"
    outRightAttrs.__expre__.z = "wg_height/2"
    outRightAttrs.__expre__.z_span = "wg_height"
    # </editor-folder>
    # </editor-folder>

    # <editor-folder desc="--- 3 modeSource ---">
    sdk.init_waveforms('./case_waveforms.json')
    waveform = sdk.Waveform.find('Waveform_1550_100')

    modeSource = project.create_mode_source(name="mode_source",
                                            injection_axis=0,  # [0:X-Axis,1:Y-Axis,2:Z-Axis]
                                            direction=0,  # [0:Forward,1:Backward]
                                            mode_selection=3,
                                            # [0:Fundamental Mode, 1:Fundamental TE Mode, 2:Fundamental TM Mode, 3:User Select, 4:User Import]
                                            mode_index=1,
                                            waveform_id=waveform["id"],
                                            x=-4,
                                            x_span=0,
                                            y=3.6,
                                            y_span=3,
                                            z=0,
                                            z_span=2
                                            )
    # </editor-folder>

    # <editor-folder desc="--- 4. set monitor ---">
    # <editor-folder desc="--- 4.1 global monitor ---">
    globalMonitorConfig = {"use_wavelength_spacing": 1,  # use wavelength_spacing [1:on, 0:off]
                           "use_source_limits": 0,  # source_limits [1:on, 0:off]
                           "spacing_type": 0,  # [0:wavelength, 1:frequency]
                           "spacing_limit": 0,  # [0:min/max, 1:center/span]
                           "wavelength_min": 1.5,
                           "wavelength_max": 1.6,
                           "frequency_points": 5,
                           }
    project.create_global_monitor(**globalMonitorConfig)
    # </editor-folder>

    # <editor-folder desc="--- 4.2 power monitor ---">
    # <editor-folder desc="--- 4.2.1 zNormal ---">
    monitorZNormalConfig = {"name": "z_normal",
                            "monitor_type": Z_Normal,
                            "x": 0,
                            "y": 0,
                            "z": 0.09,
                            "x_span": 11,
                            "y_span": 12,
                            "z_span": 0,
                            "override_global_options": 1,  # [1:override, 0:not override] [default:1]
                            "use_wavelength_spacing": 1,  # use wavelength_spacing [1:on, 0:off]
                            "use_source_limits": 0,  # source_limits [1:on, 0:off]
                            "spacing_type": 0,  # [0:wavelength, 1:frequency]
                            "spacing_limit": 1,  # [0:min/max, 1:center/span]
                            "wavelength_center": waveform["data"]["center_wavelength"],
                            "wavelength_span": waveform["data"]["wavelength_span"],
                            "frequency_points": 3,
                            }

    monitorZNormal = project.create_power_monitor(**monitorZNormalConfig)
    monitorZNormalAttrs = monitorZNormal.attrs
    monitorZNormalAttrs.__expre__.x_span = "in_x_span"
    monitorZNormalAttrs.__expre__.y = "y_center"
    monitorZNormalAttrs.__expre__.y_span = "y_span_full"
    monitorZNormalAttrs.__expre__.z_span = "wg_height/2"
    # </editor-folder>

    # <editor-folder desc="--- 4.2.2 through ---">
    monitorThroughConfig = {"name"                   : "through",
                            "monitor_type"           : X_Normal,
                            "x"                      : 4,
                            "y"                      : 3.6,
                            "z"                      : 0.09,
                            "x_span"                 : 0,
                            "y_span"                 : 3,
                            "z_span"                 : 2,
                            "override_global_options": 1,  # [1:override, 0:not override] [default:1]
                            "use_wavelength_spacing" : 1,  # use wavelength_spacing [1:on, 0:off]
                            "use_source_limits"      : 0,  # source_limits [1:on, 0:off]
                            "spacing_type"           : 0,  # [0:wavelength, 1:frequency]
                            "spacing_limit"          : 0,  # [0:min/max, 1:center/span]
                            "wavelength_center"      : waveform["data"]["center_wavelength"],
                            "wavelength_span"        : waveform["data"]["wavelength_span"],
                            "frequency_points"       : 101
                            }

    monitorThrough = project.create_power_monitor(**monitorThroughConfig)
    monitorThroughAttrs = monitorThrough.attrs
    monitorThroughAttrs.__expre__.x = "-(sour_x)"
    monitorThroughAttrs.__expre__.y = "in_y"
    monitorThroughAttrs.__expre__.y_span = "sour_width"
    monitorThroughAttrs.__expre__.z_span = "sour_height"
    # </editor-folder>

    # <editor-folder desc="--- 4.2.3 cross ---">
    monitorCrossConfig = {"name"                   : "cross",
                          "monitor_type"           : Y_Normal,
                          "x"                      : 3.1,
                          "y"                      : -3,
                          "z"                      : 0.09,
                          "x_span"                 : 3,
                          "y_span"                 : 0,
                          "z_span"                 : 2,
                          "override_global_options": 0  # [1:override, 0:not override] [default:1]
                          }

    monitorCross = project.create_power_monitor(**monitorCrossConfig)
    monitorCrossAttrs = monitorCross.attrs
    monitorCrossAttrs.__expre__.x = "out_x"
    monitorCrossAttrs.__expre__.x_span = "sour_width"
    monitorCrossAttrs.__expre__.y = "-out_y_span/2"
    monitorCrossAttrs.__expre__.z_span = "sour_height"
    # </editor-folder>

    # <editor-folder desc="--- 4.2.4 reflection ---">
    monitorReflectionConfig = {"name"                   : "reflection",
                               "monitor_type"           : X_Normal,
                               "x"                      : -4.2,
                               "y"                      : 3.6,
                               "z"                      : 0.09,
                               "x_span"                 : 0,
                               "y_span"                 : 3,
                               "z_span"                 : 2,
                               "override_global_options": 1,  # [1:override, 0:not override] [default:1]
                               "use_wavelength_spacing" : 1,  # use wavelength_spacing [1:on, 0:off]
                               "use_source_limits"      : 0,  # source_limits [1:on, 0:off]
                               "spacing_type"           : 0,  # [0:wavelength, 1:frequency]
                               "spacing_limit"          : 0,  # [0:min/max, 1:center/span]
                               "wavelength_center"      : waveform["data"]["center_wavelength"],
                               "wavelength_span"        : waveform["data"]["wavelength_span"],
                               "frequency_points"       : 101
                               }

    monitorReflection = project.create_power_monitor(**monitorReflectionConfig)
    monitorReflectionAttrs = monitorReflection.attrs
    monitorReflectionAttrs.__expre__.x = "(sour_x)-0.2"
    monitorReflectionAttrs.__expre__.y = "in_y"
    monitorReflectionAttrs.__expre__.y_span = "sour_width"
    monitorReflectionAttrs.__expre__.z = "wg_height/2"
    monitorReflectionAttrs.__expre__.z_span = "sour_height"
    # </editor-folder>
    # </editor-folder>

    # <editor-folder desc="--- 4.3 index monitor ---">
    # </editor-folder>

    # <editor-folder desc="--- 5. see mode source result ---">
    if source_view:
        start = time.time()
        print("\x1b[6;30;42m" + "--- starting calculate modes now !!!! ---" + "\x1b[0m")
        modeSourceResult = project.run_calculate_modes(modeSource)
        modeSourceData = modeSourceResult.passive_fde_result_chart(target="intensity",
                                                                   attribute="E",
                                                                   operation="ABS",
                                                                   x=0,
                                                                   plotX="y",
                                                                   plotY="z",
                                                                   mode=0
                                                                   )
        x, y, Z = modeSourceData.raw_data["horizontal"], modeSourceData.raw_data["vertical"], \
            modeSourceData.raw_data["data"]
        heatmap(x, y, Z)
        plt.xlabel("y (μm)")
        plt.ylabel("z (μm)")
        plt.title("source_mode_profile")
        plt.savefig(plotPath + "00_source_modeprofile_fdeonly.jpg")
        plt.close()
        stop = time.time()
        print("\x1b[6;30;42m" + "[Finished in %(t)s mins for calculate modes]" %
              {"t": round((stop - start) / 60, 2)} + "\x1b[0m")
    # </editor-folder>

    # <editor-folder desc="--- 6. run_parameter_sweep ---">
    if run_parameter_sweep:
        start = time.time()
        print("\x1b[6;30;42m" + "--- starting FDTD PARAMETER SWEEP now !!!! ---" + "\x1b[0m")

        # create sweep
        fdtdSweep = project.create_sweep()

        # add sweep parameter(name,start_value,stop_value,points number)
        fdtdSweep.append_param_data("gap", gapConfig["start"], gapConfig["stop"], gapConfig["points"])

        # add sweep monitor
        fdtdSweep.append_result_monitor("through_t", monitorThrough, "T")

        # save project
        project.save()

        # run fdtd parameter sweep
        fdtdSweepResult = project.run_fdtd_parameter_sweep()

        stop = time.time()
        print("\x1b[6;30;42m" + "[Finished in %(t)s mins for FDTD PARAMETER SWEEP]" %
              {"t": round((stop - start) / 60, 2)} + "\x1b[0m")
    # </editor-folder>

    # <editor-folder desc="--- 7. see results ---">
    if run_parameter_sweep and extract:
        x = []
        y = []
        gap_c = [0.1, 0.2, 0.3]
        marker = ['*', '.', '+']
        label = ['0.1', '0.2', '0.3']
        color = ['red', 'blue', 'yellow']
        j = 0

        # get sweep result for each gap_c
        for j in range(len(gap_c)):
            t_param = fdtdSweepResult.passive_fdtd_sweep_chart(
                "line",
                attribute="T",
                operation="ABS",
                plotX="wavelength",
                x=0,
                y=0,
                z=0,
                sweep_gap=j,
                monitor=monitorThrough)
            x = t_param.raw_data['horizontal']
            y = t_param.raw_data['data'][0]
            plt.plot(x, y, color=color[j], marker=marker[j], label=label[j])

        plt.xlabel("wavelength")
        plt.ylabel("transmission")
        plt.title("halfring transmission")
        plt.legend()
        plt.savefig(plotPath + "11_parameter_sweep_gap_result.jpg")
        plt.close()

        for i in range(gapConfig["points"]):
            # <editor-folder desc="--- 7.1 z_normal ---">
            monitorZNormalData = fdtdSweepResult.passive_fdtd_sweep_result_chart_new(target="intensity",
                                                                                     monitor=monitorZNormal,
                                                                                     attribute="E",
                                                                                     operation="ABS",
                                                                                     plotX="x",
                                                                                     plotY="y",
                                                                                     z=0,
                                                                                     wavelength=0,
                                                                                     sweep_gap=i,
                                                                                     )
            x, y, Z = monitorZNormalData.raw_data["horizontal"], monitorZNormalData.raw_data["vertical"], \
                monitorZNormalData.raw_data["data"]
            heatmap(x, y, Z)
            plt.xlabel("x (μm)")
            plt.ylabel("y (μm)")
            plt.title("znormal_mon wavelength=0_ABS(E)_intensity gap_" + str(i))
            plt.savefig(plotPath + "21_zNormal_abs(E)_" + str(i) + ".jpg")
            plt.close()
            json_save(os.path.join(plotPath, "21_zNormal_abs(E)_" + str(i) + ".json"),
                      monitorZNormalData.raw_data
                      )
            # </editor-folder>

            # <editor-folder desc="--- 7.2 through ---">
            # <editor-folder desc="--- 7.2.1 through_line ---">
            monitorThroughData = fdtdSweepResult.passive_fdtd_sweep_result_chart_new(target="line",
                                                                                     monitor=monitorThrough,
                                                                                     attribute="T",
                                                                                     operation="ABS",
                                                                                     x=0,
                                                                                     y=0,
                                                                                     z=0,
                                                                                     plotX="wavelength",
                                                                                     sweep_gap=i
                                                                                     )
            lineplot(monitorThroughData.DataFrame)
            plt.xlabel("wavelength (μm)")
            plt.ylabel("Transmission_Through")
            plt.title("through_mon ABS(T)_line gap_" + str(i))
            plt.savefig(plotPath + "22_through_abs(T)_" + str(i) + ".jpg")
            plt.close()
            json_save(os.path.join(plotPath, "22_through_abs(T)_" + str(i) + ".json"),
                      monitorThroughData.raw_data
                      )
            # </editor-folder>

            # <editor-folder desc="--- 7.2.2 through_intensity ---">
            monitorThroughData = fdtdSweepResult.passive_fdtd_sweep_result_chart_new(target="intensity",
                                                                                     monitor=monitorThrough,
                                                                                     attribute="E",
                                                                                     operation="ABS",
                                                                                     x=0,
                                                                                     plotX="y",
                                                                                     plotY="z",
                                                                                     wavelength=0,
                                                                                     sweep_gap=i,
                                                                                     )
            x, y, Z = monitorThroughData.raw_data["horizontal"], monitorThroughData.raw_data["vertical"], \
                monitorThroughData.raw_data["data"]
            heatmap(x, y, Z)
            plt.xlabel("y (μm)")
            plt.ylabel("z (μm)")
            plt.title("through_mon wavelength=0_ABS(E)_intensity gap_" + str(i))
            plt.savefig(plotPath + "22_through_abs(E)_" + str(i) + ".jpg")
            plt.close()
            json_save(os.path.join(plotPath, "22_through_abs(E)_" + str(i) + ".json"),
                      monitorThroughData.raw_data
                      )
            # </editor-folder>
            # </editor-folder>

            # <editor-folder desc="--- 7.3 cross ---">
            # <editor-folder desc="--- 7.3.1 cross_line ---">
            monitorCrossData = fdtdSweepResult.passive_fdtd_sweep_result_chart_new(target="line",
                                                                                   monitor=monitorCross,
                                                                                   attribute="T",
                                                                                   operation="ABS",
                                                                                   x=0,
                                                                                   y=0,
                                                                                   z=0,
                                                                                   plotX="wavelength",
                                                                                   sweep_gap=i
                                                                                   )
            lineplot(monitorCrossData.DataFrame)
            plt.xlabel("wavelength (μm)")
            plt.ylabel("Transmission_Cross")
            plt.title("cross_mon ABS(T)_line gap_" + str(i))
            plt.savefig(plotPath + "23_cross_abs(T)_" + str(i) + ".jpg")
            plt.close()
            json_save(os.path.join(plotPath, "23_cross_abs(T)_" + str(i) + ".json"),
                      monitorCrossData.raw_data
                      )
            # </editor-folder>
            # <editor-folder desc="--- 7.3.2 cross_intensity ---">
            monitorCrossData = fdtdSweepResult.passive_fdtd_sweep_result_chart_new(target="intensity",
                                                                                   monitor=monitorCross,
                                                                                   attribute="E",
                                                                                   operation="ABS",
                                                                                   plotX="x",
                                                                                   y=0,
                                                                                   plotY="z",
                                                                                   wavelength=0,
                                                                                   sweep_gap=i,
                                                                                   )
            x, y, Z = monitorCrossData.raw_data["horizontal"], monitorCrossData.raw_data["vertical"], \
                monitorCrossData.raw_data["data"]
            heatmap(x, y, Z)
            plt.xlabel("x (μm)")
            plt.ylabel("z (μm)")
            plt.title("cross_mon wavelength=0_ABS(E)_intensity gap_" + str(i))
            plt.savefig(plotPath + "23_cross_abs(E)_" + str(i) + ".jpg")
            plt.close()
            json_save(os.path.join(plotPath, "23_cross_abs(E)_" + str(i) + ".json"),
                      monitorCrossData.raw_data
                      )
            # </editor-folder>
            # </editor-folder>

            # <editor-folder desc="--- 7.4 reflection ---">
            # <editor-folder desc="--- 7.4.1 ref_line ---">
            monitorReflectionData = fdtdSweepResult.passive_fdtd_sweep_result_chart_new(target="line",
                                                                                        monitor=monitorReflection,
                                                                                        attribute="T",
                                                                                        operation="ABS",
                                                                                        x=0,
                                                                                        y=0,
                                                                                        z=0,
                                                                                        plotX="wavelength",
                                                                                        sweep_gap=i
                                                                                        )
            lineplot(monitorReflectionData.DataFrame)
            plt.xlabel("wavelength (μm)")
            plt.ylabel("Transmission_Reflection")
            plt.title("reflection_mon ABS(T)_line gap_" + str(i))
            plt.savefig(plotPath + "24_reflection_abs(T)_" + str(i) + ".jpg")
            plt.close()
            json_save(os.path.join(plotPath, "24_reflection_abs(T)_" + str(i) + ".json"),
                      monitorReflectionData.raw_data
                      )
            # </editor-folder>

            # <editor-folder desc="--- 7.4.2 ref_intensity ---">
            monitorReflectionData = fdtdSweepResult.passive_fdtd_sweep_result_chart_new(target="intensity",
                                                                                        monitor=monitorReflection,
                                                                                        attribute="E",
                                                                                        operation="ABS",
                                                                                        x=0,
                                                                                        plotX="y",
                                                                                        plotY="z",
                                                                                        wavelength=0,
                                                                                        sweep_gap=i,
                                                                                        )
            x, y, Z = monitorReflectionData.raw_data["horizontal"], monitorReflectionData.raw_data["vertical"], \
                monitorReflectionData.raw_data["data"]
            heatmap(x, y, Z)
            plt.xlabel("y (μm)")
            plt.ylabel("z (μm)")
            plt.title("reflection_mon wavelength=0_ABS(E)_intensity gap_" + str(i))
            plt.savefig(plotPath + "24_reflection_abs(E)_" + str(i) + ".jpg")
            plt.close()
            json_save(os.path.join(plotPath, "24_reflection_abs(E)_" + str(i) + ".json"),
                      monitorReflectionData.raw_data
                      )
            # </editor-folder>
            # </editor-folder>

    # </editor-folder>


if __name__ == "__main__":
    startTime = time.time()
    currentDate = time.strftime("%Y%m%d", time.localtime(time.time()))
    path = str(Path(__file__).parent.as_posix())
    projectName = "FDTD_HALFRING_PARAMETER_SWEEP"  # + currentDate
    meshType = 0  # [0:Staircase, 1:Advanced Volume Average, 2:Dielectric Volume Average, 4:CP-EP]
    gridsPerLambda = 15
    simulation(project_name=projectName,
               extract=True,
               source_view=True,
               run_parameter_sweep=True,
               mesh_type=meshType,
               grids_per_lambda=gridsPerLambda
               )
    stopTime = time.time()
    print("[Finished in %(t)s mins]" % {"t": round((stopTime - startTime) / 60, 2)})
