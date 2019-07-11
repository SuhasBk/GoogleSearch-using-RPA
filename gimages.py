#!/usr/bin/python3
import requests,sys,shutil,os
from bs4 import *
from PIL import Image

if len(sys.argv[1:])==0:
    search_term = input("What do you want to see?\n> ")
else:
    search_term = '_'.join(sys.argv[1:])
os.mkdir(search_term)
os.chdir(search_term)

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'}

r = requests.get("https://www.google.com/search?tbm=isch&q={}".format(search_term),headers=headers)
s = BeautifulSoup(r.text,'html.parser')

images = s.findAll('img',attrs={'data-src':re.compile(r'[\w+]')})

try:
    for i in images[:5]:
        input("Press 'enter' to see images...\n")
        im = requests.get(i.get('data-src'))
        path = 'img{}.jpg'.format(images.index(i))
        with open(path,"wb+") as f:
            f.write(im.content)
        img = Image.open(path)
        img.show()
finally:
    shutil.rmtree(os.getcwd())
