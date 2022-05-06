#!/usr/bin/env python
# coding: utf-8

# In[29]:


import os
import pandas as pd
import numpy as np


# In[2]:


#import data from provided csv 
CGMData=pd.read_csv('CGMData.csv',low_memory=False,usecols=['Date','Time','Sensor Glucose (mg/dL)'])
InsulinData=pd.read_csv('InsulinData.csv',low_memory=False)


# In[3]:


#date_time_stamp, Columns B and C combined for CGMData
CGMData['date_time_stamp']=pd.to_datetime(CGMData['Date'] + ' ' + CGMData['Time'])


# In[4]:


#RemoveNaN
RemoveData=CGMData[CGMData['Sensor Glucose (mg/dL)'].isna()]['Date'].unique()
CGMData=CGMData.set_index('Date').drop(index=RemoveData).reset_index()


# In[5]:


#cgm_test=CGMData.copy()
#cgm_test=cgm_test.set_index(pd.DatetimeIndex(CGMData['date_time_stamp']))


# In[6]:


#Columns B and C combined for insulin data

InsulinData['date_time_stamp']=pd.to_datetime(InsulinData['Date'] + ' ' + InsulinData['Time'])


# In[7]:


#Find auto mode start time
auto_mode_start=InsulinData.sort_values(by='date_time_stamp',ascending=True).loc[InsulinData['Alarm']=='AUTO MODE ACTIVE PLGM OFF'].iloc[0]['date_time_stamp']
#Extract automode data
auto_mode_data=CGMData.sort_values(by='date_time_stamp',ascending=True).loc[CGMData['date_time_stamp']>=auto_mode_start]
#Extract manual mode data
manual_mode_data=CGMData.sort_values(by='date_time_stamp',ascending=True).loc[CGMData['date_time_stamp']<auto_mode_start]


# In[91]:


auto_mode_data_date_index=auto_mode_data.copy()
auto_mode_data_date_index=auto_mode_data_date_index.set_index('date_time_stamp')
#auto_mode_index_list=auto_mode_data_date_index.groupby('Date')['Sensor Glucose (mg/dL)'].count().where(lambda x:x>0.8*288).dropna().index.tolist()
auto_mode_index_list=auto_mode_data_date_index.groupby('Date')['Sensor Glucose (mg/dL)'].count().where(lambda x:x>0.5*288).dropna().index.tolist()
auto_mode_data_date_index=auto_mode_data_date_index.loc[auto_mode_data_date_index['Date'].isin(auto_mode_index_list)]


# In[92]:


print([auto_mode_index_list],[auto_mode_index_list2])
print(len(auto_mode_index_list))
print(len(auto_mode_index_list2))   
           


# In[93]:


#Auto mode: Percentage time in hyperglycemia (CGM > 180 mg/dL)
percent_time_in_hyperglycemia_daytime_automode=(auto_mode_data_date_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_data_date_index['Sensor Glucose (mg/dL)']>180].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_hyperglycemia_overnight_automode=(auto_mode_data_date_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_data_date_index['Sensor Glucose (mg/dL)']>180].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_hyperglycemia_wholeday_automode=(auto_mode_data_date_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_data_date_index['Sensor Glucose (mg/dL)']>180].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


# In[94]:


#Auto mode:  percentage of time in hyperglycemia critical (CGM > 250 mg/dL)
percent_time_in_hyperglycemia_critical_daytime_automode=(auto_mode_data_date_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_data_date_index['Sensor Glucose (mg/dL)']>250].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_hyperglycemia_critical_overnight_automode=(auto_mode_data_date_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_data_date_index['Sensor Glucose (mg/dL)']>250].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_hyperglycemia_critical_wholeday_automode=(auto_mode_data_date_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_data_date_index['Sensor Glucose (mg/dL)']>250].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


# In[95]:


