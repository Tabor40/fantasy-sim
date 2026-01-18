import streamlit as st
import random

st.set_page_config(page_title="Thuggernaut FF Simulator", page_icon="🏈")

st.title("Thuggernaut Fantasy Football Simulator 🏈")
st.markdown("Simulate thousands of seasons and see your playoff odds! Built by @Tailwind40")

st.write("Adjust the sliders below and hit the button to run simulations.")

# User inputs
team_name = st.text_input("Your team name", "@Tailwind40")
team_strength = st.slider(
    "Team strength (higher = better roster)", 
    min_value=6.0, 
    max_value=13.0, 
    value=10.2, 
    step=0.1,
    help="Average team ≈9.0 | Strong contender ≈10.5–11.5 | Elite ≈12+"
)
num_seasons = st.slider(
    "Number of seasons to simulate", 
    min_value=100, 
    max_value=20000, 
    value=5000, 
    step=100
)
playoff_threshold = st.number_input(
    "Wins needed to make playoffs", 
    min_value=8, 
    max_value=12, 
    value=10
)

if st.button("Run Simulations!", type="primary"):
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
