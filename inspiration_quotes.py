# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 02:31:25 2018

@author: My Pc
"""

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import pandas as pd

bot=ChatBot('Inspiration Quotes')
bot.set_trainer(ListTrainer)
df=pd.read_csv('quotes_data.csv',encoding ='latin1')
new = df["hrefs"].str.split("src=t_", n = 1, expand = True)
df['quotes_type']=new[1]
author = df["lines"].str.split(".-", n = 1, expand = True)
df["quotes_lines"]=author[0]
dataset=df.drop(['lines', 'hrefs'], axis=1)
df_new = dataset.groupby('quotes_type').agg({'quotes_lines': ', '.join}).reset_index()
final_df=df_new[['quotes_type','quotes_lines']]
for index, row in final_df.iterrows():
    ques=row['quotes_type']
    ans=row['quotes_lines']
    bot.train([ques, ans])

while True:
    message=input('You:')
    if message.strip() !='Bye':

        reply=bot.get_response(message)
        print('Chatbot :',reply)
    if message.strip()=='Bye':
        print('Chatbot : Bye')
        break