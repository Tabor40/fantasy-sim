import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="FF Simulator", page_icon="🏈")

st.title("Fantasy Football Simulator 🏈")
st.markdown("Simulate seasons, build/draft a team, and check playoff odds! Built by @Tailwind40")

# Simple player pool (early 2026 consensus projections - total season fantasy points, approx PPR)
# You can expand this list massively later (100+ players) or load from CSV
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
    # Add more! Top 50-100 from FantasyPros consensus for realism
]

players_df = pd.DataFrame(player_data)

tab1, tab2 = st.tabs(["Quick Sim", "Draft & Build Team"])

with tab1:
    st.write("Quick sim on estimated team strength (no drafting needed)")
    team_name = st.text_input("Your team name", "@Tailwind40", key="quick_name")
    team_strength = st.slider(
        "Team strength (higher = better)", 6.0, 13.0, 10.2, step=0.1,
        help="Average ~9.0 | Strong ~10.5–11.5 | Elite ~12+"
    )
    num_seasons = st.slider("Seasons to simulate", 100, 20000, 5000, step=100)
    playoff_threshold = st.number_input("Wins for playoffs", 8, 12, 10)

    if st.button("Run Quick Simulations!", type="primary", key="quick_run"):
        with st.spinner("Simulating..."):
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

        st.success("Done!")
        st.subheader("Results")
        st.markdown(f"**Team:** {team_name}")
        st.markdown(f"**Avg wins:** {avg_wins:.1f}")
        st.markdown(f"**Playoff %:** **{playoff_percent:.1f}%**")
        st.progress(playoff_percent / 100)
        st.caption(f"{playoff_percent:.1f}% → {'Very likely!' if playoff_percent > 70 else 'Solid shot!' if playoff_percent > 50 else 'Grind time.'}")
        st.balloons()

with tab2:
    st.write("Draft players to build your team, then simulate!")
    st.markdown("Pick as many as you want (e.g., 15–20 for a full roster). The app estimates strength from total projected points.")

    # Draft interface
    available_players = players_df["player"].tolist()
    drafted = st.multiselect(
        "Draft players (search/select multiple)",
        available_players,
        default=[],
        placeholder="Start typing player names..."
    )

    if drafted:
        drafted_df = players_df[players_df["player"].isin(drafted)]
        total_proj = drafted_df["proj_points"].sum()
        num_drafted = len(drafted)

        # Rough team strength: scale total proj to ~8–13 range (adjust formula as needed)
        # e.g., assume ~3000–5000 total proj points for a good roster → map to strength
        team_strength_drafted = 6.0 + (total_proj / 400.0)  # tweak divisor for realism
        team_strength_drafted = min(13.0, max(6.0, team_strength_drafted))

        st.subheader("Your Drafted Team")
        st.dataframe(drafted_df[["player", "pos", "proj_points"]].sort_values("proj_points", ascending=False))

        st.markdown(f"**Total projected points:** {total_proj:.0f}")
        st.markdown(f"**Estimated team strength:** {team_strength_drafted:.1f} (based on your picks)")

        # Reuse sim from quick tab, but with drafted strength
        num_seasons_d = st.slider("Seasons to simulate for this team", 100, 20000, 5000, step=100, key="draft_seasons")
        playoff_threshold_d = st.number_input("Wins for playoffs", 8, 12, 10, key="draft_threshold")

        if st.button("Simulate My Drafted Team!", type="primary"):
            with st.spinner("Simulating your custom team..."):
                playoff_count = 0
                total_wins = 0
                for _ in range(num_seasons_d):
                    wins = round(random.gauss(team_strength_drafted, 1.8))
                    wins = max(4, min(14, wins))
                    total_wins += wins
                    if wins >= playoff_threshold_d:
                        playoff_count += 1
                avg_wins = total_wins / num_seasons_d
                playoff_percent = (playoff_count / num_seasons_d) * 100

            st.success("Simulation complete!")
            st.subheader("Results for Your Draft")
            st.markdown(f"**Team:** {team_name}")
            st.markdown(f"**Avg wins:** {avg_wins:.1f}")
            st.markdown(f"**Playoff %:** **{playoff_percent:.1f}%**")
            st.progress(playoff_percent / 100)
            st.caption(f"{playoff_percent:.1f}% → {'Very likely!' if playoff_percent > 70 else 'Solid shot!' if playoff_percent > 50 else 'Grind time.'}")
            st.balloons()
    else:
        st.info("Select players above to start drafting and see your projected strength!")
