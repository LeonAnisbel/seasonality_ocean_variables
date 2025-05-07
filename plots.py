import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.patches as mpatches

import global_vars
import utils


def plot_map_box_station(axs, conditions, reg_data_globe, create_fig=False):
    """ This function creates a map with color-coded boxes defined by "conditions" with names "reg_data_globe"
    Regions are defined considering the locations where seawater samples were collected """
    if create_fig:
        fig = plt.figure(figsize=(6, 4))
        projection = ccrs.Robinson(central_longitude=30)
        ax = plt.axes(projection=projection)
        gl = ax.gridlines(draw_labels=True,
                          x_inline=False,
                          y_inline=False)  # adding grid lines with labels
        gl.top_labels = False
        gl.right_labels = False
    else: ax = axs

    ax.coastlines(resolution='110m', color='k')
    ax.set_extent([-100, 30, -90, 90], crs=ccrs.PlateCarree())
    color= global_vars.color_regions
    for i, c, n in zip(conditions, color, list(reg_data_globe.keys())):
        low_lim_lat = i[0][1]
        low_lim_lon = i[1][1]
        upper_lim_lat = i[0][2]
        upper_lim_lon = i[1][2]
        pl = ax.add_patch(mpatches.Rectangle(xy=[low_lim_lon, low_lim_lat],
                                             width=upper_lim_lon - low_lim_lon,
                                             height=upper_lim_lat - low_lim_lat,
                                             facecolor=c, edgecolor=c,
                                             label=n,
                                             transform=ccrs.PlateCarree()))

    plt.legend()
    if create_fig:
        plt.tight_layout()
        plt.savefig('Map_boxes.png', dpi=300)
        plt.close()

def fill_between_shade(ax,t_ax,data,data_std,c):
    """ This function plots around the data values ("data") the standard deviation
    ("data_std") as shaded area """
    fill_min = [x-std for x, std in zip(data, data_std)]
    fill_max = [x+std for x, std in zip(data, data_std)]

    ax.fill_between(t_ax, fill_min, fill_max,
                    alpha=0.2, color = c)

def plot_each_station(ax2, ax3, data):
    """ This function plots the observational data for each station and biomolecule on each subfigure
     containing the predefined boxes around the station locations (as represented in function
     "plot_map_box_station") """
    for sta in data['names']:
        for v_id, v in enumerate(sta['monthly_mean'].columns):
            new_months = [m - 1 for m in sta['months']]
            if sta['colors'][v_id]=='darkred': ax = ax3
            else: ax = ax2
            ax.errorbar(new_months,
                       sta['monthly_mean'][v].values,
                       yerr=sta['monthly_mean_std'][v].values,
                       c=sta['colors'][v_id],
                       fmt='o')

def plot_monthly_series_pannel(axes, C_omf, std_omf, title, limits, var_id, pos, c, data_stations, font, lower_axis=False, stations=False):
    """ This function plots the seasonality of the ocean biomolecule concentration or OMF for predefined regions """
    t_ax = np.arange(0,12)
    ax2 = axes
    ax3 = ax2.twinx()
    if var_id == 'OMF':
        subindex = '$_{aer}$'
        ylab = f'PCHO{subindex}, DCAA{subindex}'
        ax3_label = f"PL{subindex}"

    elif var_id == 'Biom':
        subindex = '$_{sw}$'
        if stations:
            ylab = f'PCHO{subindex}, DCAA{subindex}'
            ax3_label = f'PL{subindex}'
        else:
            ylab = f'PCHO{subindex}, DCAA{subindex}'
            ax3_label = f'PL{subindex}'

    p2, = ax2.plot(t_ax, C_omf[0], label=f'PCHO{subindex}', linewidth=2, color='b')
    fill_between_shade(ax2, t_ax, C_omf[0], std_omf[0], 'b')

    p21, = ax2.plot(t_ax, C_omf[1], label=f'DCAA{subindex}', linewidth=2, color='g')
    fill_between_shade(ax2, t_ax, C_omf[1], std_omf[1], 'g')

    p22, = ax3.plot(t_ax, C_omf[2], label=f'PL{subindex}', linewidth=2, color='darkred')
    fill_between_shade(ax3, t_ax, C_omf[2], std_omf[2], 'darkred')

    ax3.set_ylabel(ax3_label, color='darkred', fontsize=font)
    ax3.yaxis.set_tick_params(labelsize=font)
    # ax3.legend(loc='upper right', fontsize=14)
    ax3.spines['right'].set_color('darkred')
    ax3.tick_params(axis='y', colors='darkred')

    ax2.set_ylabel(ylab, fontsize=font)
    ax2.yaxis.set_tick_params(labelsize=font)
    ax2.set_title(title,
                  fontweight='bold',
                  color=c,
                  fontsize=font)

    ax3.set_ylim(0, limits[1])
    ax2.set_ylim(0, limits[0])

    if lower_axis:
        ax2.set_xlabel("Months", fontsize=font)
    # ax2.legend(loc='upper left', fontsize=14)

    def format_func(value, tick_number):
        N = int(value + 1)
        return N
    ax2.xaxis.set_major_formatter(plt.FuncFormatter(format_func))
    ax2.xaxis.set_tick_params(labelsize=font)


    if stations:
        plot_each_station(ax2, ax3, data_stations)
    return p2, p21, p22

