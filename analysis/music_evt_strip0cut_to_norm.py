"""Take the strip0cut feather file and generate a normalized dataset.
Normalize strips (beam side) to 500.
author: David Neto
usage: python music_evt_strip0cut_to_norm.py <input.feather>
"""

import sys
import numpy as np
import pandas as pd
from tqdm import tqdm

FILE_NAME = ''

# Check for file
if len(sys.argv) == 1:
    print('Need file to import data, check usage')
    sys.exit(0)
else:
    FILE_NAME = sys.argv[1]

print('=====================================================================')
print('Opening ' + FILE_NAME)
print('=====================================================================')

df = pd.read_feather(FILE_NAME)
print(df.describe())

print('Normalizing Beam to 500')
print('=====================================================================')
# Strip0
df.iloc[:, 0] = df.iloc[:, 0]*(500/np.mean(df.iloc[:, 0]))

# Beam Strips
beam = [1,4,5,8,9,12,13,16,17,20,21,24,25,28,29,32]
no_beam = [2,3,6,7,10,11,14,15,18,19,22,23,26,27,30,31]
left_strips = np.arange(1, 32, 2)
right_strips = np.arange(2, 33, 2)

# Per Strip on Beam Side
# for i in tqdm(range(len(beam))):
#     # Left
#     df.iloc[:, left_strips[i]] = df.iloc[:, left_strips[i]]*(500/np.mean(df.iloc[:, beam[i]]))
#     # Right
#     df.iloc[:, int(left_strips[i])+1] = df.iloc[:, int(left_strips[i])+1]*(500/np.mean(df.iloc[:, beam[i]]))
# # Strip17
# df.iloc[:, 33] = df.iloc[:, 33]*(500/np.mean(df.iloc[:, 33]))

# Beam side 500, non Beam 50
# Beam
for i in tqdm(range(len(beam))):
    df.iloc[:, beam[i]] = df.iloc[:, beam[i]]*(500/np.mean(df.iloc[:, beam[i]]))
# No Beam
for i in tqdm(range(len(no_beam))):
    df.iloc[:, no_beam[i]] = df.iloc[:, no_beam[i]]*(50/np.mean(df.iloc[:, no_beam[i]]))

# Strip17
df.iloc[:, 33] = df.iloc[:, 33]*(500/np.mean(df.iloc[:, 33]))

print('Normalized')
print('=====================================================================')
print(df.describe())


# Save dataframe to some format
file_save_name = FILE_NAME[:-8] + '_norm.feather'
print('Saving to ' + file_save_name)
print('=====================================================================')
df.to_feather(file_save_name)
