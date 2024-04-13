def fetch_stats(selected_user,df):
   if selected_user != 'Overall':
      df=df[df['users']==selected_user]
      num_messeges=df.shape[0]
   num_messeges=df.shape[0]
   words=[]
   for message in df['message']:
      words.extend(message.split())
   df=df[df['message']=="<Media omitted>\n"]
   media=df.shape[0]

   return num_messeges,len(words),media

   
   
   
   
   