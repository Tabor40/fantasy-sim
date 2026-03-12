import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="FF Simulator", page_icon="🏈")

# ── Player Pool (180 players — 15 rounds × 12 teams) ─────────────────────────
player_data = [
    # ── QBs ──────────────────────────────────────────────────────────────────
    {"player": "Josh Allen",               "pos": "QB",  "proj": 420, "team": "BUF", "adp": 33.2},
    {"player": "Lamar Jackson",            "pos": "QB",  "proj": 410, "team": "BAL", "adp": 43.1},
    {"player": "Jalen Hurts",              "pos": "QB",  "proj": 400, "team": "PHI", "adp": 60.4},
    {"player": "Kyler Murray",             "pos": "QB",  "proj": 390, "team": "ARI", "adp": 128.3},
    {"player": "C.J. Stroud",              "pos": "QB",  "proj": 380, "team": "HOU", "adp": 143.2},
    {"player": "Joe Burrow",               "pos": "QB",  "proj": 375, "team": "CIN", "adp": 65.2},
    {"player": "Patrick Mahomes",          "pos": "QB",  "proj": 370, "team": "KC", "adp": 92.3},
    {"player": "Jayden Daniels",           "pos": "QB",  "proj": 365, "team": "WAS", "adp": 55.8},
    {"player": "Baker Mayfield",           "pos": "QB",  "proj": 350, "team": "TB", "adp": 112.4},
    {"player": "Tua Tagovailoa",           "pos": "QB",  "proj": 345, "team": "MIA", "adp": 172.1},
    {"player": "Sam Darnold",              "pos": "QB",  "proj": 338, "team": "MIN", "adp": 151.6},
    {"player": "Jordan Love",              "pos": "QB",  "proj": 332, "team": "GB", "adp": 138.8},
    {"player": "Dak Prescott",             "pos": "QB",  "proj": 325, "team": "DAL", "adp": 84.7},
    {"player": "Trevor Lawrence",          "pos": "QB",  "proj": 318, "team": "JAX", "adp": 97.5},
    {"player": "Matthew Stafford",         "pos": "QB",  "proj": 310, "team": "LAR", "adp": 101.3},
    {"player": "Geno Smith",               "pos": "QB",  "proj": 302, "team": "SEA", "adp": 155.2},
    {"player": "Anthony Richardson",       "pos": "QB",  "proj": 295, "team": "IND", "adp": 182.4},
    {"player": "Justin Fields",            "pos": "QB",  "proj": 285, "team": "PIT", "adp": 178.9},
    {"player": "Derek Carr",               "pos": "QB",  "proj": 275, "team": "NO", "adp": 192.1},
    {"player": "Kirk Cousins",             "pos": "QB",  "proj": 265, "team": "ATL", "adp": 188.6},
    {"player": "Caleb Williams",           "pos": "QB",  "proj": 258, "team": "CHI", "adp": 75.1},
    {"player": "Will Levis",               "pos": "QB",  "proj": 250, "team": "TEN", "adp": 183.7},
    # ── RBs ──────────────────────────────────────────────────────────────────
    {"player": "Bijan Robinson",           "pos": "RB",  "proj": 380, "team": "ATL", "adp": 1.4},
    {"player": "Jahmyr Gibbs",             "pos": "RB",  "proj": 370, "team": "DET", "adp": 2.6},
    {"player": "Christian McCaffrey",      "pos": "RB",  "proj": 370, "team": "SF", "adp": 5.1},
    {"player": "Saquon Barkley",           "pos": "RB",  "proj": 360, "team": "PHI", "adp": 22.3},
    {"player": "Jonathan Taylor",          "pos": "RB",  "proj": 340, "team": "IND", "adp": 8.2},
    {"player": "De'Von Achane",            "pos": "RB",  "proj": 320, "team": "MIA", "adp": 7.4},
    {"player": "Kyren Williams",           "pos": "RB",  "proj": 310, "team": "LAR", "adp": 31.5},
    {"player": "James Cook",               "pos": "RB",  "proj": 255, "team": "BUF", "adp": 9.3},
    {"player": "Kenneth Walker III",       "pos": "RB",  "proj": 250, "team": "SEA", "adp": 50.1},
    {"player": "Derrick Henry",            "pos": "RB",  "proj": 245, "team": "BAL", "adp": 27.4},
    {"player": "Josh Jacobs",              "pos": "RB",  "proj": 240, "team": "GB", "adp": 20.1},
    {"player": "Breece Hall",              "pos": "RB",  "proj": 235, "team": "NYJ", "adp": 38.2},
    {"player": "Rhamondre Stevenson",      "pos": "RB",  "proj": 228, "team": "NE", "adp": 105.6},
    {"player": "Aaron Jones",              "pos": "RB",  "proj": 222, "team": "MIN", "adp": 89.4},
    {"player": "Tony Pollard",             "pos": "RB",  "proj": 215, "team": "TEN", "adp": 95.2},
    {"player": "Joe Mixon",                "pos": "RB",  "proj": 208, "team": "HOU", "adp": 100.3},
    {"player": "Rachaad White",            "pos": "RB",  "proj": 200, "team": "TB", "adp": 125.1},
    {"player": "D'Andre Swift",            "pos": "RB",  "proj": 193, "team": "CHI", "adp": 52.4},
    {"player": "Isiah Pacheco",            "pos": "RB",  "proj": 186, "team": "KC", "adp": 120.7},
    {"player": "Travis Etienne Jr.",       "pos": "RB",  "proj": 180, "team": "JAX", "adp": 35.3},
    {"player": "Zack Moss",                "pos": "RB",  "proj": 173, "team": "CIN", "adp": 160.4},
    {"player": "Javonte Williams",         "pos": "RB",  "proj": 166, "team": "DEN", "adp": 58.1},
    {"player": "Chuba Hubbard",            "pos": "RB",  "proj": 160, "team": "CAR", "adp": 85.2},
    {"player": "Najee Harris",             "pos": "RB",  "proj": 153, "team": "LAC", "adp": 153.8},
    {"player": "Alvin Kamara",             "pos": "RB",  "proj": 147, "team": "NO", "adp": 82.3},
    {"player": "Miles Sanders",            "pos": "RB",  "proj": 140, "team": "CAR", "adp": 162.1},
    {"player": "Devin Singletary",         "pos": "RB",  "proj": 133, "team": "NYG", "adp": 168.4},
    {"player": "Ezekiel Elliott",          "pos": "RB",  "proj": 126, "team": "DAL", "adp": 174.2},
    {"player": "Kareem Hunt",              "pos": "RB",  "proj": 120, "team": "KC", "adp": 170.8},
    {"player": "Dameon Pierce",            "pos": "RB",  "proj": 113, "team": "HOU", "adp": 176.3},
    {"player": "David Montgomery",         "pos": "RB",  "proj": 107, "team": "DET", "adp": 102.5},
    {"player": "Tyjae Spears",             "pos": "RB",  "proj": 100, "team": "TEN", "adp": 163.9},
    {"player": "Rico Dowdle",              "pos": "RB",  "proj":  94, "team": "DAL", "adp": 78.1},
    {"player": "Jaylen Warren",            "pos": "RB",  "proj":  88, "team": "PIT", "adp": 78.6},
    {"player": "Ty Chandler",              "pos": "RB",  "proj":  82, "team": "MIN", "adp": 177.2},
    {"player": "Jaleel McLaughlin",        "pos": "RB",  "proj":  76, "team": "DEN", "adp": 179.6},
    {"player": "Roschon Johnson",          "pos": "RB",  "proj":  70, "team": "CHI", "adp": 181.3},
    {"player": "Kimani Vidal",             "pos": "RB",  "proj":  64, "team": "LAC", "adp": 183.8},
    {"player": "Patrick Taylor",           "pos": "RB",  "proj":  58, "team": "MIA", "adp": 185.4},
    {"player": "Keaton Mitchell",          "pos": "RB",  "proj":  54, "team": "BAL", "adp": 187.1},
    {"player": "Marlon Mack",              "pos": "RB",  "proj":  50, "team": "HOU", "adp": 191.5},
    {"player": "Samaje Perine",            "pos": "RB",  "proj":  46, "team": "DEN", "adp": 193.8},
    {"player": "Elijah Mitchell",          "pos": "RB",  "proj":  42, "team": "SF", "adp": 195.2},
    {"player": "Jordan Mason",             "pos": "RB",  "proj":  38, "team": "SF", "adp": 58.7},
    {"player": "Chris Rodriguez Jr.",      "pos": "RB",  "proj":  34, "team": "WAS", "adp": 172.4},
    # ── WRs ──────────────────────────────────────────────────────────────────
    {"player": "Ja'Marr Chase",            "pos": "WR",  "proj": 360, "team": "CIN", "adp": 4.1},
    {"player": "Puka Nacua",               "pos": "WR",  "proj": 355, "team": "LAR", "adp": 3.2},
    {"player": "CeeDee Lamb",              "pos": "WR",  "proj": 350, "team": "DAL", "adp": 10.4},
    {"player": "Justin Jefferson",         "pos": "WR",  "proj": 350, "team": "MIN", "adp": 24.1},
    {"player": "Amon-Ra St. Brown",        "pos": "WR",  "proj": 340, "team": "DET", "adp": 11.2},
    {"player": "Tyreek Hill",              "pos": "WR",  "proj": 325, "team": "MIA", "adp": 18.9},
    {"player": "Jaxon Smith-Njigba",       "pos": "WR",  "proj": 330, "team": "SEA", "adp": 6.3},
    {"player": "Malik Nabers",             "pos": "WR",  "proj": 315, "team": "NYG", "adp": 15.2},
    {"player": "A.J. Brown",               "pos": "WR",  "proj": 315, "team": "PHI", "adp": 30.4},
    {"player": "Marvin Harrison Jr.",      "pos": "WR",  "proj": 310, "team": "ARI", "adp": 58.2},
    {"player": "Nico Collins",             "pos": "WR",  "proj": 305, "team": "HOU", "adp": 19.4},
    {"player": "Cooper Kupp",              "pos": "WR",  "proj": 305, "team": "LAR", "adp": 108.4},
    {"player": "Drake London",             "pos": "WR",  "proj": 300, "team": "ATL", "adp": 13.1},
    {"player": "Mike Evans",               "pos": "WR",  "proj": 300, "team": "TB", "adp": 80.2},
    {"player": "Garrett Wilson",           "pos": "WR",  "proj": 295, "team": "NYJ", "adp": 39.2},
    {"player": "DK Metcalf",               "pos": "WR",  "proj": 295, "team": "SEA", "adp": 67.3},
    {"player": "Deebo Samuel",             "pos": "WR",  "proj": 290, "team": "SF", "adp": 110.3},
    {"player": "Rashee Rice",              "pos": "WR",  "proj": 290, "team": "KC", "adp": 14.3},
    {"player": "Chris Olave",              "pos": "WR",  "proj": 285, "team": "NO", "adp": 38.1},
    {"player": "Brian Thomas Jr.",         "pos": "WR",  "proj": 285, "team": "JAX", "adp": 73.2},
    {"player": "Davante Adams",            "pos": "WR",  "proj": 280, "team": "LV", "adp": 28.3},
    {"player": "Rome Odunze",              "pos": "WR",  "proj": 280, "team": "CHI", "adp": 63.1},
    {"player": "DJ Moore",                 "pos": "WR",  "proj": 275, "team": "CHI", "adp": 115.2},
    {"player": "Xavier Worthy",            "pos": "WR",  "proj": 275, "team": "KC", "adp": 140.1},
    {"player": "Jaylen Waddle",            "pos": "WR",  "proj": 270, "team": "MIA", "adp": 45.2},
    {"player": "Ladd McConkey",            "pos": "WR",  "proj": 270, "team": "LAC", "adp": 70.1},
    {"player": "Zay Flowers",              "pos": "WR",  "proj": 265, "team": "BAL", "adp": 48.1},
    {"player": "Tetairoa McMillan",        "pos": "WR",  "proj": 265, "team": "CAR", "adp": 41.3},
    {"player": "DeVonta Smith",            "pos": "WR",  "proj": 260, "team": "PHI", "adp": 55.4},
    {"player": "Tank Dell",                "pos": "WR",  "proj": 255, "team": "HOU", "adp": 118.3},
    {"player": "Stefon Diggs",             "pos": "WR",  "proj": 250, "team": "NE", "adp": 90.1},
    {"player": "Tee Higgins",              "pos": "WR",  "proj": 245, "team": "CIN", "adp": 36.1},
    {"player": "Amari Cooper",             "pos": "WR",  "proj": 240, "team": "BUF", "adp": 145.2},
    {"player": "Christian Kirk",           "pos": "WR",  "proj": 235, "team": "JAX", "adp": 148.3},
    {"player": "Terry McLaurin",           "pos": "WR",  "proj": 230, "team": "WAS", "adp": 44.2},
    {"player": "Diontae Johnson",          "pos": "WR",  "proj": 225, "team": "CAR", "adp": 152.1},
    {"player": "Keenan Allen",             "pos": "WR",  "proj": 220, "team": "CHI", "adp": 158.4},
    {"player": "Courtland Sutton",         "pos": "WR",  "proj": 215, "team": "DEN", "adp": 62.3},
    {"player": "Adam Thielen",             "pos": "WR",  "proj": 210, "team": "CAR", "adp": 164.2},
    {"player": "Michael Pittman Jr.",      "pos": "WR",  "proj": 205, "team": "IND", "adp": 56.4},
    {"player": "Calvin Ridley",            "pos": "WR",  "proj": 200, "team": "TEN", "adp": 142.3},
    {"player": "Chris Godwin",             "pos": "WR",  "proj": 195, "team": "TB", "adp": 125.1},
    {"player": "Kendrick Bourne",          "pos": "WR",  "proj": 190, "team": "NE", "adp": 168.4},
    {"player": "Darnell Mooney",           "pos": "WR",  "proj": 185, "team": "ATL", "adp": 160.2},
    {"player": "Quentin Johnston",         "pos": "WR",  "proj": 180, "team": "LAC", "adp": 138.3},
    {"player": "Wan'Dale Robinson",        "pos": "WR",  "proj": 175, "team": "NYG", "adp": 143.1},
    {"player": "Gabe Davis",               "pos": "WR",  "proj": 170, "team": "JAX", "adp": 173.4},
    {"player": "Elijah Moore",             "pos": "WR",  "proj": 165, "team": "CLE", "adp": 178.2},
    {"player": "Rashid Shaheed",           "pos": "WR",  "proj": 160, "team": "NO", "adp": 163.4},
    {"player": "Cedric Tillman",           "pos": "WR",  "proj": 155, "team": "CLE", "adp": 169.1},
    {"player": "Odell Beckham Jr.",        "pos": "WR",  "proj": 148, "team": "MIA", "adp": 180.2},
    {"player": "Demarcus Robinson",        "pos": "WR",  "proj": 142, "team": "LAR", "adp": 187.4},
    {"player": "Marquez Valdes-Scantling", "pos": "WR",  "proj": 136, "team": "NE", "adp": 191.2},
    {"player": "Nelson Agholor",           "pos": "WR",  "proj": 130, "team": "NE", "adp": 193.4},
    {"player": "Jalen Tolbert",            "pos": "WR",  "proj": 124, "team": "DAL", "adp": 176.3},
    {"player": "Parris Campbell",          "pos": "WR",  "proj": 118, "team": "NYG", "adp": 182.1},
    {"player": "Tutu Atwell",              "pos": "WR",  "proj": 112, "team": "LAR", "adp": 185.6},
    {"player": "Dontayvion Wicks",         "pos": "WR",  "proj": 106, "team": "GB", "adp": 172.8},
    {"player": "Jakobi Meyers",            "pos": "WR",  "proj": 100, "team": "LV", "adp": 155.3},
    {"player": "Tre Tucker",               "pos": "WR",  "proj":  94, "team": "LV", "adp": 195.1},
    {"player": "K.J. Osborn",              "pos": "WR",  "proj":  88, "team": "NE", "adp": 197.4},
    {"player": "Khalil Shakir",            "pos": "WR",  "proj":  82, "team": "BUF", "adp": 135.4},
    {"player": "Allen Lazard",             "pos": "WR",  "proj":  76, "team": "NYJ", "adp": 196.2},
    {"player": "Kadarius Toney",           "pos": "WR",  "proj":  70, "team": "KC", "adp": 198.8},
    {"player": "Skyy Moore",               "pos": "WR",  "proj":  64, "team": "KC", "adp": 200.3},
    # ── TEs ──────────────────────────────────────────────────────────────────
    {"player": "Travis Kelce",             "pos": "TE",  "proj": 280, "team": "KC", "adp": 100.2},
    {"player": "Sam LaPorta",              "pos": "TE",  "proj": 270, "team": "DET", "adp": 70.3},
    {"player": "Brock Bowers",             "pos": "TE",  "proj": 265, "team": "LV", "adp": 28.4},
    {"player": "Trey McBride",             "pos": "TE",  "proj": 255, "team": "ARI", "adp": 12.3},
    {"player": "Mark Andrews",             "pos": "TE",  "proj": 250, "team": "BAL", "adp": 95.4},
    {"player": "George Kittle",            "pos": "TE",  "proj": 245, "team": "SF", "adp": 40.2},
    {"player": "Dalton Kincaid",           "pos": "TE",  "proj": 240, "team": "BUF", "adp": 138.2},
    {"player": "Kyle Pitts",               "pos": "TE",  "proj": 235, "team": "ATL", "adp": 62.1},
    {"player": "David Njoku",              "pos": "TE",  "proj": 230, "team": "CLE", "adp": 115.3},
    {"player": "Evan Engram",              "pos": "TE",  "proj": 225, "team": "JAX", "adp": 140.2},
    {"player": "T.J. Hockenson",           "pos": "TE",  "proj": 220, "team": "MIN", "adp": 88.1},
    {"player": "Jake Ferguson",            "pos": "TE",  "proj": 215, "team": "DAL", "adp": 78.3},
    {"player": "Pat Freiermuth",           "pos": "TE",  "proj": 210, "team": "PIT", "adp": 150.2},
    {"player": "Cole Kmet",                "pos": "TE",  "proj": 205, "team": "CHI", "adp": 155.1},
    {"player": "Isaiah Likely",            "pos": "TE",  "proj": 200, "team": "BAL", "adp": 105.3},
    {"player": "Hunter Henry",             "pos": "TE",  "proj": 193, "team": "NE", "adp": 112.4},
    {"player": "Gerald Everett",           "pos": "TE",  "proj": 186, "team": "LAC", "adp": 165.1},
    {"player": "Mike Gesicki",             "pos": "TE",  "proj": 178, "team": "CIN", "adp": 170.3},
    {"player": "Juwan Johnson",            "pos": "TE",  "proj": 170, "team": "NO", "adp": 130.4},
    {"player": "Tucker Kraft",             "pos": "TE",  "proj": 163, "team": "GB", "adp": 48.4},
    {"player": "Noah Fant",                "pos": "TE",  "proj": 157, "team": "SEA", "adp": 175.2},
    {"player": "Cade Otton",               "pos": "TE",  "proj": 150, "team": "TB", "adp": 180.1},
    {"player": "Tyler Higbee",             "pos": "TE",  "proj": 143, "team": "LAR", "adp": 178.3},
    {"player": "Jonnu Smith",              "pos": "TE",  "proj": 136, "team": "MIA", "adp": 172.4},
    # ── Ks ───────────────────────────────────────────────────────────────────
    {"player": "Justin Tucker",            "pos": "K",   "proj": 155, "team": "BAL", "adp": 148.1},
    {"player": "Evan McPherson",           "pos": "K",   "proj": 148, "team": "CIN", "adp": 152.3},
    {"player": "Harrison Butker",          "pos": "K",   "proj": 142, "team": "KC", "adp": 156.4},
    {"player": "Tyler Bass",               "pos": "K",   "proj": 136, "team": "BUF", "adp": 159.2},
    {"player": "Jake Elliott",             "pos": "K",   "proj": 130, "team": "PHI", "adp": 161.8},
    {"player": "Brandon Aubrey",           "pos": "K",   "proj": 125, "team": "DAL", "adp": 163.5},
    {"player": "Cameron Dicker",           "pos": "K",   "proj": 120, "team": "LAC", "adp": 165.2},
    {"player": "Younghoe Koo",             "pos": "K",   "proj": 115, "team": "ATL", "adp": 167.4},
    {"player": "Chris Boswell",            "pos": "K",   "proj": 110, "team": "PIT", "adp": 169.1},
    {"player": "Greg Joseph",              "pos": "K",   "proj": 105, "team": "MIN", "adp": 171.3},
    {"player": "Matt Gay",                 "pos": "K",   "proj": 100, "team": "IND", "adp": 173.6},
    {"player": "Jason Sanders",            "pos": "K",   "proj":  95, "team": "MIA", "adp": 175.8},
    # ── DEF ──────────────────────────────────────────────────────────────────
    {"player": "San Francisco 49ers",      "pos": "DEF", "proj": 155, "team": "SF", "adp": 149.2},
    {"player": "Dallas Cowboys",           "pos": "DEF", "proj": 148, "team": "DAL", "adp": 153.4},
    {"player": "New England Patriots",     "pos": "DEF", "proj": 142, "team": "NE", "adp": 157.1},
    {"player": "Baltimore Ravens",         "pos": "DEF", "proj": 136, "team": "BAL", "adp": 159.8},
    {"player": "Buffalo Bills",            "pos": "DEF", "proj": 130, "team": "BUF", "adp": 161.4},
    {"player": "Pittsburgh Steelers",      "pos": "DEF", "proj": 125, "team": "PIT", "adp": 163.7},
    {"player": "Cleveland Browns",         "pos": "DEF", "proj": 120, "team": "CLE", "adp": 165.9},
    {"player": "Philadelphia Eagles",      "pos": "DEF", "proj": 115, "team": "PHI", "adp": 167.3},
    {"player": "Kansas City Chiefs",       "pos": "DEF", "proj": 110, "team": "KC", "adp": 169.6},
    {"player": "Miami Dolphins",           "pos": "DEF", "proj": 105, "team": "MIA", "adp": 171.8},
    {"player": "Minnesota Vikings",        "pos": "DEF", "proj": 100, "team": "MIN", "adp": 173.4},
    {"player": "Los Angeles Rams",         "pos": "DEF", "proj":  95, "team": "LAR", "adp": 175.9},
]
players_df = pd.DataFrame(player_data).sort_values("adp", ascending=True).reset_index(drop=True)

