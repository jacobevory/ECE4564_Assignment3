#!/usr/bin/env python3
import requests
import re




filename="Team 18 Proposal.pdf"
url="url"
token="4511~qCyMvD0YiKX4IrjRoxuhJ7iytKJkKCXIYGM4nQdqFPgjimz8a0gdZtljZWuoq533"
url = "https://vt.instructure.com/api/v1/groups/46402/files?access_token=" + token
r=requests.get(url)
data = r.content
datas = data.split('{')

i=0; 
while i < len(datas):
   lines = datas[i].split(',')
   if any(filename in s for s in lines):
      temp=filter(lambda x: 'url' in x, lines)
      strtemp = ''.join(temp)
      urls = re.search("(?P<url>https?://[^\s]+)", strtemp).group("url")
      rest = urls.split('"', 1)[0]
      finalurl = rest.replace("\u0026", "&")
      r = requests.get(finalurl, allow_redirects=True)
      open("filename", 'wb').write(r.content)
   i+=1


