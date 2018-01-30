import pandas as pd
from __future__ import division
import matplotlib.pyplot as plt
import numpy as np


review = pd.read_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/chicago_reviews_updated.csv",sep=',',header=0,infer_datetime_format=True,parse_dates=['review_date','stay_date'])


review["post_month"] = review["review_date"].dt.to_period('M')
review["stay_month"] = review["stay_date"].dt.to_period('M')
review["renovation"] = review["renovation"].astype(str)
# percentage of reviews are not posted during the stay month
len(review[review["stay_month"]!=review["post_month"]])/len(review)
# Average delay of posting among delayed reviews 
mean(review[review["stay_month"]!=review["post_month"]]["post_month"]-review[review["stay_month"]!=review["post_month"]]["stay_month"])

hotels=review.groupby("SHARE ID")

# Aggregate by review post month
l=[]
for name,hotel in hotels:
    aggregations={
    "ratings":{"month_rating_mean":"mean","monthly_reviews":"count","negatives1":lambda x: sum(x==10.0),"negatives2":lambda x: sum(x==20.0)},
    "hotel_response":{"monthly_hotel_response":"count"},
    "collect_by":{"partnerships": lambda x: sum(x == "partnership")},
    "Cleanliness":{"cleanliness_count":lambda x: sum(x!=0), "cleanliness_mean": lambda x: sum(x)/sum(x!=0)},
    "Location":{"location_count":lambda x: sum(x!=0), "location_mean": lambda x: sum(x)/sum(x!=0)},
    "Quality":{"sleepQuality_count":lambda x: sum(x!=0), "sleepQuality_mean": lambda x: sum(x)/sum(x!=0)},
    "Rooms":{"roomsQuality_count":lambda x: sum(x!=0), "roomsQuality_mean": lambda x: sum(x)/sum(x!=0)},
    "Service":{"service_count":lambda x: sum(x!=0), "service_mean": lambda x: sum(x)/sum(x!=0)},
    "Value":{"value_count":lambda x: sum(x!=0), "value_mean": lambda x: sum(x)/sum(x!=0)},
    "renovation":{"renovate": lambda x: (sum(x == 'True')!=0)},
    "stayed_as_type":{"solo": lambda x: sum(x.str.contains("solo")),"couple": lambda x: sum(x.str.contains("couple")), "family": lambda x: sum(x.str.contains("family")), "business": lambda x: sum(x.str.contains("business"))}
    }
    d = hotel.groupby("post_month").agg(aggregations)
    d["shareid"]=name   
    l.append(d)

df=pd.concat(l,axis=0)

df.to_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/miami_aggby_post_month.csv")

#### In excel, arrange the column names 

df = pd.read_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/chicago_aggby_post_month.csv",sep=',',header=0,infer_datetime_format=True,parse_dates=['review_month'])

df["review_month"] = df["review_month"].dt.to_period("M")

l=[]
g = df.groupby("shareid")

for name,group in g:
    group["accum_rating"] = pd.expanding_mean(group["month_rating_mean"])
    group["num_of_reviews"] = pd.expanding_sum(group["monthly_reviews"])
    group["num_of_responses"] = pd.expanding_sum(group["monthly_hotel_response"])
    group["num_of_partnerships"] = pd.expanding_sum(group["partnerships"])
    group["num_of_solo"] = pd.expanding_sum(group["solo"])
    group["num_of_couple"] = pd.expanding_sum(group["couple"])
    group["num_of_family"] = pd.expanding_sum(group["family"])
    group["num_of_business"] = pd.expanding_sum(group["business"])
    group["shareid"]=name
    l.append(group)
    
df_2= pd.concat(l,axis=0)
df_2.to_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/chicago_aggby_post_month_2.csv", index = False)


# Aggregate by stayed month

review = pd.read_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/houston_reviews_updated.csv",sep=',',header=0,infer_datetime_format=True,parse_dates=['review_date','stay_date'])


review["post_month"] = review["review_date"].dt.to_period('M')
review["stay_month"] = review["stay_date"].dt.to_period('M')
review["renovation"] = review["renovation"].astype(str)
# percentage of reviews are not posted during the stay month
len(review[review["stay_month"]!=review["post_month"]])/len(review)
# Average delay of posting among delayed reviews 
mean(review[review["stay_month"]!=review["post_month"]]["post_month"]-review[review["stay_month"]!=review["post_month"]]["stay_month"])


hotels=review.groupby("SHARE ID")

