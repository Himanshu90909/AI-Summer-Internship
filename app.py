"""
Sports Analytics Dashboard (Streamlit-only, no third-party charting libs)
Run with: streamlit run app.py
"""

import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Sports Analytics Dashboard",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
@st.cache_data
def load_data():
    teams = pd.read_csv("teams.csv")
    players = pd.read_csv("players.csv")
    games = pd.read_csv("games.csv", parse_dates=["date"])
    logs = pd.read_csv("player_game_logs.csv", parse_dates=["date"])
    return teams, players, games, logs


teams_df, players_df, games_df, logs_df = load_data()

# ---------------------------------------------------------------------------
# Standings helper
# ---------------------------------------------------------------------------
def compute_standings(games: pd.DataFrame, teams: pd.DataFrame) -> pd.DataFrame:
    records = {t: {"W": 0, "L": 0, "PF": 0, "PA": 0} for t in teams["team"]}
    for _, g in games.iterrows():
        h, a = g["home_team"], g["away_team"]
        hs, aw = g["home_score"], g["away_score"]
        records[h]["PF"] += hs
        records[h]["PA"] += aw
        records[a]["PF"] += aw
        records[a]["PA"] += hs
        if hs > aw:
            records[h]["W"] += 1
            records[a]["L"] += 1
        else:
            records[a]["W"] += 1
            records[h]["L"] += 1
    rows = []
    for t, r in records.items():
        gp = r["W"] + r["L"]
        rows.append({
            "team": t,
            "W": r["W"], "L": r["L"], "GP": gp,
            "Win%": round(r["W"] / gp, 3) if gp else 0.0,
            "PF": r["PF"], "PA": r["PA"],
            "Diff": r["PF"] - r["PA"],
            "PPG": round(r["PF"] / gp, 1) if gp else 0.0,
        })
    standings = pd.DataFrame(rows).merge(teams, on="team")
    return standings.sort_values(["conference", "Win%"], ascending=[True, False])


# ---------------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------------
st.sidebar.title("🏀 Filters")

min_date, max_date = games_df["date"].min(), games_df["date"].max()
date_range = st.sidebar.date_input(
    "Date range", value=(min_date.date(), max_date.date()),
    min_value=min_date.date(), max_value=max_date.date(),
)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date.date(), max_date.date()

conf_options = ["All"] + sorted(teams_df["conference"].unique().tolist())
conf_filter = st.sidebar.selectbox("Conference", conf_options)

team_pool = teams_df["team"].tolist() if conf_filter == "All" else teams_df[teams_df.conference == conf_filter]["team"].tolist()
team_filter = st.sidebar.multiselect("Teams", options=sorted(team_pool), default=sorted(team_pool))

st.sidebar.markdown("---")
st.sidebar.caption("Swap `teams.csv`, `players.csv`, `games.csv`, `player_game_logs.csv` with your own data using the same columns to plug in a real league.")

# Apply filters
mask_games = (
    (games_df["date"].dt.date >= start_date)
    & (games_df["date"].dt.date <= end_date)
    & (games_df["home_team"].isin(team_filter) | games_df["away_team"].isin(team_filter))
)
f_games = games_df[mask_games]
f_logs = logs_df[(logs_df["date"].dt.date >= start_date) & (logs_df["date"].dt.date <= end_date) & (logs_df["team"].isin(team_filter))]
f_teams = teams_df[teams_df["team"].isin(team_filter)]
f_players = players_df[players_df["team"].isin(team_filter)]

standings = compute_standings(f_games[f_games.home_team.isin(team_filter) & f_games.away_team.isin(team_filter)], f_teams) if len(f_games) else pd.DataFrame()

# ---------------------------------------------------------------------------
# Header + KPIs
# ---------------------------------------------------------------------------
st.title("🏀 Sports Analytics Dashboard")
st.caption("Synthetic league data — swap in your own CSVs to make this real. Use the sidebar to filter by date and team.")

