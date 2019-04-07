#!/usr/bin/python3
import requests,sys,webbrowser,os
from bs4 import BeautifulSoup
from markdown import markdown

if len(sys.argv[1:])==0:
    exit("Usage : scrape.py [search_term]")
else:
    search_term = ' '.join(sys.argv[1:])

save = input("Do you want to save the search results in a folder? ('y' or 'n')\n")
save = True if save=='y' else False
if save:
    dir = '_'.join(search_term.split())

    try:
        os.mkdir(dir)
    except OSError:
        pass

    os.chdir(dir)
    dir = search_term.replace(' ','_')

headers = {'user-agent':'MyProj'}
r = requests.get("https://google.com/search?q={}".format(search_term),headers=headers)

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
        temp_url = results[i][0]

        url = temp_url[temp_url.index('http',1):]
        print('------ ',results[i][1].upper(),'----->\n')
        print('------ ','URL :',url,'----->\n')

        r = requests.get(temp_url,headers={'user-agent':'boom-boom'})
        s = BeautifulSoup(r.text,'html.parser')
        p = s.select('p')

        for k in p:
            print(k.text,'\n')
            if save:
                open("{}.html".format(title.upper()),'a+').write(markdown(k.text))
        input("Press 'enter' for next article or 'Ctrl + C' to quit...\n")

    except KeyboardInterrupt:
        exit()
    except requests.exceptions.ConnectionError:
        pass
