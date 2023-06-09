# -*- coding: utf-8 -*-
"""netflix

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rDCIyfOp1YNxDUgohp9Smy0h8giGDLYZ
"""

!pip install pandas

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

!gdown https://d2beiqkhq929f0.cloudfront.net/public_assets/assets/000/000/940/original/netflix.csv

df=pd.read_csv("/content/netflix.csv")
df

df.shape

df.info()

null=df.isna().sum().to_frame().reset_index().rename(columns={0:"number Of null","index":"column"})
null

sns.boxplot(data=null,y="number Of null")
plt.title("Outlier")
plt.show()

"""the outlier lies between 825 to 2650
 
"""

sns.barplot(data=null,x="column",y="number Of null")
plt.xticks(rotation=90)
plt.title("Number of null values in each columns")
plt.show()

df=df.drop_duplicates(keep="first")
df

df.shape

df["timestamp"]=pd.to_datetime(df["date_added"])
df.info()

df=df.dropna(subset=["date_added","country","rating","duration"])

df.isna().sum()

"""##Filling null values

"""

df["director"].fillna("unknown",inplace=True)
df["cast"].fillna("unknown",inplace=True)
df.reset_index(drop=True,inplace=True)
df

sns.countplot(df["type"])

"""there are more number of movies then tv show

#Top 10 Actors performed in tv show or in Movies
"""

import numpy as np
a=df["cast"].str.split(",").to_list()
flatlist = [element for sub_list in a for element in sub_list]  
b=np.unique(np.array(flatlist),return_counts=True)
actor=pd.DataFrame({"actor":b[0],"number_of_show":b[1]})
actor_most=actor.sort_values(by="number_of_show",ascending=False).reset_index().head(10).drop(0)
actor_most_=actor_most.drop(['index'],axis=1)
actor_most_

sns.barplot(data=actor_most_,x='actor',y='number_of_show')
plt.xticks(rotation=90)
plt.title("Actor vs Number of show")
plt.xlabel('Actor', fontsize=10)
plt.ylabel('Total Show', fontsize=10)
plt.show()

"""Anupam Kher	,Takahiro Sakurai,Om Puri,Shah Rukh Khan,	Boman Irani	shows are most in this Netflix platfrom

#Movies added since beganing
"""

sns.histplot(df["release_year"],bins=10)
plt.show()

"""from the above it is clear that number of movies and tv shoe released in this decaed is in creases repaidly"""

df["add_year"]=df["timestamp"].dt.year

m_add_y=df.groupby(["add_year","type"])["title"].count().to_frame().sort_values(by=['add_year',"type"],ascending=[False,False]).reset_index().rename(columns={"title":"number Of movies",})
m_add=pd.pivot(m_add_y,index=['add_year'],columns='type',values='number Of movies').sort_values(by=['add_year'],ascending=False).fillna(0).reset_index()
m_add.columns.name=None

m_add

sns.lineplot(data=m_add,x='add_year',y="Movie",label='Movie')
sns.lineplot(data=m_add,x='add_year',y="TV Show",label='TV Show')
plt.title("Movies and Tvshow added per Year")
plt.xlabel('Added Year', fontsize=10)
plt.ylabel('Total number', fontsize=10)
plt.grid()
plt.show()

"""from the above bivariate analysis it is clear that number of movies &Tv show added from the year 2014 to 2019 will be highest and then it decreases

#year by year analysis of movies and tv show that are added
"""

m_add_y=df.groupby(["add_year","type"])['title'].count().to_frame().sort_values(by=["add_year","title"],ascending=[False,False]).reset_index().rename(columns={"title":"count"})
m_add_y_pivot=pd.pivot(m_add_y,index="add_year",columns="type",values="count").reset_index().fillna(0)
m_add_y_pivot.columns.name=None
m_add_y_pivot

plt.figure(figsize=(10,5))
plt.subplot(1,2,1)
sns.distplot(m_add_y_pivot.Movie)
plt.title("distribution of Movies")
plt.subplot(1,2,2)
sns.distplot(m_add_y_pivot["TV Show"])
plt.title("distribution of TV Show")
plt.subplots_adjust(hspace=5)
plt.show()

