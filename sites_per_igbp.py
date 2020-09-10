#!/discover/nobackup/jframe/anaconda3/bin/python

import netCDF4
import numpy as np
import pandas as pd
import csv
import sys
import datetime as dt
import glob

flux_directory = '/discover/nobackup/jframe/data/plumber-2/met-nc/'

# This is a long and dumb function to get the string values out of the masked array for IGBP
def get_igbp(veg_ma):
    S = [str(veg_ma[i].data).split(('\'|b')[0])[1] for i in range(200)]
    s = ''
    old_i = None
    for i in S:
        s = s + i 
        old_i = i 
        if i == '' and old_i == '': 
            break
    s_ = ''
    for i in s:
        if i.isalpha():
            s_ = s_ + i 
    return s_

sites_per_igbp = {}
for filepath in glob.iglob(flux_directory+'*.nc'):
    flux_file = filepath.split('/')[-1]
    d = netCDF4.Dataset(filepath, "r", format="NETCDF4")
    igbp = get_igbp(d.variables['IGBP_veg_long'])
    if igbp in sites_per_igbp.keys():
        sites_per_igbp[igbp].append(flux_file)
    else:
        sites_per_igbp[igbp] = [flux_file]
for igbp in sites_per_igbp.keys():
    print(igbp, len(sites_per_igbp[igbp]))

sites_per_igbp_short = {}
for filepath in glob.iglob(flux_directory+'*.nc'):
    flux_file = filepath.split('/')[-1]
    d = netCDF4.Dataset(filepath, "r", format="NETCDF4")
    try:
        igbp = get_igbp(d.variables['IGBP_veg_short'])
    except:
        continue
    if igbp in sites_per_igbp.keys():
        sites_per_igbp[igbp].append(flux_file)
    else:
        sites_per_igbp[igbp] = [flux_file]
for igbp in sites_per_igbp.keys():
    print(igbp, len(sites_per_igbp[igbp]))
