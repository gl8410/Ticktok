import csv
import random
import time
from urllib.parse import urlencode
import requests

# Self settings
# 在这里改存储路径
VodRank_storePath="./DxsVodRank/"
# 在这里改文件名
TaskName="0724_0731_Cos4"
# Cookies
VodRand_Cookie="Hm_lvt_f434dd2d0c8ecc66d832210642e3fa64=1597912234,1598071633,1598084116,1598143748; PHPFRONTSESSID=7fbl3a2gvqed06s2h4qjvljb45; _csrf=992a848fe2977443f932183723bc85031ae9fc813ec78a59786cf2b52a6a0f51a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22J8TKj550JpkWe4J0gKNaxAKFA4Y7ikwV%22%3B%7D; Hm_lpvt_f434dd2d0c8ecc66d832210642e3fa64=1598149147"

# Basic settings
VodRank_baseUrl = "https://www.daxiansuo.com/client/web/market/vodrankvideo?"
CosMetics_baseUrl = "https://www.daxiansuo.com/client/web/market/dypinfolist?"
VodRank_Header2=["VodTitle","VodLong","pub_time","CoverLink","VodLink","TicktockVID","Anchor","TicktockUID",
                 "Likes","Comments","ChangeRate","UpdateDate"]
Cosmetics_Header=["VodTitle","VodLong","pub_time","CoverLink","TicktockVID","Anchor","TicktockUID","Likes",
                  "Comments","ProductID","PlatForm","ProductLink","Sales","Price","Commission","ChangeRate",
                  "Links","Views","UpdateDate","Type"]
VodRank_headers = {
    "Host": "www.daxiansuo.com",
    "Referer": "https://www.daxiansuo.com/client/web/market/vodrank",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": VodRand_Cookie
}
CosMetics_headers = {
    "Host": "www.daxiansuo.com",
    "Referer": "https://www.daxiansuo.com/client/web/market/dypinfo",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": VodRand_Cookie
}
VodRank_get_params={
    "category": "1",
    "day": "2020-7-23",
    "month": "",
    "startDate": "",
    "endDate": "",
    "dateType": "day",
    "sAge": "",
    "eAge": "",
    "gender": "",
    "province": "",
    "city": "",
    "sTime": "",
    "eTime": "",
    "sLiked": "",
    "eLiked": "",
    "isProduct": "",
    "page": "",
    "limit": "10",
    "orderType": "desc",
    "orderField": "liked"
}
CosMetics_get_params={
    "category": "5",
    "source": "",
    "orderType": "desc",
    "orderField": "pv",
    "page": "4",
    "limit": "10",
    "dateType": "day",
    "day": "2020-08-16",
    "month": "",
    "startDate": "",
    "endDate": ""
}

# functions
def getJson(baseurl="",params={},headers={}):
    url=baseurl+urlencode(params)
    try:
        req=requests.get(url,headers=headers)
        if req.status_code==200:
            req.encoding="utf-8"
            return req.json()
    except requests.ConnectionError as e:
        print("Connection error",e.args)

def getRow(json):
    if json:
        items=json.get("data").get("list")
        for item in items:
            vod= {}
            vod["VodTitle"]=str(item.get("vintro"))
            vod["VodLong"]=item.get("vlong")
            timeSec=int(item.get("pub_dt"))
            timeDate=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(timeSec))
            vod["pub_time"]=str(timeDate)
            vod["CoverLink"]=str(item.get("cover"))
            vod["VodLink"]=str(item.get("dyvid2"))
            vod["TicktockVID"] = item.get("dyvid")
            vod["Anchor"]=str(item.get("nickname"))
            vod["TicktockUID"]= item.get("dyuid")
            vod["Likes"]=item.get("liked")
            vod["Comments"]=item.get("comments")
            vod["ChangeRate"]=item.get("lc")
            yield vod

def getCosmeticRow(json):
    if json:
        items=json.get("data").get("data")
        for item in items:
            vod={}
            vod["VodTitle"] = str(item.get("vintro"))
            vod["VodLong"] = item.get("vlong")
            timeSec = int(item.get("pub_dt"))
            timeDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timeSec))
            vod["pub_time"] = str(timeDate)
            vod["CoverLink"] = str(item.get("cover"))
            vod["TicktockVID"] = item.get("dyvid")
            vod["Anchor"] = str(item.get("nickname"))
            vod["TicktockUID"] = item.get("dyuid")
            vod["Likes"] = item.get("liked")
            vod["Comments"] = item.get("comments")
            vod["ProductID"]=item.get("pid")
            vod["PlatForm"]=item.get("platform")
            vod["ProductLink"] = str(item.get("dyvid2"))
            vod["Sales"] = item.get("sales")
            vod["Price"] = str(item.get("rprice"))
            vod["Commission"] = item.get("cos_fee")
            vod["ChangeRate"] = item.get("lc")
            vod["Links"] = item.get("vNum")
            vod["Views"] = item.get("pv")
            yield vod
# Cosmetics_Header=["VodTitle","VodLong","pub_time","CoverLink","TicktockVID","Anchor","TicktockUID","Likes",
#                   "Comments","ProductID","PlatForm","ProductLink","Sales","Price","Commission","ChangeRate","Links","Views",
#                   "UpdateDate","Type"]

def makeCsv(Test_data,headers):
    name=VodRank_storePath+TaskName+".csv"
    with open(name, mode="w", encoding="utf-8", newline="") as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        for r in Test_data:
            f_csv.writerow(r.values())

# Setting timespan here
def getJsonbySetting():
    m=7
    i=0
    data=[]
    for d in range(24,32):
#1
#        VodRank_get_params["day"]="2020"+"-"+str(m)+"-"+str(d)
#2
        CosMetics_get_params["day"]="2020"+"-"+str(m)+"-"+str(d)
        CosMetics_get_params["category"]=4
#
        for p in range(1,31):
            s=random.random()*5
            time.sleep(s)
#1
#            VodRank_get_params["page"]=str(p)
#            json=getJson(VodRank_baseUrl, VodRank_get_params,VodRank_headers)
#2
            CosMetics_get_params["page"]=str(p)
            json=getJson(CosMetics_baseUrl,CosMetics_get_params,CosMetics_headers)
#1
#            rows=getRow(json)
#2
            rows=getCosmeticRow(json)
            for r in rows:
#1
#                r["UpdateDate"]=VodRank_get_params["day"]
#2
                r["UpdateDate"]=CosMetics_get_params["day"]
                r["Type"]=CosMetics_get_params["category"]
                data.insert(0,r)
                print("正在下载第 "+str(i)+" 行数据!"+"\n")
                i=i+1
    print("下载完成，准备写入")
# 1
#   makeCsv(data,VodRank_Header2)
    makeCsv(data,Cosmetics_Header)

if __name__=="__main__":
    getJsonbySetting()