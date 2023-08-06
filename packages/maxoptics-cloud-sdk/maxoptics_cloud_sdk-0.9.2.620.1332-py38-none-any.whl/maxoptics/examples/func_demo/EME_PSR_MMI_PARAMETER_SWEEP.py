import json
import os
import time
from pathlib import Path

from matplotlib import pyplot as plt
import pandas

import maxoptics
from maxoptics import X_Normal
from maxoptics.core import heatmap, lineplot

client = maxoptics.MosLibraryCloud()

SiO2 = client.public_materials["SiO2 (Glass) - Palik"]
Si = client.public_materials["Si (Silicon) - Palik"]


def json_save(path, data):
    with open(path, "w") as f:
        json.dump(data, f)


def simulation(project_name, run_eme=False, run_parameter_sweep=False, source_view=False,
               extract=False, number_of_modes=10, grid=0.02, _wavelength=1.55):
    # <editor-folder desc="--- 0. general parameter ---">
    mmiWidthConfig = {"start": 1.4, "stop": 2.2, "points": 11}
    plotPath = str(Path(__file__).parent.as_posix()) + "/plots/EME_PSR_MMI_PARAMETER_SWEEP/"
    meshPath = plotPath + "mesh"
    if not os.path.exists(plotPath):
        os.makedirs(plotPath)
    if not os.path.exists(meshPath):
        os.makedirs(meshPath)
    # </editor-folder>

    # <editor-folder desc="--- 1. create project & EME ---">
    # <editor-folder desc="--- 1.1 project---">
    project = client.create_project_as(project_name)

    # add global param
    project.DOCUMENT.append_global_param("wg_win", "", 0.75, "")
    project.DOCUMENT.append_global_param("wg_wout", "", 0.7, "")
    project.DOCUMENT.append_global_param("mmi_w", "", 1.8, "")
    project.DOCUMENT.append_global_param("wg_l", "", 2.5, "")
    project.DOCUMENT.append_global_param("mmi_l", "", 5.2, "")
    # </editor-folder>

    # <editor-folder desc="--- 1.2 EME ---">
    # create eme
    eme = project.create_eme(background_material=client.public_materials["Air"],
                             use_wavelength_sweep=1,  # [0:not use wavelength sweep,1:use wavelength sweep]
                             wavelength=_wavelength,
                             x_min=0,
                             y=0,
                             y_span=4,
                             z=0,
                             z_span=4,
                             energy_conversation=1,  # [0:None, 1:Make Passive]
                             define_y_mesh=1,
                             # [0:Number of Mesh Cells, 1:maximum Mesh Step] boolean parameter. 1: allow to set dy by user.
                             define_z_mesh=1,
                             # [0:Number of Mesh Cells, 1:maximum Mesh Step] boolean parameter. 1: allow to set dz by user.
                             dy=grid,
                             dz=grid,
                             min_mesh_step=1e-05,
                             grading_factor=1.2,
                             y_min_bc=1,  # [0:PML, 1:PEC, 2:PMC, 3:Symmetric, 4:Anti-Symmetry, 5:Periodic]
                             y_max_bc=1,  # [0:PML, 1:PEC, 2:PMC, 5:Periodic]
                             z_min_bc=1,  # [0:PML, 1:PEC, 2:PMC, 3:Symmetric, 4:Anti-Symmetry, 5:Periodic]
                             z_max_bc=1,  # [0:PML, 1:PEC, 2:PMC, 5:Periodic]
                             refinement_type=1,  # [1:Dielectric Volume Average]
                             max_stored_modes=1000
                             )
    # set cell
    eme.append_cell(span=2.5,
                    cell_num=1,
                    number_of_modes=number_of_modes,
                    sc=0,  # [0:None, 1:Sub cell]
                    fix="x_min"  # use eme's x_min position as fix position of cell calc dependency; default fix position is eme's x position
                    )
    eme.append_cell(span=5.2,
                    cell_num=1,
                    number_of_modes=number_of_modes,
                    sc=0,  # [0:None, 1:Sub cell]
                    fix="x_min"  # use eme's x_min position as fix position of cell calc dependency; default fix position is eme's x position
                    )
    eme.append_cell(span=2.5,
                    cell_num=1,
                    number_of_modes=number_of_modes,
                    sc=0,  # [0:None, 1:Sub cell]
                    fix="x_min"  # use eme's x_min position as fix position of cell calc dependency; default fix position is eme's x position
                    )
    # </editor-folder>
    # </editor-folder>

    # <editor-folder desc="--- 2. structure ---">
    # <editor-folder desc="--- 2.1 wg_in ---">
    wgIn = project.create_rectangle(name="wg_in",
                                    x=1.25,
                                    x_span=2.5,
                                    y=0,
                                    y_span=0.75,
                                    z=0.11,
                                    z_span=0.22,
                                    materialId=client.public_materials["Si (Silicon) - Palik"],
                                    overrideMeshOrder=0,  # [0:use material mesh order,1:set mesh order by user]
                                    meshOrder=1
                                    )
    wgInAttrs = wgIn.attrs
    wgInAttrs.__expre__.x_max = "wg_l"
    wgInAttrs.__expre__.y_min = "-wg_win/2"
    wgInAttrs.__expre__.y_max = "wg_win/2"
    # </editor-folder>

    # <editor-folder desc="--- 2.2 mmi ---">
    mmi = project.create_rectangle(name="mmi",
                                   x=5.1,
                                   x_span=5.2,
                                   y=0,
                                   y_span=1.8,
                                   z=0.11,
                                   z_span=0.22,
                                   materialId=client.public_materials["Si (Silicon) - Palik"],
                                   overrideMeshOrder=0,  # [0:use material mesh order,1:set mesh order by user]
                                   meshOrder=1
                                   )
    mmiAttrs = mmi.attrs
    mmiAttrs.__expre__.x_min = "wg_l"
    mmiAttrs.__expre__.x_max = "wg_l+mmi_l"
    mmiAttrs.__expre__.y_min = "-mmi_w/2"
    mmiAttrs.__expre__.y_max = "mmi_w/2"
    # </editor-folder>

    # <editor-folder desc="--- 2.3 wg_out ---">
    wgOut = project.create_rectangle(name="wg_out",
                                     x=1.25,
                                     x_span=2.5,
                                     y=0,
                                     y_span=0.75,
                                     z=0.11,
                                     z_span=0.22,
                                     materialId=client.public_materials["Si (Silicon) - Palik"],
                                     overrideMeshOrder=0,  # [0:use material mesh order,1:set mesh order by user]
                                     meshOrder=1
                                     )
    wgOutAttrs = wgOut.attrs
    wgOutAttrs.__expre__.x_min = "wg_l+mmi_l"
    wgOutAttrs.__expre__.x_max = "wg_l+mmi_l+wg_l"
    wgOutAttrs.__expre__.y_min = "-wg_wout/2"
    wgOutAttrs.__expre__.y_max = "wg_wout/2"
    wgOutAttrs.__expre__.x_max = "wg_l*2+mmi_l"

    # </editor-folder>

    # <editor-folder desc="--- 2.4 box ---">
    box = project.create_rectangle(name="box",
                                   x=5.1,
                                   x_span=10.2,
                                   y=0,
                                   y_span=4,
                                   z=-2,
                                   z_span=4,
                                   materialId=client.public_materials["SiO2 (Glass) - Palik"],
                                   overrideMeshOrder=0,  # [0:use material mesh order,1:set mesh order by user]
                                   meshOrder=1
                                   )
    boxAttrs = box.attrs
    # </editor-folder>
    # </editor-folder>

    # <editor-folder desc="--- 3. port ---">
    leftPort = project.create_eme_port(name="left_port",
                                       port_location=0,  # [0:Left, 1:Right]
                                       use_full_simulation_span=1,  # [0:False, 1:True]
                                       mode_selection=0,
                                       # [0:Fundamental Mode, 1:Fundamental TE Mode, 2:Fundamental TM Mode, 3:User Select, 4:User Import]
                                       )
    rightPort = project.create_eme_port(name="right_port",
                                        port_location=1,  # [0:Left, 1:Right]
                                        use_full_simulation_span=1,  # [0:False, 1:True]
                                        mode_selection=0,
                                        # [0:Fundamental Mode, 1:Fundamental TE Mode, 2:Fundamental TM Mode, 3:User Select, 4:User Import]
                                        )
    # </editor-folder>

    # <editor-folder desc="--- 4. see mesh ---">
    # </editor-folder>

    # <editor-folder desc="--- 5. see port fde result ---">
    if source_view:
        start = time.time()
        print("\x1b[6;30;42m" + "--- starting calculate modes now !!!! ---" + "\x1b[0m")
        for port in [leftPort, rightPort]:
            modeSelection = port.attrs.mode_selection
            port.attrs.mode_selection = 3
            portResult = project.run_calculate_modes(port)
            portData = portResult.passive_fde_result_chart(target="intensity",
                                                           attribute="E",
                                                           operation="ABS",
                                                           x=0,
                                                           plotX="y",
                                                           plotY="z",
                                                           mode=0
                                                           )
            x, y, Z = portData.raw_data["horizontal"], portData.raw_data["vertical"], \
                portData.raw_data["data"]
            heatmap(x, y, Z)
            plt.xlabel("y (μm)")
            plt.ylabel("z (μm)")
            plt.title("port_mode_profile")
            plt.savefig(plotPath + "01_" + port.name + "_modeprofile_fdeonly.jpg")
            plt.close()
            port.attrs.mode_selection = modeSelection
        stop = time.time()
        print("\x1b[6;30;42m" + "[Finished in %(t)s mins for calculate modes]" %
              {"t": round((stop - start) / 60, 2)} + "\x1b[0m")
    # </editor-folder>

    # <editor-folder desc="--- 6. run ---">
    start = time.time()
    print("\x1b[6;30;42m" + "--- starting now !!!! ---" + "\x1b[0m")

    # <editor-folder desc="--- 6.1 run EME ---">
    if run_eme:
        emeFDEResult = project.run_eme_fde()
        emeResult = project.run_eme_eme(dep_task=emeFDEResult.id)
    # </editor-folder>

    # <editor-folder desc="--- 6.2 run EME parameter sweep ---">
    if run_parameter_sweep:

        # create sweep solver
        emeSweep = project.create_sweep()

        # add param data to sweep
        emeSweep.append_param_data("mmi_w", mmiWidthConfig["start"], mmiWidthConfig["stop"],
                                   mmiWidthConfig["points"]
                                   )
        # add smatrix monitor to sweep
        emeSweep.append_result_monitor("SMatrix", "S-Matrix", "S")

        # save project
        project.save()

        # run eme parameter sweep
        emeSweepResult = project.run_eme_parameter_sweep()
    # </editor-folder>

    stop = time.time()
    print("\x1b[6;30;42m" + "[Finished in %(t)s mins]" % {"t": round((stop - start) / 60, 2)} + "\x1b[0m")
    # </editor-folder>

    # <editor-folder desc="--- 7. see results ---">
    # <editor-folder desc="--- 7.1 EME ---">
    if run_eme and extract:

        # get eme smatrix result
        sMatrixData = emeResult.passive_eme_smatrix_chart(target="intensity",
                                                          attribute="S",
                                                          operation="ABS"
                                                          )
        x, y, Z = sMatrixData.raw_data["horizontal"], sMatrixData.raw_data["vertical"], \
            sMatrixData.raw_data["data"]
        fig, ax = heatmap(x, y, Z)
        ax.invert_yaxis()
        plt.xlabel("")
        plt.ylabel("")
        plt.title("EME SMatrix")
        plt.savefig(plotPath + "02_eme_SMatrix.jpg")
        plt.close()
        json_save(os.path.join(plotPath, "02_eme_SMatrix_result.json"),
                  sMatrixData.raw_data
                  )
    # </editor-folder>

    # <editor-folder desc="--- 7.2 EME parameter sweep ---">
    if run_parameter_sweep and extract:

        y_param = []
        # get sweep options
        mmi_result = emeSweepResult.passive_eme_params_sweep_option('intensity')['sweep_mmi_w']
        for i in range(mmiWidthConfig["points"]):
            # get each mmi_w sMatrix of eme sweep chart
            sMatrixData = emeSweepResult.passive_eme_params_sweep_chart(target="intensity",
                                                                        attribute="S",
                                                                        operation="ABS",
                                                                        sweep_mmi_w=i  # index of sweep_mmi_w
                                                                        )
            x, y, Z = sMatrixData.raw_data["horizontal"], sMatrixData.raw_data["vertical"], \
                sMatrixData.raw_data["data"]
            fig, ax = heatmap(x, y, Z)
            ax.invert_yaxis()
            plt.xlabel("")
            plt.ylabel("")
            plt.title("EME SMatrix")
            plt.savefig(plotPath + "03_parameter_sweep_SMatrix_" + str(i + 1) + ".jpg")
            plt.close()
            json_save(os.path.join(plotPath, "03_parameter_sweep_Result_" + str(i + 1) + ".json"),
                      sMatrixData.raw_data['data'][1][0]
                      )
            y_param.append(sMatrixData.raw_data['data'][1][0])

        # draw combined x:mmi_w and y: transmission data for lineplot mmi_result
        lineplot(dataframe=pandas.DataFrame(data=y_param, index=mmi_result, columns=["sweep"]))
        plt.xlabel("mmi_w")
        plt.ylabel("transmission")
        plt.title("EME lineplot")
        plt.savefig(plotPath + "03_eme_parameter_sweep_lineplot_result.jpg")
        plt.close()

    # </editor-folder>
    # </editor-folder>


if __name__ == "__main__":
    startTime = time.time()
    currentDate = time.strftime("%Y%m%d", time.localtime(time.time()))
    path = str(Path(__file__).parent.as_posix())
    projectName = "EME_PSR_MMI_PARAMETER_SWEEP"  # + currentDate
    simulation(project_name=projectName,
               extract=True,
               source_view=True,
               run_eme=True,
               run_parameter_sweep=True,
               number_of_modes=20,
               grid=0.02,
               _wavelength=1.5
               )
    stopTime = time.time()
    print("[Finished in %(t)s mins]" % {"t": round((stopTime - startTime) / 60, 2)})
