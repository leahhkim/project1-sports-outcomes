import logging
from pathlib import Path
import pandas as pd

# Configure logging
logging.basicConfig(
    filename="data_creation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    """Create cleaned relational tables from raw NBA CSV files and save them as CSV and Parquet."""
    try:
        RAW_DIR = Path("CSV")
        OUT_DIR = Path("data")
        OUT_DIR.mkdir(exist_ok=True)

        logging.info("Starting data creation pipeline")

        # Load raw data
        team = pd.read_csv(RAW_DIR / "team.csv")
        game = pd.read_csv(RAW_DIR / "game.csv")
        logging.info("Raw CSV files loaded successfully")

        # Create teams table
        teams = team.rename(columns={
            "id": "team_id",
            "full_name": "team_name"
        })[
            ["team_id", "team_name", "abbreviation", "nickname", "city", "state", "year_founded"]
        ].drop_duplicates()
        logging.info("Teams table created")

        # Create seasons table
        seasons = game[["season_id", "season_type"]].drop_duplicates().copy()
        seasons["season_year"] = seasons["season_id"]
        seasons = seasons[["season_id", "season_year", "season_type"]]
        logging.info("Seasons table created")

        # Create games table
        games = game.rename(columns={
            "team_id_home": "home_team_id",
            "team_id_away": "away_team_id",
            "pts_home": "home_score",
            "pts_away": "away_score"
        })[
            [
                "game_id", "game_date", "season_id", "season_type",
                "home_team_id", "away_team_id", "home_score", "away_score"
            ]
        ].drop_duplicates(subset=["game_id"]).copy()

        games["winner_team_id"] = games.apply(
            lambda row: row["home_team_id"] if row["home_score"] > row["away_score"] else row["away_team_id"],
            axis=1
        )
        logging.info("Games table created")

        # Create home team game stats
        home = game[
            [
                "game_id", "team_id_home", "fg_pct_home", "ft_pct_home", "fg3_pct_home",
                "ast_home", "reb_home", "tov_home", "pts_home", "wl_home"
            ]
        ].copy()

        home = home.rename(columns={
            "team_id_home": "team_id",
            "fg_pct_home": "fg_pct",
            "ft_pct_home": "ft_pct",
            "fg3_pct_home": "fg3_pct",
            "ast_home": "ast",
            "reb_home": "reb",
            "tov_home": "tov",
            "pts_home": "pts",
            "wl_home": "wl"
        })

        # Create away team game stats
        away = game[
            [
                "game_id", "team_id_away", "fg_pct_away", "ft_pct_away", "fg3_pct_away",
                "ast_away", "reb_away", "tov_away", "pts_away", "wl_away"
            ]
        ].copy()

        away = away.rename(columns={
            "team_id_away": "team_id",
            "fg_pct_away": "fg_pct",
            "ft_pct_away": "ft_pct",
            "fg3_pct_away": "fg3_pct",
            "ast_away": "ast",
            "reb_away": "reb",
            "tov_away": "tov",
            "pts_away": "pts",
            "wl_away": "wl"
        })

        # Combine home and away stats into one table
        team_game_stats = pd.concat([home, away], ignore_index=True)

        # Remove duplicates so each team has one record per game
        team_game_stats = team_game_stats.drop_duplicates(subset=["game_id", "team_id"]).copy()

        # Convert win/loss label into binary target
        team_game_stats["win_flag"] = team_game_stats["wl"].map({"W": 1, "L": 0})

        # Add surrogate primary key
        team_game_stats.insert(0, "team_game_stats_id", range(1, len(team_game_stats) + 1))

        # Keep final columns
        team_game_stats = team_game_stats[
            ["team_game_stats_id", "game_id", "team_id", "fg_pct", "ft_pct", "fg3_pct", "ast", "reb", "tov", "pts", "win_flag"]
        ]
        logging.info("Team game stats table created")

        # Save as CSV
        teams.to_csv(OUT_DIR / "teams.csv", index=False)
        games.to_csv(OUT_DIR / "games.csv", index=False)
        seasons.to_csv(OUT_DIR / "seasons.csv", index=False)
        team_game_stats.to_csv(OUT_DIR / "team_game_stats.csv", index=False)

        # Save as Parquet
        teams.to_parquet(OUT_DIR / "teams.parquet", index=False)
        games.to_parquet(OUT_DIR / "games.parquet", index=False)
        seasons.to_parquet(OUT_DIR / "seasons.parquet", index=False)
        team_game_stats.to_parquet(OUT_DIR / "team_game_stats.parquet", index=False)

        logging.info("All tables saved as CSV and Parquet")
        print("Data creation complete.")

    except Exception as e:
        logging.exception("Data creation pipeline failed")
        print(f"Error during data creation: {e}")

if __name__ == "__main__":
    main()