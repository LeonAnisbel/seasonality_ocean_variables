import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib as mpl
import matplotlib.path as mpath
from matplotlib import ticker as mticker
from cartopy.mpl.gridliner import LATITUDE_FORMATTER
from utils_plots import *
import global_vars
from utils import rm_nan
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


def fill_between_shade(ax, t_ax, data, fill_val, c):
    ax.fill_between(t_ax, data - fill_val, data + fill_val,
                    alpha=0.2, color=c)

f = 14
t_ax = global_vars.months
def plot_monthly_series_pannel(axes, C_conc, C_omf, std_conc, std_omf, title, limits, pos, left_axis=False):
    ax = axes[0]
    ax2 = axes[1]
    ax3 = ax2.twinx()
    #     ax2.set_yscale('log')
    factor_pcho = 10
    p2, = ax2.plot(t_ax, C_omf[0]*factor_pcho, label='PCHO$_{aer}$', linewidth=2, color='b')
    fill_between_shade(ax2, t_ax, C_omf[0]*factor_pcho, std_omf[0]*factor_pcho, 'b')
    p3, = ax.plot(t_ax, C_conc[0], label='PCHO$_{sw}$', linewidth=2, color='b')
    fill_between_shade(ax, t_ax, C_conc[0], std_conc[0], 'b')

    p21, = ax2.plot(t_ax, C_omf[1]*factor_pcho, label='DCAA$_{aer}$', linewidth=2, color='g')
    fill_between_shade(ax2, t_ax, C_omf[1]*factor_pcho, std_omf[1]*factor_pcho, 'g')
    p31, = ax.plot(t_ax, C_conc[1], label='DCAA$_{sw}$', linewidth=2, color='g')
    fill_between_shade(ax, t_ax, C_conc[1], std_conc[1], 'g')

    factor_pl = 1
    p22, = ax3.plot(t_ax, C_omf[2]*factor_pl, label='PL$_{aer}$', linewidth=2, color='darkred')
    fill_between_shade(ax3, t_ax, C_omf[2]*factor_pl, std_omf[2]*factor_pl, 'darkred')
    p32, = ax.plot(t_ax, C_conc[2], label='PL$_{sw}$', linewidth=2, color='darkred')
    fill_between_shade(ax, t_ax, C_conc[2], std_conc[2], 'darkred')

    ax.set_ylabel(f"Carbon concentration \n ({global_vars.units_concentration})", fontsize=f)
    ax.set_ylim(limits[0])
    ax.yaxis.set_tick_params(labelsize=f)

    ax2.set_ylabel("OMF (10$^{-1}$) \n PCHO $_{aer}$,  DCAA$_{aer}$  ", fontsize=f)
    ax2.set_ylim(0, 0.02*factor_pcho)
    ax3.set_ylabel("OMF PL$_{aer}$", color='darkred', fontsize=f)
    ax3.set_ylim(0, 0.5*factor_pl)

    ax.set_ylim(limits[0])
    ax2.yaxis.set_tick_params(labelsize=f)
    ax3.yaxis.set_tick_params(labelsize=f)

    #     ax2.yaxis.set_minor_locator(mticker.LogLocator(numticks=999, subs="auto"))

    #     fig.legend(handles=[p2,p21, p22],ncol = len(ax.lines),
    #                bbox_to_anchor=(0.1, 0.1),loc='lower left',fontsize = 16)
    ax.legend(loc='upper right', fontsize=f-2)
    ax2.legend(loc='upper left', fontsize=f-2)
    ax3.legend(loc='upper right', fontsize=f-2)
    ax3.spines['right'].set_color('darkred')
    ax3.tick_params(axis='y', colors='darkred')


def plot_seasons_reg(ax, C_conc, C_omf, na, c, lw, ylabels, ylims, reg_gray_line=False):
    if na != 'Arctic':
        line_sty = '--'
    else:
        line_sty = '-'
    ax, ax2 = ax[0], ax[1]

    #   Plot gray lines only
    if reg_gray_line:
        p2 = ax.plot(t_ax, C_conc, color=c, label='Arctic', linewidth=lw)
        p3 = ax2.plot(t_ax, C_omf, color=c, label='Arctic', linewidth=lw)

    else:
        p2, = ax.plot(t_ax, C_conc,
                      linewidth=lw, label=na, color=c, linestyle=line_sty)  # linestyle = li_style,
        #     p1 = ax.plot(t_ax, C_conc[1],color = c,linestyle = 'dashed',label = 'PL',linewidth = lw)
        p3, = ax2.plot(t_ax, C_omf,
                       linewidth=lw, label=na, color=c, linestyle=line_sty)  # linestyle = li_style,

    ax.set_ylabel("PL$_{sw}$" + f" Carbon concentration \n ({global_vars.units_concentration})", fontsize=f)
    ax.set_ylim(0, 1.5)
    ax.yaxis.set_tick_params(labelsize=f)

    ax2.set_ylabel("Total OMF", fontsize=f)
    ax2.set_ylim(0, 0.5)
    ax2.yaxis.set_tick_params(labelsize=f)

    ax.xaxis.set_tick_params(labelsize=f)

    ax2.set_xlabel("Months", fontsize=f)
    ax.set_xlabel("Months", fontsize=f)

    if na == 'Arctic' and reg_gray_line:
        print('here')
        ax.legend(loc='upper left', fontsize=f-2)
        ax2.legend(loc='upper left', fontsize=f-2)
    if reg_gray_line:
        pass
    else:
        return p2, p3


