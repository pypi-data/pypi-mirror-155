import maxoptics
from case_alias import SiO2_SSC, SiON, Si_SSC


def simulation(wavelength=1.5, run=False, gridy=0.002, gridz=0.002, mesh=False, x=0):
    client = maxoptics.MosLibrary()

    Air = client.public_materials["Air"]
    # 1. creat project & import gds
    FDE_SSC_i1 = client.create_project_as("FDE_SSC_i1", log_folder="./logs")

    s1 = FDE_SSC_i1.gds_import("./gds/SSC.gds", "SSC", "1/0", SiO2_SSC, -3, 0)
    s2 = FDE_SSC_i1.gds_import("./gds/SSC.gds", "SSC", "2/0", Si_SSC, 0, 0.2)
    s3 = FDE_SSC_i1.gds_import("./gds/SSC.gds", "SSC", "3/0", SiON, 0, 3)
    s1["mesh_order"] = 2
    s2["mesh_order"] = 3
    s3["mesh_order"] = 2

    # 2. create fde
    fde_config = {
        "solver_type"        : 0,  # [0: XNormal, 1: YNormal, 2:ZNormal]
        "x"                  : x,
        "y"                  : 0,
        "z"                  : 0,
        "x_span"             : 0,
        "y_span"             : 7,
        "z_span"             : 5.5,
        "define_x_mesh"      : 1,  # [0: Number of Mesh Cells, 1: Maximum Mesh Step]
        "define_y_mesh"      : 1,  # [0: Number of Mesh Cells, 1: Maximum Mesh Step]
        "dxd"                : 0.02,
        "dyd"                : 0.02,
        "refinement_type"    : 1,  # [0: Staircase, 1: Advanced Volume Average, 2: Dielectric Volume Average, 4: CP-EP]
        "background_material": Air,
        "use_max_index"      : 0,  # [0: False , 1: True]
        "n"                  : 3  # users don't need to set n when use_max_index is 1
    }

    fde = FDE_SSC_i1.create_fde(**fde_config)

    # 3. create mesh
    if mesh:
        FDE_SSC_i1.create_mesh(
            name='Mesh',
            x=x,
            x_span=1,
            y=0,
            y_span=1,
            z=0.1,
            z_span=0.4,
            # override_x_mesh=0,  # override dx mesh switch [0:False, 1:True]
            override_y_mesh=1,  # override dy mesh switch [0:False, 1:True]
            override_z_mesh=1,  # override dz mesh switch [0:False, 1:True]
            # dx=0.02,  # dx maximum mesh step
            dy=gridy,  # dy maximum mesh step
            dz=gridz  # dz maximum mesh step
        )

    # 4. save project & run simulation
    FDE_SSC_i1.save()

    if run:
        fdeAttrs = fde.attrs
        fdeAttrs.wavelength = wavelength
        fdeAttrs.number_of_trial_modes = 3
        fdeResult = FDE_SSC_i1.run_fde()
        fdeData = fdeResult.passive_fde_result_chart(target="table",
                                                     attribute="E",
                                                     operation="ABS",
                                                     )
        data = [_[1] for _ in fdeData.data]
        print(f'Neff_Wavelength({wavelength}):', data)
        print(fdeData.DataFrame)


if __name__ == "__main__":
    simulation(run=True, mesh=True, x=-102.5)
