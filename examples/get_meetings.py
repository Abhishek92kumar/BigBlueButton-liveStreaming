#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### to use this script you will need to ###
# apt install pip3
# pip3 install bigbluebutton_api_python
# pip3 install pyyaml

import argparse, sys, os, logging, yaml, urllib, json
from bigbluebutton_api_python import BigBlueButton

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

parser = argparse.ArgumentParser()
parser.add_argument("-s","--server", help="Big Blue Button Server URL")
parser.add_argument("-c","--config", help="path to config file in yaml format e.g. your docker-compose.yml", default="./docker-compose.yml")
parser.add_argument("-p","--secret", help="Big Blue Button Secret")
args = parser.parse_args()

def get_config_item(list_item):
    try:
        with open(args.config) as file:
            config = yaml.load(file)
    except FileNotFoundError as ERR:
        logging.error(ERR)
        sys.exit()

    docker_environment = config['services']['bbb-streamer']['environment']
    for line in docker_environment:
        if line.strip().startswith(list_item):
            return line.partition('=')[2]

def get_meetings():
    logging.info("fetching meetings from {}".format(args.server))
    try:
        return bbb.get_meetings()
    except urllib.error.URLError as ERR:
        logging.error(ERR)
        sys.exit()

if args.config:
    args.server = get_config_item('BBB_URL')
    args.secret = get_config_item('BBB_SECRET')
if not args.server and not args.secret:
    logging.error("Error: Please specify server and password or the path to the config file")
    sys.exit()

bbb = BigBlueButton(args.server,args.secret)
meetingsXML = get_meetings()
rawMeetings = meetingsXML['xml']['meetings']['meeting']
meetings = []
if isinstance(rawMeetings, list):
    meetings = rawMeetings
else:
    meetings.append(rawMeetings)

for meeting in meetings:
    print(meeting['meetingName'])
    print("ID: {}".format(meeting['meetingID']))
    print("ATTENDEE_PASSWORD: {}".format(meeting['attendeePW']))
    print("MODERATOR_PASSWORD: {}".format(meeting['moderatorPW']))
    print("")
