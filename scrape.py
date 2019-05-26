#!/usr/bin/python3
import requests,sys,webbrowser,os,re
from bs4 import BeautifulSoup
from markdown import markdown

if len(sys.argv[1:])==0:
    search_term = ' '.join(input("Enter the search term\n").split())
else:
    search_term = ' '.join(sys.argv[1:])

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'}
r = requests.get("http://google.com/search?q={}".format(search_term),headers=headers)

open('source.html','w+').write(r.text)
s = BeautifulSoup(r.text,'html.parser')
links = s.select('.r a')
head = s.findAll('div',attrs={'class':'kp-header'})

if len(head) !=0 :
    print('Found an extra header!\n')
    contents = s.findAll('div',attrs={'class':'i4J0ge'})
    if len(contents) != 0:
        for i in contents:
            s = i.text
            cor = []

            err = re.findall(r'[a-z][A-Z]',s)
            for i in err:
                i = i.replace('','. ').lstrip('. ').rstrip('. ')
                cor.append(i)

            l=list(zip(err,cor))

            for i in l:
                s = s.replace(*i)
            print(s+'\n')

save = input("Do you want to save the search results in a folder? ('y' or 'n')\n")
save = True if save=='y' else False
if save:
    dir = '_'.join(search_term.split())

    try:
        os.mkdir(dir)
    except OSError:
        pass

    os.chdir(dir)

results = []

for j,i in enumerate(links,1):
    url = i.get('href').replace('/url?q=','https://google.com/url?q=')
    results.append([url,i.text])

for i in range(0,5):
    try:
        #webbrowser.open(results[i])
        title = results[i][1]
        url = results[i][0]

        print('------ ',title.upper(),'----->\n')
        print('------ ','URL :',url,'----->\n')

        r = requests.get(url,headers=headers)
        s = BeautifulSoup(r.text,'html.parser')
        p = s.select('p')

        for k in p:
            print(k.text,'\n')
            if save:
                open("{}.html".format(title.upper()),'a+').write(markdown(k.text))
        input("Press 'enter' for next article or 'Ctrl + C' to quit...\n")

    except KeyboardInterrupt:
        exit()
    except:
        pass
