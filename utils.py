import xarray as xr

def get_var_reg(v, cond):
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
    v_mo_var = []
    v_std_var = []

    for v in variable:
        v = get_var_reg(v, cond)
        v = v.where((v.time.dt.year > yr_cond[0]) &
                    (v.time.dt.year < yr_cond[1]), drop=True)

        da_m_std_list = []
        da_mean_yrs_list = []

        # monthly multiannual mean
        for m in months:
            da_t = v.where(v.time.dt.month == m, drop=True)
            da_t['time'] = da_t['time'].dt.year

            da_m_std = da_t.std(dim=('lat', 'lon', 'time'),
                                skipna=True).values
            da_mean_yrs = da_t.mean(dim=('time', 'lat', 'lon'),
                                    skipna=True).values

            da_mean_yrs_list.append(float(da_mean_yrs))
            da_m_std_list.append(float(da_m_std))

        v_mo_var.append(da_mean_yrs_list)
        v_std_var.append(da_m_std_list)


        #print('mean value', da_mean_yrs, '+-', da_m_std)

    return v_mo_var, v_std_var


def var_alloc_val(data, mo_yr_id, var_type, v_id, var_mo_season):
    for v, va in enumerate(data[mo_yr_id][var_type][v_id].keys()):
        # print(data, mo_yr_id, var_type, va, v_id)
        data[mo_yr_id][var_type][v_id][va] = var_mo_season[v]



def read_files_data(path_dir):
    data = xr.open_mfdataset(path_dir,
                             concat_dim='time',
                             combine='nested')
    return data