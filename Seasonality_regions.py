#!/usr/bin/env python
# coding: utf-8


# ##### Import packges
import global_vars
import os
import pickle
import utils

#read data
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

conditions, reg_data_globe, file_name = utils.regions_dict()

var_ocean = [C_conc_tot,
            C_pl,
            C_pcho,
            C_dcaa,
            C_pcho+C_dcaa]
var_omf = [C_omf_tot,
           C_omf['OMF_POL'],
           C_omf['OMF_PRO'],
           C_omf['OMF_LIP'],
           ]
list_vars = [var_ocean,
            var_omf]

# If arctic_regions apply sea ice mask
if global_vars.arctic_regions:
    data_dir_ocean = global_vars.path_ocean
    C_temp = utils.read_files_data(data_dir_ocean + "temperature/sst*.nc")['sst'] * C_ice_msk
    C_phyN = utils.read_files_data(data_dir_ocean + "PhyN*")['VAR'] * C_ice_msk
    C_diaN = utils.read_files_data(data_dir_ocean + "DiaN*")['VAR'] * C_ice_msk
    C_phyC = utils.read_files_data(data_dir_ocean + "PhyC*")['VAR'] * C_ice_msk
    C_diaC = utils.read_files_data(data_dir_ocean + "DiaC*")['VAR'] * C_ice_msk

    C_ice = C_ice * 100

    var_other = [C_phyC,
                 C_diaC,
                 C_phyC + C_diaC,
                 C_ice,
                 C_temp]
    list_vars.append(var_other)

# Create dictionaries grouping variables into different groups (e.g. Biom for biomolecules, OMF for organic mass
# fraction and Others for ocean parameters and phytoplankton groups)
for na in reg_data_globe.keys():
    reg_data_globe[na]={'months_30_yr':[]}
    for i,mo in enumerate(reg_data_globe[na].keys()):
        reg_data_globe[na][mo]= {
                              'var_seasonality':{},
                              'var_season_std':{}
                              }
        if global_vars.arctic_regions:
            reg_data_globe[na][mo]['var_data_region'] = {}
        for v,va in enumerate(reg_data_globe[na][mo].keys()):
            reg_data_globe[na][mo][va]['Biom']= {'Total concentration':[],
                                            'PL':[],
                                            'PCHO':[],
                                            'DCAA':[],
                                            'PCHO_DCAA': [],
                                                 }
            reg_data_globe[na][mo][va]['OMF']= {
                                           'Total OMF':[],
                                           'PCHO':[],
                                           'DCAA':[],
                                           'PL':[],}

            if global_vars.arctic_regions:
                reg_data_globe[na][mo][va]['Other'] = {
                                                    'Phy': [],
                                                    'Dia': [],
                                                    'PhyDia': [],
                                                    'SIC': [],
                                                    'SST': []}


years_set = [1989,2020]

data = []
for i_id, var in enumerate(list_vars):
    if i_id == 0:
        v_id = 'Biom'
    elif i_id == 1:
        v_id = 'OMF'
    elif i_id == 2:
        v_id = 'Other'

    print(i_id, v_id)
    region = []
    season = []
    var_value = []
    var_std = []
    var_na = []


    for i,na in enumerate(reg_data_globe.keys()):   
        print(na)
        for y,yr in enumerate(list(reg_data_globe[na].keys())):
            # select data per regions and return multiannual monthly means and std
            var_mo_season, var_season_std, var_data_reg = utils.find_region(var,
                                                         conditions[i],
                                                         na,
                                                         years_set)
            # save data into a dictionary
            utils.var_alloc_val(reg_data_globe[na], yr, 'var_seasonality',v_id, var_mo_season)
            utils.var_alloc_val(reg_data_globe[na], yr, 'var_season_std',v_id, var_season_std)

            if global_vars.arctic_regions:
                utils.var_alloc_val(reg_data_globe[na], yr, 'var_data_region', v_id, var_data_reg)

try:
    os.makedirs(global_vars.pkl)
except OSError:
    pass
with open(f'{global_vars.pkl}/{file_name}.pkl', 'wb') as handle:
    pickle.dump(reg_data_globe, handle, protocol=pickle.HIGHEST_PROTOCOL)



