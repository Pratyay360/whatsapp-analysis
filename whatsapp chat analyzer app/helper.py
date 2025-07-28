import re
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import emoji
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from urllib.parse import urlparse

def fetch_stats(selected_user, df_original):
    # Stats: msgs, words, media, links.
    df = df_original.copy()
    
    # Filter data based on selected user
    if selected_user != 'Overall':
        df = df[(df['users'] == selected_user) &
                (~df['users'].isin(['group_notification', 'unknown_user', 'empty_message', 'error_processing']))]
    else:
        df = df[~df['users'].isin(['group_notification', 'unknown_user', 'empty_message', 'error_processing'])]
    
    if df.empty:
        return 0, 0, 0, 0
    
    num_messages = df.shape[0]
    
    # Count words efficiently
    words = []
    for message in df['message']:
        if pd.notna(message) and str(message).strip():
            words.extend(str(message).split())
    
    # Count links with improved pattern
    links = []
    for message in df['message']:
        if pd.notna(message):
            url_pattern = r'https?://\S+|www\.\S+'
            urls = re.findall(url_pattern, str(message))
            links.extend(urls)
    
    # Count media messages
    media_messages_df = df[df['message'].astype(str).str.contains("<Media omitted>", case=False, na=False)]
    media_count = media_messages_df.shape[0]
    
    return num_messages, len(words), media_count, len(links)

# Active users and percentages.
def most_busy_user(df):
    """Return active users and their percentages."""
    user_df = df[~df['users'].isin(['group_notification', 'unknown_user', 'empty_message', 'error_processing'])]
    
    if user_df.empty:
        return pd.Series(dtype='int'), pd.DataFrame(columns=['Name', 'Percent'])
    
    x = user_df['users'].value_counts().head()
    
    # Calculate percentages
    percent_df = round(((user_df['users'].value_counts()) / user_df.shape[0]) * 100, 2).reset_index()
    percent_df.columns = ['Name', 'Percent']
    
    return x, percent_df

# Create word cloud.
def create_wordcloud(selected_user, df):
    """Generate a word cloud for messages."""
    if selected_user != 'Overall':
        df_filtered = df[df['users'] == selected_user]
    else:
        df_filtered = df.copy()
    
    # Remove media messages and null values
    temp = df_filtered[~df_filtered['message'].astype(str).str.contains("<Media omitted>", case=False, na=False)]
    temp = temp.dropna(subset=['message'])
    
    if temp.empty:
        return None
    
    # Load Bengali stop words with better error handling
    try:
        with open('bengali_stop_words.txt', 'r', encoding='utf-8') as f:
            stop_words = set([line.strip() for line in f if line.strip()])
    except FileNotFoundError:
        print("Warning: bengali_stop_words.txt not found. Using empty stop words set.")
        stop_words = set()
    except Exception as e:
        print(f"Error reading stop words file: {e}")
        stop_words = set()
    
    # Filter messages by removing stop words
    filtered_messages = []
    for message in temp['message']:
        if pd.notna(message) and str(message).strip():
            words = [w for w in str(message).split() if w.lower() not in stop_words and len(w) > 1]
            if words:  # Only add if there are words left after filtering
                filtered_messages.append(' '.join(words))
    
    if not filtered_messages:
        return None
    
    text_for_wc = ' '.join(filtered_messages)
    if not text_for_wc.strip():
        return None
    
    try:
        wc = WordCloud(width=500, height=500, min_font_size=10, background_color="white").generate(text_for_wc)
        return wc
    except Exception as e:
        print(f"Error generating word cloud: {e}")
        return None

# Most common words.
def most_common_words(selected_user, df):
    """Return 20 most common words."""
    # Load stop words with better error handling
    try:
        with open('bengali_stop_words.txt', 'r', encoding='utf-8') as f:
            stop_words = set([line.strip() for line in f if line.strip()])
    except FileNotFoundError:
        print("Warning: bengali_stop_words.txt not found. Using empty stop words set.")
        stop_words = set()
    except Exception as e:
        print(f"Error reading stop words file: {e}")
        stop_words = set()
    
    if selected_user != 'Overall':
        df_filtered = df[df['users'] == selected_user]
    else:
        df_filtered = df.copy()
    
    # Filter out media messages and null values
    temp = df_filtered[~df_filtered['message'].astype(str).str.contains("<Media omitted>", case=False, na=False)]
    temp = temp.dropna(subset=['message'])
    
    if temp.empty:
        return pd.DataFrame(columns=['Word', 'Frequency'])
    
    words = []
    for message in temp['message']:
        if pd.notna(message) and str(message).strip():
            for word in str(message).lower().split():
                # Filter out stop words and very short words
                if word not in stop_words and len(word) > 1 and word.isalpha():
                    words.append(word)
    
    if not words:
        return pd.DataFrame(columns=['Word', 'Frequency'])
    
    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Frequency'])
    return most_common_df
    
