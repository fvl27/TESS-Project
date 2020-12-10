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

filepath = "/home/flavia/Documentos/TESS/pandas-EXO/PDC/"
#filename = "/home/flavia/Documentos/TESS/pandas-EXO/table_prueba.csv"
filename = "/home/flavia/Documentos/TESS/pandas-EXO/table_prueba.csv"
sample = pd.read_csv(filename,index_col='pl_name', header=0, comment='#')

# Crea columnas vacía
#
# sample.loc[:, 'P_bls'] = None
# sample.loc[:, 'snr_bls'] = None
# sample.loc[:, 'T0_bls'] = None
# sample.loc[:,'duration_bls'] = None

#already_searched = []
#-----------------------------------------------------------------------------------
#USAR CUANDO TENGO QUE DESCARGAR CURVAS
#cuando quiero trabajar con todos los objetos de la tabla
#for i, planet in enumerate(sample.index):

#cuando quiero trabajas con solo unos pocos en lista planets
#planets= ['HD 136352 b', 'HD 136352 c']
#planets=['HD 136352 b', 'HD 31527 b', 'HD 20003 b', 'GJ 676 A d', 'GJ 3138 b', 'HD 1461 b', 'GJ 180 b', 'HD 20781 b', 'GJ 357 c', 'HD 51608 b', 'GJ 273 b']
#for i, planet in enumerate(planets):

    # star = sample.loc[planet, "pl_hostname"]
    # if star in already_searched:
    #     continue
    #
    # print(star)
    #
    # lcfs = search_lightcurvefile(star, mission='tess').download_all()
    # print(lcfs)
    # for j, lcfi in enumerate(lcfs):
    #
    #     lci = lcfi.PDCSAP_FLUX.remove_nans().remove_outliers().normalize()
    #     sector = str(lcfi.hdu[0].header['SECTOR'])
    #     lci.to_fits(path=filepath+star.replace(' ','')+'sector'+sector+'lc.fits', overwrite=True)
    #
    #     if j == 0:
    #         lc = lci
    #
    #     else:
    #         lc = lc.append(lci)
    #
    # star = star.replace(' ','')
    # lc = lc.remove_nans().remove_outliers()
    # #lc.to_fits(path=filepath+star+'_pdc_lc.fits', overwrite=True)
    # np.savetxt(filepath+star+'_pdc_lc.txt',np.array([lc.time,lc.flux,lc.flux_err]).T, delimiter=" ")
#----------------------------------------------------------------------------------------------------------
    #para abrir el to_fits cuando se necesite
    #from astropy.io import fits
    #filepath = "/home/flavia/Documentos/TESS/pandas-EXO/PDC/"
    #hdu = fits.open(filepath+star+'_pdc_lc.fits')
#----------------------------------------------------------------------------------------------------------
#YA DESCARGADAS LAS CURVAS
#cuando quiero trabajar con todos los objetos de la tabla
for i, planet in enumerate(sample.index):

#cuando quiero trabajar con solo unos pocos en lista planets
#planets=['61 Vir b']

#for i, planet in enumerate(planets):
    star = sample.loc[planet, "pl_hostname"]

    print(planet)
    star = star.replace(' ','')
    #data = np.loadtxt(filepath+star+'lc_pld.txt', unpack=True, usecols=[0,1,2])
    data = np.loadtxt(filepath+star+'_pdc_lc.txt', unpack=True, usecols=[0,1,2])
    lc = LC(time=data[0], flux=data[1], flux_err=data[2])
    lc = lc.remove_nans().remove_outliers()
