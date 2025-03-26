import streamlit as st

#Me
#  
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")

with col1:
    st.image("./assets/Abie Anders Passport Sized Photo 80kb - 2024.jpg", width=230)
with col2:
    st.title("Abie Anders R", anchor=False)
    st.write("Welcome, look around")

#st.markdown("---")
#st.markdown('<hr style="border:1px solid gray;">', unsafe_allow_html=True)
st.divider()

#Documentation

st.title("Documentation")
st.write("Please proceed with use of the application in the following order,")
st.write("### 1) Go to the Search page")
st.write("• Click the 'Search & Extract' button.")
st.write("### 2) Go to the Analysis page")
st.write("• Click the 'Analyse Sentiment' button.")
st.write("• The audio files will automatically be downloaded once sentiment analysis is complete")
st.write("• Click either the 'Generate Comparison Report' or 'Collected Data' buttons.")
st.write("The order no longer matters and the data will persist unless the session is reset or a new query is searched up.")
st.divider()

st.title("Running the app")
st.write("• Clone the repo from https://github.com/AbieAnders/Sentiment-Analysis.git")
st.write("• Create a python virtual environment.")
st.write("• Install the dependencies using pip.")
st.write("• Now run 'cd client' and 'streamlit run main.py' for the frontend.")
st.write("• And run 'cd server' and 'uvicorn main:app --reload' for the backend.")

st.divider()
st.title("Design choices")
st.write("I chose to perform a lot of the data processing in the search page because I believe that users will be willing to wait longer when the search results are being extracted than when sentiment analysis is done.")
st.write("I decided to use **FastAPI** because it was familiar for me and used **streamlit**(not too great an experience) because it was suggested.")