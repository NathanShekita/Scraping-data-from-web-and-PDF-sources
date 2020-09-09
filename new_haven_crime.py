# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 14:18:15 2020

@author: ns662
"""

import tabula
import time
import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 

from PyPDF2 import PdfFileReader, PdfFileWriter

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
#Part 2 - Scrape and download files

#With options set, open the page
driver.get('https://www.newhavenct.gov/gov/depts/nhpd/compstat_reports.htm')

#Wait until end of page loads
xml_wait='//*[@id="page-content"]/table/tbody/tr/td[2]/font'
WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH,xml_wait)))

#download each report
for i in range(2,48):
    pager=str(i)
    xml='//*[@id="page-content"]/div[4]/table/tbody/tr['+pager+']/td[1]/a'
    download_element=driver.find_element_by_xpath(xml)
    download_element.send_keys(webdriver.common.keys.Keys.RETURN)  
    
    #Need to let chrome finish downloading, so sleep for 4 seconds a bit before iterating
    time.sleep(4)

#end the web session
driver.quit()   

##############################################################################
#Part 3 - Extract the first page from downloaded pdfs

#Extract first page from each pdf (~30 pages each)
#Otherwise tabula takes too long

#Loop through all files in directory
directory = r'C:/Users/ns662/Documents/master_Python/new_haven_compstat/Weekly_Report_onepage'
for entry in os.scandir(directory):
    file=entry.path
    
    #Using PyPDF2 package, extract first page
    with open(file, 'rb') as infile:

        reader = PdfFileReader(infile)
        writer = PdfFileWriter()
        writer.addPage(reader.getPage(0))

        #Save one-page output as "temp.pdf", delete original file, replace with one-page version
        with open('C:/Users/ns662/Documents/master_Python/new_haven_compstat/Weekly_Report_onepage/temp.pdf', 'wb') as outfile:
            writer.write(outfile)
            infile.close()
            outfile.close()
            os.remove(file)
            os.rename('C:/Users/ns662/Documents/master_Python/new_haven_compstat/Weekly_Report_onepage/temp.pdf',file)
    
##############################################################################