#----------------------------------------------------------------------------------------------------------
    #primer flatteo
    flat, trend = lc.flatten(window_length=10001, polyorder=2, return_trend=True)
    flat=flat.remove_nans().remove_outliers()
    trend=trend.remove_nans().remove_outliers()

    flat_n = flat[::2]
    flat_10 = flat[10:-10]
    #BoxLeastSquares

    bls = BoxLeastSquares(flat.time, flat.flux, flat.flux_err)
    #bls_n = BoxLeastSquares(flat_n.time, flat_n.flux, flat_n.flux_err)
    #bls_10 = BoxLeastSquares(flat_10.time, flat_10.flux, flat_10.flux_err)
    #se definen los arreglos de periodos y duraciones tomados para calcular el periodograma
    Per = sample.loc[planet, "P"]
    sig = sample.loc[planet, "err_P"]

    max_d = sample.loc[planet, "MAX_D"]
    max = np.max(np.array([max_d, 30.])) #es el máximo de días consecutivos (ojo! tiene baches de downlink)
    basel = flat.time.max()-flat.time.min()

    frequencies2 = np.arange(1/(Per+10*sig), 1/(Per-10*sig), 1/basel**2/50)#limites distintos
    frequencies = np.arange(1/max, 1.5, 1/basel**2/10)#comun
    durations = np.arange(0.005, 0.25, 0.001)

    #se calcula el periodograma

    periodogram = bls.power(1/frequencies,durations, objective='snr', method='fast')
    #periodogram2 = bls.power(1/frequencies2, durations, objective='snr', method='fast')
    # periodogram_n = bls_n.power(1/frequencies, durations, objective='snr', method='fast')
    # periodogram_10 = bls_10.power(1/frequencies, durations, objective='snr', method='fast')

    #save bls.txt
    #np.savetxt(filepath+planet.replace(' ','')+'foc_bls.txt', np.array([periodogram.period, periodogram.power, periodogram.duration, periodogram.transit_time, periodogram.depth]).T, delimiter=" ")
    np.savetxt(filepath+star.replace(' ','')+'ciegas_bls.txt', np.array([periodogram.period, periodogram.power, periodogram.duration, periodogram.transit_time, periodogram.depth]).T, delimiter=" ")

    #max_power2 = np.argmax(periodogram2.power)
    max_power = np.argmax(periodogram.power)
    # max_power_n = np.argmax(periodogram_n.power)
    # max_power_10 = np.argmax(periodogram_10.power)#defino max_power como la máxima potencia en el BLS
    #stats = bls.compute_stats(periodogram.period[max_power], periodogram.duration[max_power], periodogram.transit_time[max_power])
    #
    # period2 = periodogram2.period[max_power2] # o period = periods[np.argmax(periodogram.power)] 35.6110000000 days
    # t02 = periodogram2.transit_time[max_power2] # o t0 = periodogram.transit_time[np.argmax(periodogram.power)] 32.7062862527
    # duration2=periodogram2.duration[max_power2] # o duration=periodogram.duration[np.argmax(periodogram.power)] 0.1190000000
    # depth2 = periodogram2.depth[max_power2]
    # snr2 = periodogram2.power[max_power2]
    #
    period = periodogram.period[max_power] # o period = periods[np.argmax(periodogram.power)] 35.6110000000 days
    t0 = periodogram.transit_time[max_power] # o t0 = periodogram.transit_time[np.argmax(periodogram.power)] 32.7062862527
    duration=periodogram.duration[max_power] # o duration=periodogram.duration[np.argmax(periodogram.power)] 0.1190000000
    depth = periodogram.depth[max_power]
    snr = periodogram.power[max_power]
    #
    # period_n = periodogram_n.period[max_power_n]
    # period_10 = periodogram_10.period[max_power_10]
    #
    # sample.loc[planet,'P_foc'] = period2
    # sample.loc[planet,'snr_foc'] = snr2
    # sample.loc[planet,'T0_foc'] = t02
    # sample.loc[planet,'duration_foc'] = duration2
    #
    sample.loc[planet,'P_bls'] = period
    sample.loc[planet,'snr_bls'] = snr
    sample.loc[planet,'T0_bls'] = t0
    sample.loc[planet,'duration_bls'] = duration

    print('Best Fit Period: {:0.4f} days'.format(period))#,' and Period: {:0.4f} days'.format(period2))
    print('potencia', snr)#,'and', snr2)
    print('en ', max, 'días muestreados')

    #graficamos BLS
    plt.figure(111)
    plt.semilogx(periodogram.period, periodogram.power, color='black',label='period: {:0.4f} d'.format(period))
    #plt.semilogx(periodogram2.period, periodogram2.power,color='magenta',label='Target'+planet+'Focus Periodo: {:0.4f} d'.format(period2))
    # plt.semilogx(periodogram_n.period, periodogram_n.power, color='green',label='slice Periodo: {:0.4f} d'.format(period_n))
    # plt.semilogx(periodogram_10.period, periodogram_10.power,linestyle ='dashed',color='blue',label='Focus Periodo: {:0.4f} d'.format(period_10))
    plt.ylabel("SNR")
    plt.xlabel("Period [day]")
    plt.axvline(x=period,linestyle ='dashed', color='black', alpha=0.7)
    #plt.axvline(x=period2,linestyle ='dashed', color='magenta', alpha=0.7)
    # plt.axvline(x=period_n,linestyle ='dashed', color='green', alpha=0.7)
    # plt.axvline(x=period_10,linestyle ='dashed', color='blue', alpha=0.7)
    plt.title(star)
    #plt.title(planet)
    plt.legend(loc='lower right');
    plt.show()
    #plt.savefig(filepath+'BLSFoc/'+planet.replace(' ','')+'foc_bls.jpg')
    plt.savefig(filepath+'BLS/'+star.replace(' ','')+'ciegas_bls.jpg')
    plt.close('all')


    transit_mask = bls.transit_mask(lc.time, period,duration+0.02,t0)
    tlc=lc[transit_mask]

    bx=lc.errorbar(linestyle='none',color='red')

    lc.plot(ax=bx,linestyle='none', marker='o',color='orange')
    tlc.plot(ax=bx,linestyle='none', marker='o',color='black')
    #bx.figure.savefig(filepath+'BLSFoc/'+planet.replace(' ','')+'foc_lc.jpg')
    bx.figure.savefig(filepath+'BLS/'+planet.replace(' ','')+'ciegas_lc.jpg')
    bx.clear()
    plt.close('bx')
    plt.close('all')

    flat2, trend2 = lc.flatten(window_length=4001, polyorder= 2, return_trend=True,mask=transit_mask)
    flat2=flat2.remove_nans().remove_outliers()
    trend2=trend2.remove_nans().remove_outliers()

    # Se calcula la curva de luz en fase para los datos flateados
    flat2_fold = flat2.fold(period,t0)

    # Hacemos un bineado de los anterior (Average 20 points per bin)
    bin_flat2 = flat2_fold.bin(binsize=5)

    #graficamos flat2_fold y bin_flat2 para planeta 'b'
    ax = flat2_fold.errorbar(alpha=0.1, label=planet)
    flat2_fold.scatter(alpha=0.2, ax=ax, color='red', label='Periodo: {:0.4f} d'.format(period))
    bin_flat2.errorbar(c='r', ax=ax)
    #ax.legend('Periodo = '+str(period)+' días')
    ax.set_xlim(-0.5, 0.5)


    #ax.figure.savefig(filepath+'BLSFoc/'+planet.replace(' ','')+'foc_fold.jpg')
    ax.figure.savefig(filepath+'BLS/'+planet.replace(' ','')+'ciegas_fold.jpg')
    #np.savetxt(filepath+planet.replace(' ','')+'_fold.txt',np.array([flat2_fold.phase,flat2_fold.flux,flat2_fold.flux_err]).T, delimiter=" ")
    #plt.show('ax')
    ax.clear()
    bx.clear()
    plt.close('bx')
    plt.close('ax')
    plt.close('all')

# Save CSV
sample.to_csv("/home/flavia/Documentos/TESS/pandas-EXO/table_prueba.csv")
