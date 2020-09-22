#!/discover/nobackup/jframe/anaconda3/bin/python

import netCDF4
import numpy as np
import pandas as pd
import csv
import sys
import datetime as dt
import glob

flux_directory = '/discover/nobackup/jframe/data/plumber-2/met-nc/'

for filepath in glob.iglob(flux_directory+'*.nc'):
    flux_file = filepath.split('/')[-1]
    d = netCDF4.Dataset(filepath, "r", format="NETCDF4")
    print("{}, {}, {}".format(flux_file, d.variables['longitude'][:],d.variables['latitude'][:]))
    d.close()
