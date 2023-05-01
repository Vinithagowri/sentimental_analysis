#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importing nesssary libraries to perform sentiment analysis
import numpy as np  #To manipulate datasets
import pandas as pd 
import tweepy # to extrate tweets
import re     # for cleaning tweets
import matplotlib.pyplot as plt  #to visualize the data
from textblob import TextBlob
from wordcloud import WordCloud   # to create word cloud for our data


# In[2]:


# function to extract the tweets from twitter API
#this function get the use query an extract the tweets and return it as dataframe
def extract_tweets(keyword):
    consumer_key='QEucacPA4PSBPyvogFdTTn'
    consumer_key_token='3YQlDxT9azthvVnPZc2yBWZDFpvPAZtChm9ZndnAZFD49rb'
    access_key='1613040908085374978-IlnfD6zopVDKjvymp3ZvYZ2W9t'
    access_key_secret='aX2Xhwu06CQzQiAGCR9SDKRpvnkKQjCsd6VnWMIp'
    auth=tweepy.OAuthHandler(consumer_key,consumer_key_token)
    auth.set_access_token(access_key,access_key_secret)
    api=tweepy.API(auth)
    tweets=tweepy.Cursor(api.search_tweets,q=keyword,lang='en',tweet_mode='extended').items(300)
    tl=[[tweet.created_at,tweet.full_text,tweet.retweet_count] for tweet in tweets]
    df=pd.DataFrame(tl,columns=["created at",'tweet','retweets'])
    return df


# In[3]:


#this function cleans the tweet so that the unwanted parts of tweet canbe removed
#this uses Regular expression library to clean the tweets
def cleantxt(text):
    text=re.sub(r'@[A-Za-z0-9_]+','',text)  # it removes '@'mentions
    text=re.sub(r'#',"",text)               # it removes hash tags(#)
    text=re.sub(r'RT[\s]+','',text)         # it removes Retweets
    text=re.sub(r'https:\/\/\s+','',text)   # it removes urls ans links
    text = re.sub(u'['                     # it removes emojies
    u'\U0001F300-\U0001F64F'
    u'\U0001F680-\U0001F6FF'
    u'\u2600-\u26FF\u2700-\u27BF]+','',text)
    text = re.sub('http[^\s]+','',text)
    return text


# In[4]:


# these functions per form some natural language processing
# and find out the subjectivity and polarity of tweets
def getsub(text):
    return TextBlob(text).sentiment.subjectivity
def getpola(text):
    return TextBlob(text).sentiment.polarity


# In[ ]:


#this function helps to identify whether the tweet is positive/negative/neutral
def analysis(score):
    if(score<0):
        return 'negative'
    elif(score>0):
        return 'positive'
    else:
        return 'neutral'


# In[23]:


# this is our main functions
# the call of above function are here


keyword=input("enter the #tag which you what to know about the sentiment score")
df=extract_tweets(keyword)
df['tweet']=df['tweet'].apply(cleantxt)
df['polarity']=df['tweet'].apply(getpola)
df['subjectivity']=df['tweet'].apply(getsub)
df['analysis']=df['polarity'].apply(analysis)
print(f"the sentimental analysis hasbeen done for yur hash tag : {keyword}")
while(True):
    print("""
          1.To see the data set
          2.To see the word cloud of the data
          3.To see the nature of the tweets
          4.To visualise the finding
          5.To download the data set
          6.exit
          """)
    ch=int(input("enter your choice  "))
    if(ch==1):
        print(df)
    elif(ch==2):
        alword=' '.join([twt for twt in df['tweet']])  #it create a word cloud using wordcloud module of python
        wc=WordCloud(width=500,height=300,random_state=21,max_font_size=100).generate(alword)
        plt.imshow(wc,interpolation='bilinear')
        plt.axis('off')
        plt.show()
    elif(ch==3):
        x=df.groupby(df['analysis']).count()
        print(x)
    elif(ch==4):
        plt.hist(df["analysis"])
        plt.show()
    elif(ch==5):
        df.to_csv('cleaned_bitcoin.csv')   # which save our result data set
        print("dataset has been save in your current working directory")
    elif(ch==6):
        break
    else:
        break
        
        

