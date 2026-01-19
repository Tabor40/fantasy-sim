import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="FF Simulator", page_icon="🏈")

st.title("FF Simulator 🏈")
st.markdown("12-Team Snake Draft (5 Rounds) + Season Simulation. Built by @Tailwind40")

# Player pool (expand as needed with more realistic 2026 projections)
player_data = [
    {"player": "Bijan Robinson", "pos": "RB", "proj": 380},
    {"player": "Jahmyr Gibbs", "pos": "RB", "proj": 370},
    {"player": "Ja'Marr Chase", "pos": "WR", "proj": 360},
    {"player": "Puka Nacua", "pos": "WR", "proj": 355},
    {"player": "CeeDee Lamb", "pos": "WR", "proj": 350},
    {"player": "Josh Allen", "pos": "QB", "proj": 420},
    {"player": "Lamar Jackson", "pos": "QB", "proj": 410},
    {"player": "Jalen Hurts", "pos": "QB", "proj": 400},
    {"player": "Christian McCaffrey", "pos": "RB", "proj": 370},
    {"player": "Saquon Barkley", "pos": "RB", "proj": 360},
    {"player": "Justin Jefferson", "pos": "WR", "proj": 350},
    {"player": "Amon-Ra St. Brown", "pos": "WR", "proj": 340},
    {"player": "Tyreek Hill", "pos": "WR", "proj": 325},
    {"player": "Travis Kelce", "pos": "TE", "proj": 280},
    {"player": "Sam LaPorta", "pos": "TE", "proj": 270},
    {"player": "De'Von Achane", "pos": "RB", "proj": 320},
    {"player": "Jonathan Taylor", "pos": "RB", "proj": 340},
    {"player": "Jaxon Smith-Njigba", "pos": "WR", "proj": 330},
    # ← Add more players here when you want (50–100 is ideal)
]

players_df = pd.DataFrame(player_data).sort_values("proj", ascending=False).reset_index(drop=True)

# Session state initialization
if 'draft_started' not in st.session_state:
    st.session_state.draft_started = False
    st.session_state.drafted_players = None
    st.session_state.rosters = {}
    st.session_state.current_pick = 0
    st.session_state.your_pick = None
    st.session_state.your_team_name = "@Tailwind40"

# Settings (always update your name in session state)
your_team_name = st.text_input("Your team name", value=st.session_state.your_team_name)
st.session_state.your_team_name = your_team_name

your_draft_position = st.selectbox("Your draft position (1-12)", options=list(range(1, 13)))

num_rounds = 5
num_teams = 12
total_picks = num_rounds * num_teams

if not st.session_state.draft_started:
    if st.button("Start Draft"):
        st.session_state.draft_started = True
        st.session_state.drafted_players = players_df.copy()
        # Initialize all rosters, including yours with current name
        st.session_state.rosters = {f"Team {i+1}": [] for i in range(12)}
        st.session_state.rosters[your_team_name] = []
        st.session_state.current_pick = 0
        st.session_state.your_pick = your_draft_position
        st.rerun()

