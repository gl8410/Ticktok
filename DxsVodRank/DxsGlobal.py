import csv
from urllib.parse import urlencode
import requests
import os

def getReq(url="", header={}, paras={}):
    url = url + urlencode(paras)
    try:
        req = requests.get(url, headers=header)
        if req.status_code == 200:
            return req
    except requests.ConnectionError as e:
        return None
        print("Connection error", e.args)


def store2CSV(path, colnames, data):
    with open(path, mode="w", encoding="utf-8", newline="") as f:
        fcsv = csv.writer(f)
        fcsv.writerow(colnames)
        for d in data:
            fcsv.writerow(d)