def fetch_stats(selected_user,df):
    if selected_user=='Overall':
       num_messages=df.shape[0]
       words=[]
       for message in df["message"]:
          words.extend(message.split())
       return num_messages,len(words)
    else:
        words=[]
        new_df=df[df['users']=='selected_user'].shape[0]
        num_message=new_df.shape[0]
        for message in new_df["message"]:
              words.extend(message.split())
        return num_message,len(words)
        

