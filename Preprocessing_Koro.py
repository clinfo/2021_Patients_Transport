#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob

from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio',
                               'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']


# 最新の計測日でN_min 以上の患者数存在する県は，個別に重症者率を推定する最小
N_min = 500


df_patients = pd.read_csv('data_Koro/patients.csv', index_col=0)
df_severe_patients = pd.read_csv('data_Koro/severe_patients.csv', index_col=0)

times = df_patients.columns[2:]
new_time = max(times)

calc_ken = df_patients[new_time] >= N_min
ratio_data = (df_severe_patients[calc_ken]
              [times]/df_patients[calc_ken][times]).values

ratio_data = np.c_[ratio_data.T, df_severe_patients[times].values.sum(
    axis=0) / df_patients[times].values.sum(axis=0)].T
names = list(df_patients[calc_ken]['都道府県名']) + ['全国']


for i in range(len(names)):
    plt.plot(pd.to_datetime(times), ratio_data[i], '-*', label=names[i])

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
plt.ylabel("重症者数比")
plt.title(min(times)+'から'+max(times)+'の厚労省発表のデータを使った各県の重症者数比')
plt.grid()
plt.gca().tick_params(axis='x', rotation=-60)
plt.savefig('resultA_severe_patients_ratio/ratio.png',
            bbox_inches='tight', dpi=300)
plt.savefig(
    'resultA_severe_patients_ratio/ratio_{0}.png'.format(new_time), bbox_inches='tight', dpi=300)
plt.close()


df_ratio = pd.DataFrame(df_patients[['japan_prefecture_code', '都道府県名']])
df_ratio['new_ratio'] = df_severe_patients[new_time].sum() / \
    df_patients[new_time].sum()
df_ratio.loc[calc_ken, 'new_ratio'] = df_severe_patients[calc_ken][new_time] / \
    df_patients[calc_ken][new_time]
df_ratio.to_csv('data_severe_ratio/ratio.csv')
df_ratio.to_csv('data_severe_ratio/ratio_{0}.csv'.format(new_time))


df_hospital_patients = pd.read_csv(
    'data_Koro/hospital_patients.csv', index_col=0)


hospital_ratio_data = (
    df_hospital_patients[calc_ken][times]/df_patients[calc_ken][times]).values

hospital_ratio_data = np.c_[hospital_ratio_data.T, df_hospital_patients[times].values.sum(
    axis=0) / df_patients[times].values.sum(axis=0)].T


for i in range(len(names)):
    plt.plot(pd.to_datetime(times),
             hospital_ratio_data[i], '-*', label=names[i])

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
plt.ylabel("入院者数比")
plt.title(min(times)+'から'+max(times)+'の厚労省発表のデータを使った各県の入院者数比')
plt.grid()
plt.gca().tick_params(axis='x', rotation=-60)
plt.savefig('resultA_hospital_patients_ratio/ratio.png',
            bbox_inches='tight', dpi=300)
plt.savefig('resultA_hospital_patients_ratio/ratio_{0}.png'.format(
    new_time), bbox_inches='tight', dpi=300)
plt.close()


df_hospital_ratio = pd.DataFrame(
    df_patients[['japan_prefecture_code', '都道府県名']])
df_hospital_ratio['new_ratio'] = df_hospital_patients[new_time].sum(
)/df_patients[new_time].sum()
df_hospital_ratio.loc[calc_ken, 'new_ratio'] = df_hospital_patients[calc_ken][new_time] / \
    df_patients[calc_ken][new_time]

df_hospital_ratio.to_csv('data_hospital_ratio/ratio.csv')
df_hospital_ratio.to_csv('data_hospital_ratio/ratio_{0}.csv'.format(new_time))
