import os
import re
import pandas as pd

OutPutfile="Vmerged0925.xlsx"
Tsfile="/VTimeSeries.xlsx"
Datafolder = "./Vdata"
Vcolumns = ["Vname", "CoverLink", "Vlong", "Vlink", "VID", "Tag", "VLikes", "Vcomments", "Vtransmits", "HotWords",
            "PubTime", "UpdateTime", "AnchorID", "ACoverLink", "AnchorName", "TotalFans", "AUID", "ASex",
            "ATag", "ABriefing", "AnchorIndex", "Aworks", "AAllLikes", "AAvgLikes", "AAvgComments", "AAvgTransmit",
            "MaleP", "FemaleP", "MaleAge", "FemaleAge", "Top10city", "Top10cityP", "Citylevel", "CitylevelP",
            "Top5Province", "Top5ProvinceP"]

SelectColums = ["Vname", "CoverLink", "Vlong", "Vlink", "VID", "Tag", "VLikes", "Vcomments", "Vtransmits", "HotWords",
                "PubTime", "UpdateTime", "AnchorID", "ACoverLink", "AnchorName", "TotalFans", "AUID", "ASex",
                "ATag", "ABriefing", "AnchorIndex", "Aworks", "AAllLikes", "AAvgLikes", "AAvgComments", "AAvgTransmit",
                "MaleP", "FemaleP", "MaleAge", "FemaleAge", "Top10city", "Top10cityP", "Citylevel", "CitylevelP",
                "Top5Province", "Top5ProvinceP"]

def loadingFromfolder(fdir,columns):
    df = pd.DataFrame(columns=columns)
    if os.listdir(fdir):
        for f in os.listdir(fdir):
            if os.path.isfile(fdir+"/"+f):
                dfin = pd.read_csv(fdir + "/" + f, header=0)
                df = pd.concat([df, dfin], axis=0)
    return df

def changeMintoSecond(time):
    time=str(time)
    time=re.sub("秒","",time)
    if re.search("分",time)!=None:
        nums=time.split("分")
        sec=int(nums[0])*60+int(nums[1])
    else:
        try:
            sec = int(time)
        except:
            sec=0
    return sec

def changeThousandtoNumber(amount):
    amount=str(amount)
    if re.search("亿", amount) != None:
        amount = re.sub("亿", "", amount)
        nums=amount.split(".")
        num=int(nums[0])*100000000+int(nums[1])*10000000
    elif re.search("\.",amount)!=None:
        amount = re.sub("w", "", amount)
        nums=amount.split(".")
        num=int(nums[0])*10000+int(nums[1])*1000
    else:
        try:
            num = int(amount)
        except:
            num=0
    return num

def changeSextoNums(sex):
    sex=str(sex)
    if sex=="女":
        return 2
    elif sex=="男":
        return 1
    else:
        return 0

def changetoInt(num):
    num =str(num)
    try:
        num = int(num)
    except:
        num = 0
    return 0

def formatDf(df):
    print("Before cleaning!")
    print(df.dtypes)
    df.fillna(0)
    df["Vname"]=df["Vname"].astype("string")
    df["Vlong"] = df["Vlong"].apply(changeMintoSecond)
    df["VLikes"]=df["VLikes"].apply(changeThousandtoNumber)
    df["Vcomments"] = df["Vcomments"].apply(changeThousandtoNumber)
    df["Vtransmits"] = df["Vtransmits"].apply(changeThousandtoNumber)
    df["HotWords"] = df["HotWords"].astype("string")
    df["PubTime"] = df["PubTime"].astype("datetime64")
    df["UpdateTime"] = df["UpdateTime"].astype("datetime64")
    df["AnchorName"] = df["AnchorName"].astype("string")
    df["TotalFans"]=df["TotalFans"].apply(changeThousandtoNumber)
    df["ASex"] = df["ASex"].apply(changeSextoNums)
    df["ABriefing"] = df["ABriefing"].astype("string")
    df["AAllLikes"] = df["AAllLikes"].apply(changeThousandtoNumber)
    df["AAvgLikes"] = df["AAvgLikes"].apply(changeThousandtoNumber)
    df["AAvgComments"] = df["AAvgComments"].apply(changeThousandtoNumber)
    df["AAvgTransmit"] = df["AAvgTransmit"].apply(changeThousandtoNumber)
    print("After cleaning!")
    print(df.dtypes)
    return df

def selectColums(df,columns):
    df=df[columns]
    return df

def getTimeSeries(df,pubtime):
    series=df[pubtime]
    series=series.dropna()
    tdf=pd.DataFrame({"Time":series})
    tdf["Time"] = tdf["Time"].astype("datetime64")
    tdf["hour"]=tdf["Time"].apply(lambda x:x.strftime("%Y-%m-%d %H"))
    agg=tdf.groupby("hour").agg("count")
    agg["index"]=agg.index
    times = pd.date_range('30/8/2020', periods=600, freq='H')
    odf=pd.DataFrame({"Time":times})
    odf["index"]=odf["Time"].apply(lambda x:x.strftime("%Y-%m-%d %H"))
    odf=odf.merge(agg,how="left",on="index")
    odf=odf.fillna(0)
    odf.reset_index(drop=True)
    odf=odf.drop(columns=["Time_x"])
    odf.columns=["Hour","Vnumbers"]
    return odf

def write2file():
    df=loadingFromfolder(Datafolder,Vcolumns)
    df=formatDf(df)
    df=selectColums(df,Vcolumns)
    df.to_excel(OutPutfile)

def writeTS2file():
    df=loadingFromfolder(Datafolder,Vcolumns)
    df=formatDf(df)
    df = selectColums(df, Vcolumns)
    tdf=getTimeSeries(df,"PubTime")
    tdf.to_excel("VTimeSeries.xlsx")


if __name__=="__main__":
#    writeTS2file()
    write2file()






