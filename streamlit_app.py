import streamlit as st
import random
import pandas as pd
import numpy as np

st.set_page_config(page_title="FF Simulator", page_icon="🏈")

st.title("FF Simulator 🏈")
st.markdown("12-Team Snake Draft + Full Season + Playoffs. Built by @Tailwind40")

# Player pool - 60 players
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
    {"player": "Brock Bowers", "pos": "TE", "proj": 265},
    {"player": "Malik Nabers", "pos": "WR", "proj": 315},
    {"player": "Kyren Williams", "pos": "RB", "proj": 310},
    {"player": "Nico Collins", "pos": "WR", "proj": 305},
    {"player": "Drake London", "pos": "WR", "proj": 300},
    {"player": "Garrett Wilson", "pos": "WR", "proj": 295},
    {"player": "Deebo Samuel", "pos": "WR", "proj": 290},
    {"player": "Chris Olave", "pos": "WR", "proj": 285},
    {"player": "Davante Adams", "pos": "WR", "proj": 280},
    {"player": "DJ Moore", "pos": "WR", "proj": 275},
    {"player": "Jaylen Waddle", "pos": "WR", "proj": 270},
    {"player": "Zay Flowers", "pos": "WR", "proj": 265},
    {"player": "DeVonta Smith", "pos": "WR", "proj": 260},
    {"player": "James Cook", "pos": "RB", "proj": 255},
    {"player": "Kenneth Walker III", "pos": "RB", "proj": 250},
    {"player": "Derrick Henry", "pos": "RB", "proj": 245},
    {"player": "Josh Jacobs", "pos": "RB", "proj": 240},
    {"player": "Breece Hall", "pos": "RB", "proj": 235},
    {"player": "Kyler Murray", "pos": "QB", "proj": 390},
    {"player": "C.J. Stroud", "pos": "QB", "proj": 380},
    {"player": "Joe Burrow", "pos": "QB", "proj": 375},
    {"player": "Patrick Mahomes", "pos": "QB", "proj": 370},
    {"player": "Jayden Daniels", "pos": "QB", "proj": 365},
    {"player": "Baker Mayfield", "pos": "QB", "proj": 350},
    {"player": "Trey McBride", "pos": "TE", "proj": 255},
    {"player": "Mark Andrews", "pos": "TE", "proj": 250},
    {"player": "George Kittle", "pos": "TE", "proj": 245},
    {"player": "Dalton Kincaid", "pos": "TE", "proj": 240},
    {"player": "Kyle Pitts", "pos": "TE", "proj": 235},
    {"player": "David Njoku", "pos": "TE", "proj": 230},
    {"player": "Evan Engram", "pos": "TE", "proj": 225},
    {"player": "T.J. Hockenson", "pos": "TE", "proj": 220},
    {"player": "A.J. Brown", "pos": "WR", "proj": 315},
    {"player": "Marvin Harrison Jr.", "pos": "WR", "proj": 310},
    {"player": "Cooper Kupp", "pos": "WR", "proj": 305},
    {"player": "Mike Evans", "pos": "WR", "proj": 300},
    {"player": "DK Metcalf", "pos": "WR", "proj": 295},
    {"player": "Rashee Rice", "pos": "WR", "proj": 290},
    {"player": "Brian Thomas Jr.", "pos": "WR", "proj": 285},
    {"player": "Rome Odunze", "pos": "WR", "proj": 280},
    {"player": "Xavier Worthy", "pos": "WR", "proj": 275},
    {"player": "Ladd McConkey", "pos": "WR", "proj": 270},
    {"player": "Tetairoa McMillan", "pos": "WR", "proj": 265},
]

players_df = pd.DataFrame(player_data).sort_values("proj", ascending=False).reset_index(drop=True)