"""highest distribution observed for movies around 480 and for tv show around 190"""

plt.figure(figsize=(12,8))
sns.barplot(data=m_add_y,x="add_year",y="count",hue="type")
plt.legend(loc=(0,0.92))
plt.title("Movies and Tvshow added per Year")
plt.xlabel('Added Year', fontsize=10)
plt.ylabel('Total number', fontsize=10)
plt.grid()
plt.show()

"""#Country wise Movies and Tv show

"""

movie_tvshow_country_wise=df.groupby(["country","type"])["title"].count().to_frame().sort_values(by=["type","title"],ascending=[False,False]).reset_index().rename(columns={"title":"count"})
movie_tvshow_country_wise

movie_tvshow_country_wise_pivot=pd.pivot(movie_tvshow_country_wise,index="country",columns="type",values="count").fillna(0).sort_values(by=["Movie"],ascending=False).reset_index()
movie_tvshow_country_wise_pivot.columns.name=None

movie_tvshow_country_wise_pivot_10=movie_tvshow_country_wise_pivot.head(10)

plt.figure(figsize=(5,5))
sns.pairplot(data=movie_tvshow_country_wise_pivot_10,hue="country")

"""usa has heighest number of tv show and movies"""

sns.heatmap(data=movie_tvshow_country_wise_pivot_10.corr(),annot=True)
plt.title("corelation between tv show and movies")



"""#Top 10 country where Movies are highest"""

#top10  movies producing counrty 
movie_tvshow_country_wise_pivot=pd.pivot(movie_tvshow_country_wise,index=['country'],columns='type',values="count").fillna(0).sort_values(by=["Movie"],ascending=[False]).reset_index()
movie_tvshow_country_wise_pivot.columns.name=None
movies_top_10=movie_tvshow_country_wise_pivot[["country","Movie"]].head(10)
movies_top_10

"""#Top10 tvshow producing counrty """

movie_tvshow_country_wise_pivot=pd.pivot(movie_tvshow_country_wise,index=['country'],columns='type',values="count").fillna(0).sort_values(by=["TV Show"],ascending=[False]).reset_index()
movie_tvshow_country_wise_pivot.columns.name=None
tvshow_top_10=movie_tvshow_country_wise_pivot[["country","TV Show"]].head(10)
tvshow_top_10

plt.figure(figsize=(15 ,12))

plt.subplot(1,2,1)
plt.pie(movies_top_10['Movie'], labels=movies_top_10['country'],  autopct='%.0f%%',radius=1)
plt.title("Percentage of Movies in top 10 country")

plt.subplot(1,2,2)
plt.pie(tvshow_top_10['TV Show'], labels=tvshow_top_10['country'],  autopct='%.0f%%',radius=1)
plt.title("Percentage of Tvshow in top 10 country")

plt.subplots_adjust(hspace=5)
plt.show()

"""USA is the counrty where maximum number of movies and Tv show are launched

#Countries where Movies and TvShow are more than 50
"""

#country most in netflix heaving tvshow/movies more then 50
movie_tvshow_country_wise_pivot_50=movie_tvshow_country_wise_pivot[(movie_tvshow_country_wise_pivot['Movie']>50) & (movie_tvshow_country_wise_pivot["TV Show"]>50)]
movie_tvshow_country_wise_pivot_50.reset_index(drop=True)

sns.heatmap(movie_tvshow_country_wise_pivot_50.corr(),annot=True)

movie_tvshow_country_wise_50_=pd.melt(movie_tvshow_country_wise_pivot_50,id_vars=['country'],var_name="type",value_name="count")
sns.barplot(data=movie_tvshow_country_wise_50_,x="country",y="count",hue="type")
plt.xticks(rotation=90)
plt.title("Country having more than 50 Tv show and Movies")
plt.show()

