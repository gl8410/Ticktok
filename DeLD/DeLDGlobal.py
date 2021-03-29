import csv
from urllib.parse import urlencode
import requests
import os

Cookies="Hm_lvt_a0f9e240fdf94097d93363308f3939ca=1598364361,1598514268,1598854467,1599040973; spm=from=www.baidu.com; token=ew0KICAidHlwIjogIkpXVCIsDQogICJhbGciOiAiSFMyNTYiDQp9.ew0KICAiVG9rZW5JZCI6ICI3NzE2NmM5MzcwODU0NjE4YThlNGQ4MDFhMWUyMGFmNiIsDQogICJNZW1iZXJJZCI6IDY2OTIxNjAsDQogICJSYW1JZCI6IDE5NTcsDQogICJFeHBpcmVkVGltZSI6ICIyMDIwLTA5LTI2IDEwOjIyOjQ4Ig0KfQ.6ujH5ccdcOpGPdostarNmwSQXTagh4b7NaQ-vK17ZC4; SERVERID=9088ee2b3a500e9c1aa86d559c1988a4|1601000569|1601000553"

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
    if os.path.isfile(path):
        with open(path, mode="a+", encoding="utf-8", newline="") as f:
            fcsv = csv.writer(f)
            for d in data:
                fcsv.writerow(d)
    else:
        with open(path, mode="w", encoding="utf-8", newline="") as f:
            fcsv = csv.writer(f)
            fcsv.writerow(colnames)
            for d in data:
                fcsv.writerow(d)

def testPrint(dumps):
    print(dumps)