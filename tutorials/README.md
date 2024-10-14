# Tutorial Notebooks
Here is a collection of Jupyter notebooks that cover the basics of manipulating and exploring MUSIC experiment data with Python. Included in this directory is a ROOT file "test_music_data.root" which contains data from a MUSIC fusion experiment with a $`^{20}`$Ne beam on CH$`_{4}`$ gas. This experiment used the older analog DAQ; therefore, extending these examples to newer digital DAQ experiments requires minor modifications in the ROOT->DataFrame conversion from the difference in the ROOT file structure (digital DAQ experiments have slightly different branches than the older analog DAQ ROOT files). 

## 1 - Looking at a MUSIC ROOT data file with uproot.
Use uproot to read a MUSIC experiment ROOT file and do basic histograms.

## 2 - Getting MUSIC traces.
Convert ROOT file to pandas DataFrame. Basic plotting of traces. Saving a DataFrame as a CSV or feather file.

## 3 - Basic Analysis and Identifying Potential Events.
Manipulating data in the DataFrame. Removing pile-up events. Normalizing anode strips. Basic cuts to identify potential fusion events.

## 4 - Plotting with Seaborn
Some examples of basic plots of MUSIC data using seaborn.

## 5 Playing with Scikit-Learn
Some examples of using some scikit-learn functions and algorithms on MUSIC data.

## 6 Manifold Clustering with t-SNE
An example of using t-SNE manifold clustering via openTSNE on MUSIC data.