"""there are only 5 country USA,UK, Japan,India,Canada where movies and Tv show more than 50

#Catagory content in netflix
"""

#catagoy wise most in netflix
catagory=df.groupby("listed_in")["title"].agg("count").to_frame().sort_values(by=["title"],ascending=[False]).reset_index().rename(columns={"title":"count",'listed_in':'catagory'}).head(10)
catagory

sns.scatterplot(data=catagory,x="catagory",y='count')
plt.xticks(rotation=90)
plt.title("top 10 Catagory")
plt.show()

"""Documentaries,Dramas,Stand-Up Comedy	are the top three catagory

#Movies released year by year
"""

mpy=df.groupby(["type","release_year"])["title"].count().to_frame().sort_values(by=["type",'release_year'],ascending=[False,False]).reset_index().rename(columns={"title":"number Of movies",})
mpy

plt.figure(figsize=(5,10))
sns.boxplot(data=mpy,x="type",y="number Of movies")
plt.title("movies vs tv show")
plt.show()

#last 20 years movies released
mpy=df.groupby(["type","release_year"])["title"].count().to_frame().sort_values(by=["type",'release_year'],ascending=[False,False]).reset_index().rename(columns={"title":"number Of movies",})
mpy_pivot=pd.pivot(mpy,index=["release_year"],columns="type",values="number Of movies").fillna(0).reset_index()
mpy_pivot.columns.name=None
mpy_pivot_released=mpy_pivot.sort_values(by="release_year",ascending=False).reset_index(drop=True).drop(columns=["TV Show"])
mpy_pivot_released

"""#Movies released in last 20 year"""

mpy_20=mpy_pivot_released.head(20)
mpy_20

"""#Movies released in last 30 years """

mpy_30=mpy_pivot_released.head(30)
mpy_30

plt.figure(figsize=(18,5))
plt.subplot(1,2,1)
sns.barplot(data=mpy_20,x="release_year",y="Movie")
plt.xticks(rotation=90)
plt.title("Movies released in last 20 years")

plt.subplot(1,2,2)
sns.barplot(data=mpy_30,x="release_year",y="Movie")
plt.xticks(rotation=90)
plt.subplots_adjust(hspace=2)
plt.title("Movies released in last 30 years")
plt.show()

"""from the above it is seen that since 2018 Number of Movies Realesed decreases year by year

#Tv show released year by year
"""

#last 20 years tv show released
mpy=df.groupby(["type","release_year"])["title"].count().to_frame().sort_values(by=["type",'release_year'],ascending=[False,False]).reset_index().rename(columns={"title":"number Of movies",})
mpy_pivot=pd.pivot(mpy,index=["release_year"],columns="type",values="number Of movies").fillna(0).reset_index()
mpy_pivot.columns.name=None
mpy_pivot_released=mpy_pivot.sort_values(by="release_year",ascending=False).reset_index(drop=True).drop(columns=["Movie"])
mpy_pivot_released

"""#Tv show released in last 20 years """

mpy_tv_20=mpy_pivot_released.head(20)
mpy_tv_20

"""#Tv show released in last 30 years """

mpy_tv_30=mpy_pivot_released.head(30)
mpy_tv_30

plt.figure(figsize=(18,5))
plt.subplot(1,2,1)
sns.barplot(data=mpy_tv_20,x="release_year",y="TV Show")
plt.xticks(rotation=90)
plt.title("TV Show released in last 20 years")

plt.subplot(1,2,2)
sns.barplot(data=mpy_tv_30,x="release_year",y="TV Show")
plt.xticks(rotation=90)
plt.subplots_adjust(hspace=2)
plt.title("TV Show released in last 30 years")
plt.show()

"""from the above it is clear that till 2020 number of tv show released was increasing but last year number of tv show decreases

#Increases in tvshow released
"""