def plot_seasons_reg_conc_ice(ax, var, na, c, title, vm, lstyle, lower_axis=False):
    p1, = ax.plot(t_ax, var,
                  linewidth=1.5, label=na, color=c, linestyle=lstyle)  # + ' ['+diff+']', )#linestyle = li_style,
    ax.set_title('\n '+ title[0][0],
                 loc='right',
                 fontsize=f,
                 weight='bold')
    ax.set_title('\n '+ title[0][1],
                 loc='left',
                 fontsize=f,
                 weight='bold')
    ax.set_ylabel(title[1], fontsize=f)
    ax.set_ylim(vm[0], vm[1])
    ax.yaxis.set_tick_params(labelsize=f)

    ax.xaxis.set_major_formatter(plt.FuncFormatter(format_func))
    ax.grid(linestyle='--', linewidth=0.4)

    ax.xaxis.set_tick_params(labelsize=f)
    if lower_axis:
        ax.set_xlabel("Months", fontsize=f)

    return p1


def plot_seasons_reg_only(ax, C_conc, na, c, title):

    p1, = ax.plot(t_ax, C_conc[0],
                  linewidth=2, label=na, color=c, linestyle='dashed')  # linestyle = li_style,
    p2, = ax.plot(t_ax, C_conc[1], label=na, color=c, linestyle='solid')

    ax.set_ylabel(f"Carbon concentration \n ({global_vars.units_concentration})", fontsize=f)
    # ax.set_yscale('log')
    # ax.set_ylim(0, 7)
    ax.yaxis.set_tick_params(labelsize=f)

    ax.set_title('\n '+ title[0],
                 loc='right',
                 fontsize=f,
                 weight='bold')
    ax.set_title('\n '+ title[1],
                 loc='left',
                 fontsize=f,
                 weight='bold')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(format_func))
    ax.grid(linestyle='--', linewidth=0.4)

    #     ax.set_title(titles[i], fontsize = 16)
    #     ax.set_title(titles_1[i], loc='right', fontsize = 16)
    ax.xaxis.set_tick_params(labelsize=f)
    ax.legend([p1, p2], ['PCHO', 'PL'], loc='upper right', fontsize=f)

    return p2

def seasonality_conc_omf_arctic_and_reg(reg_data):
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))  # 15,8
    ax = axs.flatten()

    fig.subplots_adjust(right=0.75)
    limits = [[0, 7.5], [1e-6, 1e0], [0.1, 0.23]]

    yr = 'months_30_yr'
    na = 'Arctic'
    data = reg_data[na][yr]['var_seasonality']['Biom']
    C_conc = [data['PCHO'],
              data['DCAA'],
              data['PL']]
    data = reg_data[na][yr]['var_seasonality']['OMF']
    C_omf = [data['PCHO'],
             data['DCAA'],
             data['PL']]

    data = reg_data[na][yr]['var_season_std']['Biom']
    C_conc_std = [data['PCHO'],
                  data['DCAA'],
                  data['PL']]
    data_omf_std = reg_data[na][yr]['var_season_std']['OMF']
    C_omf_std = [data_omf_std['PCHO'],
                 data_omf_std['DCAA'],
                 data_omf_std['PL']]

    plot_monthly_series_pannel([ax[0], ax[1]], C_conc, C_omf, C_conc_std, C_omf_std, \
                               r'$\bf{Arctic}$', limits, 0.27, left_axis=True)
