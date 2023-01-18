import os
import re
from bs4 import BeautifulSoup as bs
import urllib.parse as ulparse
import requests as rq
from dotenv import load_dotenv

load_dotenv()

session = rq.Session()

# Just to get the __RequestVerificationToken
_ = session.get(url = "https://www.solarweb.com/")

login_page_resp = session.get(
        os.getenv("login-url"),
        allow_redirects = True)

key_pattern = re.compile("(?<=&sessionDataKey=)[a-z0-9\-]*")
session_key = None

for line in login_page_resp.iter_lines():
        match = re.search(key_pattern, line.decode())
        if match:
                session_key = match.group()

login_form_resp = session.post(
        url = os.getenv("login-form-target-url"),
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

session.cookies.set_cookie(
        cookie = rq.cookies.create_cookie(
                name = "CookieConsent",
                value = "{stamp:%27gRVY3rqRIx2YJ2RHmObsmUmG28xBYPMuFZWa8FCMSmDuKBJHF0QtZw==%27%2Cnecessary:true%2Cpreferences:false%2Cstatistics:false%2Cmarketing:false%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1673814469854%2Cregion:%27de%27}"))


callback_resp = session.post(
        url = callback_url,
        data = login_params)

print("Done")

# chart_resp = session.get(url = "https://www.solarweb.com/Chart/GetChartNew", data = {"pvSystemId": os.getenv("fronius-id"), "year": 2023, "month": 1, "day": 14, "interval": "day", "view": "production"}, cookies = session.cookies)

def chart_url(id, year, month, day):
        host = "https://www.solarweb.com/"
        file = "Chart/GetChartNew"
        params = {
                "id": id,
                "year": year,
                "month": month,
                "day": day}

        chart_url = f"{host}{file}&interval=day&view=production"