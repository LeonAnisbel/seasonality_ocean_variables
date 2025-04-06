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
import global_vars
import os
import pickle
import plots
import utils


try:
    os.mkdir('plots')
except OSError:
    pass

C_ice =  utils.read_files_data(global_vars.data_dir + 'ice_var*')['sic']
C_ice_msk = utils.read_files_data(global_vars.data_dir + 'mask_ice*')['sic']
C_pl = utils.read_files_data(global_vars.data_dir + 'PL_var_*')['PL'] * C_ice_msk
C_pcho = utils.read_files_data(global_vars.data_dir + 'PCHO_var_*')['PCHO'] * C_ice_msk
C_dcaa = utils.read_files_data(global_vars.data_dir + 'DCAA_var_*')['DCAA'] * C_ice_msk
C_conc_tot = C_pl+C_pcho+C_dcaa

C_omf = utils.read_files_data(global_vars.path_omf + "oceanfilms_omf_*")
C_omf_pol = C_omf['OMF_POL']
C_omf_pro = C_omf['OMF_PRO']
C_omf_lip = C_omf['OMF_LIP']
C_omf_tot = C_omf_pol + C_omf_pro + C_omf_lip

months = [np.arange(1,13)]
conditions, reg_data_globe, file_name = utils.regions_dict()

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

            var_mo_season, var_season_std = utils.find_region(var,
                                                         conditions[i],
                                                         mon,
                                                         na,
                                                         years_set[y],
                                                         seasonality=True)
            utils.var_alloc_val(reg_data_globe[na], yr, 'var_seasonality',v_id, var_mo_season)
            utils.var_alloc_val(reg_data_globe[na], yr, 'var_season_std',v_id, var_season_std)



with open(file_name+'.pkl', 'wb') as handle:
    pickle.dump(reg_data_globe, handle, protocol=pickle.HIGHEST_PROTOCOL)



