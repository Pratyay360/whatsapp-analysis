import re
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

   
   
   
   
   