# ─────────────────────────────────────────────────────────
# FIX 1: Balanced round-robin schedule
# Uses the polygon/circle method — every team plays exactly
# once per week, and no pair appears more than twice across
# 14 weeks (11-round RR, then weeks 12-14 reuse rounds 1-3).
# ─────────────────────────────────────────────────────────
def generate_schedule(team_names, num_weeks=14):
    teams = list(team_names)
    n = len(teams)

    # Polygon/circle method for even n
    fixed = teams[0]
    rotating = teams[1:]
    rounds = []

    for i in range(n - 1):  # 11 rounds for 12 teams
        round_teams = [fixed] + rotating
        pairs = []
        for j in range(n // 2):
            t1 = round_teams[j]
            t2 = round_teams[n - 1 - j]
            pairs.append((t1, t2))
        rounds.append(pairs)
        rotating = [rotating[-1]] + rotating[:-1]  # rotate right

    # Fill 14 weeks by cycling (weeks 12-14 reuse rounds 1-3)
    schedule = [rounds[w % len(rounds)] for w in range(num_weeks)]
    return schedule


# ─────────────────────────────────────────────────────────
# FIX 2: Realistic fantasy point scoring
# Instead of a 6–20 integer, we simulate actual weekly
# fantasy totals. A "good" team averages ~120 pts/week;
# a weaker one ~90. Std dev of ~18 mirrors real variance.
#
# Team strength (proj sum) maps linearly into a weekly
# mean score between 88 (weakest) and 128 (strongest).
# ─────────────────────────────────────────────────────────
SCORE_MIN = 88.0    # worst realistic weekly total
SCORE_MAX = 128.0   # best realistic weekly total
SCORE_STD = 18.0    # realistic week-to-week variance

def proj_to_weekly_mean(proj_sum, all_proj_sums):
    lo, hi = min(all_proj_sums), max(all_proj_sums)
    if hi == lo:
        return (SCORE_MIN + SCORE_MAX) / 2
    t = (proj_sum - lo) / (hi - lo)
    return SCORE_MIN + t * (SCORE_MAX - SCORE_MIN)

def simulate_score(mean):
    raw = random.gauss(mean, SCORE_STD)
    return round(max(55.0, min(200.0, raw)), 2)


# ─────────────────────────────────────────────────────────
# Session state
# ─────────────────────────────────────────────────────────
if 'draft_started' not in st.session_state:
    st.session_state.draft_started = False
    st.session_state.drafted_players = None
    st.session_state.rosters = {}
    st.session_state.current_pick = 0
    st.session_state.your_pick = None
    st.session_state.your_team_name = "@Tailwind40"
    st.session_state.schedule = None
    st.session_state.standings = None
    st.session_state.team_strengths = None

your_team_name = st.text_input("Your team name", value=st.session_state.your_team_name)
st.session_state.your_team_name = your_team_name

your_draft_position = st.selectbox("Your draft position (1-12)", options=list(range(1, 13)))

num_rounds = 5
num_teams = 12
total_picks = num_rounds * num_teams
weeks_regular = 14

if not st.session_state.draft_started:
    if st.button("Start Draft"):
        st.session_state.draft_started = True
        st.session_state.drafted_players = players_df.copy()
        st.session_state.rosters = {f"Team {i+1}": [] for i in range(12)}
        st.session_state.rosters[your_team_name] = []
        st.session_state.current_pick = 0
        st.session_state.your_pick = your_draft_position
        st.session_state.schedule = None
        st.session_state.standings = None
        st.session_state.team_strengths = None
        st.rerun()

if st.session_state.draft_started:
    draft_order = []
    for r in range(num_rounds):
        if r % 2 == 0:
            draft_order.extend(range(1, num_teams + 1))
        else:
            draft_order.extend(range(num_teams, 0, -1))

    if st.session_state.current_pick >= total_picks:
        st.success("Draft Complete!")

        all_teams = list(st.session_state.rosters.keys())

        # Build team strengths mapped to realistic weekly means
        if st.session_state.team_strengths is None:
            proj_sums = {}
            for team, roster in st.session_state.rosters.items():
                team_players = players_df[players_df["player"].isin(roster)]
                proj_sums[team] = team_players["proj"].sum()

            all_sums = list(proj_sums.values())
            team_strengths = {
                team: proj_to_weekly_mean(psum, all_sums)
                for team, psum in proj_sums.items()
            }
            st.session_state.team_strengths = team_strengths

        # Generate balanced schedule once
        if st.session_state.schedule is None:
            st.session_state.schedule = generate_schedule(all_teams, weeks_regular)

        # Simulate regular season once
        if st.session_state.standings is None:
            with st.spinner("Simulating full regular season..."):
                standings = pd.DataFrame({
                    'Team': all_teams,
                    'Wins': 0,
                    'Losses': 0,
                    'Points For': 0.0,
                    'Points Against': 0.0
                }).set_index('Team')

                weekly_results = []

                for week_num, matchups in enumerate(st.session_state.schedule, 1):
                    week_scores = {}
                    for t1, t2 in matchups:
                        s1 = simulate_score(st.session_state.team_strengths[t1])
                        s2 = simulate_score(st.session_state.team_strengths[t2])

                        week_scores[t1] = s1
                        week_scores[t2] = s2

                        standings.loc[t1, 'Points For'] += s1
                        standings.loc[t1, 'Points Against'] += s2
                        standings.loc[t2, 'Points For'] += s2
                        standings.loc[t2, 'Points Against'] += s1

                        if s1 > s2:
                            standings.loc[t1, 'Wins'] += 1
                            standings.loc[t2, 'Losses'] += 1
                        elif s2 > s1:
                            standings.loc[t2, 'Wins'] += 1
                            standings.loc[t1, 'Losses'] += 1
                        else:
                            standings.loc[t1, 'Wins'] += 0.5
                            standings.loc[t2, 'Wins'] += 0.5

                    weekly_results.append({
                        'Week': week_num,
                        'Matchups': [(t1, t2, week_scores[t1], week_scores[t2]) for t1, t2 in matchups]
                    })

                standings['Points For'] = standings['Points For'].round(2)
                standings['Points Against'] = standings['Points Against'].round(2)
                standings = standings.sort_values(
                    ['Wins', 'Points For'], ascending=[False, False]
                ).reset_index()

                st.session_state.standings = standings
                st.session_state.weekly_results = weekly_results

        # Display regular season standings
        st.subheader("Regular Season Standings (Weeks 1–14)")
        st.dataframe(
            st.session_state.standings.style.highlight_max(subset=['Wins'], color='#90EE90'),
            use_container_width=True
        )

        with st.expander("View Weekly Matchups & Scores"):
            for week in st.session_state.weekly_results:
                st.markdown(f"**Week {week['Week']}**")
                for t1, t2, s1, s2 in week['Matchups']:
                    winner = t1 if s1 > s2 else t2 if s2 > s1 else "Tie"
                    st.write(f"{t1} **{s1}** – **{s2}** {t2}  →  Winner: **{winner}**")

        # Playoffs
        playoff_teams = st.session_state.standings.head(6)['Team'].tolist()
        st.subheader("Playoffs (Top 6 Teams)")
        st.write("Seeds 1 & 2 get byes | 3 vs 6, 4 vs 5 (Week 15) | Semis (Week 16) | Championship (Week 17)")

        if st.button("Simulate Playoffs"):
            with st.spinner("Simulating playoffs..."):
                def playoff_game(t1, t2):
                    s1 = simulate_score(st.session_state.team_strengths[t1])
                    s2 = simulate_score(st.session_state.team_strengths[t2])
                    winner = t1 if s1 >= s2 else t2
                    return winner, s1, s2

                # Week 15 — Wild Card
                w15_results = []
                for matchup in [(playoff_teams[2], playoff_teams[5]), (playoff_teams[3], playoff_teams[4])]:
                    winner, s1, s2 = playoff_game(*matchup)
                    w15_results.append((matchup[0], matchup[1], s1, s2, winner))

                st.markdown("**Week 15 – Wild Card**")
                for t1, t2, s1, s2, w in w15_results:
                    st.write(f"{t1} **{s1}** – **{s2}** {t2}  →  **{w} advances**")

                winners_15 = [r[4] for r in w15_results]

                # Week 16 — Semifinals
                w16_results = []
                for matchup in [(playoff_teams[0], winners_15[1]), (playoff_teams[1], winners_15[0])]:
                    winner, s1, s2 = playoff_game(*matchup)
                    w16_results.append((matchup[0], matchup[1], s1, s2, winner))

                st.markdown("**Week 16 – Semifinals**")
                for t1, t2, s1, s2, w in w16_results:
                    st.write(f"{t1} **{s1}** – **{s2}** {t2}  →  **{w} advances**")

                finalists = [r[4] for r in w16_results]

                # Week 17 — Championship
                champion, cs1, cs2 = playoff_game(finalists[0], finalists[1])
                st.markdown("**Week 17 – Championship**")
                st.write(f"{finalists[0]} **{cs1}** – **{cs2}** {finalists[1]}")

            st.success(f"🏆 Champion: **{champion}**")
            st.balloons()

    else:
        # ── Draft Phase ──────────────────────────────────────────
        draft_order = []
        for r in range(num_rounds):
            if r % 2 == 0:
                draft_order.extend(range(1, num_teams + 1))
            else:
                draft_order.extend(range(num_teams, 0, -1))

        current_team_num = draft_order[st.session_state.current_pick]
        current_team_name = (
            your_team_name
            if current_team_num == st.session_state.your_pick
            else f"Team {current_team_num}"
        )

        st.subheader("Snake Draft in Progress (5 Rounds)")
        st.write(
            f"**Pick {st.session_state.current_pick + 1} / {total_picks}** "
            f"| Round {(st.session_state.current_pick // num_teams) + 1}"
        )
        st.write(
            f"**On the clock:** {current_team_name} "
            f"{'(You)' if current_team_num == st.session_state.your_pick else '(CPU)'}"
        )

        st.dataframe(
            st.session_state.drafted_players[["player", "pos", "proj"]].head(15),
            use_container_width=True,
            hide_index=True
        )

        if current_team_num == st.session_state.your_pick:
            available_names = st.session_state.drafted_players["player"].tolist()
            your_selection = st.selectbox(
                "Your pick:", available_names, index=None, placeholder="Choose a player..."
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Confirm Pick") and your_selection:
                    picked_row = st.session_state.drafted_players[
                        st.session_state.drafted_players["player"] == your_selection
                    ].iloc[0]
                    st.session_state.rosters[your_team_name].append(picked_row["player"])
                    st.session_state.drafted_players = st.session_state.drafted_players[
                        st.session_state.drafted_players["player"] != your_selection
                    ]
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
                            break
                        curr_name = (
                            your_team_name
                            if curr_num == st.session_state.your_pick
                            else f"Team {curr_num}"
                        )
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

        if your_team_name in st.session_state.rosters and st.session_state.rosters[your_team_name]:
            st.subheader("Your Roster")
            st.dataframe(pd.DataFrame({"Player": st.session_state.rosters[your_team_name]}))

        if st.button("Auto-Complete Entire Draft"):
            while st.session_state.current_pick < total_picks:
                curr_num = draft_order[st.session_state.current_pick]
                curr_name = (
                    your_team_name
                    if curr_num == st.session_state.your_pick
                    else f"Team {curr_num}"
                )
                if not st.session_state.drafted_players.empty:
                    best = st.session_state.drafted_players.iloc[0]
                    st.session_state.rosters[curr_name].append(best["player"])
                    st.session_state.drafted_players = st.session_state.drafted_players.iloc[1:]
                st.session_state.current_pick += 1
            st.rerun()