mpy=df.groupby(["type","release_year"])["title"].count().to_frame().sort_values(by=["type",'release_year'],ascending=[False,False]).reset_index().rename(columns={"title":"number Of movies",})
mpy_pivot=pd.pivot(mpy,index=["release_year"],columns="type",values="number Of movies").fillna(0).reset_index()
mpy_pivot.columns.name=None
mpy_pivot_released=mpy_pivot.sort_values(by="release_year",ascending=False).reset_index(drop=True)
mpy_pivot_released_tv_movies=mpy_pivot_released.head(5)
mpy_pivot_released_tv_movies

#increase in trand of tv show
sns.lineplot(data=mpy_pivot_released_tv_movies,x="release_year",y="Movie",label="Movies")
sns.lineplot(data=mpy_pivot_released_tv_movies,x="release_year",y="TV Show",label="TV Show")
plt.grid()
plt.title("Trand of Movies and Tv show relesed per year")
plt.show()

"""
from the above it is clear that number of tvshow released are more  compair to movies in2021 and a clear increase in trand of tv show realesed"""

mpy=df.groupby(["type","add_year"])["title"].count().to_frame().sort_values(by=["type",'add_year'],ascending=[False,False]).reset_index().rename(columns={"title":"number Of movies",})
mpy_pivot=pd.pivot(mpy,index=["add_year"],columns="type",values="number Of movies").fillna(0).reset_index()
mpy_pivot.columns.name=None
mpy_pivot_released=mpy_pivot.sort_values(by="add_year",ascending=False).reset_index(drop=True)
mpy_pivot_released_tv_movies=mpy_pivot_released.head(5)
mpy_pivot_released_tv_movies

"""#Trand of Tv show and movies added in recent time"""

sns.lineplot(data=mpy_pivot_released_tv_movies,x="add_year",y="Movie",label="Movies")
sns.lineplot(data=mpy_pivot_released_tv_movies,x="add_year",y="TV Show",label="TV Show")
plt.grid()
plt.title("Trand of Movies and Tv show added per year")
plt.show()

"""there is a dreaseing trand in movies and tv show added

#Rating for Movies and Tv show
"""

#highly rated tvshow and movies

highlyrated=df.groupby(["type","rating"])["show_id"].count().to_frame().sort_values(by=["type","show_id"],ascending=[True,False]).rename(columns={"show_id":"no of ratings"}).reset_index()
highlyrated_pivot=pd.pivot(highlyrated,index="rating",columns="type",values="no of ratings").fillna(0).reset_index()
highlyrated_pivot.columns.name=None
highlyrated_pivot

sns.heatmap(highlyrated_pivot.corr(),annot=True)

sns.pairplot(highlyrated_pivot,hue="rating")

plt.show()

"""Tv_MA is top rated movie and tvshow

#Top 5 Ratings for Movies
"""



top_5_rated_movies=highlyrated_pivot.sort_values(by="Movie",ascending=False).head(5)
top_5_rated_movies[["rating","Movie"]].reset_index(drop=True)

"""#Top 5 Ratings for Tvshow """

top_5_rated_Tvshow=highlyrated_pivot.sort_values(by="TV Show",ascending=False).head(5)
top_5_rated_Tvshow[["rating","TV Show"]].reset_index(drop=True)

plt.figure(figsize=(15 ,5))

plt.subplot(1,2,1)
plt.pie(top_5_rated_movies['Movie'], labels=top_5_rated_movies['rating'],  autopct='%.0f%%',radius=1)
plt.title("Top 5 catagory of ratings of Movies")

plt.subplot(1,2,2)
plt.pie(top_5_rated_Tvshow['TV Show'], labels=top_5_rated_Tvshow['rating'],  autopct='%.0f%%',radius=1)
plt.title("Top 5 catagory of rating of Tv show")
#plt.tight_layout()
plt.subplots_adjust(hspace=5)
plt.show()

"""TV-MA,TV-14 are top rating

#Seasonality to launched a Tvshoe and Movies
"""

df["month"]=df["timestamp"].dt.month_name()

#seasonal peak for a movies or tv show to launch

