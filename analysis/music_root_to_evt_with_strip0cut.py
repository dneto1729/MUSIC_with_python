"""File to look at generate csv/feather file from MUSIC events ROOT file. Takes
input ROOT file and process using uproot. Output file is event data along row.
Pile-up events are removed with a cut on strip 0.
author: David Neto
usage: python music_root_to_evt_strip0cut.py <input.root>
"""

import sys
import uproot
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LogNorm
from scipy.optimize import curve_fit
import numpy as np
import pandas as pd

def root_to_dataframe(file_name, full_output=False):
    ''' Takes an analog MUSIC ROOT file and pulls the anode into a DataFrame.

    This function uses uproot to read the ROOT file and pandas to create the
    DataFrame.
    
    Parameters
    ----------
    file_name : ROOT
        ROOT file to take anode data from.
    full_output : Boolean
        True to return DataFrame and branches object.

    Returns
    -------
    DataFrame
        DataFrame with the anode along columns and one event per row.
    Awkward array
        Awkward array of branches, only if full_output is true.

    '''
    print('=' * 80)
    print('Opening ' + file_name)
    # Open file
    file = uproot.open(file_name)
    print('=' * 80)
    print('Getting tree and building branches to arrays...')
    print('=' * 80)
    # Read TTree
    tree = file['tree']
    # Get branches
    branches = tree.arrays()
    # Make Dictionary
    dict_branches = {}
    # strip0 first
    dict_branches.update({'s0':branches['strip0'][branches['seg'] == 1]})
    # segmented anode, left first then right
    for i in range(1,17):
        dict_branches.update({f's{i}L' : branches['edepl'][branches['seg'] == i]})
        dict_branches.update({f's{i}R' : branches['edepr'][branches['seg'] == i]})
    # strip17 last
    dict_branches.update({'s17':branches['strip17'][branches['seg'] == 1]})
    # create dataframe
    print('Building DataFrame')
    print('=' * 80)
    df = pd.DataFrame(dict_branches)
    print(df.describe())
    if full_output is True:
        return df, branches
    return df

def summary_plot(branches, file_name='MUSIC Data Summary'):
    ''' Takes branches of MUSIC data, plot and save a figure of basic histograms.

    Parameters
    ----------
    branches : awkward array
        Awkward arrays from uproot containing the analog MUSIC ROOT data.
    file_name : string
        String used for plot title and terminal text, could be original ROOT
        file name.

    '''
    # Plotting
    # Use more REVTEX-esque fonts
    mpl.rcParams["font.family"] = "serif"
    mpl.rcParams["font.serif"] = "STIXGeneral"
    mpl.rcParams["mathtext.fontset"] = "stix"
    #
    _, ax = plt.subplots(2,2)
    plt.suptitle(file_name)
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
    #
    plt.tight_layout()
    file_save_name = file_name + '.png'
    plt.savefig(file_save_name, dpi=300)

def strip0_cut(df, auto_lims=True):
    ''' Apply strip 0 cut to DataFrame to remove pile-up events.
    
    Parameters
    ----------
    df : DataFrame
        DataFrame with anode strips across columns and one event per row.
    auto_lims : Boolean
        True means fit largest peak in histogram of strip 0 with a Gaussian 
        where the high cut value is then mean + 2*sigma of Guassian and low 
        cut value is mean - 2*sigma. False will cause code to prompt user in 
        terminal for high and low cut values.

    Returns
    -------
    DataFrame
        DataFrame with the strip 0 cut applied.

    '''
    if auto_lims is True:
        # Fit largest histogram peak with Gaussian
        counts, bins = np.histogram(df['s0'], bins=150)
        # Get center of bins
        center_bins = bins[:-1] + np.diff(bins) / 2
        # For p0
        max_indx = np.unravel_index(np.argmax(counts), counts.shape)
        max_counts = counts.max()
        # Function to optimize
        gauss = lambda x, a, mu, sigma : a*np.exp(-(x-mu)**2/(2*sigma**2))
        # Fit largest peak
        # pylint: disable-next=unbalanced-tuple-unpacking
        param, _ = curve_fit(gauss, center_bins, counts,
                            p0=(max_counts, bins[max_indx], 25))
        # Use mean and sigma to set cuts
        low_cut = param[1] - 2.0*param[2]
        high_cut = param[1] + 2.0*param[2]
    else:
        # Ask user for cuts
        low_cut = input('For Strip0 where to put lower cut:')
        high_cut = input('For Strip0 where to put upper cut:')
    #
    print('=' * 80)
    print(f'Strip 0 High Cut = {high_cut:.2f} Low Cut = {low_cut:.2f}')
    df.drop(df[low_cut > df.s0].index,
            inplace=True)
    df.drop(df[df.s0 > high_cut].index,
            inplace=True)
    print('=' * 80)
    #
    print(df.describe())
    return df

def main():
    ''' Open analog MUSIC ROOT file, create dataframe and cut pile-up in strip 0.
    
    '''
    save_plot = False # True to also make and save plot

    file_name = ''

    # Check for file
    if len(sys.argv) == 1:
        print('Need file to import data, check usage')
        sys.exit(0)
    else:
        file_name = sys.argv[1]

    # Save plot of Run summary
    if save_plot is True:
        df, branches = root_to_dataframe(file_name, True)
        summary_plot(branches, file_name)
    else: # Just get DataFrame
        df = root_to_dataframe(file_name)

    # do strip 0 cut
    df = strip0_cut(df, True).reset_index(drop=True)

    # Save to feather file
    file_save_name = file_name[:-5] + '_evt_strip0cut.feather'
    print('Saving to ' + file_save_name)
    print('=' * 80)
    df.to_feather(file_save_name)

if __name__ == "__main__":
    main()
