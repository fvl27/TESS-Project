# This code performs the BLS search (Kovács et al. 2002). We
# performed a global search for transits of putative
# additional planets (global-BLS).
# At the end also plots the foled light curve

import lightkurve as lk
import pandas as pd
import astropy
import numpy as np
import astropy.units as u
import matplotlib.pyplot as plt
from lightkurve.lightcurve import LightCurve as LC
from astropy.io import fits
from lightkurve import search_lightcurvefile
from lightkurve import correctors
from astropy.timeseries import BoxLeastSquares
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
from scipy.signal import medfilt
from scipy.ndimage import median_filter
import os
import pathlib

path = os.path.abspath(os.path.dirname(__file__))

data_path = pathlib.Path(path) / "Data"

filename = data_path / "short_table_prueba.csv"

sample = pd.read_csv(filename,index_col='pl_name', header=0, comment='#')

# Set new columns for new parameters from BLS algorithm

sample.loc[:, 'P_bls'] = None
sample.loc[:, 'snr_bls'] = None
sample.loc[:, 'T0_bls'] = None
sample.loc[:,'duration_bls'] = None



#----------------------------------------------------------------------------------------------------------
# To analize planets in the table

# for i, planet in enumerate(sample.index):

# To analize a particular object we can create a list. Comment line 39 and uncomment lines 43 an 45

planets=['61 Vir b']

for i, planet in enumerate(planets):
    star = sample.loc[planet, "pl_hostname"]

    print(planet)
    data = np.loadtxt(pdc_path+star.replace(' ','')+'_pdc_lc.txt', unpack=True, usecols=[0,1,2])
    lc = LC(time=data[0], flux=data[1], flux_err=data[2])
    lc = lc.remove_nans().remove_outliers()


    #First Flatting: It Removes the low frequency trend using scipy’s Savitzky-Golay filter.

    size = lc.time.size

    print('número de datos', size)


    flat, trend = lc.flatten(window_length=2001,niters=3,sigma=5, break_tolerance=1000, polyorder=3, return_trend=True)
    flat=flat.remove_nans().remove_outliers()
    trend=trend.remove_nans().remove_outliers()

    ax=lc.plot(linestyle='none',color='red', marker='o')
    trend.plot(ax=ax,color='black', linewidth=2, label=star+' '+'tendencia')
    bx=flat.plot(linestyle='none', color='green', marker='o', label='flateada')
    plt.show()
    plt.close('all');



    #Computes BoxLeastSquares periodogram

    bls = BoxLeastSquares(flat.time.value, flat.flux.value, flat.flux_err.value)

    max_d = sample.loc[planet, "MAX_D"]
    max = np.max(np.array([max_d, 30.])) #es el máximo de días consecutivos (ojo! tiene baches de downlink)
    basel = lc.time.value.max()-lc.time.value.min()

    # Next lines are for computing Global-BoxLeastSquares - lines from 90 to 103------------
    # We set the arranges for periods and durations

    frequencies = np.arange(1/max, 1.5, 1/basel/100)#comun
    durations = np.arange(0.005, 0.25, 0.001)

    periodogram = bls.power(1/frequencies,durations, objective='snr', method='fast')

    # Save bls.txt
    np.savetxt(pdc_path+star.replace(' ','')+'ciegas_blsF.txt', np.array([periodogram.period, periodogram.power, periodogram.duration, periodogram.transit_time, periodogram.depth]).T, delimiter=" ")

    max_power = np.argmax(periodogram.power)
    period = periodogram.period[max_power]
    t0 = periodogram.transit_time[max_power]
    duration=periodogram.duration[max_power]
    depth = periodogram.depth[max_power]
    snr = periodogram.power[max_power]

    sample.loc[planet,'P_bls'] = period
    sample.loc[planet,'snr_bls'] = snr
    sample.loc[planet,'T0_bls'] = t0
    sample.loc[planet,'duration_bls'] = duration


    # Plots the BLS periodogram
    plt.figure(111)
    plt.semilogx(periodogram.period, periodogram.power, color='black',label='P = {:0.2f} d'.format(period))
    plt.ylabel("SNR")
    plt.xlabel("Period [day]")
    plt.axvline(x=period,linestyle ='dashed', color='black', alpha=0.7)
    plt.title(star)

    plt.legend(loc='lower right');
    plt.savefig(pdc_path+'BLS/'+star.replace(' ','')+'global_blsF.jpg')
    plt.show()
    plt.close('all');


    # Folded light curve
    flat_fold = flat.fold(period,t0)
    #
    # It performs a binned folded light curve (Average 20 points per bin)
    bin_flat = flat_fold.bin(binsize=5)
    #
    # Plot
    ax = flat_fold.errorbar(alpha=0.1, label=star)
    flat_fold.scatter(alpha=0.2, ax=ax, color='red', label='P = {:0.4f} d'.format(period))
    bin_flat.errorbar(c='r', ax=ax)
    ax.set_xlim(-0.5, 0.5)
    #
    #
    ax.figure.savefig(pdc_path+'Fold/'+planet.replace(' ','')+'global_fold.jpg')
    plt.show()
    plt.close('all')


# Save CSV
sample.to_csv(filename)
