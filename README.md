# MUSIC_with_python
![Examples of some plots using Matplotlib and Seaborn of MUSIC data.](./doc/img/image_main.jpg)
Example Python scripts for the analysis of data from the ANL MUSIC detector.

WORK IN PROGRESS!

## Argonne MUSIC Detector
For more information on the MUSIC detector, see [Nucl. Instrum. Meth. A 799, 197 (2015)](https://doi.org/10.1016/j.nima.2015.07.030) about the use of MUSIC with radioactive beams, and see [Nucl. Instrum. Meth. A 859, 63 (2017)](https://doi.org/10.1016/j.nima.2017.03.060) to learn more about the use of MUSIC to measure ($\alpha$,p) and ($\alpha$,n) reactions.

## FAQ

Q: Why should I use Python instead of the standard particle physics code ROOT?

A: There is no difference in doing analysis on experimental data with ROOT or Python. At the end of the day you want to get some measurable (cross section, mass, charge, yield, etc...) choice of code should not matter. I prefer Python; most other people work with ROOT. If you want to see an example of some very nice ROOT scripts to analyze MUSIC data, see [MUSIC_CoMPASS_softwares](https://github.com/CFougeres/MUSIC_CoMPASS_softwares).

Q: Why did you write these as "simple" scripts? Why not a library or something more like a package?

A: I would definitely not claim the code here is perfect or even optimal. This should be treated as a set of minimal viable beta scripts. I do plan to refactor these into a nicer format at some point. But, for the moment, these are here to give an idea of how to work with MUSIC data within Python.
