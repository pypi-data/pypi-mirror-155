import os
import time
from pathlib import Path
from pprint import pprint
import pandas as pd

from matplotlib import pyplot as plt
from maxoptics.core import lineplot, heatmap
import maxoptics

from maxoptics.maxopt_sdk import TaskResult
from maxoptics.maxopt_sdk import json_save
from maxoptics.maxopt_sdk import (
    passive_eme_fd_result_chart,
    passive_eme_smatrix_chart
)

client = maxoptics.MosLibraryCloud()


def simulation(
    gds_file,
    gds_topcell,
    wavelength,
    grid,
    number_of_modes,
    run=False,
    source_view=False,
    extract=False,
    run_eme_propagation_sweep=True,
    project_name=''
):
    # -------general parameter
    from case_alias import (
        SiO2_SSC,
        eme_config
    )

    plot_path = str(Path(__file__).parent.as_posix()) + "/plots/EME_SSC_PROPAGATE/"

    meshPath = plot_path + "mesh"
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)
    if not os.path.exists(meshPath):
        os.makedirs(meshPath)

    project = client.create_project_as(project_name)

    # -----------1 eme config
    eme_config_private = {"dy": grid, "dz": grid, "wavelength": wavelength, "background_material": SiO2_SSC}
    eme_config.update(eme_config_private)
    eme = project.create_eme(**eme_config)

    eme.set_geometry(y=0, z=0.5, y_span=5.5, z_span=7)
    eme.set_cell_group(
        x_min=-103,
        cell_group=[
            {
                "cell_num": 1,
                "number_of_modes": number_of_modes,
                "sc": 0,  # [0:None, 1:Sub cell]
                "span": 2,
            },
            {
                "cell_num": 1,
                "number_of_modes": number_of_modes,
                "sc": 0,  # [0:None, 1:Sub cell]
                "span": 1,
            },
            {
                "cell_num": 30,
                "number_of_modes": number_of_modes,
                "sc": 1,  # [0:None, 1:Sub cell]
                "span": 200,
            },
            {
                "cell_num": 1,
                "number_of_modes": number_of_modes,
                "sc": 0,  # [0:None, 1:Sub cell]
                "span": 3,
            },
        ],
    )
    # --------2.set project and structure     -----------------
    struct_sio2 = project.gds_import(gds_file, gds_topcell, "1/0", "SiO2_SSC", -3, 0)
    struct_sio2['mesh_order'] = 2
    struct_si = project.gds_import(gds_file, gds_topcell, "2/0", "Si_SSC", 0, 0.2)
    struct_si['mesh_order'] = 3
    struct_sion = project.gds_import(gds_file, gds_topcell, "3/0", "SiON", 0, 3)
    struct_sion['mesh_order'] = 2

    # --------3.set waveform and source     -----------------

    # --------4.set port and monitor    -----------------------------------
    # --------4.1 set port    -----------------------------------
    # --------4.1.1 set portLeft    -----------------------------------
    portLeft = project.create_eme_port(
        x=-103, y=0, z=0.5, y_span=5.5, z_span=7,
        mode_selection=1,
        # [0:Fundamental Mode, 1:Fundamental TE Mode, 2:Fundamental TM Mode, 3:User Select, 4:User Import]
        port_location=0
    )

    # --------4.1.2 set portRight    -----------------------------------
    portRight = project.create_eme_port(
        x=103, y=0, z=0.5, y_span=5.5, z_span=7,
        mode_selection=1,
        # [0:Fundamental Mode, 1:Fundamental TE Mode, 2:Fundamental TM Mode, 3:User Select, 4:User Import]
        port_location=1
    )

    # --------4.1.3 set source port for eme    -----------------------------------
    eme.attrs.source_port = 0  # set portLeft as source port

    # --------4.2 set y_normal monitor    -----------------------------------
    y_normal = project.create_profile_monitor(
        name='y_normal',
        monitor_type=1,  # [0:x normal,1:y normal,2:z normal]
        x=0, y=0, z=0.5, x_span=206, z_span=7, y_span=0
    )

    # --------5.run project   -----------------------------------
    # --------5.1 run eme   -----------------------------------
    if run:
        start = time.time()
        print(
            "\x1b[6;30;42m"
            + "-------starting eme now !!!!------------- "
            + "\x1b[0m"
        )
        _ = project.run_eme_fde()
        result = project.run_eme_eme(dep_task=_.id)
        print(
            "\x1b[6;30;42m"
            + "[Finished in %(t)s mins for eme]"
            % {"t": round((time.time() - start) / 60, 2)}
            + "\x1b[0m"
        )

    # --------5.2 run eme propagation sweep  -----------------------------------
    if run_eme_propagation_sweep:
        emeAttrs = eme.attrs  # get attrs interface of eme
        emeAttrs.parameter = 2  # set group span 3 for sweep, start with 0 for group span 1
        emeAttrs.start = 50  # start position for eme sweep along with x forward direction
        emeAttrs.stop = 250  # stop position for eme sweep along with x forward direction
        emeAttrs.interval = 50  # interval length between two points
        # emeAttrs.number_of_points = 5 # number of points equals to number of interval + 1

        _ = project.run_eme_fde()  # run eme fde at the first step
        propagateResult = project.run_eme_propagation_sweep(dep_task=_.id)  # run eme propagation sweep at the second step

    # --------6.get source view    -----------------------------------
    if source_view:

        # --------6.1 get fde mode result of portRight    -----------------------------------
        # set the mode_selection and mode_index for fde mode
        selection = portRight.attrs.mode_selection
        portRight.attrs.mode_selection = 3
        mode_index = portRight.attrs.mode_index
        portRight.attrs.mode_index = 1

        # run function to get fde mode result of portRight
        resultFDE = project.run_calculate_modes(portRight)

        # show the fde mode result of portRight
        df = resultFDE.passive_fde_result_chart(
            "intensity", "E", "ABS", plotX='y', plotY='z', mode=0
        )

        # transfer result data to format for drawing
        tf = TaskResult(df, "intensity")
        x, y, Z = (
            tf.raw_data["horizontal"],
            tf.raw_data["vertical"],
            tf.raw_data["data"],
        )

        # draw the heatmap of portRight's fde mode
        heatmap(x, y, Z)
        plt.xlabel("x (μm)")
        plt.ylabel("y (μm)")
        plt.title("source_mode_profile")
        plt.savefig(plot_path + "00_source_modeprofile_fdeonly.jpg")
        plt.close()

        # reset the setting of mode_selection and mode_index
        portRight.attrs.mode_selection = selection
        portRight.attrs.mode_index = mode_index

        # --------6.2 get fde mode result of portLeft    -----------------------------------

        # set the mode selection and mode_index for fde mode
        selection = portLeft.attrs.mode_selection
        portLeft.attrs.mode_selection = 3
        mode_index = portLeft.attrs.mode_index
        portLeft.attrs.mode_index = 1

        # run function to get fde mode result of portLeft
        resultFDE = project.run_calculate_modes(portLeft)

        # show the fde mode result of portLeft
        df = resultFDE.passive_fde_result_chart(
            "intensity", "E", "ABS", plotX='y', plotY='z', mode=0
        )

        # transfer result data to format for drawing
        tf = TaskResult(df, "intensity")
        x, y, Z = (
            tf.raw_data["horizontal"],
            tf.raw_data["vertical"],
            tf.raw_data["data"],
        )

        # draw the heatmap of portLeft's fde mode
        heatmap(x, y, Z)
        plt.xlabel("x (μm)")
        plt.ylabel("y (μm)")
        plt.title("source_mode_profile")
        plt.savefig(plot_path + "01_output_modeprofile_fdeonly.jpg")
        plt.close()

        # reset the setting of mode_selection and mode_index
        portLeft.attrs.mode_selection = selection
        portLeft.attrs.mode_index = mode_index

        print(
            "=========================== generated source profile from FDE-only ================================="
        )

    # --------7.get result    -----------------------------------
    # --------7.1 get eme propagation sweep result    -----------------------------------

    """RESULT - Sweep"""
    if run_eme_propagation_sweep and extract:

        # set legendName list circular enumeration for S transmission rate
        legendName = ["S11", "S21", "S12", "S22"]

        # get the sweep result
        sParameterData = propagateResult.passive_eme_sweep_chart(
            "line", "S", "ABS^2", plotX="Group__span__3"
        )

        # get the interval points' list [50,100,150,200,250]
        emesweep_result = propagateResult.passive_eme_sweep_option('line')['propagation']

        # set the x index of sweep map
        x = emesweep_result

        # draw transmission rate on each interval point by cycle
        for i in range(4):
            # set each list of raw_data‘s data to y
            y = sParameterData.raw_data["data"][i]
            # get the DataFrame format of raw_data's data
            lineplot(dataframe=pd.DataFrame(data=y, index=x, columns=["sweep"]))
            # set the xlabel name of figure
            plt.xlabel("Group__span__3 (μm)")
            # set the ylabel name of figure
            plt.ylabel("Coupling efficiency")
            # set the title of figure
            plt.title("abs^2(" + legendName[i] + ")")
            # save the figure
            plt.savefig(plot_path + "11_eme_ssc_propagate_abs(" + legendName[i] + ").jpg")
            # clear the figure content
            plt.close()

            # save the raw_data's data to json format file
            json_save(os.path.join(plot_path, "11_eme_ssc_propagate_abs(" + legendName[i] + ").json"),
                      sParameterData.raw_data["data"][i]
                      )

    # --------7.2 get eme result    -----------------------------------
    if run and extract:
        # get the result of y_normal monitor with E and ABS
        df = passive_eme_fd_result_chart(
            "intensity",  # get heatmap
            dict(
                log=False,
                monitor=y_normal,  # monitor
                attribute="E",  # attribute [E,Ex,Ey,Ez,H,Hx,Hy,Hz,Px,Py,Pz,Energy density]
                operation="ABS",  # operation [ABS,ABS^2,Real,-Real]
                taskPath=Path(result.workspace),  # workspace path for getting result
            ),
            dict(plotX="x", plotY="z", y="0"),  # set the display figure xy index content
        )

        # transfer result data to format for drawing
        tf = TaskResult(df, "intensity")
        x, y, Z = (
            tf.raw_data["horizontal"],
            tf.raw_data["vertical"],
            tf.raw_data["data"],
        )
        # draw the result for eme y_normal monitor on heatmap
        heatmap(x, y, Z)
        plt.xlabel("x (μm)")
        plt.ylabel("z (μm)")
        plt.title("y_normal profile")
        plt.savefig(plot_path + "21_y_normal_eme.jpg")
        plt.close()

        """RESULT - Smatrix"""
        # get the result of smatrix with table format and ABS^2 operation
        df = passive_eme_smatrix_chart(
            "table",
            dict(
                operation="ABS^2",
                taskPath=Path(result.workspace),
            ),
            dict(),
        )

        # transfer result data to format for print
        tf = TaskResult(df, "table")
        pprint(tf.raw_data["data"])
        pprint(tf.DataFrame)
        T = tf.DataFrame[0][1]  # column:1,row 2
        R = tf.DataFrame[0][0]  # column:1,row 1
        print("Transmission=", T)
        print("Reflection=", R)
        json_save(os.path.join(plot_path, "Transmission.json"), dict(T=str(T)))
        json_save(os.path.join(plot_path, "Reflection.json"), dict(R=str(R)))


if __name__ == "__main__":
    start = time.time()
    # -----------------------------
    path = str(Path(__file__).parent.as_posix())
    gds_file = path + "/gds/" + "SSC.gds"
    project_name = "EME_SSC_PROPAGATE"  # + currentDate
    simulation(
        extract=True,
        source_view=True,
        run_eme_propagation_sweep=True,
        run=True,
        gds_file=gds_file,
        gds_topcell="SSC",
        number_of_modes=10,
        grid=0.02,
        wavelength=1.5,
        project_name=project_name
    )
    # ----------------------------
    print(
        "\x1b[6;30;42m"
        + "[Finished in %(t)s mins]"
        % {"t": round((time.time() - start) / 60, 2)}
        + "\x1b[0m"
    )
