#Script to download PDCSAP_FLUX using Lightkurve - Python package for Kepler and TESS data analysis
# (Lightkurve Collaboration et al. 2018).

import lightkurve as lk
import pandas as pd
import astropy
import numpy as np
import astropy.units as u
import matplotlib.pyplot as plt
from lightkurve.lightcurve import LightCurve as LC
from astropy.io import fits
from lightkurve import search_lightcurve
from lightkurve import correctors
from astropy.timeseries import BoxLeastSquares
import os
import pathlib

path = os.path.abspath(os.path.dirname(__file__))

data_path = pathlib.Path(path) / "Data"

filename = data_path / "Tess_Sample.csv"

sample = pd.read_csv(filename,index_col='pl_name', header=0, comment='#')

# Set new columns

sample.loc[:, 'MAX_D'] = None
sample.loc[:, 'MAX_I'] = None


# To analize planets in the table

# for i, planet in enumerate(sample.index):

# To analize a particular object we can create a list. Comment line 29 and uncomment lines 33 an 34

planets= ['61 Vir b']
for i, planet in enumerate(planets):

    star = sample.loc[planet, 'pl_hostname']
    TIC_ID= sample.loc[planet,'tic_id']

    print(star , TIC_ID )

    search_result= search_lightcurve(star, mission='tess', author='SPOC',exptime=120)
    lcfs = search_result.download_all()
    print(search_result)
    print(lcfs)

    for j, lcfi in enumerate(lcfs):

        lci = lcfi.remove_nans().remove_outliers().normalize()
        sector = lcfi.hdu[0].header['SECTOR']
        tic = lcfi.hdu[0].header['TICID']
        RA=lcfi.hdu[0].header['RA_OBJ']*24/360
        DEC=lcfi.hdu[0].header['DEC_OBJ']
        print(star, ', RA', RA ,', DEC', DEC )

        max = lci.time.value[-1]-lci.time.value[0]-2.
        delta = lci.time.shape

        N_fr = lcfs[j].num_frm
        print('frames number ', N_fr, ', tic', tic)

        #Selects data with the right cadence and removes repited data from TIC number and frames number
        if  N_fr == 60 and tic == sample.loc[planet,'tic_id']:
            print(sector)
            cadence = 2
            #concatenates all the observed sectors for each star
            if j == 0:
                lc = lci
                r = sector
                d = max
                maxT = d
                sample.loc[planet, 'MAX_D'] = d
                print('TIC', tic ,', primer sector', sector,', cadencia de ', cadence, ' minutos, numero de datos', delta)
                print('max_d', d)
            else:

                lc = lc.append(lci)
                print('se concatena TIC', tic ,', sector', sector ,', cadencia de ', cadence, ' minutos, numero de datos', delta)
                MAX = maxT
                if sector is r+1:
                    r = sector
                    maxT = d + max
                    d = maxT
                    sample.loc[planet, 'MAX_D'] = np.max(np.array([MAX, maxT]))
                    print('sector consecutivo ', r, ' con max',max, 'y', d,' días consecutivos.')
                    print('MAX', MAX, 'maxT', maxT)
                else:
                    r = sector
                    maxI = d
                    sample.loc[planet, 'MAX_I'] = maxI
                    #MAX = maxI
                    d = max
                    print('sector ', r, ' con máximo intermedio de sectores anteriores ' ,maxI , ' y ', d, 'días del sector.')
                    print('maxI', maxI)



        else:
            cadence = max/delta*1440
            print('No se suma TIC', tic ,', sector', sector ,', cadencia de ', cadence, ' minutos, numero de datos', delta)

        print('TIC', tic ,', sector', sector ,', cadencia de ', cadence, ' minutos, numero de datos', delta)


    star = star.replace(' ','')
    lc = lc.remove_nans().remove_outliers(sigma_lower=5, sigma_upper= 3)
    maxT = lc.time[-1]-lc.time[0]
    deltaT=lc.time.shape
    cadenceT = maxT/deltaT*1440
    print('TIC', sample.loc[planet,'TIC'] ,'numero de datos TOTAL', deltaT)
    plt.plot(lc.time.value, lc.flux.value,linestyle='none', marker='.', label= star, color='orange')
    plt.legend(loc='upper right');
    plt.show()


    pdc_path = pathlib.Path(path) / "Data/PDC"

    np.savetxt(pdc_path+star+'_pdc_lc.txt',np.array([lc.time.value,lc.flux.value,lc.flux_err.value]).T, delimiter=" ")
# Save CSV
sample.to_csv(filename)
