import os
import pickle
import arctic_plots
import global_vars
import plots

try:
    os.makedirs(global_vars.plot_dir)
except OSError:
    pass

if global_vars.seasonality_stations_MH_AI:
    with open(global_vars.pkl+'/reg_data_stat_bx_test_MH_AI.pkl', 'rb') as f:
        reg_data_globe = pickle.load(f)
    plots.plot_seasonality_regions_AI_MH(reg_data_globe)

if global_vars.arctic_regions:
    with open(global_vars.pkl+'/reg_data_arctic_regions_66_arctic_limit.pkl', 'rb') as f:
        reg_data_globe_stat = pickle.load(f)
    # Creates plot Fig. 3 submitted to ACP (https://egusphere.copernicus.org/preprints/2025/egusphere-2025-2829/)
    arctic_plots.seasonality_conc_omf_arctic_and_reg(reg_data_globe_stat)
    arctic_plots.seasonality_plot_thesis(reg_data_globe_stat, paper=True)

    with open(global_vars.pkl+'/reg_data_arctic_regions_63_arctic_limit.pkl', 'rb') as f:
        reg_data_globe_stat = pickle.load(f)
    # Create Arctic seasonality plots used in thesis
    arctic_plots.seasonality_plot_thesis(reg_data_globe_stat)
    # Create map of regions definitions (Fig 1. https://egusphere.copernicus.org/preprints/2025/egusphere-2025-2829/)
    arctic_plots.regions_map(reg_data_globe_stat)

    if global_vars.yearly_months:
        with open(global_vars.pkl+'/reg_data_arctic_regions_yearly_months.pkl', 'rb') as f:
            reg_data_globe_stat = pickle.load(f)
        # Create heatmaps of yearly monthly values for selected regions (Fig C1.
        # https://egusphere.copernicus.org/preprints/2025/egusphere-2025-2829/))
        arctic_plots.yearly_seasonality_specific_reg_heatmap(reg_data_globe_stat)
        arctic_plots.yearly_seasonality_arctic_and_reg_heatmap(reg_data_globe_stat,
                                                               'Other',
                                                               'PhyDia',
                                                               2)
        # Create heatmaps of yearly monthly values for all subregions and biomolecules
        # for var, l in zip(['PCHO', 'DCAA', 'PL'], [8, 2.5, 2]):
        #     # arctic_plots.yearly_seasonality_arctic_and_reg(reg_data_globe_stat, 'Biom', var, l)
        #     arctic_plots.yearly_seasonality_arctic_and_reg_heatmap(reg_data_globe_stat, 'Biom', var, l)

if global_vars.seasonality_stations:
    with open(global_vars.pkl+'/reg_data_stat_bx.pkl', 'rb') as f:
        reg_data_globe_stat = pickle.load(f)
    #Creates plot of seasonality and interpolated values to measurements sites (Shown in Thesis)
    plots.plot_seasonality_regions_with_stations(reg_data_globe_stat)
else:
    with open(global_vars.pkl+'/reg_data_global_regions.pkl', 'rb') as f:
        reg_data_globe = pickle.load(f)
    # Creates plot of seasonality for global regions (shown in Thesis)
    plots.plot_seasonality_regions(reg_data_globe)
