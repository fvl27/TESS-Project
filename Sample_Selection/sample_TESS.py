#! /bin/env python

#Fisrt part! From the full planets2020.csv previuously downloaded from the exoplanet ebsite, this script selects
# the items with the conditions in 'cond' and conforms a sample

import pandas as pd
import numpy as np
import os
import pathlib

# Read exoplanet.eu catalog

path = os.path.abspath(os.path.dirname(__file__))

data_path = pathlib.Path(path) / "Data"

filename = data_path / "planets2020.csv"

cat = pd.read_csv(filename, index_col='pl_name', header=0, comment='#')

cond = (cat['sy_pnum'] > 1) & (cat['discoverymethod']== 'Radial Velocity') & (cat['pl_orbper'] < 30) & (cat['pl_rade'].isnull()) & (cat['pl_bmasse'] < 20)

cc = cat.loc[cond]
cc.to_csv("/media/flavia/35744470-866d-4558-a059-cb47f71de7e3/home/flavia/Documentos/TESS/pandas-EXO/Git-hub/Data/Sample.csv")

# Second part! Check for TESS data using Lightkurve - Python package for Kepler and TESS data analysis
# (Lightkurve Collaboration et al. 2018).
# Also adding a new column with the Tess observed sectors for each star

import lightkurve as lk

filename2 = data_path /"Sample.csv"

cat2 = pd.read_csv(filename2, index_col='pl_name', header=0, comment='#')

# Set a empty variable for addding stars

already_searched = []

cat2.loc[:, 'sectors'] = None

for i, planet in enumerate(cat2.index):
    print(planet)
    star = str(cat2.loc[planet, 'tic_id'])

    print(star)
    if star in already_searched:
        cat2.loc[planet,'sectors'] = str(sectors)
        continue

    result = lk.search_tesscut(star)
    print(result)


    try:
        sectors = result.table['sequence_number'].data
        print(sectors)
    except KeyError:
        sectors = np.array([])


    # Set paramater on row
    cat2.loc[planet,'sectors'] = str(sectors)

    # Add star to already searched
    already_searched.append(star)

cond2 = (cat2['sectors'] != '[]')
cc2 = cat2.loc[cond2]

# Save CSV
sample_file = data_path / "Tess_Sample.csv"
cc2.to_csv(sample_file)
