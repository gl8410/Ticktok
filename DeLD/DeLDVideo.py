import random
import re
import time
from DeLDGlobal import getReq, Cookies, store2CSV
from lxml import etree

VideoListHeaders = {
    "Host": "https://dy.delidou.com/",
    "Referer": "https://dy.delidou.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": Cookies
}

videoListParams={
    "keyword": "",
    "cateid": "18",
    "like": "0",
    "comment": "0",
    "share": "0",
    "hours": "24",
    "duration": "0",
    "sku": "0",
    "sticker": "0",
    "citylabel": "0",
    "agelabel": "0",
    "genderlabel": "0",
    "province": "0",
    "city": "0",
    "sort": "1",
    "segs": "",
    "page": "1"
}

WebcastListParams={
    "cateid": "18",
    "period": "undefined",
    "datecode": "20200831",
    "ajax": "1",
    "sort": "8",
    "page": "11"
}

videoColnames=["Vname","CoverLink","Vlong","Vlink","VID","Tag","VLikes","Vcomments","Vtransmits","HotWords",
               "PubTime","UpdateTime","AnchorID","ACoverLink","AnchorName","TotalFans","AUID","ASex",
               "ATag","ABriefing","AnchorIndex","Aworks","AAllLikes","AAvgLikes","AAvgComments","AAvgTransmit"]

videoColnames2=["Vname","CoverLink","Vlong","Vlink","VID","Tag","VLikes","Vcomments","Vtransmits","HotWords",
               "PubTime","UpdateTime","AnchorID","ACoverLink","AnchorName","TotalFans","AUID","ASex",
               "ATag","ABriefing","AnchorIndex","Aworks","AAllLikes","AAvgLikes","AAvgComments","AAvgTransmit",
                "MaleP","FemaleP","MaleAge","FemaleAge","Top10city","Top10cityP","Citylevel","CitylevelP",
                "Top5Province","Top5ProvinceP"]

WebcastColumns=["Cname","Aname","Fans","Starttime","Endtime","Clong","AvgStayTime","TotalWatch","Peak","Products",
                "GiftUV","GainConcerns","NewFans","TotalCommission","WaveIncome","Sales","Amount","TimeSeries","WaveSeries",
                "LikesSeries","OnlineUserSeries","AddFansSeries","Male/Female","MaleMapping","FemaleMapping",
                "Top10Citites","Top10CitiesProp","AudienceSource","WordCloud","Constellation","ConstellationProp"
]

videoHeaders={
    "Host": "dy.delidou.com",
    "Referer": "https://dy.delidou.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    "Cookie": Cookies
}

baseUrl="https://dy.delidou.com/"
userBaseUrl="user/detail/"
videoBaseUrl="video/detail/"
WebcastBaseUrl="webcast/detail/"
videoListBaseUrl="video/list/search?"
WebcastListBaseUrl="rank/webcast/marketing?"
videoPath="./Data/Hotvideo20200925.csv"
WebcastPath="./Data/Webcast"
slowindex=4
datacodes=["20200912","20200911","20200910"]


def getVideoList(Req):
    html=etree.HTML(Req.text)
    list=html.xpath('//td[@class="video-td"]/a[1]/@data-href')
#    list2=re.findall('/video/detail/\d+/\d+/\d+(?=")',Req.text,re.S)
    return list

def getWebcastList(Req):
    html = etree.HTML(Req.text)
    list = html.xpath('//div[contains(@class,"info-area")]/a/@href')
    #    list2=re.findall('/video/detail/\d+/\d+/\d+(?=")',Req.text,re.S)
    return list

