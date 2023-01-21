#!/usr/bin/env python3

import os
import json
import datetime as dt
from dotenv import load_dotenv

from fronius_scraper.fronius_session import FroniusSession

load_dotenv()

fsession = FroniusSession(
        user = os.getenv("username"),
        password = os.getenv("password"),
        id = os.getenv("fronius-id")
)

yesterday = dt.date.today() - dt.timedelta(days = 1)

json_out = json.dumps(fsession.get_chart(date = yesterday))

output_dir = "./"
output_file = output_dir + yesterday.strftime("%Y%m%d.json")

with open(output_file, "w") as outfile:
        outfile.write(json_out)