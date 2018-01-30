#### Initial cleaning of data from STR
####  Merge Review data with STR data in two ways
####  (1) df1: merge by SHARE ID, reviewer post month
####  (2) df2: merge by SHARE ID, reviewer stayed month
####  Because df1 and df2 are on individual review level, I need to aggregate df1, df2 to monthly level



import pandas as pd
 

# Financial performance data
df = pd.read_excel("/Users/juju/Dropbox/Sent_to_STR_ZHU/SHARE Property Data Chicago.xlsx")

# Basic info data
info = pd.read_excel("/Users/juju/Dropbox/Sent_to_STR_ZHU/Basic Property Info Chicago.xlsx")

# Number of hotels by operation
print(info[info["Operation"]==1]["SHARE ID"].nunique())
print(info[info["Operation"]==2]["SHARE ID"].nunique())
print(info[info["Operation"]==3]["SHARE ID"].nunique())
# Number of hotels by class
print(info[info["Class"]==1]["SHARE ID"].nunique())
print(info[info["Class"]==2]["SHARE ID"].nunique())
print(info[info["Class"]==3]["SHARE ID"].nunique())
print(info[info["Class"]==4]["SHARE ID"].nunique())
print(info[info["Class"]==5]["SHARE ID"].nunique())
print(info[info["Class"]==6]["SHARE ID"].nunique())
# Number of hotels by size
print(info[info["SizeCode"]==1]["SHARE ID"].nunique())
print(info[info["SizeCode"]==2]["SHARE ID"].nunique())
print(info[info["SizeCode"]==3]["SHARE ID"].nunique())
print(info[info["SizeCode"]==4]["SHARE ID"].nunique())
print(info[info["SizeCode"]==5]["SHARE ID"].nunique())


#Calculate days in month
df["date_month"] = pd.to_datetime(df["Year Month"],format = "%Y%m")
df['year'] = df['date_month'].dt.year
df['month'] = df['date_month'].dt.month
df['days_in_month'] = df.apply(lambda x: pd.tslib.monthrange(x['year'],x['month'])[1], axis = 1)

# The number of rooms supplied per month
df["supply_rooms"] = df["Supply"]/df["days_in_month"]
hotels = df.groupby("SHARE ID")

l = []
for name,hotel in hotels:
# Find the number of rooms (size) of a hotel
    hotel["size"] = hotel["supply_rooms"].value_counts().index[0]
    l.append(hotel)
df = pd.concat(l,axis=0)


df["ln_revenue"]=log(df["Revenue"])
df["ln_revpar"]=log(df["RevPAR"])
df["ln_adr"]=log(df["ADR"])

#merge basic info with performance data
data=df.merge(info, on = "SHARE ID")

data.to_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/chicago_STR.csv", index = False)

#####Check the average ADR in each ``Class" segment:

#mean(data[data["Class"]==1].ADR)
#Out[39]: 266.51796298645047

#mean(data[data["Class"]==2].ADR)
#Out[40]: 166.76369216691307

#mean(data[data["Class"]==3].ADR)
#Out[41]: 151.49044765408979

#mean(data[data["Class"]==4].ADR)
#Out[42]: 138.73675718898585

#mean(data[data["Class"]==5].ADR)
#Out[43]: 111.33334414339865

#mean(data[data["Class"]==6].ADR)
#Out[44]: 98.98907904956755

#std(data[data["Class"]==1].ADR)
#Out[391]: 86.948205781003722

#std(data[data["Class"]==2].ADR)
#Out[392]: 44.124081124226549

#std(data[data["Class"]==3].ADR)
#Out[393]: 44.042231790141074

#std(data[data["Class"]==4].ADR)
#Out[394]: 40.864132609465287

#std(data[data["Class"]==5].ADR)
#Out[395]: 37.380092279312819

#std(data[data["Class"]==6].ADR)
#Out[396]: 23.878583279972361

# Load review data
review = pd.read_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/miami_reviews_updated_3.csv",sep=',',header=0)
missing_stay_date = review[review["stayed_month"].isnull()]
with_stay_date = review[review["stayed_month"].notnull()]
missing_stay_date ["stayed_month"] = pd.to_datetime(missing_stay_date ["review_date"])
with_stay_date["stayed_month"] = (with_stay_date ["stayed_month"]).astype(int).astype(str) + '-'+(with_stay_date ["stayed_year"]+2000).astype(int).astype(str)
with_stay_date["stayed_month"] = pd.to_datetime(with_stay_date["stayed_month"],format = "%m-%Y")
review = pd.concat([missing_stay_date,with_stay_date],axis = 0)
review.to_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/miami_reviews_updated_3.csv",index = False)


review["review_month"]=review["review_date"].dt.month.astype(str)+'-'+review["review_date"].dt.year.astype(str)
review["review_month"] = pd.to_datetime(review["review_month"],format = "%m-%Y")
review["stay_month"] = pd.to_datetime(review["stay_month"],format = "%b-%y")
review["stay_month"] = '1.0'+review["stayed_month"].astype(str)+review["stayed_year"].astype(str)

# merge review data with STR data (Note Chicago review data has "SHARE ID" = "#N/A", replace them with 0)
df_1 = review.merge(data, left_on = ["SHARE ID", "review_month"], right_on = ["SHARE ID", "date_month"], how = "outer")
df_2 = review.merge(data, left_on = ["SHARE ID", "stay_month"], right_on = ["SHARE ID", "date_month"], how = "outer")


df_1.to_csv("/Users/juju/Downloads/temp/chicago_df1.csv",index = False)
df_2.to_csv("/Users/juju/Downloads/temp/chicago_df2.csv",index = False)

####   Some hotels are not on STR sample (with SHARE ID =0 )but has reviews
####   Some hotels that are in STR sample, but do not have revenue while still have reviews in some months 


review_2=review[review["SHARE ID"]!=0] # The reviews for hotels in STR sample 


df_1 = review_2.merge(data, left_on = ["SHARE ID", "review_month"], right_on = ["SHARE ID", "date_month"], how = "outer")
df_2 = review_2.merge(data, left_on = ["SHARE ID", "stay_month"], right_on = ["SHARE ID", "date_month"], how = "outer")


df_1.to_csv("/Users/juju/Downloads/temp/chicago_df1_allinstr.csv",index = False)
df_2.to_csv("/Users/juju/Downloads/temp/chicago_df2_allinstr.csv",index = False)



