# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 14:50:57 2020

@author: ns662
"""

import tabula
import os
import pandas as pd

#Loop through all files in this directory. Extract the data and crime data   
#Table extracted from Sept 2-8, 2019 & March 3-8, 2020 appears broken beyond repair (sadly, manual entry needed)
#Sept. 23-29, 2019 - Tabula returns two tables instead of 3

directory = r'C:/Users/ns662/Documents/master_Python/new_haven_compstat/Weekly_Report_onepage'
for entry in os.scandir(directory):
    file=entry.path
    print(file)

    tables = tabula.read_pdf(file, pages = 1, multiple_tables = True)
    
    #core data has the statistics, date label has the date
    #If three tables are returned from tabula, we want table 0 (core stats) and table 2 (dates). If two are returned, we want table 0 and table 1
    core_data=tables[0]
    try:
        date_label=tables[2]
    except: date_label=tables[1]
    
    #find date, add this to column later. Date is also used to name file
    date_label['period'] = date_label[['Unnamed: 0','Unnamed: 1','Unnamed: 2']].agg(' '.join,axis=1)
    labeler=date_label.iloc[0,5]
    labeler_prior=date_label.iloc[1,5]
    flabel=labeler.replace('/',"-")
    
    curr_week=date_label.iloc[0,3]
    priorweek=date_label.iloc[1,3]
    
    #For some reason tables in the PDFs are formatted differently. This tests if "nums" column already exists or needs to be split from inital column.
    #If nums are already formatted nicely, use the file_exception_list and simply rename the column. If not, need to split from initial column
    if len(core_data['Unnamed: 1'].value_counts()) > 0:
        file_exception_list = file
    else: file_exception_list=[]
    
    if file in file_exception_list:
            core_data=core_data.rename(columns={'Unnamed: 0':'strings', 'Unnamed: 1':'nums','Prior Week': 'pstatnum'})
            core_data=core_data[['strings','nums','pstatnum']]
            keystat = core_data[core_data.index<24]
            
            result=keystat[['strings','nums']]
            
            result2=keystat.pstatnum.str.split(('(\d+)'),expand=True)
            result2 = result2.loc[:,[1]]
            result2.rename(columns={1: 'nums_prior'}, inplace=True)
            
            data_final= pd.concat([result,result2],axis=1)
            
    else:
    
        #Tabula extracts a column that has both crime type and the number of cases, we need to split this column
        core_data=core_data.rename(columns={'Unnamed: 0':'statnum','Prior Week': 'pstatnum'})
        core_data=core_data[['statnum','pstatnum']]
        keystat = core_data[core_data.index<24]
        
        #create a column that is only the number of cases
        result = keystat.statnum.str.split(('(\d+)'),expand=True)
        result = result.loc[:,[0,1]]
        result.rename(columns={0:'strings', 1:'nums'}, inplace=True)
        result['strings']=result.strings.str.strip()
        
        result2=keystat.pstatnum.str.split(('(\d+)'),expand=True)
        result2 = result2.loc[:,[1]]
        result2.rename(columns={1: 'nums_prior'}, inplace=True)
    
        #create new dataset that has crime type as column, number of instances as second column
        data_final= pd.concat([result,result2],axis=1)
        
        #add in date
    data_final['week']=labeler
    data_final['week_prior']=labeler_prior
    data_final['date_ind']=curr_week
    data_final['date_ind_prior']=priorweek

#Create a broader classification column for crime type (based on New Haven PD groupings)
    data_final['strings']=data_final['strings'].replace(['Agg. Assault (NIBRS)'],'Agg Assault')
    data_final['strings']=data_final['strings'].replace(['Intimidation/Threatening-no force'],'Intimidation')
    data_final['type']=data_final['strings'].replace(['Murder Victims', 'Felony Sex. Assault', 'Robbery with Firearm', 'Other Robbery', 'Assault with Firearm Victims','Agg Assault'],'Violent Crimes')
    data_final['type']=data_final['type'].replace(['Burglary','MV Theft','Larceny from Vehicle','Other Larceny'],'Property Crimes')
    data_final['type']=data_final['type'].replace(['Simple Assault','Prostitution','Drugs & Narcotics','Vandalism','Intimidation','Weapons Violation'],'Other Crimes')
    #Keep these classifications as the final rows to be included
    data_final=data_final[data_final['type'].isin(['Violent Crimes','Property Crimes','Other Crimes','Motor Vehicle Stops','Confirmed Shots Fired'])]
        
    data_final.to_csv('C:/Users/ns662/Documents/master_Python/new_haven_compstat/weekly_report_data/crime_cleaned '+flabel+'.csv', index=False)

################################################
#Missing list has dates for which the week prior is a PDF missing from NHPD's website. Take the week priors and define as week, save csv

missing_list=['9-2-2019 to 9-8-2019', '9-16-2019 to 9-22-2019', '11-25-2019 to 12-1-2019','1-6-2020 to 1-12-2020','5-18-2020 to 5-24-2020','6-1-2020 to 6-7-2020',
              '6-15-2020 to 6-21-2020', '6-29-2020 to 7-5-2020', '7-13-2020 to 7-19-2020','8-3-2020 to 8-9-2020']

for missing in missing_list:
    
    df=pd.read_csv('C:/Users/ns662/Documents/master_Python/new_haven_compstat/weekly_report_data/crime_cleaned '+missing+'.csv') 
    
    last_week=df[['nums_prior', 'week_prior', 'date_ind_prior', 'type', 'strings']]
    last_week=last_week.rename(columns={'nums_prior':'nums', 'week_prior':'week','date_ind_prior': 'date_ind'})
    
    labeler=last_week.iloc[1,1]
    flabel=labeler.replace('/',"-")
    
    if missing=='6-15-2020 to 6-21-2020':
        flabel='6-8-2020 to 6-14-2020'
    
    last_week.to_csv('C:/Users/ns662/Documents/master_Python/new_haven_compstat/weekly_report_data/crime_cleaned '+flabel+'.csv', index=False)
    
#######################################
#Append all data!
df=pd.read_csv('C:/Users/ns662/Documents/master_Python/new_haven_compstat/weekly_report_data/crime_cleaned 7-1-2019 to 7-7-2019.csv')

directory = r'C:/Users/ns662/Documents/master_Python/new_haven_compstat/weekly_report_data'
for entry in os.scandir(directory):
    file=entry.path
    if file=='C:/Users/ns662/Documents/master_Python/new_haven_compstat/weekly_report_data/crime_cleaned 7-1-2019 to 7-7-2019.csv':
        continue
    df_append=pd.read_csv(file) 
    df=df.append(df_append)
    
df_final=df[['strings','nums','week','date_ind','type']]

df_final.to_csv('C:/Users/ns662/Documents/master_Python/new_haven_compstat/nhpd_crime_data.csv', index=False)

######################################################
#df_test=df[df.nums_prior.isnull()]
#unvals=df_test.drop_duplicates(subset=['date_ind'])
#df_test = df_test.reset_index(drop=True)
#df_test['date_ind']=pd.to_datetime(df_test['date_ind'],errors="raise")