def monthly_timeline(selected_user, df):
    # Monthly timeline.
    if selected_user != 'Overall':
        df_filtered = df[df['users'] == selected_user]
    else:
        df_filtered = df.copy()
    
    if df_filtered.empty:
        return pd.DataFrame(columns=['year', 'month', 'month_num', 'message', 'time'])
    
    try:
        timeline = df_filtered.groupby(['year', 'month', 'month_num']).count()['message'].reset_index()
        
        # Create time labels for better visualization
        time = []
        for i in range(timeline.shape[0]):
            time.append(f"{timeline['month'][i]}-{timeline['year'][i]}")
        timeline['time'] = time
        
        return timeline
    except Exception as e:
        print(f"Error in monthly_timeline: {e}")
        return pd.DataFrame(columns=['year', 'month', 'month_num', 'message', 'time'])

def daily_timeline(selected_user, df):
    # Daily timeline.
    if selected_user != 'Overall':
        df_filtered = df[df['users'] == selected_user]
    else:
        df_filtered = df.copy()
    
    if df_filtered.empty:
        return pd.DataFrame(columns=['specific_date', 'message'])
    
    try:
        daily_timeline_df = df_filtered.groupby('specific_date').count()['message'].reset_index()
        return daily_timeline_df
    except Exception as e:
        print(f"Error in daily_timeline: {e}")
        return pd.DataFrame(columns=['specific_date', 'message'])

def week_activity_map(selected_user, df):
    # Weekly activity map.
    if selected_user != 'Overall':
        df_filtered = df[df['users'] == selected_user]
    else:
        df_filtered = df.copy()
    
    if df_filtered.empty:
        return pd.Series(dtype='int')
    
    try:
        return df_filtered["day_name"].value_counts()
    except Exception as e:
        print(f"Error in week_activity_map: {e}")
        return pd.Series(dtype='int')

def month_activity_map(selected_user, df):
    # Monthly activity map.
    if selected_user != 'Overall':
        df_filtered = df[df['users'] == selected_user]
    else:
        df_filtered = df.copy()
    
    if df_filtered.empty:
        return pd.Series(dtype='int')
    
    try:
        return df_filtered["month"].value_counts()
    except Exception as e:
        print(f"Error in month_activity_map: {e}")
        return pd.Series(dtype='int')

def activity_heatmap(selected_user, df):
    # Activity heatmap.
    if df.empty:
        return pd.DataFrame()
    
    if selected_user != 'Overall':
        df_filtered = df[df['users'] == selected_user]
    else:
        df_filtered = df.copy()
    
    if df_filtered.empty:
        return pd.DataFrame()
    
    try:
        user_heatmap = df_filtered.pivot_table(
            index='day_name', 
            columns='period', 
            values='message', 
            aggfunc="count"
        ).fillna(0)
        return user_heatmap
    except Exception as e:
        print(f"Error in activity_heatmap: {e}")
        return pd.DataFrame()

# Analyze sentiment.
def analyze_sentiment(selected_user, df):
    """Perform sentiment analysis per message."""
    if selected_user != 'Overall':
        df_filtered = df[df['users'] == selected_user]
    else:
        df_filtered = df.copy()
    temp = df_filtered[~df_filtered['message'].astype(str).str.contains("<Media omitted>", case=False, na=False)]
    temp = temp.dropna(subset=['message'])
    if temp.empty:
        return pd.DataFrame()
    analyzer = SentimentIntensityAnalyzer()
    sentiments = []
    polarities = []
    subjectivities = []
    for message in temp['message']:
        text = str(message)
        vs = analyzer.polarity_scores(text)
        if vs['compound'] >= 0.05:
            sentiments.append('Positive')
        elif vs['compound'] <= -0.05:
            sentiments.append('Negative')
        else:
            sentiments.append('Neutral')
        tb = TextBlob(text)
        polarities.append(tb.polarity)
        subjectivities.append(tb.subjectivity)
    temp = temp.copy()
    temp['sentiment'] = sentiments
    temp['polarity'] = polarities
    temp['subjectivity'] = subjectivities
    return temp

