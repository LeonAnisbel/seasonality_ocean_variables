import os
from utils_functions import global_vars

os.system('conda env_seasonality create -f env.yml')
os.system('conda activate env_seasonality')


try:
    os.makedirs(global_vars.plot_dir)
except OSError:
    pass

try:
    os.makedirs(global_vars.pkl)
except OSError:
    pass

