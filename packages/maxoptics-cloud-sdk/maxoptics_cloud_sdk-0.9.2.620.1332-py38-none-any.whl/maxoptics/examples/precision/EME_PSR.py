import os
from pathlib import Path
import maxoptics
from maxoptics.var.MosIO.Network.MosClient import Material,Waveform
from matplotlib import pyplot as plt
from maxoptics.core.plot.heatmap import heatmap
from case_alias import client,Si_PSR,SiO2_PSR,Air
import json,time



def simulation(gds_file, gds_topcell,run=True,wavelength=1.5,grid=0.02,inMode=1):
    plot_path = str(Path(__file__).parent.as_posix()) + '/plots/PSR/'
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)
    #--------------------------------create project
    EME_PSR=client.create_project_as("EME_PSR")
    #--------------------------------gds import
    EME_PSR.gds_import(gds_file,gds_topcell, "1/0", SiO2_PSR, -4, 0)      
    EME_PSR.gds_import(gds_file,gds_topcell, "2/0", Si_PSR, 0, 0.22) 
    
    eme_config = {
        'background_material': Air,
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
        'z':0,
        'y_span':8,
        'z_span':6,
        'y':1.256,
        'x_min': -30.5,
    }
    #---------------------create eme
    eme=EME_PSR.create_eme(**eme_config)
    #---------------------eme append_cell new method
    eme.append_cell(1, 1, 10, 0,fix='x_min')     # (span,cell_number,number_of_modes,sub_cell_method,fix=X_Min(cell_geometry.x_min))
    eme.append_cell(6, 6, 10, 1,fix='x_min')
    eme.append_cell(30, 6, 10, 1,fix='x_min')
    eme.append_cell(12, 6, 10, 1,fix='x_min')
    eme.append_cell(8.9, 1, 10, 0,fix='x_min')
    eme.append_cell(5, 40, 10, 1,fix='x_min')
    eme.append_cell(5.2, 1, 10, 0,fix='x_min')
    eme.append_cell(5, 1, 10, 0,fix='x_min')
    #-----------------------create eme_port
    portLeft=EME_PSR.create_eme_port(name='portLeft',port_location=0,mode_selection=inMode)
    portTE=EME_PSR.create_eme_port(name='portTE',port_location=1,y_span=2,z_span=2,z=0.11,y=0,use_full_simulation_span=0,mode_selection=1)
    portTM=EME_PSR.create_eme_port(name='portTM',port_location=1,y_span=2,z_span=2,z=0.11,y=2.6785,use_full_simulation_span=0,mode_selection=1)
    portTE2=EME_PSR.create_eme_port(name='portTE2',port_location=1,y_span=2,z_span=2,z=0.11,y=0,use_full_simulation_span=0,mode_selection=2)
    portTM2=EME_PSR.create_eme_port(name='portTM2',port_location=1,y_span=2,z_span=2,z=0.11,y=2.6785,use_full_simulation_span=0,mode_selection=2)
    #----------------------create Mesh
    EME_PSR.create_mesh(
        name = 'Mesh',
        x=6.05,
        x_span=73.1,
        y=1.256,
        y_span=5,
        z=0.11,
        z_span=0.4,
        override_y_mesh=1, #trun on dy setting
        override_z_mesh=1, #turn on dz setting
        dy=0.01,
        dz=0.01
    )
    #----------------------craete eme_monitor
    monitor = EME_PSR.create_profile_monitor(
        name = 'Mesh',
        monitor_type=maxoptics.Z_Normal,
        x=6.05,
        x_span=73.1,
        y=1.256,
        y_span=8,
        z=0.11,
    )
    #-------------------------save project
    EME_PSR.save()

    if run:
        t1 = EME_PSR.run_eme_fde()
        t2 = EME_PSR.run_eme_eme(dep_task=t1.id)
        data = t2.passive_eme_smatrix_chart("table", "S", "ABS^2")

        def json_save(path, data):
            with open(path, "w") as f:
                json.dump(data, f)

        TE_outTE=(data.DataFrame[0][1])#column:1,row 2
        TE_outTM=(data.DataFrame[0][2])#column:1,row 3
        TM_outTE=(data.DataFrame[0][3])#column:1,row 4
        TM_outTM=(data.DataFrame[0][4])#column:1,row 5
        print("TE_outTE=",TM_outTE)
        print("TE_outTM=",TE_outTE)
        print("TM_outTE=",TM_outTM)
        print("TM_outTM=",TE_outTM)
        json_save(os.path.join(plot_path,f"{wavelength}TM_outTE.json"),TM_outTE)
        json_save(os.path.join(plot_path,f"{wavelength}TE_outTE.json"),TE_outTE)
        json_save(os.path.join(plot_path,f"{wavelength}TM_outTM.json"),TM_outTM)
        json_save(os.path.join(plot_path,f"{wavelength}TE_outTM.json"),TE_outTM)
        
        print(data.DataFrame)

        data2=t2.passive_eme_monitor_chart(
            "intensity", monitor, "E", "ABS", x="plotX", y="plotY"
        )
        x, y, Z = data2.raw_data["horizontal"], data2.raw_data["vertical"], data2.raw_data["data"]
        fig = heatmap(x, y, Z)
        plt.xlabel("x (μm)")
        plt.ylabel("y (μm)")
        plt.title("z_normal profile")
        plt.savefig(plot_path + f"{wavelength}z_normal_eme.jpg")
        plt.clf()

if __name__ == '__main__':
    start = time.time()
    # -----------------------------
    path = str(Path(__file__).parent)
    gds_file = path + '/gds/' + 'PSR.gds'
  
    simulation( run=True,wavelength=1.5,grid=0.2,gds_file=gds_file, gds_topcell="PSR")
    print('\x1b[6;30;42m' + '[Finished in %(t)s mins]' % {'t': round((time.time() - start)/60, 2)} + '\x1b[0m')

