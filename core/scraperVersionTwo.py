
import os
from zlib import DEF_BUF_SIZE
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from cb_dj_weather_app.settings import BASE_DIR, STATIC_ROOT
import shutil
from webdriver_manager.chrome import ChromeDriverManager
from django.http import FileResponse
from pathlib import Path

from time import sleep
from email import header
from core.forms import getDataForm


from core.views import get_balance_sheet
from requests.structures import CaseInsensitiveDict
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.shortcuts import render,redirect
import requests
import json 
from typing import List, final
from collections import Iterable
from django.http import HttpResponse
import re
from bs4 import BeautifulSoup
import csv
import pandas as pd
from json import loads
import requests
from time import *
from time import sleep
import glob
from django.http import JsonResponse

from .models import APIRequest
from register.models import Profile
from django.contrib.auth.models import User


def scrape_operating_performance(request):
    if 'ticker' in request.GET and 'market' in request.GET:
        ticker_value = request.GET.get("ticker", "")
        market_value = request.GET.get("market", "")
        CHROME_DRIVER_PATH = BASE_DIR+"/chromedriver"
        prefs = {'download.default_directory' :  BASE_DIR + "/selenium"}
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('prefs', prefs)
        chromeOptions.add_argument("--disable-infobars")
        chromeOptions.add_argument("--start-maximized")
        chromeOptions.add_argument("--disable-extensions")
        chromeOptions.add_argument('--window-size=1920,1080')
        chromeOptions.add_argument("--headless")
        chromeOptions.add_argument('--no-sandbox')   
        chromeOptions.add_argument("--disable-dev-shm-usage") 
        # driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chromeOptions)
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chromeOptions)
        driver.get(f"https://www.morningstar.com/stocks/{market_value}/{ticker_value}/performance")
      
        data = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='mds-table__scroller__sal']"))).get_attribute("outerHTML")
        df  = pd.read_html(data)    
        df[0].to_json ('jsonfile.json', orient='records')
        a_file = open("jsonfile.json", "r")
        a_json = json.load(a_file)
        pretty_json = json.dumps(a_json).replace("null", '"0"')
        a_file.close()
        return HttpResponse(pretty_json, content_type='text/json')

def scrape_dividends(request):
    if 'ticker' in request.GET and 'market' in request.GET:
        ticker_value = request.GET.get("ticker", "")
        market_value = request.GET.get("market", "")
        CHROME_DRIVER_PATH = BASE_DIR+"/chromedriver"
        prefs = {'download.default_directory' :  BASE_DIR + "/selenium"}
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('prefs', prefs)
        chromeOptions.add_argument("--disable-infobars")
        chromeOptions.add_argument("--start-maximized")
        chromeOptions.add_argument("--disable-extensions")
        chromeOptions.add_argument('--window-size=1920,1080')
        chromeOptions.add_argument("--headless")
        chromeOptions.add_argument('--no-sandbox')   
        chromeOptions.add_argument("--disable-dev-shm-usage") 
        # driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chromeOptions)
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chromeOptions)
        driver.get(f"https://www.morningstar.com/stocks/{market_value}/{ticker_value}/dividends")
      
        data = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='mds-table__scroller__sal']"))).get_attribute("outerHTML")
        df  = pd.read_html(data)    
        df[0].to_json ('jsonfile.json', orient='records')
        a_file = open("jsonfile.json", "r")
        a_json = json.load(a_file)
        pretty_json = json.dumps(a_json).replace("null", '"0"')
        a_file.close()
        return HttpResponse(pretty_json, content_type='text/json')


