import os
import sys
import socket
import pandas as pd

if socket.gethostname() == 'chime4':
    sys.path.append('/mnt/hdd8tb/phiwei/repos/chimecore')
    path_imgs_base = '/mnt/ssd2tb/data/prostate_tcga_macenko_0.904037'
    path_out_base = '/mnt/ssd2tb/data/data_lab'
    path_df_lab = '/mnt/ssd2tb/data/data_lab/df_tile_lab.pkl'

from chimecore.utils import Copier

df_lab = pd.read_pickle(path_df_lab)

copier = Copier(slide_col='slide_name', 
                tile_col_in='tile_name_ssd', 
                tile_col_out='tile_name_ssd')

# Loop over sets
for i_set, set_name in enumerate(['train', 'valid', 'test']):
    
    # Set output paths
    path_out_base_curr_lo = os.path.join(path_out_base, set_name, 'low') 
    path_out_base_curr_hi = os.path.join(path_out_base, set_name, 'high') 

    # Make output paths
    os.makedirs(path_out_base_curr_lo)
    os.makedirs(path_out_base_curr_hi)

    # Get current dataframes
    df_curr = df_lab.loc[df_lab['set'] == i_set].reset_index(drop=True)
    df_curr_lo = df_curr.loc[df_curr['class'] == 'low'].reset_index(drop=True)
    df_curr_hi = df_curr.loc[df_curr['class'] == 'high'].reset_index(drop=True)

    # Copy files
    copier.write(df_curr_lo, path_base_in=path_imgs_base, path_base_out=path_out_base_curr_lo, n_jobs=-1)
    copier.write(df_curr_hi, path_base_in=path_imgs_base, path_base_out=path_out_base_curr_hi, n_jobs=-1)
