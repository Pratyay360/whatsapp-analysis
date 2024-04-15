import re
from wordcloud import WordCloud
from collections import Counter
import pandas as pd

def fetch_stats(selected_user,df):
   if selected_user != 'Overall':
      df=df[df['users']==selected_user]
      num_messeges=df.shape[0]
   num_messeges=df.shape[0]
   
   words=[]
   for message in df['message']:
      words.extend(message.split())
      
   links=[]
   for message in df['message']:
      url_pattern = r'https?://\S+|www\.\S+' # Regular expression pattern to match URLs
      urls = re.findall(url_pattern,message) # Extract URLs from the text using the regular expression
      links.extend(urls) # Print the extracted URLs
      
   df=df[df['message']=="<Media omitted>\n"]
   media=df.shape[0]
   
   return num_messeges,len(words),media,len(links)

# bar chart and percentage of chatting
def most_busy_user(df):
   x=df['users'].value_counts().head()
   df=round(((df['users'].value_counts())/df.shape[0])*100,2).reset_index().rename(columns={'users':'Name','count':'Percent'})
   return x,df    
#word cloud

def create_wordcloud(selected_user,df):
   if selected_user != 'Overall':
      df=df[df['users']==selected_user]
   temp=df[df['users']!='group_notification']
   temp=temp[temp['message']!='<Media omitted>\n']     
    
   wc=WordCloud(width=500,height=500,min_font_size=10,background_color="white")
   df_wc=wc.generate(temp['message'].str.cat(sep=" "))
   
   return df_wc
# most common words

def most_common_words(selected_user,df):
   
   f=open('bengali_stop_words.txt','r',encoding= 'utf-8')
   stop_words=f.read()
   if selected_user != 'Overall':
      df=df[df['users']==selected_user]
   temp=df[df['users']!='group_notification']
   temp=temp[temp['message']!='<Media omitted>\n']
   words=[]
   for message in temp['message']:
    for word in message.lower().split():
        if word not in stop_words:
            words.append(word)
    most_common_df=pd.DataFrame(Counter(words).most_common(20))
   return most_common_df
    
def monthly_timeline(selected_user,df):
   if selected_user != 'Overall':
      df=df[df['users']==selected_user]
   timeline=df.groupby(['year','month','month_num']).count()['message'].reset_index()
   time=[]
   for i in range(timeline.shape[0]):
      time.append(timeline['month'][i]+'-'+ str(timeline['year'][i]))
   timeline['time']=time
   return timeline

def daily_timeline(selected_user,df):
   if selected_user != 'Overall':
      df=df[df['users']==selected_user]
   daily_timeline=df.groupby('specific_date').count()['message'].reset_index()
   return daily_timeline
def week_activity_map(selected_user,df):
   if selected_user != 'Overall':
      df=df[df['users']==selected_user]
   return df["day_name"].value_counts()
   
def month_activity_map(selected_user,df):
   if selected_user != 'Overall':
      df=df[df['users']==selected_user]
   return df["month"].value_counts()

def activity_heatmap(selected_user,df):
   if selected_user != 'Overall':
      df=df[df['users']==selected_user]
   user_heatmap=df.pivot_table(index='day_name',columns='period',values='message',aggfunc="count").fillna(0)
   return user_heatmap
   
   
   
   
   
   
   
   