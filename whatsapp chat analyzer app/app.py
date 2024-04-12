import streamlit as st
import preprocessor,helper
st.title("Whatsapp chat analyzer")
st.subheader("Analyse your whats app chat")
uploaded_file = st.file_uploader("Choose a text file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data= bytes_data.decode("utf-8")
    # st.text(data)
    df=preprocessor.preprocess(data)
    
    st.dataframe(df)
    
    # fetch unique users
    user_list=df["users"].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"Overall")
    st.sidebar.title("Analysis")
    selected_user= st.sidebar.selectbox("The analysis with respect to",user_list)
    if st.sidebar.button('Show analysis'):

        num_messeges,words= helper.fetch_stats(selected_user,df)
        st.sidebar.header(selected_user)

        col1,col2,col3,col4= st.columns([2,2,1,2])
        with col1:
            st.title("Total messeges")
            st.subheader(num_messeges)
        with col2:
            st.title("Total words")
            st.subheader(words)