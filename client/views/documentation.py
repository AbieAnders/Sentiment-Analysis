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