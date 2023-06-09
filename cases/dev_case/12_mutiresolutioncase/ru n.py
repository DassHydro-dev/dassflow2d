# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""


import dassflow2d as df2d
import numpy as np
import pandas as pd
import sys
import os
import random
from matplotlib.colors import ListedColormap
os.chdir("/home/livillenave/Documents/distant/dassflow2d-wrap/code/bin_A")


#-------------------------------------------
# FIRST : CHECK AVAILABLE CASE
# Load python data
#-------------------------------------------
run_type = "direct"
# initialise fortran instance, and python corrponding data
model = df2d.dassflowmodel(bin_dir = os.getcwd(), 
                           hdf5_path=os.getcwd()+"/res/simu.hdf5", 
                           run_type = run_type,
                           clean=True)

# SET UP MANNING VALUE
model.config["use_obs"] = 0
model.config["w_obs"] = 1
model.config.set()

if model.mpi[0]==0:
    model.init_all()
else:
	model.init_fortran_mpi()

model.run()
model.save_all()


df2d.wrapping.call_model.clean_model(self = model.kernel)
#
#model.boundary.plot(what = "meshing")
#model.meshing.plot(my_scalar=init_values["bathy"], title_plot ="Bathymetry")
#model.meshing.plot(my_scalar=init_values["manningALPHA"], title_plot ="land_use")
#
#
#model.meshing.plot(my_scalar=init_values["h"], title_plot ="initial h")
#model.meshing.plot(my_scalar=init_values["u"], title_plot ="initial u")
#model.meshing.plot(my_scalar=init_values["v"], title_plot ="initial v")


init_values = model.outputs.all_res[0].copy()
reference_manning = model.param.friction.manning.copy()

df2d.wrapping.call_model.clean_model(self = model.kernel)



#-------------------------------------------
# SECOND : GENERATE  TRUE RUN
#-------------------------------------------

x_coord = init_values["x"]
y_coord = init_values["y"]

# INPUTS
run_type = "direct"
print(init_values)
print(reference_manning)

true_mesh_corresp = np.arange(1, len(reference_manning["mesh_correspondance"])+1,
                              1, dtype= "int32" )
true_values =0.01 + np.array(x_coord)/20000 + abs(50 - np.array(y_coord)) / 10000
# random.random() generate a number between 0 and 1


# initialise fortran instance, and python corrponding data
model = df2d.dassflowmodel(bin_dir = os.getcwd(), 
                           hdf5_path=os.getcwd()+"/res/simu.hdf5", 
                           run_type = run_type,
                           clean=True)

# SET UP MANNING VALUE
model.config["use_obs"] = 0
model.config["w_obs"] = 1
model.config.set()

model.init_all()

model.param.friction.manning["mesh_correspondance"] = true_mesh_corresp
model.param.friction.manning["patch_correspondance"] = true_mesh_corresp
model.param.friction.manning["patch_value"] = true_values
model.param.set()
model.run()
model.save_all()

df2d.wrapping.call_model.clean_model(self = model.kernel)

#
os.chdir(model.bin_dir)
os.system(f"mkdir obs")
os.system(f"cp ./res/obs/* ./obs")

os.system(f"mkdir hdf5_file")
os.system(f"mv ./res/simu.hdf5 ./hdf5_file/true_simu.hdf5")






#-------------------------------------------
# THIRD : PREPARE PATCHES FOR INFERENCE
#-------------------------------------------
x_coord = init_values["x"]
y_coord = init_values["y"]

xmin, xmax=0,1000
ymin, ymax=0,100

my_square = dict()
my_square["xmin"],my_square["xmax"]=xmin, xmax
my_square["ymin"],my_square["ymax"]=ymin, ymax

def half_cut(my_square):
    
    xmin, xmax = my_square["xmin"],my_square["xmax"]
    ymin, ymax = my_square["ymin"],my_square["ymax"]
    
    xmin1=xmin
    xmax1=(xmax+xmin)/2    
    xmin2=xmax1 
    xmax2=xmax
    
    ymin1=ymin
    ymax1=(ymax+ymin)/2    
    ymin2=ymax1 
    ymax2=ymax
    
    all_squares=dict()
    
    all_squares[1] =dict()
    all_squares[1]["xmin"],all_squares[1]["xmax"]=xmin1, xmax1
    all_squares[1]["ymin"],all_squares[1]["ymax"]=ymin1, ymax1
    
    
    all_squares[2] =dict()
    all_squares[2]["xmin"],all_squares[2]["xmax"]=xmin2, xmax2
    all_squares[2]["ymin"],all_squares[2]["ymax"]=ymin2, ymax2
    
    all_squares[3] =dict()
    all_squares[3]["xmin"],all_squares[3]["xmax"]=xmin1, xmax1
    all_squares[3]["ymin"],all_squares[3]["ymax"]=ymin2, ymax2
    
    all_squares[4] =dict()
    all_squares[4]["xmin"],all_squares[4]["xmax"]=xmin2, xmax2
    all_squares[4]["ymin"],all_squares[4]["ymax"]=ymin1, ymax1
    
    return( all_squares[1],  all_squares[2], all_squares[3], all_squares[4])


