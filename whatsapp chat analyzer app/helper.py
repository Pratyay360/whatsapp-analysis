def fetch_stats(selected_user,df):
    if selected_user=='Overall':
        num_messages=df.shape[0]
        return 
    else:
        return df[df['users']==selected_user].shape[0]