import streamlit as st
from datetime import datetime
from static.elements import tile, gradient_tile


def leaderboard_page():
    st.subheader("Leaderboard", anchor=False)
    st.info("Compete in regular competitions against the AnalytiQ **Leaderboard** for valuable prizes.")
    
    with st.expander("Competition Rules", icon=":material/gavel:"):
        st.markdown("Rules here")
    
    st.markdown("**Active Competitions**")

    col1, col2, col3 = st.columns(3,vertical_alignment="top")
    with col1:
        with tile("competition_countdown", 40, True):
            # Set the target date and time for the countdown
            target_date = datetime(2025, 1, 24, 12, 0, 0)  # Valentine's Day at 12:00 PM
            target_date_js = int(target_date.timestamp() * 1000)  # Convert to milliseconds for JavaScript

            countdown_html = f"""
            <span id="countdown" style="font-size: 20px; font-family: 'Source Sans Pro', sans-serif; color: #E8E8E8;"></span>
            <script>
                const targetDate = new Date({target_date_js});
                function updateCountdown() {{
                    const now = new Date();
                    const delta = targetDate - now;
                    if (delta > 0) {{
                        const days = Math.floor(delta / (1000 * 60 * 60 * 24));
                        const hours = Math.floor((delta % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                        const minutes = Math.floor((delta % (1000 * 60 * 60)) / (1000 * 60));
                        const seconds = Math.floor((delta % (1000 * 60)) / 1000);
                        
                        document.getElementById('countdown').textContent = `${{days.toString().padStart(2, '0')}}:${{hours.toString().padStart(2, '0')}}:${{minutes.toString().padStart(2, '0')}}:${{seconds.toString().padStart(2, '0')}}`;
                    }} else {{
                        document.getElementById('countdown').textContent = "Countdown Complete!";
                    }}
                }}
                setInterval(updateCountdown, 1000);
                updateCountdown();  // Initial call
            </script>
            """

            st.components.v1.html(countdown_html, height=35)
    
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
            st.html(f'''
                        <div style="line-height: 2.55;">
                            <p style="margin: 0; font-size: 1em; font-weight: bold; color: #E8E8E8;">🥈 2nd Place</p>
                            <p style="margin: 0; font-size: 0.9em; color: #878884;">⚡ $500 Cash</p>
                            <p style="margin: 0; font-size: 0.9em; color: #878884;">⚡ 1 Months AnalytiQ Pro</p>
                            <p style="margin: 0; font-size: 0.9em; color: #878884;">⚡ $10k 2-Step Challenge</p>
                        </div>
                        ''')

    with prize_3:
        with tile("prize_3", height=150, border=False):
            st.html(f'''
                        <div style="line-height: 2.55;">
                            <p style="margin: 0; font-size: 1em; font-weight: bold; color: #E8E8E8;">🥉 3rd Place</p>
                            <p style="margin: 0; font-size: 0.9em; color: #878884;">⚡ $250 Cash</p>
                            <p style="margin: 0; font-size: 0.9em; color: #878884;">⚡ 1 Months AnalytiQ Plus</p>
                            <p style="margin: 0; font-size: 0.9em; color: #878884;">⚡ $5k 2-Step Challenge</p>
                        </div>
                        ''')


    tile("leaderboard", height=450, border=False)

if __name__ == "__main__":
    leaderboard_page()