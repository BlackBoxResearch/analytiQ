import streamlit as st
from st_social_media_links import SocialMediaIcons
from streamlit_extras.bottom_container import bottom
from pages import dashboard, leaderboard, login, logout, settings, support, pricing, lab, insights

st.set_page_config(
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })

# st.markdown(
#     """
#     <style>
#         /* Hide the Streamlit header */
#         header {visibility: hidden;}
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# Define pages with icons
login_page = st.Page(page=login.login_page, title="Login", icon=":material/login:")
dashboard_page = st.Page(page=dashboard.dashboard_page, title="Dashboard", icon=":material/dashboard:")
support_page = st.Page(page=support.support_page, title="Support", icon=":material/support_agent:")
settings_page = st.Page(page=settings.settings_page, title="Settings", icon=":material/settings:")
logout_page = st.Page(page=logout.logout_page, title="Logout", icon=":material/logout:")
leaderboard_page = st.Page(page=leaderboard.leaderboard_page, title="Leaderboard", icon=":material/social_leaderboard:")
pricing_page = st.Page(page=pricing.pricing_page, title="Pricing", icon=":material/paid:")
lab_page = st.Page(page=lab.lab_page, title="Strategy Lab", icon=":material/experiment:")
insights_page = st.Page(page=insights.insights_page, title="Insights", icon=":material/search_insights:")

# Group pages for logged-out users
logged_out_pages = [login_page]

# Group pages for logged-in users
logged_in_pages = {
    "Trading": [dashboard_page, lab_page],
    "Community": [leaderboard_page, insights_page],
    "Settings": [pricing_page, settings_page, logout_page]  # Logout page added here
}

def create_navigation(pages):
    # Create the navigation sidebar
    selected_page = st.navigation(pages, position="sidebar")
    # Run the selected page function
    selected_page.run()

def main():
    # Initialize session state keys with default values
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "logged_out" not in st.session_state:
        st.session_state["logged_out"] = False
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None  # Default to None or another appropriate default value
    if "first_name" not in st.session_state:
        st.session_state["first_name"] = None
    if "last_name" not in st.session_state:
        st.session_state["last_name"] = None
    if "email" not in st.session_state:
        st.session_state["email"] = None

    # Display pages based on login state
    if st.session_state["logged_in"]:
        st.logo(image="static/analytiq_type_logo_dark.png", size="large", icon_image="static/analytiq_icon.png")

        create_navigation(logged_in_pages)

        with st.sidebar:
            social_media_links = [
                "https://x.com/AnalytIQtrade",
                "https://www.instagram.com/analytiq.trade"
            ]
            social_media_icons = SocialMediaIcons(social_media_links, colors=["#ffffff", "#ffffff"])
            social_media_icons.render()
    else:
        create_navigation(logged_out_pages)

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
