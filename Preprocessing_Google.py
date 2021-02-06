#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']


# 事前処理

df_google = pd.read_csv("https://storage.googleapis.com/covid-external/forecast_JAPAN_PREFECTURE_28.csv")
df_google['target_prediction_date'] = pd.to_datetime(df_google['target_prediction_date'])
df_real =df_google[df_google['hospitalized_patients'].isnull()]
df_google = df_google[~df_google['hospitalized_patients'].isnull()]


# 重症者率
df_ratio = pd.read_csv('data_severe_ratio/ratio.csv',index_col=0)

# 入院率
df_hospital = pd.read_csv('data_hospital_ratio/ratio.csv',index_col=0)




# データ整理
N = 47
kens =  df_ratio['japan_prefecture_code']
df_x =  pd.DataFrame()
for i in range(N):
    ken = kens[i]

    df_tmp = df_google[df_google['japan_prefecture_code'] == ken][['target_prediction_date','hospitalized_patients']]
    df_tmp_min = df_google[df_google['japan_prefecture_code'] == ken][['target_prediction_date','hospitalized_patients_q0025']]
    df_tmp_max = df_google[df_google['japan_prefecture_code'] == ken][['target_prediction_date','hospitalized_patients_q0975']]
    df_tmp.columns = ['target_prediction_date',ken]
    df_tmp_min.columns = ['target_prediction_date',ken]
    df_tmp_max.columns = ['target_prediction_date',ken]
    if i == 0:
        df_x = df_tmp
        df_x0025 = df_tmp_min
        df_x0975 = df_tmp_max
    else:
        df_x = pd.merge(df_x,df_tmp,on  = 'target_prediction_date')
        df_x0025 = pd.merge(df_x0025,df_tmp_min,on  = 'target_prediction_date')
        df_x0975 = pd.merge(df_x0975,df_tmp_max,on  = 'target_prediction_date')

df_x.index = df_x.target_prediction_date.values
df_x0025.index = df_x0025.target_prediction_date.values
df_x0975.index = df_x0975.target_prediction_date.values
df_x = df_x[df_x.columns[1:]]
df_x0025 = df_x0025[df_x0025.columns[1:]]
df_x0975 = df_x0975[df_x0975.columns[1:]]
df_p = df_x.copy()
df_p0025 = df_x0025.copy()
df_p0975 = df_x0975.copy()
df_h = df_x.copy()
df_h0025 = df_x0025.copy()
df_h0975 = df_x0975.copy()


df_x[df_x.columns] =df_ratio['new_ratio'].values *df_p.values
df_x0025[df_x0025.columns] =df_ratio['new_ratio'].values *df_p0025.values
df_x0975[df_x0975.columns] =df_ratio['new_ratio'].values *df_p0975.values

df_h[df_h.columns] =df_hospital['new_ratio'].values *df_p.values
df_h0025[df_h0025.columns] =df_hospital['new_ratio'].values *df_p0025.values
df_h0975[df_h0975.columns] =df_hospital['new_ratio'].values *df_p0975.values



forecast_date = df_google.forecast_date[0]


df_p.to_csv("data_Google/p.csv")
df_p0025.to_csv("data_Google/p0025.csv")
df_p0975.to_csv("data_Google/p0975.csv")

df_x.to_csv("data_severe/x.csv")
df_x0025.to_csv("data_severe/x0025.csv")
df_x0975.to_csv("data_severe/x0975.csv")

df_h.to_csv("data_hospital/x.csv")
df_h0025.to_csv("data_hospital/x0025.csv")
df_h0975.to_csv("data_hospital/x0975.csv")


df_p.to_csv("data_Google/p_{0}.csv".format(forecast_date))
df_p0025.to_csv("data_Google/p0025_{0}.csv".format(forecast_date))
df_p0975.to_csv("data_Google/p0975_{0}.csv".format(forecast_date))

df_x.to_csv("data_severe/x_{0}.csv".format(forecast_date))
df_x0025.to_csv("data_severe/x0025_{0}.csv".format(forecast_date))
df_x0975.to_csv("data_severe/x0975_{0}.csv".format(forecast_date))

df_h.to_csv("data_hospital/x_{0}.csv".format(forecast_date))
df_h0025.to_csv("data_hospital/x0025_{0}.csv".format(forecast_date))
df_h0975.to_csv("data_hospital/x0975_{0}.csv".format(forecast_date))



print('forecast_date=' + forecast_date)


