#Bin Generic
import pandas as pd
import numpy as np
df = pd.read_csv('D:/Bristol/DataScience/Pre-processed/for_reading.csv', parse_dates=[['bt_date', 'bt_time']]) 
df.set_index('bt_date_bt_time', inplace=True)
df = df.replace(0,np.NaN)
df_group = df.groupby(pd.TimeGrouper(level='bt_date_bt_time', freq='40S'))['BMP_TEMP','HDC_TEMP','HDC_HUM'].agg('mean')   
#df_group.dropna(inplace=True)
#df_group = df_group.to_frame().reset_index()
df_group.index.to_pydatetime()
df_group['Date']=df_group.index.strftime('%d-%m-%Y')
df_group['Time']=df_group.index.strftime('%H:%M:%S:%f')
#df_group.reset_index(['Date','Time'])
#df_group['Date'] = pd.to_datetime(df_group['bt_date_bt_time']).dt.date
#df_group['Time'] = pd.to_datetime(df_group.index).dt.time
df_group.to_csv('D:/Bristol/DataScience/Transformation/Binned_EnvSensor_Readings_40second.csv')
#print df_group[:12]

#binning and labelling electricity 

import pandas as pd
import numpy as np
df1 = pd.read_csv('D:/Bristol/DataScience/Pre-processed/for_reading_Elec.csv', parse_dates=[['bt_date', 'bt_time']]) 
df1.set_index('bt_date_bt_time', inplace=True)
df1 = df1.replace(0,np.NaN)
df_group1 = df1.groupby(pd.TimeGrouper(level='bt_date_bt_time', freq='40S'))['ELEC'].agg('mean')   
#df_group1.index = pd.MultiIndex.from_arrays([df_group1.index.date, df_group1.index.time], names=['Date','Time'])
df_group1 = df_group1.to_frame()

df_group1.index.to_pydatetime()
df_group1['Date']=df_group1.index.strftime('%d-%m-%Y')
df_group1['Time']=df_group1.index.strftime('%H:%M:%S:%f')
df_group1 = df_group1.replace(np.NaN,0)
cols = list(df_group1.columns.values)

cols = cols[-2:] + cols[:-2]
df_group1 = df_group1[cols]

df_group1['Kettle In Use'] = np.where(df_group1['ELEC'] == 0, 0, 1)

#df_group1

df_group1.to_csv('D:/Bristol/DataScience/Transformation/Binned_Labelled_Electricity_Usage.csv', header=True)


#dropping duplicates
import pandas as pd
import numpy as np
df = pd.read_csv('D:/Bristol/DataScience/Pre-processed/WearC_duplicateprocess.csv') 
df.sort_values(['bt_time', 'fd00::212:4b00:0:3'], ascending=[True, True])
df.drop_duplicates(subset='bt_time', keep='first', inplace=True)
df.to_csv('D:/Bristol/DataScience/Pre-processed/WearC_withoutduplicates.csv')

#transform wearable data after duplicate dropping
import pandas as pd
import numpy as np
df = pd.read_csv('D:/Bristol/DataScience/Pre-processed/WearC_withoutduplicates.csv', parse_dates=[['bt_date', 'bt_time']]) 
df.set_index('bt_date_bt_time', inplace=True)
df = df.replace(0,np.NaN)
df_group = df.groupby(pd.TimeGrouper(level='bt_date_bt_time', freq='40S'))['fd00::212:4b00:0:3'].agg('mean')   
#df_group.dropna(inplace=True)
df_group = df_group.to_frame()

df_group.index.to_pydatetime()
df_group['Date']=df_group.index.strftime('%d-%m-%Y')
df_group['Time']=df_group.index.strftime('%H:%M:%S:%f')
df_group = df_group.rename(columns = {"fd00::212:4b00:0:3":"Kitchen Sphere Gateway"
                               # "b8:ae:ed:78:cf:fe":"Kitchen NUC Video", 
                                #"b8:ae:ed:75:e0:24": "Hall NUC Video",
                                #"b8:ae:ed:75:61:45":"Living Room NUC Video"
                                 }) 
cols = list(df_group.columns.values)

cols = cols[-2:] + cols[:-2]
df_group = df_group[cols]
df_group['In Kitchen'] = np.where(df_group['Kitchen Sphere Gateway'] >= -70, 1, 0)

#df_group.reset_index(['Date','Time'])
#df_group['Date'] = pd.to_datetime(df_group['bt_date_bt_time']).dt.date
#df_group['Time'] = pd.to_datetime(df_group.index).dt.time
df_group.to_csv('D:/Bristol/DataScience/Transformation/Binned_WearC_noduplicates_40second.csv')
#print df_group[:12]

#PIR Trigger Processing

import pandas as pd
import numpy as np
import ast

