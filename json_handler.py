#!/usr/bin/env python

import requests
import json
import time

filename = "option_chain.json"


def get_OC_json(index_name='NIFTY'):
    url=''
    if index_name.upper() in ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNITFY"]:
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={index_name}"
    elif index_name.upper()=='USDINR':
        url = f"https://www.nseindia.com/api/option-chain-currency?symbol=USDINR"
    else:
        url = f"https://www.nseindia.com/api/option-chain-equities?symbol={index_name}"

    headers={'Connection': 'keep-alive','sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"','Accept': 'application/json, text/javascript, */*; q=0.01','DNT': '1','X-Requested-With': 'XMLHttpRequest','sec-ch-ua-mobile': '?0','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36','Content-Type': 'application/json; charset=UTF-8','Origin': 'https://niftyindices.com','Sec-Fetch-Site': 'same-origin','Sec-Fetch-Mode': 'cors','Sec-Fetch-Dest': 'empty','Referer': 'https://niftyindices.com/reports/historical-data','Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',}
    base_url='https://www.nseindia.com/option-chain'
    sess=requests.Session()
    request=sess.get(base_url, headers=headers, timeout=25)
    cookies=dict(request.cookies)
    data=sess.get(url, headers=headers, cookies=cookies, timeout=35)
    content = data.json()

    with open(filename, "w") as json_file:

        json.dump(content, json_file, indent=4)



def filter_OC_json_data():

    content = {}

    expiry_list = []
    strikes = []

    with open(filename, "r") as json_file:

        content = json.load(json_file)

    # get strikes, Spot and ATM strike
    # underlying value is given as float in NIFTY,BANKNIFTY api
    # and as text in USDINR api

    spot = float(content["records"]["underlyingValue"])
    strikes = content["records"]["strikePrices"]
    expiry_list = content["records"]["expiryDates"]

    # print(spot)
    # print(type(content))

    return (spot, strikes, expiry_list)


# get_OC_json('NIFTY')
# filter_OC_json_data()
