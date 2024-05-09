# TESS Project


<!--<p align="center">
<img src="https://github.com/Gaiana/nirdust/blob/main/docs/source/_static/logo.png?raw=true" alt="logo" height="200"/>
</p>

[![PyPi Version](https://badge.fury.io/py/nirdust.svg)](https://badge.fury.io/py/nirdust)
[![Nirdust](https://github.com/Gaiana/nirdust/actions/workflows/nirdust_ci.yml/badge.svg)](https://github.com/Gaiana/nirdust/actions/workflows/nirdust_ci.yml)
[![https://github.com/leliel12/diseno_sci_sfw](https://img.shields.io/badge/DiSoftCompCi-FAMAF-ffda00)](https://github.com/leliel12/diseno_sci_sfw)
[![Documentation Status](https://readthedocs.org/projects/nirdust/badge/?version=latest)](https://nirdust.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/Gaiana/nirdust/badge.svg?branch=main)](https://coveralls.io/github/Gaiana/nirdust?branch=main)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![arXiv](https://img.shields.io/badge/arXiv-2401.01888-b31b1b.svg)](https://arxiv.org/abs/2401.01888) 

This project is a summary of many codes made for my postdoctoral research in Astrophysics on transiting exoplanets.
Implementing many techniques such as a lot of data extraction and downloading. In this programme we use CVS tables from the Exoplanet data base and photometric data from the TESS satellite observatory. We filtered the important information we needed in the exoplanet tables. We select in detail the photometric data with specific carefully in not include duplicated light curves, and checking the cadence needed.
After the data were correctly cured, we started with the photometric analysis using the Box-Least-Square algorithm, looking for periodic signals in two different stages, for known RV (Radial Velocity) planets and for new planets. We also performed a theoritical modelling of light curves to compare with the observational data corresponding to the knonw planets.

## Motivation:
The motivation of this work was to search for transit signals of known RV (Radial Velocity) planets using TESS data focusing on low-mass planets with sizes smaller than Neptune. Additionally, to achieve high geometric transit probabilities, we aplied some conditioms to filter the selected data.
The detection of exoplanets by means of both transits and RVs is of importance because this allows the characterization of their bulk densities and internal compositions.

## Features

The research was performed in two stages, first we looked for transits signals sing BLS algorithm , and then we performed transit models from literature parameters and using an analytical relationships between
masses and radii for three different compositions (Fortney et al., 2007b,a).




Footnote: the hot dust component may or may not be present in your type 2 
nuclei, do not get disappointed if NIRDust finds nothing.


## Requeriments

You will need Python 3.8 or higher to run NIRDust.



## Citation

If you use *NIRDust* in a scientific publication, we would appreciate citations to the following paper:

> Gaspar, Gaia and Chalela, Martín and Cabral, Juan and Alacoria, José and Mast, Damián and Díaz, Rubén J (2024). 
> NIRDust: probing hot dust emission around type 2 AGN using K-band spectra. 10.1093/mnras/stae008

### Bibtex

```bibtex
@article{10.1093/mnras/stae008,
    author = {Gaspar, Gaia and Chalela, Martín and Cabral, Juan and Alacoria, José and Mast, Damián and Díaz, Rubén J},
    title = "{nirdust: probing hot dust emission around type 2 AGN using K-band spectra}",
    journal = {Monthly Notices of the Royal Astronomical Society},
    volume = {528},
    number = {2},
    pages = {2952-2963},
    year = {2024},
    month = {01},
    issn = {0035-8711},
    doi = {10.1093/mnras/stae008},
    url = {https://doi.org/10.1093/mnras/stae008},
    eprint = {https://academic.oup.com/mnras/article-pdf/528/2/2952/56541590/stae008.pdf},
}
```

Full-text: [https://arxiv.org/abs/1912.09585](https://arxiv.org/abs/2401.01888)

-->

