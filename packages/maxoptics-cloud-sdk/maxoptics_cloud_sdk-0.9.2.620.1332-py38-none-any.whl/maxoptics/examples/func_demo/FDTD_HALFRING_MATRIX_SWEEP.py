import json
import os
import time
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt
import maxoptics.maxopt_sdk as sdk

import maxoptics
from maxoptics.core import heatmap, lineplot
from maxoptics.macros import X_Normal, Y_Normal, Z_Normal

client = maxoptics.MosLibraryCloud()

SiO2 = client.public_materials["SiO2 (Glass) - Palik"]
Si = client.public_materials["Si (Silicon) - Palik"]


def json_save(path, data):
    with open(path, "w") as f:
        json.dump(data, f)


def simulation(gds_file="", gds_topcell="", project_name="", run_fdtd=False, run_matrix_sweep=False,
               source_view=False, extract=False, mesh_type=0, grids_per_lambda=6):
    # <editor-folder desc="--- 0. general parameter ---">
    plotPath = str(Path(__file__).parent.as_posix()) + "/plots/FDTD_HALFRING_MATRIX_SWEEP/"
    meshPath = plotPath + "mesh"
    if not os.path.exists(plotPath):
        os.makedirs(plotPath)
    if not os.path.exists(meshPath):
        os.makedirs(meshPath)
    # </editor-folder>

    # <editor-folder desc="--- 1. create project & FDTD ---">
    # <editor-folder desc="--- 1.1 project---">
    sdk.init_waveforms('./case_waveforms.json')
    waveform = sdk.Waveform.find('Waveform_1550_100')  # set waveform
    project = client.create_project_as(project_name)  # create project
    # </editor-folder>

    # <editor-folder desc="--- 1.2 FDTD ---">
    fdtd_config = {"simulation_time"     : 2000,
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
    # </editor-folder>
    # </editor-folder>

    # <editor-folder desc="--- 2. structure ---">
    project.gds_import(gds_file, gds_topcell, "1/0", "SiO2 (Glass) - Palik", -4, 0)
    project.gds_import(gds_file, gds_topcell, "2/0", "Si (Silicon) - Palik", 0, 0.18)
    # </editor-folder>

    # <editor-folder desc="--- 3. set monitor ---">
    # <editor-folder desc="--- 3.1 global monitor ---">
    globalMonitorConfig = {"use_wavelength_spacing": 1,  # use wavelength_spacing [1:on, 0:off]
                           "use_source_limits": 0,  # source_limits [1:on, 0:off]
                           "spacing_type": 0,  # [0:wavelength, 1:frequency]
                           "spacing_limit": 0,  # [0:min/max, 1:center/span]
                           "wavelength_min": 1.5,
                           "wavelength_max": 1.6,
                           "frequency_points": 101,
                           }
    project.create_global_monitor(**globalMonitorConfig)
    # </editor-folder>

    # <editor-folder desc="--- 3.2 power monitor ---">
    # <editor-folder desc="--- 3.2.1 zNormal ---">
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
                            "frequency_points": 11,
                            }

    monitorZNormal = project.create_power_monitor(**monitorZNormalConfig)
    # </editor-folder>

    # <editor-folder desc="--- 3.2.2 through ---">
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
    # </editor-folder>

    # <editor-folder desc="--- 3.2.3 cross ---">
    monitorCrossConfig = {"name"                   : "cross",
                          "monitor_type"           : Y_Normal,
                          "x"                      : 3.1,
                          "y"                      : -3,
                          "z"                      : 0.09,
                          "x_span"                 : 3,
                          "y_span"                 : 0,
                          "z_span"                 : 2,
                          "override_global_options": 1,  # [1:override, 0:not override] [default:1]
                          "use_wavelength_spacing" : 1,  # use wavelength_spacing [1:on, 0:off]
                          "use_source_limits"      : 0,  # source_limits [1:on, 0:off]
                          "spacing_type"           : 0,  # [0:wavelength, 1:frequency]
                          "spacing_limit"          : 0,  # [0:min/max, 1:center/span]
                          "wavelength_center"      : waveform["data"]["center_wavelength"],
                          "wavelength_span"        : waveform["data"]["wavelength_span"],
                          "frequency_points"       : 51
                          }

    monitorCross = project.create_power_monitor(**monitorCrossConfig)
    # </editor-folder>

    # <editor-folder desc="--- 3.2.4 reflection ---">
    monitorReflectionConfig = {"name"                   : "reflection",
                               "monitor_type"           : X_Normal,
                               "x"                      : -4.2,
                               "y"                      : 3.6,
                               "z"                      : 0.09,
                               "x_span"                 : 0,
                               "y_span"                 : 3,
                               "z_span"                 : 2,
                               "override_global_options": 1,  # [1:use global option, 0:not override] [default:1]
                               "use_wavelength_spacing" : 1,  # use wavelength_spacing [1:on, 0:off]
                               "use_source_limits"      : 0,  # source_limits [1:on, 0:off]
                               "spacing_type"           : 0,  # [0:wavelength, 1:frequency]
                               "spacing_limit"          : 0,  # [0:min/max, 1:center/span]
                               "wavelength_center"      : waveform["data"]["center_wavelength"],
                               "wavelength_span"        : waveform["data"]["wavelength_span"],
                               "frequency_points"       : 101
                               }

    monitorReflection = project.create_power_monitor(**monitorReflectionConfig)
    # </editor-folder>
    # </editor-folder>
    # </editor-folder>

    # <editor-folder desc="--- 4. set fdtd port group & port ---">
    portGroup = project.create_fdtd_port_group(waveform_id=waveform["id"])

    # <editor-folder desc="--- 4.1 portIn ---">
    portIn = project.create_fdtd_port(name="port_in",
                                      injection_axis=0,  # [0:X-Axis,1:Y-Axis,2:Z-Axis]
                                      direction=0,  # [0:Forward,1:Backward]
                                      mode_selection=3,
                                      # [0:Fundamental Mode, 1:Fundamental TE Mode, 2:Fundamental TM Mode, 3:User Select, 4:User Import]
                                      mode_index=1,
                                      use_max_index=1,  # [0:near n,1:max index]
                                      bent_waveguide=False,
                                      x=-4.005,
                                      x_span=0,
                                      y=3.6,
                                      y_span=3,
                                      z=0.09,
                                      z_span=2
                                      )
    # </editor-folder>

    # <editor-folder desc="--- 4.2 portThrough ---">
    portThrough = project.create_fdtd_port(name="port_through",
                                           injection_axis=0,  # [0:X-Axis,1:Y-Axis,2:Z-Axis]
                                           direction=1,  # [0:Forward,1:Backward]
                                           mode_selection=3,
                                           # [0:Fundamental Mode, 1:Fundamental TE Mode, 2:Fundamental TM Mode, 3:User Select, 4:User Import]
                                           mode_index=1,
                                           use_max_index=1,  # [0:near n,1:max index]
                                           bent_waveguide=False,
                                           x=4,
                                           x_span=0,
                                           y=3.6,
                                           y_span=3,
                                           z=0.09,
                                           z_span=2
                                           )
    # </editor-folder>

    # <editor-folder desc="--- 4.3 portCross ---">
    portCross = project.create_fdtd_port(name="port_cross",
                                         injection_axis=1,  # [0:X-Axis,1:Y-Axis,2:Z-Axis]
                                         direction=0,  # [0:Forward,1:Backward]
                                         mode_selection=0,
                                         # [0:Fundamental Mode, 1:Fundamental TE Mode, 2:Fundamental TM Mode, 3:User Select, 4:User Import]
                                         mode_index=1,
                                         use_max_index=1,  # [0:near n,1:use max index]
                                         bent_waveguide=False,
                                         x=3.1,
                                         x_span=3,
                                         y=-3.5,
                                         y_span=0,
                                         z=0.09,
                                         z_span=2
                                         )
    # </editor-folder>

    portGroup.attrs.source_port = portIn.id

    # </editor-folder>

    # <editor-folder desc="--- 5. see mode source result ---">
    if source_view:
        start = time.time()
        print("\x1b[6;30;42m" + "--- starting calculate modes now !!!! ---" + "\x1b[0m")
        plotOption = [{"x": 0, "y": "plotX", "z": "plotY"}, {"x": "plotX", "y": 0, "z": "plotY"},
                      {"x": "plotX", "y": "plotY", "z": 0}]
        labelName = [{"x": "y (μm)", "y": "z (μm)"}, {"x": "x (μm)", "y": "z (μm)"}, {"x": "x (μm)", "y": "y (μm)"}]

        # get fde mode for each port
        for port in [portIn, portCross, portThrough]:
            modeSelection = port.attrs.mode_selection
            modeIndex = port.attrs.mode_index

            # set the mode_selection and mode_index for calculating
            port.attrs.mode_selection = 3
            port.attrs.mode_index = 1

            # run calculate modes for port
            portResult = project.run_calculate_modes(port)

            # get the fde mode result with E and ABS and mode=0
            portData = portResult.passive_fde_result_chart(target="intensity",
                                                           attribute="E",
                                                           operation="ABS",
                                                           x=plotOption[port.attrs.injection_axis]["x"],
                                                           y=plotOption[port.attrs.injection_axis]["y"],
                                                           z=plotOption[port.attrs.injection_axis]["z"],
                                                           mode=0
                                                           )
            x, y, Z = portData.raw_data["horizontal"], portData.raw_data["vertical"], \
                portData.raw_data["data"]
            heatmap(x, y, Z)
            plt.xlabel(labelName[port.attrs.injection_axis]["x"])
            plt.ylabel(labelName[port.attrs.injection_axis]["y"])
            plt.title("source_mode_profile")
            plt.savefig(plotPath + "00_" + port.name + "_modeprofile_fdeonly.jpg")
            plt.close()
            port.attrs.mode_selection = modeSelection
            port.attrs.mode_index = modeIndex
        stop = time.time()
        print("\x1b[6;30;42m" + "[Finished in %(t)s mins for calculate modes]" %
              {"t": round((stop - start) / 60, 2)} + "\x1b[0m")
    # </editor-folder>

    # <editor-folder desc="--- 6. run ---">
    start = time.time()
    print("\x1b[6;30;42m" + "--- starting now !!!! ---" + "\x1b[0m")

    # <editor-folder desc="--- 6.1 run fdtd ---">
    if run_fdtd:
        fdtdResult = project.run_fdtd()
    # </editor-folder>

    # <editor-folder desc="--- 6.2 run fdtd matrix sweep ---">
    if run_matrix_sweep:
        # create matrix sweep
        fdtdMatrixSweep = project.create_matrix_sweep()

        # add portIn to matrix sweep for calculating
        # mode is the source mode index, default is 1, if user need to modify the
        # mode, user need to set the value of mode
        fdtdMatrixSweep.append_table_data(port=portIn, mode=1, active=True)

        # add portThrough to matrix sweep for calculating
        # mode is the source mode index, default is 1, if user need to modify the
        # mode, user need to set the value of mode
        fdtdMatrixSweep.append_table_data(port=portThrough, mode=1, active=True)

        # add portCross to matrix sweep for calculating
        # mode is the source mode index, default is 1, if user need to modify the
        # mode, user need to set the value of mode
        fdtdMatrixSweep.append_table_data(port=portCross, mode=1, active=True)

        # run fdtd smatrix
        fdtdMatrixSweepResult = project.run_fdtd_smatrix()
    # </editor-folder>

    stop = time.time()
    print("\x1b[6;30;42m" + "[Finished in %(t)s mins]" % {"t": round((stop - start) / 60, 2)} + "\x1b[0m")
    # </editor-folder>

    # <editor-folder desc="--- 7. see results ---">
    # <editor-folder desc="--- 7.1 fdtd ---">
    if run_fdtd and extract:
        # <editor-folder desc="--- 7.1.1 z_normal ---">
        monitorZNormalData = fdtdResult.passive_fdtd_fd_result_chart("intensity", monitorZNormal, "E", "ABS", plotX='x',
                                                                     plotY='y', z=0, wavelength=0
                                                                     )
        x, y, Z = monitorZNormalData.raw_data["horizontal"], monitorZNormalData.raw_data["vertical"], \
            monitorZNormalData.raw_data["data"]
        heatmap(x, y, Z)
        plt.xlabel("x (μm)")
        plt.ylabel("y (μm)")
        plt.title("z_normal_mon-E-ABS-x-y heatmap with z=0")
        plt.savefig(plotPath + "11_fdtd_zNormal_abs(E).jpg")
        plt.close()
        json_save(os.path.join(plotPath, "11_fdtd_zNormal_abs(E).json"),
                  monitorZNormalData.raw_data
                  )
        # </editor-folder>

        # <editor-folder desc="--- 7.1.2 through ---">
        # <editor-folder desc="--- 7.1.2.1 through_line ---">
        monitorThroughData = fdtdResult.passive_fdtd_fd_result_chart(target="line",
                                                                     monitor=monitorThrough,
                                                                     attribute="T",
                                                                     operation="ABS",
                                                                     x=0,
                                                                     y=0,
                                                                     z=0,
                                                                     plotX="wavelength"
                                                                     )
        lineplot(monitorThroughData.DataFrame)
        plt.xlabel("wavelength (μm)")
        plt.ylabel("Transmission_Through")
        plt.title("through_mon-T-ABS line")
        plt.savefig(plotPath + "12_fdtd_through_abs(T).jpg")
        plt.close()
        json_save(os.path.join(plotPath, "12_fdtd_through_abs(T).json"), monitorThroughData.raw_data)
        # </editor-folder>

        # <editor-folder desc="--- 7.1.2.2 through_intensity ---">
        monitorThroughData = fdtdResult.passive_fdtd_fd_result_chart(target="intensity",
                                                                     monitor=monitorThrough,
                                                                     attribute="E",
                                                                     operation="ABS",
                                                                     x=0,
                                                                     plotX="y",
                                                                     plotY="z",
                                                                     wavelength=0
                                                                     )
        x, y, Z = monitorThroughData.raw_data["horizontal"], monitorThroughData.raw_data["vertical"], \
            monitorThroughData.raw_data["data"]
        heatmap(x, y, Z)
        plt.xlabel("y (μm)")
        plt.ylabel("z (μm)")
        plt.title("through_mon wavelength=0_ABS(E) plot")
        plt.savefig(plotPath + "12_fdtd_through_abs(E).jpg")
        plt.close()
        json_save(os.path.join(plotPath, "12_fdtd_through_abs(E).json"), monitorThroughData.raw_data)
        # </editor-folder>
        # </editor-folder>

        # <editor-folder desc="--- 7.1.3 cross ---">
        # <editor-folder desc="--- 7.1.3.1 cross_line---">
        monitorCrossData = fdtdResult.passive_fdtd_fd_result_chart(target="line",
                                                                   monitor=monitorCross,
                                                                   attribute="T",
                                                                   operation="ABS",
                                                                   x=0,
                                                                   y=0,
                                                                   z=0,
                                                                   plotX="wavelength"
                                                                   )
        lineplot(monitorCrossData.DataFrame)
        plt.xlabel("wavelength (μm)")
        plt.ylabel("Transmission_Cross")
        plt.title("cross_mon-T-ABS line")
        plt.savefig(plotPath + "13_fdtd_cross_abs(T).jpg")
        plt.close()
        json_save(os.path.join(plotPath, "13_fdtd_cross_abs(T).json"), monitorCrossData.raw_data)
        # </editor-folder>

        # <editor-folder desc="--- 7.1.3.2 cross_intensity ---">
        monitorCrossData = fdtdResult.passive_fdtd_fd_result_chart(target="intensity",
                                                                   monitor=monitorCross,
                                                                   attribute="E",
                                                                   operation="ABS",
                                                                   plotX="x",
                                                                   y=0,
                                                                   plotY="z",
                                                                   wavelength=0
                                                                   )
        x, y, Z = monitorCrossData.raw_data["horizontal"], monitorCrossData.raw_data["vertical"], \
            monitorCrossData.raw_data["data"]
        heatmap(x, y, Z)
        plt.xlabel("x (μm)")
        plt.ylabel("z (μm)")
        plt.title("cross_mon wavelength=0_ABS(E) plot")
        plt.savefig(plotPath + "13_fdtd_cross_abs(E).jpg")
        plt.close()
        json_save(os.path.join(plotPath, "13_fdtd_cross_abs(E).json"), monitorCrossData.raw_data)
        # </editor-folder>
        # </editor-folder>

        # <editor-folder desc="--- 7.1.4 reflection ---">
        # <editor-folder desc="--- 7.1.4.1 reflection_line ---">
        monitorReflectionData = fdtdResult.passive_fdtd_fd_result_chart(target="line",
                                                                        monitor=monitorReflection,
                                                                        attribute="T",
                                                                        operation="ABS",
                                                                        x=0,
                                                                        y=0,
                                                                        z=0,
                                                                        plotX="wavelength"
                                                                        )
        lineplot(monitorReflectionData.DataFrame)
        plt.xlabel("wavelength (μm)")
        plt.ylabel("Transmission_Reflection")
        plt.title("ref_mon-T-ABS line")
        plt.savefig(plotPath + "14_fdtd_reflection_abs(T).jpg")
        plt.close()
        json_save(os.path.join(plotPath, "14_fdtd_reflection_abs(T).json"), monitorReflectionData.raw_data)
        # </editor-folder>

        # <editor-folder desc="--- 7.1.4.2 reflection_intensity ---">
        monitorReflectionData = fdtdResult.passive_fdtd_fd_result_chart(target="intensity",
                                                                        monitor=monitorReflection,
                                                                        attribute="E",
                                                                        operation="ABS",
                                                                        x=0,
                                                                        plotX="y",
                                                                        plotY="z",
                                                                        wavelength=0
                                                                        )
        x, y, Z = monitorReflectionData.raw_data["horizontal"], monitorReflectionData.raw_data["vertical"], \
            monitorReflectionData.raw_data["data"]
        heatmap(x, y, Z)
        plt.xlabel("y (μm)")
        plt.ylabel("z (μm)")
        plt.title("ref_mon wavelength=0_ABS(E) plot")
        plt.savefig(plotPath + "14_fdtd_reflection_abs(E).jpg")
        plt.close()
        json_save(os.path.join(plotPath, "14_fdtd_reflection_abs(E).json"), monitorReflectionData.raw_data)
        # </editor-folder>
        # </editor-folder>
    # </editor-folder>

    # <editor-folder desc="--- 7.2 fdtd matrix sweep ---">
    if run_matrix_sweep and extract:
        # <editor-folder desc="--- 7.2.1 S-Matrix ---">
        sMatrixData = fdtdMatrixSweepResult.passive_fdtd_smatrix_sweep_chart(target="intensity",
                                                                             attribute="S",
                                                                             operation="ABS",
                                                                             wavelength=0
                                                                             )
        x, y, Z = sMatrixData.raw_data["horizontal"], sMatrixData.raw_data["vertical"], \
            sMatrixData.raw_data["data"]
        fig, ax = heatmap(x, y, Z)
        ax.invert_yaxis()
        plt.xlabel("")
        plt.ylabel("")
        plt.title("S-Matrix")
        plt.savefig(plotPath + "21_matrix_sweep_abs(S).jpg")
        plt.close()
        json_save(os.path.join(plotPath, "21_matrix_sweep_abs(S).json"),
                  sMatrixData.raw_data
                  )
        # </editor-folder>

        # <editor-folder desc="--- 7.2.2 S-Parameter ---">
        # set legendName list circular enumeration for S transmission rate
        sParamWavelengthoption = fdtdMatrixSweepResult.passive_fdtd_smatrix_sweep_option("intensity")['wavelength']

        legendName = ["S11", "S21", "S31", "S12", "S22", "S32", "S13", "S23", "S33"]

        # get the sweep result
        sParameterData = fdtdMatrixSweepResult.passive_fdtd_smatrix_sweep_chart(target="line",
                                                                                attribute="S",
                                                                                operation="ABS",
                                                                                log=False,
                                                                                plotX="wavelength"
                                                                                )
        # draw transmission rate on each S Matrix
        for i in range(9):
            lineplot(
                pd.DataFrame(
                    data=sParameterData.raw_data['data'][i],
                    index=sParamWavelengthoption,
                    columns=["sweep"]))
            plt.xlabel("wavelength (μm)")
            plt.ylabel("")
            plt.title("FDTD S-Matrix abs(" + legendName[i] + ")")
            plt.savefig(plotPath + "22_matrix_sweep_abs(" + legendName[i] + ").jpg")
            plt.close()
            json_save(os.path.join(plotPath, "22_matrix_sweep_abs(" + legendName[i] + ").json"),
                      sParameterData.raw_data["data"][i]
                      )
        # </editor-folder>
        # </editor-folder>
    # </editor-folder>


if __name__ == "__main__":
    startTime = time.time()
    currentDate = time.strftime("%Y%m%d", time.localtime(time.time()))
    path = str(Path(__file__).parent.as_posix())
    gdsFilePath = path + "/gds/" + "/hfr.gds"
    gdsTopCell = "HalfRing"
    projectName = "FDTD_HALFRING_MATRIX_SWEEP"  # + currentDate
    meshType = 4  # [0:Staircase, 1:Advanced Volume Average, 2:Dielectric Volume Average, 4:CP-EP]
    gridsPerLambda = 15
    simulation(project_name=projectName,
               extract=True,
               source_view=True,
               run_fdtd=True,
               run_matrix_sweep=True,
               gds_file=gdsFilePath,
               gds_topcell=gdsTopCell,
               mesh_type=meshType,
               grids_per_lambda=gridsPerLambda
               )
    stopTime = time.time()
    print("[Finished in %(t)s mins]" % {"t": round((stopTime - startTime) / 60, 2)})
