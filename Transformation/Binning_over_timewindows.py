import pandas as pd
import numpy as np
df = pd.read_csv('D:/Bristol/DataScience/Pre-processed/for_reading.csv', parse_dates=[['bt_date', 'bt_time']]) 
df.set_index('bt_date_bt_time', inplace=True)
df = df.replace(0,np.NaN)
df_group = df.groupby(pd.TimeGrouper(level='bt_date_bt_time', freq='1T'))['BMP_TEMP','HDC_TEMP','HDC_HUM','LT','BMP_PRES'].agg('mean')   
#df_group.dropna(inplace=True)
#df_group = df_group.to_frame().reset_index()
df_group.index.to_pydatetime()
#df_group['Date']=df_group.index.strftime('%d-%m-%Y')
#df_group['Time']=df_group.index.strftime('%H:%M:%S:%f')
#df_group.reset_index(['Date','Time'])
#df_group['Date'] = pd.to_datetime(df_group['bt_date_bt_time']).dt.date
#df_group['Time'] = pd.to_datetime(df_group.index).dt.time
df_group.to_csv('D:/Bristol/DataScience/Transformation/Binned_EnvSensor_Readings.csv')
#print df_group[:12]

#Binning Wearable A and C Code
import pandas as pd
import numpy as np
df = pd.read_csv('D:/Bristol/DataScience/Transformation/for_reading_wearC.csv', parse_dates=[['bt_date', 'bt_time']]) 
df.set_index('bt_date_bt_time', inplace=True)
df = df.replace(0,np.NaN)
df_group = df.groupby(pd.TimeGrouper(level='bt_date_bt_time', freq='40S'))['fd00::212:4b00:0:3','b8:ae:ed:78:cf:fe','b8:ae:ed:75:e0:24','b8:ae:ed:75:61:45'].agg('mean')   
#df_group.dropna(inplace=True)
#df_group = df_group.to_frame().reset_index()
df_group.index.to_pydatetime()
df_group['Date']=df_group.index.strftime('%d-%m-%Y')
df_group['Time']=df_group.index.strftime('%H:%M:%S:%f')
df_group = df_group.rename(columns = {"fd00::212:4b00:0:3":"Kitchen Sphere Gateway", 
                                "b8:ae:ed:78:cf:fe":"Kitchen NUC Video", 
                                "b8:ae:ed:75:e0:24": "Hall NUC Video",
                                "b8:ae:ed:75:61:45":"Living Room NUC Video"
                                 }) 
#df_group.reset_index(['Date','Time'])
#df_group['Date'] = pd.to_datetime(df_group['bt_date_bt_time']).dt.date
#df_group['Time'] = pd.to_datetime(df_group.index).dt.time
df_group.to_csv('D:/Bristol/DataScience/Transformation/Binned_WearC_40second.csv')
#print df_group[:12]