if st.session_state.draft_started:
    st.subheader("Snake Draft in Progress (5 Rounds)")

    # Snake draft order
    draft_order = []
    for r in range(num_rounds):
        if r % 2 == 0:
            draft_order.extend(range(1, num_teams + 1))
        else:
            draft_order.extend(range(num_teams, 0, -1))

    current_team_num = draft_order[st.session_state.current_pick]
    current_team_name = your_team_name if current_team_num == st.session_state.your_pick else f"Team {current_team_num}"

    st.write(f"**Pick {st.session_state.current_pick + 1} / {total_picks}** | Round {(st.session_state.current_pick // num_teams) + 1}")
    st.write(f"**On the clock:** {current_team_name} {'(You)' if current_team_num == st.session_state.your_pick else '(CPU)'}")

    # Show top remaining players
    st.dataframe(
        st.session_state.drafted_players[["player", "pos", "proj"]].head(15),
        use_container_width=True,
        hide_index=True
    )

    # Your turn
    if current_team_num == st.session_state.your_pick:
        available_names = st.session_state.drafted_players["player"].tolist()
        your_selection = st.selectbox("Your pick:", available_names, index=None, placeholder="Choose a player...")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Confirm Pick") and your_selection:
                picked_row = st.session_state.drafted_players[st.session_state.drafted_players["player"] == your_selection].iloc[0]
                st.session_state.rosters[your_team_name].append(picked_row["player"])
                st.session_state.drafted_players = st.session_state.drafted_players[st.session_state.drafted_players["player"] != your_selection]
                st.session_state.current_pick += 1
                st.rerun()
        with col2:
            if st.button("Auto-Pick Best"):
                if not st.session_state.drafted_players.empty:
                    best = st.session_state.drafted_players.iloc[0]
                    st.session_state.rosters[your_team_name].append(best["player"])
                    st.session_state.drafted_players = st.session_state.drafted_players.iloc[1:]
                    st.session_state.current_pick += 1
                    st.rerun()
                else:
                    st.warning("No more players left!")
    else:
        # CPU turn area with the fixed "Auto-Draft Until My Next Pick"
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Advance Draft (CPU picks once)"):
                if not st.session_state.drafted_players.empty:
                    best = st.session_state.drafted_players.iloc[0]
                    st.session_state.rosters[current_team_name].append(best["player"])
                    st.session_state.drafted_players = st.session_state.drafted_players.iloc[1:]
                    st.session_state.current_pick += 1
                    st.rerun()
                else:
                    st.warning("No more players available!")
        with col2:
            if st.button("Auto-Draft Until My Next Pick"):
                advanced = 0
                while st.session_state.current_pick < total_picks:
                    curr_num = draft_order[st.session_state.current_pick]
                    if curr_num == st.session_state.your_pick:
                        break  # Stop BEFORE your turn

                    curr_name = your_team_name if curr_num == st.session_state.your_pick else f"Team {curr_num}"

                    if st.session_state.drafted_players.empty:
                        st.warning("Ran out of players during auto-draft!")
                        break

                    best = st.session_state.drafted_players.iloc[0]
                    st.session_state.rosters[curr_name].append(best["player"])
                    st.session_state.drafted_players = st.session_state.drafted_players.iloc[1:]
                    st.session_state.current_pick += 1
                    advanced += 1

                if advanced > 0:
                    st.info(f"Auto-advanced {advanced} CPU picks.")
                st.rerun()

    # Show your roster progress
    if your_team_name in st.session_state.rosters and st.session_state.rosters[your_team_name]:
        st.subheader("Your Roster")
        st.dataframe(pd.DataFrame({"Player": st.session_state.rosters[your_team_name]}))

    # Full auto-complete
    if st.button("Auto-Complete Entire Draft"):
        while st.session_state.current_pick < total_picks:
            curr_num = draft_order[st.session_state.current_pick]
            curr_name = your_team_name if curr_num == st.session_state.your_pick else f"Team {curr_num}"
            if not st.session_state.drafted_players.empty:
                best = st.session_state.drafted_players.iloc[0]
                st.session_state.rosters[curr_name].append(best["player"])
                st.session_state.drafted_players = st.session_state.drafted_players.iloc[1:]
            st.session_state.current_pick += 1
        st.rerun()

    # Draft finished
    if st.session_state.current_pick >= total_picks:
        st.success("Draft Complete!")
        st.subheader("Your Final Roster")
        st.dataframe(pd.DataFrame({"Player": st.session_state.rosters.get(your_team_name, [])}))

        your_players = players_df[players_df["player"].isin(st.session_state.rosters.get(your_team_name, []))]
        total_proj = your_players["proj"].sum()
        team_strength = 6.0 + (total_proj / (num_rounds * 40.0))
        team_strength = min(13.0, max(6.0, team_strength))

        st.markdown(f"**Estimated team strength:** {team_strength:.1f}")

        num_seasons = st.slider("Seasons to simulate", 100, 20000, 5000, step=100)
        playoff_threshold = st.number_input("Wins needed for playoffs", 8, 12, 10)

        if st.button("Simulate Season!", type="primary"):
            with st.spinner("Running simulations..."):
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
            st.markdown(f"**Team:** {your_team_name}")
            st.markdown(f"**Avg wins:** {avg_wins:.1f}")
            st.markdown(f"**Playoff %:** **{playoff_percent:.1f}%**")
            st.progress(playoff_percent / 100)
            st.caption(f"{playoff_percent:.1f}% → {'Very likely!' if playoff_percent > 70 else 'Solid shot!' if playoff_percent > 50 else 'Grind time.'}")
            st.balloons()
