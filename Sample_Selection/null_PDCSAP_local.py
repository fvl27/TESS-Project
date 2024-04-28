# This code performs the BLS search (Kovács et al. 2002). We searched for transits in
# the period range around the known planet periods (local-BLS).

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

sample.loc[:, 'P_foc'] = None
sample.loc[:, 'snr_foc'] = None
sample.loc[:, 'T0_foc'] = None
sample.loc[:,'duration_foc'] = None

#----------------------------------------------------------------------------------------------------------
# To analize planets in the table

# for i, planet in enumerate(sample.index):

# To analize a particular object we can create a list. Comment line 35 and uncomment lines 39 an 41

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



    # Computes BoxLeastSquares periodogram

    bls = BoxLeastSquares(flat.time.value, flat.flux.value, flat.flux_err.value)

    max_d = sample.loc[planet, "MAX_D"]
    max = np.max(np.array([max_d, 30.])) #es el máximo de días consecutivos (ojo! tiene baches de downlink)
    basel = lc.time.value.max()-lc.time.value.min()

    # Next lines are for computing Local-BoxLeastSquares - lines from 115 to 104------------

    # We set the arranges for periods -from literature- and durations

    Per = sample.loc[planet, "P"] #LEO DATOS DE LITERATURA
    sig = sample.loc[planet, "err_P"] #LEO DATOS DE LITERATURA
    frequencies2 = np.arange(1/(Per+10*sig), 1/(Per-10*sig), 1/basel**2/50)#limites distintos
    durations = np.arange(0.005, 0.25, 0.001)

    periodogram2 = bls.power(1/frequencies2, durations, objective='snr', method='fast')

    # save bls.txt

    np.savetxt(pdc_path+planet.replace(' ','')+'foc_bls.txt', np.array([periodogram2.period, periodogram2.power,periodogram2.power-pow_vals2, periodogram2.duration, periodogram2.transit_time, periodogram2.depth]).T, delimiter=" ")

    max_power2 = np.argmax(periodogram2.power)
    period2 = periodogram2.period.value[max_power2]
    t02 = periodogram2.transit_time.value[max_power2]
    duration2=periodogram2.duration.value[max_power2]
    depth2 = periodogram2.depth.value[max_power2]
    snr2 = periodogram2.power.value[max_power2]


    sample.loc[planet,'P_foc'] = period2
    sample.loc[planet,'snr_foc'] = snr2
    sample.loc[planet,'T0_foc'] = t02
    sample.loc[planet,'duration_foc'] = duration2

    print('Best Fit Period: {:0.4f} days'.format(period2))
    print('signal-to-noise', snr2)

    #Plots the BLS periodogram
    plt.figure(111)
    plt.semilogx(periodogram2.period, periodogram2.power,color='magenta',label='P$_\sigma$ = {:0.2f} d'.format(period2))
    plt.semilogx(periodogram2.period, pow_vals2, color='green',linewidth=2)
    plt.semilogx(periodogram2.period, (periodogram2.power-pow_vals2), color='red',linewidth=1.5)

    plt.ylabel("SNR")
    plt.xlabel("Period [day]")
    plt.axvline(x=period,linestyle ='dashed', color='black', alpha=0.7)

    plt.title(planet)

    plt.legend(loc='lower right');
    ax.figure.savefig(pdc_path+'BLSFoc/'+planet.replace(' ','')+'foc_bls.jpg')
    plt.show()
    plt.close('all');


    # Folded light curve
    flat_fold = flat.fold(period2,t02)
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
    ax.figure.savefig(pdc_path+star+'BLSFoc/'+planet.replace(' ','')+'foc_fold.jpg')
    plt.show()
    plt.close('all')



# Save CSV
sample.to_csv(filename)