def getVideoDetail(url):
    slowDown()
    titles = url.split('/')
    url=baseUrl+url
    req=getReq(url,videoHeaders)
    if req is None:
        return [""]
    html=etree.HTML(req.text)
    AnchorID=titles[3]
    VID=titles[5]
    data=[]
    coverlink=ScratchTry(html,'//div[@class="info-top-row"]/img/@src')
    tag=ScratchTry(html,'//span[@class="title-tag"]/text()')
    vName=ScratchTry(html,'//span[@class="title-content"]/text()')
    likes=ScratchTry(html,'//span[@class="interaction-item"][1]/span/text()')
    comments=ScratchTry(html,'//span[@class="interaction-item"][2]/span/text()')
    transmit =ScratchTry(html,'//span[@class="interaction-item"][3]/span/text()')
    hotwords=html.xpath('//span[@class="hot-words"]/text()')
    words=""
    for w in hotwords:
        words=words+w+"/"
    words=words[:-1]
    Vlong=ScratchTry(html,'//span[contains(@class,"time-value")][1]/text()')
    PubTime=ScratchTry(html,'//span[contains(@class,"time-value")][2]/text()')
    UpdateTime=ScratchTry(html,'//span[contains(@class,"time-value")][3]/text()')
    VLink= ScratchTry(html,'//a[(@class="play-video")][1]/@href')
    data.insert(0,vName)
    data.insert(0,coverlink)
    data.insert(0,Vlong)
    data.insert(0,VLink)
    data.insert(0,VID)
    data.insert(0,tag)
    data.insert(0,likes)
    data.insert(0,comments)
    data.insert(0,transmit)
    data.insert(0,words)
    data.insert(0,PubTime)
    data.insert(0,UpdateTime)
    data.insert(0,AnchorID)
    data.reverse()
    userLink = baseUrl+userBaseUrl+AnchorID
    detail = getVedioAnchor(userLink)
    data = data +detail
    # purl=re.sub('detail','detail/persona',url)
    # persona=getVideoPersona(purl)
    # data = data + persona
    return data

def getVideoPersona(url):
    slowDown()
    req = getReq(url, videoHeaders)
    if req is None:
        return [""]
    if re.search('数据不足',req.text,re.S)!=None:
        return [""]
    html = etree.HTML(req.text)
    sRatio=["",""]
    ratio=html.xpath('//div[contains(@class,"name-box")]/span[2]/text()')
    sRatio=getInfos(ratio,sRatio)
    manp=ReTry(req.text,r"(?<=y1: JSON\.parse\('\[)\d{1,2}\..*?(?=\]'\),)")
    manp=re.sub(",","/",manp)
    womanp=ReTry(req.text,r"(?<=y2: JSON\.parse\('\[)-?\d{1,2}\..*?(?=\]'\),)")
    womanp=re.sub("-","",womanp)
    womanp = re.sub(",", "/", womanp)
    top10city=ReTry(req.text,r"""(?<=data: JSON\.parse\('\[").*?(?="\]'\))""")
    top10city = re.sub("\",\"", "/", top10city)
    top10cityp=ReTry(req.text,r"(?<=data: JSON\.parse\('\[)0\..*?(?=\]'\)\.r)")
    top10cityp=re.sub(",","/",top10cityp)
    citylevelandp=["",""]
    citylevelandp=ReTrylist(req.text,r"(?<=data: JSON\.parse\('\[).*?(?=]'\),)")
    citylevel=parseJsonName(citylevelandp[0])
    citylevelp = parseJsonValue(citylevelandp[0])
    provincelevel=parseJsonName(citylevelandp[1])
    provincelevelp=parseJsonValue(citylevelandp[1])
    data=[]
    data.append(sRatio[0])
    data.append(sRatio[1])
    data.append(manp)
    data.append(womanp)
    data.append(top10city)
    data.append(top10cityp)
    data.append(citylevel)
    data.append(citylevelp)
    data.append(provincelevel)
    data.append(provincelevelp)
    return data

def parseJsonName(json):
    if json:
        d = ""
        ls=re.findall('(?<={"name":").*?(?=",")',json,re.S)
        if ls:
            for l in ls:
                d=d+str(l)+"/"
        d = d[:-1]
        return d
    else:
        return ""

