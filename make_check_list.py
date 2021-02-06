#!/usr/bin/env python
# coding: utf-8

import numpy  as np
import pandas as pd
import glob


filnames  = glob.glob('data_transport/u_*')
filnames.sort()
dates = [filname.split('.')[-2].split('_')[-1] for filname in filnames]
gammas = [filname.split('.')[-2].split('_')[-2] for filname in filnames]
opt_types = [filname.split('.')[-2].split('_')[-3] for filname in filnames]


df_severe_beds = pd.read_csv('data_Koro/severe_beds.csv',index_col=0)
df_u =  pd.DataFrame(df_severe_beds['japan_prefecture_code'])
df_u['都道府県名'] = df_severe_beds['都道府県名']
df_i = df_u.copy()

for i in range(len(filnames)):
    uv = np.load(filnames[i])
    T = uv.shape[0]
    N = int(np.sqrt(uv.shape[1]))
    U = uv.reshape(T,N,N)
    df_u[opt_types[i] + '_' + gammas[i] + '_' + dates[i]] = U[:14,:,:].sum(axis = 0).sum(1)
    df_i[opt_types[i] + '_' + gammas[i] + '_' + dates[i]] = U[:14,:,:].sum(axis = 0).sum(0)


df_u.to_csv('resultC_transport_strategy/summary/export_num.csv')
df_i.to_csv('resultC_transport_strategy/summary/import_num.csv')


dirC = 'resultC_tranport_strategy/'
dirnames = (df_severe_beds['japan_prefecture_code'] + df_severe_beds['都道府県名']).values



for i in range(len(filnames)):
    uv = np.load(filnames[i])
    T = uv.shape[0]
    N = int(np.sqrt(uv.shape[1]))
    U = uv.reshape(T,N,N)

    png_links = [dirC +  dirnames[j] + '/transport_{0}_{1}_{2}.png\n'.format(opt_types[i],gammas[i],dates[i]) for j in range(df_u.shape[0]) if U[:14,:,:].sum(axis = 0).sum(1)[j]>0]

    path = 'slide_png_list/transport_{0}_{1}_{2}.txt'.format(opt_types[i],gammas[i],dates[i])

    with open(path, mode='w') as f:
        f.writelines(png_links)

    if dates[i] == max(dates) and opt_types[i] == 'mean':
        path = 'slide_png_list/transport_{0}.txt'.format(gammas[i])

        with open(path, mode='w') as f:
            f.writelines(png_links)

# ################################### Hospital ######################################

filnames  = glob.glob('data_hospital_transport/u_*')
filnames.sort()
dates = [filname.split('.')[-2].split('_')[-1] for filname in filnames]
gammas = [filname.split('.')[-2].split('_')[-2] for filname in filnames]
opt_types = [filname.split('.')[-2].split('_')[-3] for filname in filnames]


df_severe_beds = pd.read_csv('data_Koro/hospital_beds.csv',index_col=0)
df_u =  pd.DataFrame(df_severe_beds['japan_prefecture_code'])
df_u['都道府県名'] = df_severe_beds['都道府県名']
df_i = df_u.copy()

for i in range(len(filnames)):
    uv = np.load(filnames[i])
    T = uv.shape[0]
    N = int(np.sqrt(uv.shape[1]))
    U = uv.reshape(T,N,N)
    df_u[opt_types[i] + '_' + gammas[i] + '_' + dates[i]] = U[:14,:,:].sum(axis = 0).sum(1)
    df_i[opt_types[i] + '_' + gammas[i] + '_' + dates[i]] = U[:14,:,:].sum(axis = 0).sum(0)


df_u.to_csv('resultD_transport_strategy_hospital/summary/export_num.csv')
df_i.to_csv('resultD_transport_strategy_hospital/summary/import_num.csv')


dirD = 'resultD_transport_strategy_hospital/'
dirnames = (df_severe_beds['japan_prefecture_code'] + df_severe_beds['都道府県名']).values


for i in range(len(filnames)):
    uv = np.load(filnames[i])
    T = uv.shape[0]
    N = int(np.sqrt(uv.shape[1]))
    U = uv.reshape(T,N,N)

    png_links = [dirD +  dirnames[j] + '/transport_{0}_{1}_{2}.png\n'.format(opt_types[i],gammas[i],dates[i]) for j in range(df_u.shape[0]) if U[:14,:,:].sum(axis = 0).sum(1)[j]>0]

    path = 'slide_png_hospital/transport_{0}_{1}_{2}.txt'.format(opt_types[i],gammas[i],dates[i])

    with open(path, mode='w') as f:
        f.writelines(png_links)

    if dates[i] == max(dates) and opt_types[i] == 'mean':
        path = 'slide_png_hospital/transport_{0}.txt'.format(gammas[i])

        with open(path, mode='w') as f:
            f.writelines(png_links)




# ################################### over_beds_date ######################################

filenames = glob.glob('data_severe/x_*')
filenames.sort()
forecast_dates = [filename.split('_')[-1].split('.')[0] for filename in filenames]

df_severe = pd.read_csv("data_severe/x_" +max(forecast_dates) +  ".csv",index_col=0)
df_hospital = pd.read_csv("data_hospital/x_" +max(forecast_dates) +  ".csv",index_col=0)
df_hospital_beds = pd.read_csv('data_Koro/hospital_beds.csv',index_col=0)
df_severe_beds = pd.read_csv('data_Koro/severe_beds.csv',index_col=0)

new_time_google = max(forecast_dates)
new_time_Koro = max(df_hospital_beds.columns[2:])
N = df_severe.shape[1]

severe_beds = df_severe_beds[new_time_Koro].values
hospital_beds = df_hospital_beds[new_time_Koro].values


gamma = 1
over_severe_beds100 = []
over_hospital_beds100 = []

for i in range(N):
    if sum(df_severe[df_severe.columns[i]] > gamma * severe_beds[i]) !=0:
        over_severe_beds100.append( min(df_severe.index[df_severe[df_severe.columns[i]] > gamma * severe_beds[i]]))
    else:
        over_severe_beds100.append(None)
    if sum(df_hospital[df_hospital.columns[i]] > gamma * hospital_beds[i]) !=0:
        over_hospital_beds100.append( min(df_hospital.index[df_hospital[df_hospital.columns[i]] > gamma * hospital_beds[i]]))
    else:
        over_hospital_beds100.append(None)



gamma = 0.8
over_severe_beds080 = []
over_hospital_beds080 = []

for i in range(N):
    if sum(df_severe[df_severe.columns[i]] > gamma * severe_beds[i]) !=0:
        over_severe_beds080.append( min(df_severe.index[df_severe[df_severe.columns[i]] > gamma * severe_beds[i]]))
    else:
        over_severe_beds080.append(None)

    if sum(df_hospital[df_hospital.columns[i]] > gamma * hospital_beds[i]) !=0:
        over_hospital_beds080.append( min(df_hospital.index[df_hospital[df_hospital.columns[i]] > gamma * hospital_beds[i]]))
    else:
        over_hospital_beds080.append(None)

df = df_hospital_beds[['japan_prefecture_code','都道府県名']].copy()
df['over_severe_beds080'] = over_severe_beds080
df['over_severe_beds100'] = over_severe_beds100
df['over_hospital_beds080'] = over_hospital_beds080
df['over_hospital_beds100'] = over_hospital_beds100
df.to_csv('slide_over_beds/over_list_'+new_time_google +'.csv')
