import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="FF Simulator", page_icon="🏈")

st.title("FF Simulator 🏈")
st.markdown("Simulate thousands of seasons and see your playoff odds! Built by @Tailwind40")

st.write("Draft players to build your team, then simulate your playoff chances.")

# Simple player pool (early 2026 consensus projections - total season fantasy points, approx PPR)
# Expand this list as much as you want later
player_data = [
    {"player": "Bijan Robinson", "pos": "RB", "proj_points": 380},
    {"player": "Christian McCaffrey", "pos": "RB", "proj_points": 370},
    {"player": "Ja'Marr Chase", "pos": "WR", "proj_points": 360},
    {"player": "CeeDee Lamb", "pos": "WR", "proj_points": 355},
    {"player": "Justin Jefferson", "pos": "WR", "proj_points": 350},
    {"player": "Josh Allen", "pos": "QB", "proj_points": 420},
    {"player": "Lamar Jackson", "pos": "QB", "proj_points": 410},
    {"player": "Jalen Hurts", "pos": "QB", "proj_points": 400},
    {"player": "Saquon Barkley", "pos": "RB", "proj_points": 360},
    {"player": "Amon-Ra St. Brown", "pos": "WR", "proj_points": 340},
    {"player": "Puka Nacua", "pos": "WR", "proj_points": 330},
    {"player": "Tyreek Hill", "pos": "WR", "proj_points": 325},
    {"player": "Travis Kelce", "pos": "TE", "proj_points": 280},
    {"player": "Sam LaPorta", "pos": "TE", "proj_points": 270},
    # ← Add more players here when you want (50–100 is ideal)
]

players_df = pd.DataFrame(player_data)

# Draft interface
available_players = players_df["player"].tolist()
drafted = st.multiselect(
    "Draft players (search and select as many as you want)",
    available_players,
    default=[],
    placeholder="Start typing player names..."
)

if drafted:
    drafted_df = players_df[players_df["player"].isin(drafted)]
    total_proj = drafted_df["proj_points"].sum()
    num_drafted = len(drafted)

    # Estimate team strength from total projected points
    # This is a rough mapping — you can tune the formula later
    team_strength = 6.0 + (total_proj / 400.0)
    team_strength = min(13.0, max(6.0, team_strength))

    st.subheader("Your Drafted Team")
    st.dataframe(
        drafted_df[["player", "pos", "proj_points"]]
        .sort_values("proj_points", ascending=False)
        .reset_index(drop=True)
    )

    st.markdown(f"**Total projected points:** {total_proj:.0f}")
    st.markdown(f"**Estimated team strength:** {team_strength:.1f}")

    # Simulation settings
    team_name = st.text_input("Your team name", "@Tailwind40")
    num_seasons = st.slider("Number of seasons to simulate", 100, 20000, 5000, step=100)
    playoff_threshold = st.number_input("Wins needed to make playoffs", 8, 12, 10)

    if st.button("Simulate My Team!", type="primary"):
        with st.spinner("Simulating seasons..."):
            playoff_count = 0
            total_wins = 0
            for _ in range(num_seasons):
                wins = round(random.gauss(team_strength, 1.8))
                wins = max(4, min(14, wins))
                total_wins += wins
                if wins >= playoff_threshold:
                    playoff_count += 1
            avg_wins = total_wins / num_seasons
            playoff_percent = (playoff_count / num_seasons) * 100

        st.success("Simulation complete!")
        
        st.subheader("Results")
        st.markdown(f"**Team:** {team_name}")
        st.markdown(f"**Average wins per season:** {avg_wins:.1f}")
        st.markdown(f"**Playoff probability:** **{playoff_percent:.1f}%**")
        
        st.progress(playoff_percent / 100)
        st.caption(f"{playoff_percent:.1f}% chance → {'Very likely!' if playoff_percent > 70 else 'Solid shot!' if playoff_percent > 50 else 'Grind time.'}")
        
        st.balloons()
else:
    st.info("Select some players above to build your team and run the simulation!")
