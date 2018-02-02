from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df_post_houston = pd.read_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/houston_post.csv",sep=',',header=0,infer_datetime_format = True, parse_dates = ['date_month','review_month'])
df_post_chicago = pd.read_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/chicago_post.csv",sep=',',header=0,infer_datetime_format = True, parse_dates = ['date_month','review_month'])
df_post_miami = pd.read_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/miami_post.csv",sep=',',header=0,infer_datetime_format = True, parse_dates = ['date_month','review_month'])

df_stay_miami = pd.read_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/miami_stay.csv",sep=',',header=0,infer_datetime_format = True, parse_dates = ['date_month','stay_month'])
df_stay_houston = pd.read_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/houston_stay.csv",sep=',',header=0,infer_datetime_format = True, parse_dates = ['date_month','stay_month'])
df_stay_chicago = pd.read_csv("/Users/juju/Dropbox/Sent_to_STR_ZHU/chicago_stay.csv",sep=',',header=0,infer_datetime_format = True, parse_dates = ['date_month','stay_month'])

df_post = pd.concat([df_post_chicago, df_post_houston,df_post_miami], axis = 0)
df_stay = pd.concat([df_stay_chicago, df_stay_houston,df_stay_miami], axis = 0)



def replace_zero(df):
    df ["location_mean"] = df ["location_mean"].replace(0,np.NaN)
    df ["service_mean"] = df ["service_mean"].replace(0,np.NaN)
    df ["cleanliness_mean"] = df ["cleanliness_mean"].replace(0,np.NaN)
    df ["roomsQuality_mean"] = df ["roomsQuality_mean"].replace(0,np.NaN)
    df ["sleepQuality_mean"] = df ["sleepQuality_mean"].replace(0,np.NaN)
    df ["value_mean"] = df ["value_mean"].replace(0,np.NaN)
    df ["month_rating_mean"] = df ["month_rating_mean"].replace(0,np.NaN)
    df ["accum_rating"] = df ["accum_rating"].replace(0,np.NaN)
    
    return df

def plot_rating_by_cat(data):
    df = replace_zero(data[data["OpenDate"]<2005]) # use hotels opened before 2005
    
    years = df.groupby(df["date_month"].dt.year)
    
    line1, = plt.plot(years["location_mean"].mean(), label="Location")
    line2, = plt.plot(years["service_mean"].mean(), label="Service")
    line3, = plt.plot(years["cleanliness_mean"].mean(), label="Cleanliness")
    line4, = plt.plot(years["value_mean"].mean(), label="Value")
    line5, = plt.plot(years["roomsQuality_mean"].mean(), label="Rooms Quality")
    line6, = plt.plot(years["sleepQuality_mean"].mean(), label="Sleep Quality")
    line7, = plt.plot(years["month_rating_mean"].mean(), label="Overall")


    legend1 = pyplot.legend([line1,line2,line3,line4,line5,line6,line7], ["Location","Service","Cleanliness","Value","Rooms Quality","Sleep Quality","Overall"], loc = 4)

    pyplot.gca().add_artist(legend1)