def scrape_valuation(request):
    if 'ticker' in request.GET and 'market' in request.GET and 'type' in request.GET:
        type_value = request.GET.get("type", "")
        ticker_value = request.GET.get("ticker", "")
        market_value = request.GET.get("market", "")
        CHROME_DRIVER_PATH = BASE_DIR+"/chromedriver"
        prefs = {'download.default_directory' :  BASE_DIR + "/selenium"}
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('prefs', prefs)
        chromeOptions.add_argument("--disable-infobars")
        chromeOptions.add_argument("--start-maximized")
        chromeOptions.add_argument("--disable-extensions")
        chromeOptions.add_argument('--window-size=1920,1080')
        chromeOptions.add_argument("--headless")
        chromeOptions.add_argument('--no-sandbox')   
        chromeOptions.add_argument("--disable-dev-shm-usage") 
       # driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chromeOptions)
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chromeOptions)
        if type_value == "cf":
            driver.get(f"https://www.morningstar.com/stocks/{market_value}/{ticker_value}/valuation")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Cash Flow')]"))).click()
            data = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='sal-component-ctn sal-component-key-stats-cash-flow sal-eqcss-key-stats-cash-flow']"))).get_attribute("outerHTML")
            df  = pd.read_html(data)    
            df[0].to_json ('jsonfile.json', orient='records')
            a_file = open("jsonfile.json", "r")
            a_json = json.load(a_file)
            pretty_json = json.dumps(a_json).replace("null", '"0"')
            a_file.close()
            return HttpResponse(pretty_json, content_type='text/json')

        elif type_value == "fh":
            driver.get(f"https://www.morningstar.com/stocks/{market_value}/{ticker_value}/valuation")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Financial Health')]"))).click()
            data = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='sal-component-ctn sal-component-key-stats-financial-health sal-eqcss-key-stats-financial-health']"))).get_attribute("outerHTML")
            df  = pd.read_html(data)    
            df[0].to_json ('jsonfile.json', orient='records')
            a_file = open("jsonfile.json", "r")
            a_json = json.load(a_file)
            pretty_json = json.dumps(a_json).replace("null", '"0"')
            a_file.close()
            return HttpResponse(pretty_json, content_type='text/json')
        elif type_value == "g":
            driver.get(f"https://www.morningstar.com/stocks/{market_value}/{ticker_value}/valuation")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Growth')]"))).click()
            data = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='sal-component-ctn sal-component-key-stats-growth-table sal-eqcss-key-stats-growth-table']"))).get_attribute("outerHTML")
            df  = pd.read_html(data)    
            df[0].to_json ('jsonfile.json', orient='records')
            a_file = open("jsonfile.json", "r")
            a_json = json.load(a_file)
            pretty_json = json.dumps(a_json).replace("null", '"0"')
            a_file.close()
            return HttpResponse(pretty_json, content_type='text/json')
        elif type_value == "ef":
            driver.get(f"https://www.morningstar.com/stocks/{market_value}/{ticker_value}/valuation")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Operating and Efficiency')]"))).click()
            data = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='sal-component-ctn sal-component-key-stats-oper-efficiency sal-eqcss-key-stats-oper-efficiency']"))).get_attribute("outerHTML")
            df  = pd.read_html(data)    
            df[0].to_json ('jsonfile.json', orient='records')
            a_file = open("jsonfile.json", "r")
            a_json = json.load(a_file)
            pretty_json = json.dumps(a_json).replace("null", '"0"')
            a_file.close()
            return HttpResponse(pretty_json, content_type='text/json')
        else: 
            return HttpResponse('error', content_type='text/json')





