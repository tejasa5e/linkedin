
from selenium import webdriver#select the drive 
from selenium.webdriver.common.by import By#select the id ,or class ,or atribute in the html website 
from selenium.webdriver.common.keys import Keys#keys are like which key i used  when one code is run
from selenium.webdriver.support.ui import WebDriverWait#it is used to stop the selenium to to execute another code 
#it says that wate for the code to find the elements of the page which the progamer has written

#expected_conditions
from selenium.webdriver.support.expected_conditions import presence_of_element_located#1.1
#The expected_conditions module contains a set of predefined conditions to use with WebDriverWait.
from selenium.common.exceptions import NoSuchElementException#1.2

import time 

import string
#import openpyxl
import os
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import requests
#from linkedin_scraper import Person, actions
#import numpy as np 
import pandas as pd 
import json
from linkedin_search_results import *
import pymysql as p
from flask import *

def conn():#connection to server
    return p.connect(host='localhost',user='root',password='',database='Linkedin_names')

def Add_name(t):#to add name into database
    db=conn()
    sql='insert into data (name) value(%s)'
    cr=db.cursor()
    cr.execute(sql,t)
    db.commit()
    db.close()

    
def Get_name():#to select name specific from database 
    db=conn()
    sql='select name from data ORDER BY id DESC LIMIT 1'
    cr=db.cursor()
    cr.execute(sql)
    name=cr.fetchone()
    db.commit()
    db.close()
    return name
    
def Linkedin_login():#to get all profiles data like name link etc. in json format
    
    p=Get_name()
    p=p[0]
    #p=input('enter full  name: ')# to get input from user
    s=Service("C:\Windows\chromedriver.exe")#web driver
    driver= webdriver.Chrome(service=s)
    wait = WebDriverWait(driver,5)
#go to google
    driver.get("https://www.linkedin.com/login")
    time.sleep(3)

    box= driver.find_element(By.ID,('username'))#fro login id
    n= "nikhilr@a5econsulting.net"
    box.send_keys(n)
#box.send_keys(Keys.ENTER)

    box= driver.find_element(By.ID,('password'))#for pass
    n= "nikhil008"
    box.send_keys(n)
    box.send_keys(Keys.ENTER)


    a=p.split()
    j='_'
    a=j.join(a)

    b=(f'https://www.linkedin.com/search/results/all/?keywords=',a)#to create link 
    y=""
    x=y.join(b)
    driver.get(x)
    wait = WebDriverWait(driver,5)


    html = driver.page_source#to get html source of page 
    time.sleep(2)
    soup=BeautifulSoup(html,'lxml')
    return soup

def getdata():
    a=Linkedin_login()
    result=a.find_all('div' ,attrs={'class':'entity-result__content entity-result__divider pt3 pb3 t-12 t-black--light'})
    l=[]
    for i in result:
        name=i('span',{'aria-hidden':'true'})[0].text
        link=i('a',{'class':'app-aware-link'})[0]['href']
        position=i('div',{'class':'entity-result__primary-subtitle t-14 t-black t-normal'})[0].text.strip('\n')
        location=i('div',{'class':'entity-result__secondary-subtitle t-14 t-normal'})[0].text.strip('\n')
        l.append([name,link,position,location])
    
   

    return  l

def to_data():
    l=getdata()
    df=pd.DataFrame(l,columns=['Name','Link','Position','Location'])
    #df.reset_index(drop=True)
    t=df.to_json()
    return t

def Add_link():# to add selected profile link into database
    db=conn()
    sql='insert into data value(link=%s) where name=%s'
    cr=db.cursor()
    cr.execute(sql,l)
    db.commit()
    db.close()

def Get_links():#select specific link from database
    res=Linkedin_loginForLink()
    db=conn()
    sql='select link=%s from data where name=%s'
    cr=db.cursor()
    cr.execute(sql)
    link=cr.fetchone()
    db.commit()
    db.close()
    return link
    
def Driver_login():#login to driver and open profile and get page source
    x=Get_links()
    s=Service("C:\Windows\chromedriver.exe")#web driver
    driver= webdriver.Chrome(service=s)
    wait = WebDriverWait(driver,5)

    email = "nikhilr@a5econsulting.net"
    password = "nikhil008"
    actions.login(driver, email, password)
   
    driver.get(x)
    wait = WebDriverWait(driver,5)


    html = driver.page_source#to get html source of page 
    time.sleep(2)
    soup=BeautifulSoup(html,'lxml')

    return soup



def Data_list():#get required data into list format
    soup=Driver_login()
    data=[]
    intro = soup.find('div', {'class': 'pv-text-details__left-panel'})

    name_loc = intro.find("h1")
    name = name_loc.get_text().strip()#to find name

    works_at_loc = intro.find("div", {'class': 'text-body-medium'})
    works_at = works_at_loc.get_text().strip()# to find company name

    loc=soup.find_all('div',{'class':'pb2 pv-text-details__left-panel'})[0].text.split('\n')[2].strip()# to find location

    experience=[]# to find experience 
    exp=soup.find_all('div',{'class':'pvs-list__outer-container'},)[1]('span',{'class':'visually-hidden'})
    for i in exp:
        s= i.text
        experience.append(s)

    education=[]# to find education
    edu=soup.find_all('div',{'class':'pvs-list__outer-container'},)[2]('span',{'class':'visually-hidden'})
    for i in edu:
        s= i.text
        education.append(s)
        
    skills=[]# to find skills
    skil=soup.find_all('div',{'class':'pvs-list__outer-container'},)[3]('span',{'class':'visually-hidden'})
    for i in skil:
        s= i.text
        skills.append(s)

    print('\033[1m'+'Name -->'+'\033[0m', name,
        '\033[1m'+'\nWorks At -->'+'\033[0m', works_at,
          '\033[1m'+"\nLocation-->"+'\033[0m',loc,'\033[1m'+"\nExperience-->"+'\033[0m',experience,'\033[1m'+"\nEducation-->"+'\033[0m',education,'\033[1m'+"\nSkills-->"+'\033[0m',skills)
    data.append([name,works_at,loc,experience,education,skills])

    return data

def Data_to_json():#to convert list into dataframe and then convert this data to json format
    a=Data_list()
    
    Dataframe=pd.DataFrame(a,columns=['Name','Work at','Location','Experience','Education','Skills'])
    output=json.loads(Dataframe.to_json(orient="records"))

    return output
            
