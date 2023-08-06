import os
from pathlib import Path
from secrets import choice
import maxoptics
from maxoptics.var.MosIO.Network.MosClient import Material,Waveform
import pandas as pd
from matplotlib import pyplot as plt
# from seaborn import lineplot
import json,time
from maxoptics.core import heatmap, lineplot
from case_alias import client,Si_SSC,SiO2_SSC,SiON_SSC

def simulation(gds_file, gds_topcell,run=True,wavelength=1.5,grid=0.2):
    plot_path = str(Path(__file__).parent.as_posix()) + '/plots/SSC/'
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)


    EME_SSC=client.create_project_as("EME_SSC")

    struct_sio2 =EME_SSC.gds_import(gds_file,gds_topcell, '1/0', SiO2_SSC, -3, 0)
    struct_sio2["mesh_order"] = 1      
    struct_si =EME_SSC.gds_import(gds_file,gds_topcell, '2/0', Si_SSC, 0, 0.2)
    struct_si["mesh_order"] = 2
    struct_sion =EME_SSC.gds_import(gds_file,gds_topcell, '3/0', SiON_SSC, 0, 3)
    struct_sion["mesh_order"] = 1                         
    
    eme_config = {
        'background_material': SiO2_SSC,
        'wavelength': wavelength,
        'define_y_mesh': 1,  # boolean parameter. 1 allow to set dy.
        'define_z_mesh': 1,
        'dy': grid,  # um
        'dz': grid,  # um
        'min_mesh_step': 1e-5,  # um
        'refinement_type': 1,   #1:Dielectric volume average
        'grading_factor': 1.41,
        'y_min_bc': 1,
        'y_max_bc': 1,
        'z_min_bc': 1,
        'z_max_bc': 1,
        'z':0.5,
        'y_span':5.5,
        'z_span':7,
        'x_min':0,
        'y':0,
        'x_min': -103,
    }
    eme=EME_SSC.create_eme(**eme_config)
    eme.append_cell(2, 1, 10, 0,fix='x_min')
    eme.append_cell(1, 1, 10, 0,fix='x_min')
    eme.append_cell(200, 30, 10, 1,fix='x_min')
    eme.append_cell(3, 1, 10, 0,fix='x_min')
    EME_SSC.create_eme_port(name='portLeft',port_location=0,y_span=5.5,z_span=7,z=0.5,y=0,mode_selection=1)
    EME_SSC.create_eme_port(name='portRight',port_location=1,y_span=5.5,z_span=7,z=0.5,y=0,mode_selection=1)
    #-------------------------------setting eme analysis
    emeAttrs = eme.attrs
    emeAttrs.propagation = 1  # [0:False, 1:True]
    emeAttrs.parameter=2      #choose group to sweep
    emeAttrs.start = 50
    emeAttrs.stop = 250
    emeAttrs.interval=50


    monitor = EME_SSC.create_profile_monitor(
        name = 'z_normal',
        monitor_type=maxoptics.Z_Normal,
        x=0,
        x_span=206,
        y=0,
        y_span=5.5,
        z=0,
    )

    EME_SSC.save()

    if run:
        t1 = EME_SSC.run_eme_fde()
        t2 = EME_SSC.run_eme_propagation_sweep(dep_task=t1.id)

        from maxoptics.var.visualizer import EMEResultHandler
        t2_sub = EMEResultHandler(t2.task_id, t2.project, t2.config, 2)
        data=t2_sub.passive_eme_monitor_chart(
            "intensity", monitor, "E", "ABS", x="plotX", y="plotY"
        )

        x, y, Z = data.raw_data["horizontal"], data.raw_data["vertical"], data.raw_data["data"]
        fig = heatmap(x, y, Z)
        plt.xlabel("x (μm)")
        plt.ylabel("y (μm)")
        plt.title("z_normal profile")
        plt.savefig(plot_path + f"{wavelength}z_normal_eme.jpg")
        plt.clf()

        def json_save(path, data):
            with open(path, "w") as f:
                json.dump(data, f)
        
        emePropagationData = t2.passive_eme_sweep_chart(target="line",
                                                                            attribute="S",
                                                                            operation="ABS^2"
                                                                            )
        df = pd.DataFrame({'S21': emePropagationData.raw_data["data"][2]})
        # lineplot(data=df)
        plt.plot(df['S21'], "r*-",label='S21')
        plt.xlabel("group span 3")
        plt.ylabel("")
        plt.title("abs^2(" + "S21" + ")")
        plt.savefig(plot_path + "_abs^2(" + 'S21' + ")_line.jpg")
        # plt.show()
        plt.clf()
        # json_save(os.path.join(plot_path "01"  + "_abs^2(" + "S21" + ")_line.json"),
        #             emePropagationData.raw_data
        #             )
        json_save(os.path.join(plot_path, "01" + "_abs^2(" + 'S21' + ")_line.json"),
                      emePropagationData.raw_data
                      )

if __name__ == '__main__':
    start = time.time()
    # -----------------------------
    path = str(Path(__file__).parent)
    gds_file = path + '/gds/' + 'SSC.gds'
  
    simulation(run=True,wavelength=1.5,grid=0.02,gds_file=gds_file, gds_topcell="SSC")
    print('\x1b[6;30;42m' + '[Finished in %(t)s mins]' % {'t': round((time.time() - start)/60, 2)} + '\x1b[0m')

