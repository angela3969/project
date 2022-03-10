#!/usr/bin/env python3
# -*- coding: utf-8-sig -*-
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
  return data
