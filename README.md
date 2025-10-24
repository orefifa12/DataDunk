# DataDunk (College Basketball, Team-Season)

## Dataset notes
- `cbb.csv`: seasons **2013–2019** and **2021–2024** combined.
- `cbb20.csv`: **2020** season only (no postseason due to COVID). Has `RK`.
- `cbb25.csv`: **2025** in-progress snapshot (as of 2025-03-18). Has `RK`. Will be merged into `cbb.csv` after the tournament.

## Variables (selected)
- `RK` (only in 2020 and 2025), `TEAM`, `CONF`, `G`, `W`, `ADJOE`, `ADJDE`, `BARTHAG`,
  `EFG_O/EFG_D`, `TOR/TORD`, `ORB/DRB`, `FTR/FTRD`, `2P_O/2P_D`, `3P_O/3P_D`,
  `ADJ_T`, `WAB`, `POSTSEASON` (round reached), `SEED`, `YEAR`.

## Quick start
1. Create `.env` from `.env.example` and fill **Kaggle** credentials (or ensure `~/.kaggle/kaggle.json` exists).
2. Create a venv and install:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

	3.	Build SQLite DB (auto-downloads dataset; no manual download needed):

python etl.py

	4.	Run app:

python app.py

Open http://127.0.0.1:5000

Schema
	•	Conference(conf_code PK, conf_name)
	•	Team(team_id PK, team_name UNIQUE, conf_code FK)
	•	SeasonStat(team_id, year, rk?, g, w, adjoe, adjde, barthag, efg_o, efg_d, tor, tord, orb, drb, ftr, ftrd, 2p/3p splits, adj_t, wab, postseason?, seed?, PK(team_id, year))

rk is present only in 2020/2025; postseason is NULL in 2020 by design.

---

**Run commands to give the agent after creation:**
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# set .env or rely on ~/.kaggle/kaggle.json
python etl.py
python app.pyreadme