def scrape(request):
    if request.POST:
        ticker_value =  request.POST.get("ticker", "")
        market_value =  request.POST.get("market", "")
        download_type = request.POST.get("download_type", "")

        scraper(ticker_value=ticker_value, market_value=market_value, download_type=download_type)
        print("===========")
        print(download_type)
        print("===========")
        if download_type == "INCOME_STATEMENT":
            with open(BASE_DIR + "/selenium/Income Statement_Annual_As Originally Reported.xls", 'rb') as file:
                response = HttpResponse(file, content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment; filename=stockData.xls'  
                return response
        elif download_type == "BALANCE_SHEET":
            with open(BASE_DIR + "/selenium/Balance Sheet_Annual_As Originally Reported.xls", 'rb') as file:
                response = HttpResponse(file, content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment; filename=stockData.xls'  
        elif download_type == "CASH_FLOW":
            with open(BASE_DIR + "/selenium/Cash Flow_Annual_As Originally Reported.xls", 'rb') as file:
                    response = HttpResponse(file, content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment; filename=stockData.xls'   
                    return response
        else:
            return render(request, "../templates/stockData.html")
    else:
        return render(request, "../templates/stockData.html")




def scraper(ticker_value,market_value,download_type):
    CHROME_DRIVER_PATH = BASE_DIR+"/chromedriver"
    prefs = {'download.default_directory' :  BASE_DIR + "/selenium"}
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option('prefs', prefs)
    chromeOptions.add_argument("--disable-infobars")
    chromeOptions.add_argument("--start-maximized")
    chromeOptions.add_argument("--disable-extensions")
    chromeOptions.add_argument('--window-size=1920,1080')
    # chromeOptions.add_argument("--headless")
    # chromeOptions.add_argument('--no-sandbox')   
    chromeOptions.add_argument("--disable-dev-shm-usage") 
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chromeOptions)
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chromeOptions) 
    driver.get(f"https://www.morningstar.com/stocks/{market_value}/{ticker_value}/financials")
    if download_type == "INCOME_STATEMENT":
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Expand Detail View')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export Data')]"))).click()
        sleep(5)
        driver.quit()
        
    elif download_type == "BALANCE_SHEET":
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Balance Sheet')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Expand Detail View')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export Data')]"))).click()
        sleep(5)
        driver.quit()
    elif download_type == "CASH_FLOW":
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Cash Flow')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Expand Detail View')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export Data')]"))).click()
        sleep(5)
        driver.quit()
    elif download_type == "ALL":
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Expand Detail View')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export Data')]"))).click()
        sleep(5)
       
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Balance Sheet')]"))).click()
        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Expand Detail View')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export Data')]"))).click()
        sleep(5)
    
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Cash Flow')]"))).click()
        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Expand Detail View')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export Data')]"))).click()
        sleep(5)
        driver.quit()
        





          




            

    # if 'ticker' in request.GET and 'market' in request.GET and 'type' in request.GET:
    #     ticker_value = request.GET.get("ticker", "")
    #     market_value = request.GET.get("market", "")
    #     type_value = request.GET.get("type", "")
    #     
    #     driver.get(f"https://www.morningstar.com/stocks/{market_value}/{ticker_value}/financials")
    #     if type_value == "is":
    #         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Expand Detail View')]"))).click()
    #         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export Data')]"))).click()
    #         sleep(5)
    #         driver.quit()
    #         with open(BASE_DIR + "/selenium/Income Statement_Annual_As Originally Reported.xls", 'rb') as file:
    #             response = HttpResponse(file, content_type='text/csv')
    #             response['Content-Disposition'] = 'attachment; filename=stockhistory.csv'  
    #             # return response
    #             return render(request, "stockData.html", response)
    #         #     df = pd.read_excel (BASE_DIR + "/selenium/Income Statement_Annual_As Originally Reported.xls")
    #         #     df.replace(',','', regex=True, inplace=True)
    #         #     df.to_json ('jsonfile.json', orient='records')
    #         #     a_file = open("jsonfile.json", "r")
    #         #     a_json = json.load(a_file)
    #         #     pretty_json = json.dumps(a_json).replace("null", '"0"').replace(" ","")
    #         #     a_file.close()
    #         # return HttpResponse(pretty_json, content_type='text/json')
    #     elif type_value == "bs":
    #         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Balance Sheet')]"))).click()
    #         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Expand Detail View')]"))).click()
    #         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export Data')]"))).click()
    #         sleep(5)
    #         driver.quit()
    #         with open(BASE_DIR + "/selenium/Balance Sheet_Annual_As Originally Reported.xls", 'rb') as file:
    #             response = HttpResponse(file, content_type='text/csv')
    #             response['Content-Disposition'] = 'attachment; filename=stockhistory.csv'  

                
    #             return response
    #             # df = pd.read_excel (BASE_DIR + "/selenium/Balance Sheet_Annual_As Originally Reported.xls")
    #         #     df.replace(',','', regex=True, inplace=True)
    #         #     df.to_json ('jsonfile.json', orient='records')
    #         #     a_file = open("jsonfile.json", "r")
    #         #     a_json = json.load(a_file)
    #         #     pretty_json = json.dumps(a_json).replace("null", '"0"').replace(" ","")
    #         #     a_file.close()
    #         # return HttpResponse(pretty_json, content_type='text/json')
    #     elif type_value == "cf":
    #         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Cash Flow')]"))).click()
    #         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Expand Detail View')]"))).click()
    #         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export Data')]"))).click()
    #         sleep(5)
    #         driver.quit()
    #     with open(BASE_DIR + "/selenium/Cash Flow_Annual_As Originally Reported.xls", 'rb') as file:
    #         # df = pd.read_excel (BASE_DIR + "/selenium/Cash Flow_Annual_As Originally Reported.xls")
    #         # with open('BASE_DIR + "/selenium/Cash Flow_Annual_As Originally Reported.xls"') as myfile:
    #         response = HttpResponse(file, content_type='text/csv')
    #         response['Content-Disposition'] = 'attachment; filename=stockhistory.csv'   
    #         return response
            # df.replace(',','', regex=True, inplace=True)
            # df.to_json ('jsonfile.json', orient='records')
            # a_file = open("jsonfile.json", "r")
            # a_json = json.load(a_file)
            # pretty_json = json.dumps(a_json).replace("null", '"0"').replace(" ","")
            # a_file.close()
            # return HttpResponse(pretty_json, content_type='text/json')

            #  dfs = (pd.read_csv(day + '.csv', error_bad_lines=False) for day in days)
            # pd.concat(dfs).to_csv('stock_history.csv')




