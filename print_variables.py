#!/discover/nobackup/jframe/anaconda3/bin/python

import netCDF4
import numpy as np
import pandas as pd
import csv
import sys
import datetime as dt
import glob

#flux_directory = '/discover/nobackup/jframe/data/flux-evaluation-20200722T145656Z-001/'
flux_directory = '/discover/nobackup/jframe/data/plumber-2/met-nc/'
flux_files = []
n_flux_files = 0
for filepath in glob.iglob(flux_directory+'*.nc'):
    n_flux_files += 1
    flux_files.append(filepath.split('/')[-1])

flux_variables = {}
flux_time_min_max = {}
count_files = 0
for filepath in glob.iglob(flux_directory+'*.nc'):
    flux_file = filepath.split('/')[-1]
    d = netCDF4.Dataset(filepath, "r", format="NETCDF4")
    flux_time_min_max[flux_file] = [min(d['time']),max(d['time'])]
    flux_variables[flux_file] = list(d.variables.keys())
    count_files += 1
    print(d['time'])
    break
    print(flux_file, "file {} out of {}".format(count_files, n_flux_files))
    print("minimum time: {} and maximum time{}".format(min(d['time']),max(d['time'])))
    print(flux_variables[flux_file])
    print(flux_time_min_max[flux_file])
    print('\n')
    d.close()


# Check to see what variables are in all the files, if any.
#for i, flux_file in enumerate(flux_variables.keys()):
#    current_variables = flux_variables[flux_file]
#    if i == 0:
#        variable_list = current_variables
#    else:
#        for variable in variable_list:
#            if variable not in current_variables:
#                variable_list.remove(variable)
#    break
#print(variable_list) # ['x', 'y', 'time', 
                     # 'NEE', 'GPP', 'NEE_qc', 'Qle', 'Qle_qc', 'Qh', 'Qh_qc', 'Qg_qc', 
                     # 'Ustar', 'Ustar_qc', 'latitude', 'longitude', 'elevation', 'IGBP_veg_long'] 
# check the unbroken time periods for the variables
#fluxes = ['NEE', 'GPP', 'NEE_qc', 'Qle', 'Qle_qc', 'Qh', 'Qh_qc', 'Qg_qc']
#variable_time_periods = {}
#for filepath in glob.iglob(flux_directory+'*.nc'):
#    flux_file = filepath.split('/')[-1]
#    d = netCDF4.Dataset(filepath, "r", format="NETCDF4")
#    variable_time_periods[flux_file] = {f:[] for f in fluxes}
#    for f in fluxes:
#        variable_time_periods[flux_file][f][0] = 
#    d.close()
