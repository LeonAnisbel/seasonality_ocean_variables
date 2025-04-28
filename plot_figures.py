import pickle

import global_vars
import plots

stations_seasonality = global_vars.seasonality_stations

if stations_seasonality:
    with open('reg_data_stat_bx.pkl', 'rb') as f:
        reg_data_globe_stat = pickle.load(f)
    plots.plot_seasonality_regions_with_stations(reg_data_globe_stat)
else:
    with open('reg_data_global_regions.pkl', 'rb') as f:
        reg_data_globe = pickle.load(f)
    plots.plot_seasonality_regions(reg_data_globe)