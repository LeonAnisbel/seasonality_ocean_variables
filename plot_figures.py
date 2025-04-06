import pickle
import plots

with open('reg_data_global_regions.pkl', 'rb') as f:
    reg_data_globe = pickle.load(f)
plots.plot_seasonality_regions(reg_data_globe)

with open('reg_data_stat_bx.pkl', 'rb') as f:
    reg_data_globe_stat = pickle.load(f)
plots.plot_seasonality_regions_with_stations(reg_data_globe_stat)