seasonality=df.groupby(["type","month"])["title"].count().to_frame().sort_values(by=["title"],ascending=False).rename(columns={"title":"no.of production"}).reset_index()
seasonality_pivot=pd.pivot(seasonality,index="month",columns="type",values="no.of production").reset_index()
seasonality_pivot.columns.name=None

months = ["January", "February", "March", "April", "May", "June", 
          "July", "August", "September", "October", "November", "December"]
seasonality_pivot_sorted=seasonality_pivot.sort_values(by='month', key = lambda x : pd.Categorical(x, categories=months, ordered=True)).reset_index(drop=True)
seasonality_pivot_sorted

plt.figure(figsize=(15,5))
seasonality=df.groupby(["type","month"])["title"].count().to_frame().sort_values(by=["title"],ascending=False).rename(columns={"title":"no.of production"}).reset_index()
sns.barplot(data=seasonality,x="month",y="no.of production",hue="type")
plt.title("Month on month relesed of Movies and Tvshow")
plt.show()

"""december to january are the top session to released tvshow and movies in the platfrom"""

plt.figure(figsize=(15 ,6))

plt.subplot(1,2,1)
plt.pie(seasonality_pivot_sorted['Movie'], labels=seasonality_pivot_sorted['month'],  autopct='%.0f%%',radius=1)
plt.title("monthly relesed of Movies")

plt.subplot(1,2,2)
plt.pie(seasonality_pivot_sorted['TV Show'], labels=seasonality_pivot_sorted['month'],  autopct='%.0f%%',radius=1)
plt.title("monthly relesed of  Tv show")
#plt.tight_layout()
plt.subplots_adjust(hspace=5)
plt.suptitle("Percentage of Movies and Tv show Month on Month")
plt.show()

"""december to january are the top session to released tvshow and movies in the platfrom

#Median of tvshow and movies
"""

#monthly median of tv show and movies
sns.boxplot(data=seasonality_pivot,x="Movie",y="TV Show")
plt.grid()
plt.minorticks_on()
plt.title("Median of Tv show and Movies")

plt.show()

"""the median Number of movies& tvshow per month (518,212)

#Top director
"""

s=df.groupby(["type","director"])["title"].count().to_frame().sort_values(by=["type","title"],ascending=[False,False]).rename(columns={"title":"production"}).reset_index()

director_top_movies=pd.pivot(s,index="director",columns="type",values="production").fillna(0).sort_values(by="Movie",ascending=False).reset_index().drop(0,axis=0).reset_index(drop=True)
director_top_movies.columns.name=None
director_top_movies

"""#Top 10 Movies Director"""

director_top_10_movies=director_top_movies.drop("TV Show",axis=1).head(10)
director_top_10_movies

"""#Top 10 Tv show Director"""

director_top_tvshow=pd.pivot(s,index="director",columns="type",values="production").fillna(0).sort_values(by="TV Show",ascending=False).reset_index().drop(0,axis=0).drop_duplicates(keep="first").reset_index(drop=True)
director_top_tvshow.columns.name=None

director_top_10_tvshow=director_top_tvshow.drop("Movie",axis=1).head(10)
director_top_10_tvshow

plt.figure(figsize=(15 ,5))

plt.subplot(1,2,1)
sns.barplot(data=director_top_10_movies, x="director", y="Movie")
plt.xticks(rotation=90)
plt.title("Top 10 director  of Movies")

plt.subplot(1,2,2)
sns.barplot(data=director_top_10_tvshow, x="director",y="TV Show")
plt.title("Top 10 director  of Tv show")
plt.xticks(rotation=90)
plt.subplots_adjust(hspace=5)
plt.suptitle("Top 10 Directors")
plt.show()

"""Raúl Campos, Jan Suter,Jay Karas,Marcus Raboy are the top movies director
Alastair Fothergill,,Ken Burns,Iginio Straffi,Rob Seidenglanz	are top tvshow director

#Top 5 movies catagory
"""

