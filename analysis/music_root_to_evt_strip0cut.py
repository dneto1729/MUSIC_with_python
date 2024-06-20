"""File to look at and generate a feather file from a MUSIC events ROOT file.
Takes input ROOT file and process using uproot. Output file is event data along 
row. Good events are taken from a cut on strip0 and cut on strip17.
This is setup for the "analog DAQ" ROOT files, the newer "digital DAQ" ROOT
files have a slightly different format.
author: David Neto
usage: python music_root_to_evt_strip0cut.py <input.root>
"""

import sys
import uproot
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LogNorm

# import numpy as np
import pandas as pd

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
# Open file
file = uproot.open(FILE_NAME)

print('Getting tree and building branches to arrays...')
print('=====================================================================')

# Read TTree
tree = file['tree']

# Get branches
branches = tree.arrays()

# Plotting

# Use more REVTEX-esque fonts?
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["font.serif"] = "STIXGeneral"
mpl.rcParams["mathtext.fontset"] = "stix"

#
fig, ax = plt.subplots(2,2)

plt.suptitle(FILE_NAME)
ax[0,0].hist(branches['strip0'],
        bins=100)
ax[0,0].set_title('strip0')
ax[0,0].set_yscale('log')
#
ax[0,1].hist(branches['strip17'],
        bins=100)
ax[0,1].set_title('strip17')
ax[0,1].set_yscale('log')
#
ax[1,0].hist2d(branches['strip0'],branches['grid'],
               bins=400,
               norm=LogNorm())
ax[1,0].set_xlabel('strip0')
ax[1,0].set_ylabel('grid')
#
ax[1,1].hist2d(branches['tac'],branches['cath'],
               bins=100,
               norm=LogNorm())
ax[1,1].set_xlabel('tac')
ax[1,1].set_ylabel('cath')
ax[1,1].set_ylim(0,1400)

plt.tight_layout()
plt.show()

# User input for cuts
LOW_CUT = input('For Strip0 where to put lower cut:')
HIGH_CUT = input('For Strip0 where to put upper cut:')
# S17_CUT = input('Upper limit for Strip17:')

# Strip0 mask
strip0_mask = (int(LOW_CUT) <= branches['strip0']) & (branches['strip0'] <= int(HIGH_CUT))

total_events = len(branches['strip0'])/16
print('=====================================================================')
print('Total entries in ' + FILE_NAME + ' = ' + str(total_events))
print('Cutting on strip0 reduces this to ' \
    + str(len(branches['strip0'][strip0_mask])/16) + ' entries')
print('=====================================================================')
# Include Strip17 mask
# strip0_mask = (int(LOW_CUT) <= branches['strip0']) & \
    # (branches['strip0'] <= int(HIGH_CUT)) & (branches['strip17'] < int(S17_CUT))
# print(' Using a cut on strip0 and strip17 yields ' \
#     + str(len(branches['strip0'][strip0_mask])) + ' entries')
# print(' Cut on strip0 and strip17 gives us ' \
#     + str(int(len(branches['strip0'][strip0_mask])/16)) \
#     +  ' good events out of the ' + str(int(total_events/16)) \
#     + ' total events in ' + FILE_NAME)
# print('=====================================================================')

# Apply cuts as mask
cut_run = branches[strip0_mask]

# To DataFrame

dict_branches = {}

# strip0 first
dict_branches.update({'s0':cut_run['strip0'][cut_run['seg'] == 1]})
# segmented anode, left first then right
for i in range(1,17):
    dict_branches.update({'s%iL' % i : cut_run['edepl'][cut_run['seg'] == i]})
    dict_branches.update({'s%iR' % i  : cut_run['edepr'][cut_run['seg'] == i]})
# strip17 last
dict_branches.update({'s17':cut_run['strip17'][cut_run['seg'] == 1]})

df = pd.DataFrame(dict_branches)

# Save dataframe to feather file
file_save_name = FILE_NAME[:-5] + '_evt_strip0cut.feather'
print('Saving to ' + file_save_name)
print('=====================================================================')
df.to_feather(file_save_name)
