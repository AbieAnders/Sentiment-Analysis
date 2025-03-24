import requests
import streamlit as st
api_base_url = st.secrets["api_base_url"]

# Default Sidebar
st.sidebar.markdown("#### Search Settings")

region_options = ["Worldwide-English", "US-English", "Uk-English", "India-English"]
time_options = ["Past day", "Past week", "Past month", "Past year"]
safesearch_options = ["Off", "Moderate", "On"]

if "region_choice" not in st.session_state:
    st.session_state.region_choice = region_options[0]
if "time_choice" not in st.session_state:
    st.session_state.time_choice = time_options[2]
if "safesearch_choice" not in st.session_state:
    st.session_state.safesearch_choice = safesearch_options[0]

region_choice = st.sidebar.selectbox("Search region", options=region_options, index=region_options.index(st.session_state.region_choice))
time_choice = st.sidebar.selectbox("Search time frame", options=time_options, index=time_options.index(st.session_state.time_choice))
safesearch_choice = st.sidebar.selectbox("Search moderation", options=safesearch_options, index=safesearch_options.index(st.session_state.safesearch_choice))

st.session_state.region_choice = region_choice
st.session_state.time_choice = time_choice
st.session_state.safesearch_choice = safesearch_choice

region_mapping = {
    "Worldwide-English": "wt-wt",
    "US-English": "us-en",
    "Uk-English": "uk-en",
    "India-English": "in-en",
}

time_mapping = {
    "Past day": "d",
    "Past week": "w",
    "Past month": "m",
    "Past year": "y",
}

safesearch_mapping = {
    "Off": "off",
    "Moderate": "moderate",
    "On": "on",
}

selected_region = region_mapping[region_choice]
selected_time = time_mapping[time_choice]
selected_moderation = safesearch_mapping[safesearch_choice]

# Main content

# Initialize session state
if "search_terms" not in st.session_state:
    st.session_state.search_terms = ""

st.session_state.search_terms = st.text_input(f"Find company reports within {time_choice}", value=st.session_state.search_terms)

if "search_completed" not in st.session_state:
    st.session_state.search_completed = False
if "search_results" not in st.session_state:
    st.session_state.search_results = []


st.title("Search & Results")

if st.button("Search & Extract"):
    if not st.session_state.search_terms.strip():
        st.status("Invalid input", state="error")
    else:
        with st.status(label="Searching... Please wait", state="running", expanded=True) as status:
            try:
                search_api_url = f"{api_base_url}/api/search/search_ddg" #change it from being hardcoded
                params = {
                    "search_query": st.session_state.search_terms,
                    "search_region": selected_region,
                    "search_moderation": selected_moderation,
                    "search_time": selected_time,
                }
                search_response = requests.get(search_api_url, params=params)

                if search_response.status_code == 200:
                    st.write(f"### Search Terms: {st.session_state.search_terms}")
                    st.session_state.search_results = search_response.json().get("results", [])
                    print(st.session_state.search_results)

                    if st.session_state.search_results:
                        status.update(label="Results found", state="complete", expanded=True)
                        st.success(f"{len(st.session_state.search_results)} articles found in the news tab")
                        st.session_state.search_completed = True
                elif search_response.status_code == 404:
                    status.update(label="No results found, please try different keywords", state="error", expanded=True)
                    st.warning("The keywords cannot find articles in the news tab")
                else:
                    status.update(label="An unknown error occurred", state="error", expanded=True)
                    st.error(f"API response log: {search_response.json().get('detail', 'detail key missing')}") #detail key may not be the only thing to look at
            except Exception as e:
                status.update(label="An error occurred", state="error", expanded=True)
                st.error(f"Error: {str(e)}")

if st.session_state.search_completed and st.session_state.search_results:
    st.write("### Search Results")
    for article in st.session_state.search_results:
        with st.expander(f"{article['source']}"): #Can also use title key
            st.markdown(f"#### {article['title']}")
            st.write(f"{article['body']}") #Render something else for a better description
            try:
                if article.get('image') and article['image'].startswith(('http://', 'https://')):
                    image_req = requests.head(article['image'], timeout=5)
                    if image_req.status_code==200 and image_req.headers.get("Content-Type", "").startswith("image/"):
                        st.image(article['image'], use_container_width=True)
                    else:
                        st.warning("Image currently unavailable for this article")
                else:
                    st.warning("Image not found for this article")
            except Exception as e:
                st.warning(f"Unable to load image: {str(e)}")
            st.markdown(f"[Visit article]({article['url']})")
    