df = pd.read_csv('D:/Bristol/DataScience/Transformation/for_reading_pir.csv')
l1=[]
#df.set_index('bt_date_bt_time', inplace=True)
df = df.replace(0,np.NaN)
df['PIR_TRIGS'] = df['PIR_TRIGS'].apply(lambda x: ast.literal_eval(x))
df1 = df['PIR_TRIGS'].apply(lambda x: pd.Series(x))
df2 =pd.concat([df['bt_date'], df['bt_time'],df['uid'],df1],axis=1)
#df2= df2.replace(np.NaN,0) #needs assignment otherwise doesnot work
#(pd.to_datetime(df2['bt_date_bt_time']))
'''df2 = df2.rename(columns = {"0":"TimeSecond 0", "1":"TimeSecond 1", "2":"TimeSecond 2", "3":"TimeSecond 3", "4":"TimeSecond 4", 
                             "5":"TimeSecond 5", "6":"TimeSecond 6","7":"TimeSecond 7", "8":"TimeSecond 8", "9":"TimeSecond 9", 
                            "10":"TimeSecond 10", "11":"TimeSecond 11", "12":"TimeSecond 12", "13":"TimeSecond 13", "14":"TimeSecond 14", 
                             "15":"TimeSecond 15", "16":"TimeSecond 16","17":"TimeSecond 17", "18":"TimeSecond 18", "19":"TimeSecond 19",
                            "20":"TimeSecond 20", "21":"TimeSecond 21", "22":"TimeSecond 22", "23":"TimeSecond 23", "24":"TimeSecond 24", 
                             "25":"TimeSecond 25", "26":"TimeSecond 26","27":"TimeSecond 27", "28":"TimeSecond 28", "29":"TimeSecond 29",  
                           "30":"TimeSecond 30"}) '''
df2.to_csv('D:/Bristol/DataScience/Transformation/IntermediatePIR_TRIG.csv')

df3 = pd.read_csv('D:/Bristol/DataScience/Transformation/IntermediatePIR_TRIG.csv', parse_dates=[['bt_date', 'bt_time']]) 
df3.rename( columns={'Unnamed: 0':'new column name'}, inplace=True )
df3 =df3.drop(columns=['new column name'])
df3=df3[df3['uid'].isin(['fd00::212:4b00:0:81','fd00::212:4b00:0:82','fd00::212:4b00:0:86','fd00::212:4b00:0:87',\
                     'fd00::212:4b00:0:84','fd00::212:4b00:0:83','fd00::212:4b00:0:80'])]
#df3=df3.replace(np.NaN, 0)
df3.uid = df3.uid.str.replace('fd00::212:4b00:0:81', 'dining room 1')
df3.uid = df3.uid.str.replace('fd00::212:4b00:0:82', 'kitchen 1')
df3.uid = df3.uid.str.replace('fd00::212:4b00:0:86', 'bathroom 1')
df3.uid = df3.uid.str.replace('fd00::212:4b00:0:87', 'staircase 1')
df3.uid = df3.uid.str.replace('fd00::212:4b00:0:84', 'bedroom 1')
df3.uid = df3.uid.str.replace('fd00::212:4b00:0:83', 'hall 1')
df3.uid = df3.uid.str.replace('fd00::212:4b00:0:80', 'living room 1')
df3.dropna(inplace=True)
df3.set_index(['bt_date_bt_time'], inplace=True, drop=True)

df3['Date']=df3.index.strftime('%d-%m-%Y')
df3['Time']=df3.index.strftime('%H:%M:%S:%f')
df3 = df3.rename(columns = {"0":"TimeSecond 0", "1":"TimeSecond 1", "2":"TimeSecond 2", "3":"TimeSecond 3", "4":"TimeSecond 4", 
                             "5":"TimeSecond 5", "6":"TimeSecond 6","7":"TimeSecond 7", "8":"TimeSecond 8", "9":"TimeSecond 9", 
                            "10":"TimeSecond 10", "11":"TimeSecond 11", "12":"TimeSecond 12", "13":"TimeSecond 13", "14":"TimeSecond 14", 
                             "15":"TimeSecond 15", "16":"TimeSecond 16","17":"TimeSecond 17", "18":"TimeSecond 18", "19":"TimeSecond 19",
                            "20":"TimeSecond 20", "21":"TimeSecond 21", "22":"TimeSecond 22", "23":"TimeSecond 23", "24":"TimeSecond 24", 
                             "25":"TimeSecond 25", "26":"TimeSecond 26","27":"TimeSecond 27", "28":"TimeSecond 28", "29":"TimeSecond 29"  
                          })
cols = list(df3.columns.values)
#print cols
cols = cols[-2:] + cols[:-2]
df3 = df3[cols] 
df3.dropna(inplace=True)
df3=df3[df3['Date'].isin(['28-03-2019'])]
#df3 = df3[['bt_date_bt_time', 'Date','Time',2,1]]
df3.sort_values(['Date', 'Time','uid'], ascending=[True, True, False])
#df3.head()
#df3.to_csv('D:/Bristol/DataScience/Transformation/PirTrig_OnlyMarch.csv')
df_group = df3.groupby(pd.TimeGrouper(level='bt_date_bt_time', freq='40S'))['0','1','2','3','4','5','6','7',\
                                              '8','9','10','11','12','13','14','15','16' ,'17','18','19','20', \
                                               '21','22','23','24','25','26','27','28','29'].agg('mean')
#df_group
df_group.to_csv('D:/Bristol/DataScience/Transformation/Binned_PirTrig_40second.csv')
df4 = pd.read_csv('D:/Bristol/DataScience/Transformation/Binned_Labelled_PIRTRIG.csv', parse_dates=[['Date', 'Time']])
df4.set_index('Date_Time', inplace=True, drop=True)
df4.to_csv('D:/Bristol/DataScience/Transformation/Binned_Labelled_PIRTRIG_final.csv')



