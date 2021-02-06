#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pulp
import glob

from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']


# In[5]:


filenames = glob.glob('data_hospital/x_*')
filenames.sort()
filenames
date_list = [filename.split('_')[-1].split('.')[0] for filename in filenames]
f_date = max(date_list)


# In[9]:


def calc_transport(gamma,x_type,forecast_date):
    # データの入力
    if x_type == 'upper':
        df_x = pd.read_csv('data_hospital/x0975_{0}.csv'.format(forecast_date),index_col=0 )
    if x_type == 'mean':
        df_x = pd.read_csv('data_hospital/x_{0}.csv'.format(forecast_date),index_col=0 )

    x = df_x.values

    df_hospital_beds = pd.read_csv('data_Koro/hospital_beds.csv',index_col=0)
    dirnames = (df_hospital_beds['japan_prefecture_code']+df_hospital_beds['都道府県名']).values
    names = df_hospital_beds['都道府県名'].values

    weeks  =  df_hospital_beds.columns[2:].values
    new_week = max(weeks)
    M = df_hospital_beds[new_week].values


    N = x.shape[1]
    T = x.shape[0]

    U = np.zeros((T,N,N))
    L =  np.kron(np.ones((1,N)),np.eye(N)) - np.kron(np.eye(N),np.ones((1,N)))


    df_w = pd.read_csv('data_Kokudo/w_distance.csv',index_col=0)
    W= df_w.values


    k = 0
    y = np.zeros(x.shape)
    uv = np.zeros((T,N*N))
    y[0] = x[0].copy()

    w_pulp = W.T.reshape(-1)

    status = np.zeros(T-1)

    gammas = gamma * np.ones(T)

##################Start of OPTIMIZATION#######################################################
    for k in range(T-1):
        for i_calc in range(100):
            A_pulp =  L.copy()
            b_pulp =np.trunc(gammas[k]*M) - (y[k] + x[k+1]-x[k])



            # 数理モデル
            m = pulp.LpProblem()

            # 変数
            uv_N = N*N
            # x_pulp = [pulp.LpVariable('x%d'%i, lowBound=0) for i in range(uv_N)]
            x_pulp = [pulp.LpVariable('x%d'%i, lowBound=0,cat='Integer') for i in range(uv_N)]


            #  目的関数
            m += pulp.lpDot(w_pulp,x_pulp) 

            # 拘束条件(Ax<=b)
            for i in range(A_pulp.shape[0]):
                m += pulp.lpDot(A_pulp[i],x_pulp)  <= b_pulp[i]


                #Build the solverModel for your preferred
            solver = pulp.PULP_CBC_CMD(maxSeconds = 30)


            status[k] = m.solve(solver)
            print(k,gammas[k])
            if status[k]==1:
                gammas[k+1] = gammas[k]
                break;
            else:
                gammas[k] = gammas[k] + 0.01

        for i in range(len(x_pulp)):
            uv[k,i] = pulp.value(x_pulp[i])


        y[k+1] = y[k] + x[k+1] - x[k] + L.dot(uv[k])
################## End of OPTIMIZATION #######################################################

    
    np.save('data_hospital_transport/u_{0}_{1:03}_{2}.npy'.format(x_type,int(gamma*100),forecast_date), uv)
    np.save('data_hospital_transport/gammas_{0}_{1:03}_{2}.npy'.format(x_type,int(gamma*100),forecast_date), gammas)


# In[10]:


gamma_list = [0.8,1.0]
# 使う条件の設定
x_type_list = ['upper','mean']
for gamma in gamma_list:
    for x_type in x_type_list:
        calc_transport(gamma,x_type,f_date)




# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




