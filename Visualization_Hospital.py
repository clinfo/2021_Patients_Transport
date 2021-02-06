#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']


# In[2]:


# Make directory
# 
# df_hospital_beds = pd.read_csv('data_Koro/hospital_beds.csv',index_col=0)
# dirnames = (df_hospital_beds['japan_prefecture_code']+df_hospital_beds['都道府県名']).values
# for i in range(len(dirnames)):
#     path = 'resultD_transport_strategy_hospital/' +  dirnames[i]
#     os.makedirs(path, exist_ok=True)


# In[3]:


# MODE = 'all'
MODE = 'normal'

filenames = glob.glob('data_hospital/x_*')
filenames.sort()
forecast_dates = [filename.split('_')[-1].split('.')[0] for filename in filenames]


# In[ ]:





# In[18]:





def visualization(gamma,x_type,forecast_date): 
    print("forcasted date ={0}".format(f_date))
    
    # 重みの入力
    df_w = pd.read_csv('data_Kokudo/w_distance.csv',index_col=0)
    W= df_w.values
    w_pulp = W.T.reshape(-1)

    
    # x, x_q0025も計算
    df_x0975 = pd.read_csv('data_hospital/x0975_{0}.csv'.format(forecast_date),index_col=0 )
    df_x0025 = pd.read_csv('data_hospital/x0025_{0}.csv'.format(forecast_date),index_col=0 )
    df_xmean = pd.read_csv('data_hospital/x_{0}.csv'.format(forecast_date),index_col=0 )
    gammas = np.load('data_hospital_transport/gammas_{0}_{1:03}_{2}.npy'.format(x_type,int(gamma*100),forecast_date))

    x_mean = df_xmean.values
    x_q0975 = df_x0975.values
    x_q0025 = df_x0025.values

    N = x_mean.shape[1]
    T = x_mean.shape[0]

    L = np.kron(np.ones((1,N)),np.eye(N)) - np.kron(np.eye(N),np.ones((1,N)))

    uv = np.load('data_hospital_transport/u_{0}_{1:03}_{2}.npy'.format(x_type,int(gamma*100),forecast_date))
    
    y_mean =  np.zeros(x_mean.shape)
    y_q0975 = np.zeros(x_mean.shape)
    y_q0025 =  np.zeros(x_mean.shape)

    y_mean[0] = x_mean[0]
    y_q0975[0] = x_q0975[0]
    y_q0025[0] = x_q0025[0]

    sum_u = np.zeros(T)
    sum_cost = np.zeros(T)

    for k in range(T-1):
        y_mean[k+1] = y_mean[k] + x_mean[k+1] - x_mean[k]  + L.dot(uv[k])
        y_q0975[k+1] = y_q0975[k] + x_q0975[k+1] - x_q0975[k]  + L.dot(uv[k])
        y_q0025[k+1] = y_q0025[k] + x_q0025[k+1] - x_q0025[k]  + L.dot(uv[k])
        sum_u[k+1] = np.sum(uv[k])
        sum_cost[k+1] = np.sum(w_pulp*uv[k])

    # ベット数の入力 
    df_hospital_beds = pd.read_csv('data_Koro/hospital_beds.csv',index_col=0)
    dirnames = (df_hospital_beds['japan_prefecture_code']+df_hospital_beds['都道府県名']).values
    names = df_hospital_beds['都道府県名'].values

    weeks  =  df_hospital_beds.columns[2:].values
    new_week = max(weeks)
    M = df_hospital_beds[new_week].values

    times = pd.to_datetime(df_xmean.index)
    date_s = min(times)
    date_e = max(times)



    # 全国の入院者数の予測値
    plt.figure(figsize = (6,4)) 

    plt.fill_between(times,x_q0025.sum(axis=1),x_q0975.sum(axis=1),facecolor = 'lime',alpha = 0.3,label = '95%信頼区間')
    plt.plot(times,x_mean.sum(axis=1),'*-',color = 'lime',label = '平均値')

    plt.plot([date_s,date_e],np.ones(2)*0.8*M.sum(),"--",label = '病床使用率 80%',color = 'red',linewidth = 2.0)
    plt.plot([date_s,date_e],np.ones(2)*M.sum(),"--",label = '病床使用率 100%',color = 'purple',linewidth = 2.0)

    plt.gca().tick_params(axis='x', rotation= -60)
    plt.title('全国の入院者数の予測値, 予測日={0}'.format(forecast_date),fontsize = 15)
    plt.xlim([date_s,date_e])
    plt.ylim([0, 1.5* M.sum(),])
    plt.ylabel('入院者数 [人]')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.grid()

    plt.savefig('resultB_google_prediction/all_hospital_{0}.png'.format(forecast_date),bbox_inches='tight',dpi = 100)
    if MODE == 'normal':
        plt.savefig('resultB_google_prediction/all_hospital.png',bbox_inches='tight',dpi = 100)

    plt.close()

    # 県ごとの入院者数
    plt.figure(figsize = (50,25)) 
    plt.subplots_adjust(wspace=0.1, hspace=0.5)

    for i in range(47):
        plt.subplot(10,5,i+1)

        plt.fill_between(times,x_q0025[:,i],x_q0975[:,i],facecolor = 'lime',alpha = 0.3,label = '95%信頼区間')
        plt.plot(times,x_mean[:,i],'*-',color = 'lime',label = '平均値')

        plt.plot([date_s,date_e],np.ones(2)*0.8*M[i],"--",label = '病床使用率 80%',color = 'red',linewidth = 2.0)
        plt.plot([date_s,date_e],np.ones(2)*M[i],"--",label = '病床使用率 100%',color = 'purple',linewidth = 2.0)


        plt.gca().tick_params(axis='x', rotation= -60)
        plt.title(names[i],fontsize = 20)
        plt.xlim([date_s,date_e])
        plt.ylim([0, 1.5* M[i]])
        plt.grid()

        if i < 42:
            plt.tick_params(labelbottom=False)
        if i == 0:
            plt.legend()

    plt.savefig('resultB_google_prediction/each_hospital_{0}.png'.format(forecast_date),bbox_inches='tight',dpi = 100)
    if MODE == 'normal':
        plt.savefig('resultB_google_prediction/each_hospital.png',bbox_inches='tight',dpi = 100)
    plt.close()

        
    # 県ごとの感染者数の予測結果
    plt.figure(figsize = (50,25)) 
    plt.subplots_adjust(wspace=0.1, hspace=0.5)
    for i in range(47):
        plt.subplot(10,5,i+1)

        max_beds = M[i]
    # ベットの限界
        plt.plot([date_s,date_e],[0.8*max_beds,0.8*max_beds],'--',label = '病床使用率80%',color = 'red',linewidth = 2.0)
        plt.plot([date_s,date_e],[max_beds,max_beds],'--',label = '病床使用率100%',color = 'purple',linewidth = 2.0)
    # 輸送なし
        plt.fill_between(times,x_q0025[:,i],x_q0975[:,i],facecolor = 'lime',alpha = 0.5,label = '医療シェアリングなし',)    
        plt.plot(times,x_mean[:,i],"*-",linewidth =  2,color= 'lime')

    # 輸送あり
        plt.fill_between(times,y_q0025[:,i],y_q0975[:,i],facecolor = 'orange',alpha = 0.5,label = '医療シェアリングあり',)    
        plt.plot(times,y_mean[:,i],"*-",linewidth =  2,color = 'orange')


        plt.xlim([date_s,date_e])
        plt.ylim([0,1.5*max_beds])
        plt.grid()
        plt.gca().tick_params(axis='x', rotation= -60)
        plt.title(names[i],fontsize = 20)
        if i < 42:
            plt.tick_params(labelbottom=False)
        if i == 0:
            plt.legend()


    if MODE == 'normal':
        plt.savefig('resultD_transport_strategy_hospital/main/each_severe_{0}_{1:03}.png'.format(x_type,int(gamma*100)),bbox_inches='tight',dpi = 100)
    plt.savefig('resultD_transport_strategy_hospital/main/each_severe_{0}_{1:03}_{2}.png'.format(x_type,int(gamma*100),forecast_date),bbox_inches='tight',dpi = 100)
    plt.close()

    # コスト評価

    times = pd.to_datetime(df_xmean.index)[:-1]

    date_s = min(times)
    date_e = max(times)
    max_beds = M.sum()

    # 輸送人数
    plt.plot(times,sum_u[:-1],"*-",linewidth =  2,color= 'black',label = '入院者数')

    plt.xlim([date_s,date_e])

    plt.gca().tick_params(axis='x', rotation= -60)
    # plt.title('',fontsize = 20)
    plt.ylabel('毎日の医療シェアが必要な入院者の合計 [人]')

    plt.legend()
    if MODE == 'normal':
        plt.savefig('resultD_transport_strategy_hospital/cost/num_{0}_{1:03}.png'.format(x_type,int(gamma*100)),bbox_inches='tight',dpi = 100)
    plt.savefig('resultD_transport_strategy_hospital/cost/num_{0}_{1:03}_{2}.png'.format(x_type,int(gamma*100),forecast_date),bbox_inches='tight',dpi = 100)
    plt.close()


    times = pd.to_datetime(df_xmean.index)[:-1]

    date_s = min(times)
    date_e = max(times)
    max_beds = M.sum()

    # 輸送コスト
    plt.plot(times,sum_cost[:-1],"*-",linewidth =  2,color= 'black',label = '医療シェアリングのコスト')

    plt.xlim([date_s,date_e])

    plt.gca().tick_params(axis='x', rotation= -60)

    plt.legend()

    plt.ylabel('毎日のコスト [km]')
    if MODE == 'normal':
        plt.savefig('resultD_transport_strategy_hospital/cost/cost_{0}_{1:03}.png'.format(x_type,int(gamma*100)),bbox_inches='tight',dpi = 100)
    plt.savefig('resultD_transport_strategy_hospital/cost/cost_{0}_{1:03}_{2}.png'.format(x_type,int(gamma*100),forecast_date),bbox_inches='tight',dpi = 100)
    plt.close()


    times = pd.to_datetime(df_xmean.index)[:-1]

    date_s = min(times)
    date_e = max(times)
    max_beds = M.sum()

    # 輸送コスト
    plt.plot(times,sum_cost[:-1]/sum_u[:-1],"*-",linewidth =  2,color= 'black',label = '入院者ごとの依頼コスト')

    plt.xlim([date_s,date_e])

    plt.gca().tick_params(axis='x', rotation= -60)
    plt.legend()

    plt.ylabel('入院者ごとの依頼コスト [km/人]')

    if MODE == 'normal':
        plt.savefig('resultD_transport_strategy_hospital/cost/performance_{0}_{1:03}.png'.format(x_type,int(gamma*100)),bbox_inches='tight',dpi = 100)
    plt.savefig('resultD_transport_strategy_hospital/cost/performance_{0}_{1:03}_{2}.png'.format(x_type,int(gamma*100),forecast_date),bbox_inches='tight',dpi = 100)
    plt.close()


    times = pd.to_datetime(df_xmean.index)

    plt.plot(times,gammas*100)
    plt.gca().tick_params(axis='x', rotation= -60)
    plt.ylabel('病床利用率の上限 [%]')

    if MODE == 'normal':
        plt.savefig('resultD_transport_strategy_hospital/cost/gammas_{0}_{1:03}.png'.format(x_type,int(gamma*100)),bbox_inches='tight',dpi = 300)
    plt.savefig('resultD_transport_strategy_hospital/cost/gammas_{0}_{1:03}_{2}.png'.format(x_type,int(gamma*100),forecast_date),bbox_inches='tight',dpi = 300)
    plt.close()


    #  各県の搬送数
    U = uv.reshape(T,N,N)

    U_sum = np.zeros(U.shape)
    U_sum[0] = U[0]
    for i in range(U_sum.shape[0]-1):
        U_sum[i+1] = U_sum[i] + U[i+1]

    times_U = np.sum(U_sum>0,axis=0)


    for target in range(N):
