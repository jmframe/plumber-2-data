#!/discover/nobackup/jframe/anaconda3/bin/python

import netCDF4
import numpy as np
import pandas as pd
import csv
import sys
import datetime as dt
import glob

#flux_directory = '/discover/nobackup/jframe/data/flux-evaluation-20200722T145656Z-001/'
flux_directory = '/discover/nobackup/jframe/data/plumber-2-met/'
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
    if 'reference_height' not in d.variables.keys() or 'canopy_height' not in d.variables.keys():
        print(flux_file)
        print(d.variables.keys())
        print('\n')
    d.close()


