#!/usr/bin/python3
import requests,sys,webbrowser,os,re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

if len(sys.argv[1:])==0:
    search_term = ' '.join(input("Enter the search term\n").split())
else:
    search_term = ' '.join(sys.argv[1:])

headers = {'User-Agent':UserAgent().random}
r = requests.get("https://google.com/search?q={}".format(search_term),headers=headers)

if not r.ok:
    exit("Error encountered.\n Status code : "+str(r.status_code)+"\n"+r.text)

s = BeautifulSoup(r.text,'html.parser')
links = s.select('.r a')

results = []

for j,i in enumerate(links,1):
    url = i.get('href').replace('/url?q=','https://google.com/url?q=')
    results.append([url,i.text])

for i in range(0,5):
    try:
        #webbrowser.open(results[i])
        title = results[i][1]
        url = results[i][0]

        print('------ TITLE : ',title.upper(),'----->\n')
        print('------ URL : ',url,'----->\n')

        r = requests.get(url,headers=headers)
        s = BeautifulSoup(r.text,'html.parser')
        p = s.select('p')

        for k in p:
            print(k.text,'\n')
            
        input("Press 'enter' for next article or 'Ctrl + C' to quit...\n")

    except KeyboardInterrupt:
        exit()
    except:
        pass
