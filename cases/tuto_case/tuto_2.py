#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 10:27:01 2022

@author: livillenave
"""

#########################################################################################################
# Import dassflow2d package
# 
# In df2d, you must have a look at 2 submodules
# - df2d.wrapping which is automaticaly generated by f90 wrap (expet the .__init__ file), and enable the fortran subroutines calls
# - df2d.DassFlow model, that creat a class. This class enable the call of multiple python functions and the storage in python format of main data
#                           these python functions mainly use calls to df2d.wrapping submodule 
#########################################################################################################
import dassflow2d as df2d
import os  

# main directory
dassflow_dir="/home/livillenave/Documents/distant/dassflow2d-wrap/"
# code directory, where compilation happens
code_dir =  f"{dassflow_dir}/code/"
# bin directory, where simulation happens
bin_dir = f"{code_dir}/bin_A/"



os.chdir(code_dir)
os.system("make cleanres")               # removes all in bin_dir/res directory
os.system("make cleanmsh")               # removes all in bin_dir/msh directory
#os.system(f"rm {bin_dir}/restart.bin")   # removes restart.bin file in bin directory
os.chdir(bin_dir)
df2d.wrapping.read_input(f"{bin_dir}input.txt")  




# it is possible to access fortran kernel values and modify them: for exemple:
mesh_name = df2d.wrapping.m_common.get_mesh_name().decode('utf-8')

# We build the function that enable the  acces to all configuration values defined in fortran kernel:
def get_config(input_param={ "mesh_name":'channel.geo',
                                            "ts":0, 
                                            "dta":0, 
                                            "dtw":0, 
                                            "dtp":0,
                                            "dt":0, 
                                            "temp_scheme":'euler', 
                                            "spatial_scheme":'first_b1', 
                                            "adapt_dt":0, 
                                            "cfl":0., 
                                            "feedback_inflow":0,                                    
                                            "coef_feedback":0.,
                                            "heps":0, 
                                            "friction":0, 
                                            "g":10, 
                                            "w_tecplot":0,
                                            "w_vtk":0, 
                                            "w_gnuplot":0, 
                                            "w_obs":0, 
                                            "use_obs":0, 
                                            "max_nt_for_adjoint":0,
                                            "c_manning":0,
                                            "c_manning_beta":0,
                                            "c_bathy":0,
                                            "c_hydrograph":0,
                                            "c_ratcurve":0,
                                            "c_rain":0,
                                            #"c_infil":0,
                                            "c_ic":0,
                                            "restart_min":0,
                                            "eps_min":0} ):
    
    res =input_param
#    all_keys = input_param.keys()
    for k in res:
        # in module m_common
       if k == 'mesh_name':      
             res[k] = df2d.wrapping.m_common.get_mesh_name().decode('utf-8')
       elif k == 'ts':
             res[k] = df2d.wrapping.m_common.get_ts()
       elif k == 'dtw':
               print("dtw")
               res[k] = df2d.wrapping.m_common.get_dtw()
       elif k == 'dtp':
               res[k] = df2d.wrapping.m_common.get_dtp()
       elif k == 'adapt_dt':
               res[k] = df2d.wrapping.m_common.get_adapt_dt()
       elif k == 'dt':
               res[k] = df2d.wrapping.m_common.get_dt()
       elif k == 'cfl':
               res[k] = df2d.wrapping.m_common.get_cfl()
       elif k == 'temp_scheme':
               res[k] = df2d.wrapping.m_common.get_temp_scheme().decode('utf-8')
       elif k == 'spatial_scheme':
               res[k] = df2d.wrapping.m_common.get_spatial_scheme().decode('utf-8')               
       elif k == 'w_tecplot':
               res[k] = df2d.wrapping.m_common.get_w_tecplot()
       elif k == 'w_gnuplot':
               res[k] = df2d.wrapping.m_common.get_w_gnuplot()
       elif k == 'w_vtk':
               res[k] = df2d.wrapping.m_common.get_w_vtk()
       elif k == 'w_obs':
               res[k] = df2d.wrapping.m_common.get_w_obs()
       elif k == 'use_obs':
               res[k] = df2d.wrapping.m_common.get_use_obs()
       elif k == 'max_nt_for_adjoint':
               res[k] = df2d.wrapping.m_common.get_max_nt_for_adjoint()
       elif k == 'max_nt_for_direct':
               res[k] = df2d.wrapping.m_common.get_max_nt_for_direct()
       elif k == 'restart_min':
               res[k] = df2d.wrapping.m_common.get_restart_min()
       elif k == 'get_eps_min':
               res[k] = df2d.wrapping.m_common.get_eps_min()

           #in module m_model
       elif k == 'feedback_inflow':
               res[k] = df2d.wrapping.m_model.get_feedback_inflow()
       elif k == 'coef_feedback':              
               res[k] = df2d.wrapping.m_model.get_coef_feedback()
       elif k == 'friction':
               res[k] = df2d.wrapping.m_model.get_friction()
       elif k == 'g':           
               res[k] = df2d.wrapping.m_model.get_g()
       elif k == 'c_manning':           
              res[k] =  df2d.wrapping.m_model.get_c_manning()
       elif k == 'c_manning_beta':           
               res[k] = df2d.wrapping.m_model.get_c_manning_beta()
       elif k == 'c_bathy':           
               df2d.wrapping.m_model.get_c_bathy()
       elif k == 'c_hydrograph':           
               res[k] = df2d.wrapping.m_model.get_c_hydrograph()               
       elif k == 'c_rain':           
               res[k] = df2d.wrapping.m_model.get_c_rain()             
       elif k == 'c_ic':           
               res[k] = df2d.wrapping.m_model.get_c_ic()    
       
        
    return(res)   
    


# load configuration values from fortran kernel
config = get_config()
# config is a dictionary containing correspongind data to the input.txt file
import pprint 
pprint.pprint(config)


###################################################
# the antagonist of the getters: the setters, gives us the possibility to update fortran kernel value:
########################################################
true_mesh_name = df2d.wrapping.m_common.get_mesh_name()
mesh_name = "new_mesh_name.geo"
# to update in fortran kernel the value, you must use the setter function
df2d.wrapping.m_common.set_mesh_name(mesh_name)

# now, the value is updated in fortrna kernel

tmp = df2d.wrapping.m_common.get_mesh_name().decode('utf-8')
print(tmp )



###################################################
# As well as for the setters a globalise function can be built:
########################################################



# update values in fortran kernel based on provided input
# @param: input_param :: dictionary with keys corresponging to fields to be filled in fortran + values set
# @return: nothing : set the values in fortran kernel
# df2d istance must be on
def set_config(input_param):
#    all_keys = input_param.keys()
    for k in input_param:    
        # in module m_common
       if k == 'mesh_name':
                df2d.wrapping.m_common.set_mesh_name(input_param[k])
       elif k == 'ts':
                df2d.wrapping.m_common.set_ts(input_param[k])
               # DTA IN ASSIMILATION FILE (OBSOLETE HERE ?)
#       if k == 'dta':
#               input_param[k] = df2d.wrapping.m_common.set_dta()
       elif k == 'dtw':
               df2d.wrapping.m_common.set_dtw(input_param[k])
       elif k == 'dtp':
               df2d.wrapping.m_common.set_dtp(input_param[k])
       elif k == 'adapt_dt':
               df2d.wrapping.m_common.set_adapt_dt(input_param[k])
       elif k == 'dt':
               df2d.wrapping.m_common.set_dt(input_param[k])
       elif k == 'cfl':
               df2d.wrapping.m_common.set_cfl(input_param[k])
       elif k == 'temp_scheme':
               df2d.wrapping.m_common.set_temp_scheme(input_param[k])
       elif k == 'spatial_scheme':
               df2d.wrapping.m_common.set_spatial_scheme(input_param[k])           
       elif k == 'w_tecplot':
               df2d.wrapping.m_common.set_w_tecplot(input_param[k])
       elif k == 'w_gnuplot':
               df2d.wrapping.m_common.set_w_gnuplot(input_param[k])
       elif k == 'w_vtk':
               df2d.wrapping.m_common.set_w_vtk(input_param[k])
       elif k == 'w_obs':
               df2d.wrapping.m_common.set_w_obs(input_param[k])
       elif k == 'use_obs':
               df2d.wrapping.m_common.set_use_obs(input_param[k])
       elif k == 'max_nt_for_adjoint':
               df2d.wrapping.m_common.set_max_nt_for_adjoint(input_param[k])
       elif k == 'max_nt_for_direct':
               df2d.wrapping.m_common.set_max_nt_for_direct(input_param[k])
       elif k == 'restart_min':
               df2d.wrapping.m_common.set_restart_min(input_param[k])
       elif k == 'set_eps_min':
               df2d.wrapping.m_common.set_eps_min(input_param[k])

           #in module m_model
       elif k == 'feedback_inflow':
               df2d.wrapping.m_model.set_feedback_inflow(input_param[k]) 
       elif k == 'coef_feedback':              
               df2d.wrapping.m_model.set_coef_feedback(input_param[k]) 
       elif k == 'friction':
               df2d.wrapping.m_model.set_friction(input_param[k]) 
       elif k == 'g':           
               df2d.wrapping.m_model.set_g(input_param[k]) 
       elif k == 'c_manning':           
               df2d.wrapping.m_model.set_c_manning(input_param[k]) 
       elif k == 'c_manning_beta':           
               df2d.wrapping.m_model.set_c_manning_beta(input_param[k]) 
       elif k == 'c_bathy':           
               df2d.wrapping.m_model.set_c_bathy(input_param[k]) 
       elif k == 'c_hydrograph':           
               df2d.wrapping.m_model.set_c_hydrograph(input_param[k])           
    #   elif k == 'c_rain':           
    #           df2d.wrapping.m_model.set_c_rain()              
       #elif k == 'c_ic':           
               #df2d.wrapping.m_model.set_c_ic()    
    print(f"values {[x for x in input_param.keys()]} set")
    return()   
    
# concerning this function, you can personalise the quantity of input you give
# taking advantage of the dictionary structure:
    

to_update_input_param={ "mesh_name":'channel.geo',
                                            "ts":2000,
                                            "dtw":100}    
set_config(input_param=to_update_input_param)



# you can check you updated the configuration by using get_config function
config = get_config()



# you can note that any moment, you can also read an input file specifying its absolute path
df2d.wrapping.read_input(f"{bin_dir}input.txt")  
#check your fortran kernel values again:
config = get_config()

######################################################
# the classical code to perform a run can be used
######################################################
os.chdir(code_dir)
os.system("make cleanres")               # removes all in bin_dir/res directory
os.system("make cleanmsh")               # removes all in bin_dir/msh directory
if os.path.isfile(f"rm {bin_dir}/restart.bin"):
    os.system(f"rm {bin_dir}/restart.bin")   # removes all in bin_dir/msh directory
os.chdir(bin_dir)
df2d.wrapping.read_input(f"{bin_dir}input.txt")  


#>>>>>>>>>>>>><
# update input
to_update_input_param={ "ts":5000,
                        "dtw":1000}    

set_config(input_param=to_update_input_param)
#>>>>>>>>>>>>><

df2d.wrapping.m_mpi.init_mpi()
rank = df2d.wrapping.m_mpi.get_proc()
nproc = df2d.wrapping.m_mpi.get_np()

model = df2d.wrapping.call_model.Model()
model.mesh = df2d.wrapping.m_mesh.msh()
model.dof  = df2d.wrapping.m_model.unk(model.mesh)
model.dof0 = model.dof 
df2d.wrapping.call_model.init_solver(model)
df2d.wrapping.call_model.init_fortran(model)
df2d.wrapping.call_model.run(model, arg = "direct")
df2d.wrapping.call_model.clean_model(model)



# you can check in your bin_dir/res directory that the time of simulation changed in the produced result files
#  (it evolved from ts=3600s to ts=5000s)
#








#############################################
#############################################
#                          HINT1
# using input setter and  restart.bin file, you can
#  generate an initialization setup:
#
#
# 1- perform first simulation with ts ='xxx's 
# 2- clean model
# 3- load previous configuration
# 4 - update ts ='xxx's  to  ts ='yyy's  higher, using set_config method
# 5- keep restart.bin file, and perform a new run
#    --> the simulation will start at t0 = 'xxx' with dof values equals to the values at 'xxx'
#    -->                  and end at ts = 'yyy'.

#############################################.
#############################################

    
    ######################################################
    # FIRST RUN
    ######################################################
os.chdir(code_dir)
os.system("make cleanres")               # removes all in bin_dir/res directory
#os.system("make cleanmsh")               # removes all in bin_dir/msh directory
if os.path.isfile(f"rm {bin_dir}/restart.bin"):
    os.system(f"rm {bin_dir}/restart.bin")   # removes all in bin_dir/msh directory
os.chdir(bin_dir)
df2d.wrapping.read_input(f"{bin_dir}/input.txt")  


# get ts 
ts = df2d.wrapping.m_common.get_ts()



df2d.wrapping.m_mpi.init_mpi()
rank = df2d.wrapping.m_mpi.get_proc()
nproc = df2d.wrapping.m_mpi.get_np()

model = df2d.wrapping.call_model.Model()
model.mesh = df2d.wrapping.m_mesh.msh()
model.dof  = df2d.wrapping.m_model.unk(model.mesh)
model.dof0 = model.dof 
df2d.wrapping.call_model.init_solver(model)
df2d.wrapping.call_model.init_fortran(model)
df2d.wrapping.call_model.run(model, arg = "direct")
df2d.wrapping.call_model.clean_model(model)
    
    ######################################################
    # SECOND RUND WITH UPDATED TS RUN
    ######################################################
os.chdir(code_dir)
#os.system("make cleanmsh")               # removes all in bin_dir/msh directory
os.chdir(bin_dir)
df2d.wrapping.read_input(f"{bin_dir}/input.txt")  


#>>>>>>>>>>>>>
# update input
to_update_input_param={ "ts":ts+3600,
                        "dtw":1000}    

set_config(input_param=to_update_input_param)
#>>>>>>>>>>>>>

df2d.wrapping.m_mpi.init_mpi()
rank = df2d.wrapping.m_mpi.get_proc()
nproc = df2d.wrapping.m_mpi.get_np()

model = df2d.wrapping.call_model.Model()
model.mesh = df2d.wrapping.m_mesh.msh()
model.dof  = df2d.wrapping.m_model.unk(model.mesh)
model.dof0 = model.dof 
df2d.wrapping.call_model.init_solver(model)
df2d.wrapping.call_model.init_fortran(model)
df2d.wrapping.call_model.run(model, arg = "direct")
df2d.wrapping.call_model.clean_model(model)







#############################################
#############################################
#                          HINT2
# If you want to specify initial condition about dof (h,u,v)
# directly, be carfull, you must also specify the values for the gost cells. 
# if not specified the values are 0 
# no more invstingation has be done yet
# open problem
#############################################.
#############################################