patch_uniform = dict()
patch_uniform[0] = my_square

patch_lvl2    = dict()
patch_lvl2[0] = {'xmin': 0,  'xmax': 100, 'ymin': 0, 'ymax': 100}
patch_lvl2[1] = {'xmin': 100, 'xmax': 200, 'ymin': 0, 'ymax': 100}
patch_lvl2[2] = {'xmin': 200, 'xmax':300, 'ymin': 0, 'ymax': 100}
patch_lvl2[3] = {'xmin': 300, 'xmax': 400, 'ymin': 0, 'ymax': 100}
patch_lvl2[4] = {'xmin': 400, 'xmax': 500, 'ymin': 0, 'ymax': 100}
patch_lvl2[5] = {'xmin': 500, 'xmax': 600, 'ymin': 0, 'ymax': 100}
patch_lvl2[6] = {'xmin': 600, 'xmax': 700, 'ymin': 0, 'ymax': 100}
patch_lvl2[7] = {'xmin': 700, 'xmax': 800, 'ymin': 0, 'ymax': 100}
patch_lvl2[8] = {'xmin': 800, 'xmax': 900, 'ymin': 0, 'ymax': 100}
patch_lvl2[9] = {'xmin': 900, 'xmax': 1000, 'ymin': 0, 'ymax': 100}

patch_lvl3 = dict()
count=0
for i in range(len(patch_lvl2)):
    sq1,sq2,sq3,sq4=half_cut(patch_lvl2[i])
    patch_lvl3[count]=sq1
    patch_lvl3[count+1]=sq2
    patch_lvl3[count+2]=sq3
    patch_lvl3[count+3]=sq4
    count = count+4


patch_lvl4 = dict()
count=0
for i in range(len(patch_lvl3)):
    sq1,sq2,sq3,sq4=half_cut(patch_lvl3[i])
    patch_lvl4[count]=sq1
    patch_lvl4[count+1]=sq2
    patch_lvl4[count+2]=sq3
    patch_lvl4[count+3]=sq4
    count = count+4




def cell_in_patch(x_coord, y_coord, id_cell, patch):
    x_coord=np.array(x_coord)
    y_coord=np.array(y_coord)
    
    x=x_coord[id_cell]
    y=y_coord[id_cell]
    
    for key, my_square in patch.items():
        if x< my_square["xmax"] and x >=my_square["xmin"] and y < my_square["ymax"] and y >= my_square["ymin"]:
            return(key)


###########################################
# subroutines for simpler plots
def random_color():
    levels = range(32,256,32)
    my_tuple = tuple(random.choice(levels)/256 for _ in range(3))
    my_tuple +=(1,)
    return my_tuple

def get_colormap(id_patch):
    newcolors = np.empty((len(id_patch), 4))
    for i in np.unique(id_patch):
        id_modif=np.where(id_patch == i)
        newcolors[id_modif] = np.array(random_color())
    
    my_colormap = ListedColormap(newcolors)
    return(my_colormap)
###########################################

# store ids and plot

all_patches = dict()

# ----------
# check uniform
# ------------

id_patch = []
for id_cell in range(len(x_coord)):            
    id_patch.append(cell_in_patch(x_coord=x_coord, y_coord=y_coord, id_cell = id_cell, 
                                  patch = patch_uniform))

id_patch = np.array(id_patch)
model.meshing.plot(my_scalar = id_patch)

model.meshing.mesh_pyvista.plot(scalars=id_patch+1, cpos = "xy", 
                                show_edges=True, 
                                notebook = True, show_bounds=True)

all_patches[0] = id_patch
# ----------
# check lvl2
# ------------

id_patch = []
for id_cell in range(len(x_coord)):            
    id_patch.append(cell_in_patch(x_coord=x_coord, y_coord=y_coord, id_cell = id_cell, 
                                  patch = patch_lvl2))

id_patch = np.array(id_patch)
#pv.plotter()
model.meshing.mesh_pyvista.plot(scalars = id_patch, cpos = "xy", 
                                show_edges=True, 
                                notebook = True)


