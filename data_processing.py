import numpy as np
import pandas as pd
origin_data=pd.read_csv('full.csv')
data=origin_data[['TurbID','Day', 'Wspd', 'Wdir', 'Etmp', 'Itmp', 'Ndir', 'Pab1', 'Pab2', 'Pab3','Prtv', 'Patv']]
data['Prtv'][data['Prtv']<0]=0
data['Patv'][data['Patv']<0]=0
#data['date'] = pd.to_datetime(data['date'])
conda=((data.Patv<=0)&(data.Wspd>2.5))|(data.Pab1>89)|(data.Pab2>89)|(data.Pab3>89)
indice=np.where(~conda)
list(*indice)
indice=np.where(~conda)
data_new=data.iloc[list(*indice)]
def pre_data(df):
   #去除异常值
    for col in df.columns.tolist():
        if   col != 'TurbID'  and col != 'Day' :
            df.drop(df[(df[col] > (df[col].mean() + 4 * df[col].std()))|(df[col] < (df[col].mean() - 4 * df[col].std()))].index,inplace=True)
    return df
df1=pre_data(data_new)
dd=df1.pivot_table(index='TurbID',columns='Day',aggfunc='mean')
dd.fillna(dd.mean(),inplace=True)
## 处理Patv
Patv=dd['Patv']
Patv=Patv.reset_index()
Patv.columns=['TurbID']+[i for i in range(1,184)]
Patv_data=pd.melt(Patv,id_vars='TurbID',var_name='Day',value_name='Patv')
Wspd=dd['Wspd']
Wspd=Wspd.reset_index()
Wspd.columns=['TurbID']+[i for i in range(1,184)]
Wspd_data=pd.melt(Wspd,id_vars='TurbID',var_name='Day',value_name='Wspd')
Prtv=dd['Prtv']
Prtv=Prtv.reset_index()
Prtv.columns=['TurbID']+[i for i in range(1,184)]
Prtv_data=pd.melt(Prtv,id_vars='TurbID',var_name='Day',value_name='Prtv')
Wdir=dd['Wdir']
Wdir=Wdir.reset_index()
Wdir.columns=['TurbID']+[i for i in range(1,184)]
Wdir_data=pd.melt(Wdir,id_vars='TurbID',var_name='Day',value_name='Wdir')
Etmp=dd['Etmp']
Etmp=Etmp.reset_index()
Etmp.columns=['TurbID']+[i for i in range(1,184)]
Etmp_data=pd.melt(Etmp,id_vars='TurbID',var_name='Day',value_name='Etmp')
Ndir=dd['Ndir']
Ndir=Ndir.reset_index()
Ndir.columns=['TurbID']+[i for i in range(1,184)]
Ndir_data=pd.melt(Ndir,id_vars='TurbID',var_name='Day',value_name='Ndir')
Pab1=dd['Pab1']
Pab1=Pab1.reset_index()
Pab1.columns=['TurbID']+[i for i in range(1,184)]
Pab1_data=pd.melt(Pab1,id_vars='TurbID',var_name='Day',value_name='Pab1')
Pab2=dd['Pab2']
Pab2=Pab2.reset_index()
Pab2.columns=['TurbID']+[i for i in range(1,184)]
Pab2_data=pd.melt(Pab2,id_vars='TurbID',var_name='Day',value_name='Pab2')
Pab3=dd['Pab3']
Pab3=Pab3.reset_index()
Pab3.columns=['TurbID']+[i for i in range(1,184)]
Pab3_data=pd.melt(Pab3,id_vars='TurbID',var_name='Day',value_name='Pab3')
feature_data=pd.concat([Wdir_data['Wdir'],Etmp_data['Etmp'],Ndir_data['Ndir'],Pab1_data['Pab1'],Pab2_data['Pab2'],Pab3_data['Pab3']],axis=1)

h = 7
lag = 7
###lag1
Lag_Patv_day = [col for col in range(1, h + lag)]
Lag_day = [col for col in range(1, lag + 1)]

Patv_lag_data = Patv_data.assign(**{
    '{}_lag_{}'.format(col, l): Patv_data.groupby(['TurbID'])[col].transform(lambda x: x.shift(l,fill_value=x.iloc[0]))
    for l in Lag_Patv_day
    for col in ['Patv']
})
Wspd_lag_data = Wspd_data.assign(**{
    '{}_lag_{}'.format(col, l): Wspd_data.groupby(['TurbID'])[col].transform(lambda x: x.shift(l,fill_value=x.iloc[0]))
    for l in Lag_day
    for col in ['Wspd']
})
Prtv_lag_data = Prtv_data.assign(**{
    '{}_lag_{}'.format(col, l): Prtv_data.groupby(['TurbID'])[col].transform(lambda x: x.shift(l,fill_value=x.iloc[0]))
    for l in Lag_day
    for col in ['Prtv']
})
data_lag = pd.concat([Patv_lag_data, Wspd_lag_data.iloc[:, 2:], Prtv_lag_data.iloc[:, 2:], feature_data], axis=1)


##划分cv
cvs=[]
h=7


for i in range(15):
    cvs.append(f'cv{i+1}')
data_shot={}
data_valid_shot={}
for i in range(15):
    data_shot[f'cv{i+1}']=[i*7+1,i*7+85-7]
    data_valid_shot[f'cv{i+1}']=[i*7+78+1,i*7+85]