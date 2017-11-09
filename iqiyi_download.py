#!/usr/bin/python
import json
import requests
import sys
import time
import subprocess
title = sys.argv[1].split(".")[0]

# call you-get
url = open(sys.argv[1], "r").read()
args = "you-get --json --format=HD " + url
m3u8_text = subprocess.check_output(args, shell=True)

# parse json, get HD stream m3u8
meta = json.loads(m3u8_text)
m3u8_url = meta["streams"]["HD"]["m3u8_url"]

# download m3u8
m3u8_request = requests.get(m3u8_url)
m3u8_text = m3u8_request.content

# download video
data_file = open(title + ".mp4", "w")
m3u8_contents = m3u8_text.split("\n")
total = len(m3u8_contents)
current = 0
for line in m3u8_contents:
    current = current + 1
    print "\rprogress: {progress}%".format(progress=round(current) * 100 / total),
    sys.stdout.flush()
    line = line.strip()
    if line.startswith("#"):
        continue
    while True:
        try:
            request = requests.get(line)
            data_file.write(request.content)
            break
        except:
            print "\rdownload failed, retry",
            time.sleep(0.2)
data_file.close()