# ── Constants ─────────────────────────────────────────────────────────────────
SCORE_MIN   = 88.0
SCORE_MAX   = 128.0
SCORE_STD   = 18.0
NUM_TEAMS   = 12
NUM_ROUNDS  = 15
TOTAL_PICKS = NUM_TEAMS * NUM_ROUNDS
WEEKS_REG   = 14

# Lineup slots: label -> eligible positions
LINEUP_SLOTS = {
    "QB":   ["QB"],
    "RB1":  ["RB"],
    "RB2":  ["RB"],
    "WR1":  ["WR"],
    "WR2":  ["WR"],
    "TE":   ["TE"],
    "FLEX": ["RB", "WR", "TE"],
    "K":    ["K"],
    "DEF":  ["DEF"],
}
STARTER_SLOTS = list(LINEUP_SLOTS.keys())

# ── 2025 NFL Bye Weeks (NFL week number) ─────────────────────────────────────
# Source: 2025 NFL regular season schedule
BYE_WEEKS = {
    "ARI":  5,  "LAC":  5,
    "DET":  6,  "NYG":  6,
    "CAR":  7,  "GB":   7,  "LV":  7,  "NYJ":  7,
    "CHI":  8,  "SF":   8,  "SEA": 8,  "ATL":  8,
    "DAL":  9,  "MIA":  9,  "NO":  9,  "BAL":  9,
    "DEN": 10,  "TB":  10,  "CLE":10,  "HOU": 10,
    "BUF": 11,  "LAR": 11,  "NE": 11,  "PIT": 11,
    "IND": 12,  "MIN": 12,  "PHI":12,  "WAS": 12,
    "JAX": 13,  "KC":  13,  "CIN":13,  "TEN": 13,
}

