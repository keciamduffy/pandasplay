# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

#highlights in red if there were no changes in impressions values
def highlight_nochange(s,threshold,column):
    nochange = pd.Series(data=False, index=s.index)
    nochange[column] = s.loc[column] = threshold

    return ['' if nochange.any() else 'background-color: black' for v in nochange]




#read in files
dfyesterday = pd.read_csv(r'C:\Users\kecia\kellyads\campaignsprev.csv')
dftoday = pd.read_csv(r'C:\Users\kecia\kellyads\campaigns.csv')

#declare empty pandas frame for holding the final data
dfcombined=pd.DataFrame()

#get records with running ads
dfyesterdayrun=dfyesterday.loc[dfyesterday['Status'].isin(['Running'])]
dftodayrun=dftoday.loc[dftoday['Status'].isin(['Running'])]
dfyesterdayrun

#for each campaign from today, check to see if the Impressions column has changed
for index, row in dftodayrun.iterrows():
    try:
         oldImp=(dfyesterdayrun.loc[dfyesterdayrun['Campaign Name']==row['Campaign Name']]['Impressions']).values[0]
         if row['Impressions'] != '-':
             Imptoday=(int(((row['Impressions'].replace(',','')))))
             Impyest=int(oldImp.replace(',',''))
             Impdiff = Imptoday-Impyest
             
             #Net profit = (.7*Total sales)-Spend
             #Profit/click=(.7*totalsales-Spend)/clicks)
             ##if no change highlight the data in red and the Start Date, budget, spend, impressions, clicks,Total Sales
             if Impdiff ==0:
                netprofit = (.7*float(row['Total Sales']))-float(row['Spend'])
                profitclick = netprofit/int(row['Clicks'].replace(',',''))
                dfcombined=dfcombined.append({'Change':'No','Campaign Name':row['Campaign Name'],'Start Date':row['Start Date'],'Budget':row['Budget'],
                                             'Spend':row['Spend'],'Impressions':row['Impressions'],
                                             'Clicks':row['Clicks'],'Total Sales':row['Total Sales'],
                                             'Net Profit':netprofit,'Profit/click':profitclick},ignore_index=True)
             else: 
                yesterdayspend=(dfyesterdayrun.loc[dfyesterdayrun['Campaign Name']==row['Campaign Name']]['Spend']).values[0]
                yesterdaybudget=(dfyesterdayrun.loc[dfyesterdayrun['Campaign Name']==row['Campaign Name']]['Budget']).values[0]
                yesterdayimpressions=(dfyesterdayrun.loc[dfyesterdayrun['Campaign Name']==row['Campaign Name']]['Impressions']).values[0]
                yesterdayclicks=(dfyesterdayrun.loc[dfyesterdayrun['Campaign Name']==row['Campaign Name']]['Clicks']).values[0]
                yesterdaysales=(dfyesterdayrun.loc[dfyesterdayrun['Campaign Name']==row['Campaign Name']]['Total Sales']).values[0]
                yesterdaynetprofit = (.7*float(yesterdaysales))-float(yesterdayspend)             
                yesterdayprofitclick= yesterdaynetprofit/int(yesterdayclicks.replace(',',''))
              
                deltaspend=float(row['Spend'])-float(yesterdayspend)
                deltabudget=int(row['Budget'].replace(',','')) - int(yesterdaybudget.replace(',',''))
                deltaimpressions=int(row['Impressions'].replace(',','')) - int(yesterdayimpressions.replace(',',''))
                deltaclicks=int(row['Clicks'].replace(',','')) - int(yesterdayclicks.replace(',',''))
                todaynetprofit = (.7*float(row['Total Sales']))-float(row['Spend'])             
                todayprofitclick= todaynetprofit/int(row['Clicks'].replace(',',''))
                deltanetprofit=todaynetprofit-yesterdaynetprofit
                deltaprofitclick=todayprofitclick-yesterdayprofitclick
                dfcombined=dfcombined.append({'Change':'Yes','Campaign Name':row['Campaign Name'],'Start Date':row['Start Date'],'Budget':deltabudget,
                                             'Spend':deltaspend,'Impressions':deltaimpressions,
                                             'Clicks':deltaclicks,'Total Sales':row['Total Sales'],
                                             'Net Profit':,'Profit/click':profitclick},ignore_index=True)
    except:
       pass
             
dfcombined=dfcombined[['Change','Campaign Name','Start Date','Budget','Spend','Impressions',
                                         'Clicks','Total Sales','Net Profit','Profit/click']]
             
             
html = dfcombined.style.apply(highlight_nochange,threshold='No',column=['Change'], axis=1).render()
#dfcombined.to_html()


with open(r'C:\Users\kecia\kellyads\out.html', 'w') as f:
    f.write(html)