#
    titles_1 = [r'$\bf{(a)}$', r'$\bf{(b)}$', r'$\bf{(c)}$', r'$\bf{(d)}$']

    axs = [ax[2], ax[3]]
    list_conc_x_month = [[] for i in range(12)]
    list_omf_x_month = [[] for i in range(12)]

    color_reg = global_vars.colors_arctic_reg
    leg_list = []
    for idx, na in enumerate(reg_data.keys()):
        print(na)
        data = reg_data[na][yr]['var_seasonality']
        C_conc = data['Biom']['PL']
        C_omf = data['OMF']['Total OMF']

        C_conc = rm_nan(C_conc)
        C_omf = rm_nan(C_omf)

        if na == 'Arctic':
            C_conc_ar, C_omf_ar = C_conc, C_omf
            lw = 2
        else:
            lw = 1.5

        ylabels = [f"PL Concentration \n ({global_vars.units_concentration})",
                   "Total OMF"]
        lims = [2, 1.]
        p2, p3 = plot_seasons_reg(axs, C_conc, C_omf,
                                  na, color_reg[idx], lw,
                                  ylabels, lims)
        leg_list.append(p2)

        for i, val in enumerate(C_omf):
            list_conc_x_month[i].append(C_conc[i])
            list_omf_x_month[i].append(val)
        # uncomment to create plot with gray lines for the regions intead of coloured
        # if na != 'Antarctica' and na != 'Arctic':
        #     plot_seasons_reg(axs, C_conc, C_omf, \
        #                      na, 'gray', 0.7)
        #     for i, val in enumerate(C_omf):
        #         list_conc_x_month[i].append(C_conc[i])
        #         list_omf_x_month[i].append(val)
        #
        # if na == 'Arctic':
        #     plot_seasons_reg(axs, C_conc, C_omf, \
        #                      na, 'k', 2)
        #     C_conc_ar, C_omf_ar = C_conc, C_omf
        #     for i, val in enumerate(C_omf):
        #         list_conc_x_month[i].append(C_conc[i])
        #         list_omf_x_month[i].append(val)

    from statistics import variance

    var_conc = C_conc_std[-1]
    fill_between_shade(axs[0], t_ax, C_conc_ar, var_conc, 'gray')

    var_omf = data_omf_std['Total OMF']
    fill_between_shade(axs[1], t_ax, C_omf_ar, var_omf, 'gray')

    for i, axs in enumerate(ax):
        axs.set_title(titles_1[i], loc='right', fontsize=f)
        axs.xaxis.set_tick_params(labelsize=f)
        axs.grid(linestyle='--', linewidth=0.4)

        axs.xaxis.set_major_formatter(plt.FuncFormatter(format_func))

    box = ax[0].get_position()
    ax[0].set_position([box.x0, box.y0 + box.height * 0.1,
                        box.width, box.height * 0.9])
    fig.legend(handles=leg_list,
               ncol=3,
               bbox_to_anchor=(0.5, 0.),
               loc='upper center',
               fontsize=f)
    fig.tight_layout()
    plt.savefig(f'Multiannual monthly trends poles and subregions{yr}_updated.png', dpi=300, bbox_inches="tight")



