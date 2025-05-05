import xarray as xr
import pandas as pd
import global_vars
import plots
import codecs

def get_var_reg(v, cond):
    """ This function is used to select a region in variable data "v" under withing the latitude and
    longitude limits define in "cond" """
    if len(cond) <= 1:
        v = v.where((cond[0][0] > cond[0][1]) &
                    (cond[0][0] < cond[0][2])
                    , drop=True)
    elif len(cond) > 1:
        v = v.where(((cond[0][0] > cond[0][1]) &
                     (cond[0][0] < cond[0][2]) &
                     (cond[1][0] > cond[1][1]) &
                     (cond[1][0] < cond[1][2]))
                    , drop=True)
    return v


def find_region(variable, cond, months, na, yr_cond, seasonality=False):
    """ This function calculates the multiannual monthly mean values of "months"
    over the period "yr_cond" defining the years to consider in the average for the regions
    definition of latitude and longitude limits in "cond" """
    v_mo_var = []
    v_std_var = []

    for v in variable:
        v = get_var_reg(v, cond)
        v = v.where((v.time.dt.year > yr_cond[0]) &
                    (v.time.dt.year < yr_cond[1]), drop=True)

        v_m = v.groupby(v.time.dt.month).mean('time')
        v_m_lalo = v_m.mean(['lat', 'lon'], skipna=True).values
        v_m_lalo_std = v_m.std(['lat', 'lon'], skipna=True).values

        print(na, 'mean value', v_m_lalo, '+-', v_m_lalo_std, '\n \n')

        v_mo_var.append(v_m_lalo)
        v_std_var.append(v_m_lalo_std)

    return v_mo_var, v_std_var


def var_alloc_val(data, mo_yr_id, var_type, v_id, var_mo_season):
    """ Allocates variable into the dictionary """
    for v, va in enumerate(data[mo_yr_id][var_type][v_id].keys()):
        data[mo_yr_id][var_type][v_id][va] = var_mo_season[v]



def read_files_data(path_dir):
    """ Read model data netcdf files """
    data = xr.open_mfdataset(path_dir,
                             concat_dim='time',
                             combine='nested')
    return data

def regions_dict():
    """ This function creates the dictionaries with the region limits  """
    c = read_files_data(global_vars.path_omf + "oceanfilms_omf_*")

    lat = c.lat
    lon = c.lon

    if global_vars.seasonality_stations:
        conditions = [[[lat, 63, 82], [lon, 1, 10]],
                      [[lat, -70, -58], [lon, -70, -58]],
                      [[lat, 12, 25], [lon, -32, -18]],
                      [[lat, -17, -5], [lon, -85, -77]],
                      [[lat, 37, 42], [lon, -75, -65]],
                      [[lat, 36, 45], [lon, 1, 14]],
                      # [[lat, -37, -36], [lon, 77, 78]],

                      ]

        reg_data_globe = {'NAO': [],
                          'WAP': [],
                          'SATL, CVAO': [],
                          'PUR': [],
                          'NWAO, SB': [],
                          'AS, WMED': [],
                          # 'AI':[]
                          }

        plots.plot_map_box_station(0, conditions, reg_data_globe, create_fig=True)
        file_name = 'reg_data_stat_bx_test'

    else:
        conditions = [[[lat, 63, 90]],
                      [[lat, -90, -63]],
                      [[lat, 23, 63]],
                      [[lat, -63, -23]],
                      [[lat, -23, 23]], ]

        reg_data_globe = {'Arctic Ocean': [],
                          'Southern Ocean': [],
                          'Northern Subtropics': [],
                          'Southern Subtropics': [],
                          'Equator': [],
                          }
        file_name = 'reg_data_global_regions'
    return conditions, reg_data_globe, file_name


def get_monthly_group_mean(data, var_name):
    """ This function calculates the monthly mean values and standard deviation (used for observational data)  """
    times = pd.to_datetime(data['Date/Time'], dayfirst=False)
    data_month = data.groupby([times.dt.year, times.dt.month], dropna=True)[var_name].mean()
    data_month_std = data.groupby([times.dt.year, times.dt.month], dropna=True)[var_name].std()
    months = [i[1] for i in data_month.index]
    return data_month, data_month_std, months

def read_ocean_data_monthly(axs):
    """ This function reads the seawater samples data, computes the monthly averages,
     allocate them into a dictionary grouped by the box regions defined in global_vars.seasonality_stations  """
    file_water = "../../../SEAWATER_data.csv"
    doc = codecs.open(file_water, 'r', 'UTF-8')  # open for reading with "universal" type set 'rU'
    data_water = pd.read_csv(doc, sep=',')
    data_water.loc[:, ('Date/Time')] = data_water['Date/Time'].apply(pd.to_datetime, dayfirst=False)

    dict_stat = {'WAP':{'name':'WAP'},
                 'PASCAL':{'name':'NAO'},
                 'CVAO':{'name':'CVAO'},
                 'PUR12':{'name':'PUR12'},
                 'PUR17':{'name':'PUR17'},
                 'SB':{'name':'SB'},
                 'NAO':{'name':'NWAO'},
                 'SATL':{'name':'SATL'},
                 'WMED':{'name':'WMED'},
                 'AS08':{'name':'AS'},}

    var_names = [['DCCHO [µMC]'],
                 ['DCCHO [µMC]'],
                 ['DCCHO [µMC]', 'DCAA [µMC]', 'PG'],
                 ['DCCHO [µMC]', 'DCAA [µMC]'],
                 ['DCCHO [µMC]'],
                 ['DCAA [µMC]'],
                 ['DCAA [µMC]'],
                 ['DCAA [µMC]'],
                 ['DCAA [µMC]'],
                 ['PG'],]

    for i, d in enumerate(dict_stat):
        dict_stat[d]['dataframe'] = data_water[data_water['Event'] == d]
        dict_stat[d]['var_names'] = var_names[i]
        val_m, val_m_std, m = get_monthly_group_mean(dict_stat[d]['dataframe'], var_names[i])
        dict_stat[d]['monthly_mean'] = val_m
        dict_stat[d]['monthly_mean_std'] = val_m_std
        dict_stat[d]['months'] = m
        c_list = []
        for c in (var_names[i]):
            if c == 'DCCHO [µMC]':
                c_list.append('blue')
            if c == 'DCAA [µMC]':
                c_list.append('green')
            if c == 'PG':
                c_list.append('darkred')
        dict_stat[d]['colors'] = c_list

    dict_stat_groups = {'WAP': {'names': [dict_stat['WAP']]},
                     'NAO': {'names': [dict_stat['PASCAL']]},
                     'SATL, CVAO': {'names': [dict_stat['SATL'], dict_stat['CVAO']]},
                     'PUR': {'names': [dict_stat['PUR12'], dict_stat['PUR17']]},
                     'NWAO, SB': {'names': [dict_stat['NAO'], dict_stat['SB']]},
                     'AS, WMED': {'names': [dict_stat['AS08'], dict_stat['WMED']]}, }

    return dict_stat_groups