total_games = len(f_games)
total_points = int(f_games["home_score"].sum() + f_games["away_score"].sum())
avg_margin = round((f_games["home_score"] - f_games["away_score"]).abs().mean(), 1) if total_games else 0
top_scorer = (
    f_logs.groupby("player")["points"].mean().sort_values(ascending=False).head(1)
    if len(f_logs) else pd.Series(dtype=float)
)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Games in range", f"{total_games:,}")
k2.metric("Total points scored", f"{total_points:,}")
k3.metric("Avg. margin of victory", f"{avg_margin}")
k4.metric(
    "Top scorer (PPG)",
    top_scorer.index[0] if len(top_scorer) else "—",
    f"{top_scorer.iloc[0]:.1f} pts" if len(top_scorer) else None,
)

st.markdown("---")

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab_overview, tab_teams, tab_players, tab_h2h, tab_data = st.tabs(
    ["📊 Overview", "🏟️ Team Analysis", "🧍 Player Stats", "⚔️ Head-to-Head", "🗂️ Raw Data"]
)

# --- Overview -----------------------------------------------------------
with tab_overview:
    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.subheader("Standings")
        if len(standings):
            disp = standings[["team", "conference", "city", "W", "L", "Win%", "PPG", "Diff"]].reset_index(drop=True)
            st.dataframe(
                disp.style.background_gradient(subset=["Win%"], cmap="Greens").format({"Win%": "{:.3f}"}),
                use_container_width=True, height=420,
            )
        else:
            st.info("No games in the selected filters.")

    with col2:
        st.subheader("Points For vs Against")
        if len(standings):
            scatter_df = standings.set_index("team")[["PF", "PA"]]
            st.scatter_chart(standings, x="PF", y="PA", color="conference", size="GP", height=420)
            st.caption("Teams above the diagonal (PA > PF) are outscored more than they outscore opponents.")
        else:
            st.info("No data to plot.")

    st.subheader("Scoring Trend Over Time (League Avg Points per Game)")
    if len(f_games):
        trend = f_games.copy()
        trend["total_pts"] = trend["home_score"] + trend["away_score"]
        trend = (
            trend.groupby(trend["date"].dt.to_period("W").apply(lambda p: p.start_time))["total_pts"]
            .mean()
            .rename("Avg total points / game")
        )
        st.line_chart(trend, height=350)

# --- Team Analysis --------------------------------------------------------
with tab_teams:
    if not len(f_teams):
        st.info("Select at least one team in the sidebar.")
    else:
        sel_team = st.selectbox("Choose a team", sorted(f_teams["team"].unique()))
        team_games = games_df[(games_df.home_team == sel_team) | (games_df.away_team == sel_team)]
        team_games = team_games[(team_games["date"].dt.date >= start_date) & (team_games["date"].dt.date <= end_date)]

        team_games = team_games.assign(
            team_score=np.where(team_games.home_team == sel_team, team_games.home_score, team_games.away_score),
            opp_score=np.where(team_games.home_team == sel_team, team_games.away_score, team_games.home_score),
            opponent=np.where(team_games.home_team == sel_team, team_games.away_team, team_games.home_team),
        )
        team_games["result"] = np.where(team_games.team_score > team_games.opp_score, "W", "L")
        team_games = team_games.sort_values("date")

        c1, c2, c3 = st.columns(3)
        c1.metric("Record", f"{(team_games.result=='W').sum()}-{(team_games.result=='L').sum()}")
        c2.metric("Avg points scored", round(team_games.team_score.mean(), 1) if len(team_games) else 0)
        c3.metric("Avg points allowed", round(team_games.opp_score.mean(), 1) if len(team_games) else 0)

        st.subheader(f"{sel_team} — Scoring margin by game")
        if len(team_games):
            team_games["margin"] = team_games.team_score - team_games.opp_score
            margin_series = team_games.set_index("date")["margin"]
            st.bar_chart(margin_series, height=350)
            st.caption("Positive bars = win margin, negative bars = loss margin.")

        st.subheader("Roster")
        roster = players_df[players_df.team == sel_team].sort_values("skill", ascending=False)
        agg = f_logs[f_logs.team == sel_team].groupby("player").agg(
            GP=("game_id", "nunique"), PPG=("points", "mean"), RPG=("rebounds", "mean"),
            APG=("assists", "mean"), SPG=("steals", "mean"), BPG=("blocks", "mean"),
        ).round(1).reset_index()
        roster = roster.merge(agg, on="player", how="left")
        st.dataframe(roster[["player", "position", "age", "GP", "PPG", "RPG", "APG", "SPG", "BPG"]],
                     use_container_width=True, height=350)