def seasonality_plot_thesis(reg_data):
    for yr in list(reg_data['Arctic'].keys()):

        fig, axis = plt.subplots(2, 2, figsize=(10, 8))  # 15,8
        axs = axis.flatten()
        fig.subplots_adjust(right=0.75)
        limits = [[0, 7.5], [1e-6, 1e0], [0.1, 0.23]]

        leg_list = []
        linestyle = [
            '-',  # Arctic (solid)
            '--',  # Barents Sea (dashed)
            ':',  # Kara Sea (dotted)
            '-.',  # Laptev Sea (dash–dot)
            (0, (3, 5, 1, 5)),  # East-Siberian Sea (long-dash + dot)
            (0, (5, 1, 1, 1)),  # Chukchi Sea (medium-dash + dot)
            (0, (5, 2, 1, 2)),  # Beaufort Sea (medium-dash + dot, slightly longer gaps)
            (0, (3, 1, 1, 1, 1, 1)),  # Canadian Archipelago (short-dash + multi-dot)
            (0, (1, 5)),  # Baffin Bay (short-dash + long gap)
            ':',  # Greenland & Norwegian Sea (dotted)
            '--',  # Central Arctic (dashed)
        ]
        color_reg = global_vars.colors_arctic_reg
        unit = global_vars.units_concentration
        unit = f'Carbon concentration \n ({unit})'
        for idx, na in enumerate(reg_data.keys()):
            if na != 'Antarctica':
                data = reg_data[na][yr]['var_seasonality']
                title = ['Biomolecules', r'$\bf{(a)}$']
                # C_conc = [rm_nan(data['Biom']['PCHO_DCAA']),
                #           rm_nan(data['Biom']['PL'])]
                #
                # plot_seasons_reg_only(axs[0], C_conc,na, color_reg[idx], title)



                C_conc = rm_nan(data['Biom']['PCHO_DCAA'])
                title = ['PCHO$_{sw}$ + DCAA$_{sw}$', r'$\bf{(a)}$']
                plot_seasons_reg_conc_ice(axs[0], C_conc,
                                          na, color_reg[idx], [title, unit], [0, 9], linestyle[idx])

                title = ['PL$_{sw}$', r'$\bf{(b)}$']
                C_conc = rm_nan(data['Biom']['PL'])
                plot_seasons_reg_conc_ice(axs[1], C_conc,
                                          na, color_reg[idx], [title, unit], [0, 1.5], linestyle[idx])

                C_conc = rm_nan(data['Other']['PhyDia'])
                title = ['Phytoplankton', r'$\bf{(c)}$']
                plot_seasons_reg_conc_ice(axs[2], C_conc,
                                          na, color_reg[idx], [title, unit], [0, 40], linestyle[idx],
                                          lower_axis=True)

                omf = rm_nan(data['OMF']['Total OMF'])
                title_omf = ["Total OMF", r'$\bf{(d)}$']
                leg_list.append(plot_seasons_reg_conc_ice(axs[3], omf,
                                          na, color_reg[idx], [title_omf, ' '], [0, 0.5], linestyle[idx],
                                          lower_axis=True))

                # sic = rm_nan(data['Other']['SIC'])
                # title = ["SIC", r'$\bf{(d)}$']
                # leg_list.append(plot_seasons_reg_conc_ice(axs[3], sic,
                #                           na, color_reg[idx], [title, '%'], [0, 100],
                #                                           lower_axis=True),)

        box = axs[0].get_position()
        axs[0].set_position([box.x0, box.y0 + box.height * 0.1,
                            box.width, box.height * 0.9])
        fig.legend(handles=leg_list,
                   ncol=3,
                   bbox_to_anchor=(0.97, 0.),
                   fontsize=f)
        #fig.legend(handles=leg_list, bbox_to_anchor=(0.93, 0.11), loc='lower left', fontsize=18)
        fig.tight_layout()
        plt.savefig(f'Seasonal_concent_omf_regions_{yr}.png', dpi=300, bbox_inches="tight")


def regions_map(reg_data):
    idx = 0
    region_idx = []
    fig, ax = plt.subplots(1, 1, figsize=(7, 4),
                           subplot_kw={'projection': ccrs.NorthPolarStereo()}, )
    ax.set_extent([-180, 180, 63, 90], ccrs.PlateCarree())

    # cmap = mpl.cm.rainbow
    cmap = plt.get_cmap('tab20')
    bounds = np.arange(1, len(list(reg_data.keys())[1:]) + 2)
    cmap = ListedColormap(global_vars.colors_arctic_reg[1:])
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    for i, na in enumerate(reg_data.keys()):
        print(na)
        if na != 'Arctic':
            idx += 1
            # for y,yr in enumerate(list(reg_data[na].keys())):
            for yr in list(reg_data['Arctic'].keys()):
                x = reg_data[na][yr]['var_data_region']['Biom']['Total concentration'].mean('month').to_dataset(name='var1')
                x = x.fillna(0)
                reg_mk = x.assign(var2=lambda x: x['var1'] * 0 + idx)
                print(reg_mk['var2'].max().values)
                reg_data[na][yr]['var_data_region']['reg_mk'] = reg_mk
                #             reg_mk_list_const = [idx]*len()
                region_idx.append(reg_mk['var2'])

                cb = ax.pcolormesh(reg_mk.lon, reg_mk.lat,
                                   reg_mk['var2'],
                                   norm=norm,
                                   cmap=cmap,
                                   alpha=0.8,
                                   # vmin = 0, vmax = 11,
                                   transform=ccrs.PlateCarree())

    cbar = fig.colorbar(cb)
    cbar.set_ticks(np.arange(2, len(list(reg_data.keys())[1:]) + 2) - 0.5,
                   labels=list(reg_data.keys())[1:])
    cbar.ax.tick_params(length=0)  # remove tick lines

    # compute circle
    theta = np.linspace(0, 2 * np.pi, 100)
    center, radius = [0.5, 0.5], 0.5
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = mpath.Path(verts * radius + center)
    ax.set_boundary(circle, transform=ax.transAxes)

    gl = ax.gridlines(draw_labels=True, )
    ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land',
                                                '10m', edgecolor='face',
                                                facecolor='lightgray'))
    ax.coastlines(color='gray')
    gl.ylocator = mticker.FixedLocator([65, 75, 85])
    gl.yformatter = LATITUDE_FORMATTER

    ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land',
                                                '110m', edgecolor='face',
                                                linewidth=0.05,
                                                facecolor='lightgray'))

    fig.tight_layout()
    plt.savefig('Arctic_seas.png', dpi=300)
    plt.show()

    return None