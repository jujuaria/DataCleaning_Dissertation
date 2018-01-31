import pandas as pd

data_str = pd.read_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/houston_STR.csv",sep=',',header=0, infer_datetime_format=True,parse_dates=['date_month'])

data_ta_post = pd.read_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/houston_aggby_post_month.csv",sep=',',header=0, infer_datetime_format=True,parse_dates=['review_month','first_review_date'])

data_ta_stay = pd.read_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/houston_aggby_stay_month.csv",sep=',',header=0, infer_datetime_format=True,parse_dates=['stay_month','first_review_date'])





df_post = data_str.merge(data_ta_post, left_on = ["SHARE ID", "date_month"], right_on = ["shareid", "review_month"], how = "left")
df_stay = data_str.merge(data_ta_stay, left_on = ["SHARE ID", "date_month"], right_on = ["shareid", "stay_month"], how = "left")

df_post = df_post [df_post["shareid"] !=0]
df_stay = df_stay [df_stay["shareid"] !=0]


def Myfillna (data_frame):
    
    df = data_frame
    df["solo"] = df["solo"].fillna(0)
    df["couple"] = df["couple"].fillna(0)
    df["business"] = df["business"].fillna(0)
    df["family"] = df["family"].fillna(0)
    df["value_mean"] = df["value_mean"].fillna(0)
    df["value_count"] = df["value_count"].fillna(0)
    df["service_mean"] = df["service_mean"].fillna(0)
    df["service_count"] = df["service_count"].fillna(0)
    df["location_mean"] = df["location_mean"].fillna(0)
    df["location_count"] = df["location_count"].fillna(0)
    df["cleanliness_mean"] = df["cleanliness_mean"].fillna(0)
    df["cleanliness_count"] = df["cleanliness_count"].fillna(0)
    df["roomsQuality_mean"] = df["roomsQuality_mean"].fillna(0)
    df["roomsQuality_count"] = df["roomsQuality_count"].fillna(0)
    df["sleepQuality_mean"] = df["sleepQuality_mean"].fillna(0)
    df["sleepQuality_count"] = df["sleepQuality_count"].fillna(0)
    df["month_rating_mean"] = df["month_rating_mean"].fillna(0)
    df["monthly_reviews"] = df["monthly_reviews"].fillna(0)
    df["monthly_hotel_response"] = df["monthly_hotel_response"].fillna(0)
    df["partnerships"] = df["partnerships"].fillna(0)



    l = []

    hotels = df.groupby("SHARE ID")

    for name, hotel in hotels:
        hotel ["first_review_date"] = hotel ["first_review_date"].fillna(method='bfill')
        hotel ["accum_rating"] = hotel ["accum_rating"].fillna(method='ffill')
        hotel ["num_of_reviews"] = hotel ["num_of_reviews"].fillna(method='ffill')
        hotel ["num_of_responses"] = hotel ["num_of_responses"].fillna(method='ffill')
        hotel ["num_of_partnerships"] = hotel ["num_of_partnerships"].fillna(method='ffill')
        hotel ["num_of_solo"] = hotel ["num_of_solo"].fillna(method='ffill')
        hotel["num_of_couple"] = hotel ["num_of_couple"].fillna(method='ffill')
        hotel["num_of_family"] = hotel ["num_of_family"].fillna(method='ffill')
        hotel["num_of_business"] = hotel ["num_of_business"].fillna(method='ffill')
        l.append(hotel)
    
    df_2= pd.concat(l,axis=0)
#### Keep data up to Nov, 2017
    df_2 = df_2[df_2 ["Year Month"]<=201711]
    df_2["no_list_ta"]=df_2["first_review_date"].isnull()
    df_2["on_ta"] = df_2["date_month"]>=df_2["first_review_date"]
    return df_2


Myfillna(df_post).to_csv("/Users/juju/Downloads/temp/houston_post.csv", index = False)
Myfillna(df_stay).to_csv("/Users/juju/Downloads/temp/houston_stay.csv", index = False)



