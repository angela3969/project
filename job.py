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

#getSkill
def getSkill(applyURL):
  link = applyURL.split('?')
  code = link[0].split('/')[2]
  print(code)
  url = 'https://www.104.com.tw/job/ajax/content/'+code
  headers = {
    "Referer": "https://www.104.com.tw/job/"+code,
  }
 

  response = requests.get(url = url, headers = headers)
  content = json.loads(response.text)
  print(content)
  data = (content['data'])['condition']
  dataDict = {}
  
  #
  major = data['major']
  if(major !=""):
    print(major)
    #return major
    dataDict['major'] = major
    
  #
  languages = data['language']
  dataDict['language'] = []
  for language in languages:
    languageRequired = language['language']
    abilities = language['ability'].split("、")
    for ability in abilities:
      try:
        abilityRequired = ability.split("/")
        requiredLanguageAbility = languageRequired+"("+abilityRequired[0]+")"
        level = abilityRequired[1]
        dataDict['language'].append([requiredLanguageAbility],level)
        #saveSkill(line,jobId,requiredLanguageAbility,level,category)  
      except:
        print('')
        
  #
  Specialties = data['specialty']
  dataDict['specialty'] = []
  for specialty in Specialties:
    try:
      toolSpecialty = specialty['description']
      dataDict['specialty'].append(toolSpecialty )
    except:
      print('')
      
  #
  skills = data['skill']
  dataDict['skill'] = []
  for skill in skills:
    try:  
      skillRequired = skill['description']
      dataDict['skill'].append(skillRequired)
    except:
      print('')
      
  #
  certificates = data['certificate']
  dataDict['certificate'] = []
  for certificate in certificates:
    try:
      certificateRequired = certificate['description']
      dataDict['certificate'].append(certificateRequired)
    except:
      print('')
  
  #
  driverLicenses = data['driverLicense']
  dataDict['driverLicense'] = []
  for driverLicense in driverLicenses:
    try:
      driverLicenseRequired = driverLicense['description']
      dataDict['driverLicense'].append(driverLicenseRequired )
    except:
      print('')
  
  
  #
  others = data['other']
  try:
     dataDict['others'] = others
  except:
     print('')
      
  return dataDict
