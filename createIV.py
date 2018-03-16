from __future__ import division
import numpy as np
import pandas as pd

df = pd.read_csv("/Users/juju/downloads/temp/overall_post_2.csv",sep=',',header=0,infer_datetime_format = True, parse_dates = ['date_month','review_month'])

round_threshold = [1.25,1.75,2.25,2.75,3.25,3.75,4.25,4.75]
round_width = 0.1 #### Neet robust check 

df["round_up"] = ((round_threshold [1]<=df["accum_rating"]) & (df["accum_rating"]<round_threshold [1]+round_width))| ((round_threshold [2]<=df["accum_rating"]) & (df["accum_rating"]<round_threshold [2]+ round_width)) | ((round_threshold [3]<=df["accum_rating"]) & (df["accum_rating"]<round_threshold [3]+round_width))|((round_threshold [4]<=df["accum_rating"]) & (df["accum_rating"]<round_threshold [4]+round_width))|((round_threshold [5]<=df["accum_rating"]) & (df["accum_rating"]<round_threshold [5]+round_width))|((round_threshold [6]<=df["accum_rating"]) & (df["accum_rating"]<round_threshold [6]+round_width))|((round_threshold [7]<=df["accum_rating"]) & (df["accum_rating"]<round_threshold [7]+round_width))|((round_threshold [0]<=df["accum_rating"]) & (df["accum_rating"]<round_threshold [0]+round_width))

df["round_down"] = ((round_threshold [1]>df["accum_rating"]) & (df["accum_rating"]>round_threshold [1]-round_width))| ((round_threshold [2]>df["accum_rating"]) & (df["accum_rating"]>round_threshold [2]- round_width)) | ((round_threshold [3]>df["accum_rating"]) & (df["accum_rating"]>round_threshold [3]-round_width))|((round_threshold [4]>df["accum_rating"]) & (df["accum_rating"]>round_threshold [4]-round_width))|((round_threshold [5]>df["accum_rating"]) & (df["accum_rating"]>round_threshold [5]-round_width))|((round_threshold [6]>df["accum_rating"]) & (df["accum_rating"]>round_threshold [6]-round_width))|((round_threshold [7]>df["accum_rating"]) & (df["accum_rating"]>round_threshold [7]-round_width))|((round_threshold [0]>df["accum_rating"]) & (df["accum_rating"]>round_threshold [0]-round_width))

df["class_group"] = df["class_group"].fillna("economy") #### Missing "class" properties are economy class 

df["demand"] = df["Supply"]*df["Occ"]*0.01    #### number of room-nights sold



class gen_IV():
    
    #### This class calculates market size and create IVs for demand estimation
    
    def __init__(self,df):
        self.data = df
        self.market_share = pd.DataFrame()
        self.group_share = pd.DataFrame()
        
    #### replace zero with NaN in order to calculate mean later
       
    def replace_zero(self):
        
        df = self.data
        df ["location_mean"] = df ["location_mean"].replace(0,np.NaN)
        df ["service_mean"] = df ["service_mean"].replace(0,np.NaN)          
        df ["cleanliness_mean"] = df ["cleanliness_mean"].replace(0,np.NaN)
        df ["roomsQuality_mean"] = df ["roomsQuality_mean"].replace(0,np.NaN)
        df ["sleepQuality_mean"] = df ["sleepQuality_mean"].replace(0,np.NaN)
        df ["value_mean"] = df ["value_mean"].replace(0,np.NaN)
        df ["month_rating_mean"] = df ["month_rating_mean"].replace(0,np.NaN)
        df ["accum_rating"] = df ["accum_rating"].replace(0,np.NaN)
    
        return self.data
        
    #### Calculate market share in each city
     
    def cal_market_share(self):
         
         
         
         df = self.data
         
         months = df.groupby("date_month")
         l = []
         for name, g in months:
             g["market_size"] = g["Supply"].sum() #### The total number of room-nights supplied
             g["inside_size"] = g["demand"].sum() #### The total number of room-nights sold
             g["local_service_mean"] = g["service_mean"].mean()
             g["local_cleanliness_mean"] = g["cleanliness_mean"].mean()
             g["local_value_mean"] = g["value_mean"].mean()
             g["local_location_mean"] = g["location_mean"].mean()
             g["local_roomsquality_mean"] = g["roomsQuality_mean"].mean()
             g["local_sleepquality_mean"] = g["sleepQuality_mean"].mean()
             g["num_of_hotels_per_citymonth"] = g["shareid"].nunique()
             l.append(g)
    
         df = pd.concat(l,axis = 0)
         df ["market_size"] = max(df["market_size"])
         df ["market_share"] = df ["demand"]/df ["market_size"]
         df ["out_share"] = 1-(df["inside_size"]/df["market_size"])
         
         self.market_share = df
         return self.market_share
    
         #### Calculate market share for each city
         
         
    
         #### Calcualte class_group share


    def cal_group_share(self):
             
             
             
             df = self.data
     
             groups = df.groupby("date_month")
             l1=[]
             for name,g in groups:
                 classes = g.groupby("class_group")
                 l2 =[]
                 
                 #### Variables are per month-class-city:
                 
                 for name,c in classes:
                     
                     brands = c.groupby("Chain")
                     l3=[]
                     for name, b in brands:
                         b["adr_class_brand"] = b["ADR"].mean()
                         l3.append(b)
                     c = pd.concat(l3, axis =0)
                     
                     
                     
                     c["class_size"] = sum(c["demand"])
                     c["num_of_chain_withinClass"] = c[c["Operation"]==1]["shareid_str"].nunique()
                     c["num_of_franchise_withinClass"] = c[c["Operation"]==2]["shareid_str"].nunique()
                     c["num_of_inde_withinClass"] = c[c["Operation"]==3]["shareid_str"].nunique()
                     c["num_of_hotels_withinClass"] = c["shareid_str"].nunique()
                     c["adr_inclass_mean"] = c["ADR"].mean()
                     c["num_up_withinClass"] = c[c["round_up"]==True]["shareid_str"].nunique()
                     c["class_service_mean"] = c["service_mean"].mean()
                     c["class_cleanliness_mean"] = c["cleanliness_mean"].mean()
                     c["class_value_mean"] = c["value_mean"].mean()
                     c["class_location_mean"] = c["location_mean"].mean()
                     c["class_roomsquality_mean"] = c["roomsQuality_mean"].mean()
                     c["class_sleepquality_mean"] = c["sleepQuality_mean"].mean()
        
                     l2.append(c)
                     
                 df_temp = pd.concat(l2,axis = 0)
                 df_temp ["pecent_up_withinClass"] = df_temp["num_up_withinClass"]/ df_temp["num_of_hotels_withinClass"]
                 
                 l1.append(df_temp)
             
             df = pd.concat(l1,axis = 0)
             df ["class_share"] = df["class_size"]/df["market_size"]
             df ["inclass_share"] = df["market_share"]/df["class_share"]
             self.group_share = df
             return self.group_share

df = gen_IV(df).replace_zero()
chicago = df[df["Market"].str.contains("Chicago")]
chicago = gen_IV(chicago).cal_market_share()
chicago = gen_IV(chicago).cal_group_share()

houston = df[df["Market"].str.contains("Houston")]
houston = gen_IV(houston).cal_market_share()
houston = gen_IV(houston).cal_group_share()

miami = df[df["Market"].str.contains("Miami")]
miami = gen_IV(miami).cal_market_share()
miami = gen_IV(miami).cal_group_share()


pd.concat([chicago,houston,miami]).to_csv("/Users/juju/downloads/temp/df_demand.csv")


