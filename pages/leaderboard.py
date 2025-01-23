import asyncio
import streamlit as st
from datetime import datetime, timedelta
from static.elements import tile, gradient_tile

def run_async_function(async_func, *args, **kwargs):
    """
    Runs an asynchronous function within a properly managed event loop.

    Parameters:
        async_func (Callable): The asynchronous function to run.
        *args: Positional arguments to pass to the async function.
        **kwargs: Keyword arguments to pass to the async function.

    Returns:
        The result of the asynchronous function.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # Create a new event loop if there is none
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Run the async function in the current thread's event loop
    return loop.run_until_complete(async_func(*args, **kwargs))

async def countdown_between_dates(start_date: datetime, end_date: datetime):
    """
    Asynchronous countdown timer between two dates.

    Parameters:
        start_date (datetime): The start of the countdown.
        end_date (datetime): The target end of the countdown.
    """
    while True:
        now = datetime.now()
        if now < start_date:
            st.metric("Countdown", "Not started yet")
        else:
            remaining_time = end_date - now
            if remaining_time.total_seconds() > 0:
                days = remaining_time.days
                hours, remainder = divmod(remaining_time.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                st.metric("Countdown", f"{days} Days, {hours:02d}:{minutes:02d}")
            else:
                st.metric("Countdown", "Time's up!")
                break

        await asyncio.sleep(1)

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
            # Define fixed start and end dates
            start_datetime = datetime(2025, 1, 22, 0, 0)  # 22nd Jan 2025 at midnight
            end_datetime = datetime(2025, 1, 29, 0, 0)  # 29th Jan 2025 at midnight

            run_async_function(countdown_between_dates, start_datetime, end_datetime)
    
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