from Vdatacleaning import loadingFromfolder
import pandas as pd

Datafolder = "./Pdata"

CosmeticColumns1=["Vname","UpName","Vlong","Source","Uptime","UpID","VID","RelatedVs","newDayviews","Sales",
                  "Price","Commission","TotalLikes","TotalComments","Changerate","PLink"]

CosmeticColumns2=["Vname","Vlong","Source","Uptime","UpID","VID","RelatedVs","newDayviews","Sales",
                  "Price","Commission","TotalLikes","TotalComments","Changerate","PLink"]

def getPdatadf():
    df1 = loadingFromfolder(Datafolder, CosmeticColumns1)
    df2 = loadingFromfolder(Datafolder + "/Noname", [])
    df2.columns = ['Vname', 'Vlong', 'Source', 'Uptime', 'UpID', 'VID',
                   'RelatedVs', 'newDayviews', 'Sales', 'Price', 'Commission',
                   'TotalLikes', 'TotalComments', 'Changerate', 'PLink', 'delete']
    df2 = df2.drop(columns=["delete"])
    df1 = pd.concat([df1, df2], axis=0)
    return df1

def getTimeSeries(df,pubtime):
    series=df[pubtime]
    series=series.dropna()
    tdf=pd.DataFrame({"Time":series})
    tdf["Time"]=tdf["Time"].astype("datetime64")
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

if __name__=="__main__":
    df=getPdatadf()
    df.to_excel("PdataTseries0923.xlsx")
    # df=getTimeSeries(df,"Uptime")
    # df.to_excel("PdataTseries0923.xlsx")