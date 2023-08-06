import maxoptics
from maxoptics.var.MosIO.Network.MosClient import Material,Waveform

#------------connect server
client=maxoptics.MosLibraryCloud()
#------------create material
client.ensure_materials(
    [Material("Si_PSR",{1.55e-06:[3.455,0]},mesh_order=2)],
    "passive",
    replace=True
)
client.ensure_materials(
    [Material("SiO2_PSR",{1.55e-06:[1.445,0]},mesh_order=1)],
    "passive",
    replace=True
)
client.ensure_materials(
    [Material("Si_SSC",{1.55e-06:[3.476,0]},mesh_order=2)],
    "passive",
    replace=True
)
client.ensure_materials(
    [Material("SiO2_SSC",{1.55e-06:[1.465,0]},mesh_order=1)],
    "passive",
    replace=True
)
client.ensure_materials(
    [Material("SiON_SSC",{1.55e-06:[1.5,0]},mesh_order=2)],
    "passive",
    replace=True
)
client.ensure_materials(
    [Material("Si_3472",{1.55e-06:[3.472,0]},mesh_order=2)],
    "passive",
    replace=True
)
client.ensure_materials(
    [Material("SiO2_1444",{1.55e-06:[1.444,0]},mesh_order=1)],
    "passive",
    replace=True
)
#-------------Binding material
Si_PSR=client.user_materials["Si_PSR"]
SiO2_PSR=client.user_materials["SiO2_PSR"]
Si_SSC=client.user_materials["Si_SSC"]
SiO2_SSC=client.user_materials["SiO2_SSC"]
SiON_SSC=client.user_materials["SiON_SSC"]
Si_3472=client.user_materials["Si_3472"]
SiO2_1444=client.user_materials["SiO2_1444"]
Air = client.public_materials["Air"]
#-------------create waveforms
client.ensure_waveforms(
    [Waveform("waveform1550", 1.55, 0.1, "wavelength")],
    replace=True,
)
#------------Binding waveform
waveform = client.user_waveforms["waveform1550"]

