# TESS Data Analysis: Exoplanet Transit Detection



<!--<p align="center">
<img src="https://github.com/Gaiana/nirdust/blob/main/docs/source/_static/logo.png?raw=true" alt="logo" height="200"/>
</p>

[![TESS Data](https://github.com/fvl27/TESS-Project/blob/main/figuras-tessproject/dataset_tess.svg)](https://exoplanetarchive.ipac.caltech.edu/) -->
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![arXiv](https://img.shields.io/badge/arXiv-2401.01888-b31b1b.svg)](https://arxiv.org/abs/2207.12498) 

## Project Overview

This project presents data analysis workflows developed during my postdoctoral research in astrophysics, focused on the detection and characterization of transiting exoplanets using data from NASA's Transiting Exoplanet Survey Satellite (TESS).

The project combines data extraction, data cleaning, sample selection, time-series analysis, and light-curve modeling to investigate transit signals from known radial-velocity planets and identify potential new candidates.

This project is a summary of many codes made for my postdoctoral research in Astrophysics on transiting exoplanets.
Implementing many techniques such as a lot of data extraction and downloading. In this programme we use CVS tables from the Exoplanet data base and photometric data from the TESS satellite observatory. We filtered the important information we needed in the exoplanet tables. We select in detail the photometric data with specific carefully in not include duplicated light curves, and checking the cadence needed.
After the data were correctly cured, we started with the photometric analysis using the Box-Least-Square algorithm, looking for periodic signals in two different stages, for known RV (Radial Velocity) planets and for new planets. We also performed a theoritical modelling of light curves to compare with the observational data corresponding to the knonw planets.

## Motivation:
The motivation of this work was to search for transit signals of known RV (Radial Velocity) planets using TESS data focusing on low-mass planets with sizes smaller than Neptune. Additionally, to achieve high geometric transit probabilities, we aplied some conditioms to filter the selected data.
The detection of exoplanets by means of both transits and RVs is of importance because this allows the characterization of their bulk densities and internal compositions.

## Objectives

* Retrieve and organize exoplanet catalogues and TESS photometric data.

* Filter datasets according to scientific criteria and observational requirements.

* Identify periodic transit signals using the Box Least Squares (BLS) algorithm.

* Model transit light curves and compare the results with observational data.

* Support the scientific interpretation of potential exoplanet detections.

## Methodology

1. Data collection: Retrieve exoplanet catalogue information and TESS photometric observations.

2. Data cleaning and preparation: Apply selection criteria, check observational cadence, and exclude duplicated light curves.

3. Exploratory and time-series analysis: Search for periodic transit signals using the BLS algorithm.

4. Light-curve modeling: Compare observational data with theoretical transit models and parameters from the literature.

5. Scientific interpretation: Evaluate the results in the context of exoplanet detection and characterization.

## Skills Demonstrated

* Python programming for scientific data analysis

* Data extraction, cleaning, and preparation

* Time-series analysis and periodic signal detection

* Statistical and computational methods

* Data visualization and scientific interpretation

* Working with large astronomical datasets

## Research Publication

This work is related to the following peer-reviewed publication:

Astronomy & Astrophysics, 665, A157 (2022)

Preprint: arXiv:2207.12498

## Repository Structure

Sample_Selection/: Scripts related to sample selection and data preparation.

figuras-tessproject/: Project figures and visualizations.

For details about the implementation, please refer to the code and notebooks included in the repository.



Full-text: 
See [A&A 665, A157 (2022)] (https://www.aanda.org/articles/aa/pdf/2022/09/aa43763-22.pdf), 
or see [arXiv: astro-ph: arXiv:2207.12498] (https://arxiv.org/abs/2207.12498)


