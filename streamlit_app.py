import streamlit as st
from st_social_media_links import SocialMediaIcons
from streamlit_extras.bottom_container import bottom

st.set_page_config(
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })

with bottom():
    social_media_links = [
        "https://x.com/blackboxstats",
        "https://www.instagram.com/blackboxstats"
    ]

    social_media_icons = SocialMediaIcons(social_media_links, colors=["#ffffff", "#ffffff"])

    social_media_icons.render()
    