def parseJsonValue(json):
    if json:
        d = ""
        ls=re.findall('(?<=","value":).*?(?=})',json,re.S)
        if ls:
            for l in ls:
                d=d+str(l)+"/"
        d=d[:-1]
        return d
    else:
        return ""


def getWebcastdetail(url):
    slowDown()
    url=url[3:]
    url=baseUrl+url
    req=getReq(url,videoHeaders)
    if req is None:
        return [""]
    html=etree.HTML(req.text)
    cname=ScratchTry(html,'//div[contains(@class,"hot-top-title")]/a/text()')
    aname=ScratchTry(html,'//span[contains(@class,"hot-top-info-name")]/a/text()')
    fans=ScratchTry(html,'//span[contains(@class,"hot-top-info1")]/text()')
    fans=fans[4:]
    info=html.xpath('//div[contains(@class,"hot-top-info2")]/p/text()')
    infos=["NA1","NA2","NA3","NA4"]
    infos=getInfos(info,infos)
    Stime=infos[0]
    etime=infos[1]
    clong=infos[2]
    avgstay=infos[3]
    info2=html.xpath('//div[@class="hot-left-bottom"]/div/div/p[2]/text()')
    infos2=["NA1","NA2","NA3","NA4","NA5","NA6","NA7","NA8","NA9","NA10"]
    infos2=getInfos(info2,infos2)
    ttwatch=infos2[0]
    peak=infos2[1]
    pros=infos2[2]
    gift=infos2[3]
    gainconcern=infos2[4]
    newfans=infos2[5]
    ttcommission=infos2[6]
    waveincome=infos2[7]
    sales=infos2[8]
    amount=infos2[9]
    data=[]
    data.insert(0,cname)
    data.insert(0, aname)
    data.insert(0, fans)
    data.insert(0, Stime)
    data.insert(0, etime)
    data.insert(0, clong)
    data.insert(0, avgstay)
    data.insert(0, ttwatch)
    data.insert(0, peak)
    data.insert(0, pros)
    data.insert(0, gift)
    data.insert(0, gainconcern)
    data.insert(0, newfans)
    data.insert(0, ttcommission)
    data.insert(0, waveincome)
    data.insert(0, sales)
    data.insert(0, amount)
    data.reverse()
    trendUrl=re.sub('detail','detail/trend',url)
    personaUrl = re.sub('detail', 'detail/persona', url)
    data1=getTrend(trendUrl)
#   data2=getPersona(personaUrl) # +data2
    data = data +data1
    return data
    # "Cname", "Aname", "Fans", "Starttime", "Endtime", "Clong", "AvgStayTime", "TotalWatch", "Peak", "Products",
    # "GiftUV", "GainConcerns", "NewFans", "TotalCommission", "WaveIncome", "Sales", "Amount"
def getTrend(url):
    slowDown()
    req=getReq(url,videoHeaders)
    if req is None:
        return [""]
    content=re.findall(r"(?<=JSON\.parse\('\[).*?(?=\]'\))",req.text,re.S)
    infos=["","","","",""]
    infos=getInfoslist(content,infos)
    return infos
                # "TimeSeries",
                # "LikesSeries","WaveSeries","OnlineUserSeries","AddFansSeries"
