#!/usr/bin/python3
import webbrowser,sys
if len(sys.argv[1:]) < 1:
    exit('Usage : seek.py [search_term]')
search_term = ' '.join(sys.argv[1:])
webbrowser.open("http://google.com/search?q="+search_term)
