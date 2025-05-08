import numpy as np
path_omf =  f"/Users/Leon/Desktop/Folder_from_linux/Downloads/Observ_sites_maps/Burows_param/"
path_ocean = f"/Users/leon/Desktop/Burrows_param/DATA_BGC_model/fesom-recon_BGC/regular_grid_interp/"
seasonality_stations = True
plot_dir = './plots/'
data_dir = '/Users/Leon/Desktop/Folder_from_linux/Downloads/ocean_data/yearly_data/'
color_regions = ['royalblue', 'orange', 'limegreen', 'pink', 'orangered', 'purple']
units_concentration = 'mmol C m$^{-3}$'
arctic_regions = False # comment if not wanted
colors_arctic_reg = ['k', 'r', 'm', 'pink', 'lightgreen', 'darkblue', 'orange',
                 'brown', 'lightblue', 'y', 'gray']
months = np.arange(0, 12)