def getPersona(url):
    slowDown()
    req = getReq(url, videoHeaders)
    if req is None:
        return [""]
    html = etree.HTML(req.text)
    sps=["","","","","","",""]
    script=html.xpath('//script')
    if len(script)==6:
        sps=getInfostext(script,sps)
    else:
        return ["","","","","","","","",""]
    sexs=["",""]
    sex=re.findall(r"(?<=value: )\d+(?=-)",sps[0])
    sexs=getInfos(sex,sexs)
    sexratio=str(sexs[0])+"/"+str(sexs[1])
    MaleMap=ReTry(sps[1],r"(?<=y1: JSON\.parse\('\[).+?(?=\]'\))")
    FemaleMap = ReTry(sps[1], r"(?<=y2: JSON\.parse\('\[).+?(?=\]'\))")
    FemaleMap =re.sub('--',"-",FemaleMap)
    topcities=ReTry(sps[2], r"""(?<=data: JSON\.parse\('\[)"\w{2,3}"-"\w{2,3}".+?(?=\]'\))""")
    topcityprop=ReTry(sps[2], r"(?<=data: JSON\.parse\('\[)\d{1,2}.\d+-\d{1,2}.+?(?=\]'\))")
    Audisource=ReTry(sps[3],r"""(?<=data: JSON\.parse\('\[){"name":.+?(?=\]'\))""")
    wordcloud=ReTry(sps[4],r"""(?<=data: JSON\.parse\('\[){"name":.+}(?=\]'\))""")
    constellation=ReTry(sps[5],r"""(?<=name: JSON\.parse\('\[)"\w{3,3}".+?(?=\]'\))""")
    constprop=ReTry(sps[5],r"""(?<=percent: JSON\.parse\('\[)"\d{1,2}.\d{1,2}%".+?(?=\]'\))""")
    data=[]
    data.insert(0,sexratio)
    data.insert(0, MaleMap)
    data.insert(0, FemaleMap)
    data.insert(0, topcities)
    data.insert(0, topcityprop)
    data.insert(0, Audisource)
    data.insert(0, wordcloud)
    data.insert(0, constellation)
    data.insert(0, constprop)
    data.reverse()
    return data

# "Male/Female","MaleMapping","FemaleMapping",
#                 "Top10Citites","Top10CitiesProp","AudienceSource","WordCloud","Constellation","ConstellationProp"

def getVedioAnchor(url):
    slowDown()
    req = getReq(url, videoHeaders)
    if req is None:
        return [""]
    html = etree.HTML(req.text)
    AnchorCoverLink=ScratchTry(html,'//div[@class="clearfix"]/div/img/@src')
    Anchor=ScratchTry(html,'//div[@class="clearfix"]/div[contains(@class,"id-txt")]/dl/dt/text()[1]')
    Anchor=str(Anchor)
    Anchor=tidyUpName(Anchor)
#   Anchor="".join(re.findall('\w*?',Anchor))
#   Anchor=Anchor.strip("rn")
    AUID = ScratchTry(html,'//div[@class="clearfix"]/div[contains(@class,"id-txt")]//dd[1]/text()')
    AUID = str(AUID)[4:]
    ASEX = ScratchTry(html,'//div[@class="clearfix"]/div[contains(@class,"id-txt")]//dd[2]/text()')
    ASEX=str(ASEX)[3:]
    ATag = ScratchTry(html,'//div[@class="clearfix"]/div[contains(@class,"id-txt")]//span[@class="type-item"]/text()')
    Abriefing = ScratchTry(html,'//div[@class="id-introductio"]/text()')
    Abriefing=str(Abriefing)
    Abriefing=tidyUpBriefing(Abriefing)
    AIndex=ScratchTry(html,'//div[@class="data-value"]/text()')
    datainfo=["NA1","NA2","NA3","NA4","NA5","NA6"]
    info=html.xpath('//div[@class="item-info"]/p[@class="data-value"]/text()')
    datainfo=getInfos(info,datainfo)
    AFans=datainfo[0]
    Aworks=datainfo[1]
    AAllLikes=datainfo[2]
    AAvgLikes=datainfo[3]
    AAvgComments=datainfo[4]
    AAvgTransmit=datainfo[5]
    data=[]
    data.insert(0,AnchorCoverLink)
    data.insert(0,Anchor)
    data.insert(0,AFans)
    data.insert(0,AUID)
    data.insert(0,ASEX)
    data.insert(0,ATag)
    data.insert(0,Abriefing)
    data.insert(0,AIndex)
    data.insert(0,Aworks)
    data.insert(0,AAllLikes)
    data.insert(0,AAvgLikes)
    data.insert(0,AAvgComments)
    data.insert(0,AAvgTransmit)
    data.reverse()
    return data

