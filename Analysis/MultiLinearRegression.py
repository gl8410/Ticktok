import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy as sp
from sklearn.metrics import mean_squared_error as mse
from sklearn.model_selection import train_test_split
import time
from sklearn.linear_model import LinearRegression
from datetime import timedelta

Datasource="Vmerged0925.xlsx"
Output="MLRegression0925.xlsx"

def cleanVdata(df):
    columns=["Vname",'Vlong','VLikes','Vcomments', 'Vtransmits', 'PubTime','UpdateTime','TotalFans',
             'ASex','ABriefing','AnchorIndex', 'Aworks','AAllLikes', 'AAvgLikes', 'AAvgComments',
             'AAvgTransmit']
    df=df.loc[:,columns]
    df = df.dropna()
    df["Nlong"] = df["Vname"].apply(len)
    df["Blong"] = df["ABriefing"].apply(len)
    df=df.drop(columns=["Vname",'ABriefing'])
    df["PubTime"]=df["PubTime"].astype("datetime64")
    df["UpdateTime"] = df["UpdateTime"].astype("datetime64")
    df["Period"]=df["UpdateTime"]-df["PubTime"]
    df["Period"]=df["Period"].apply(timedelta.total_seconds)
    df = df.drop(columns=["PubTime", 'UpdateTime'])
    df["Aworks"] = df["Aworks"].astype("double")
    df["AvgLSpeed"] = (df["VLikes"] * 3600) / df["Period"]
    return df

# def period2Second(time):
#     h,m,s=str(time).split(":")
#     return int(h)*3600 + int(m)*60 + int(s)



if __name__=="__main__":
    df = pd.DataFrame()
    df=pd.read_excel(Datasource,sheet_name="Sheet1")
    df=cleanVdata(df)



