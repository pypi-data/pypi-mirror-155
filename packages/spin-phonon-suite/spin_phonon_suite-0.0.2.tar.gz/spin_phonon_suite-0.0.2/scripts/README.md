# Solid Sate Spin Phonon Coupling Calculations

These instructions detail how to install and use the solid state spin phonon program sp_ss.py

## Installation - CSF

This guide assumes you are using the Computational Shared Facility (CSF) at the University of Manchester.

### Requirements

- Conda (Anaconda Python)
- Chilton Group Python packages `molcas_suite` and `gaussian_suite` installed using `pip`
- Python package `xyz-py` installed using `pip`
- Python package `phonopy` installed using `condaforge`

### Setting up your conda env

To keep the installation clean, you must use a conda environment. This makes a specific copy of python which is sandboxed from any other copies you may have. 

Start by adding the following command to your `~/.bashrc` file. This will load anaconda python every time you log in.

```
module load apps/binapps/anaconda3/2019.07
```

If you already have this line, **do not re-add it**.

Now initialise conda in your shell

```
conda init bash
```
answering `yes` to any prompts.

and disable the `(base)` conda environment

```
conda config --set auto_activate_base false 
```

Restart your shell if you are prompted to

Now create a conda environment for sp_ss.py to run in. In this example the conda environment will be called `sp_ss_env`

```
conda create -n sp_ss_env
```
answering `yes` to any prompts.

To enter the environment type

```
conda activate sp_ss_env
```

and to leave type
```
conda deactivate
```

### Installing dependencies

First add the following proxy module load to your `~/.bashrc` file

```
module load tools/env/proxy2
```

If you already have this line, **do not re-add it**

To install the packages required to run `sp_ss.py` first enter your conda environment

```
conda activate sp_ss_env
```

Then install the `pip` package manager

```
conda install pip
```

answering `yes` to any prompts.

When this is complete, install the `xyz-py`, `molcas_suite` and `gaussian_suite` packages
```
pip install xyz-py molcas_suite gaussian_suite --user
```

Now install `phonopy` using `condaforge`

```
conda install -c conda-forge phonopy
```
answering `yes` to any prompts.