# Sentiment summary.
def sentiment_summary(selected_user, df):
    """Summarize sentiment counts."""
    sentiment_df = analyze_sentiment(selected_user, df)
    if sentiment_df.empty or 'sentiment' not in sentiment_df.columns:
        return pd.DataFrame(columns=['Sentiment', 'Count'])
    summary = sentiment_df['sentiment'].value_counts().reset_index()
    summary.columns = ['Sentiment', 'Count']
    return summary

def emotion_timeline(selected_user, df):
    # Emotion timeline.
    sentiment_df = analyze_sentiment(selected_user, df)
    if sentiment_df.empty:
        return pd.DataFrame()
    sentiment_df['date'] = pd.to_datetime(sentiment_df['date'])
    sentiment_df['specific_date'] = sentiment_df['date'].dt.date  # Add this line for plotting
    timeline = sentiment_df.groupby(['specific_date', 'sentiment']).size().unstack(fill_value=0).reset_index()
    return timeline

def emoji_analysis(selected_user, df):
    # Emoji analysis.
    if selected_user != 'Overall':
        df_filtered = df[df['users'] == selected_user]
    else:
        df_filtered = df.copy()
    temp = df_filtered[~df_filtered['message'].astype(str).str.contains("<Media omitted>", case=False, na=False)]
    temp = temp.dropna(subset=['message'])
    if temp.empty:
        return pd.DataFrame(columns=['Emoji', 'Count'])
    emojis = []
    for message in temp['message']:
        emojis.extend([c for c in str(message) if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(20), columns=['Emoji', 'Count'])
    return emoji_df

def message_length_analysis(selected_user, df):
    # Message length analysis.
    if selected_user != 'Overall':
        df_filtered = df[df['users'] == selected_user]
    else:
        df_filtered = df.copy()
    temp = df_filtered[~df_filtered['message'].astype(str).str.contains("<Media omitted>", case=False, na=False)]
    temp = temp.dropna(subset=['message'])
    if temp.empty:
        return pd.DataFrame(columns=['users', 'message_length'])
    temp = temp.copy()
    temp['message_length'] = temp['message'].apply(lambda x: len(str(x)))
    # Ensure 'users' column is present for overall mode
    if 'users' not in temp.columns:
        temp['users'] = df_filtered['users']
    return temp[['users', 'message_length']]

def response_time_analysis(df):
    # Response time analysis.
    # Only for overall, not per user
    df_sorted = df.sort_values('date')
    df_sorted = df_sorted[~df_sorted['users'].isin(['group_notification', 'unknown_user', 'empty_message', 'error_processing'])]
    if df_sorted.empty or df_sorted.shape[0] < 2:
        return pd.DataFrame(columns=['responder', 'response_time_minutes'])
    response_times = []
    prev_user = None
    prev_time = None
    for idx, row in df_sorted.iterrows():
        user = row['users']
        time = row['date']
        if prev_user is not None and user != prev_user:
            diff = (time - prev_time).total_seconds() / 60.0
            if 0 < diff < 720:  # Ignore gaps > 12 hours
                response_times.append({'responder': user, 'response_time_minutes': diff})
        prev_user = user
        prev_time = time
    return pd.DataFrame(response_times)

def conversation_starters(df):
    # Conversation starters.
    # A conversation is started if the time gap from previous message is > 2 hours
    df_sorted = df.sort_values('date')
    df_sorted = df_sorted[~df_sorted['users'].isin(['group_notification', 'unknown_user', 'empty_message', 'error_processing'])]
    if df_sorted.empty or df_sorted.shape[0] < 2:
        return pd.DataFrame(columns=['User', 'Conversations_Started'])
    starters = []
    prev_time = None
    prev_user = None
    for idx, row in df_sorted.iterrows():
        user = row['users']
        time = row['date']
        if prev_time is None or (time - prev_time).total_seconds() > 7200:
            starters.append(user)
        prev_time = time
        prev_user = user
    starter_counts = Counter(starters)
    starter_df = pd.DataFrame(starter_counts.items(), columns=['User', 'Conversations_Started'])
    starter_df = starter_df.sort_values('Conversations_Started', ascending=False).reset_index(drop=True)
    return starter_df

def get_chat_insights(selected_user, df):
    # Chat insights summary.
    if df.empty:
        return {}
    if selected_user != 'Overall':
        df_filtered = df[df['users'] == selected_user]
    else:
        df_filtered = df.copy()
    total_messages = df_filtered.shape[0]
    if total_messages == 0:
        return {}
    date_range = {}
    if 'date' in df_filtered.columns:
        min_date = df_filtered['date'].min()
        max_date = df_filtered['date'].max()
        date_range = {
            'start': str(min_date.date()),
            'end': str(max_date.date()),
            'duration_days': (max_date - min_date).days + 1
        }
    avg_messages_per_day = total_messages / date_range['duration_days'] if date_range and date_range['duration_days'] > 0 else 0
    peak_activity = {}
    if 'day_name' in df_filtered.columns:
        peak_day = df_filtered['day_name'].value_counts().idxmax()
        peak_activity['day'] = peak_day
    if 'hour' in df_filtered.columns:
        peak_hour = df_filtered['hour'].value_counts().idxmax()
        peak_activity['hour'] = peak_hour
    if 'month' in df_filtered.columns:
        peak_month = df_filtered['month'].value_counts().idxmax()
        peak_activity['month'] = peak_month
    
    # URL Analysis part for insights
    links = []
    for message in df_filtered['message']:
        if pd.notna(message):
            url_pattern = r'https?://\S+|www\.\S+'
            urls_found = re.findall(url_pattern, str(message))
            links.extend(urls_found)
    
    return {
        'total_messages': total_messages,
        'date_range': date_range,
        'avg_messages_per_day': avg_messages_per_day,
        'peak_activity': peak_activity,
        'total_links_shared': len(links),
        'unique_links_shared': len(set(links))
    }

def analyze_urls(selected_user, df):
    # Analyze URL domains.
    if selected_user != 'Overall':
        df_filtered = df[df['users'] == selected_user]
    else:
        df_filtered = df.copy()

    temp = df_filtered[~df_filtered['message'].astype(str).str.contains("<Media omitted>", case=False, na=False)]
    temp = temp.dropna(subset=['message'])

    if temp.empty:
        return pd.DataFrame(columns=['Domain', 'Count'])

    links = []
    for message in temp['message']:
        if pd.notna(message):
            url_pattern = r'https?://\S+|www\.\S+'
            urls_found = re.findall(url_pattern, str(message))
            links.extend(urls_found)
    
    if not links:
        return pd.DataFrame(columns=['Domain', 'Count'])

    domains = []
    for link in links:
        try:
            parsed_url = urlparse(link)
            domain = parsed_url.netloc
            if domain.startswith('www.'):
                domain = domain[4:]
            domains.append(domain)
        except Exception:
            # Handle cases where URL parsing might fail for malformed links
            domains.append("unknown_domain")
            
    domain_counts = Counter(domains)
    domain_df = pd.DataFrame(domain_counts.items(), columns=['Domain', 'Count']).sort_values(by='Count', ascending=False)
    return domain_df

def export_analysis_summary(selected_user, df):
    # Export analysis summary.
    insights = get_chat_insights(selected_user, df)
    if not insights:
        return "No data available."
    lines = [f"Analysis Summary for: {selected_user}"]
    lines.append(f"Total Messages: {insights.get('total_messages', 0)}")
    dr = insights.get('date_range', {})
    if dr:
        lines.append(f"Date Range: {dr.get('start', 'N/A')} to {dr.get('end', 'N/A')} ({dr.get('duration_days', 0)} days)")
    lines.append(f"Average Messages/Day: {insights.get('avg_messages_per_day', 0):.1f}")
    pa = insights.get('peak_activity', {})
    if pa:
        lines.append(f"Peak Day: {pa.get('day', 'N/A')}")
        lines.append(f"Peak Hour: {pa.get('hour', 'N/A')}:00") # Corrected to show :00 for hour
        lines.append(f"Peak Month: {pa.get('month', 'N/A')}")
    
    lines.append(f"Total Links Shared: {insights.get('total_links_shared', 0)}")
    lines.append(f"Unique Links Shared: {insights.get('unique_links_shared', 0)}")
    
    # Add sentiment summary if available
    sentiment_data = sentiment_summary(selected_user, df)
    if not sentiment_data.empty:
        lines.append("\nSentiment Overview:")
        for _, row in sentiment_data.iterrows():
            lines.append(f"- {row['Sentiment']}: {row['Count']} messages")

    # Add top 5 most common words
    common_words_data = most_common_words(selected_user, df)
    if not common_words_data.empty:
        lines.append("\nTop 5 Most Common Words:")
        for i, row in common_words_data.head(5).iterrows():
            lines.append(f"- {row['Word']}: {row['Frequency']} times")

    return '\n'.join(lines)







