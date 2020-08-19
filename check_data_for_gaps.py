#!/discover/nobackup/jframe/anaconda3/bin/python

import numpy as np
import pandas as pd
import glob
from datetime import datetime as dt

data_dir = '/discover/nobackup/jframe/data/'
directory = {'flux':data_dir+'plumber-2-flux-txt/', 'met':data_dir+'plumber-2-met-txt/'}
flux_met = ['flux', 'met']
for fm in flux_met:
    for filepath in glob.iglob(directory[fm]+'*.txt'):
        plumber_site = filepath.split('/')[-1]
        print(plumber_site)
        with open(filepath, 'r') as f:
            df = pd.read_csv(f)
        l = df.shape[0]
        d0 = dt(df.year[0],df.month[0],df.day[0],df.hour[0],df.minute[0])
        d1 = dt(df.year[1],df.month[1],df.day[1],df.hour[1],df.minute[1])
        deltime = d1 - d0
        for i in range(1,l):
            d1 = dt(df.year[i],  df.month[i],  df.day[i],  df.hour[i],  df.minute[i])
            d0 = dt(df.year[i-1],df.month[i-1],df.day[i-1],df.hour[i-1],df.minute[i-1])
            deltime2 = d1 - d0
            if deltime2 != deltime:
                print('There is a gap in the data at timestep ',i)
                print(deltime2, deltime)
                break