# --- Player Stats -----------------------------------------------------------
with tab_players:
    st.subheader("League Leaders")
    if len(f_logs):
        stat_choice = st.radio("Rank by", ["points", "rebounds", "assists", "steals", "blocks"], horizontal=True)
        leaders = f_logs.groupby("player")[stat_choice].mean().round(1).sort_values(ascending=False).head(15)
        st.bar_chart(leaders, height=500, horizontal=True)

        st.subheader("Player Comparison")
        players_avail = sorted(f_logs["player"].unique())
        default_pair = players_avail[:3] if len(players_avail) >= 3 else players_avail
        compare = st.multiselect("Pick 2–5 players", players_avail, default=default_pair, max_selections=5)
        if len(compare) >= 2:
            radar_stats = ["points", "rebounds", "assists", "steals", "blocks"]
            comp_df = f_logs[f_logs.player.isin(compare)].groupby("player")[radar_stats].mean().round(1)
            st.caption("Average per-game stats side by side (grouped bars):")
            st.bar_chart(comp_df.T, height=400)
            st.dataframe(comp_df, use_container_width=True)
        else:
            st.caption("Pick at least 2 players to compare.")
    else:
        st.info("No player logs in the selected filters.")

# --- Head-to-Head -----------------------------------------------------------
with tab_h2h:
    st.subheader("Team Head-to-Head")
    colA, colB = st.columns(2)
    team_a = colA.selectbox("Team A", sorted(teams_df["team"].unique()), index=0)
    team_b = colB.selectbox("Team B", sorted(teams_df["team"].unique()), index=1)

    if team_a == team_b:
        st.warning("Pick two different teams.")
    else:
        h2h = games_df[
            ((games_df.home_team == team_a) & (games_df.away_team == team_b))
            | ((games_df.home_team == team_b) & (games_df.away_team == team_a))
        ]
        if not len(h2h):
            st.info(f"{team_a} and {team_b} haven't played this season.")
        else:
            a_wins = (h2h.winner == team_a).sum()
            b_wins = (h2h.winner == team_b).sum()
            c1, c2 = st.columns(2)
            c1.metric(f"{team_a} wins", a_wins)
            c2.metric(f"{team_b} wins", b_wins)

            win_counts = pd.Series({team_a: a_wins, team_b: b_wins}, name="Wins")
            st.bar_chart(win_counts, height=300)

            h2h_disp = h2h[["date", "home_team", "home_score", "away_team", "away_score", "winner"]].sort_values("date")
            st.dataframe(h2h_disp, use_container_width=True)

# --- Raw Data -----------------------------------------------------------
with tab_data:
    st.subheader("Underlying tables (filtered)")
    st.markdown("**Games**")
    st.dataframe(f_games, use_container_width=True, height=250)
    st.markdown("**Player Game Logs**")
    st.dataframe(f_logs, use_container_width=True, height=250)
    st.download_button("Download filtered games CSV", f_games.to_csv(index=False), "games_filtered.csv")
    st.download_button("Download filtered logs CSV", f_logs.to_csv(index=False), "logs_filtered.csv")
