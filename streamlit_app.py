import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="FF Simulator", page_icon="🏈")

# ── Player Pool ───────────────────────────────────────────────────────────────
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

SCORE_MIN  = 88.0
SCORE_MAX  = 128.0
SCORE_STD  = 18.0
NUM_TEAMS  = 12
NUM_ROUNDS = 5
TOTAL_PICKS = NUM_TEAMS * NUM_ROUNDS
WEEKS_REG  = 14

# ── Helpers ───────────────────────────────────────────────────────────────────
def generate_schedule(team_names):
    teams = list(team_names)
    n = len(teams)
    fixed, rotating = teams[0], teams[1:]
    rounds = []
    for _ in range(n - 1):
        rt = [fixed] + rotating
        rounds.append([(rt[j], rt[n - 1 - j]) for j in range(n // 2)])
        rotating = [rotating[-1]] + rotating[:-1]
    return [rounds[w % len(rounds)] for w in range(WEEKS_REG)]

def proj_to_mean(proj_sum, all_sums):
    lo, hi = min(all_sums), max(all_sums)
    t = (proj_sum - lo) / (hi - lo) if hi != lo else 0.5
    return SCORE_MIN + t * (SCORE_MAX - SCORE_MIN)

def sim_score(mean):
    return round(max(55.0, min(200.0, random.gauss(mean, SCORE_STD))), 2)

def get_standings(weekly_results, all_teams):
    s = {t: {"W": 0, "L": 0, "PF": 0.0, "PA": 0.0} for t in all_teams}
    for wk in weekly_results:
        for t1, t2, s1, s2 in wk["matchups"]:
            s[t1]["PF"] += s1; s[t1]["PA"] += s2
            s[t2]["PF"] += s2; s[t2]["PA"] += s1
            if s1 > s2:   s[t1]["W"] += 1; s[t2]["L"] += 1
            elif s2 > s1: s[t2]["W"] += 1; s[t1]["L"] += 1
            else:         s[t1]["W"] += 0.5; s[t2]["W"] += 0.5
    rows = [{"Team": t, "Wins": v["W"], "Losses": v["L"],
             "Points For": round(v["PF"], 2), "Points Against": round(v["PA"], 2)}
            for t, v in s.items()]
    return pd.DataFrame(rows).sort_values(["Wins","Points For"], ascending=[False,False]).reset_index(drop=True)

# ── Session state — single `phase` drives everything ─────────────────────────
# Phases: "setup" → "draft" → "week_preview" → "week_results"
#         → (after wk 14) "playoff_wildcard_preview" → "playoff_wildcard_results"
#         → "playoff_semis_preview" → "playoff_semis_results"
#         → "playoff_champ_preview" → "playoff_champ_results"
if "phase" not in st.session_state:
    st.session_state.phase          = "setup"
    st.session_state.rosters        = {}
    st.session_state.drafted        = None
    st.session_state.current_pick   = 0
    st.session_state.your_pick_pos  = 1
    st.session_state.your_team      = "@Tailwind40"
    st.session_state.team_strengths = {}
    st.session_state.schedule       = []
    st.session_state.current_week   = 1
    st.session_state.weekly_results = []   # list of {week, matchups: [(t1,t2,s1,s2)]}
    st.session_state.week_results   = []   # results for the just-simulated week
    st.session_state.playoff_seeds  = []
    st.session_state.playoff_wc     = []   # wildcard results
    st.session_state.playoff_semis  = []
    st.session_state.playoff_champ  = None

ss = st.session_state

# draft_order helper
def get_draft_order():
    order = []
    for r in range(NUM_ROUNDS):
        order.extend(range(1, NUM_TEAMS+1) if r % 2 == 0 else range(NUM_TEAMS, 0, -1))
    return order

# ══════════════════════════════════════════════════════════════
# PHASE: SETUP
# ══════════════════════════════════════════════════════════════
if ss.phase == "setup":
    st.title("FF Simulator 🏈")
    st.markdown("12-Team Snake Draft + Full Season + Playoffs. Built by @Tailwind40")

    ss.your_team = st.text_input("Your team name", value=ss.your_team)
    ss.your_pick_pos = st.selectbox("Your draft position (1–12)", list(range(1, 13)))

    if st.button("🏈 Start Draft"):
        ss.rosters = {f"Team {i+1}": [] for i in range(NUM_TEAMS)}
        ss.rosters[ss.your_team] = []
        ss.drafted = players_df.copy()
        ss.current_pick = 0
        ss.weekly_results = []
        ss.current_week = 1
        ss.phase = "draft"
        st.rerun()

# ══════════════════════════════════════════════════════════════
# PHASE: DRAFT
# ══════════════════════════════════════════════════════════════
elif ss.phase == "draft":
    st.title("🗒️ Snake Draft — 5 Rounds")

    draft_order = get_draft_order()

    # If draft is finished, compute strengths + schedule and move on
    if ss.current_pick >= TOTAL_PICKS:
        all_teams = list(ss.rosters.keys())
        proj_sums = {
            t: players_df[players_df["player"].isin(r)]["proj"].sum()
            for t, r in ss.rosters.items()
        }
        all_sums = list(proj_sums.values())
        ss.team_strengths = {t: proj_to_mean(v, all_sums) for t, v in proj_sums.items()}
        ss.schedule = generate_schedule(all_teams)
        ss.current_week = 1
        ss.phase = "week_preview"
        st.rerun()

    curr_num  = draft_order[ss.current_pick]
    is_yours  = curr_num == ss.your_pick_pos
    curr_name = ss.your_team if is_yours else f"Team {curr_num}"

    st.write(f"**Pick {ss.current_pick + 1} / {TOTAL_PICKS}** | Round {ss.current_pick // NUM_TEAMS + 1}")
    st.write(f"**On the clock:** {curr_name} {'👈 (You)' if is_yours else '(CPU)'}")

    st.dataframe(ss.drafted[["player","pos","proj"]].head(15), use_container_width=True, hide_index=True)

    def cpu_pick(team_name):
        best = ss.drafted.iloc[0]
        ss.rosters[team_name].append(best["player"])
        ss.drafted = ss.drafted.iloc[1:]
        ss.current_pick += 1

    if is_yours:
        sel = st.selectbox("Your pick:", ss.drafted["player"].tolist(), index=None, placeholder="Choose a player...")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Confirm Pick") and sel:
                ss.rosters[ss.your_team].append(sel)
                ss.drafted = ss.drafted[ss.drafted["player"] != sel]
                ss.current_pick += 1
                st.rerun()
        with c2:
            if st.button("⚡ Auto-Pick Best"):
                cpu_pick(ss.your_team)
                st.rerun()
    else:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("▶️ CPU Picks Once"):
                cpu_pick(curr_name)
                st.rerun()
        with c2:
            if st.button("⏩ Skip to My Next Pick"):
                while ss.current_pick < TOTAL_PICKS:
                    cn = draft_order[ss.current_pick]
                    if cn == ss.your_pick_pos:
                        break
                    nm = ss.your_team if cn == ss.your_pick_pos else f"Team {cn}"
                    cpu_pick(nm)
                st.rerun()

    if st.button("⏭️ Auto-Complete Entire Draft"):
        while ss.current_pick < TOTAL_PICKS:
            cn   = draft_order[ss.current_pick]
            nm   = ss.your_team if cn == ss.your_pick_pos else f"Team {cn}"
            cpu_pick(nm)
        st.rerun()

    if ss.rosters.get(ss.your_team):
        with st.expander("Your roster so far"):
            st.dataframe(pd.DataFrame({"Player": ss.rosters[ss.your_team]}), hide_index=True)

# ══════════════════════════════════════════════════════════════
# PHASE: WEEK PREVIEW  (show matchups, wait for simulate click)
# ══════════════════════════════════════════════════════════════
elif ss.phase == "week_preview":
    wk       = ss.current_week
    matchups = ss.schedule[wk - 1]
    all_teams = list(ss.rosters.keys())

    st.title(f"📅 Week {wk} of {WEEKS_REG}")

    # Your matchup callout
    your_game = next(((t1,t2) for t1,t2 in matchups if ss.your_team in (t1,t2)), None)
    if your_game:
        opp = your_game[1] if your_game[0] == ss.your_team else your_game[0]
        st.info(f"**Your matchup:** {ss.your_team} vs **{opp}**")

    st.markdown("**This week's matchups:**")
    for t1, t2 in matchups:
        tag = "  👈 your game" if ss.your_team in (t1, t2) else ""
        st.write(f"• {t1} vs {t2}{tag}")

    # Standings expander
    if ss.weekly_results:
        with st.expander("📊 Current standings"):
            st.dataframe(get_standings(ss.weekly_results, all_teams), use_container_width=True, hide_index=True)

    st.divider()
    if st.button(f"🏈 Simulate Week {wk}", type="primary"):
        results = [(t1, t2, sim_score(ss.team_strengths[t1]), sim_score(ss.team_strengths[t2]))
                   for t1, t2 in matchups]
        ss.weekly_results.append({"week": wk, "matchups": results})
        ss.week_results = results
        ss.phase = "week_results"
        st.rerun()

# ══════════════════════════════════════════════════════════════
# PHASE: WEEK RESULTS  (show scores, then advance)
# ══════════════════════════════════════════════════════════════
elif ss.phase == "week_results":
    wk        = ss.current_week
    results   = ss.week_results
    all_teams = list(ss.rosters.keys())

    st.title(f"📋 Week {wk} Results")

    for t1, t2, s1, s2 in results:
        winner   = t1 if s1 > s2 else (t2 if s2 > s1 else "Tie")
        is_yours = ss.your_team in (t1, t2)
        prefix   = "🏈 " if is_yours else ""
        st.write(f"{prefix}**{t1}** {s1} – {s2} **{t2}**  →  Winner: **{winner}**")

    # Highlighted result for user
    your_result = next((r for r in results if ss.your_team in (r[0], r[1])), None)
    if your_result:
        t1, t2, s1, s2 = your_result
        ys = s1 if t1 == ss.your_team else s2
        os = s2 if t1 == ss.your_team else s1
        on = t2 if t1 == ss.your_team else t1
        st.divider()
        if ys > os:
            st.success(f"✅ You won!  {ss.your_team} **{ys}** – **{os}** {on}")
        elif ys < os:
            st.error(f"❌ You lost.  {ss.your_team} **{ys}** – **{os}** {on}")
        else:
            st.warning(f"🤝 Tie.  {ys} – {os}")

    with st.expander("📊 Standings after Week {wk}"):
        st.dataframe(get_standings(ss.weekly_results, all_teams), use_container_width=True, hide_index=True)

    st.divider()
    if wk < WEEKS_REG:
        if st.button(f"➡️ Go to Week {wk + 1}", type="primary"):
            ss.current_week += 1
            ss.phase = "week_preview"
            st.rerun()
    else:
        st.success("🎉 Regular season complete! Time for the playoffs.")
        if st.button("🏆 Begin Playoffs", type="primary"):
            final = get_standings(ss.weekly_results, all_teams)
            ss.playoff_seeds = final.head(6)["Team"].tolist()
            ss.phase = "playoff_wildcard_preview"
            st.rerun()

# ══════════════════════════════════════════════════════════════
# PHASE: PLAYOFF WILD CARD PREVIEW
# ══════════════════════════════════════════════════════════════
elif ss.phase == "playoff_wildcard_preview":
    seeds = ss.playoff_seeds
    st.title("🏆 Playoffs — Week 15: Wild Card")
    st.markdown("**Seeds 1 & 2 have byes.**")
    st.write(f"• (3) **{seeds[2]}** vs (6) **{seeds[5]}**")
    st.write(f"• (4) **{seeds[3]}** vs (5) **{seeds[4]}**")

    your_in = ss.your_team in seeds[:6]
    your_bye = ss.your_team in seeds[:2]
    if your_bye:
        st.info(f"You ({ss.your_team}) have a bye this week! 🎉")
    elif your_in:
        opp_idx = {2:5, 3:4, 4:3, 5:2}.get(seeds.index(ss.your_team))
        st.info(f"**Your matchup:** {ss.your_team} vs {seeds[opp_idx]}")
    else:
        st.warning(f"{ss.your_team} did not make the playoffs.")

    if st.button("🏈 Simulate Wild Card", type="primary"):
        r1_w, r1_s1, r1_s2 = (seeds[2], *[sim_score(ss.team_strengths[seeds[2]]), sim_score(ss.team_strengths[seeds[5]])])
        r1_w = seeds[2] if r1_s1 >= r1_s2 else seeds[5]
        r2_w, r2_s1, r2_s2 = (seeds[3], *[sim_score(ss.team_strengths[seeds[3]]), sim_score(ss.team_strengths[seeds[4]])])
        r2_w = seeds[3] if r2_s1 >= r2_s2 else seeds[4]
        ss.playoff_wc = [
            (seeds[2], seeds[5], r1_s1, r1_s2, r1_w),
            (seeds[3], seeds[4], r2_s1, r2_s2, r2_w),
        ]
        ss.phase = "playoff_wildcard_results"
        st.rerun()

# ══════════════════════════════════════════════════════════════
# PHASE: PLAYOFF WILD CARD RESULTS
# ══════════════════════════════════════════════════════════════
elif ss.phase == "playoff_wildcard_results":
    st.title("📋 Wild Card Results")
    for t1, t2, s1, s2, w in ss.playoff_wc:
        is_yours = ss.your_team in (t1, t2)
        st.write(f"{'🏈 ' if is_yours else ''}**{t1}** {s1} – {s2} **{t2}**  →  **{w} advances**")

    your_wc = next((r for r in ss.playoff_wc if ss.your_team in (r[0], r[1])), None)
    if your_wc:
        st.divider()
        if your_wc[4] == ss.your_team:
            st.success(f"✅ You advance to the Semifinals!")
        else:
            st.error(f"❌ Your season is over. Better luck next year.")

    if st.button("➡️ Advance to Semifinals", type="primary"):
        ss.phase = "playoff_semis_preview"
        st.rerun()

# ══════════════════════════════════════════════════════════════
# PHASE: PLAYOFF SEMIS PREVIEW
# ══════════════════════════════════════════════════════════════
elif ss.phase == "playoff_semis_preview":
    seeds    = ss.playoff_seeds
    wc_wins  = [r[4] for r in ss.playoff_wc]
    matchups = [(seeds[0], wc_wins[1]), (seeds[1], wc_wins[0])]

    st.title("🏆 Playoffs — Week 16: Semifinals")
    for t1, t2 in matchups:
        tag = "  👈 your game" if ss.your_team in (t1, t2) else ""
        st.write(f"• **{t1}** vs **{t2}**{tag}")

    if st.button("🏈 Simulate Semifinals", type="primary"):
        results = []
        for t1, t2 in matchups:
            s1 = sim_score(ss.team_strengths[t1])
            s2 = sim_score(ss.team_strengths[t2])
            w  = t1 if s1 >= s2 else t2
            results.append((t1, t2, s1, s2, w))
        ss.playoff_semis = results
        ss.phase = "playoff_semis_results"
        st.rerun()

# ══════════════════════════════════════════════════════════════
# PHASE: PLAYOFF SEMIS RESULTS
# ══════════════════════════════════════════════════════════════
elif ss.phase == "playoff_semis_results":
    st.title("📋 Semifinals Results")
    for t1, t2, s1, s2, w in ss.playoff_semis:
        is_yours = ss.your_team in (t1, t2)
        st.write(f"{'🏈 ' if is_yours else ''}**{t1}** {s1} – {s2} **{t2}**  →  **{w} advances**")

    your_semi = next((r for r in ss.playoff_semis if ss.your_team in (r[0], r[1])), None)
    if your_semi:
        st.divider()
        if your_semi[4] == ss.your_team:
            st.success("✅ You're in the Championship! 🏆")
        else:
            st.error("❌ You lost in the Semis. So close!")

    if st.button("➡️ Advance to Championship", type="primary"):
        ss.phase = "playoff_champ_preview"
        st.rerun()

# ══════════════════════════════════════════════════════════════
# PHASE: CHAMPIONSHIP PREVIEW
# ══════════════════════════════════════════════════════════════
elif ss.phase == "playoff_champ_preview":
    finalists = [r[4] for r in ss.playoff_semis]
    st.title("🏆 Playoffs — Week 17: Championship")
    st.markdown(f"### {finalists[0]} vs {finalists[1]}")
    if ss.your_team in finalists:
        opp = finalists[1] if finalists[0] == ss.your_team else finalists[0]
        st.info(f"**You're in the Championship!** {ss.your_team} vs {opp}")

    if st.button("🏈 Simulate Championship", type="primary"):
        t1, t2 = finalists
        s1 = sim_score(ss.team_strengths[t1])
        s2 = sim_score(ss.team_strengths[t2])
        w  = t1 if s1 >= s2 else t2
        ss.playoff_champ = (t1, t2, s1, s2, w)
        ss.phase = "playoff_champ_results"
        st.rerun()

# ══════════════════════════════════════════════════════════════
# PHASE: CHAMPIONSHIP RESULTS
# ══════════════════════════════════════════════════════════════
elif ss.phase == "playoff_champ_results":
    t1, t2, s1, s2, champ = ss.playoff_champ
    all_teams = list(ss.rosters.keys())

    st.title("🏆 Championship Result")
    st.markdown(f"## {t1}  {s1}  –  {s2}  {t2}")
    st.markdown(f"# 🎉 {champ} wins the Championship!")

    if champ == ss.your_team:
        st.balloons()
        st.success("🥳 That's YOU! Congratulations, Champion!")
    else:
        if ss.your_team in (t1, t2):
            st.error("So close — runner-up is still something to be proud of.")

    st.divider()
    st.subheader("📊 Final Regular Season Standings")
    st.dataframe(get_standings(ss.weekly_results, all_teams), use_container_width=True, hide_index=True)

    if st.button("🔄 Start New Season"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
