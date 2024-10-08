# MUSIC_with_python
[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![jupyter](https://img.shields.io/badge/Jupyter-Lab-F37626.svg?style=flat&logo=Jupyter)](https://jupyterlab.readthedocs.io/en/stable)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![Examples of some plots using Matplotlib and Seaborn of MUSIC data.](./doc/img/image_main.jpg)

A collection of example Python scripts and tutorials on using Python to analyze data from the ANL MUSIC detector.

WORK IN PROGRESS!

You can check out the first example notebook on binder

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/dneto1729/MUSIC_with_python/main?labpath=tutorials%2F1+-+Looking+at+a+MUSIC+ROOT+data+file+with+uproot.ipynb)

## Requirements

The tutorials and scripts here use several well-known Python packages (NumPy, SciPy, Pandas, scikit-learn, seaborn). To read/write ROOT files, you must install [uproot](https://pypi.org/project/uproot/). Since these experiment files are often quite large (several GB), anything saved after pulling from the ROOT container is done in the Apache Arrow format using [PyArrow](https://arrow.apache.org/docs/python/index.html), which can natively be read/write with Pandas. Finally, since it is always nice to have progress bars, some of these scripts use [tqdm](https://github.com/tqdm/tqdm), a lightweight package for progress bars. 

## Setup

You can use Conda, a combination of Conda with pip, or the native Python environment tool venv in conjunction with pip. First, clone the repo
```
git clone https://github.com/dneto1729/MUSIC_with_python.git
```
and cd in the new directory
```
cd MUSIC_with_python
```
### Using Conda:
To install a [new environment using Conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) using the included enviroment.yml file do:
```
conda env create -f environment.yml
```
With the packages installed, you can then activate the new environment with
```
conda activate music_py
```
### Create an environment with Conda but handle packages with pip:
First, create and activate an environment with Conda by doing:
```
conda create -n music_py python=3.9
```
Then, activate the new environment:
```
conda activate music_py
```
Using pip with the requirements.txt file, install the necessary packages and dependencies with:
```
pip install -r requirements.txt
```
### Using venv and pip:
Using venv is slightly more OS dependent. However, it comes with the advantage of being a native Python package, so it is a useful alternative if you can't install Conda. [To set up an environment with venv, follow the instructions here for your OS](https://docs.python.org/3/library/venv.html). Then, in your new environment, you can install the packages and dependencies using pip with the included requirement.txt file by doing the following:
```
pip install -r requirements.txt
```

## Argonne MUSIC Detector
For more information on the MUSIC detector, see [Nucl. Instrum. Meth. A 799, 197 (2015)](https://doi.org/10.1016/j.nima.2015.07.030) about the use of MUSIC with radioactive beams, and see [Nucl. Instrum. Meth. A 859, 63 (2017)](https://doi.org/10.1016/j.nima.2017.03.060) to learn more about the use of MUSIC to measure ($\alpha$,p) and ($\alpha$,n) reactions.

## Working with Uproot
Some of the examples here build off of the excellent [Uproot Tutorial](https://masonproffitt.github.io/uproot-tutorial/) by Mason Proffitt. For more info on uproot, see the [uproot documentation](https://uproot.readthedocs.io/en/latest/index.html). 

## FAQ

Q: Why use uproot instead of just using ROOT directly with PyROOT?

A: One could certainly install ROOT and, with PyROOT, do many of the same things (using functions from NumPy, SciPy, scikit-learn, etc...). However, you could then ask yourself, why use PyROOT to access some functions from NumPy when ROOT already has built-in stats and numerical analysis functions? First, it never hurts to have an alternative. Second, getting ROOT to run on Windows is always challenging; with uproot, you can open, read, and write ROOT files all within Python. Third, there are a ton of really cool Python packages that can do things "out of the box," which, in many cases, you would have to build from scratch to replicate with ROOT or C++.  

Q: Why should I use Python instead of the standard particle physics code ROOT?

A: There is no difference in analyzing experimental data with ROOT or Python. Ultimately, if you want to get some measurable (cross section, mass, charge, yield, etc.), the choice of code should not matter. I prefer Python; most other people work with ROOT. If you want to see an example of some very nice ROOT scripts to analyze MUSIC data, see [MUSIC_CoMPASS_softwares](https://github.com/CFougeres/MUSIC_CoMPASS_softwares).

Q: Why did you write these as "simple" scripts? Why not a library or something more like a package?

A: I would not claim the code here is perfect or even optimal. This should be treated as a set of minimal viable beta scripts. I do plan to refactor these into a nicer format at some point. But, for the moment, these are here to give an idea of how to work with MUSIC data using Python.
