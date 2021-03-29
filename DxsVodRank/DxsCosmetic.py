import time
import random
from urllib.parse import urlencode
import requests
import csv
import os

Cookies="Hm_lvt_f434dd2d0c8ecc66d832210642e3fa64=1600567523,1600824785,1602148909,1602843025; PHPFRONTSESSID=1erp7ngmo6lv9ve1kh5f3v7ir6; _csrf=b43063b0b77e3750534ee4d4207edb4201100db3716582aa0f20c5d41f8edb4ca%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22r8G0DlIk_Jxa1zBiOioVRyETjTMLoG_D%22%3B%7D; Hm_lpvt_f434dd2d0c8ecc66d832210642e3fa64=1602843035"
DataPath="./Data/"
Categories=["4","5"]
Days=["2020-10-19","2020-8-23","2020-8-24","2020-9-10","2020-9-11"]
Lagging=4

CosmeticBaseurl="https://www.daxiansuo.com/client/web/market/dypinfolist?"


CosmeticColumns=["Vname","UpName","Vlong","Source","Uptime","UpID","VID","RelatedVs","newDayviews","Sales",
                  "Price","Commission","TotalLikes","TotalComments","Changerate","PLink"]

CosmeticsHeaders = {
    "Host": "www.daxiansuo.com",
    "Referer": "https://www.daxiansuo.com/client/web/market/dypinfo",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": Cookies
}

CosmeticParams={
    "category": "4",
    "source": "",
    "orderType": "desc",
    "orderField": "pv",
    "page": "3",
    "limit": "10",
    "day": "2020-9-7",
    "month": "",
    "startDate": "",
    "endDate": ""
}

def getCosmeticRow(json):
    if json:
        items=json.get("data").get("data")
        for item in items:
            vod=[]
            vod.append(str(item.get("vintro")))
            vod.append(str(item.get("nickname")))
            vod.append(item.get("vlong"))
            vod.append(str(item.get("platform")))
            timeSec = int(item.get("pub_dt"))
            timeDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timeSec))
            vod.append(str(timeDate))
            vod.append(item.get("dyuid"))
            vod.append(item.get("dyvid"))
            vod.append(item.get("vNum"))
            vod.append(item.get("pv"))
            vod.append(item.get("sales"))
            vod.append(item.get("rprice"))
            vod.append(item.get("cos_fee"))
            vod.append(item.get("liked"))
            vod.append(item.get("comments"))
            vod.append(item.get("lc"))
            vod.append(item.get("dyvid2"))
            yield vod

def getJson(baseurl="",params={},headers={}):
    url=baseurl+urlencode(params)
    try:
        req=requests.get(url,headers=headers)
        if req.status_code==200:
            req.encoding="utf-8"
            return req.json()
    except requests.ConnectionError as e:
        print("Connection error",e.args)

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

def slowDown():
    time.sleep(random.random() * Lagging)

def stopForAwhile2(index,pIndex,limit=20):
    if len(pIndex)>limit:
        stoppoint = len(pIndex) // 2
        if index == pIndex[stoppoint]:
            stopmins(10)

def stopmins(mins):
    print("我太累了，休息一会~")
    t = mins*60 + random.random() * 199
    time.sleep(t)
    print("休息好了，继续干活")

def getCosmetic():
    for d in Days:
        CosmeticParams["day"] = d
        for t in Categories:
            CosmeticParams["category"] = t
            path = DataPath + str(d) + "_" + str(t) + ".csv"
            index = [m for m in range(1, 51)]
            random.shuffle(index)
            for i in index:
                data=[]
                CosmeticParams["page"] = str(i)
                json = getJson(CosmeticBaseurl, CosmeticParams, CosmeticsHeaders)
                slowDown()
                print("正在处理数据, "+str(d)+" 天, "+str(t)+" 类第 " +str(i)+" 页.")
                rows = getCosmeticRow(json)
                for r in rows:
                    data.append(r)
                store2CSV(path,CosmeticColumns,data)
                stopForAwhile2(i, index, limit=20)

if __name__=="__main__":
    getCosmetic()