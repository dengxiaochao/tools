#!/usr/bin/python
import json
import requests
import sys
import time
import subprocess
import logging
title = sys.argv[1].split(".")[0]

logging.basicConfig(filename='dowload.log',level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s')

logging.info("downloading: {title}".format(title=title))
# call you-get
url = open(sys.argv[1], "r").read()
args = "you-get --json --format=HD " + url
m3u8_text = subprocess.check_output(args, shell=True)

# parse json, get HD stream m3u8
meta = json.loads(m3u8_text)
m3u8_url = meta["streams"]["HD"]["m3u8_url"]

# download m3u8
m3u8_request = requests.get(m3u8_url, timeout=1)
m3u8_text = m3u8_request.content

# download video
data_file = open(title + ".mp4", "w")
m3u8_contents = m3u8_text.split("\n")
total = len(m3u8_contents)
current = 0
for line in m3u8_contents:
    current = current + 1
    time_out = 0.1
    print "\rprogress: {:.2f}%".format(round(current) * 100 / total),
    sys.stdout.flush()
    line = line.strip()
    if not line or line.startswith("#"):
        logging.debug("line is comment, skip")
        continue
    while True:
        try:
            logging.debug("downloading: {line}".format(line=line))
            request = requests.get(line, timeout=1)
            data_file.write(request.content)
            break
        except:
            logging.info("download failed, wait {time_out}s".format(time_out=time_out))
            time.sleep(time_out)
            time_out = min(1, time_out*2)
data_file.close()