def ScratchTry(html,xpath):
    try:
        content=html.xpath(xpath)
        if content==None:
            return ""
        else:
            return str(content[0])
    except:
        return ""

def ReTry(html,text):
    try:
        content = re.search(text,html,re.S)
        if content == None:
            return ""
        else:
            return content.group()
    except:
        return ""

def ReTrylist(html,text):
    try:
        content = re.findall(text,html,re.S)
        if content == None:
            return ""
        else:
            return content
    except:
        return ""

def getInfos(info,infos):
    try:
        for i,l in enumerate(info):
            infos[i]=str(l)
    except:
        return infos
    return infos

def getInfostext(info,infos):
    try:
        for i,l in enumerate(info):
            t=l.text
            t=re.sub(',','-',t)
            infos[i]=t
    except:
        return infos
    return infos

def getInfoslist(info,infos):
    try:
        for i,l in enumerate(info):
            l=re.sub(',','-',l)
            infos[i]=l
    except:
        return infos
    return infos


def tidyUpBriefing(name=""):
    name=name.strip()
    name=name.strip("\r\n")
    name=name.strip()
    name=name.replace("\n","\\")
    return name[3:]

def tidyUpName(name=""):
    name=name.strip()
    name=name.strip("\r\n")
    name=name.strip()
    return name

def slowDown():
    time.sleep(2+random.random() * slowindex)

def stopForAwhile3(index,pIndex,limit=20):
    if len(pIndex)>limit:
        stoppoint = len(pIndex) // 3
        stoppoint2 = stoppoint*2
        if index == pIndex[stoppoint] or index == pIndex[stoppoint2]:
            stopmins(40)

def stopForAwhile2(index,pIndex,limit=10):
    if len(pIndex)>limit:
        stoppoint = len(pIndex) // 2
        if index == pIndex[stoppoint]:
            stopmins(40)


def stopmins(mins):
    print("我太累了，休息一会~")
    t = mins*60 + random.random() * 499
    time.sleep(t)
    print("休息好了，继续干活")

def GetVideoData():
    listurl=baseUrl+videoListBaseUrl
    pIndex = [n for n in range(1, 56)]
    random.shuffle(pIndex)
    for i in pIndex:
        data = []
        stopForAwhile3(i,pIndex)
        videoListParams["page"]=i
        Req=getReq(listurl,videoHeaders,videoListParams)
        list=getVideoList(Req)
        print("正在处理热门视频第 "+str(i)+" 页.")
        for l in list:
            row = getVideoDetail(l)
            data.insert(0,row)
            print("正在获取数据："+str(l))
        print("正在存储数据")
#        store2CSV(videoPath, videoColnames, data)
        store2CSV(videoPath, videoColnames2, data)
        print("存储完成")


def GetWebcastData():
    listurl=baseUrl+WebcastListBaseUrl
    for d in datacodes:
        WebcastListParams["datecode"]=d
        path = WebcastPath + str(d) + ".csv"
        # top is 20 pages
        pIndex=[n for n in range(1,21)]
        random.shuffle(pIndex)
        for i in pIndex:
            data = []
            stopForAwhile3(i, pIndex,9)
            WebcastListParams["page"] = i
            Req=getReq(listurl,videoHeaders,WebcastListParams)
            list=getWebcastList(Req)
            if list is not None:
                print("正在处理直播带货第 " +str(d)+" 天第 "+ str(i) + " 页.")
                for l in list:
                    row=getWebcastdetail(l)
                    data.insert(0,row)
                    print("正在获取数据：" + str(l))
            print("正在存储数据 " + str(d))
            store2CSV(path, WebcastColumns, data)
            print("存储完成")
        stopmins(64)

if __name__=="__main__":
    GetVideoData()
#   GetWebcastData()













