import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import math
import matplotlib as mpl
from matplotlib import ticker as mticker

def fill_between_shade(ax,t_ax,data,fill_val,c):
    fill_min = [x-std for x, std in zip(data, fill_val)]
    fill_max = [x+std for x, std in zip(data, fill_val)]

    ax.fill_between(t_ax, fill_min, fill_max,
                    alpha=0.2, color = c)

def plot_monthly_series_pannel(axes, C_omf, std_omf, title, limits, var_id, pos, lower_axis=False):
    t_ax = np.arange(0,12)
    ax2 = axes
    ax3 = ax2.twinx()
    if var_id == 'OMF':
        subindex = '$_{aer}$'
        ylab = f'OMF (PCHO{subindex}, DCAA{subindex}) '
        ax3_label = f"OMF PL{subindex}"

        #     ax2.set_yscale('log')

    elif var_id == 'Biom':
        subindex = '$_{sw}$'
        ylab = f'Concentration \n (PCHO{subindex}, DCAA{subindex}) \n($mmol\ C\ m^{-3}$)'
        ax3_label = f"Concentration PL{subindex}\n($mmol\ C\ m^{-3}$)"


    p2, = ax2.plot(t_ax, C_omf[0], label=f'PCHO{subindex}', linewidth=2, color='b')
    fill_between_shade(ax2, t_ax, C_omf[0], std_omf[0], 'b')

    p21, = ax2.plot(t_ax, C_omf[1], label=f'DCAA{subindex}', linewidth=2, color='g')
    fill_between_shade(ax2, t_ax, C_omf[1], std_omf[1], 'g')

    p22, = ax3.plot(t_ax, C_omf[2], label=f'PL{subindex}', linewidth=2, color='darkred')
    fill_between_shade(ax3, t_ax, C_omf[2], std_omf[2], 'darkred')

    ax3.set_ylabel(ax3_label, color='darkred', fontsize=16)
    ax3.yaxis.set_tick_params(labelsize=16)
    # ax3.legend(loc='upper right', fontsize=14)
    ax3.spines['right'].set_color('darkred')
    ax3.tick_params(axis='y', colors='darkred')

    ax2.set_ylabel(ylab, fontsize=16)
    ax2.yaxis.set_tick_params(labelsize=16)
    ax2.set_title(title,
                  fontweight='bold',
                  fontsize=16)

    if title=='PUR':
        ax3.set_ylim(0, limits[1])
        ax2.set_ylim(0, limits[0])

    if lower_axis:
        ax2.set_xlabel("Months", fontsize=16)
    # ax2.legend(loc='upper left', fontsize=14)

    def format_func(value, tick_number):
        N = int(value + 1)
        return N
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(format_func))
    ax2.xaxis.set_tick_params(labelsize=16)
    return p2, p21, p22

def get_vals_std(data, region, var_id):
    da_var = data[region]['months_30_yr']['var_seasonality'][var_id]
    da_std = data[region]['months_30_yr']['var_season_std'][var_id]

    C_vals = [da_var['PCHO'],
             da_var['DCAA'],
             da_var['PL']]
    C_vals_std = [da_std['PCHO'],
                 da_std['DCAA'],
                 da_std['PL']]
    return C_vals, C_vals_std

def plot_seasonality_regions(data):
    fig, axs = plt.subplots(6, 2, figsize=(16, 26))  # 15,8
    ax = axs.flatten()
    ax1 = [ax[0], ax[2], ax[4], ax[6], ax[8], ax[10]]
    ax2 = [ax[1], ax[3], ax[5], ax[7], ax[9], ax[11]]
    fig.subplots_adjust(right=0.75)

    for i, region in enumerate(list(data.keys())):
        if region == 'WAP':
            print(data[region]['months_30_yr']['var_seasonality']['OMF'])
        C_omf, C_omf_std = get_vals_std(data, region, 'OMF')
        C_biom, C_biom_std = get_vals_std(data, region, 'Biom')


        limits_omf = [[0.02, 0.5], [0.02, 0.3], [0.03, 0.3], [0.02, 0.3],[0.016, 0.2],[0.02, 0.4]]
        limits_biom = [[9, 1], [8, 1], [8, 1], [6, 1],[5, 0.2],[8, 1]]


        if i == 5: laxis = True
        else: laxis = False
        p2omf, p21omf, p22omf = plot_monthly_series_pannel(ax2[i], C_omf, C_omf_std,
                                         region, limits_omf[i], 'OMF', 0.27, lower_axis=laxis)
        p2oc, p21oc, p22oc = plot_monthly_series_pannel(ax1[i], C_biom, C_biom_std,
                                         region, limits_biom[i], 'Biom', 0.27, lower_axis=laxis)

        if i == 0:    fig.legend(handles=[p2omf, p21omf, p22omf], ncol=3,
               bbox_to_anchor=(0.9, 1.02), fontsize=14)
        if i == 0:    fig.legend(handles=[p2oc, p21oc, p22oc], ncol=3,
               bbox_to_anchor=(0.1, 1.0), loc='lower left', fontsize=14)

    fig.tight_layout()
    plt.savefig(f'Multiannual monthly subregions_updated.png',
                dpi=300,
                bbox_inches="tight")
