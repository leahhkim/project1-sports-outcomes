-- DS 4320 Project 1
-- schema.sql
-- Relational schema for basketball game outcome project

DROP TABLE IF EXISTS team_game_stats;
DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS seasons;
DROP TABLE IF EXISTS teams;

CREATE TABLE teams (
    team_id BIGINT PRIMARY KEY,
    team_name VARCHAR NOT NULL,
    abbreviation VARCHAR,
    nickname VARCHAR,
    city VARCHAR,
    state VARCHAR,
    year_founded INTEGER
);

CREATE TABLE seasons (
    season_id INTEGER,
    season_year INTEGER NOT NULL,
    season_type VARCHAR NOT NULL,
    PRIMARY KEY (season_id, season_type)
);

CREATE TABLE games (
    game_id BIGINT PRIMARY KEY,
    game_date DATE NOT NULL,
    season_id INTEGER NOT NULL,
    season_type VARCHAR NOT NULL,
    home_team_id BIGINT NOT NULL,
    away_team_id BIGINT NOT NULL,
    home_score DOUBLE,
    away_score DOUBLE,
    winner_team_id BIGINT NOT NULL,
    FOREIGN KEY (season_id, season_type) REFERENCES seasons(season_id, season_type),
    FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (winner_team_id) REFERENCES teams(team_id)
);

CREATE TABLE team_game_stats (
    team_game_stats_id BIGINT PRIMARY KEY,
    game_id BIGINT NOT NULL,
    team_id BIGINT NOT NULL,
    fg_pct DOUBLE,
    ft_pct DOUBLE,
    fg3_pct DOUBLE,
    ast DOUBLE,
    reb DOUBLE,
    tov DOUBLE,
    pts DOUBLE,
    win_flag INTEGER NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    CHECK (win_flag IN (0, 1))
);