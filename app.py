import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("💬 WhatsApp Chat Analyzer")
st.markdown("### Analyze your WhatsApp chat exports with detailed insights and visualizations")

# Sidebar for file upload
st.sidebar.title("📁 Upload Chat File")
st.sidebar.markdown("Export your WhatsApp chat as a text file and upload it here.")
uploaded_file = st.sidebar.file_uploader(
    "Choose a WhatsApp chat text file", 
    type=['txt'],
    help="Export chat from WhatsApp and select the .txt file"
)
if uploaded_file is not None:
    try:
        # Read file with error handling
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        
        # Process the chat data
        with st.spinner("Processing chat data..."):
            df = preprocessor.preprocess(data)
        
        if df.empty:
            st.error("❌ The uploaded file does not contain valid chat data. Please upload a valid WhatsApp chat file.")
            st.info("💡 **How to export WhatsApp chat:**\n"
                   "1. Open WhatsApp\n"
                   "2. Go to the chat you want to analyze\n"
                   "3. Tap the three dots (⋮) → More → Export chat\n"
                   "4. Choose 'Without Media' for faster processing\n"
                   "5. Save the .txt file and upload it here")
            st.stop()
        
        # Success message
        st.success(f"✅ Chat data processed successfully! Found {len(df)} messages.")
        
    except UnicodeDecodeError:
        st.error("❌ Error reading the file. Please ensure it's a valid text file with UTF-8 encoding.")
        st.stop()
    except Exception as e:
        st.error(f"❌ An error occurred while processing the file: {str(e)}")
        st.stop()
    # Prepare user list for analysis
    user_list = df["users"].unique().tolist()
    
    # Remove system messages from user list
    system_users = ["group_notification", "unknown_user", "empty_message", "error_processing"]
    for sys_user in system_users:
        if sys_user in user_list:
            user_list.remove(sys_user)
    
    user_list.sort()
    user_list.insert(0, "Overall")
    
    # Sidebar for user selection and analysis options
    st.sidebar.title("🔍 Analysis Options")
    selected_user = st.sidebar.selectbox(
        "Select user for analysis", 
        user_list,
        help="Choose 'Overall' for group analysis or select a specific user"
    )
    
    # Display basic info
    st.sidebar.markdown("---")
    st.sidebar.markdown("**📊 Quick Stats:**")
    total_users = len([u for u in df["users"].unique() if u not in system_users])
    st.sidebar.info(f"👥 **{total_users}** active users\n\n📅 **{len(df)}** total messages")
    
    # Analysis button
    show_analysis = st.sidebar.button('🚀 Show Detailed Analysis', type="primary")
    # Top Statistics Section
    if show_analysis:
        try:
            num_messages, words, media, num_links = helper.fetch_stats(selected_user, df)
            
            st.sidebar.markdown("---")
            st.sidebar.markdown(f"**Selected:** {selected_user}")
            
            st.title("📊 Top Statistics")
            
            # Create metrics in columns with better styling
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="💬 Total Messages",
                    value=f"{num_messages:,}",
                    help="Total number of messages sent"
                )
            
            with col2:
                st.metric(
                    label="📝 Total Words",
                    value=f"{words:,}",
                    help="Total words across all messages"
                )
            
            with col3:
                st.metric(
                    label="📸 Media Shared",
                    value=f"{media:,}",
                    help="Photos, videos, documents shared"
                )
            
            with col4:
                st.metric(
                    label="🔗 Links Shared",
                    value=f"{num_links:,}",
                    help="URLs shared in messages"
                )
                
        except Exception as e:
            st.error(f"❌ Error calculating statistics: {str(e)}")
    
    else:
        st.info("👆 Click 'Show Detailed Analysis' in the sidebar to start the analysis!")
        st.stop()
            
    # Timeline Analysis Section
    st.title("📈 Timeline Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Monthly Timeline")
        try:
            timeline = helper.monthly_timeline(selected_user, df)
            if not timeline.empty:
                fig = px.line(
                    timeline, 
                    x='time', 
                    y='message', 
                    labels={'time': 'Month-Year', 'message': 'Total Messages'},
                    title=f"Monthly Activity - {selected_user}",
                    markers=True
                )
                fig.update_xaxes(tickangle=45)
                fig.update_layout(hovermode='x unified')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📊 No data available for monthly timeline.")
        except Exception as e:
            st.error(f"❌ Error generating monthly timeline: {str(e)}")
    
    with col2:
        st.subheader("📊 Daily Timeline")
        try:
            daily_timeline = helper.daily_timeline(selected_user, df)
            if not daily_timeline.empty:
                fig = px.line(
                    daily_timeline, 
                    x='specific_date', 
                    y='message', 
                    labels={'specific_date': 'Date', 'message': 'Messages'},
                    title=f"Daily Activity - {selected_user}",
                    color_discrete_sequence=['green']
                )
                fig.update_xaxes(tickangle=45)
                fig.update_layout(hovermode='x unified')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📊 No data available for daily timeline.")
        except Exception as e:
            st.error(f"❌ Error generating daily timeline: {str(e)}")

    # Activity Maps Section
    st.title("🗓️ Activity Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Most Active Days")
        try:
            busy_day = helper.week_activity_map(selected_user, df)
            if not busy_day.empty:
                fig = px.bar(
                    x=busy_day.index, 
                    y=busy_day.values, 
                    labels={'x': 'Day of Week', 'y': 'Message Count'},
                    title=f"Weekly Activity - {selected_user}",
                    color=busy_day.values,
                    color_continuous_scale='Blues'
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
                
                # Show peak day
                peak_day = busy_day.idxmax()
                peak_count = busy_day.max()
                st.info(f"📈 Peak day: **{peak_day}** with {peak_count:,} messages")
            else:
                st.info("📊 No data for weekly activity.")
        except Exception as e:
            st.error(f"❌ Error generating weekly activity: {str(e)}")
    
    with col2:
        st.subheader("📆 Most Active Months")
        try:
            busy_month = helper.month_activity_map(selected_user, df)
            if not busy_month.empty:
                fig = px.bar(
                    x=busy_month.index, 
                    y=busy_month.values, 
                    labels={'x': 'Month', 'y': 'Message Count'},
                    title=f"Monthly Activity - {selected_user}",
                    color=busy_month.values,
                    color_continuous_scale='Reds'
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
                
                # Show peak month
                peak_month = busy_month.idxmax()
                peak_count = busy_month.max()
                st.info(f"📈 Peak month: **{peak_month}** with {peak_count:,} messages")
            else:
                st.info("📊 No data for monthly activity.")
        except Exception as e:
            st.error(f"❌ Error generating monthly activity: {str(e)}")

    # Activity Heatmap Section
    st.title("🔥 Activity Heatmap")
    st.markdown("**Hourly activity patterns throughout the week**")
    
    try:
        user_heatmap = helper.activity_heatmap(selected_user, df)
        
        if user_heatmap.empty or user_heatmap.isnull().values.all():
            st.warning("⚠️ No data available to generate the heatmap.")
        else:
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.heatmap(
                user_heatmap, 
                annot=True, 
                fmt='g', 
                cmap='YlOrRd',
                cbar_kws={'label': 'Number of Messages'},
                ax=ax
            )
            ax.set_title(f'Activity Heatmap - {selected_user}', fontsize=16, pad=20)
            ax.set_xlabel('Time Period', fontsize=12)
            ax.set_ylabel('Day of Week', fontsize=12)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
            
            # Additional insights
            if not user_heatmap.empty:
                max_activity = user_heatmap.max().max()
                max_pos = user_heatmap.stack().idxmax()
                st.info(f"🔥 Peak activity at **{max_pos}** with {max_activity:.0f} messages")
                
    except Exception as e:
        st.error(f"❌ Error generating heatmap: {str(e)}")
    # Most Active Users (Only for Overall view)
    if selected_user == "Overall":
        st.title("👥 Most Active Users")
        
        try:
            x, new_df = helper.most_busy_user(df)
            
            if not x.empty and not new_df.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 User Activity")
                    fig = px.bar(
                        x=x.index, 
                        y=x.values, 
                        labels={'x': 'User', 'y': 'Message Count'},
                        title="Most Active Users",
                        color=x.values,
                        color_continuous_scale='viridis'
                    )
                    fig.update_xaxes(tickangle=45)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.subheader("📈 Activity Percentage")
                    # Create a pie chart for better visualization
                    fig_pie = px.pie(
                        new_df.head(10), 
                        values='Percent', 
                        names='Name',
                        title="Chat Contribution %"
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                # Display table with better formatting
                st.subheader("📋 Detailed Statistics")
                st.dataframe(
                    new_df.style.format({'Percent': '{:.1f}%'}),
                    use_container_width=True
                )
            else:
                st.info("📊 No user activity data available.")
                
        except Exception as e:
            st.error(f"❌ Error analyzing user activity: {str(e)}")
    # Word Analysis Section
    st.title("📝 Word Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("☁️ Word Cloud")
        try:
            df_wc = helper.create_wordcloud(selected_user, df)
            if df_wc is None:
                st.warning("⚠️ No data available to generate the word cloud.")
                st.info("💡 This could be because:\n"
                       "- All messages are media files\n"
                       "- Messages contain only stop words\n"
                       "- No valid text content found")
            else:
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.imshow(df_wc, interpolation='bilinear')
                ax.axis("off")
                ax.set_title(f'Word Cloud - {selected_user}', fontsize=16, pad=20)
                st.pyplot(fig)
        except Exception as e:
            st.error(f"❌ Error generating word cloud: {str(e)}")
    
    with col2:
        st.subheader("📊 Most Common Words")
        try:
            most_common_df = helper.most_common_words(selected_user, df)
            if not most_common_df.empty:
                fig = px.bar(
                    most_common_df.head(15), 
                    y='Word', 
                    x='Frequency', 
                    orientation='h',
                    labels={'Word': 'Word', 'Frequency': 'Count'},
                    title=f"Top 15 Words - {selected_user}",
                    color='Frequency',
                    color_continuous_scale='blues'
                )
                fig.update_layout(yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
                
                # Show top 3 words
                top_words = most_common_df.head(3)
                st.info(f"🔝 Top words: **{', '.join(top_words['Word'].tolist())}**")
            else:
                st.info("📊 No common words data to display.")
        except Exception as e:
            st.error(f"❌ Error analyzing common words: {str(e)}")
    
    # Sentiment Analysis Section
    st.title("📊 Sentiment Analysis")
    
    # Sentiment Summary
    sentiment_summary = helper.sentiment_summary(selected_user, df)
    if not sentiment_summary.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sentiment Distribution")
            fig = px.pie(sentiment_summary, values='Count', names='Sentiment', title='Sentiment Distribution',
                         color_discrete_map={'Positive':'green', 'Negative':'red', 'Neutral':'blue'})
            st.plotly_chart(fig)
        
        with col2:
            st.subheader("Sentiment Summary")
            st.dataframe(sentiment_summary)
    
    # Emotion Timeline
    st.subheader("Sentiment Over Time")
    emotion_timeline = helper.emotion_timeline(selected_user, df)
    if not emotion_timeline.empty:
        # Melt the DataFrame for Plotly Express
        plot_df = emotion_timeline.melt(id_vars=['specific_date'], value_vars=['Positive', 'Negative', 'Neutral'],
                                        var_name='Sentiment', value_name='Message Count')
        fig = px.line(plot_df, x='specific_date', y='Message Count', color='Sentiment',
                      title='Sentiment Over Time', markers=True,
                      labels={'specific_date': 'Date', 'Message Count': 'Number of Messages'},
                      color_discrete_map={'Positive':'green', 'Negative':'red', 'Neutral':'blue'})
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig)
    else:
        st.info("No data for sentiment over time.")
    
    # Emoji Analysis
    st.title("😊 Emoji Analysis")
    emoji_df = helper.emoji_analysis(selected_user, df)
    if not emoji_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Most Used Emojis")
            fig = px.bar(emoji_df.head(10), y='Emoji', x='Count', orientation='h',
                         labels={'Emoji': 'Emoji', 'Count': 'Frequency'}, title='Top 10 Emojis')
            fig.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig)
        
        with col2:
            st.subheader("Emoji Usage Statistics")
            st.dataframe(emoji_df.head(10))
    
    # Message Length Analysis
    st.title("📝 Message Patterns")
    message_stats = helper.message_length_analysis(selected_user, df)
    if not message_stats.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Average Message Length by User")
            if selected_user == "Overall":
                avg_length = message_stats.groupby('users')['message_length'].mean().sort_values(ascending=False)
                if not avg_length.empty:
                    fig = px.bar(avg_length.head(10), x=avg_length.head(10).index, y=avg_length.head(10).values,
                                 labels={'index': 'User', 'y': 'Average Characters'})
                    fig.update_xaxes(tickangle=45)
                    st.plotly_chart(fig)
                else:
                    st.info("No data for average message length by user.")
        
        with col2:
            st.subheader("Message Length Distribution")
            fig = px.histogram(message_stats, x='message_length', nbins=30,
                               labels={'message_length': 'Message Length (characters)', 'count': 'Frequency'},
                               title='Message Length Distribution')
            st.plotly_chart(fig)
    
    # Response Time Analysis (only for Overall view)
    if selected_user == "Overall":
        st.title("⚡ Response Time Analysis")
        response_times = helper.response_time_analysis(df)
        if not response_times.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Average Response Time by User")
                avg_response = response_times.groupby('responder')['response_time_minutes'].mean().sort_values()
                if not avg_response.empty:
                    fig = px.bar(avg_response, y=avg_response.index, x=avg_response.values, orientation='h',
                                 labels={'index': 'User', 'x': 'Average Response Time (minutes)'})
                    fig.update_layout(yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig)
                else:
                    st.info("No data for average response time.")
            
            with col2:
                st.subheader("Response Time Distribution")
                fig = px.histogram(response_times, x='response_time_minutes', nbins=20,
                                   labels={'response_time_minutes': 'Response Time (minutes)', 'count': 'Frequency'},
                                   title='Response Time Distribution', color_discrete_sequence=['lightcoral'])
                st.plotly_chart(fig)
        
        # Conversation Starters
        st.title("🚀 Conversation Starters")
        starters = helper.conversation_starters(df)
        if not starters.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Who Starts Conversations Most?")
                fig = px.pie(starters, values='Conversations_Started', names='User',
                             title='Conversation Starters')
                st.plotly_chart(fig)
            
            with col2:
                st.subheader("Conversation Starter Statistics")
                st.dataframe(starters)
    
    # URL Analysis Section
    st.title("🔗 URL Analysis")
    url_analysis_df = helper.analyze_urls(selected_user, df)
    if not url_analysis_df.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top Shared Domains")
            # Display top 10 domains
            fig = px.bar(url_analysis_df.head(10), y='Domain', x='Count', orientation='h',
                         labels={'Domain': 'Domain', 'Count': 'Times Shared'}, title='Top 10 Shared Domains')
            fig.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig)
        with col2:
            st.subheader("Domain Share Statistics")
            st.dataframe(url_analysis_df)
    else:
        st.info("No URLs found or no data to analyze for URLs.")
    
    # Chat Insights Summary
    st.title("📈 Chat Insights Summary")
    
    insights = helper.get_chat_insights(selected_user, df)
    summary_text = helper.export_analysis_summary(selected_user, df)
    
    # Display key insights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Messages", f"{insights.get('total_messages', 0):,}")
        st.metric("Duration (Days)", insights.get('date_range', {}).get('duration_days', 0))
    
    with col2:
        st.metric("Messages/Day", f"{insights.get('avg_messages_per_day', 0):.1f}")
        st.metric("Peak Day", insights.get('peak_activity', {}).get('day', 'N/A'))
    
    with col3:
        st.metric("Peak Hour", f"{insights.get('peak_activity', {}).get('hour', 'N/A')}:00")
        st.metric("Peak Month", insights.get('peak_activity', {}).get('month', 'N/A'))
    
    # Exportable summary
    st.subheader("📄 Exportable Analysis Report")
    st.text_area("Analysis Summary (Copy to save)", summary_text, height=300)