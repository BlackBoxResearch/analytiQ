import streamlit as st
from datetime import datetime
from static.elements import tile, gradient_tile


def leaderboard_page():
    st.subheader("Leaderboard", anchor=False)
    st.info("Compete in regular competitions against the AnalytiQ **Leaderboard** for valuable prizes.")
    
    with st.expander("Competition Rules", icon=":material/gavel:"):
        st.markdown("Rules here")
    
    active_leaderboards_l, active_leaderboards_r = st.columns(2, vertical_alignment="bottom")
    
    with active_leaderboards_l:
        st.markdown("**Active Competitions**")

    with active_leaderboards_r:
        with tile("competition_countdown", 50, True):
            # Set the target date and time for the countdown
            target_date = datetime(2025, 2, 14, 12, 0, 0)  # Valentine's Day at 12:00 PM
            target_date_js = int(target_date.timestamp() * 1000)  # Convert to milliseconds for JavaScript

            countdown_html = f"""
            <div style="height: 50px; display: flex; align-items: center; justify-content: center; font-size: 20px; font-family: 'Source Sans Pro', sans-serif; color: #E8E8E8; background-color: #171717; border-radius: 5px;">
                <span id="countdown"></span>
            </div>
            <script>
                const targetDate = new Date({target_date_js});
                function updateCountdown() {{
                    const now = new Date();
                    const delta = targetDate - now;
                    if (delta > 0) {{
                        const days = Math.floor(delta / (1000 * 60 * 60 * 24));
                        const hours = Math.floor((delta % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                        const minutes = Math.floor((delta % (1000 * 60 * 60)) / (1000 * 60));
                        document.getElementById('countdown').textContent = `${{days}} Days, ${{hours}} Hours, ${{minutes}} Minutes`;
                    }} else {{
                        document.getElementById('countdown').textContent = "Countdown Complete!";
                    }}
                }}
                setInterval(updateCountdown, 1000);
                updateCountdown();  // Initial call
            </script>
            """

            st.components.v1.html(countdown_html, height=40)
    
    prize_1, prize_2, prize_3 = st.columns(3, vertical_alignment="top")

    with prize_1:
        gradient_tile(
            key="summary_tile_4", 
            content=f"""
                <div style="line-height: 2.55;">
                    <p style="margin: 0; font-size: 1em; font-weight: bold; color: #E8E8E8;">🥇 1st Place</p>
                    <p style="margin: 0; font-size: 0.9em; color: #878884;">⚡ $1,000 Cash</p>
                    <p style="margin: 0; font-size: 0.9em; color: #878884;">⚡ 3 Months AnalytiQ Pro</p>
                    <p style="margin: 0; font-size: 0.9em; color: #878884;">⚡ $25k 2-Step Challenge</p>
                </div>
                """
            )

    with prize_2:
        with tile("prize_2", height=150, border=False):
            st.markdown("🥈 **2nd Place**")
            st.caption("⚡ $500 Cash")
            st.caption("⚡ 1 Month AnalytiQ Pro")
            st.caption("⚡ $10k 2-Step Challenge")

    with prize_3:
        with tile("prize_3", height=150, border=False):
            st.markdown("🥉 **3rd Place**")
            st.caption("⚡ $250 Cash")
            st.caption("⚡ 1 Month AnalytiQ Plus")
            st.caption("⚡ $5k 2-Step Challenge")

    tile("leaderboard", height=450, border=False)

if __name__ == "__main__":
    leaderboard_page()