#!/discover/nobackup/jframe/anaconda3/bin/python

import netCDF4
import numpy as np
import pandas as pd
import csv
import sys
import datetime as dt
import glob

meta = {'flux':['x', 'y', 'time'], 'met':['x','y','time','longitude', 'elevation']}
#varz = {'flux':['NEE', 'GPP', 'Qle', 'Qh', 'Qg'], 
varz = {'flux':['NEE', 'GPP', 'Qle', 'Qh'], 
        'met':['Tair', 'SWdown', 'LWdown', 'VPD', 'Qair',
               'Psurf', 'Precip', 'Wind', 'RH', 'CO2air',
               'LAI_alternative','LAI']}
#timez = ['datetime', 'year', 'month', 'day', 'hour', 'minute']
timez = ['year', 'month', 'day', 'hour', 'minute']
vegs = {'flux':[''], 'met':['IGBP_veg_long']}

data_dir = '/discover/nobackup/jframe/data/'
directory = {'flux':data_dir+'plumber-2/flux-nc/', 'met':data_dir+'plumber-2/met-nc/'}
directory_txt = {'flux':data_dir+'plumber-2/flux-txt/', 'met':data_dir+'plumber-2/met-txt/'}
files = {'flux':[], 'met':[]}
n_files = {'flux':0, 'met':0}

# September 2020, updating a few new met files only
flux_met = ['met'] # ['flux', 'met']

#for fm in flux_met:
#    for filepath in glob.iglob(directory[fm]+'*.nc'):
#        n_files[fm] += 1
#        files[fm].append(filepath.split('/')[-1])

files['met'] = ['US-UMB_2000-2014_FLUXNET2015_Met.nc',
               'UK-PL3_2005-2006_LaThuile_Met.nc',
               'UK-Ham_2004-2004_LaThuile_Met.nc',
               'RU-Zot_2003-2003_LaThuile_Met.nc',
               'RU-Che_2003-2004_FLUXNET2015_Met.nc',
               'PL-wet_2004-2005_LaThuile_Met.nc',
               'NL-Hor_2008-2011_FLUXNET2015_Met.nc',
               'NL-Ca1_2003-2006_LaThuile_Met.nc',
               'IT-Non_2002-2002_LaThuile_Met.nc',
               'IT-Mal_2003-2003_LaThuile_Met.nc',
               'IT-LMa_2003-2004_LaThuile_Met.nc',
               'IT-CA3_2012-2013_FLUXNET2015_Met.nc',
               'IT-Amp_2003-2006_LaThuile_Met.nc',
               'IE-Ca1_2004-2006_LaThuile_Met.nc',
               'FR-Lq2_2004-2006_LaThuile_Met.nc',
               'FR-Lq1_2004-2006_LaThuile_Met.nc',
               'FI-Kaa_2000-2002_LaThuile_Met.nc',
               'ES-VDA_2004-2004_LaThuile_Met.nc',
               'DK-Ris_2004-2005_LaThuile_Met.nc',
               'DK-Lva_2005-2006_LaThuile_Met.nc',
               'DE-Obe_2008-2014_FLUXNET2015_Met.nc',
               'AU-Wrr_2016-2017_OzFlux_Met.nc',
               'AU-Whr_2015-2016_OzFlux_Met.nc',
               'AU-Tum_2002-2017_OzFlux_Met.nc',
               'AU-Stp_2010-2017_OzFlux_Met.nc',
               'AU-Rig_2011-2016_OzFlux_Met.nc',
               'AU-Otw_2009-2010_OzFlux_Met.nc',
               'AU-Gin_2012-2017_OzFlux_Met.nc',
               'AU-GWW_2013-2017_OzFlux_Met.nc',
               'AU-DaP_2009-2012_OzFlux_Met.nc',
               'AU-Cpr_2011-2017_OzFlux_Met.nc',
               'AU-Cow_2010-2015_OzFlux_Met.nc',
               'AU-Lit_2016-2017_OzFlux_Met.nc']

# Open and read the txt file with all the unique veg values
IGBP_veg_unique = []
with open('IGBP_veg_long.txt', 'r') as f:
      for line in f:
          a = line[:-1]
          IGBP_veg_unique.append(a)

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

# Set up data, this is goping to get a tad bit confusing...
# A disctionary of two dictionaries, each with pandas dataframes for each data file
data = {fm:{ifile:pd.DataFrame(columns=timez+varz[fm]+vegs[fm]) for ifile in files[fm]} for fm in flux_met}
#data = {fm:{ifile:pd.DataFrame(columns=timez+varz[fm]) for ifile in files[fm]} for fm in flux_met}

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
    
            # Add vegetation data.
            # Need to convert the vegetation data to numeric values.
            if fm == 'met':
                v = get_igbp(d['IGBP_veg_long'])
                for i, iv in enumerate(IGBP_veg_unique):
                    if v == iv:
                        data[fm][ifile]['IGBP_veg_long'] = i
            

        # Add dates to Pandas
        dtime = netCDF4.num2date(d.variables['time'][:],d.variables['time'].units)
        dtime = np.ma.getdata(dtime)
        #data[fm][ifile]['datetime'] = dtime
        data[fm][ifile]['year'] = [i.year for i in dtime]
        data[fm][ifile]['month'] = [i.month for i in dtime]
        data[fm][ifile]['day'] = [i.day for i in dtime]
        data[fm][ifile]['hour'] = [i.hour for i in dtime]
        data[fm][ifile]['minute'] = [i.minute for i in dtime]

        d.close()
    
        # Then write the text file!
        data[fm][ifile].to_csv(directory_txt[fm]+ifile.split('.')[0]+'.txt',
                               index=False)
