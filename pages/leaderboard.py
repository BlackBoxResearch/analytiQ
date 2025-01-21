import streamlit as st
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
        competition_timeframe_options = ["Week 1", "January", "Quarter 4", "2025"]
        competition_timeframe = st.segmented_control(
            "Competition", competition_timeframe_options, selection_mode="single", label_visibility="hidden"
        )
    
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