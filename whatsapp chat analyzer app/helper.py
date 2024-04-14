import re
from wordcloud import WordCloud

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
      
   wc=WordCloud(width=500,height=500,min_font_size=10,background_color="white")
   df_wc=wc.generate(df['message'].str.cat(sep=" "))
   return df_wc
    
   

   
   
   
   
   