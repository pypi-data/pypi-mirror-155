import json
import os
from pathlib import Path
import time
from maxoptics.var.MosIO.Network.MosClient import Material,Waveform
import maxoptics
from case_alias import client,Si_3472, SiO2_1444,Air,waveform
from maxoptics.core import heatmap
from matplotlib import pyplot as plt
from seaborn import lineplot

def json_save(path, data):
    with open(path, "w") as f:
        json.dump(data, f)
        
def simulation(gds_file, gds_topcell, run=True, grids_per_lambda=15):
    plot_path = str(Path(__file__).parent.as_posix()) + '/plots/Halfring/'
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)

    FDTD_halfring=client.create_project_as("FDTD_HalfRing")

    FDTD_halfring.gds_import(gds_file,gds_topcell, "1/0", SiO2_1444, -4, 0)      
    FDTD_halfring.gds_import(gds_file,gds_topcell, "2/0", Si_3472, 0, 0.18) 

    fdtd_config={
        'x': 0,
        'y': 0,
        'z': 0,
        'x_span': 11,
        'y_span': 12,
        'z_span': 8,
        'background_material': Air,
        'simulation_time': 10000,  # default 1000fs
        'mesh_type': 0,            # set FDTD mesh_type [0:Auto non-uniform, 1:Uniform]
        'cells_per_wavelength':  grids_per_lambda,  # set FDTD's cells_per_wavelength = 2 + LumMesh*4
        'refinement_type': 1,      # set FDTD's refinement_type [0:Staircase, 1:Average volume average, 2:Dielectric volume average, 3:VP-EP, 4:CP-EP]
        'grading_factor': 1.2,     # higher factor brings wider grids at low index material, typical 1.2
        'x_min_bc': 0,             # set FDTD's xyz boundary conditions [0:PML, 1:PEC]
        'x_max_bc': 0,
        'y_min_bc': 0,
        'y_max_bc': 0,
        'z_min_bc': 0,
        'z_max_bc': 0,
    }

    source_config={
        'x': -4,
        'y': 3.6,
        'z': 0.09,
        'x_span': 0,
        'y_span': 3,
        'z_span': 2,
        'x_min_bc': 1,       # set ModeSource's xyz boundary conditions
        'x_max_bc': 1,
        'y_min_bc': 1,
        'y_max_bc': 1,
        'z_min_bc': 1,
        'z_max_bc': 1,
        'injection_axis': 0,  # set ModeSource's injection_axis param [0:x-axis, 1:y-axis ,2:z-axis ]
        'direction': 0,       # set ModeSource's direction param [0:Forward, 1:Backward]
        'mode_selection': 0,  # set ModeSource's mode_selection [0:fundamental mode, 1:fundamental TE mode, 2:fundamental TM mode, 3:user select]
        # mode_index calculatored in mode_selection which rank by refractive index.You don't have to write this when mode_selection is not 'user select'
        # 'mode_index': 1,
        # 'number_of_trial_modes': 5,      # set number of trial modes
        # set ModeSource's waveform id
        'waveform_id':waveform["id"],
    }

    FDTD_halfring.create_fdtd(**fdtd_config)

    # ----------- Add ModeSource
    FDTD_halfring.create_mode_source(**source_config)

    # ----------- Add Monitor
    z_normal = {
        'x': fdtd_config["x"], 'y': fdtd_config["y"], 'z': fdtd_config["z"], 'x_span': fdtd_config["x_span"], 'y_span': fdtd_config["y_span"], 'z_span': 0,
        'use_wavelength_spacing': 1,         # use wavelength_spacing [1:on, 0:off]
        "override_global_options": 1,
        'use_source_limits': 0,              # source_limits [1:on, 0:off]
        'frequency_points': 3, "wavelength_center": 1.55, "wavelength_span": 0.5,
        "spacing_type": 0,   # [0:wavelength, 1:frequency]
        "spacing_limit": 0}  # [0:min/max, 1:center/span]

    monitor_T = {
        'x': 4, 'y': 3.6, 'z': 0.09, 'x_span': 0, 'y_span': 3, 'z_span': 2,
        'use_wavelength_spacing': 1, 'use_source_limits': 0, "spacing_type": 0, "spacing_limit": 0}
    monitor_C = {
        'x': 3.1, 'y': -3, 'z': 0.09, 'x_span': 3, 'y_span': 0, 'z_span': 2,
        'use_wavelength_spacing': 1, 'use_source_limits': 0, "spacing_type": 0, "spacing_limit": 0}
    monitor_R = {
        'x': -4.21, 'y': 3.6, 'z': 0.09, 'x_span': 0, 'y_span': 3, 'z_span': 2,
        'use_wavelength_spacing': 1, 'use_source_limits': 0, "spacing_type": 0, "spacing_limit": 0}

    monitorThrough=FDTD_halfring.create_power_monitor("T",**monitor_T)
    monitorCross=FDTD_halfring.create_power_monitor("C",**monitor_C)
    monitorReflection=FDTD_halfring.create_power_monitor("R",**monitor_R)
    monitorZNormal=FDTD_halfring.create_power_monitor("R",**z_normal)

    FDTD_halfring.save()
     
    if run:
        start = time.time()
        print("\x1b[6;30;42m" + "--- starting FDTD now !!!! ---" + "\x1b[0m")

        fdtdResult = FDTD_halfring.run_fdtd()

        stop = time.time()
        print("\x1b[6;30;42m" + "[Finished in %(t)s mins for FDTD]" % {"t": round((stop - start) / 60, 2)} + "\x1b[0m")

    
        monitorZNormalData = fdtdResult.passive_fdtd_fd_result_chart("intensity", monitorZNormal, "E", "ABS", x="plotX",
                                                                     y="plotY", z=0, wavelength=0
                                                                     )
        x, y, Z = monitorZNormalData.raw_data["horizontal"], monitorZNormalData.raw_data["vertical"], \
                  monitorZNormalData.raw_data["data"]
        heatmap(x, y, Z)
        plt.xlabel("x (μm)")
        plt.ylabel("y (μm)")
        plt.title("z_normal_1.5 heatmap with z=0")
        plt.savefig(plot_path + "01_top_profile.jpg")
        # plt.show()
        plt.clf()

        monitorZNormalData2 = fdtdResult.passive_fdtd_fd_result_chart("intensity", monitorZNormal, "E", "ABS", x="plotX",
                                                                     y="plotY", z=0, wavelength=1
                                                                     )
        x, y, Z = monitorZNormalData2.raw_data["horizontal"], monitorZNormalData2.raw_data["vertical"], \
                  monitorZNormalData2.raw_data["data"]
        heatmap(x, y, Z)
        plt.xlabel("x (μm)")
        plt.ylabel("y (μm)")
        plt.title("z_normal_1.55 heatmap with z=0")
        plt.savefig(plot_path + "02_top_profile.jpg")
        # plt.show()
        plt.clf()

        monitorZNormalData3 = fdtdResult.passive_fdtd_fd_result_chart("intensity", monitorZNormal, "E", "ABS", x="plotX",
                                                                     y="plotY", z=0, wavelength=2
                                                                     )
        x, y, Z = monitorZNormalData3.raw_data["horizontal"], monitorZNormalData3.raw_data["vertical"], \
                  monitorZNormalData3.raw_data["data"]
        heatmap(x, y, Z)
        plt.xlabel("x (μm)")
        plt.ylabel("y (μm)")
        plt.title("z_normal_1.6 with z=0")
        plt.savefig(plot_path + "03_top_profile.jpg")
        # plt.show()
        plt.clf()


        monitorThroughData = fdtdResult.passive_fdtd_fd_result_chart(target="line",
                                                                     monitor=monitorThrough,
                                                                     attribute="T",
                                                                     operation="ABS",
                                                                     x=0,
                                                                     y=0,
                                                                     z=0,
                                                                     wavelength="plotX"
                                                                     )
        lineplot(data=monitorThroughData.DataFrame)
        plt.xlabel("wavelength (μm)")
        plt.ylabel("Transmission_Through")
        plt.title("HalfRing FDTD, cloud sdk v0.9.2")
        plt.savefig(plot_path + "021_Trans_ThroughVsLambda_power.jpg")
        # plt.show()
        plt.clf()
        json_save(os.path.join(plot_path, "hfr_Through.json"), monitorThroughData.raw_data)

        monitorCrossData = fdtdResult.passive_fdtd_fd_result_chart(target="line",
                                                                   monitor=monitorCross,
                                                                   attribute="T",
                                                                   operation="ABS",
                                                                   x=0,
                                                                   y=0,
                                                                   z=0,
                                                                   wavelength="plotX"
                                                                   )
        lineplot(data=monitorCrossData.DataFrame)
        plt.xlabel("wavelength (μm)")
        plt.ylabel("Transmission_Cross")
        plt.title("HalfRing FDTD, cloud sdk v0.9.2")
        plt.savefig(plot_path + "031_Trans_CrossVsLambda_power.jpg")
        # plt.show()
        plt.clf()
        json_save(os.path.join(plot_path, "hfr_Cross.json"), monitorCrossData.raw_data)

        monitorReflectionData = fdtdResult.passive_fdtd_fd_result_chart(target="line",
                                                                        monitor=monitorReflection,
                                                                        attribute="T",
                                                                        operation="ABS",
                                                                        x=0,
                                                                        y=0,
                                                                        z=0,
                                                                        wavelength="plotX"
                                                                        )
        lineplot(data=monitorReflectionData.DataFrame)
        plt.xlabel("wavelength (μm)")
        plt.ylabel("Reflection")
        plt.title("HalfRing FDTD, cloud sdk v0.9.2")
        plt.savefig(plot_path + "041_Trans_ReflVsLambda_power.jpg")
        # plt.show()
        plt.clf()
        json_save(os.path.join(plot_path, "hfr_Refl.json"), monitorReflectionData.raw_data)


if __name__ == '__main__':
    start = time.time()
    # -----------------------------
    path = str(Path(__file__).parent)
    gds_file = path + '/gds/' + 'hfr.gds'
  
    simulation( run=True,gds_file=gds_file, gds_topcell="HalfRing")
    print('\x1b[6;30;42m' + '[Finished in %(t)s mins]' % {'t': round((time.time() - start)/60, 2)} + '\x1b[0m')


   