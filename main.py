#!/usr/bin/python

import json
import urllib2
import base64
import os.path

covid_api_url = 'https://api.covid19api.com/live/country/south-africa'

recent_updates = json.loads(urllib2.urlopen(urllib2.Request(
    covid_api_url,
    headers={"Accept": 'application/json'}
)).read())

country_stats = recent_updates[-1]

confirmed = country_stats["Confirmed"]
deaths = country_stats["Deaths"]
recovered = country_stats["Recovered"]
active = country_stats["Active"]

print 'C:{} D:{} A:{}'.format(confirmed, deaths, active)