def get_vals_std(data, region, var_id):
    """ Returns lists of data values and standard deviation stored in the "data" dictionary """

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
    """ This function creates the figure, define axes and other parameters relevant for plotting the
      seasonality of marine biomolecules and OMF for global oceanic regions"""

    fig, axs = plt.subplots(5, 2, figsize=(18, 24))  # 15,8
    ax = axs.flatten()
    ax1 = [ax[0], ax[2], ax[4], ax[6], ax[8]]
    ax2 = [ax[1], ax[3], ax[5], ax[7], ax[9]]
    fig.subplots_adjust(wspace=0.5)
    fig.subplots_adjust(hspace=0.3)

    c = len(ax1)*['k']
    f = 20
    for i, region in enumerate(list(data.keys())):
        C_omf, C_omf_std = get_vals_std(data, region, 'OMF')
        C_biom, C_biom_std = get_vals_std(data, region, 'Biom')


        limits_omf = [[0.03, 0.5], [0.03, 0.5], [0.03, 0.5], [0.03, 0.5],[0.03, 0.5],[0.03, 0.5]]
        limits_biom = [[8, 1.5], [8, 1.5], [8, 1.5], [8, 1.5],[8, 1.5],[8, 1.5]]


        if i == 4: laxis = True
        else: laxis = False
        if region == 'Arctic Ocean':
            title = 'OMF \n \n \n \n\n' + region
        else: title = region

        p2omf, p21omf, p22omf = plot_monthly_series_pannel(ax2[i], C_omf, C_omf_std,
                                         title, limits_omf[i], 'OMF', 0.27, c[i], [], f, lower_axis=laxis)

        if region == 'Arctic Ocean':
            title = 'Ocean biomolecule concentration \n (mmol C m$^{-3}$) \n \n \n \n' + region
        else: title = region
        p2oc, p21oc, p22oc = plot_monthly_series_pannel(ax1[i], C_biom, C_biom_std,
                                         title, limits_biom[i], 'Biom', 0.27, c[i], [],f, lower_axis=laxis)

        if i == 0:    fig.legend(handles=[p2oc, p21oc, p22oc], ncol=3,
               bbox_to_anchor=(0.1, 0.9), loc='lower left', fontsize=f)
        if i == 0:    fig.legend(handles=[p2omf, p21omf, p22omf], ncol=3,
               bbox_to_anchor=(0.92, 0.93), fontsize=f)


    # fig.tight_layout()
    plt.savefig(f'Multiannual monthly subregions_updated_global.png',
                dpi=300,
                bbox_inches="tight")


def plot_seasonality_regions_with_stations(data):
    """ This function creates the figure, define axes and other parameters relevant for plotting the
      seasonality of marine biomolecules and observational data for regions defined around the station
      locations """
    fig, axs = plt.subplots(2, 3,
                            figsize=(18, 8),
                            constrained_layout=True)  # 15,8
    plt.title('Ocean biomolecule concentration (mmol C m$^{-3}$) \n \n \n \n')

    ax = axs.flatten()
    c = global_vars.color_regions
    dict_stat_groups= utils.read_ocean_data_monthly(ax)

    order_keys = ['NAO', 'WAP', 'SATL, CVAO', 'PUR', 'NWAO, SB', 'AS, WMED'] #'AI'
    print(data.keys())
    f = 18

    for i, region in enumerate(order_keys):
        C_biom, C_biom_std = get_vals_std(data, region, 'Biom')
        # limits_biom = [[7, 1.5], [8, 1.], [6, 0.4], [9, 0.3],[9, 0.5],[6.5, 1.]]
        limits_biom = [[7, 1.5],[6.5, 1.], [9, 0.3],[9, 0.7], [8, 1.], [6, 0.4]]

        print(dict_stat_groups)
        if i == 4 or i == 3 or i == 5: laxis = True
        else: laxis = False
        title = region
        # if region == 'AI': region = 'AS, WMED'
        p2oc, p21oc, p22oc = plot_monthly_series_pannel(ax[i],
                                                        C_biom,
                                                        C_biom_std,
                                                        title,
                                                        limits_biom[i],
                                                        'Biom',
                                                        0.27,
                                                        c[i],
                                                        dict_stat_groups[region],
                                                        f,
                                                        lower_axis=laxis,
                                                        stations=True)

        if i == 0:    fig.legend(handles=[p2oc, p21oc, p22oc],
                                 ncol=3,
                                 bbox_to_anchor=(0.35, 1.0),
                                 loc='lower left',
                                 fontsize=f)


    proj = ccrs.PlateCarree()
    ax1 = fig.add_axes([0.9, 0.3, 0.4, 0.45],
                       projection=proj)
    conditions, reg_data_globe, _ = utils.regions_dict()
    plot_map_box_station(ax1,
                         conditions,
                         reg_data_globe,
                         create_fig=False)
    plt.savefig(f'Multiannual monthly subregions_updated_global_stations.png',
                dpi=300,
                bbox_inches="tight")
    plt.close()


