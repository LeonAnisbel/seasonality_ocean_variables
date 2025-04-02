import pickle
import plots
#reg_data.pkl
with open('reg_data.pkl', 'rb') as f:
    reg_data_globe = pickle.load(f)


plots.plot_seasonality_regions(reg_data_globe)