def get_player_team(name):
    row = players_df[players_df["player"] == name]
    return str(row["team"].iloc[0]) if not row.empty and "team" in row.columns else ""

def is_on_bye(name, nfl_week):
    """Return True if this player's NFL team has a bye in the given week."""
    team = get_player_team(name)
    return BYE_WEEKS.get(team, -1) == nfl_week

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

def sim_team_score(mean):
    """CPU team score as a single number."""
    return round(max(55.0, min(200.0, random.gauss(mean, SCORE_STD))), 2)

def sim_player_score(proj, player_name="", nfl_week=None):
    """Simulate one player's weekly score. Returns 0.0 on bye week."""
    if nfl_week and player_name and is_on_bye(player_name, nfl_week):
        return 0.0
    weekly_mean = proj / 17.0
    std = weekly_mean * 0.50
    return round(max(0.0, random.gauss(weekly_mean, std)), 2)

def get_player_proj(name):
    row = players_df[players_df["player"] == name]
    return float(row["proj"].iloc[0]) if not row.empty else 0.0

def get_player_pos(name):
    row = players_df[players_df["player"] == name]
    return str(row["pos"].iloc[0]) if not row.empty else ""

def auto_set_lineup(roster_names):
    """Pick the best projected lineup from the given roster."""
    roster = [(n, get_player_pos(n), get_player_proj(n)) for n in roster_names]
    lineup = {s: None for s in STARTER_SLOTS}
    used = set()

    # Fill each positional slot greedily by projection (excluding FLEX first)
    for slot, eligible in LINEUP_SLOTS.items():
        if slot == "FLEX":
            continue
        candidates = sorted(
            [(n, p, proj) for n, p, proj in roster if p in eligible and n not in used],
            key=lambda x: x[2], reverse=True
        )
        if candidates:
            best = candidates[0]
            lineup[slot] = best[0]
            used.add(best[0])

    # Fill FLEX with best remaining RB/WR/TE
    flex_candidates = sorted(
        [(n, p, proj) for n, p, proj in roster if p in ["RB", "WR", "TE"] and n not in used],
        key=lambda x: x[2], reverse=True
    )
    if flex_candidates:
        lineup["FLEX"] = flex_candidates[0][0]
        used.add(flex_candidates[0][0])

    return lineup

