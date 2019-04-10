#!/usr/bin/python3
import requests,sys,shutil,os
from bs4 import *
from PIL import Image

if len(sys.argv[1:])==0:
    exit("Usage : gimages.py [search_term]")

search_term = '_'.join(sys.argv[1:])
os.mkdir(search_term)
os.chdir(search_term)
r = requests.get("https://www.google.com/search?tbm=isch&q={}".format(search_term),headers={'user-agent':'firefox'})
s = BeautifulSoup(r.text,'html.parser')

images = s.select('img')

try:
    for i in images[:5]:
        input("Press 'enter' to see images...\n")
        im = requests.get(i.get('src'))
        path = 'img{}.jpg'.format(images.index(i))
        with open(path,"wb+") as f:
            f.write(im.content)
        img = Image.open(path)
        img.show()
finally:
    shutil.rmtree(os.getcwd())
