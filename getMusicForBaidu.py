#!/usr/bin/python
# coding:utf-8

import json
import os
import re
import urllib.request
import requests

minimumsize = 1

mm = ['等你下课','病变']

for value in mm:

    url = 'http://sug.music.baidu.com/info/suggestion'
    payload = {'word': value, 'version': '2', 'from': '0'}
    print("Song Name: " + value)

    r = requests.get(url, params=payload)
    contents = r.text
    d = json.loads(contents, encoding="utf-8")
    if ('data' not in d):
        print("do not have flac\n")
        continue
    if ('song' not in d["data"]):
        print("do not have flac\n")
        continue
    songid = d["data"]["song"][0]["songid"]
    print("Song ID: " + songid)

    url = "http://music.baidu.com/data/music/fmlink"
    payload = {'songIds': songid, 'type': 'mp3'}
    r = requests.get(url, params=payload)
    contents = r.text
    d = json.loads(contents, encoding="utf-8")
    if d is not None and 'data' not in d or d['data'] == '':
        continue
    songlink = d["data"]["songList"][0]["songLink"]
    if (len(songlink) < 10):
        print("do not have flac\n")
        continue
        print("Song Source: " + songlink + "\n");

    songdir = "songs"
    if not os.path.exists(songdir):
        os.makedirs(songdir)

    songname = d["data"]["songList"][0]["songName"]
    artistName = d["data"]["songList"][0]["artistName"]
    filename = "D:/MyResources/Multi-Media-File/Music/Baidu/" + songname + "-" + artistName + ".mp3"
    # filename = "./" + songdir + "/" + songname + "-" + artistName + ".flac"
    f = urllib.request.urlopen(songlink)
    headers = requests.head(songlink).headers
    size = int(headers['Content-Length']) / (1024 ** 2)

    if not os.path.isfile(filename) or os.path.getsize(filename) < minimumsize:
        print("%s is downloading now ......\n" % songname)
        with open(filename, "wb") as code:
            code.write(f.read())
    else:
        print("%s is already downloaded. Finding next song...\n\n" % songname)
print("\n================================================================\n")
print("Download finish!")
