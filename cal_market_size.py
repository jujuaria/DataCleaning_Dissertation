from __future__ import division
import numpy as np
import pandas as pd

df = pd.read_csv("/Users/juju/downloads/temp/overall_post_2.csv",sep=',',header=0,infer_datetime_format = True, parse_dates = ['date_month','review_month'])

df["class_group"] = df["class_group"].fillna("economy")
df["demand"] = df["Supply"]*df["Occ"]*0.01
chicago = df[df["Market"].str.contains("Chicago")]
houston = df[df["Market"].str.contains("Houston")]
miami = df[df["Market"].str.contains("Miami")]

#Calculate market size (when market is defined as a city-class):
#def cal_market_size(df):
    #l=[]

    #for name, group in classes:
        
        #group ["market_size"] =max( df.groupby("date_month")["Supply"].sum())
        #l.append(group)
        
    #df = pd.concat(l,axis = 0)
    
    #df["market_share"] = df["demand"]/df["market_size"]
    #return df
    
#def cal_outside_size(df):
    #classes = df.groupby("class_group")

    #l=[]

    #for name, group in classes:
        #group = group.set_index("date_month")
        #class_size = group.groupby(group.index)[["demand"]].sum()
        #group = group.join(class_size,how='left', lsuffix='_left', rsuffix='_class')
        #l.append(group)
        
    #df = pd.concat(l,axis = 0)
    
    #return df
    
    
#### Soppuse consumers book hotel room-hight by room-night
def cal_market_size(df):
    
    months = df.groupby("date_month")
    l=[]
    for name, g in months:
        g["market_size"] = g["Supply"].sum() #### The total number of room-nights supplied
        g["inside_size"] = g["demand"].sum() #### The total number of room-nights sold
    
        l.append(g)
    
    df = pd.concat(l,axis = 0)
    
    return df
    
    
    #df = pd.concat(l,axis = 0)
    
    #df["market_share"] = df["demand"]/df["market_size"]
    #return df

chicago = cal_market_size(chicago)
houston = cal_market_size(houston)
miami = cal_market_size(miami)

chicago ["market_size"] = max(chicago["market_size"])
houston ["market_size"] = max(houston["market_size"])
miami ["market_size"] = max(miami["market_size"])



def cal_share(df):
    df ["market_share"] = df ["demand"]/df ["market_size"]
    df ["out_share"] = 1-(df["inside_size"]/df["market_size"])
    
    
    return df
    
chicago = cal_share(chicago)
houston = cal_share(houston)
miami = cal_share(miami)

def cal_group_share(df):
     
    groups = df.groupby("date_month")
    l1=[]
    for name,g in groups:
        classes = g.groupby(["class_group"])
        l2 =[]
        for name,c in classes:
            c["class_size"] = sum(c["demand"])
            l2.append(c)
        df_temp = pd.concat(l2,axis = 0)
        
        l1.append(df_temp)
    df = pd.concat(l1,axis = 0)
    df ["class_share"] = df["class_size"]/df["market_size"]
    return df

chicago = cal_group_share(chicago)  
houston = cal_group_share(houston)
miami = cal_group_share(miami)  



#chicago["outside_share"] = (chicago["market_size"] - chicago["demand_class"])/chicago["market_size"]
#houston["outside_share"] = (houston["market_size"] - houston["demand_class"])/houston["market_size"]
#miami["outside_share"] = (miami["market_size"] - miami["demand_class"])/miami["market_size"]