def score_lineup(lineup, nfl_week=None):
    """Sum up simulated player scores for all starters. Returns (total, score_dict)."""
    scores = {}
    for slot, player in lineup.items():
        if player:
            score = sim_player_score(get_player_proj(player), player, nfl_week)
            on_bye = nfl_week and is_on_bye(player, nfl_week)
            scores[slot] = (player, score, on_bye)
        else:
            scores[slot] = (None, 0.0, False)
    total = round(sum(v[1] for v in scores.values()), 2)
    return total, scores

def render_playoff_scorecard():
    """Reusable side-by-side player scorecard for playoff results screens."""
    opp_name = ss.opp_team_name or "Opponent"

    def build_rows(score_dict):
        rows = []
        for slot, val in score_dict.items():
            player = val[0] if val else None
            score  = val[1] if len(val) > 1 else 0.0
            if player:
                rows.append({
                    "Slot":   slot,
                    "Player": player,
                    "Team":   get_player_team(player),
                    "Pos":    get_player_pos(player),
                    "Score":  score,
                    "Proj":   f"{get_player_proj(player)/17:.1f}",
                })
        return pd.DataFrame(rows)

    with st.expander("📊 Matchup Scorecard", expanded=True):
        mc1, mc2 = st.columns(2)
        with mc1:
            df = build_rows(ss.week_player_scores)
            total = round(df["Score"].sum(), 2) if not df.empty else 0.0
            st.markdown(f"### 🏈 {ss.your_team}")
            st.metric("Total Score", total)
            st.dataframe(df, use_container_width=True, hide_index=True)
        with mc2:
            df = build_rows(ss.opp_player_scores) if ss.opp_player_scores else pd.DataFrame()
            total = round(df["Score"].sum(), 2) if not df.empty else 0.0
            st.markdown(f"### 🆚 {opp_name}")
            st.metric("Total Score", total)
            if not df.empty:
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("CPU opponent — no individual player data.")

def get_standings(weekly_results, all_teams):
    s = {t: {"W": 0, "L": 0, "PF": 0.0, "PA": 0.0} for t in all_teams}
    for wk in weekly_results:
        for t1, t2, s1, s2 in wk["matchups"]:
            s[t1]["PF"] += s1; s[t1]["PA"] += s2
            s[t2]["PF"] += s2; s[t2]["PA"] += s1
            if s1 > s2:   s[t1]["W"] += 1; s[t2]["L"] += 1
            elif s2 > s1: s[t2]["W"] += 1; s[t1]["L"] += 1
            else:         s[t1]["W"] += 0.5; s[t2]["W"] += 0.5
    rows = [{"Team": t, "W": v["W"], "L": v["L"],
             "PF": round(v["PF"], 2), "PA": round(v["PA"], 2)}
            for t, v in s.items()]
    return pd.DataFrame(rows).sort_values(["W", "PF"], ascending=[False, False]).reset_index(drop=True)

