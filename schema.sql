PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS SeasonStat;
DROP TABLE IF EXISTS Team;
DROP TABLE IF EXISTS Conference;

CREATE TABLE Conference (
  conf_code TEXT PRIMARY KEY,
  conf_name TEXT
);

CREATE TABLE Team (
  team_id   INTEGER PRIMARY KEY AUTOINCREMENT,
  team_name TEXT UNIQUE NOT NULL,
  conf_code TEXT REFERENCES Conference(conf_code)
);

CREATE TABLE SeasonStat (
  team_id    INTEGER NOT NULL REFERENCES Team(team_id),
  year       INTEGER NOT NULL,
  rk         INTEGER,              -- present only in cbb20 and cbb25
  g          INTEGER,
  w          INTEGER,
  adjoe      REAL,
  adjde      REAL,
  barthag    REAL,
  efg_o      REAL,
  efg_d      REAL,
  tor        REAL,
  tord       REAL,
  orb        REAL,
  drb        REAL,
  ftr        REAL,
  ftrd       REAL,
  two_p_o    REAL,
  two_p_d    REAL,
  three_p_o  REAL,
  three_p_d  REAL,
  adj_t      REAL,
  wab        REAL,
  postseason TEXT,                  -- NULL for 2020
  seed       INTEGER,               -- NULL where missing
  PRIMARY KEY (team_id, year)
);

-- Optional initial conference name seeds (expand as needed)
INSERT OR IGNORE INTO Conference(conf_code, conf_name) VALUES
('ACC','Atlantic Coast Conference'),('B10','Big Ten'),('B12','Big 12'),('BE','Big East'),
('SEC','Southeastern Conference'),('P12','Pac-12'),('MWC','Mountain West'),('A10','Atlantic 10'),
('WCC','West Coast Conference'),('MVC','Missouri Valley Conference'),('SB','Sun Belt'),
('ASun','ASUN'),('BW','Big West'),('CAA','Colonial Athletic Association'),
('CUSA','Conference USA'),('Horz','Horizon League'),('Ivy','Ivy League'),('MAAC','Metro Atlantic'),
('MAC','Mid-American Conference'),('MEAC','Mid-Eastern Athletic Conference'),
('NEC','Northeast Conference'),('OVC','Ohio Valley Conference'),('Pat','Patriot League'),
('SC','Southern Conference'),('Slnd','Southland Conference'),('Sum','Summit League'),
('SWAC','Southwestern Athletic Conference'),('WAC','Western Athletic Conference'),('BSky','Big Sky'),
('BSth','Big South');
