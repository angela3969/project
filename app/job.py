#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 22:46:25 2022

@author: angela
"""

import requests
from bs4 import BeautifulSoup
import json
#import gspread
import pygsheets
from oauth2client.service_account import ServiceAccountCredentials as SAC

#連接google sheet
def getSpreadsheet(sheetName):
  gc = pygsheets.authorize(service_file='project-339309-44fd14c5499b.json')
  sht = gc.open_by_url(
    'https://docs.google.com/spreadsheets/d/1AAWHQbi9w09J8gx5lYTuy3TcqgX_z1vn8StbZE2iOmM/'
  )
  wks_list = sht.worksheets()
  #print(wks_list)
  return sht.worksheet_by_title(sheetName)
  #jobWks = sht.worksheet_by_title("jobList")


#存值
def saveJobValue(Id,jobId,jobName,company,location,education,applyUrl):
  jobWks = getSpreadsheet("careerList")
  jobWks.update_value(('A'+str(Id+1)),jobId)
  jobWks.update_value(('B'+str(Id+1)),jobName)
  jobWks.update_value(('C'+str(Id+1)),company)
  jobWks.update_value(('D'+str(Id+1)),location)
  jobWks.update_value(('E'+str(Id+1)),education)
  jobWks.update_value(('F'+str(Id+1)),applyUrl)

#存值
def saveSkillValue(Id,jobId,requiredSkill,level,category):
  skillWks = getSpreadsheet("skill2List")
  #print(Id)
  skillWks.update_value(('A'+str(Id+1)),jobId)
  skillWks.update_value(('B'+str(Id+1)),requiredSkill)
  skillWks.update_value(('C'+str(Id+1)),level)
  skillWks.update_value(('D'+str(Id+1)),category)
  print(str(Id)+jobId+requiredSkill+level+category)

#saveJob
def saveJob(Id,jobId,jobName,company,location,education,applyUrl):
  jobWks = getSpreadsheet("jobList")
  saveJobValue(Id,jobId,jobName,company,location,education,applyUrl)
  

#saveSkill
def saveSkill(Id,jobId,requiredSkill,level,category):
  #skillWks = getSpreadsheet("skillList")
  saveSkillValue(Id,jobId,requiredSkill,level,category)

#getJob
def getJob(career):
  url = "https://www.104.com.tw/jobs/search/?keyword="+career
  response = requests.get(url = url)
  soup = BeautifulSoup(response.text, "html.parser")
  #result = soup.find("div",id="js-job-content")
  articles = soup.find_all("article",class_="b-block--top-bord job-list-item b-clearfix js-job-item")

  Id = 0
  skillNum = 0
  for article in articles:
    jobName = article.get("data-job-name")
    print(jobName)
    company = article.get("data-cust-name")
    ul = article.find("ul","b-list-inline b-clearfix job-list-intro b-content")
    location = ul.select("li")[0].getText()
    education = ul.select("li")[2].getText()
    link = article.select_one(".js-job-link").get("href")
    applyURL = link[2:]
    Id+=1
    print(Id,company,location,education,applyURL)
    jobId = 'N'+str(Id);
    saveJob(Id,jobId ,jobName,company,location,education,applyURL)
    skillNum = getSkill(skillNum,jobId,applyURL)
  

#getSkill
def getSkill(skillNum,jobId,applyURL):
  line = skillNum
  #applyURL = 'www.104.com.tw/job/7fy5m?jobsource=jolist_d_relevance'
  link = applyURL.split('?')
  code = link[0].split('/')[2]
  print(code)
  url = 'https://www.104.com.tw/job/ajax/content/'+code
  headers = {
    "Referer": "https://www.104.com.tw/job/"+code,
  }
 
  #url = 'https://www.104.com.tw/job/ajax/content/79cls'
  #headers = {
    #"Referer": "https://www.104.com.tw/job/79cls",
  #}

  response = requests.get(url = url, headers = headers)
  content = json.loads(response.text)
  #print(content)
  data = (content['data'])['condition']
  print(data)
  major = data['major']
  if(major !=""):
    print(major)
    #return major
  languages = data['language']
  for language in languages:
    languageRequired = language['language']
    abilities = language['ability'].split("、")
    for ability in abilities:
      try:
        abilityRequired = ability.split("/")
        requiredLanguageAbility = languageRequired+"("+abilityRequired[0]+")"
        level = abilityRequired[1]
        category = "language"
        line+=1
        #saveSkill(line,jobId,requiredLanguageAbility,level,category)
        
      except:
        print('')

  Specialties = data['specialty']
  
  for specialty in Specialties:
    try:
      toolSpecialty = specialty['description']
      level = "擅長"
      category = "工具"
      line+=1
      saveSkill(line,jobId,toolSpecialty,level,category)
    except:
      print('')

  skills = data['skill']
  for skill in skills:
    try:  
      skillRequired = skill['description']
      level = ""
      category = ""
      line+=1
      saveSkill(line,jobId,skillRequired,level,category)
    except:
      print('')

  certificates = data['certificate']
  for certificate in certificates:
    try:
      certificateRequired = certificate['description']
      level = ""
      category = "certificate"
      line+=1
      saveSkill(line,jobId,certificateRequired,level,category)
    except:
      print('')
  
  driverLicenses = data['certificate']
  for driverLicense in driverLicenses:
    try:
      driverLicenseRequired = driverLicense['description']
      level = ""
      category = "drive"
      line+=1
      saveSkill(line,jobId,driverLicenseRequired,level,category)
    except:
      print('')
  
  return line
  #others = (content['data'])['others']


def setUpJobList():
  #jobWks = getSpreadsheet("jobList")
  saveJobValue(0,'jobId','jobName','company','location','education','applyUrl')
  saveSkillValue(0,'jobId','requiredSkill','level','category')
  getJob()


#saveSkill(1,'jobId','requiredSkill','level','category')
#getJob("財金")
#setUpJobList()