c=df.groupby(["listed_in","type"])["title"].count().to_frame().sort_values(by=["title","type"],ascending=[False,False]).rename(columns={"title":"production"}).reset_index()
#a.loc[a["type"].str.contains("Movie")]
c_pivot=pd.pivot(c,index="listed_in",columns="type",values="production").fillna(0)
c_pivot=c_pivot.reset_index()
c_pivot.columns.name=None

top_5_movies_catagory=c_pivot.sort_values(by=["Movie"],ascending=[False])[["listed_in","Movie"]].head(5).reset_index(drop=True)
top_5_movies_catagory

"""#Top 5 Tv show catagory"""

top_5_tvshow_catagory=c_pivot.sort_values(by=["TV Show"],ascending=[False])[["listed_in","TV Show"]].head(5).reset_index(drop=True)
top_5_tvshow_catagory

plt.figure(figsize=(8 ,5))

plt.subplot(1,2,1)
sns.barplot(data=top_5_movies_catagory, x="listed_in", y="Movie")
plt.xticks(rotation=90)
plt.title("Top 5  Movies catagory")

plt.subplot(1,2,2)
sns.barplot(data=top_5_tvshow_catagory, x="listed_in",y="TV Show")
plt.title("Top 5  tv Show catagory")
plt.xticks(rotation=90)
plt.subplots_adjust(hspace=5)
plt.suptitle("Top 5 catagory")
plt.show()

"""**Insides**

1.the data set contain 8807 rows, 12 columns

2.Anupam Kher ,Takahiro Sakurai,Om Puri,Shah Rukh Khan, Boman Irani shows are most in this Netflix platfrom

3.from the above bivariate analysis it is clear that number of movies &Tv show added from the year 2014 to 2019 will be highest and then it decreases

4.USA is the counrty where maximum number of movies and Tv show are launched followed by India UK 

5.there are only 5 country USA,UK, Japan,India,Canada where movies and Tv show more than 50

6.Documentaries,Dramas,Stand-Up Comedy are the top three catagory in the Netflix

7.from the above it is seen that since 2018 Number of Movies Realesed decreases year by year

8.from the above it is clear that number of tvshow released are more  compair to movies in2021 and a clear increase in trand of tv show realesed

9.since 2020 there is a dreaseing trand in movies and tv show added in Netflix

10.TV-MA,TV-14 are top ratings

11.december to january are the top session to released tvshow and movies in the platfrom

12.the median Number of movies& tvshow per month (518,212)

13.Raúl Campos, Jan Suter,Jay Karas,Marcus Raboy are the top movies director Alastair Fothergill,,Ken Burns,Iginio Straffi,Rob Seidenglanz are top tvshow director

**RECOMANDATION**

1.only 5 country having more than 50 movies and tv show increase the number to 100 to those country in both catagory and also increase the content in movies and tv show in other country so that at least 20 country having more than 100 content in eatch catagory

2.there is a decrease in trand of movies and tv show added in the platfrom so there is need to increase the addition of movies and tv show

3.add more movies and tvshow of Anupam Kher ,Takahiro Sakurai,Om Puri,Shah Rukh Khan, Boman Irani 


4.provide some local and reginal content country wise

5.approch tvshow directordirector like  Alastair Fothergill,,Ken Burns,Iginio Straffi,Rob Seidenglanz to launch their tvseries in collaboration with NETFLIX

6.as the trand of  more number of tvshow released compair to movies so collaborate with some of the tv series to launched its part 2 and 3 in NETFLIX which are having highest view in you tube 

7.add most recent movies as soon as possible

8.increase more number of content on documentary ,standup commedy,& dramas

9.as the sessonality is on december january provide new year gift boucher of 200 rs off
"""

sns.heatmap(df.corr(),annot=True)
plt.title("corelation between released and add year")
plt.show()

"""released and add year are highly corelated

Q.Business Case: Netflix - Data Exploration and Visualisation - Problem | Scaler Academy

ans:
although there is higher reate of launch of tv show compair to movie but still there was more number of movies are added. so the trand for netflix towards movies till the time

created by Rahul Chakraborty
"""