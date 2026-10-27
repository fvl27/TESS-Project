# TESS Data Analysis: Exoplanet Transit Detection

A Python-based research project for selecting planetary systems, retrieving **TESS** photometry, and searching for transit signals in systems with known radial-velocity planets. The repository contains data-selection and light-curve analysis scripts, example data tables, and figures from the research workflow.

## Overview

The project explores whether planets discovered through the radial-velocity method may also produce detectable transits in TESS observations. Transit and radial-velocity measurements can complement one another and help constrain planetary properties.

The workflow brings together astronomical catalogue filtering, photometric data retrieval, light-curve preparation, periodic-signal searches, and comparison with known-planet transit models.


## Objectives

* Retrieve and organize exoplanet catalogues and TESS photometric data.

* Filter datasets according to scientific criteria and observational requirements.

* Identify periodic transit signals using the Box Least Squares (BLS) algorithm.

* Model transit light curves and compare the results with observational data.

* Support the scientific interpretation of potential exoplanet detections.

## Skills Demonstrated

* Python programming for scientific data analysis

* Data extraction, cleaning, and preparation

* Time-series analysis and periodic signal detection

* Statistical and computational methods

* Data visualization and scientific interpretation

* Working with large astronomical datasets


## Workflow

1. **Select a target sample.** Filter a planetary catalogue using scientific criteria, including multiplicity, discovery method, orbital period, and available mass/radius information.
2. **Retrieve TESS photometry.** Use [Lightkurve](https://lightkurve.github.io/) to find and download light curves, including PDCSAP flux products where available.
3. **Prepare the light curves.** Inspect the observations and prepare the data for the transit search. The scripts include filtering and smoothing operations.
4. **Search for transit signals.** Use the Box Least Squares (BLS) algorithm to look for periodic transit-like signals. The repository contains both a global search and a search focused around known orbital periods.
5. **Visualize and interpret results.** Plot light curves and compare candidate signals with known-planet information and theoretical expectations.

## Repository structure

```text
TESS-Project-main/
├── README.md
├── Scripts/
│   ├── sample_TESS.py          # Select a sample from a planetary catalogue
│   ├── download_PDC.py         # Retrieve TESS PDCSAP light curves
│   ├── null_PDCSAP_global.py   # Global BLS search
│   └── null_PDCSAP_local.py    # BLS search near known periods
├── Sample_Selection/
│   ├── Data/
│   │   ├── Sample.csv
│   │   ├── Tess_Sample.csv
│   │   ├── short_table_prueba.csv
│   │   └── PDC/                # Example light-curve data
│   └── Figures/                # Selected figures and figure notes
└── figuras-tessproject/        # Project and dataset illustrations
```

## Requirements

The scripts use Python and scientific-astronomy libraries, including:

- [NumPy](https://numpy.org/)
- [pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [Astropy](https://www.astropy.org/)
- [Lightkurve](https://lightkurve.github.io/)
- [SciPy](https://scipy.org/) (signal-processing and interpolation utilities used by the BLS scripts)

A virtual environment is recommended to keep dependencies isolated. For example:

```bash
python3 -m venv .venv
source .venv/bin/activate        # Linux/macOS
python -m pip install --upgrade pip
python -m pip install numpy pandas matplotlib astropy lightkurve scipy
```

> **Compatibility note:** Some scripts use older Lightkurve interfaces. Depending on the installed package versions, these imports or calls may need updating. The repository does not currently include a pinned dependency file, so the commands above install current releases rather than guaranteeing an identical historical environment.

## Running the scripts

Run scripts from the repository root, for example:

```bash
python Scripts/sample_TESS.py
python Scripts/download_PDC.py
python Scripts/null_PDCSAP_global.py
python Scripts/null_PDCSAP_local.py
```

**Data-path note:** the scripts build their data paths relative to the `Scripts/` directory and expect a `Scripts/Data/` directory. In the repository as currently organized, the supplied CSV files are under `Sample_Selection/Data/`. Before running the scripts, either adjust the `data_path` definitions in the scripts or place/copy the required input files in the expected location.

The sample-selection script also expects a catalogue named `planets2020.csv`, which is not included in the repository snapshot. Obtain the appropriate catalogue and place it in the expected data directory before running that step. The scripts may download observations from MAST through Lightkurve, so internet access is required for retrieval.

## Data and reproducibility

- CSV files in `Sample_Selection/Data/` contain sample tables used or generated during the analysis.
- `Sample_Selection/Data/PDC/` includes an example photometric light-curve file.
- The scripts write derived parameters and tables as part of their processing. Check each script's input and output paths before running it to avoid overwriting existing files.
- The example files are not necessarily a complete reproduction package for every stage of the original analysis.

## Publication

This repository is related to the following publication:

**Astronomy & Astrophysics, 665, A157 (2022).**

- [Published article (A&A)](https://www.aanda.org/articles/aa/pdf/2022/09/aa43763-22.pdf)
- [Preprint on arXiv:2207.12498](https://arxiv.org/abs/2207.12498)

Please consult the paper for the scientific context, selection criteria, and interpretation of the results.

## Acknowledgements

This project uses data from NASA's Transiting Exoplanet Survey Satellite (TESS) and the Python astronomy ecosystem, including Lightkurve and Astropy. Please cite the relevant software and data sources when using them in research.
