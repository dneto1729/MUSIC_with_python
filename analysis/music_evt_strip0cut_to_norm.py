"""Take the strip0cut feather file and generate a normalized dataset. For
the segmented anode the short strips are offset corrected such that
the bin which should be the "zero" bin is close to channel zero (minimize
any low channel shelf). Then the beam profile of the long strips is fit with a 
Gaussian, to generate the normalization factor. This normalization factor
is applied to both the left and right segment on a per strip basis.
author: David Neto
usage: python music_evt_strip0cut_to_norm.py <input.feather>
"""

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from tqdm import tqdm

def gauss(x, a, mu, sigma):
    ''' Non-normalized Gaussian function.
    
    Parameters
    ----------
    x : float
        Point to evaluate function at.
    a : float
        Height of curve at center.
    mu : float
        Location of center of curve.
    sigma : float
        Standard deviation.
            
    Returns
    -------
    out : float
        Value of function.
    '''
    return a*np.exp(-(x-mu)**2/(2*sigma**2))

def main():
    '''
    Normalize the input file and save the output to a new feather file.
    '''

    file_name = ''
    # Check for file
    if len(sys.argv) == 1:
        print('Need file to import data, check usage')
        sys.exit(0)
    else:
        file_name = sys.argv[1]

    print('=' * 80)
    print('Opening ' + file_name)
    print('=' * 80)

    df = pd.read_feather(file_name)
    print(df.describe())

    norm_to = 500.0
    print(f'Normalizing Beam to {norm_to}')
    print('=' * 80)

    # Setting up some arrays
    beam_strips = []
    short_strips = []
    for i in range(1,17,2):
        beam_strips.append(f's{i}L')
        beam_strips.append(f's{i+1}R')
        short_strips.append(f's{i}R')
        short_strips.append(f's{i+1}L')

    # Strip 0 and 17
    for i in ('s0','s17'):
        mean_gauss = 0.0
        # do histogram
        counts, bins, _ = plt.hist(df[i], bins=200, histtype='step')
        # for p0
        max_indx = np.unravel_index(np.argmax(counts), counts.shape)
        max_counts = counts.max()
        # center bins
        cen_bins = bins[:-1] + np.diff(bins) / 2
        # Fit
        # pylint: disable-next=unbalanced-tuple-unpacking
        param, _ = curve_fit(gauss, cen_bins, counts,
                        p0=(max_counts, bins[max_indx], 10))
        # Get Mean of Gauss
        mean_gauss = param[1]
        # normalize
        df[i] = df[i]*(norm_to/mean_gauss)
        # Close
        plt.close()

    # Middle Anode
    for i in tqdm(range(0,16)):
        mean_gauss = 0.0
        short_offset = 0.0
        # do histogram
        counts, bins, _ = plt.hist(df[beam_strips[i]], bins=200, histtype='step')
        counts_short, bins_short, _ = plt.hist(df[short_strips[i]],
                                                            bins=100,
                                                            range=[0, 500],
                                                            histtype='step',
                                                            label='short')
        # for p0
        max_indx = np.unravel_index(np.argmax(counts), counts.shape)
        max_counts = counts.max()
        # center bins
        cen_bins = bins[:-1] + np.diff(bins) / 2
        cen_bins_short = bins_short[:-1] + np.diff(bins_short) / 2
        # Fit
        # pylint: disable-next=unbalanced-tuple-unpacking
        param, _ = curve_fit(gauss, cen_bins, counts,
                        p0=(max_counts, bins[max_indx], 10))
        # Get Mean of Gauss
        mean_gauss = param[1]
        # shift of short strips
        nonzero_counts = np.nonzero(counts_short)
        indx_first_nonzero = nonzero_counts[0][0]
        short_offset = cen_bins_short[indx_first_nonzero]
        # normalize
        df[beam_strips[i]] = df[beam_strips[i]]*(norm_to/mean_gauss)
        df[short_strips[i]] = (df[short_strips[i]] - short_offset)*(norm_to/mean_gauss)
        # Close
        plt.close()

    print('Normalized')
    print('=' * 80)
    print(df.describe())

    # Save dataframe to feather file
    file_save_name = file_name[:-8] + '_norm.feather'
    print('Saving to ' + file_save_name)
    print('=' * 80)
    df.to_feather(file_save_name)

if __name__ == "__main__":
    main()