# ── Session state ─────────────────────────────────────────────────────────────
defaults = {
    "phase":            "setup",
    "rosters":          {},
    "drafted":          None,
    "current_pick":     0,
    "your_pick_pos":    1,
    "your_team":        "@Tailwind40",
    "team_strengths":   {},
    "schedule":         [],
    "current_week":     1,
    "weekly_results":   [],
    "week_results":     [],
    "week_player_scores": {},   # slot -> (player, score, on_bye) for user's last simmed week
    "opp_player_scores":  {},   # same structure for opponent
    "opp_team_name":      "",   # name of user's opponent this week
    "my_lineup":        {},     # slot -> player name
    "playoff_seeds":    [],
    "playoff_wc":       [],
    "playoff_semis":    [],
    "playoff_champ":    None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

ss = st.session_state

def get_draft_order():
    order = []
    for r in range(NUM_ROUNDS):
        order.extend(range(1, NUM_TEAMS+1) if r % 2 == 0 else range(NUM_TEAMS, 0, -1))
    return order

# ── Shared: My Team sidebar panel ─────────────────────────────────────────────
def render_my_team_panel():
    """Renders lineup editor + full roster in a sidebar expander."""
    roster = ss.rosters.get(ss.your_team, [])
    if not roster:
        return

    with st.sidebar:
        st.markdown(f"### 🏈 {ss.your_team}")

        # ── Lineup Editor ──────────────────────────────────────────────────
        st.markdown("**📋 Starting Lineup**")
        if st.button("⚡ Auto-Set Best Lineup", key="auto_lineup"):
            ss.my_lineup = auto_set_lineup(roster)
            st.rerun()

        new_lineup = {}
        all_used = []  # track picks to warn on duplicates

        for slot, eligible_pos in LINEUP_SLOTS.items():
            eligible = [p for p in roster if get_player_pos(p) in eligible_pos]
            options = ["-- Empty --"] + eligible
            current = ss.my_lineup.get(slot)
            idx = options.index(current) if current in options else 0

            # Show proj + team + bye warning next to slot label
            proj_label = ""
            if current and current in roster:
                team_tag = get_player_team(current)
                bye_wk   = BYE_WEEKS.get(team_tag, "—")
                bye_warn = f" ⚠️BYE" if bye_wk == ss.current_week else ""
                proj_label = f"  _{team_tag} · ~{get_player_proj(current)/17:.1f} proj{bye_warn}_"

            chosen = st.selectbox(
                f"{slot}{proj_label}",
                options,
                index=idx,
                key=f"lineup_{slot}"
            )
            new_lineup[slot] = chosen if chosen != "-- Empty --" else None
            if new_lineup[slot]:
                all_used.append(new_lineup[slot])

        # Warn on duplicates
        dupes = [p for p in all_used if all_used.count(p) > 1]
        if dupes:
            st.warning(f"⚠️ Duplicate players: {', '.join(set(dupes))}")
        else:
            if new_lineup != ss.my_lineup:
                ss.my_lineup = new_lineup

        st.divider()

        # ── Full Roster ────────────────────────────────────────────────────
        st.markdown("**📄 Full Roster**")
        starters = list(ss.my_lineup.values())
        current_wk = ss.current_week
        rows = []
        for p in roster:
            pos   = get_player_pos(p)
            proj  = get_player_proj(p)
            team  = get_player_team(p)
            bye   = BYE_WEEKS.get(team, "—")
            role  = "🟢 Starter" if p in starters else "⚪ Bench"
            bye_flag = f"💤 Wk {bye}" if bye == current_wk else f"Wk {bye}"
            rows.append({"Player": p, "Team": team, "Pos": pos, "Proj": proj, "Bye": bye_flag, "Status": role})
        df = pd.DataFrame(rows).sort_values(["Status", "Proj"], ascending=[True, False])
        st.dataframe(df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════
# PHASE: SETUP
# ══════════════════════════════════════════════════════════════
if ss.phase == "setup":
    st.title("FF Simulator 🏈")
    st.markdown("12-Team Snake Draft + Full Season + Playoffs. Built by @Tailwind40")

    ss.your_team    = st.text_input("Your team name", value=ss.your_team)
    ss.your_pick_pos = st.selectbox("Your draft position (1–12)", list(range(1, 13)))

    if st.button("🏈 Start Draft"):
        ss.rosters       = {f"Team {i+1}": [] for i in range(NUM_TEAMS)}
        ss.rosters[ss.your_team] = []
        ss.drafted       = players_df.sort_values("adp", ascending=True).reset_index(drop=True).copy()
        ss.current_pick  = 0
        ss.weekly_results = []
        ss.current_week  = 1
        ss.my_lineup     = {}
        ss.phase         = "draft"
        st.rerun()


# ══════════════════════════════════════════════════════════════
# PHASE: DRAFT
# ══════════════════════════════════════════════════════════════
elif ss.phase == "draft":

    # ── CSS for the draft board ──────────────────────────────
    st.markdown("""
    <style>
    /* Hide default page padding a bit */
    .block-container { padding-top: 1rem; }

    /* On-the-clock banner */
    .otc-banner {
        background: linear-gradient(90deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
        border-left: 5px solid #e94560;
        border-radius: 6px;
        padding: 10px 18px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .otc-pick { color: #aaa; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 1px; }
    .otc-name { color: #fff; font-size: 1.25rem; font-weight: 700; }
    .otc-you  { color: #e94560; font-size: 0.85rem; font-weight: 600; background: rgba(233,69,96,0.15);
                padding: 2px 8px; border-radius: 4px; border: 1px solid rgba(233,69,96,0.4); }
    .otc-round { color: #e94560; font-size: 0.85rem; font-weight: 600; margin-left: auto; }

    /* Progress bar */
    .draft-progress-bg {
        background: #1a1a2e; border-radius: 4px; height: 6px; margin-bottom: 14px;
    }
    .draft-progress-fill {
        background: linear-gradient(90deg, #e94560, #ff6b6b);
        height: 6px; border-radius: 4px; transition: width 0.3s;
    }

    /* Position pill badges */
    .pos-qb  { background:#c0392b; color:#fff; padding:2px 7px; border-radius:4px; font-size:0.72rem; font-weight:700; }
    .pos-rb  { background:#27ae60; color:#fff; padding:2px 7px; border-radius:4px; font-size:0.72rem; font-weight:700; }
    .pos-wr  { background:#2980b9; color:#fff; padding:2px 7px; border-radius:4px; font-size:0.72rem; font-weight:700; }
    .pos-te  { background:#e67e22; color:#fff; padding:2px 7px; border-radius:4px; font-size:0.72rem; font-weight:700; }
    .pos-k   { background:#8e44ad; color:#fff; padding:2px 7px; border-radius:4px; font-size:0.72rem; font-weight:700; }
    .pos-def { background:#2c3e50; color:#fff; padding:2px 7px; border-radius:4px; font-size:0.72rem; font-weight:700; }

    /* Player rows */
    .player-row {
        display: flex; align-items: center; padding: 5px 8px;
        border-bottom: 1px solid #f0f0f0; gap: 8px;
        min-height: 40px;
    }
    .player-row:hover { background: #f0f4ff; }
    .player-rank  { color: #bbb; font-size: 0.73rem; width: 20px; text-align:right; flex-shrink:0; }
    .player-name  { font-weight: 700; font-size: 0.9rem; flex: 1; min-width: 0; }
    .player-team  { color: #777; font-size: 0.72rem; flex-shrink:0; }
    .player-bye   { color: #bbb; font-size: 0.7rem; flex-shrink:0; }
    .player-stats { display:flex; flex-direction:column; align-items:flex-end; gap:1px; flex-shrink:0; }
    .player-adp   { color: #e94560; font-size: 0.72rem; font-weight:700; white-space:nowrap; }
    .player-proj  { color: #2980b9; font-size: 0.72rem; font-weight:600; white-space:nowrap; }

    /* Make draft buttons compact and consistent height */
    div[data-testid="stColumn"] .stButton > button[kind="primary"] {
        font-size: 0.8rem !important;
        padding: 4px 6px !important;
        min-height: 32px !important;
        line-height: 1.2 !important;
        white-space: nowrap !important;
        border-radius: 5px !important;
        font-weight: 700 !important;
        letter-spacing: 0.3px !important;
    }

    /* Roster slot rows */
    .roster-row {
        display: flex; align-items: center; padding: 5px 8px;
        border-bottom: 1px solid #f0f0f0; gap: 8px; font-size: 0.85rem;
    }
    .roster-slot { color: #888; font-size: 0.72rem; width: 36px; flex-shrink:0; }
    .roster-name { flex:1; font-weight:500; }
    .roster-empty { flex:1; color:#ccc; font-style:italic; }
    </style>
    """, unsafe_allow_html=True)

    draft_order = get_draft_order()

    # ── Finish draft ─────────────────────────────────────────
    if ss.current_pick >= TOTAL_PICKS:
        all_teams = list(ss.rosters.keys())
        proj_sums = {
            t: players_df[players_df["player"].isin(r)]["proj"].sum()
            for t, r in ss.rosters.items()
        }
        all_sums = list(proj_sums.values())
        ss.team_strengths = {t: proj_to_mean(v, all_sums) for t, v in proj_sums.items()}
        ss.schedule       = generate_schedule(all_teams)
        ss.current_week   = 1
        ss.my_lineup      = auto_set_lineup(ss.rosters[ss.your_team])
        ss.phase          = "week_preview"
        st.rerun()

    curr_num  = draft_order[ss.current_pick]
    is_yours  = curr_num == ss.your_pick_pos
    curr_name = ss.your_team if is_yours else f"Team {curr_num}"
    rnd       = ss.current_pick // NUM_TEAMS + 1
    pct       = ss.current_pick / TOTAL_PICKS * 100

    def cpu_pick(team_name):
        # Count current positional needs for this team
        roster = ss.rosters.get(team_name, [])
        pos_counts = {}
        for p in roster:
            pos = get_player_pos(p)
            pos_counts[pos] = pos_counts.get(pos, 0) + 1

        # Positional maximums — don't overdraft a position
        pos_max = {"QB": 2, "RB": 6, "WR": 7, "TE": 2, "K": 1, "DEF": 1}
        round_num = len(roster) + 1

        # Late rounds: force K and DEF if not drafted
        if round_num >= 13 and pos_counts.get("K", 0) == 0:
            k_options = ss.drafted[ss.drafted["pos"] == "K"]
            if not k_options.empty:
                best = k_options.iloc[0]
                ss.rosters[team_name].append(best["player"])
                ss.drafted = ss.drafted[ss.drafted["player"] != best["player"]].reset_index(drop=True)
                ss.current_pick += 1
                return
        if round_num >= 14 and pos_counts.get("DEF", 0) == 0:
            d_options = ss.drafted[ss.drafted["pos"] == "DEF"]
            if not d_options.empty:
                best = d_options.iloc[0]
                ss.rosters[team_name].append(best["player"])
                ss.drafted = ss.drafted[ss.drafted["player"] != best["player"]].reset_index(drop=True)
                ss.current_pick += 1
                return

        # Filter out overstocked positions, pick best ADP available
        available = ss.drafted[
            ss.drafted["pos"].apply(lambda p: pos_counts.get(p, 0) < pos_max.get(p, 99))
        ]
        if available.empty:
            available = ss.drafted  # fallback

        best = available.iloc[0]
        ss.rosters[team_name].append(best["player"])
        ss.drafted = ss.drafted[ss.drafted["player"] != best["player"]].reset_index(drop=True)
        ss.current_pick += 1

    def pos_badge(pos):
        cls = f"pos-{pos.lower()}"
        return f'<span class="{cls}">{pos}</span>'

    # ── On-the-clock banner + action controls ────────────────
    you_tag = '<span class="otc-you">⭐ YOUR PICK</span>' if is_yours else ''
    st.markdown(f"""
    <div class="otc-banner">
        <div>
            <div class="otc-pick">Pick {ss.current_pick + 1} of {TOTAL_PICKS}</div>
            <div class="otc-name">🏈 {curr_name} {you_tag}</div>
        </div>
        <div class="otc-round">Round {rnd} of {NUM_ROUNDS}</div>
    </div>
    <div class="draft-progress-bg">
        <div class="draft-progress-fill" style="width:{pct:.1f}%"></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Draft action bar — sits right below the banner ────────
    if is_yours:
        ac1, ac2 = st.columns([1, 1])
        with ac1:
            if st.button("⚡ Auto-Pick Best Available", use_container_width=True, type="primary"):
                cpu_pick(ss.your_team)
                st.rerun()
    else:
        ac1, ac2, ac3 = st.columns(3)
        with ac1:
            if st.button("▶️ CPU Picks Once", use_container_width=True, type="primary"):
                cpu_pick(curr_name)
                st.rerun()
        with ac2:
            if st.button("⏩ Skip to My Pick", use_container_width=True):
                while ss.current_pick < TOTAL_PICKS:
                    cn = draft_order[ss.current_pick]
                    if cn == ss.your_pick_pos:
                        break
                    nm = ss.your_team if cn == ss.your_pick_pos else f"Team {cn}"
                    cpu_pick(nm)
                st.rerun()
        with ac3:
            if st.button("⏭️ Auto-Complete Draft", use_container_width=True):
                while ss.current_pick < TOTAL_PICKS:
                    cn = draft_order[ss.current_pick]
                    nm = ss.your_team if cn == ss.your_pick_pos else f"Team {cn}"
                    cpu_pick(nm)
                st.rerun()

    st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)

    # ── Two-column layout: players left, roster right ─────────
    left_col, right_col = st.columns([3, 2])

    with left_col:
        # Position filter
        pos_filter = st.radio(
            "Filter",
            ["All", "QB", "RB", "WR", "TE", "K", "DEF"],
            horizontal=True,
            label_visibility="collapsed",
            key="pos_filter_radio"
        )

        if pos_filter == "All":
            view_df = ss.drafted.head(40).reset_index(drop=True)
        else:
            view_df = ss.drafted[ss.drafted["pos"] == pos_filter].head(30).reset_index(drop=True)

        if view_df.empty:
            st.info("No players available at this position.")
        else:
            for i, row in view_df.iterrows():
                p_col, btn_col = st.columns([4, 1])
                with p_col:
                    badge = pos_badge(row["pos"])
                    team     = row.get("team", "")
                    bye_wk   = BYE_WEEKS.get(team, "—")
                    adp      = row.get("adp", 999.0)
                    wk_proj  = round(row["proj"] / 17, 1)
                    st.markdown(
                        f'<div class="player-row">' 
                        f'<span class="player-rank">{i+1}</span>'
                        f'{badge}'
                        f'<span class="player-name">{row["player"]}</span>'
                        f'<span class="player-team">{team}</span>'
                        f'<span class="player-bye">bye {bye_wk}</span>'
                        f'<div class="player-stats">'
                        f'  <span class="player-adp">ADP {adp:.1f}</span>'
                        f'  <span class="player-proj">{wk_proj} pts/wk</span>'
                        f'</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                with btn_col:
                    if is_yours:
                        # Wrap in a styled container so button fills nicely
                        st.markdown("<div style='padding-top:2px'>", unsafe_allow_html=True)
                        if st.button(
                            "＋ Draft",
                            key=f"pick_{i}_{row['player']}",
                            use_container_width=True,
                            type="primary",
                            help=f"Draft {row['player']}"
                        ):
                            ss.rosters[ss.your_team].append(row["player"])
                            ss.drafted = ss.drafted[ss.drafted["player"] != row["player"]]
                            ss.current_pick += 1
                            st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown("#### 📋 Your Roster")

        my_roster = ss.rosters.get(ss.your_team, [])

        # Define display slots for roster panel
        display_slots = [
            ("QB", ["QB"]), ("RB", ["RB"]), ("RB", ["RB"]),
            ("WR", ["WR"]), ("WR", ["WR"]), ("TE", ["TE"]),
            ("FLEX", ["RB","WR","TE"]), ("K", ["K"]), ("DEF", ["DEF"]),
            ("BN", None), ("BN", None), ("BN", None),
            ("BN", None), ("BN", None), ("BN", None),
        ]

        # Assign players to slots greedily
        used = set()
        slot_assignments = []
        for slot_label, eligible in display_slots:
            if eligible is None:
                # bench — any remaining player
                remaining = [p for p in my_roster if p not in used]
                if remaining:
                    slot_assignments.append((slot_label, remaining[0]))
                    used.add(remaining[0])
                else:
                    slot_assignments.append((slot_label, None))
            else:
                candidates = [p for p in my_roster
                              if p not in used and get_player_pos(p) in eligible]
                if candidates:
                    # pick highest proj
                    best = max(candidates, key=get_player_proj)
                    slot_assignments.append((slot_label, best))
                    used.add(best)
                else:
                    slot_assignments.append((slot_label, None))

        rows_html = ""
        for slot_label, player in slot_assignments:
            slot_color = {"QB":"#c0392b","RB":"#27ae60","WR":"#2980b9",
                          "TE":"#e67e22","FLEX":"#7f8c8d","K":"#8e44ad",
                          "DEF":"#2c3e50","BN":"#bbb"}.get(slot_label, "#aaa")
            slot_span = f'<span class="roster-slot" style="color:{slot_color};font-weight:700">{slot_label}</span>'
            if player:
                pos  = get_player_pos(player)
                badge = pos_badge(pos)
                rows_html += f"""
                <div class="roster-row">
                    {slot_span}
                    {badge}
                    <span class="roster-name">{player}</span>
                </div>"""
            else:
                rows_html += f"""
                <div class="roster-row">
                    {slot_span}
                    <span class="roster-empty">— empty —</span>
                </div>"""

        st.markdown(rows_html, unsafe_allow_html=True)

        # Recent picks log
        if ss.current_pick > 0:
            st.markdown("#### 🕐 Recent Picks")
            recent_picks = []
            pick_num = ss.current_pick
            all_teams_in_order = []
            for i in range(ss.current_pick):
                cn = draft_order[i]
                nm = ss.your_team if cn == ss.your_pick_pos else f"Team {cn}"
                all_teams_in_order.append(nm)

            # Collect recent pick history from rosters
            pick_log = []
            team_pick_idx = {t: 0 for t in ss.rosters}
            for i in range(ss.current_pick):
                team_at_pick = all_teams_in_order[i]
                idx = team_pick_idx[team_at_pick]
                if idx < len(ss.rosters[team_at_pick]):
                    player_at_pick = ss.rosters[team_at_pick][idx]
                    pick_log.append((i + 1, team_at_pick, player_at_pick))
                    team_pick_idx[team_at_pick] += 1

            log_html = ""
            for pnum, team, player in reversed(pick_log[-8:]):
                is_you = team == ss.your_team
                style = "font-weight:700;color:#e94560;" if is_you else "color:#555;"
                pos = get_player_pos(player)
                badge = pos_badge(pos)
                log_html += f"""
                <div class="roster-row">
                    <span style="color:#aaa;font-size:0.75rem;width:28px">{pnum}</span>
                    {badge}
                    <span style="{style}font-size:0.83rem;flex:1">{player}</span>
                    <span style="color:#aaa;font-size:0.75rem">{team}</span>
                </div>"""
            st.markdown(log_html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PHASE: WEEK PREVIEW
# ══════════════════════════════════════════════════════════════
elif ss.phase == "week_preview":
    render_my_team_panel()

    wk        = ss.current_week
    matchups  = ss.schedule[wk - 1]
    all_teams = list(ss.rosters.keys())

    st.title(f"📅 Week {wk} of {WEEKS_REG}")

    your_game = next(((t1,t2) for t1,t2 in matchups if ss.your_team in (t1,t2)), None)
    if your_game:
        opp = your_game[1] if your_game[0] == ss.your_team else your_game[0]
        st.info(f"**Your matchup:** {ss.your_team} vs **{opp}**")

        opp_roster = ss.rosters.get(opp, [])
        if opp_roster:
            with st.expander(f"🔍 Scout {opp}'s Roster", expanded=False):
                opp_lineup = auto_set_lineup(opp_roster)
                starters_set = set(opp_lineup.values())
                rows = []
                for slot, player in opp_lineup.items():
                    if player:
                        team   = get_player_team(player)
                        bye_wk = BYE_WEEKS.get(team, "—")
                        rows.append({
                            "Slot":     slot,
                            "Player":   player,
                            "Team":     team,
                            "Pos":      get_player_pos(player),
                            "Proj/wk":  f"{get_player_proj(player)/17:.1f}",
                            "Bye Wk":   f"💤 THIS WEEK" if bye_wk == wk else str(bye_wk),
                            "Status":   "🟢 Starter",
                        })
                bench = [p for p in opp_roster if p not in starters_set]
                for player in bench:
                    team   = get_player_team(player)
                    bye_wk = BYE_WEEKS.get(team, "—")
                    rows.append({
                        "Slot":     "BN",
                        "Player":   player,
                        "Team":     team,
                        "Pos":      get_player_pos(player),
                        "Proj/wk":  f"{get_player_proj(player)/17:.1f}",
                        "Bye Wk":   f"💤 THIS WEEK" if bye_wk == wk else str(bye_wk),
                        "Status":   "⚪ Bench",
                    })
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # Lineup summary callout
    starters = {s: p for s, p in ss.my_lineup.items() if p}
    if starters:
        with st.expander("📋 Your starting lineup this week", expanded=False):
            rows = []
            for s, p in starters.items():
                team   = get_player_team(p)
                bye_wk = BYE_WEEKS.get(team, "—")
                on_bye = bye_wk == wk
                rows.append({
                    "Slot": s, "Player": p,
                    "Team": team,
                    "Pos":  get_player_pos(p),
                    "Wkly Proj": f"{get_player_proj(p)/17:.1f}",
                    "Bye Wk": f"💤 THIS WEEK" if on_bye else str(bye_wk),
                })
            df_lineup = pd.DataFrame(rows)
            # Warn about bye players
            bye_starters = [r["Player"] for _, r in df_lineup.iterrows() if r["Bye Wk"] == "💤 THIS WEEK"]
            if bye_starters:
                st.warning(f"⚠️ On bye this week: {', '.join(bye_starters)} — consider benching them!")
            st.dataframe(df_lineup, use_container_width=True, hide_index=True)
            missing = [s for s in STARTER_SLOTS if not ss.my_lineup.get(s)]
            if missing:
                st.warning(f"⚠️ Empty slots: {', '.join(missing)} — set your lineup in the sidebar!")
    else:
        st.warning("⚠️ No lineup set! Use the sidebar to set your starters.")

    st.markdown("**This week's matchups:**")
    for t1, t2 in matchups:
        tag = "  👈 your game" if ss.your_team in (t1, t2) else ""
        st.write(f"• {t1} vs {t2}{tag}")

    if ss.weekly_results:
        with st.expander("📊 Current standings"):
            st.dataframe(get_standings(ss.weekly_results, all_teams), use_container_width=True, hide_index=True)

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if st.button(f"🏈 Simulate Week {wk}", type="primary"):
            results = []
            for t1, t2 in matchups:
                if t1 == ss.your_team:
                    s1, player_scores = score_lineup(ss.my_lineup, nfl_week=wk)
                    opp_lineup = auto_set_lineup(ss.rosters.get(t2, []))
                    s2, opp_scores = score_lineup(opp_lineup, nfl_week=wk)
                    ss.week_player_scores = player_scores
                    ss.opp_player_scores  = opp_scores
                    ss.opp_team_name      = t2
                elif t2 == ss.your_team:
                    s2, player_scores = score_lineup(ss.my_lineup, nfl_week=wk)
                    opp_lineup = auto_set_lineup(ss.rosters.get(t1, []))
                    s1, opp_scores = score_lineup(opp_lineup, nfl_week=wk)
                    ss.week_player_scores = player_scores
                    ss.opp_player_scores  = opp_scores
                    ss.opp_team_name      = t1
                else:
                    s1 = sim_team_score(ss.team_strengths[t1])
                    s2 = sim_team_score(ss.team_strengths[t2])
                results.append((t1, t2, s1, s2))
            ss.weekly_results.append({"week": wk, "matchups": results})
            ss.week_results = results
            ss.phase = "week_results"
            st.rerun()
    with c2:
        if st.button("⏩ Sim Rest of Season"):
            for w in range(wk, WEEKS_REG + 1):
                week_matchups = ss.schedule[w - 1]
                results = []
                for t1, t2 in week_matchups:
                    if t1 == ss.your_team:
                        s1, player_scores = score_lineup(ss.my_lineup, nfl_week=w)
                        opp_lineup = auto_set_lineup(ss.rosters.get(t2, []))
                        s2, opp_scores = score_lineup(opp_lineup, nfl_week=w)
                        if w == WEEKS_REG:
                            ss.week_player_scores = player_scores
                            ss.opp_player_scores  = opp_scores
                            ss.opp_team_name      = t2
                    elif t2 == ss.your_team:
                        s2, player_scores = score_lineup(ss.my_lineup, nfl_week=w)
                        opp_lineup = auto_set_lineup(ss.rosters.get(t1, []))
                        s1, opp_scores = score_lineup(opp_lineup, nfl_week=w)
                        if w == WEEKS_REG:
                            ss.week_player_scores = player_scores
                            ss.opp_player_scores  = opp_scores
                            ss.opp_team_name      = t1
                    else:
                        s1 = sim_team_score(ss.team_strengths[t1])
                        s2 = sim_team_score(ss.team_strengths[t2])
                    results.append((t1, t2, s1, s2))
                ss.weekly_results.append({"week": w, "matchups": results})
                if w == WEEKS_REG:
                    ss.week_results = results
            ss.current_week = WEEKS_REG
            ss.phase = "week_results"
            st.rerun()


# ══════════════════════════════════════════════════════════════
# PHASE: WEEK RESULTS
# ══════════════════════════════════════════════════════════════
elif ss.phase == "week_results":
    render_my_team_panel()

    wk        = ss.current_week
    results   = ss.week_results
    all_teams = list(ss.rosters.keys())

    st.title(f"📋 Week {wk} Results")

    # League scores
    for t1, t2, s1, s2 in results:
        winner   = t1 if s1 > s2 else (t2 if s2 > s1 else "Tie")
        is_yours = ss.your_team in (t1, t2)
        prefix   = "🏈 " if is_yours else ""
        st.write(f"{prefix}**{t1}** {s1} – {s2} **{t2}**  →  Winner: **{winner}**")

    # User result banner
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

    # ── Side-by-side matchup scorecard ───────────────────────────────────────
    if ss.week_player_scores:
        opp_name = ss.opp_team_name or "Opponent"

        def build_score_rows(score_dict):
            rows = []
            for slot, val in score_dict.items():
                player = val[0] if val else None
                score  = val[1] if len(val) > 1 else 0.0
                on_bye = val[2] if len(val) > 2 else False
                if player:
                    rows.append({
                        "Slot":   slot,
                        "Player": player,
                        "Team":   get_player_team(player),
                        "Pos":    get_player_pos(player),
                        "Score":  score,
                        "Proj":   f"{get_player_proj(player)/17:.1f}",
                    })
            return pd.DataFrame(rows)

        with st.expander("📊 Matchup Scorecard", expanded=True):
            mc1, mc2 = st.columns(2)

            with mc1:
                my_df = build_score_rows(ss.week_player_scores)
                my_total = round(my_df["Score"].sum(), 2) if not my_df.empty else 0.0
                st.markdown(f"### 🏈 {ss.your_team}")
                st.metric("Total Score", my_total)
                st.dataframe(my_df, use_container_width=True, hide_index=True)

            with mc2:
                opp_df = build_score_rows(ss.opp_player_scores) if ss.opp_player_scores else pd.DataFrame()
                opp_total = round(opp_df["Score"].sum(), 2) if not opp_df.empty else 0.0
                st.markdown(f"### 🆚 {opp_name}")
                st.metric("Total Score", opp_total)
                if not opp_df.empty:
                    st.dataframe(opp_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No opponent lineup data available.")

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
            final         = get_standings(ss.weekly_results, all_teams)
            ss.playoff_seeds = final.head(6)["Team"].tolist()
            ss.phase      = "playoff_wildcard_preview"
            st.rerun()


# ══════════════════════════════════════════════════════════════
# PHASE: PLAYOFF WILD CARD PREVIEW
# ══════════════════════════════════════════════════════════════
elif ss.phase == "playoff_wildcard_preview":
    render_my_team_panel()
    seeds = ss.playoff_seeds
    st.title("🏆 Playoffs — Week 15: Wild Card")
    st.markdown("**Seeds 1 & 2 have byes.**")
    st.write(f"• (3) **{seeds[2]}** vs (6) **{seeds[5]}**")
    st.write(f"• (4) **{seeds[3]}** vs (5) **{seeds[4]}**")

    if ss.your_team in seeds[:2]:
        st.info(f"✅ You ({ss.your_team}) have a bye this week!")
    elif ss.your_team in seeds[2:]:
        idx = seeds.index(ss.your_team)
        opp_idx = {2:5, 3:4, 4:3, 5:2}.get(idx, None)
        if opp_idx is not None:
            st.info(f"**Your matchup:** {ss.your_team} vs {seeds[opp_idx]}")
    else:
        st.warning(f"{ss.your_team} did not make the playoffs.")

    # Lineup summary
    with st.expander("📋 Your lineup for Wild Card"):
        starters = {s: p for s, p in ss.my_lineup.items() if p}
        rows = [{"Slot": s, "Player": p, "Pos": get_player_pos(p),
                 "Wkly Proj": f"{get_player_proj(p)/17:.1f}"}
                for s, p in starters.items()]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    if st.button("🏈 Simulate Wild Card", type="primary"):
        pr = ss.playoff_wc = []
        for t1, t2 in [(seeds[2], seeds[5]), (seeds[3], seeds[4])]:
            if t1 == ss.your_team:
                s1, my_scores = score_lineup(ss.my_lineup)
                opp_lineup = auto_set_lineup(ss.rosters.get(t2, []))
                s2, opp_scores = score_lineup(opp_lineup)
                ss.week_player_scores = my_scores
                ss.opp_player_scores  = opp_scores
                ss.opp_team_name      = t2
            elif t2 == ss.your_team:
                opp_lineup = auto_set_lineup(ss.rosters.get(t1, []))
                s1, opp_scores = score_lineup(opp_lineup)
                s2, my_scores = score_lineup(ss.my_lineup)
                ss.week_player_scores = my_scores
                ss.opp_player_scores  = opp_scores
                ss.opp_team_name      = t1
            else:
                s1 = sim_team_score(ss.team_strengths[t1])
                s2 = sim_team_score(ss.team_strengths[t2])
            w = t1 if s1 >= s2 else t2
            pr.append((t1, t2, s1, s2, w))
        ss.phase = "playoff_wildcard_results"
        st.rerun()


# ══════════════════════════════════════════════════════════════
# PHASE: PLAYOFF WILD CARD RESULTS
# ══════════════════════════════════════════════════════════════
elif ss.phase == "playoff_wildcard_results":
    render_my_team_panel()
    st.title("📋 Wild Card Results")
    for t1, t2, s1, s2, w in ss.playoff_wc:
        is_yours = ss.your_team in (t1, t2)
        st.write(f"{'🏈 ' if is_yours else ''}**{t1}** {s1} – {s2} **{t2}**  →  **{w} advances**")

    your_wc = next((r for r in ss.playoff_wc if ss.your_team in (r[0], r[1])), None)
    if your_wc:
        st.divider()
        if your_wc[4] == ss.your_team:
            st.success("✅ You advance to the Semifinals!")
        else:
            st.error("❌ Your season is over. Better luck next year.")

    if ss.week_player_scores:
        render_playoff_scorecard()

    if st.button("➡️ Advance to Semifinals", type="primary"):
        ss.phase = "playoff_semis_preview"
        st.rerun()


# ══════════════════════════════════════════════════════════════
# PHASE: PLAYOFF SEMIS PREVIEW
# ══════════════════════════════════════════════════════════════
elif ss.phase == "playoff_semis_preview":
    render_my_team_panel()
    seeds   = ss.playoff_seeds
    wc_wins = [r[4] for r in ss.playoff_wc]
    semi_matchups = [(seeds[0], wc_wins[1]), (seeds[1], wc_wins[0])]

    st.title("🏆 Playoffs — Week 16: Semifinals")
    for t1, t2 in semi_matchups:
        tag = "  👈 your game" if ss.your_team in (t1, t2) else ""
        st.write(f"• **{t1}** vs **{t2}**{tag}")

    with st.expander("📋 Your lineup for Semis"):
        starters = {s: p for s, p in ss.my_lineup.items() if p}
        rows = [{"Slot": s, "Player": p, "Pos": get_player_pos(p),
                 "Wkly Proj": f"{get_player_proj(p)/17:.1f}"}
                for s, p in starters.items()]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    if st.button("🏈 Simulate Semifinals", type="primary"):
        results = []
        for t1, t2 in semi_matchups:
            if t1 == ss.your_team:
                s1, my_scores = score_lineup(ss.my_lineup)
                opp_lineup = auto_set_lineup(ss.rosters.get(t2, []))
                s2, opp_scores = score_lineup(opp_lineup)
                ss.week_player_scores = my_scores
                ss.opp_player_scores  = opp_scores
                ss.opp_team_name      = t2
            elif t2 == ss.your_team:
                opp_lineup = auto_set_lineup(ss.rosters.get(t1, []))
                s1, opp_scores = score_lineup(opp_lineup)
                s2, my_scores = score_lineup(ss.my_lineup)
                ss.week_player_scores = my_scores
                ss.opp_player_scores  = opp_scores
                ss.opp_team_name      = t1
            else:
                s1 = sim_team_score(ss.team_strengths[t1])
                s2 = sim_team_score(ss.team_strengths[t2])
            w = t1 if s1 >= s2 else t2
            results.append((t1, t2, s1, s2, w))
        ss.playoff_semis = results
        ss.phase = "playoff_semis_results"
        st.rerun()


# ══════════════════════════════════════════════════════════════
# PHASE: PLAYOFF SEMIS RESULTS
# ══════════════════════════════════════════════════════════════
elif ss.phase == "playoff_semis_results":
    render_my_team_panel()
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

    if ss.week_player_scores:
        render_playoff_scorecard()

    if st.button("➡️ Advance to Championship", type="primary"):
        ss.phase = "playoff_champ_preview"
        st.rerun()


# ══════════════════════════════════════════════════════════════
# PHASE: CHAMPIONSHIP PREVIEW
# ══════════════════════════════════════════════════════════════
elif ss.phase == "playoff_champ_preview":
    render_my_team_panel()
    finalists = [r[4] for r in ss.playoff_semis]
    st.title("🏆 Playoffs — Week 17: Championship")
    st.markdown(f"### {finalists[0]} vs {finalists[1]}")
    if ss.your_team in finalists:
        opp = finalists[1] if finalists[0] == ss.your_team else finalists[0]
        st.info(f"🏆 You're in the Championship! {ss.your_team} vs {opp}")

    with st.expander("📋 Your lineup for the Championship"):
        starters = {s: p for s, p in ss.my_lineup.items() if p}
        rows = [{"Slot": s, "Player": p, "Pos": get_player_pos(p),
                 "Wkly Proj": f"{get_player_proj(p)/17:.1f}"}
                for s, p in starters.items()]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    if st.button("🏈 Simulate Championship", type="primary"):
        t1, t2 = finalists
        if t1 == ss.your_team:
            s1, my_scores = score_lineup(ss.my_lineup)
            opp_lineup = auto_set_lineup(ss.rosters.get(t2, []))
            s2, opp_scores = score_lineup(opp_lineup)
            ss.week_player_scores = my_scores
            ss.opp_player_scores  = opp_scores
            ss.opp_team_name      = t2
        elif t2 == ss.your_team:
            opp_lineup = auto_set_lineup(ss.rosters.get(t1, []))
            s1, opp_scores = score_lineup(opp_lineup)
            s2, my_scores = score_lineup(ss.my_lineup)
            ss.week_player_scores = my_scores
            ss.opp_player_scores  = opp_scores
            ss.opp_team_name      = t1
        else:
            s1 = sim_team_score(ss.team_strengths[t1])
            s2 = sim_team_score(ss.team_strengths[t2])
        w = t1 if s1 >= s2 else t2
        ss.playoff_champ = (t1, t2, s1, s2, w)
        ss.phase = "playoff_champ_results"
        st.rerun()


# ══════════════════════════════════════════════════════════════
# PHASE: CHAMPIONSHIP RESULTS
# ══════════════════════════════════════════════════════════════
elif ss.phase == "playoff_champ_results":
    render_my_team_panel()
    t1, t2, s1, s2, champ = ss.playoff_champ
    all_teams = list(ss.rosters.keys())

    st.title("🏆 Championship Result")
    st.markdown(f"## {t1}  {s1}  –  {s2}  {t2}")
    st.markdown(f"# 🎉 {champ} wins the Championship!")

    if champ == ss.your_team:
        st.balloons()
        st.success("🥳 That's YOU! Congratulations, Champion!")
    elif ss.your_team in (t1, t2):
        st.error("Runner-up — so close!")

    if ss.week_player_scores:
        render_playoff_scorecard()

    st.divider()
    st.subheader("📊 Final Regular Season Standings")
    st.dataframe(get_standings(ss.weekly_results, all_teams), use_container_width=True, hide_index=True)

    if st.button("🔄 Start New Season"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
