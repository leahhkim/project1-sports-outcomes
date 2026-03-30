import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Define output path
OUTPUT_PATH = Path("../press-release/home_win_rate.png")

# Load cleaned data (use CORRECT column names from your pipeline)
games = pd.read_csv(
    "../data/games.csv",
    usecols=["game_id", "game_date", "home_team_id", "away_team_id", "home_score", "away_score"]
)

teams = pd.read_csv(
    "../data/teams.csv",
    usecols=["team_id", "team_name"]
)

# Create target variable
games["home_win"] = (games["home_score"] > games["away_score"]).astype(int)

# Merge team names
games = games.merge(
    teams.rename(columns={"team_id": "home_team_id", "team_name": "home_team_name"}),
    on="home_team_id",
    how="left"
)

games = games.merge(
    teams.rename(columns={"team_id": "away_team_id", "team_name": "away_team_name"}),
    on="away_team_id",
    how="left"
)

# Compute home win rate
home_win_rate = (
    games.groupby("home_team_name")["home_win"]
    .mean()
    .reset_index()
)

top15 = home_win_rate.sort_values("home_win", ascending=False).head(15)
top15 = top15.sort_values("home_win")

# Plot
plt.figure(figsize=(10, 6))

sns.barplot(data=top15, x="home_win", y="home_team_name")

plt.title("Top 15 NBA Teams by Home Win Rate")
plt.xlabel("Home Win Rate")
plt.ylabel("Team")

plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.tight_layout()

# SAVE IMAGE HERE
plt.savefig(OUTPUT_PATH, dpi=300)

# Show plot (optional)
plt.show()

print(f"Chart saved to: {OUTPUT_PATH}")