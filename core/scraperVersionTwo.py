
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


def scrape(request):
    if request.POST:
        ticker_value =  request.POST.get("ticker", "")
        market_value =  request.POST.get("market", "")
        download_type = request.POST.get("download_type", "")
        if download_type == "INCOME_STATEMENT" or download_type == "BALANCE_SHEET" or download_type == "CASH_FLOW":
            scraper(ticker_value=ticker_value, market_value=market_value, download_type=download_type)
        elif download_type == "VALUATION_CASH_FLOW" or download_type == "VALUATION_GROWTH" or download_type == "VALUATION_FINANCIAL_HEALTH" or download_type == "VALUATION_OPERATING_EFFICIENCY":
            scraper_valuation(ticker_value=ticker_value, market_value=market_value, download_type=download_type)
        elif download_type =="DIVIDENDS":
            scraper_dividends(ticker_value=ticker_value, market_value=market_value)
        elif download_type == "OPERATING_PERFORMANCE":
            scraper_operating_performance(ticker_value=ticker_value, market_value=market_value)
        elif download_type == "ALL":
            scraper(ticker_value=ticker_value, market_value=market_value, download_type=download_type)
            # scraper_valuation(ticker_value=ticker_value, market_value=market_value, download_type=download_type)
            # scraper_dividends(ticker_value=ticker_value, market_value=market_value)
            # scraper_operating_performance(ticker_value=ticker_value, market_value=market_value)


        if download_type == "INCOME_STATEMENT":
            with open(BASE_DIR + "/selenium/Income Statement_Annual_As Originally Reported.xls", 'rb') as file:
                response = HttpResponse(file, content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment; filename=stockData.xls'  
                return response
        elif download_type == "BALANCE_SHEET":
            with open(BASE_DIR + "/selenium/Balance Sheet_Annual_As Originally Reported.xls", 'rb') as file:
                response = HttpResponse(file, content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment; filename=stockData.xls'  
                return response 
        elif download_type == "CASH_FLOW":
            with open(BASE_DIR + "/selenium/Cash Flow_Annual_As Originally Reported.xls", 'rb') as file:
                    response = HttpResponse(file, content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment; filename=stockData.xls'   
                    return response
        elif download_type == "VALUATION_CASH_FLOW" or download_type == "VALUATION_GROWTH" or download_type == "VALUATION_FINANCIAL_HEALTH" or download_type == "VALUATION_OPERATING_EFFICIENCY" or download_type =="DIVIDENDS" or download_type == "OPERATING_PERFORMANCE":
             pd.read_json("jsonfile.json").to_excel("output.xls")
             with open("output.xls", 'rb') as file:
                    response = HttpResponse(file, content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment; filename=stockData.xls'   
                    return response
        elif download_type == "ALL":
            df1 = pd.read_excel(BASE_DIR + "/selenium/Balance Sheet_Annual_As Originally Reported.xls")
            df2 = pd.read_excel(BASE_DIR + "/selenium/Cash Flow_Annual_As Originally Reported.xls")
            df3 = pd.read_excel(BASE_DIR + "/selenium/Income Statement_Annual_As Originally Reported.xls")
            writer = pd.ExcelWriter("all.xls", engine = 'xlsxwriter')
            df1.to_excel(writer, sheet_name = 'BALANCE SHEET')
            df2.to_excel(writer, sheet_name = 'CASH FLOW')
            df3.to_excel(writer, sheet_name = 'INCOME STATEMENT')
            writer.save()
            writer.close()
            with open("all.xls", 'rb') as file:
                    response = HttpResponse(file, content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment; filename=stockData.xls'   
                    return response
        else:
            return render(request, "../templates/stockData.html")
    else:
        return render(request, "../templates/stockData.html")


def scraper_operating_performance(ticker_value, market_value):
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
    # driver_operating_perfomance = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chromeOptions)
    driver_operating_perfomance = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chromeOptions)
    driver_operating_perfomance.get(f"https://www.morningstar.com/stocks/{market_value}/{ticker_value}/performance")
    data = WebDriverWait(driver_operating_perfomance, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='mds-table__scroller__sal']"))).get_attribute("outerHTML")
    data = WebDriverWait(driver_operating_perfomance, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='mds-table__scroller__sal']"))).get_attribute("outerHTML")
    df  = pd.read_html(data)    
    df[0].to_json ('jsonfile.json', orient='records')
    a_file = open("jsonfile.json", "r")
    a_file.close()
    sleep(5)
    driver_operating_perfomance.quit()
    

def scraper_dividends(ticker_value,market_value):
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
    # driver_dividends = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chromeOptions)
    driver_dividends = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chromeOptions)
    driver_dividends.get(f"https://www.morningstar.com/stocks/{market_value}/{ticker_value}/dividends")
    data = WebDriverWait(driver_dividends, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='mds-table__scroller__sal']"))).get_attribute("outerHTML")
    df  = pd.read_html(data)    
    df[0].to_json ('jsonfile.json', orient='records')
    a_file = open("jsonfile.json", "r")
    a_file.close()
    sleep(5)
    driver_dividends.quit()


def scraper_valuation(ticker_value,market_value,download_type):
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
    # valuation_driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chromeOptions)
    valuation_driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chromeOptions) 
    valuation_driver.get(f"https://www.morningstar.com/stocks/{market_value}/{ticker_value}/valuation")
    if download_type == "VALUATION_CASH_FLOW": 
        valuation_driver.get(f"https://www.morningstar.com/stocks/{market_value}/{ticker_value}/valuation")
        WebDriverWait(valuation_driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Cash Flow')]"))).click()
        data = WebDriverWait(valuation_driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='sal-component-ctn sal-component-key-stats-cash-flow sal-eqcss-key-stats-cash-flow']"))).get_attribute("outerHTML")
        df  = pd.read_html(data)    
        df[0].to_json ('jsonfile.json', orient='records')
        a_file = open("jsonfile.json", "r")
        a_json = json.load(a_file)
        a_file.close()
        sleep(5)
        valuation_driver.quit()    

    elif download_type == "VALUATION_GROWTH": 
        WebDriverWait(valuation_driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Growth')]"))).click()
        data = WebDriverWait(valuation_driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='sal-component-ctn sal-component-key-stats-growth-table sal-eqcss-key-stats-growth-table']"))).get_attribute("outerHTML")
        df  = pd.read_html(data)    
        df[0].to_json ('jsonfile.json', orient='records')
        a_file = open("jsonfile.json", "r")
        a_json = json.load(a_file)
        pretty_json = json.dumps(a_json).replace("null", '"0"')
        a_file.close()
        sleep(5)
        valuation_driver.quit()       

        

    elif download_type == "VALUATION_FINANCIAL_HEALTH": 
        WebDriverWait(valuation_driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Financial Health')]"))).click()
        data = WebDriverWait(valuation_driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='sal-component-ctn sal-component-key-stats-financial-health sal-eqcss-key-stats-financial-health']"))).get_attribute("outerHTML")
        df  = pd.read_html(data)    
        df[0].to_json ('jsonfile.json', orient='records')
        a_file = open("jsonfile.json", "r")
        a_json = json.load(a_file)
        pretty_json = json.dumps(a_json).replace("null", '"0"')
        a_file.close()
        sleep(5)
        valuation_driver.quit()      

    elif download_type == "VALUATION_OPERATING_EFFICIENCY":
        WebDriverWait(valuation_driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Operating and Efficiency')]"))).click()
        data = WebDriverWait(valuation_driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='sal-component-ctn sal-component-key-stats-oper-efficiency sal-eqcss-key-stats-oper-efficiency']"))).get_attribute("outerHTML")
        df  = pd.read_html(data)    
        df[0].to_json ('jsonfile.json', orient='records')
        a_file = open("jsonfile.json", "r")
        a_json = json.load(a_file)
        pretty_json = json.dumps(a_json).replace("null", '"0"')
        a_file.close()
        sleep(5)
        valuation_driver.quit()      



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
    # driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chromeOptions)
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chromeOptions) 
    driver.get(f"https://www.morningstar.com/stocks/{market_value}/{ticker_value}/financials")
    if download_type == "INCOME_STATEMENT":
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Expand Detail View')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export Data')]"))).click()
        sleep(10)
        driver.quit()
        
    elif download_type == "BALANCE_SHEET":
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Balance Sheet')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Expand Detail View')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export Data')]"))).click()
        sleep(10)
        driver.quit()
    elif download_type == "CASH_FLOW":
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Cash Flow')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Expand Detail View')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export Data')]"))).click()
        sleep(10)
        driver.quit()
    elif download_type == "ALL":
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Expand Detail View')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export Data')]"))).click()
        sleep(10)
       
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Balance Sheet')]"))).click()
        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Expand Detail View')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export Data')]"))).click()
        sleep(10)
    
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Cash Flow')]"))).click()
        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Expand Detail View')]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export Data')]"))).click()
        sleep(10)
        driver.quit()

    
        




