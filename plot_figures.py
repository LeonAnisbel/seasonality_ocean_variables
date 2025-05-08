import pickle

import arctic_plots
import global_vars
import plots

stations_seasonality = global_vars.seasonality_stations

if global_vars.arctic_regions:
    with open('reg_data_arctic_regions.pkl', 'rb') as f:
        reg_data_globe_stat = pickle.load(f)
        arctic_plots.seasonality_conc_omf_arctic_and_reg(reg_data_globe_stat)
        print('Done')
        arctic_plots.seasonality_plot_thesis(reg_data_globe_stat)
        arctic_plots.regions_map(reg_data_globe_stat)
if stations_seasonality:
    with open('reg_data_stat_bx.pkl', 'rb') as f:
        reg_data_globe_stat = pickle.load(f)
    plots.plot_seasonality_regions_with_stations(reg_data_globe_stat)
else:
    with open('reg_data_global_regions.pkl', 'rb') as f:
        reg_data_globe = pickle.load(f)
    plots.plot_seasonality_regions(reg_data_globe)