#         if sum(U[:,target,:].sum(0)>0) >0:
        plt.figure(figsize = (10,6)) 

        times = pd.to_datetime(df_xmean.index)[:-1]
        num_U=np.sum(times_U[target] !=0)
        index_U = np.argsort(times_U[target,:])[::-1]
        tmp_names = names[index_U[:num_U]]

        for i in range(tmp_names.shape[0]):
            out_target = U_sum[:-1,target,index_U[i]]
            plt.plot(times,out_target,'-*',label =  tmp_names[i])

        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.grid()
        plt.gca().tick_params(axis='x', rotation= -60)

        plt.ylabel('地域間で医療シェアが必要な入院者数の合計 [人]')
        plt.title(names[target]+'から他地域へのシェアリング')
        if MODE == 'normal':
            plt.savefig('resultD_transport_strategy_hospital/' + dirnames[target]+'/transport_{0}_{1:03}.png'.format(x_type,int(gamma*100)),bbox_inches='tight',dpi = 300)
        plt.savefig('resultD_transport_strategy_hospital/' + dirnames[target]+'/transport_{0}_{1:03}_{2}.png'.format(x_type,int(gamma*100),forecast_date),bbox_inches='tight',dpi = 300)
        plt.close()




# In[19]:


# 重傷者病床上限率の設定
gamma_list = [0.8,1.0]
# 使う条件の設定
x_type_list = ['upper','mean']

if MODE == 'all':
    for f_date in forecast_dates:
        for gamma in gamma_list:
            for x_type in x_type_list:
                visualization(gamma,x_type,f_date)
elif MODE == 'normal':
    f_date = max(forecast_dates)
    for gamma in gamma_list:
        for x_type in x_type_list:
            visualization(gamma,x_type,f_date)