def plot_rating_by_operation(data):
    df = replace_zero(data) # use hotels opened before 2005
    
    years = df.groupby(df["date_month"].dt.year)
    
    fig,ax = subplots()
    years.apply(lambda x: x.groupby("Operation")["cleanliness_mean"].mean()).plot(ax=ax)
    ax.set_title("Cleanliness Rating by Operation")
    ax.legend(["Chain","Franchise","Independent"],loc='best', fancybox=True, framealpha=0.5)
    
    
    fig,ax = subplots()
    years.apply(lambda x: x.groupby("Operation")["service_mean"].mean()).plot(ax=ax)
    ax.set_title("Service Rating by Operation")
    ax.legend(["Chain","Franchise","Independent"],loc='best', fancybox=True, framealpha=0.5)
    
    fig,ax = subplots()
    years.apply(lambda x: x.groupby("Operation")["location_mean"].mean()).plot(ax=ax)
    ax.set_title("Location Rating by Operation")
    ax.legend(["Chain","Franchise","Independent"],loc='best', fancybox=True, framealpha=0.5)
    
    fig,ax = subplots()
    years.apply(lambda x: x.groupby("Operation")["roomsQuality_mean"].mean()).plot(ax=ax)
    ax.set_title("Room-Quality Rating by Operation")
    ax.legend(["Chain","Franchise","Independent"],loc='best', fancybox=True, framealpha=0.5)
    
    fig,ax = subplots()
    years.apply(lambda x: x.groupby("Operation")["sleepQuality_mean"].mean()).plot(ax=ax)
    ax.set_title("Sleep-Quality Rating by Operation")
    ax.legend(["Chain","Franchise","Independent"],loc='best', fancybox=True, framealpha=0.5)
    
    fig,ax = subplots()
    years.apply(lambda x: x.groupby("Operation")["value_mean"].mean()).plot(ax=ax)
    ax.set_title("Value Rating by Operation")
    ax.legend(["Chain","Franchise","Independent"],loc='best', fancybox=True, framealpha=0.5)
    
    fig,ax = subplots()
    years.apply(lambda x: x.groupby("Operation")["month_rating_mean"].mean()).plot(ax=ax)
    ax.set_title("Average Monthly Rating by Operation")
    ax.legend(["Chain","Franchise","Independent"],loc='best', fancybox=True, framealpha=0.5)
    
    fig,ax = subplots()
    years.apply(lambda x: x.groupby("Operation")["accum_rating"].mean()).plot(ax=ax)
    ax.set_title("Accummulated Average Monthly Rating by Operation")
    ax.legend(["Chain","Franchise","Independent"],loc='best', fancybox=True, framealpha=0.5)
    
    
plot_rating_by_operation(df_post)    
# Plot rating by category for hotels opened before 2005    
plot_rating_by_cat(df_post)

df_post = df_post_miami
df_post["date_month"] = df_post["date_month"].dt.to_period('M')
df_post_1 = df_post.set_index("date_month")
month = df_post_1.groupby(df_post_1.index)

#### Vertical axis: percentage of hotels who have "renovation" reported in reviews
#### Title: Percentage of hotels listed on TripAdvisor who might renovated
month.apply(lambda x: sum(x["renovate"]==True)/sum(x["on_ta"]==True)).plot()

#### Number of hotels who are listed on TripAdvisor
month.apply(lambda x: sum(x["on_ta"]==True)).plot()

def plot_adr_revpar(df):
    # df's index is month period
    #month = df.groupby("date_month")
    years = df.groupby(df["date_month"].dt.year)
    
    #line1, = plt.plot(month.apply(lambda x: x["RevPAR"].mean()), label="RevPAR")
    #line2, = plt.plot(month.apply(lambda x: x["ADR"].mean()), label="ADR")
    
    line1, = plt.plot(years.apply(lambda x: x["RevPAR"].mean()), label="RevPAR")
    line2, = plt.plot(years.apply(lambda x: x["ADR"].mean()), label="ADR")
    
    
    legend1 = pyplot.legend([line1,line2], ["RevPAR","ADR"], loc = 4)
    pyplot.gca().add_artist(legend1)

plot_adr_revpar(df_post)    

def plot_adr_revpar_byOP(df):
    # df's index is month period
    #month = df.groupby("date_month")
    chain = df[df["Operation"]==1]
    franchise = df[df["Operation"]==2]
    independent = df[df["Operation"]==3]
    
    years = df.groupby(df["date_month"].dt.year)
    
    #line1, = plt.plot(month.apply(lambda x: x["RevPAR"].mean()), label="RevPAR")
    #line2, = plt.plot(month.apply(lambda x: x["ADR"].mean()), label="ADR")
    
    line1, = plt.plot(years.apply(lambda x: x.groupby("Operation")["RevPAR"].mean()), label="RevPAR")
    line2, = plt.plot(years.apply(lambda x: x["ADR"].mean()), label="ADR")
    
    
    legend1 = pyplot.legend([line1,line2], ["RevPAR","ADR"], loc = 4)
    pyplot.gca().add_artist(legend1)

plot_adr_revpar_byOP(df_post)    
