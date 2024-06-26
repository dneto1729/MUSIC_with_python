"""An example script which takes the strip0cut normalized feather file and 
generates a feather file with only potential events in strip 3.
author: David Neto
usage: python music_evt_in_strip3.py <input.feather>
"""

import sys
# import numpy as np
import pandas as pd
# from tqdm import tqdm

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
print(df)

# Check for above threshold in strip 3
# Beam is in left channel in strip 3
print('Strip 3 L above Threshold')
print('=====================================================================')
THRESHOLD = 600
# Logic is backwards, should be inplace = False for > ?
df.drop(df.loc[df['s3L'] < THRESHOLD].index, inplace = True)
# Drop removes values if return is true
# Check beam like in strip 2 and strip 1
print('Beamlike in Strip 2 and 1')
print('=====================================================================')
# Strip 2 beam in right
df.drop(df.loc[df['s2R'] > THRESHOLD].index, inplace = True)
# Strip 1 beam in left
df.drop(df.loc[df['s1L'] > THRESHOLD].index, inplace = True)
print('=====================================================================')
print('Above Threshold in Strip 4')
# Strip 5L
df.drop(df.loc[df['s4R'] < THRESHOLD].index, inplace = True)
print('=====================================================================')
print('Below Beam in Strip 16')
print('=====================================================================')
# Strip 16 below beam in Right
df.drop(df.loc[df['s16R'] > 0.5*THRESHOLD].index, inplace = True)

# Remove old index
df.loc[:].reset_index(drop=True, inplace=True)
print(df)

# # Save dataframe to some format
file_save_name = FILE_NAME[:-8] + '_Strip3.feather'
print('Saving to ' + file_save_name)
print('=====================================================================')
df.to_feather(file_save_name)

# Save dataframe to csv
# file_save_name = FILE_NAME[:-8] + '_Strip3.csv'
# print('Saving to ' + file_save_name)
# print('=====================================================================')
# df.to_csv(file_save_name, index=False)
