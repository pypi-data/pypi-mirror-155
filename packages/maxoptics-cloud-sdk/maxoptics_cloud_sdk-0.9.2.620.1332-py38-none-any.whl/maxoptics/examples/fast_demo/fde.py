from pathlib import Path
import matplotlib.pyplot as plt
import os

import maxoptics.maxopt_sdk as sdk
from maxoptics.maxopt_sdk import passive_fde_result_chart
from maxoptics.maxopt_sdk import FDE, TaskResult

path = str(Path(__file__).parent.as_posix())
plot_path = str(Path(__file__).parent.as_posix()) + '/plots/FDE/'
if not os.path.exists(plot_path):
    os.makedirs(plot_path)
gds_file = path + '/gds/' + 'fast_test.gds'
project_address = path + '/project/'
sdk.init_materials('./case_materials.json')
Si = sdk.Material.find('Si')
SiO2 = sdk.Material.find('SiO2')
Air = sdk.Material.find('Air')

project = sdk.GdsModel(gds_file)
# add rectangle((center_x,center_y),x_span,y_span,rotation_angle,z_min,z_max,material)
project.add_rectangle((0, 0), 6, 2, 0, -0.1, 0.1, Si)
project.gds_import("EXTEND_1", (3, 0), SiO2, 0, 0.1)
# Grid vertical viewed cross section must be the same with vertical simulation span. For example, dx=x_span.
vertical_grid = 0.02
fde = FDE()
fde['use_max_index'] = 1
fde.update(
    solver_type=0,
    dx=vertical_grid,
    dy=0.02,
    dz=0.02,
    background_material=Air,
)
fde.set_geometry(x=-1, x_span=0, y=0, y_span=3, z=0, z_span=2)

fde.add_structure(project.structures)

result = fde.run()

"""RESULT"""

df = passive_fde_result_chart("intensity",
                              dict(
                                  attribute="E",
                                  operation="ABS",
                                  taskPath=Path(result.workspace).parent / Path(result.workspace).name),
                              dict(y="plotX", z="plotY", x=0, mode=0)
                              )

"""PLOT"""
tf = TaskResult(df, "intensity")
x, y, Z = (
    tf.raw_data["horizontal"],
    tf.raw_data["vertical"],
    tf.raw_data["data"],
)
sdk.heatmap(x, y, Z)
plt.xlabel("x (μm)")
plt.ylabel("y (μm)")
plt.title("FDE, x=-1")
plt.savefig(plot_path + "test_FDE_mode0.jpg")
plt.clf()

df = passive_fde_result_chart("intensity",
                              dict(
                                  attribute="E",
                                  operation="ABS",
                                  taskPath=Path(result.workspace).parent / Path(result.workspace).name),
                              dict(y="plotX", z="plotY", x=0, mode=1)
                              )

"""PLOT"""
tf = TaskResult(df, "intensity")
x, y, Z = (
    tf.raw_data["horizontal"],
    tf.raw_data["vertical"],
    tf.raw_data["data"],
)
sdk.heatmap(x, y, Z)
plt.xlabel("x (μm)")
plt.ylabel("y (μm)")
plt.title("FDE, x=-1")
plt.savefig(plot_path + "test_FDE_mode1.jpg")
plt.clf()
