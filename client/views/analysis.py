import pandas as pd
import requests
import streamlit as st
api_base_url = st.secrets["api_base_url"]
import plotly.express as px # type: ignore

if "data" not in st.session_state:
    st.session_state.data = None

st.title("Sentiment & Comparative Analysis")

if st.sidebar.button("Analyze Sentiment"):
    try:
        response = requests.post(f"{api_base_url}/api/analyse/sentiment_rpt", json={"articles": st.session_state.search_results})
        if response.status_code == 200:
            st.session_state.data = response.json()
            data = st.session_state.data
            st.write("## Sentiment Analysis Results")
            for res in data["analysis"]:
                    st.write(f"**Text:** {res['text']}")
                    st.write(f"**Sentiment:** {res['sentiment']}")
                    st.write(f"**Confidence Score:** {res['score']:.2f}")
                    st.write("---")

            if data.get("most_positive"):
                st.write("### Most Positive Text")
                st.write(f"**Text:** {data['most_positive']['text']}")
                st.write(f"**Score:** {data['most_positive']['score']:.2f}")

            if data.get("most_negative"):
                st.write("### Most Negative Text")
                st.write(f"**Text:** {data['most_negative']['text']}")
                st.write(f"**Score:** {data['most_negative']['score']:.2f}")
        else:
            st.error("Error analyzing sentiment. Please try again.")
    except Exception as e:
            st.error(f"An error occurred: {e}")
if st.sidebar.button("Generate Comparison Report"):
    if st.session_state.data is None:
        st.error("Please analyze sentiment first by clicking 'Analyze Sentiment'.")
    else:
        try:
            data = st.session_state.data
            df = pd.DataFrame(data["analysis"])

            fig = px.histogram(df, x='sentiment', title='Sentiment Distribution')
            st.plotly_chart(fig)

            avg_score = df['score'].mean()
            st.write(f"### Average Sentiment Score: {avg_score:.2f}")

            st.write("### Most Positive and Negative Texts")
            if data["most_positive"]:
                st.write("**Most Positive:**")
                st.write(f"{data['most_positive']['text']}")
                st.write(f"Score: {data['most_positive']['score']:.2f}")
            if data["most_negative"]:
                st.write("**Most Negative:**")
                st.write(f"{data['most_negative']['text']}")
                st.write(f"Score: {data['most_negative']['score']:.2f}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
