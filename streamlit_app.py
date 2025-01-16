import streamlit as st
from st_social_media_links import SocialMediaIcons
from streamlit_extras.bottom_container import bottom
from pages import accounts, dashboard, leaderboard, login, logout, settings, support, pricing

st.set_page_config(
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })

# Define pages with icons
login_page = st.Page(page=login.login_page, title="Login", icon=":material/login:")
dashboard_page = st.Page(page=dashboard.dashboard_page, title="Dashboard", icon=":material/dashboard:")
support_page = st.Page(page=support.support_page, title="Support", icon=":material/support_agent:")
settings_page = st.Page(page=settings.settings_page, title="Settings", icon=":material/settings:")
logout_page = st.Page(page=logout.logout_page, title="Logout", icon=":material/logout:")
accounts_page = st.Page(page=accounts.accounts_page, title="Accounts", icon=":material/group:")
leaderboard_page = st.Page(page=leaderboard.leaderboard_page, title="Leaderboard", icon=":material/social_leaderboard:")
pricing_page = st.Page(page=pricing.pricing_page, title="Pricing", icon=":material/paid:")

# Group pages for logged-out users
logged_out_pages = [login_page]

# Group pages for logged-in users
logged_in_pages = {
    "Home": [dashboard_page, accounts_page, leaderboard_page, pricing_page],
    "Settings": [settings_page, logout_page]  # Logout page added here
}

def create_navigation(pages):
    # Create the navigation sidebar
    selected_page = st.navigation(pages, position="sidebar")
    # Run the selected page function
    selected_page.run()

def main():
    # Check if user is already logged in
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # Check if user has logged out and reset if necessary
    if "logged_out" not in st.session_state:
        st.session_state["logged_out"] = False

    # Display pages based on login state
    if st.session_state["logged_in"]:
        st.logo(image="static/analytiq_type_logo.png", size="large", icon_image="static/analytiq_icon.png")

        create_navigation(logged_in_pages)
    else:
        create_navigation(logged_out_pages)

    with bottom():
        social_media_links = [
            "https://x.com/AnalytIQtrade",
            "https://www.instagram.com/analytiq.trade"
        ]

        social_media_icons = SocialMediaIcons(social_media_links, colors=["#ffffff", "#ffffff"])

        social_media_icons.render()

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
