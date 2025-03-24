import streamlit as st

doc_page = st.Page(
    page="views/documentation.py",
    title='Documentation',
    icon=":material/account_circle:", #change
    default=True,
)

search_page = st.Page(
    page="views/search.py",
    title="Search",
    icon=":material/bar_chart:", #change
)

analysis_page = st.Page(
    page="views/analysis.py",
    title="Analysis",
    icon=":material/bar_chart:", #change
)

pg = st.navigation(
    {
        "Info": [doc_page],
        "Pages": [search_page, analysis_page],
    }
)

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            display: flex;
            flex-direction: column;
        }
        [data-testid="stSidebar"] > div:nth-child(2) {
            margin-top: auto;
        }
    </style>
    """,
    unsafe_allow_html=True
)

pg.run()