model.meshing.mesh_pyvista.plot(scalars=id_patch, cpos = "xy", 
                                show_edges=True, 
                                notebook = True)

all_patches[1] = id_patch

# ------------
# check lvl3
# ------------
id_patch = []
for id_cell in range(len(x_coord)):            
    tmp_id_patch = cell_in_patch(x_coord=x_coord, y_coord=y_coord, id_cell = id_cell, 
                                  patch = patch_lvl3)
    print(tmp_id_patch)
    id_patch.append(tmp_id_patch)

id_patch = np.array(id_patch)


my_colormap = get_colormap(id_patch)

model.meshing.mesh_pyvista.plot(scalars=id_patch,  
                                cpos="xy", 
                                cmap = my_colormap,
                                show_edges=True, 
                                notebook=True)

all_patches[2] = id_patch
# ----------
# check lvl4
# ------------

id_patch = []
for id_cell in range(len(x_coord)):            
    id_patch.append(cell_in_patch(x_coord=x_coord, y_coord=y_coord, id_cell = id_cell, 
                                  patch = patch_lvl4))

id_patch = np.array(id_patch)


my_colormap = get_colormap(id_patch)


model.meshing.mesh_pyvista.plot(scalars=id_patch, 
                                show_edges=True, 
                                cpos="xy", 
                                cmap = my_colormap, 
                                notebook=True)



all_patches[3] = id_patch


# ----------
# cell level
# ----------
all_patches[4] = np.arange(len(x_coord), step =1)
my_colormap = get_colormap(all_patches[4])
#model.meshing.mesh_pyvista.plot(scalars=all_patches[4], 
#                                show_edges=True, 
#                                cpos="xy", 
#                                cmap = my_colormap, 
#                                notebook=False)

# set 1 as minimum value
for i,patch in all_patches.items():
    patch = patch+1
    all_patches[i] = patch





#-------------------------------------------
# FORTH : Perform inference uniform
#-------------------------------------------

run_type = "min"

mesh_corresp = all_patches[0]
patch_value = 0.001

# random.random() generate a number between 0 and 1


# initialise fortran instance, and python corrponding data
model = df2d.dassflowmodel(bin_dir = os.getcwd(), 
                           hdf5_path=os.getcwd()+"/res/simu.hdf5", 
                           run_type = run_type,
                           clean=True)

# SET UP MANNING VALUE
model.config["use_obs"]   = 1
model.config["w_obs"]     = 1
model.config["c_manning"] = 1
model.config["eps_min"] = 0.001
model.config.set()

model.init_all()

model.param.friction.manning["mesh_correspondance"] = mesh_corresp
model.param.friction.manning["patch_correspondance"] = mesh_corresp
model.param.friction.manning["patch_value"] = patch_value
model.param.set()
model.run()
minimised = df2d.core.min.Min(bin_dir = model.bin_dir)
minimised.source_all()


min_files = os.listdir(model.bin_dir+"/min")
tmp = [x[:-4] for x in min_files]
def find_indices(lst, condition):
                       return [int(i) for i, elem in enumerate(lst) if elem == condition]

min_files = [x for i, x in enumerate(min_files) if i in find_indices(tmp, "manning")]
indices = np.array([int(x[-3:]) for x in min_files])

min_file = [x for i, x in enumerate(min_files) if i ==np.array(np.where(indices == max(indices)))[0]][0]
min_path = model.bin_dir + "/min/" + min_file


f = open(min_path, "r")
lines = f.readlines()
inf_patch_corresp = []
inf_patch_value = []
for i in lines:
    res = i.split()
    inf_patch_corresp.append(res[0])
    inf_patch_value.append(res[1])

optimized_patch_value = np.array(inf_patch_value, dtype = "float64")
optimized_patch_corresp =  np.array(inf_patch_corresp, dtype = "int")
df2d.wrapping.call_model.clean_model(self = model.kernel)

# ----------------------------------------------
# perform direct run with optimized values
# -----------------------------------------
run_type = "direct"

# initialise fortran instance, and python corrponding data
model = df2d.dassflowmodel(bin_dir = os.getcwd(), 
                           hdf5_path=os.getcwd()+"/res/simu.hdf5", 
                           run_type = run_type,
                           clean=True)

# SET UP MANNING VALUE
model.config["use_obs"]   = 0
model.config["w_obs"]     = 1
model.config.set()

model.init_all()

model.param.friction.manning["mesh_correspondance"] = mesh_corresp
model.param.friction.manning["patch_correspondance"] = mesh_corresp
model.param.friction.manning["patch_value"] = optimized_patch_value
model.param.set()
model.run()

