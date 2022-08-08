#!/usr/bin/env python

import requests
import json
import time

filename = "option_chain.json"


def get_OC_json(index_name):

    headers = {"User-Agent": "Mozilla/5.0"}

    #  when USD INR pair is added the word indices can be loaded as a conditional
    #  and be change to currency
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol={index_name}"

    r = requests.get(url, headers=headers)

    content = r.json()

    with open(filename, "w") as json_file:

        json.dump(content, json_file, indent=4)

    #  The below sleep command will interfere with tkinter mainloop
    #  and will reflect as a button freeze
    #  alternative is to use tkinter action function with 5000 ms delay

    #  time.sleep(5)
    #  print(type(content))

    return


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
