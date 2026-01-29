# Compute and plot ocean variables seasonality
> The scripts in this project computes the seasonality of ocean variables (e.g. biomolecules, phytoplankton concentration and SIC) and Organic mass fraction from marine biomolecules.\
> Biomolecules (DCAA and PL) were computed based on FESOM-REcoM tracers. See more information in [Leon-Marcos et al. 2025](https://doi.org/10.5194/egusphere-2025-2829). The data to reproduce the results are publicly accessible on Zenodo (https://doi.org/10.5281/zenodo.15172565)\
> The conda environment for this project is contained in env.yml file. Run [start_env.py](start_env.py) to set up and start the environment for this project.

* Customize the desire experiments (e.g. regions to select) and directories to the data in [global_vars.py](utils_functions/global_vars.py) file.
* Run [Seasonality_regions.py](calculate_seasonality/Seasonality_regions.py) to compute the multiannual monthly mean of all variables.
* Run [plot_figures.py](calculate_seasonality/plot_figures.py) to create all figures (information of the figures that are created is provided in this file).