model.min = minimised
model.save_all()

ref_manning =  model.param.friction.manning.copy()

df2d.wrapping.call_model.clean_model(self = model.kernel)

#
os.chdir(model.bin_dir)
os.system(f"mv ./res/simu.hdf5 ./hdf5_file/inf_uniform.hdf5")


model.min
##############################################################################

for my_id_patch in range(len(all_patches)):
    if my_id_patch==0:
        print("initialization done above")
    else:
        # ref manning exists
        #all_patches
        #my_id_patch
        
        print("---------------------------------------------------------------------")       
        print(my_id_patch)
        print("---------------------------------------------------------------------")    
        
        
        del model
        run_type = "min"
        
        values_i_moins_1 = [ref_manning["patch_value"][x-1] for x in ref_manning["mesh_correspondance"] ]
        mesh_corresp = all_patches[my_id_patch]
        
        tmp2 =  np.ndarray( (len(all_patches[my_id_patch]), 2) )
        tmp2[:,0] = values_i_moins_1
        tmp2[:,1] = mesh_corresp
        
        patch_value = np.zeros(len(np.unique(tmp2[:,1])))
        id_patch =  np.unique(tmp2[:,1])
        id_value_to_scrap = np.array([np.where(tmp2[:,1] ==x)[0][0] for x in id_patch], dtype="int")
        patch_value[:] = np.array([values_i_moins_1[x] for x in id_value_to_scrap], dtype = "float64")
        
        # random.random() generate a number between 0 and 1
        
        
        # initialise fortran instance, and python corrponding data
        model = df2d.dassflowmodel(bin_dir = os.getcwd(), 
                                   hdf5_path=os.getcwd()+"/res/simu.hdf5", 
                                   run_type = run_type,
                                   clean=True)
        
        # SET UP MANNING VALUE
        model.config["use_obs"]   = 1
        model.config["w_obs"]     = 1
        model.config["c_manning"] = 1
        model.config["eps_min"] = 0.001
        model.config.set()
        
        model.init_all()
        
        model.param.friction.manning["mesh_correspondance"] = mesh_corresp
        model.param.friction.manning["patch_correspondance"] = mesh_corresp
        model.param.friction.manning["patch_value"] = patch_value
        model.param.set()
        
        model.run()
        
        
        min_files = os.listdir(model.bin_dir+"/min")
        tmp = [x[:-4] for x in min_files]
        def find_indices(lst, condition):
                               return [int(i) for i, elem in enumerate(lst) if elem == condition]
        
        min_files = [x for i, x in enumerate(min_files) if i in find_indices(tmp, "manning")]
        indices = np.array([int(x[-3:]) for x in min_files])
        
        min_file = [x for i, x in enumerate(min_files) if i ==np.array(np.where(indices == max(indices)))[0]][0]
        min_path = model.bin_dir + "/min/" + min_file
        
        
        f = open(min_path, "r")
        lines = f.readlines()
        inf_patch_corresp = []
        inf_patch_value = []
        for i in lines:
            res = i.split()
            inf_patch_corresp.append(res[0])
            inf_patch_value.append(res[1])
        
        optimized_patch_value = np.array(inf_patch_value, dtype = "float64")
        
        df2d.wrapping.call_model.clean_model(self = model.kernel)
        
        # ----------------------------------------------
        # perform direct run with optimized values
        # -----------------------------------------
        run_type = "direct"
        
        # initialise fortran instance, and python corrponding data
        model = df2d.dassflowmodel(bin_dir = os.getcwd(), 
                                   hdf5_path=os.getcwd()+"/res/simu.hdf5", 
                                   run_type = run_type,
                                   clean=True)
        
        # SET UP MANNING VALUE
        model.config["use_obs"]   = 0
        model.config["w_obs"]     = 1
        model.config.set()
        
        model.init_all()
        
        model.param.friction.manning["mesh_correspondance"] = mesh_corresp
        model.param.friction.manning["patch_correspondance"] = mesh_corresp
        model.param.friction.manning["patch_value"] = optimized_patch_value
        model.param.set()
        model.run()
        
        
        model.save_all()
        
        model.min = df2d.core.min.Min(bin_dir = model.bin_dir)
        model.min.source_all()
        ref_manning =  model.param.friction.manning.copy()
        
        df2d.wrapping.call_model.clean_model(self = model.kernel)
        #
        os.chdir(model.bin_dir)
        os.system(f"mv ./res/simu.hdf5 ./hdf5_file/inf{my_id_patch}.hdf5")
        del model
