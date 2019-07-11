#!/usr/bin/python3
import re,os,sys
from subprocess import PIPE,Popen
import requests
from bs4 import BeautifulSoup

if len(sys.argv[1:])==0:
    exit("Usage : yt.py [search_term]")
else:
    search_term = ' '.join(sys.argv[1:])

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'}

try:
    r = requests.get("http://youtube.com/results?search_query=" + '+'.join(search_term),headers=headers)
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
uploaders = []
durations =[]

for i in l:
    try:
        meta = i.findAll('li')[:2]
        uploaded.append(meta[0].text)
        views.append(meta[1].text)
        durations.append(i.find('span',attrs={'class':'accessible-description'}).text)
        urls.append('http://youtube.com'+i.find('a').get('href'))
        titles.append(i.find('a').get('title'))
        uploader = i.findAll('a')[1].get('href')
        uploaders.append(re.findall('/user/(\w+)',uploader)[0])
    except:
        pass

for i,t,up,d,v,ur,us in zip(range(5),titles,uploaded,durations,views,urls,uploaders):
    try:
        p=requests.get(ur,headers=headers)
        opinion=re.findall(r'(\d+(,\d+)*)? other people',p.text)
        likes = opinion[0][0]
        dislikes=opinion[2][0]
        print(str(i)+' : '+t+'\nYouTube URL : '+ur+'\nUPLOADED : '+up+'\n'+d.upper().replace(' - ','')+'\nVIEWS : '+v+'\nLIKES : '+likes+'\nDISLIKES : '+dislikes+'\nUPLOADER : '+us+'\n')
    except requests.exceptions.ConnectionError:
        pass
    except IndexError:
        pass


while True:
    ch=input("Enter the number corresponding to the link (type 'exit' to quit)- \n")
    for i,j in enumerate(urls):
        if ch==str(i):
            print(j)
            dorv=input("Ok! So, do you want to stream the video (type 'v') or download (type 'd', requires youtube-dl) it?\n")
            if dorv == 'd':
                mp3=input("Do you want to download the audio (type 'a') or video (type 'v')?\n")
                if mp3 == 'v':
                    print("Downloading video...")
                    run("youtube-dl "+j,shell=True)
                else:
                    print("Downloading audio...")
                    run("youtube-dl --extract-audio --audio-format mp3 "+j,shell=True)
            elif dorv == 'v':
                print("Streaming...")
                try:
                    Popen(['vlc',j],stderr=PIPE,stdout=PIPE,close_fds=True)
                except FileNotFoundError:
                    Popen([input("Enter your default media player...\nEx: 'mpv','totem' : "),j],stderr=PIPE,stdout=PIPE,close_fds=True)
        elif ch=='exit':
            exit()
