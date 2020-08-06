#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import yfinance as yf
from nsepy import get_history
from datetime import datetime
import matplotlib.pyplot as plt
from nsepy import get_index_pe_history
from nsetools import Nse
nse=Nse()
print(nse)
from nsepy.symbols import get_symbol_list


# In[9]:


codes=nse.get_stock_codes()
codes=codes.keys()
codes=codes-set(['SYMBOL'])


# In[2]:


start_cp=datetime(2014,9,30)
end_cp=datetime(2014,9,30)


# In[6]:


stock_cp=get_history(symbol='HDFCBANK',start=start_cp,end=end_cp)


# In[10]:


for i in codes:
    df_cp=get_history(symbol=i,start=start_cp,end=end_cp)
    stock_cp=stock_cp.append(df_cp,sort=False)


# # Calculating return at various confidence in 1st Year (01-10-2014 to 30-09-2015)

# In[3]:


start_sp_1=datetime(2014,10,1)
end_sp_1=datetime(2015,9,30)


# In[11]:


sp_1=get_history(symbol='HDFCBANK',start=start_sp_1,end=end_sp_1)


# In[12]:


for i in codes:
    df_sp_1=get_history(symbol=i,start=start_sp_1,end=end_sp_1)
    sp_1=sp_1.append(df_sp_1,sort=False)


# In[14]:


returns_2014_2015=pd.DataFrame({'Symbol':'HDFCBANK','Minimum_Price':sp_1[sp_1['Symbol']=='HDFCBANK'].Close.describe()['min'],
                                '25 percentile':sp_1[sp_1['Symbol']=='HDFCBANK'].Close.describe()['25%'],
                               '50 percentile':sp_1[sp_1['Symbol']=='HDFCBANK'].Close.describe()['50%'],
                               '75 percentile':sp_1[sp_1['Symbol']=='HDFCBANK'].Close.describe()['75%']},index=[0])


# In[15]:


for i in codes:
    df_1=pd.DataFrame({'Symbol':i,'Minimum_Price':sp_1[sp_1['Symbol']==i].Close.describe()['min'],
                                '25 percentile':sp_1[sp_1['Symbol']==i].Close.describe()['25%'],
                               '50 percentile':sp_1[sp_1['Symbol']==i].Close.describe()['50%'],
                               '75 percentile':sp_1[sp_1['Symbol']==i].Close.describe()['75%']},index=[1])
    returns_2014_2015=returns_2014_2015.append(df_1,sort=False)


# In[16]:


returns_2014_2015=returns_2014_2015.merge(stock_cp,on='Symbol',how='outer')


# In[17]:


returns_2014_2015['Min_return']=((returns_2014_2015['Minimum_Price']/returns_2014_2015['VWAP'])-1)*100


# In[18]:


returns_2014_2015['25pct_return']=((returns_2014_2015['25 percentile']/returns_2014_2015['VWAP'])-1)*100


# In[19]:


returns_2014_2015['50pct_return']=((returns_2014_2015['50 percentile']/returns_2014_2015['VWAP'])-1)*100


# In[20]:


returns_2014_2015['75pct_return']=((returns_2014_2015['75 percentile']/returns_2014_2015['VWAP'])-1)*100


# In[22]:


