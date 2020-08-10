#!/discover/nobackup/jframe/anaconda3/bin/python

import netCDF4
import numpy as np
import pandas as pd
import csv
import sys
import datetime as dt
import glob

meta = {'flux':['x', 'y', 'time'], 'met':['x','y','time','longitude', 'elevation']}
varz = {'flux':['NEE', 'GPP', 'Qle', 'Qh', 'Qg'], 
        'met':['Tair', 'SWdown', 'LWdown', 'VPD', 'Qair', 'Psurf', 'Precip', 'Wind', 'RH', 'CO2air']}
timez = ['year', 'month', 'day', 'hour', 'minute', 'datetime']
vegs = {'flux':['IGBP_veg_long'], 'met':['IGBP_veg_long','LAI_alternative','LAI']}

data_dir = '/discover/nobackup/jframe/data/'
directory = {'flux':data_dir+'plumber-2-flux/', 'met':data_dir+'plumber-2-met/'}
files = {'flux':[], 'met':[]}
n_files = {'flux':0, 'met':0}
flux_met = ['flux', 'met']
for fm in flux_met:
    for filepath in glob.iglob(directory[fm]+'*.nc'):
        n_files[fm] += 1
        files[fm].append(filepath.split('/')[-1])

# Set up data, this is goping to get a tad bit confusing...
# A disctionary of two dictionaries, each with pandas dataframes for each data file
data = {fm:{ifile:pd.DataFrame(columns=varz[fm]+timez) for ifile in files[fm]} for fm in flux_met}

# Now the main loop where we extract the data from the NetCDF masked array
# And fill in our dictionary of two dictionaries with pandas dataframes
count_files = {fm:0 for fm in flux_met}
for fm in flux_met:
    for ifile in files[fm]:
        filepath = directory[fm]+ifile
        count_files[fm] += 1
        print(ifile, "file {} out of {}".format(count_files[fm], n_files[fm]))
        d = netCDF4.Dataset(filepath, "r", format="NETCDF4")
    
        # To get all the data out of the masked array, make some lists to store values
        value_lists = {ivar:[] for ivar in varz[fm]}
    
        # Loop through the variables and pull them out of the NetCDF
        # and put them into a dataframe for each site
        for ivar in varz[fm]:
            qc_var = ivar+"_qc"
    
            # Here is where we store the values, outside of the masked array
            # TODO: check to see if the values are masked
            data[fm][ifile][ivar] = np.array(d[ivar][:,0][:,0].tolist())
    
            # TODO: decide what to do with the quality control flag
            #if qc_flux_var in list(d.variables.keys()):
            #    flux_data[flux_file][iflux_var] = d[qc_flux_var][:].tolist(-999)
    
            # TODO: convert the vegetation data to numeric values
            
        # Add dates to Pandas
        dtime = netCDF4.num2date(d.variables['time'][:],d.variables['time'].units)
        dtime = np.ma.getdata(dtime)
        data[fm][ifile]['datetime'] = dtime
        data[fm][ifile]['year'] = [i.year for i in dtime]
        data[fm][ifile]['month'] = [i.month for i in dtime]
        data[fm][ifile]['day'] = [i.day for i in dtime]
        data[fm][ifile]['hour'] = [i.hour for i in dtime]
        data[fm][ifile]['minute'] = [i.minute for i in dtime]

        d.close()
    
        # Then write the text file!

        # Troubleshooting, delete when ready.
        if count_files[fm] > 0:
            break

for fm in flux_met:
    for ifile in files[fm]:
        print(ifile)
        print(data[fm][files[fm][0]])
        break
