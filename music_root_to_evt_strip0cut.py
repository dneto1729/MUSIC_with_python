"""File to look at and generate a csv/feather file from a MUSIC events ROOT file.
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

import numpy as np
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

cut_run = branches[strip0_mask]

# To CSV
# file_save_name = FILE_NAME[:-5] + '_evt_strip0cut.dat'
# print('=====================================================================')
# print('Saving to ' + file_save_name)
# print('=====================================================================')

# with open(file_save_name, 'w', encoding='UTF-8') as f:
#     # for i in range(0, 16000,16): # look at 1000 events
#     for i in range(0, len(branches['strip0']), 16): # look at all "good events"
#         f.write(str(cut_run['strip0'][i]) \
#                 + ',' + str(cut_run['edepl'][i] + cut_run['edepr'][i]) \
#                 + ',' + str(cut_run['edepl'][i+1] + cut_run['edepr'][i+1]) \
#                 + ',' + str(cut_run['edepl'][i+2] + cut_run['edepr'][i+2]) \
#                 + ',' + str(cut_run['edepl'][i+3] + cut_run['edepr'][i+3]) \
#                 + ',' + str(cut_run['edepl'][i+4] + cut_run['edepr'][i+4]) \
#                 + ',' + str(cut_run['edepl'][i+5] + cut_run['edepr'][i+5]) \
#                 + ',' + str(cut_run['edepl'][i+6] + cut_run['edepr'][i+6]) \
#                 + ',' + str(cut_run['edepl'][i+7] + cut_run['edepr'][i+7]) \
#                 + ',' + str(cut_run['edepl'][i+8] + cut_run['edepr'][i+8]) \
#                 + ',' + str(cut_run['edepl'][i+9] + cut_run['edepr'][i+9]) \
#                 + ',' + str(cut_run['edepl'][i+10] + cut_run['edepr'][i+10]) \
#                 + ',' + str(cut_run['edepl'][i+11] + cut_run['edepr'][i+11]) \
#                 + ',' + str(cut_run['edepl'][i+12] + cut_run['edepr'][i+12]) \
#                 + ',' + str(cut_run['edepl'][i+13] + cut_run['edepr'][i+13]) \
#                 + ',' + str(cut_run['edepl'][i+14] + cut_run['edepr'][i+14]) \
#                 + ',' + str(cut_run['edepl'][i+15] + cut_run['edepr'][i+15]) \
#                 + ',' + str(cut_run['strip17'][i]) + '\n')

# To DataFrame
# First build numpy arrays for each strip
# Hard coded for now
print('Building Numpy Arrays')
print('=====================================================================')
strip_0 = np.array(cut_run['strip0'][cut_run['seg'] == 1])
strip_1L = np.array(cut_run['edepl'][cut_run['seg'] == 1])
strip_1R = np.array(cut_run['edepr'][cut_run['seg'] == 1])
strip_2L = np.array(cut_run['edepl'][cut_run['seg'] == 2])
strip_2R = np.array(cut_run['edepr'][cut_run['seg'] == 2])
strip_3L = np.array(cut_run['edepl'][cut_run['seg'] == 3])
strip_3R = np.array(cut_run['edepr'][cut_run['seg'] == 3])
strip_4L = np.array(cut_run['edepl'][cut_run['seg'] == 4])
strip_4R = np.array(cut_run['edepr'][cut_run['seg'] == 4])
strip_5L = np.array(cut_run['edepl'][cut_run['seg'] == 5])
strip_5R = np.array(cut_run['edepr'][cut_run['seg'] == 5])
strip_6L = np.array(cut_run['edepl'][cut_run['seg'] == 6])
strip_6R = np.array(cut_run['edepr'][cut_run['seg'] == 6])
strip_7L = np.array(cut_run['edepl'][cut_run['seg'] == 7])
strip_7R = np.array(cut_run['edepr'][cut_run['seg'] == 7])
strip_8L = np.array(cut_run['edepl'][cut_run['seg'] == 8])
strip_8R = np.array(cut_run['edepr'][cut_run['seg'] == 8])
strip_9L = np.array(cut_run['edepl'][cut_run['seg'] == 9])
strip_9R = np.array(cut_run['edepr'][cut_run['seg'] == 9])
strip_10L = np.array(cut_run['edepl'][cut_run['seg'] == 10])
strip_10R = np.array(cut_run['edepr'][cut_run['seg'] == 10])
strip_11L = np.array(cut_run['edepl'][cut_run['seg'] == 11])
strip_11R = np.array(cut_run['edepr'][cut_run['seg'] == 11])
strip_12L = np.array(cut_run['edepl'][cut_run['seg'] == 12])
strip_12R = np.array(cut_run['edepr'][cut_run['seg'] == 12])
strip_13L = np.array(cut_run['edepl'][cut_run['seg'] == 13])
strip_13R = np.array(cut_run['edepr'][cut_run['seg'] == 13])
strip_14L = np.array(cut_run['edepl'][cut_run['seg'] == 14])
strip_14R = np.array(cut_run['edepr'][cut_run['seg'] == 14])
strip_15L = np.array(cut_run['edepl'][cut_run['seg'] == 15])
strip_15R = np.array(cut_run['edepr'][cut_run['seg'] == 15])
strip_16L = np.array(cut_run['edepl'][cut_run['seg'] == 16])
strip_16R = np.array(cut_run['edepr'][cut_run['seg'] == 16])
strip_17 = np.array(cut_run['strip17'][cut_run['seg'] == 1])

# DEBUG
# print('s0 ' + str(len(strip_0)))
# print('s1L ' + str(len(strip_1L)))
# print('s1R ' + str(len(strip_1R)))
# print('s10L ' + str(len(strip_10L)))
# print('s10R ' + str(len(strip_10R)))
# print('s17 ' + str(len(strip_17)))

# Build dataframe from numpy arrays
# Hard coded for now
print('Building DataFrame')
print('=====================================================================')
evt_d = {'s0':strip_0,'s1L':strip_1L,'s1R':strip_1R,
         's2L':strip_2L,'s2R':strip_2R,'s3L':strip_3L,'s3R':strip_3R,
         's4L':strip_4L,'s4R':strip_4R,'s5L':strip_5L,'s5R':strip_5R,
         's6L':strip_6L,'s6R':strip_6R,'s7L':strip_7L,'s7R':strip_7R,
         's8L':strip_8L,'s8R':strip_8R,'s9L':strip_9L,'s9R':strip_9R,
         's10L':strip_10L,'s10R':strip_10R,'s11L':strip_11L,'s11R':strip_11R,
         's12L':strip_12L,'s12R':strip_12R,'s13L':strip_13L,'s13R':strip_13R,
         's14L':strip_14L,'s14R':strip_14R,'s15L':strip_15L,'s15R':strip_15R,
         's16L':strip_16L,'s16R':strip_16R,'s17':strip_17
         }

df = pd.DataFrame(evt_d)

# Save dataframe to some format
file_save_name = FILE_NAME[:-5] + '_evt_strip0cut.feather'
print('Saving to ' + file_save_name)
print('=====================================================================')
df.to_feather(file_save_name)
