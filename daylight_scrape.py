# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 13:00:42 2020

@author: ns662
"""



from selenium import webdriver

import pandas as pd


##############################################################################
#PART 1 - Setup and options

#Configure Selenium to scrape PDFs from New Haven PD website: https://www.newhavenct.gov/gov/depts/nhpd/compstat_reports.htm

#first set of options to configure where file is downloaded
#Note: including \\ at end of directory important!
#Also added options so that "clicking" a link auto-downloads into specified directory
options = webdriver.ChromeOptions()
prefs = {"download.default_directory" : r"C:\Users\ns662\Documents\master_Python\new_haven_compstat\Weekly_Reports\\",
             "directory_upgrade" : True,
             "download.prompt_for_download": False,
             "download.directory_upgrade": True,
             "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
             }
options.add_experimental_option("prefs", prefs)

#options for enabling download when you run without opening chrome window (default is to not allow downloads in headless mode)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

#define the Chrome driver location, specify to use all the options added above
driver=webdriver.Chrome('C:/Users/ns662/Documents/master_Python/chromedriver_win32/chromedriver.exe', options=options)

##############################################################################
#November and March have errors

postlist = pd.DataFrame(columns = ['Year','Month','Day','Daylight'])

year_list=['2019','2020']


for year in year_list:
    if year in ('2019'):
        month_list=['1','2','3','4','5','6','7','8','9','10','11','12']
    else: month_list=['1','2','3','4','5','6','7','8']
    
    for months in month_list:
        
        driver.get('https://www.timeanddate.com/sun/usa/new-haven?month='+months+'&year='+year)
        
        if months in ('1','3','5','7','8','10','12'):
            ranger=32
        elif months in ('4','6','9','11'):
            ranger=31
        else: ranger=29
    
            #each page has 11 boxes, each box has the info from a job listing
        for i in range(1,ranger):
            
            pager=str(i)
            
            #November and March have errors due to daylight savings warning included in table
            if (i==10 and months in ('3') and year in ('2019')) or (i==3 and months in ('11') and year in ('2019')) or (i==8 and months in ('3') and year in ('2020')) or (i==1 and months in ('11') and year in ('2020')):
                continue
            
            if (i==10 and months in ('3') and year in ('2019')) or (i==3 and months in ('11') and year in ('2019')) or (i==8 and months in ('3') and year in ('2020')) or (i==1 and months in ('11') and year in ('2020')):
                i=i+1
            
            #each XML element iterates nicely, so you can loop through the xml path of each element
            #pull each of the desired fields (selenium pulls elements as a list) and define first list item as string
            
            xml_post='//*[@id="as-monthsun"]/tbody/tr['+pager+']/td[3]'
            post=driver.find_elements_by_xpath(xml_post)
            post_daylight=post[0].text
            
            post_day=pager
            post_month=months
            post_year=year
    
            #append each of the desired fields into each column, incrementing row each loop
            postlist.loc[len(postlist)]=[post_year,post_month,post_day,post_daylight]

postlist.to_csv('C:/Users/ns662/Documents/master_Python/new_haven_compstat/daylight_data.csv', index=False)