returns_2014_2015['min_return_cat']=pd.cut(returns_2014_2015['Min_return'],bins=[-200,0,10,20,30,40,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[24]:


returns_2014_2015['25pct_return_cat']=pd.cut(returns_2014_2015['25 percentile'],bins=[-200,0,10,20,30,40,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[25]:


returns_2014_2015['50pct_return_cat']=pd.cut(returns_2014_2015['50 percentile'],bins=[-200,0,10,20,30,40,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[26]:


returns_2014_2015['75pct_return_cat']=pd.cut(returns_2014_2015['75 percentile'],bins=[-200,0,10,20,30,40,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[40]:


features=['Symbol', 'Minimum_Price', '25 percentile', '50 percentile',
       '75 percentile','VWAP','Min_return', '25pct_return', '50pct_return',
       '75pct_return', 'min_return_cat', '25pct_return_cat',
       '50pct_return_cat', '75pct_return_cat']


# In[42]:


return_2014_15=returns_2014_2015[features]


# In[46]:


return_2014_15=return_2014_15.dropna()


# In[50]:


return_2014_15.to_csv(r'D:\nse data\return_2014_15.csv',index=False,header=True)


# In[57]:


return_2014_15['25pct_return_cat'].value_counts()


# In[128]:


returns_10_1=return_2014_15[return_2014_15['25pct_return']>=10]


# # Summary of returns of 1st Year (01-10-2014 to 30-09-2015)

# In[72]:


import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# # Categories : 
# 1) Loss : Negative Return
# 2) Very Low : 0-10% Return
#  3) Low: 10-20% Return
#  4) Fair: 20-30% Return
#  5)  High: 30-40% Return
#   6) Very High : Above 40% Return 

# In[66]:


plt.hist(return_2014_15['min_return_cat'])


# In[71]:


plt.hist(return_2014_15['25pct_return_cat'])


# In[68]:


plt.hist(return_2014_15['50pct_return_cat'])


# In[69]:


plt.hist(return_2014_15['75pct_return_cat'])


# # Calculating return at various confidence in 2nd  Year (01-10-2015 to 30-09-2016)

# In[74]:


start_sp_2=datetime(2015,10,1)
end_sp_2=datetime(2016,9,30)


# In[75]:


sp_2=get_history(symbol='HDFCBANK',start=start_sp_2,end=end_sp_2)


# In[76]:


for i in codes:
    df_sp_2=get_history(symbol=i,start=start_sp_2,end=end_sp_2)
    sp_2=sp_2.append(df_sp_2,sort=False)


# In[78]:


returns_2015_2016=pd.DataFrame({'Symbol':'HDFCBANK','Minimum_Price':sp_2[sp_2['Symbol']=='HDFCBANK'].Close.describe()['min'],
                                '25 percentile':sp_2[sp_2['Symbol']=='HDFCBANK'].Close.describe()['25%'],
                               '50 percentile':sp_2[sp_2['Symbol']=='HDFCBANK'].Close.describe()['50%'],
                               '75 percentile':sp_2[sp_2['Symbol']=='HDFCBANK'].Close.describe()['75%']},index=[0])


# In[79]:


for i in codes:
    df_2=pd.DataFrame({'Symbol':i,'Minimum_Price':sp_2[sp_2['Symbol']==i].Close.describe()['min'],
                                '25 percentile':sp_2[sp_2['Symbol']==i].Close.describe()['25%'],
                               '50 percentile':sp_2[sp_2['Symbol']==i].Close.describe()['50%'],
                               '75 percentile':sp_2[sp_2['Symbol']==i].Close.describe()['75%']},index=[1])
    returns_2015_2016=returns_2015_2016.append(df_2,sort=False)
    


# In[80]:


returns_2015_2016=returns_2015_2016.merge(stock_cp,on='Symbol',how='outer')


# In[82]:


returns_2015_2016.columns


# In[85]:


features_2015_16=['Symbol', 'Minimum_Price', '25 percentile', '50 percentile',
       '75 percentile']


# In[86]:


returns_2015_16=returns_2015_2016[features_2015_16]


# In[87]:


returns_2015_16=returns_2015_16.merge(stock_cp,on='Symbol',how='outer')


# In[89]:


returns_2015_16.columns


# In[90]:


code=['Symbol', 'Minimum_Price', '25 percentile', '50 percentile',
       '75 percentile','VWAP']


# In[91]:


returns_2015_16=returns_2015_16[code]


# In[93]:


returns_2015_16=returns_2015_16.dropna()


# In[96]:


returns_2015_2016['Min_return']=((returns_2015_2016['Minimum_Price']/returns_2015_2016['VWAP'])-1)*100


# In[97]:


returns_2015_2016['25pct_return']=((returns_2015_2016['25 percentile']/returns_2015_2016['VWAP'])-1)*100


# In[98]:


returns_2015_2016['50pct_return']=((returns_2015_2016['50 percentile']/returns_2015_2016['VWAP'])-1)*100


# In[99]:


returns_2015_2016['75pct_return']=((returns_2015_2016['75 percentile']/returns_2015_2016['VWAP'])-1)*100


# In[100]:


returns_2015_2016['min_return_cat_2']=pd.cut(returns_2015_2016['Min_return'],bins=[-200,0,20,40,60,80,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[101]:


returns_2015_2016['25pct_return_cat_2']=pd.cut(returns_2015_2016['25pct_return'],bins=[-200,0,20,40,60,80,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[102]:


returns_2015_2016['50pct_return_cat_2']=pd.cut(returns_2015_2016['50pct_return'],bins=[-200,0,20,40,60,80,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[103]:


returns_2015_2016['75pct_return_cat_2']=pd.cut(returns_2015_2016['75pct_return'],bins=[-200,0,20,40,60,80,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[105]:


returns_2015_2016=returns_2015_2016.dropna()


# In[111]:


returns_2015_2016['50pct_return_cat_2'].value_counts()


# # Summary of returns of 2nd  Year (01-10-2015 to 30-09-2016)

# # Distribution of return considering Minimum Closing prices of the stocks in 2nd year(Almost 100% of the time returns were above the same)

# In[113]:


plt.hist(returns_2015_2016['min_return_cat_2'])


# # Distribution of return considering 25 percentile Closing prices of the stock in 2nd year(75% of the time returns were above the same)

# In[114]:


plt.hist(returns_2015_2016['25pct_return_cat_2'])


# # Distribution of return considering 50 percentile Closing price of the stock in 2nd year(50% of the time returns were above the same)

# In[115]:


plt.hist(returns_2015_2016['50pct_return_cat_2'])


# # Distribution of return considering 75 percentile Closing price of the stock in 2nd year(25% of the time returns were above the same)

# In[116]:


plt.hist(returns_2015_2016['75pct_return_cat_2'])


# In[127]:


returns_20_2=returns_2015_2016[returns_2015_2016['25pct_return']>20]


# In[130]:


combine_1_2=returns_20_2.merge(returns_10_1,on='Symbol',how='outer')


# In[134]:


combine_1_2_25pct=combine_1_2.dropna()


# # Calculating return at various confidence in 3rd  Year (01-10-2016 to 30-09-2017)

# In[135]:


start_sp_3=datetime(2016,10,1)
end_sp_3=datetime(2017,9,30)


# In[136]:


sp_3=get_history(symbol='HDFCBANK',start=start_sp_3,end=end_sp_3)


# In[141]:


for i in codes:
    df_sp_3=get_history(symbol=i,start=start_sp_3,end=end_sp_3)
    sp_3=sp_3.append(df_sp_3,sort=False)


# In[142]:


returns_2016_2017=pd.DataFrame({'Symbol':'HDFCBANK','Minimum_Price_3':sp_3[sp_3['Symbol']=='HDFCBANK'].Close.describe()['min'],
                                '25 percentile_3':sp_3[sp_3['Symbol']=='HDFCBANK'].Close.describe()['25%'],
                               '50 percentile_3':sp_3[sp_3['Symbol']=='HDFCBANK'].Close.describe()['50%'],
                               '75 percentile_3':sp_3[sp_3['Symbol']=='HDFCBANK'].Close.describe()['75%']},index=[0])


# In[143]:


for i in codes:
    df_3=pd.DataFrame({'Symbol':i,'Minimum_Price_3':sp_3[sp_3['Symbol']==i].Close.describe()['min'],
                                '25 percentile_3':sp_3[sp_3['Symbol']==i].Close.describe()['25%'],
                               '50 percentile_3':sp_3[sp_3['Symbol']==i].Close.describe()['50%'],
                               '75 percentile_3':sp_3[sp_3['Symbol']==i].Close.describe()['75%']},index=[1])
    returns_2016_2017=returns_2016_2017.append(df_3,sort=False)
    


# In[144]:


returns_2016_2017.columns


# In[148]:


returns_2016_2017=returns_2016_2017.merge(stock_cp,on='Symbol',how='outer')


# In[149]:


returns_2016_2017.columns


# In[150]:


features_3=['Symbol', 'Minimum_Price_3', '25 percentile_3', '50 percentile_3',
       '75 percentile_3','VWAP']


# In[151]:


returns_2016_2017=returns_2016_2017[features_3]


# In[153]:


returns_2016_2017=returns_2016_2017.dropna()


# In[155]:


returns_2016_2017['Min_return_3']=((returns_2016_2017['Minimum_Price_3']/returns_2016_2017['VWAP'])-1)*100


# In[156]:


returns_2016_2017['25pct_return_3']=((returns_2016_2017['25 percentile_3']/returns_2016_2017['VWAP'])-1)*100


# In[157]:


returns_2016_2017['50pct_return_3']=((returns_2016_2017['50 percentile_3']/returns_2016_2017['VWAP'])-1)*100


# In[158]:


returns_2016_2017['75pct_return_3']=((returns_2016_2017['75 percentile_3']/returns_2016_2017['VWAP'])-1)*100


# In[167]:


returns_2016_2017['min_return_cat_3']=pd.cut(returns_2016_2017['Min_return_3'],bins=[-200,0,30,60,90,120,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[166]:


returns_2016_2017['25pct_return_cat_3']=pd.cut(returns_2016_2017['25pct_return_3'],bins=[-200,0,30,60,90,120,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[168]:


returns_2016_2017['50pct_return_cat_3']=pd.cut(returns_2016_2017['50pct_return_3'],bins=[-200,0,30,60,90,120,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[169]:


returns_2016_2017['75pct_return_cat_3']=pd.cut(returns_2016_2017['75pct_return_3'],bins=[-200,0,30,60,90,120,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[171]:


returns_2016_2017.to_csv(r'D:\nse data\returns_2016_2017.csv',index=False,header=True)


# In[172]:


returns_2015_2016.columns


# In[174]:


returns_2015_2016=returns_2015_2016.drop(['25pct_return_cat_3', '50pct_return_cat_3', '75pct_return_cat_3'],axis=1)


# In[176]:


returns_2015_2016=returns_2015_2016.drop('min_return_cat_3',axis=1)


# In[192]:


returns_2016_2017.min_return_cat_3.value_counts()


# In[185]:


returns_2016_2017=returns_2016_2017.dropna()


# # Summary of returns of 3rd  Year (01-10-2016 to 30-09-2017)

# # Distribution of return considering minimum Closing price of the stock in 3rd year(minimum return in this year. All other returns were above the same)

# In[187]:


plt.hist(returns_2016_2017['min_return_cat_3'])


# # Distribution of return considering 25 percentile Closing price of the stock in 3rd year(75% of the time all other retuns were above the same)

# In[229]:


plt.hist(returns_2016_2017['25pct_return_cat_3'])


# # Distribution of return considering 50 percentile Closing price of the stock in 3rd year(50% of the time in this year all other returns were above the same)

# In[189]:


plt.hist(returns_2016_2017['50pct_return_cat_3'])


# # Distribution of return considering 75 percentile Closing price of the stock in 3rd year(25% of the time returns were above the same)

# In[190]:


plt.hist(returns_2016_2017['75pct_return_cat_3'])


# # Calculating return at various confidence in 4th  Year (01-10-2017 to 30-09-2018)

# In[193]:


start_sp_4=datetime(2017,10,1)
end_sp_4=datetime(2018,9,30)


# In[196]:


sp_4=get_history(symbol='HDFCBANK',start=start_sp_4,end=end_sp_4)


# In[197]:


for i in codes:
    df_sp_4=get_history(symbol=i,start=start_sp_4,end=end_sp_4)
    sp_4=sp_4.append(df_sp_4,sort=False)


# In[198]:


returns_2017_2018=pd.DataFrame({'Symbol':'HDFCBANK','Minimum_Price_4':sp_4[sp_4['Symbol']=='HDFCBANK'].Close.describe()['min'],
                                '25 percentile_4':sp_4[sp_4['Symbol']=='HDFCBANK'].Close.describe()['25%'],
                               '50 percentile_4':sp_4[sp_4['Symbol']=='HDFCBANK'].Close.describe()['50%'],
                               '75 percentile_4':sp_4[sp_4['Symbol']=='HDFCBANK'].Close.describe()['75%']},index=[0])


# In[199]:


for i in codes:
    df_4=pd.DataFrame({'Symbol':i,'Minimum_Price_4':sp_4[sp_4['Symbol']==i].Close.describe()['min'],
                                '25 percentile_4':sp_4[sp_4['Symbol']==i].Close.describe()['25%'],
                               '50 percentile_4':sp_4[sp_4['Symbol']==i].Close.describe()['50%'],
                               '75 percentile_4':sp_4[sp_4['Symbol']==i].Close.describe()['75%']},index=[1])
    returns_2017_2018=returns_2017_2018.append(df_4,sort=False)
    


# In[200]:


returns_2017_2018=returns_2017_2018.merge(stock_cp,on='Symbol',how='outer')


# In[201]:


features_4=['Symbol', 'Minimum_Price_4', '25 percentile_4', '50 percentile_4',
       '75 percentile_4','VWAP']


# In[202]:


returns_2017_2018=returns_2017_2018[features_4]


# In[203]:


returns_2017_2018=returns_2017_2018.dropna()


# In[204]:


returns_2017_2018['Min_return_4']=((returns_2017_2018['Minimum_Price_4']/returns_2017_2018['VWAP'])-1)*100


# In[205]:


returns_2017_2018['25pct_return_4']=((returns_2017_2018['25 percentile_4']/returns_2017_2018['VWAP'])-1)*100


# In[206]:


returns_2017_2018['50pct_return_4']=((returns_2017_2018['50 percentile_4']/returns_2017_2018['VWAP'])-1)*100


# In[207]:


returns_2017_2018['75pct_return_4']=((returns_2017_2018['75 percentile_4']/returns_2017_2018['VWAP'])-1)*100


# In[208]:


returns_2017_2018['min_return_cat_4']=pd.cut(returns_2017_2018['Min_return_4'],bins=[-200,0,40,80,120,160,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[209]:


returns_2017_2018['25pct_return_cat_4']=pd.cut(returns_2017_2018['25pct_return_4'],bins=[-200,0,40,80,120,160,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[210]:


returns_2017_2018['50pct_return_cat_4']=pd.cut(returns_2017_2018['50pct_return_4'],bins=[-200,0,40,80,120,160,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[211]:


returns_2017_2018['75pct_return_cat_4']=pd.cut(returns_2017_2018['75pct_return_4'],bins=[-200,0,40,80,120,160,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[212]:


returns_2017_2018.to_csv(r'D:\nse data\returns_2017_2018.csv',index=False,header=True)


# In[213]:


returns_2017_2018=returns_2017_2018.dropna()


# # Summary of returns of 4th  Year (01-10-2017 to 30-09-2018)

# # Distribution of return considering minimum Closing price of the stock in 4th year(0% of the time returns were below and 100% of the time  retuns were above the same)

# In[214]:


plt.hist(returns_2017_2018['min_return_cat_4'])


# # Distribution of return considering 25 percentile Closing prices of the stock in 4th year(25% of the time returns were below and 75% of the time  retuns were above the same)

# In[215]:


plt.hist(returns_2017_2018['25pct_return_cat_4'])


# # Distribution of return considering 50 percentile Closing prices of the stock in 4th year(50% of the time returns were below and 50% of the time  retuns were above the same)

# In[216]:


plt.hist(returns_2017_2018['50pct_return_cat_4'])


# # Distribution of return considering 75 percentile Closing prices of the stock in 4th year(75% of the time returns were below and 25% of the time  retuns were above the same)

# In[217]:


plt.hist(returns_2017_2018['75pct_return_cat_4'])


# # Calculating return at various confidence in 5th  Year (01-10-2018 to 30-09-2019)

# In[219]:


start_sp_5=datetime(2018,10,1)
end_sp_5=datetime(2019,9,30)


# In[222]:


sp_5=get_history(symbol='HDFCBANK',start=start_sp_5,end=end_sp_5)


# In[223]:


for i in codes:
    df_sp_5=get_history(symbol=i,start=start_sp_5,end=end_sp_5)
    sp_5=sp_5.append(df_sp_5,sort=False)


# In[224]:


returns_2018_2019=pd.DataFrame({'Symbol':'HDFCBANK','Minimum_Price_5':sp_5[sp_5['Symbol']=='HDFCBANK'].Close.describe()['min'],
                                '25 percentile_5':sp_5[sp_5['Symbol']=='HDFCBANK'].Close.describe()['25%'],
                               '50 percentile_5':sp_5[sp_5['Symbol']=='HDFCBANK'].Close.describe()['50%'],
                               '75 percentile_5':sp_5[sp_5['Symbol']=='HDFCBANK'].Close.describe()['75%']},index=[0])


# In[225]:


for i in codes:
    df_5=pd.DataFrame({'Symbol':i,'Minimum_Price_5':sp_5[sp_5['Symbol']==i].Close.describe()['min'],
                                '25 percentile_5':sp_5[sp_5['Symbol']==i].Close.describe()['25%'],
                               '50 percentile_5':sp_5[sp_5['Symbol']==i].Close.describe()['50%'],
                               '75 percentile_5':sp_5[sp_5['Symbol']==i].Close.describe()['75%']},index=[1])
    returns_2018_2019=returns_2018_2019.append(df_5,sort=False)
    


# In[226]:


returns_2018_2019=returns_2018_2019.merge(stock_cp,on='Symbol',how='outer')


# In[227]:


features_5=['Symbol', 'Minimum_Price_5', '25 percentile_5', '50 percentile_5',
       '75 percentile_5','VWAP']


# In[230]:


returns_2018_2019=returns_2018_2019[features_5]


# In[231]:


returns_2018_2019=returns_2018_2019.dropna()


# In[232]:


returns_2018_2019['Min_return_5']=((returns_2018_2019['Minimum_Price_5']/returns_2018_2019['VWAP'])-1)*100


# In[233]:


returns_2018_2019['25pct_return_5']=((returns_2018_2019['25 percentile_5']/returns_2018_2019['VWAP'])-1)*100


# In[234]:


returns_2018_2019['50pct_return_5']=((returns_2018_2019['50 percentile_5']/returns_2018_2019['VWAP'])-1)*100


# In[235]:


returns_2018_2019['75pct_return_5']=((returns_2018_2019['75 percentile_5']/returns_2018_2019['VWAP'])-1)*100


# In[236]:


returns_2018_2019['min_return_cat_5']=pd.cut(returns_2018_2019['Min_return_5'],bins=[-200,0,50,100,150,200,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[237]:


returns_2018_2019['25pct_return_cat_5']=pd.cut(returns_2018_2019['25pct_return_5'],bins=[-200,0,50,100,150,200,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[238]:


returns_2018_2019['50pct_return_cat_5']=pd.cut(returns_2018_2019['50pct_return_5'],bins=[-200,0,50,100,150,200,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[239]:


returns_2018_2019['75pct_return_cat_5']=pd.cut(returns_2018_2019['75pct_return_5'],bins=[-200,0,50,100,150,200,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[240]:


returns_2018_2019.to_csv(r'D:\nse data\returns_2018_2019.csv',index=False,header=True)


# In[241]:


returns_2018_2019=returns_2018_2019.dropna()


# # Summary of returns of 5th  Year (01-10-2018 to 30-09-2019)

# # Distribution of return considering minimum Closing price of the stock in that year(0% of the time returns were below and 100% of the time  retuns were above the same)

# In[242]:


plt.hist(returns_2018_2019['min_return_cat_5'])


# # Distribution of return considering 25 percentile Closing prices of the stock in 5th year(25% of the time returns were below and 75% of the time  retuns were above the same)

# In[243]:


plt.hist(returns_2018_2019['25pct_return_cat_5'])


# # Distribution of return considering 50 percentile Closing prices of the stock in 5th year(50% of the time returns were below and 50% of the time  retuns were above the same)

# In[244]:


plt.hist(returns_2018_2019['50pct_return_cat_5'])


# # Distribution of return considering 75 percentile Closing prices of the stock in 5th year(75% of the time returns were below and 25% of the time  retuns were above the same)

# In[245]:


plt.hist(returns_2018_2019['75pct_return_cat_5'])


# # Calculating return at various confidence in 6th  Year (01-10-2019 to 31-03-2020)

# In[246]:


start_sp_6=datetime(2019,10,1)
end_sp_6=datetime(2020,3,31)


# In[249]:


sp_6=get_history(symbol='HDFCBANK',start=start_sp_6,end=end_sp_6)


# In[250]:


for i in codes:
    df_sp_6=get_history(symbol=i,start=start_sp_6,end=end_sp_6)
    sp_6=sp_6.append(df_sp_6,sort=False)


# In[251]:


returns_2019_2020=pd.DataFrame({'Symbol':'HDFCBANK','Minimum_Price_6':sp_6[sp_6['Symbol']=='HDFCBANK'].Close.describe()['min'],
                                '25 percentile_6':sp_6[sp_6['Symbol']=='HDFCBANK'].Close.describe()['25%'],
                               '50 percentile_6':sp_6[sp_6['Symbol']=='HDFCBANK'].Close.describe()['50%'],
                               '75 percentile_6':sp_6[sp_6['Symbol']=='HDFCBANK'].Close.describe()['75%']},index=[0])


# In[252]:


for i in codes:
    df_6=pd.DataFrame({'Symbol':i,'Minimum_Price_6':sp_6[sp_6['Symbol']==i].Close.describe()['min'],
                                '25 percentile_6':sp_6[sp_6['Symbol']==i].Close.describe()['25%'],
                               '50 percentile_6':sp_6[sp_6['Symbol']==i].Close.describe()['50%'],
                               '75 percentile_6':sp_6[sp_6['Symbol']==i].Close.describe()['75%']},index=[1])
    returns_2019_2020=returns_2019_2020.append(df_6,sort=False)
    


# In[253]:


returns_2019_2020=returns_2019_2020.merge(stock_cp,on='Symbol',how='outer')


# In[254]:


features_6=['Symbol', 'Minimum_Price_6', '25 percentile_6', '50 percentile_6',
       '75 percentile_6','VWAP']


# In[255]:


returns_2019_2020=returns_2019_2020[features_6]


# In[256]:


returns_2019_2020=returns_2019_2020.dropna()


# In[257]:


returns_2019_2020['Min_return_6']=((returns_2019_2020['Minimum_Price_6']/returns_2019_2020['VWAP'])-1)*100


# In[258]:


returns_2019_2020['25pct_return_6']=((returns_2019_2020['25 percentile_6']/returns_2019_2020['VWAP'])-1)*100


# In[259]:


returns_2019_2020['50pct_return_6']=((returns_2019_2020['50 percentile_6']/returns_2019_2020['VWAP'])-1)*100


# In[260]:


returns_2019_2020['75pct_return_6']=((returns_2019_2020['75 percentile_6']/returns_2019_2020['VWAP'])-1)*100


# In[261]:


returns_2019_2020['min_return_cat_6']=pd.cut(returns_2019_2020['Min_return_6'],bins=[-200,0,55,110,165,220,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[262]:


returns_2019_2020['25pct_return_cat_6']=pd.cut(returns_2019_2020['25pct_return_6'],bins=[-200,0,55,110,165,220,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[263]:


returns_2019_2020['50pct_return_cat_6']=pd.cut(returns_2019_2020['50pct_return_6'],bins=[-200,0,55,110,165,220,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[264]:


returns_2019_2020['75pct_return_cat_6']=pd.cut(returns_2019_2020['75pct_return_6'],bins=[-200,0,55,110,165,220,1000],
                                              labels=['loss','very low','low','fair','high','very high'],include_lowest=True)


# In[265]:


returns_2019_2020=returns_2019_2020.dropna()


# In[266]:


returns_2019_2020.to_csv(r'D:\nse data\returns_2019_2020.csv',index=False,header=True)


# # Summary of returns of 6th  Year (01-10-2019 to 31-03-2020)

# # Distribution of return considering minimum Closing prices of the stock in 6th year(0% of the time returns were below and 100% of the time retuns were above the same)

# In[267]:


plt.hist(returns_2019_2020['min_return_cat_6'])


# # Distribution of return considering 25 percentile Closing prices of the stock in 6th year(25% of the time returns were below and 75% of the time  retuns were above the same)

# In[268]:


plt.hist(returns_2019_2020['25pct_return_cat_6'])


# # Distribution of return considering 50 percentile Closing prices of the stock in 6th year(50% of the time returns were below and 50% of the time  retuns were above the same)

# In[269]:


plt.hist(returns_2019_2020['50pct_return_cat_6'])


# # Distribution of return considering 75 percentile Closing prices of the stock in 6th year(75% of the time returns were below and 25% of the time  retuns were above the same)

# In[270]:


plt.hist(returns_2019_2020['75pct_return_cat_6'])


# # Stocks in very high category from 2nd year to 6th year

# In[288]:


very_high_2019_20_min=returns_2019_2020[returns_2019_2020['min_return_cat_6']=='very high']


# In[289]:


very_high_2018_19_min=returns_2018_2019[returns_2018_2019['min_return_cat_5']=='very high']


# In[290]:


very_high_2017_18_min=returns_2017_2018[returns_2017_2018['min_return_cat_4']=='very high']


# In[291]:


very_high_2016_17_min=returns_2016_2017[returns_2016_2017['min_return_cat_3']=='very high']


# In[293]:


very_high_2015_16_min=returns_2015_2016[returns_2015_2016['min_return_cat_2']=='very high']


# In[297]:


very_high_18_20=very_high_2019_20_min.merge(very_high_2018_19_min,on='Symbol',how='outer')


# In[299]:


very_high_18_20=very_high_18_20.dropna()


# In[301]:


very_high_combined_min=very_high_18_20.merge(very_high_2017_18_min,on='Symbol',how='outer')


# In[303]:


very_high_combined_min=very_high_combined_min.dropna()


# In[305]:


very_high_combined_min=very_high_combined_min.merge(very_high_2016_17_min,on='Symbol',how='outer')


# In[309]:


very_high_combined_min=very_high_combined_min.dropna()


# In[311]:


very_high_combined_min=very_high_combined_min.merge(very_high_2015_16_min,on='Symbol',how='outer')


# In[314]:


very_high_combined_min=very_high_combined_min.dropna()


# In[317]:


very_high_combined_min


# In[320]:


very_high_combined_min.to_csv(r'D:\nse data\very_high_combined_min.csv',index=False,header=True)


# # Stocks in  very high category from 2nd year to 6th year(75% probability)

# In[374]:


very_high_2019_20_25pct=returns_2019_2020[returns_2019_2020['25pct_return_cat_6']=='very high']


# In[375]:


very_high_2018_19_25pct=returns_2018_2019[returns_2018_2019['25pct_return_cat_5']=='very high']


# In[376]:


very_high_2017_18_25pct=returns_2017_2018[returns_2017_2018['25pct_return_cat_4']=='very high']


# In[377]:


very_high_2016_17_25pct=returns_2016_2017[returns_2016_2017['25pct_return_cat_3']=='very high']


# In[378]:


very_high_2015_16_25pct=returns_2015_2016[returns_2015_2016['25pct_return_cat_2']=='very high']


# In[379]:


combined_high=very_high_2019_20_25pct.merge(very_high_2018_19_25pct,on='Symbol',how='outer')


# In[380]:


combined_high=combined_high.merge(very_high_2017_18_25pct,on='Symbol',how='outer')


# In[381]:


combined_high=combined_high.merge(very_high_2016_17_25pct,on='Symbol',how='outer')


# In[382]:


combined_high=combined_high.merge(very_high_2015_16_25pct,on='Symbol',how='outer')


# In[383]:


combined_high=combined_high.dropna()


# In[400]:


code=['NILKAMAL','HARITASEAT','RAJESHEXPO','CANTABIL','GMBREW','DALMIASUG','ASTEC','ELECTHERM']


# In[405]:


code_1=high_2019_20_25pct.Symbol


# In[413]:


start_1=datetime(2016,10,2)
end_1=datetime(2016,10,6)


# In[345]:


high_2019_20_min.to_csv(r'D:\nse data\high_2019_20_min.csv',index=False,header=True)


# In[346]:


very_high_2019_20_min.to_csv(r'D:\nse data\very_high_2019_20_min.csv',index=False,header=True)


# In[359]:


combined=high_2019_20_min.merge(high_2018_19_min,on='Symbol',how='outer')


# In[411]:


returns_2019_2020[returns_2019_2020['75pct_return_cat_6']=='low'].head(25).Symbol


# In[ ]:




