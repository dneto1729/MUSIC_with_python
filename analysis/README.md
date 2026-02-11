# Example Analysis Scripts

In this folder are some example scripts for analyzing MUSIC data. The Python scripts have been set up for fusion experiment data, but they can easily be modified for working with simulated data or other types of reactions ($\alpha$,p), ($\alpha$,n), (p,$\alpha$), etc...

## music_root_to_evt_strip0cut.py
Converts a root file from an analog DAQ MUSIC experiment into a feather file where each row is one event and applies a cut in strip 0 to remove pileup. For the cut in strip 0, the script will open a window with a matplotlib plot, so you can see where you would want to cut in strip 0. When you close this matplotlib window, the code will prompt you in the command line where you would like to put the lower and upper limit of the cut in strip 0.

## music_evt_strip0cut_to_norm.py
Takes the feather file, which has had the cut in strip 0 applied from the "music_root_to_evt_strip0cut.py" script, and then normalizes the beam peak in each strip. For the middle (segmented) anode and offset is used in the short strips to try to mitigate the effect of the "shelf" from the SCARLET DAQ.

## music_evt_in_strip3.py
This Python script demonstrates one way to generate an output file containing a subset of candidate fusion events in strip 3 of the MUSIC detector. These potential events are saved in a new file, which can then be used in an analysis pipeline, working with a smaller set of "interesting traces" rather than the entire event set.

## simROOT_to_Values.C
A ROOT macro to convert a root file from the [MUSIC simulation code](https://gitlab.phy.anl.gov/music/sim/-/tree/master?ref_type=heads) into a CSV-formatted file with each event on a separate row. The CSV output has the $\Delta$E of each strip (s0, s1L, s1R, s2L, s2R, ..., s17) as separate columns, followed by two more columns, one with the range in mm of the heavy recoil, and the kinetic energy in MeV of the heavy recoil. Note: The last two columns return the values for the residue, so in the simulation code this is "res0", which by convention is usually taken as the heavy residue.  