# Aggregate by review post month
l=[]
for name,hotel in hotels:
    aggregations={
    "ratings":{"month_rating_mean":"mean","monthly_reviews":"count","negatives1":lambda x: sum(x==10.0),"negatives2":lambda x: sum(x==20.0)},
    "hotel_response":{"monthly_hotel_response":"count"},
    "collect_by":{"partnerships": lambda x: sum(x == "partnership")},
    "Cleanliness":{"cleanliness_count":lambda x: sum(x!=0), "cleanliness_mean": lambda x: sum(x)/sum(x!=0)},
    "Location":{"location_count":lambda x: sum(x!=0), "location_mean": lambda x: sum(x)/sum(x!=0)},
    "Quality":{"sleepQuality_count":lambda x: sum(x!=0), "sleepQuality_mean": lambda x: sum(x)/sum(x!=0)},
    "Rooms":{"roomsQuality_count":lambda x: sum(x!=0), "roomsQuality_mean": lambda x: sum(x)/sum(x!=0)},
    "Service":{"service_count":lambda x: sum(x!=0), "service_mean": lambda x: sum(x)/sum(x!=0)},
    "Value":{"value_count":lambda x: sum(x!=0), "value_mean": lambda x: sum(x)/sum(x!=0)},
    "renovation":{"renovate": lambda x: (sum(x == 'True')!=0)},
    "stayed_as_type":{"solo": lambda x: sum(x.str.contains("solo")),"couple": lambda x: sum(x.str.contains("couple")), "family": lambda x: sum(x.str.contains("family")), "business": lambda x: sum(x.str.contains("business"))}
    }
    d = hotel.groupby("stay_month").agg(aggregations)
    d["shareid"]=name   
    l.append(d)

df=pd.concat(l,axis=0)

df.to_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/houston_aggby_stay_month.csv")

#### In excel, arrange the column names 

df = pd.read_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/houston_aggby_stay_month.csv",sep=',',header=0,infer_datetime_format=True,parse_dates=['stay_month'])

df["stay_month"] = df["stay_month"].dt.to_period("M")

l=[]
g = df.groupby("shareid")

for name,group in g:
    group["accum_rating"] = pd.expanding_mean(group["month_rating_mean"])
    group["num_of_reviews"] = pd.expanding_sum(group["monthly_reviews"])
    group["num_of_responses"] = pd.expanding_sum(group["monthly_hotel_response"])
    group["num_of_partnerships"] = pd.expanding_sum(group["partnerships"])
    group["num_of_solo"] = pd.expanding_sum(group["solo"])
    group["num_of_couple"] = pd.expanding_sum(group["couple"])
    group["num_of_family"] = pd.expanding_sum(group["family"])
    group["num_of_business"] = pd.expanding_sum(group["business"])
    group["shareid"]=name
    l.append(group)
    
df_2= pd.concat(l,axis=0)
df_2.to_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/houston_aggby_stay_month_2.csv", index = False)

data_ta_post = pd.read_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/miami_aggby_post_month.csv",sep=',',header=0, infer_datetime_format=True,parse_dates=['review_month'])

data_ta_stay = pd.read_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/miami_aggby_stay_month.csv",sep=',',header=0, infer_datetime_format=True,parse_dates=['stay_month'])

#### I forgot to get the first review posted date
l=[]
hotels = data_ta_post.groupby("shareid")

for name,hotel in hotels: 
    if min(hotel[hotel["review_month"].notnull()]["review_month"]):
        hotel ["first_review_date"] = min(hotel[hotel["review_month"].notnull()]["review_month"])
    else: hotel ["first_review_date"] = 0
    l.append(hotel)
    
data_ta_post = pd.concat(l, axis = 0)
data_ta_post.to_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/miami_aggby_post_month.csv", index = False)

first_review_date = data_ta_post["first_review_date"].groupby(data_ta_post["shareid"]).unique()

l=[]
hotels = data_ta_stay.groupby("shareid")

for name,hotel in hotels: 
    hotel ["first_review_date"] = first_review_date [name][0]
    l.append(hotel)
    
data_ta_stay = pd.concat(l, axis = 0)
data_ta_stay.to_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/miami_aggby_stay_month.csv", index = False)







data = pd.read_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/chicago_STR.csv",sep=',',header=0, infer_datetime_format=True,parse_dates=['date_month'])

df_1 = df.merge(data, left_on = ["shareid", "review_month"], right_on = ["SHARE ID", "date_month"], how = "outer")
df_2 = df2.merge(data, left_on = ["shareid", "stay_month"], right_on = ["SHARE ID", "date_month"], how = "outer"
df_1.to_csv("/Users/juju/Downloads/temp/chicago_df1.csv",index = False)
df_2.to_csv("/Users/juju/Downloads/temp/chicago_df2.csv",index = False)


