#!/usr/bin/env python3

import os
import re
import json
import datetime as dt
from bs4 import BeautifulSoup as bs
import urllib.parse as ulparse
import requests as rq
from dotenv import load_dotenv

load_dotenv()

session = rq.Session()

# Just to get the __RequestVerificationToken
# TODO Add handling of case that solarweb is not reachable.
_ = session.get(url = "https://www.solarweb.com/")

login_url = "https://www.solarweb.com/Account/ExternalLogin"
login_form_post_url = "https://login.fronius.com/commonauth"

login_page_resp = session.get(
        login_url,
        allow_redirects = True)

key_pattern = re.compile("(?<=&sessionDataKey=)[a-z0-9\-]*")
session_key = None

for line in login_page_resp.iter_lines():
        match = re.search(key_pattern, line.decode())
        if match:
                session_key = match.group()

# TODO Add handling of login errors.
login_form_resp = session.post(
        url = login_form_post_url,
        data = {
                "username": os.getenv("username"),
                "password": os.getenv("password"),
                "sessionDataKey": session_key})

callback_url = ulparse.parse_qs(
        ulparse.urlparse(login_page_resp.url).query)["redirect_uri"][0]

login_soup = bs(login_form_resp.content, "lxml")

login_params = {
        "code": None,
        "id_token": None,
        "state": None,
        "AuthenticatedIdPs": None,
        "session_state": None}

for key in login_params.keys():
        login_params[key] = login_soup.find(
                "input", {"name": key}).get("value")

callback_resp = session.post(
        url = callback_url,
        data = login_params)


def chart_data(id, date):
       return {
        "pvSystemId": id,
        "year": date.year,
        "month": date.month,
        "day": date.day,
        "interval": "day",
        "view": "production"}

yesterday = dt.date.today() - dt.timedelta(days = 1)

chart_resp = session.get(
        url = "https://www.solarweb.com/Chart/GetChartNew",
        data = chart_data(
                id = os.getenv("fronius-id"),
                date = yesterday))

# TODO Add handling of case that chart_resp doesn't contain json.
json_out = json.dumps(chart_resp.json())

output_dir = "./"
output_file = output_dir + yesterday.strftime("%Y%m%d.json")

with open(output_file, "w") as outfile:
        outfile.write(json_out)