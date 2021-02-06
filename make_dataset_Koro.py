# Author: S. Inoue
# Date: 12/19/2020
# Updated: 12/19/2020
# Project: Patients_Transport
# Scropt: To generate (add) dataset from raw Koro-sho data for preprosessing

import pandas as pd
import numpy as np
import glob
import sys

def time(df_path):
    yy = df_path.split('/')[2][0:4]
    mm = df_path.split('/')[2][4:6]
    dd = df_path.split('/')[2][6:8]
    yymmdd = yy + '-' + mm + '-' + dd
    print(f'[INFO] Timestamp of raw data [[ {yymmdd} ]]')
    return yymmdd


def add_data(df_raw, df_aim_path, df_aim_row, timestamp):
    df_aim = pd.read_csv(f'data_Koro/{df_aim_path}', index_col=0)
    print(f'[LOAD] {df_aim_path}')
    time_log = df_aim.columns
    if timestamp not in time_log:
        l = np.array(df_raw.iloc[:, df_aim_row])
        df_aim[timestamp] = l
        df_aim.to_csv(f'data_Koro/{df_aim_path}')
        print('[SAVE] add and save the data')
        return
    else:
        print('[ERROR] already added')
        return


if __name__ == '__main__':
    # read data
    df_path = f'{sys.argv[1]}'
    df_raw = pd.read_csv(df_path, header=None).replace(r"\,", "", regex=True)
    df_raw.drop(df_raw.tail(1).index, inplace=True)  # reshape
    # timestamp
    timestamp = time(df_path)

    # file list
    file_list = ['patients.csv',
                 'hospital_patients.csv', 'hospital_beds.csv',
                 'severe_patients.csv', 'severe_beds.csv',
                 'accommodation_patients.csv', 'accommodation_beds.csv']
    file_row_list = [1, 2, 4, 7, 9, 12, 14]
    # add the data
    for (f, f_r) in zip(file_list, file_row_list):
        add_data(df_raw, f, f_r, timestamp)
