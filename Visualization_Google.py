#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob 

from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']


# MODE = 'all'
MODE = 'normal'


# In[3]:


p_lists = glob.glob("data_Google/p_*")
p_lists.sort()

forecast_dates = [name.split('.')[-2].split('_')[-1] for name in p_lists]


# In[4]:



# Googleの結果(治療中の人数)の描写

df_accommodation_beds = pd.read_csv('data_Koro/accommodation_beds.csv',index_col=0)
df_hospital_beds = pd.read_csv('data_Koro/hospital_beds.csv',index_col=0)
df_severe_beds = pd.read_csv('data_Koro/severe_beds.csv',index_col=0)

weeks  =  df_accommodation_beds.columns[2:].values
new_week = max(weeks)

accommodation_beds = df_accommodation_beds[new_week].values
hospital_beds = df_hospital_beds[new_week].values
severe_beds = df_severe_beds[new_week].values
names = df_accommodation_beds['都道府県名']



# In[8]:


def make_figure(forecast_date):
    # 時間の表示
    print('forecast_date=' + forecast_date)


    df_p = pd.read_csv("data_Google/p_{0}.csv".format(forecast_date),index_col=0)
    df_p0025 = pd.read_csv("data_Google/p0025_{0}.csv".format(forecast_date),index_col=0)
    df_p0975 = pd.read_csv("data_Google/p0975_{0}.csv".format(forecast_date),index_col=0)

    df_x = pd.read_csv("data_severe/x_{0}.csv".format(forecast_date),index_col=0)
    df_x0025 = pd.read_csv("data_severe/x0025_{0}.csv".format(forecast_date),index_col=0)
    df_x0975 = pd.read_csv("data_severe/x0975_{0}.csv".format(forecast_date),index_col=0)



    times =  pd.to_datetime(df_p.index).values


    date_s = min(times)
    date_e = max(times)

    # numpy化
    p = df_p.values
    p0025 = df_p0025.values
    p0975 = df_p0975.values

    x = df_x.values
    x0025 = df_x0025.values
    x0975 = df_x0975.values




    plt.figure(figsize = (6,4)) 


    plt.fill_between(times,p0025.sum(axis=1),p0975.sum(axis=1),facecolor = 'lime',alpha = 0.3,label = '95% 信頼区間')
    plt.plot(times,p.sum(axis=1),'*-',color = 'lime',label = '平均値')

    plt.plot([date_s,date_e],np.ones(2)*hospital_beds.sum(),"--",label = 'Covid-19受け入れ可能な病院のベット数',color = 'red',linewidth = 2.0)
    plt.plot([date_s,date_e],np.ones(2)*(hospital_beds.sum()+accommodation_beds.sum()),"--",label = 'Covid-19受け入れ可能な病院と宿泊施設のベット数',color = 'purple')

    plt.gca().tick_params(axis='x', rotation= -60)
    plt.title('全国の患者数の予測値, 予測日={0}'.format(forecast_date),fontsize = 15)
    plt.xlim([date_s,date_e])
    plt.ylim([0, 3.0* (hospital_beds.sum()+accommodation_beds.sum()),])
    plt.ylabel('Covid-19患者数')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.grid()

    plt.savefig('resultB_google_prediction/all_patients_{0}.png'.format(forecast_date),bbox_inches='tight',dpi = 100)
    if MODE == 'normal':
        plt.savefig('resultB_google_prediction/all_patients.png',bbox_inches='tight',dpi = 100)

    plt.close()




    # 県ごとの感染者数の予測結果
    plt.figure(figsize = (50,25)) 
    plt.subplots_adjust(wspace=0.1, hspace=0.5)

    for i in range(47):
        plt.subplot(10,5,i+1)

        plt.fill_between(times,p0025[:,i],p0975[:,i],facecolor = 'lime',alpha = 0.3,label = '95%信頼区間')
        plt.plot(times,p[:,i],'*-',color = 'lime', label = '平均値')

        plt.plot([date_s,date_e],np.ones(2)*hospital_beds[i],"--",label = 'Covid-19受け入れ可能な病院のベット数',color = 'red',linewidth = 2.0)
        plt.plot([date_s,date_e],np.ones(2)*(hospital_beds[i]+accommodation_beds[i]),"--",label = 'Covid-19受け入れ可能な病院と宿泊施設のベット数',color = 'purple',linewidth = 2.0)

        plt.gca().tick_params(axis='x', rotation= -60)
        plt.title(names[i],fontsize = 20)
        plt.xlim([date_s,date_e])
        plt.ylim([0, 6.0* (hospital_beds[i]+accommodation_beds[i]),])
        plt.grid()
        if i < 42:
            plt.tick_params(labelbottom=False)
        if i == 0:
            plt.legend()

    plt.savefig('resultB_google_prediction/each_patients_{0}.png'.format(forecast_date),bbox_inches='tight',dpi = 100)
    if MODE == 'normal':
        plt.savefig('resultB_google_prediction/each_patients.png',bbox_inches='tight',dpi = 100)
    plt.close()



# In[9]:


if MODE == 'all':
    for f_date in forecast_dates:
        make_figure(f_date)
elif MODE == 'normal':
    make_figure(max(forecast_dates))

