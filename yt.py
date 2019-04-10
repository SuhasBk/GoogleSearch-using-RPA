#!/usr/bin/python3
import platform
import re
from subprocess import *
import webbrowser
import requests
from bs4 import *
import os

search=input("Enter the search term\n").split()
try:
    r = requests.get("http://youtube.com/results?search_query=" + '+'.join(search),headers={'user-agent':'WTF'})
except requests.HTTPError as err:
    print(err)
    exit()
print("Searching....")
s = BeautifulSoup(r.text, 'html.parser')
l = s.select('div .yt-lockup-content')

urls = []
titles = []
views = []
uploaded = []
durations =[]

for i in l:
    meta = i.findAll('li')[:2]
    uploaded.append(meta[0].text)
    views.append(meta[1].text)
    durations.append(i.find('span',attrs={'class':'accessible-description'}).text)
    urls.append('http://youtube.com'+i.find('a').get('href'))
    titles.append(i.find('a').get('title'))


for i,t,up,d,v,ur in zip(range(3),titles,uploaded,durations,views,urls):
    try:
        p=requests.get(ur)
        opinion=re.findall(r'(\d+(,\d+)*)? other people',p.text)
        likes = opinion[0][0]
        dislikes=opinion[2][0]
        print((str(i)+' : '+t+'\nYouTube URL : '+ur+'\nUPLOADED : '+up+'\n'+d.upper().replace(' - ','')+'\nVIEWS : '+v+'\nLIKES : '+likes+'\nDISLIKES : '+dislikes+'\n'))
    except:
        pass


while True:
    ch=input("Enter the number corresponding to the link (type 'exit' to quit)- \n")
    for i,j in enumerate(urls):
        if ch==str(i):
            print(j)
            dorv=input("Ok! So, do you want to stream the video (type 'v') or download (type 'd', requires youtube-dl) it?\n")
            if dorv == 'd':
                mp3=input("Cool! BTW, do you want me to download the audio (type 'a') or video (type 'v')?\n")
                if mp3 == 'v':
                    print("Downloading video...")
                    run("youtube-dl "+j,shell=True)
                else:
                    print("Downloading audio...")
                    run("youtube-dl --extract-audio --audio-format mp3 "+j,shell=True)
            elif dorv == 'v':
                print("Streaming...")
                op = run(['vlc',j],stderr=PIPE,stdout=PIPE)
        elif ch=='exit':
            exit()
