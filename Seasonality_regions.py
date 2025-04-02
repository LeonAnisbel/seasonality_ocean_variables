#!/usr/bin/env python
# coding: utf-8

# <h1><center> Macromolecular Surface concentration </center></h1>
# 
# <h4><center> Author: Anisbel León Marcos${^1}$ </center></h4>
# <h6><center> ${^1}$Institute for Tropospheric Research (TROPOS)
#  ${^1}$leon@tropos.de  
# </center></h6>
# 
# <br/>

# ### Models :
# 
# #### - Finite-Volume sea-ice ocean model  <a href="https://fesom.de/models/fesom20/">(FESOM2) </a>
# > ##### Unstructured mesh, potimized for the Arctic
# 
# #### - Regulated Ecosystem Model  <a href="https://ui.adsabs.harvard.edu/abs/2018PrOce.168...65S/abstract">(FESOM-REcoM2) </a>
# > ##### Include two phytoplankton classes and coupled with FESOM2
# 
# 
# ### Equations: 
# > #### Adapted from <a href="https://doi.org/10.5194/gmd-16-4883-2023">(Gürses et al. 2023) </a>
# 
# <br/>

# ##### Import packges

# In[1]:


import numpy as np
import pandas as pd
import os,glob,sys
import pickle
import plots
import utils
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.patches as mpatches


#path_ocean = f"/Users/leon/Desktop/Burrows_param/DATA_BGC_model/fesom-recon_BGC/regular_grid_interp/"
path_omf = '/home/manuel/Downloads/Observ_sites_maps/Burows_param/'


try:
    os.mkdir('plots')
except OSError:
    pass

try:
    os.mkdir('plots/Sfc_conc_plots')
except OSError:
    pass

plot_dir = './plots/'


data_dir = '/home/manuel/Downloads/ocean_data/yearly_data/'
C_ice =  utils.read_files_data(data_dir + 'ice_var*')['sic']
C_ice_msk = utils.read_files_data(data_dir + 'mask_ice*')['sic']
C_pl = utils.read_files_data(data_dir + 'PL_var_*')['PL'] * C_ice_msk
C_pcho = utils.read_files_data(data_dir + 'PCHO_var_*')['PCHO'] * C_ice_msk
C_dcaa = utils.read_files_data(data_dir + 'DCAA_var_*')['DCAA'] * C_ice_msk
C_conc_tot = C_pl+C_pcho+C_dcaa

C_omf = utils.read_files_data(path_omf + "oceanfilms_omf_*")
C_omf_pol = C_omf['OMF_POL']
C_omf_pro = C_omf['OMF_PRO']
C_omf_lip = C_omf['OMF_LIP']
C_omf_tot = C_omf_pol + C_omf_pro + C_omf_lip



months = [np.arange(1,13)]
lat = C_omf.lat
lon = C_omf.lon
conditions = [[[lat, 63, 82], [lon, 1, 10]],
              [[lat, 37, 42], [lon, -75 , -65]],
              [[lat, 36, 45], [lon, 1, 14]],
              [[lat,12,25], [lon, -32, -18]],
              [[lat, -17, -5], [lon, -85, -77]],
              [[lat, -70, -58], [lon, -70, -58]],]

reg_data_globe = {'NAO':[],
           'NWAO, SB':[],
           'AS, WMED':[],
            'SATL, CVAO': [],
            'PUR': [],
            'WAP': []
                  }

fig = plt.figure(figsize=(6, 4))
projection = ccrs.Robinson(central_longitude=30)
ax = plt.axes(projection=projection)
ax.coastlines(resolution='110m', color='k')
ax.set_extent([-100, 60, -90, 90], crs=ccrs.PlateCarree())
colors = ['b', 'r', 'brown', 'lightgreen', 'pink', 'orange']
for i, c, n in zip(conditions, colors, list(reg_data_globe.keys())):
    low_lim_lat = i[0][1]
    low_lim_lon = i[1][1]
    upper_lim_lat = i[0][2]
    upper_lim_lon = i[1][2]
    print(upper_lim_lon-low_lim_lon, upper_lim_lat-low_lim_lat)
    pl = ax.add_patch(mpatches.Rectangle(xy=[low_lim_lon, low_lim_lat],
                                    width=upper_lim_lon-low_lim_lon,
                                    height=upper_lim_lat-low_lim_lat,
                                   facecolor=c, edgecolor=c,
                                   label=n,
                                   transform=ccrs.PlateCarree()))
gl = ax.gridlines(draw_labels=True,
              x_inline=False,
              y_inline=False)  # adding grid lines with labels
gl.top_labels = False
gl.right_labels = False
plt.legend()
plt.tight_layout()
plt.savefig('Map_boxes.png', dpi=300)


for na in reg_data_globe.keys():
    reg_data_globe[na]={'months_30_yr':[]}
    for i,mo in enumerate(reg_data_globe[na].keys()):
        reg_data_globe[na][mo]= {
                              'var_seasonality':{'OMF':[]}, #'Biom':[],
                              'var_season_std':{ 'OMF':[]}, #'Biom':[],
                              }
        for v,va in enumerate(reg_data_globe[na][mo].keys()):
            reg_data_globe[na][mo][va]['Biom']= {'Total concentration':[],
                                            'PL':[],
                                            'PCHO':[],
                                            'DCAA':[],
                                            }
            reg_data_globe[na][mo][va]['OMF']= {
                                           'Total OMF':[],
                                           'PCHO':[],
                                           'DCAA':[],
                                           'PL':[],}

var_ocean = [C_conc_tot,
            C_pl,
            C_pcho,
            C_dcaa]

var_omf = [C_omf_tot,
             C_omf['OMF_POL'],
             C_omf['OMF_PRO'],
           C_omf['OMF_LIP'],
           ]


years_set = [[1989,2020]]*len(months)

data = []
for i_id, var in enumerate([var_ocean, var_omf]):
    if i_id == 0:
        v_id = 'Biom'
    elif i_id == 1:
        v_id = 'OMF'
    
    print(i_id, v_id)
    region = []
    season = []
    var_value = []
    var_std = []
    var_na = []


    for i,na in enumerate(reg_data_globe.keys()):   
        print(na)
        for y,yr in enumerate(list(reg_data_globe[na].keys())):
            mon = months[y]

            print(yr, mon)
            var_mo_season, var_season_std = utils.find_region(var,
                                                         conditions[i], 
                                                         mon,
                                                         na,
                                                         years_set[y],
                                                         seasonality=True)  
            utils.var_alloc_val(reg_data_globe[na], yr, 'var_seasonality',v_id, var_mo_season)
            utils.var_alloc_val(reg_data_globe[na], yr, 'var_season_std',v_id, var_season_std)



with open('reg_data.pkl', 'wb') as handle:
    pickle.dump(reg_data_globe, handle, protocol=pickle.HIGHEST_PROTOCOL)



