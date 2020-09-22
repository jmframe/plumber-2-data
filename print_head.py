#!/discover/nobackup/jframe/anaconda3/bin/python

import netCDF4
import numpy as np
import pandas as pd
import csv
import sys
import datetime as dt
import glob

#flux_directory = '/discover/nobackup/jframe/data/flux-evaluation-20200722T145656Z-001/'
flux_directory = '/discover/nobackup/jframe/data/plumber-2/flux-nc/'
met_directory = '/discover/nobackup/jframe/data/plumber-2/met-nc/'
flux_files = []
met_files = []
n_flux_files = 0
n_met_files = 0
for filepath in glob.iglob(flux_directory+'*.nc'):
    n_flux_files += 1
    flux_files.append(filepath.split('/')[-1])
for filepath in glob.iglob(met_directory+'*.nc'):
    n_met_files += 1
    met_files.append(filepath.split('/')[-1])

#flux_variables = {}
#flux_time_min_max = {}
#count_files = 0
#for filepath in glob.iglob(flux_directory+'*.nc'):
#    flux_file = filepath.split('/')[-1]
#    d = netCDF4.Dataset(filepath, "r", format="NETCDF4")
#    flux_time_min_max[flux_file] = [min(d['time']),max(d['time'])]
#    flux_variables[flux_file] = list(d.variables.keys())
#    count_files += 1
#    print(d.variables.keys())
#    print(d.variables['Qle'])
#    print(d.variables['Qh'])
#    d.close()
#    break
met_variables = {}
met_time_min_max = {}
count_files = 0
for filepath in glob.iglob(met_directory+'*.nc'):
    met_file = filepath.split('/')[-1]
    d = netCDF4.Dataset(filepath, "r", format="NETCDF4")
    met_time_min_max[met_file] = [min(d['time']),max(d['time'])]
    met_variables[met_file] = list(d.variables.keys())
    count_files += 1
    print(d.variables.keys())
    print(d.variables['SWdown'])
    print(d.variables['LWdown'])
    print(d.variables['Psurf'])
    print(d.variables['Tair'])
    print(d.variables['Precip'])
    d.close()
    break
