# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import pandas as pd
import os
import string
import re
pd.options.mode.chained_assignment = None 

os.chdir(r"C:\Users\nwfxy\OneDrive\Desktop\Program")
tweets = pd.read_csv(r'smrt_20162018.csv', encoding = "ISO-8859-1")
tweets = pd.read_csv(r'smrt_singapore_output.tsv', encoding = "ISO-8859-1", delimiter = "\t")
train_names_df = pd.read_csv(r'train-station-chinese-names.csv')
tweets_l = tweets.iloc[:,2].tolist()

def filter_tweets(tweets_l, phrase):
    tweets_l  = [ x.lower() for x in tweets_l ] 
    tweets_l  =  [t for t in tweets_l if phrase in t]
    return tweets_l

def filter_tweets_df(tweets, phrase):
    return tweets[tweets["full_text"].str.contains(phrase)]

travel_time = filter_tweets_df(tweets,"travel time|delay|track fault|train fault|power fault")
down = filter_tweets_df(tweets,"no train |not av")



#check if text is in list of names find which word belongs to the list of names of MRT

train_names_df.iloc[:,1] =  [ x.lower() for x in train_names_df.iloc[:,1]]
train_names_df["train_names_nospace"] =  [ x.lower().replace(' ','') for x in train_names_df.iloc[:,1]]

# =============================================================================
# 
# def find_mrtname_index(text, train_names_df):
#     translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
#     text = text.translate(translator)
#     nospace = (set(text.lower().split(" ")) & set(train_names_df.iloc[:,5].tolist()))
#     space = (set(text.lower().split(" |.|,")) & set(train_names_df.iloc[:,1].tolist()))
#     return list(set([train_names_df.iloc[:,5].tolist().index(x) for x in nospace] + [train_names_df.iloc[:,1].tolist().index(x) for x in space]))
# 
# 
# =============================================================================

def find_mrtname_index(text, train_names_df):
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    text = text.translate(translator).lower()
    text = text.replace('recover','')
    Ans = []
    for name in train_names_df.iloc[:,5].tolist():
        if name in text:
            Ans.append(train_names_df.iloc[:,5].tolist().index(name))
    for name in train_names_df.iloc[:,1].tolist():
        if name in text:
            Ans.append(train_names_df.iloc[:,1].tolist().index(name))
    return list(set(Ans))         
            
    
    
def get_trainlines(train_names_df):
    return list(set(train_names_df['stn_code'].str.replace('\d+', '') + 'L'))

trainlines = get_trainlines(train_names_df)
        
def find_trainlines(trainlines,text):
    Ans = []
    for name in trainlines:
        if name in text:
            Ans.append(name)
    return Ans



travel_time['Station1'] = "NA"
travel_time['Station1_Index'] = "NA"
travel_time['Station2'] = "NA"
travel_time['Station2_Index'] = "NA"
travel_time['Line1'] = "NA"
travel_time['Line2'] = "NA"


for i in range(0,len(travel_time)):
    text = travel_time.iloc[i,2]
    index = find_mrtname_index(text,train_names_df)
    lines = find_trainlines(trainlines,text)
    if len(index) > 0:
        travel_time.iloc[i,3] = train_names_df.iloc[index[0],1]
        travel_time.iloc[i,4] = train_names_df.iloc[index[0],0]
    if len(index) > 1:
        travel_time.iloc[i,5] = train_names_df.iloc[index[1],1]
        travel_time.iloc[i,6] = train_names_df.iloc[index[1],0]
    line_ind = 7
    for line in lines:
        travel_time.iloc[i,line_ind] = line
        line_ind = line_ind + 1
    if(travel_time.iloc[i,7] == 'NA' and travel_time.iloc[i,3] != 'NA'):
        travel_time.iloc[i,7] = re.sub('[0-9]', '', travel_time.iloc[i,4]) + 'L'
        
    
    
for i in range(0,len(travel_time)):
  travel_time.iloc[i,1] = travel_time.iloc[i]['created_at'].split(' ')[0]

def rm_dup_tweet(travel_time):
    travel_time2 = travel_time.drop_duplicates(['created_at','Station1','Station2'])
    return travel_time2


    

# remove rows with @
# find train line

travel_time = rm_dup_tweet(travel_time)
travel_time = travel_time[travel_time.full_text.str.contains('@') == False]

travel_time.to_csv("disrupt.csv")

train_names_df['Count'] = 0
    



                                                