#Auto mode:  percentage time in range (CGM >= 70 mg/dL and CGM <= 180 mg/dL)
percent_time_in_range_daytime_automode=(auto_mode_data_date_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(auto_mode_data_date_index['Sensor Glucose (mg/dL)']>=70) & (auto_mode_data_date_index['Sensor Glucose (mg/dL)']<=180)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_range_overnight_automode=(auto_mode_data_date_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(auto_mode_data_date_index['Sensor Glucose (mg/dL)']>=70) & (auto_mode_data_date_index['Sensor Glucose (mg/dL)']<=180)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_range_wholeday_automode=(auto_mode_data_date_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(auto_mode_data_date_index['Sensor Glucose (mg/dL)']>=70) & (auto_mode_data_date_index['Sensor Glucose (mg/dL)']<=180)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)



# In[96]:


#Auto mode:  percentage time in range secondary (CGM >= 70 mg/dL and CGM <= 150 mg/dL),
percent_time_in_range_sec_wholeday_automode=(auto_mode_data_date_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(auto_mode_data_date_index['Sensor Glucose (mg/dL)']>=70) & (auto_mode_data_date_index['Sensor Glucose (mg/dL)']<=150)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_range_sec_daytime_automode=(auto_mode_data_date_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(auto_mode_data_date_index['Sensor Glucose (mg/dL)']>=70) & (auto_mode_data_date_index['Sensor Glucose (mg/dL)']<=150)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_range_sec_overnight_automode=(auto_mode_data_date_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(auto_mode_data_date_index['Sensor Glucose (mg/dL)']>=70) & (auto_mode_data_date_index['Sensor Glucose (mg/dL)']<=150)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


# In[97]:


#Auto mode: percentage time in hypoglycemia level 1 (CGM < 70 mg/dL),
percent_time_in_hypoglycemia_L1_wholeday_automode=(auto_mode_data_date_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_data_date_index['Sensor Glucose (mg/dL)']<70].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_hypoglycemia_L1_daytime_automode=(auto_mode_data_date_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_data_date_index['Sensor Glucose (mg/dL)']<70].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_hypoglycemia_L1_overnight_automode=(auto_mode_data_date_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_data_date_index['Sensor Glucose (mg/dL)']<70].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


# In[98]:


#Auto mode: percentage time in hypoglycemia level 2 (CGM < 54 mg/dL).
percent_time_in_hypoglycemia_L2_wholeday_automode=(auto_mode_data_date_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_data_date_index['Sensor Glucose (mg/dL)']<54].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_hypoglycemia_L2_daytime_automode=(auto_mode_data_date_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_data_date_index['Sensor Glucose (mg/dL)']<54].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_hypoglycemia_L2_overnight_automode=(auto_mode_data_date_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[auto_mode_data_date_index['Sensor Glucose (mg/dL)']<54].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


# In[109]:


#Manual mode data 
manual_mode_data_index=manual_mode_data.copy()
manual_mode_data_index=manual_mode_data_index.set_index('date_time_stamp')
#manual_mode_index_list=manual_mode_data_index.groupby('Date')['Sensor Glucose (mg/dL)'].count().where(lambda x:x>0.8*288).dropna().index.tolist()
manual_mode_index_list=manual_mode_data_index.groupby('Date')['Sensor Glucose (mg/dL)'].count().where(lambda x:x>0.5*288).dropna().index.tolist()
manual_mode_data_index=manual_mode_data_index.loc[manual_mode_data_index['Date'].isin(manual_mode_index_list)]


# In[110]:


print(len(manual_mode_index_list))


# In[111]:


#Manual mode:Percentage time in hyperglycemia (CGM > 180 mg/dL),
percent_time_in_hyperglycemia_wholeday_manual=(manual_mode_data_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_data_index['Sensor Glucose (mg/dL)']>180].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_hyperglycemia_daytime_manual=(manual_mode_data_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_data_index['Sensor Glucose (mg/dL)']>180].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_hyperglycemia_overnight_manual=(manual_mode_data_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_data_index['Sensor Glucose (mg/dL)']>180].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


# In[112]:


#Manual mode:Percentage of time in hyperglycemia critical (CGM > 250 mg/dL)
percent_time_in_hyperglycemia_critical_wholeday_manual=(manual_mode_data_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_data_index['Sensor Glucose (mg/dL)']>250].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_hyperglycemia_critical_daytime_manual=(manual_mode_data_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_data_index['Sensor Glucose (mg/dL)']>250].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_hyperglycemia_critical_overnight_manual=(manual_mode_data_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_data_index['Sensor Glucose (mg/dL)']>250].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


# In[113]:


#Manual mode: percentage time in range (CGM >= 70 mg/dL and CGM <= 180 mg/dL),
percent_time_in_range_wholeday_manual=(manual_mode_data_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(manual_mode_data_index['Sensor Glucose (mg/dL)']>=70) & (manual_mode_data_index['Sensor Glucose (mg/dL)']<=180)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_range_daytime_manual=(manual_mode_data_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(manual_mode_data_index['Sensor Glucose (mg/dL)']>=70) & (manual_mode_data_index['Sensor Glucose (mg/dL)']<=180)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_range_overnight_manual=(manual_mode_data_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(manual_mode_data_index['Sensor Glucose (mg/dL)']>=70) & (manual_mode_data_index['Sensor Glucose (mg/dL)']<=180)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


# In[114]:


#Manual mode:percentage time in range secondary (CGM >= 70 mg/dL and CGM <= 150 mg/dL)
percent_time_in_range_sec_wholeday_manual=(manual_mode_data_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(manual_mode_data_index['Sensor Glucose (mg/dL)']>=70) & (manual_mode_data_index['Sensor Glucose (mg/dL)']<=150)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_range_sec_daytime_manual=(manual_mode_data_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(manual_mode_data_index['Sensor Glucose (mg/dL)']>=70) & (manual_mode_data_index['Sensor Glucose (mg/dL)']<=150)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_range_sec_overnight_manual=(manual_mode_data_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[(manual_mode_data_index['Sensor Glucose (mg/dL)']>=70) & (manual_mode_data_index['Sensor Glucose (mg/dL)']<=150)].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


# In[115]:


#Manual mode:percentage time in hypoglycemia level 1 (CGM < 70 mg/dL)
percent_time_in_hypoglycemia_L1_wholeday_manual=(manual_mode_data_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_data_index['Sensor Glucose (mg/dL)']<70].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_hypoglycemia_L1_daytime_manual=(manual_mode_data_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_data_index['Sensor Glucose (mg/dL)']<70].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_hypoglycemia_L1_overnight_manual=(manual_mode_data_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_data_index['Sensor Glucose (mg/dL)']<70].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


# In[116]:


#Manual mode:percentage time in hypoglycemia level 2 (CGM < 54 mg/dL).
percent_time_in_hypoglycemia_L2_wholeday_manual=(manual_mode_data_index.between_time('0:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_data_index['Sensor Glucose (mg/dL)']<54].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_hypoglycemia_L2_daytime_manual=(manual_mode_data_index.between_time('6:00:00','23:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_data_index['Sensor Glucose (mg/dL)']<54].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)
percent_time_in_hypoglycemia_L2_overnight_manual=(manual_mode_data_index.between_time('0:00:00','05:59:59')[['Date','Time','Sensor Glucose (mg/dL)']].loc[manual_mode_data_index['Sensor Glucose (mg/dL)']<54].groupby('Date')['Sensor Glucose (mg/dL)'].count()/288*100)


# In[117]:


#Create Result Dataframe
results_df = pd.DataFrame({'percent_time_in_hyperglycemia_overnight':[ sum(percent_time_in_hyperglycemia_overnight_manual)/len(manual_mode_index_list),sum(percent_time_in_hyperglycemia_overnight_automode)/len(auto_mode_index_list)],


'percent_time_in_hyperglycemia_critical_overnight':[ sum(percent_time_in_hyperglycemia_critical_overnight_manual)/len(manual_mode_index_list),sum(percent_time_in_hyperglycemia_critical_overnight_automode)/len(auto_mode_index_list)],


'percent_time_in_range_overnight':[ sum(percent_time_in_range_overnight_manual)/len(manual_mode_index_list),sum(percent_time_in_range_overnight_automode)/len(auto_mode_index_list)],


'percent_time_in_range_sec_overnight':[ sum(percent_time_in_range_sec_overnight_manual)/len(manual_mode_index_list),sum(percent_time_in_range_sec_overnight_automode)/len(auto_mode_index_list)],


'percent_time_in_hypoglycemia_L1_overnight':[ sum(percent_time_in_hypoglycemia_L1_overnight_manual)/len(manual_mode_index_list),sum(percent_time_in_hypoglycemia_L1_overnight_automode)/len(auto_mode_index_list)],

'percent_time_in_hypoglycemia_L2_overnight':[ sum(percent_time_in_hypoglycemia_L2_overnight_manual)/len(manual_mode_index_list),sum(percent_time_in_hypoglycemia_L2_overnight_automode)/len(auto_mode_index_list)],
'percent_time_in_hyperglycemia_daytime':[ sum(percent_time_in_hyperglycemia_daytime_manual)/len(manual_mode_index_list),sum(percent_time_in_hyperglycemia_daytime_automode)/len(auto_mode_index_list)],
'percent_time_in_hyperglycemia_critical_daytime':[ sum(percent_time_in_hyperglycemia_critical_daytime_manual)/len(manual_mode_index_list),sum(percent_time_in_hyperglycemia_critical_daytime_automode)/len(auto_mode_index_list)],
'percent_time_in_range_daytime':[ sum(percent_time_in_range_daytime_manual)/len(manual_mode_index_list),sum(percent_time_in_range_daytime_automode)/len(auto_mode_index_list)],
'percent_time_in_range_sec_daytime':[ sum(percent_time_in_range_sec_daytime_manual)/len(manual_mode_index_list),sum(percent_time_in_range_sec_daytime_automode)/len(auto_mode_index_list)],
'percent_time_in_hypoglycemia_L1_daytime':[ sum(percent_time_in_hypoglycemia_L1_daytime_manual)/len(manual_mode_index_list),sum(percent_time_in_hypoglycemia_L1_daytime_automode)/len(auto_mode_index_list)],
'percent_time_in_hypoglycemia_L2_daytime':[ sum(percent_time_in_hypoglycemia_L2_daytime_manual)/len(manual_mode_index_list),sum(percent_time_in_hypoglycemia_L2_daytime_automode)/len(auto_mode_index_list)],

                           
'percent_time_in_hyperglycemia_wholeday':[ sum(percent_time_in_hyperglycemia_wholeday_manual)/len(manual_mode_index_list),sum(percent_time_in_hyperglycemia_wholeday_automode)/len(auto_mode_index_list)],
'percent_time_in_hyperglycemia_critical_wholeday':[ sum(percent_time_in_hyperglycemia_critical_wholeday_manual)/len(manual_mode_index_list),sum(percent_time_in_hyperglycemia_critical_wholeday_automode)/len(auto_mode_index_list)],
'percent_time_in_range_wholeday':[ sum(percent_time_in_range_wholeday_manual)/len(manual_mode_index_list),sum(percent_time_in_range_wholeday_automode)/len(auto_mode_index_list)],
'percent_time_in_range_sec_wholeday':[ sum(percent_time_in_range_sec_wholeday_manual)/len(manual_mode_index_list),sum(percent_time_in_range_sec_wholeday_automode)/len(auto_mode_index_list)],
'percent_time_in_hypoglycemia_L1_wholeday':[ sum(percent_time_in_hypoglycemia_L1_wholeday_manual)/len(manual_mode_index_list),sum(percent_time_in_hypoglycemia_L1_wholeday_automode)/len(auto_mode_index_list)],
'percent_time_in_hypoglycemia_L2_wholeday':[ sum(percent_time_in_hypoglycemia_L2_wholeday_manual)/len(manual_mode_index_list),sum(percent_time_in_hypoglycemia_L2_wholeday_automode)/len(auto_mode_index_list)]
                    
                          
},
                          index=['manual_mode','auto_mode'])


# In[118]:


results_df.to_csv('Results.csv', index = False, header=False)


# In[ ]:




