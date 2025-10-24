import os, tempfile, zipfile, sqlite3
import pandas as pd
from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi

DB_PATH = "cbb.db"
DATASET = "andrewsundberg/college-basketball-dataset"

EXPECTED_COLS = {
    'RK','TEAM','CONF','G','W','ADJOE','ADJDE','BARTHAG',
    'EFG_O','EFG_D','TOR','TORD','ORB','DRB','FTR','FTRD',
    '2P_O','2P_D','3P_O','3P_D','ADJ_T','WAB','POSTSEASON','SEED','YEAR'
    # Note: RK may be absent in cbb.csv (present in cbb20/cbb25)
}

RENAME_MAP = {
    'RK':'rk','TEAM':'team_name','CONF':'conf_code','G':'g','W':'w',
    'ADJOE':'adjoe','ADJDE':'adjde','BARTHAG':'barthag',
    'EFG_O':'efg_o','EFG_D':'efg_d','TOR':'tor','TORD':'tord',
    'ORB':'orb','DRB':'drb','FTR':'ftr','FTRD':'ftrd',
    '2P_O':'two_p_o','2P_D':'two_p_d','3P_O':'three_p_o','3P_D':'three_p_d',
    'ADJ_T':'adj_t','WAB':'wab','POSTSEASON':'postseason','SEED':'seed','YEAR':'year'
}

def _num(v):
    if pd.isna(v): return None
    try: return float(v)
    except: 
        try: return float(str(v))
        except: return None

def _int(v):
    if pd.isna(v): return None
    try: return int(v)
    except:
        try: return int(float(v))
        except: return None

def _str(v):
    if pd.isna(v): return None
    s = str(v).strip()
    return s if s else None

def download_and_unzip():
    api = KaggleApi()
    api.authenticate()
    tmpdir = tempfile.mkdtemp(prefix="cbb_")
    api.dataset_download_files(DATASET, path=tmpdir, unzip=False, force=True)
    zips = [p for p in os.listdir(tmpdir) if p.endswith(".zip")]
    if not zips:
        raise RuntimeError("No Kaggle zip downloaded")
    zpath = os.path.join(tmpdir, zips[0])
    with zipfile.ZipFile(zpath, "r") as zf:
        zf.extractall(tmpdir)
    return tmpdir

def bootstrap_db(conn):
    with open("schema.sql","r") as f:
        conn.executescript(f.read())

def load_csv(conn, csv_path):
    df = pd.read_csv(csv_path)
    # Keep only expected columns; add missing RK/POSTSEASON/SEED gracefully
    missing = EXPECTED_COLS.difference(set(df.columns))
    for col in missing:
        df[col] = pd.NA
    # Drop rows lacking essential identifiers
    if 'TEAM' in df.columns:
        df = df[df['TEAM'].notna()]
    if 'YEAR' in df.columns:
        df = df[df['YEAR'].notna()]
    # Rename to target schema
    df = df.rename(columns=RENAME_MAP)

    # Upsert Conferences and Teams
    teams = df[['team_name','conf_code']].drop_duplicates()
    for _, r in teams.iterrows():
        team_name = _str(r['team_name'])
        conf_code = _str(r['conf_code'])
        # Ensure conference exists (fallback name = code)
        if conf_code:
            conn.execute(
                "INSERT OR IGNORE INTO Conference(conf_code, conf_name) VALUES (?,?)",
                (conf_code, conf_code)
            )
        conn.execute(
            "INSERT OR IGNORE INTO Team(team_name, conf_code) VALUES (?,?)",
            (team_name, conf_code)
        )

    # Insert season rows
    for _, r in df.iterrows():
        team_name = _str(r['team_name'])
        cur = conn.execute("SELECT team_id FROM Team WHERE team_name = ?", (team_name,))
        row = cur.fetchone()
        if not row: 
            continue
        team_id = row[0]
        conn.execute("""
            INSERT OR REPLACE INTO SeasonStat (
                team_id, year, rk, g, w, adjoe, adjde, barthag, efg_o, efg_d, tor, tord,
                orb, drb, ftr, ftrd, two_p_o, two_p_d, three_p_o, three_p_d, adj_t, wab, postseason, seed
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            team_id, _int(r['year']), _int(r['rk']), _int(r['g']), _int(r['w']),
            _num(r['adjoe']), _num(r['adjde']), _num(r['barthag']),
            _num(r['efg_o']), _num(r['efg_d']), _num(r['tor']), _num(r['tord']),
            _num(r['orb']), _num(r['drb']), _num(r['ftr']), _num(r['ftrd']),
            _num(r['two_p_o']), _num(r['two_p_d']), _num(r['three_p_o']), _num(r['three_p_d']),
            _num(r['adj_t']), _num(r['wab']), _str(r['postseason']), _int(r['seed'])
        ))

def main():
    load_dotenv()  # allow .env or ~/.kaggle/kaggle.json
    tmpdir = download_and_unzip()

    csv_candidates = []
    # Always try cbb.csv, cbb20.csv, cbb25.csv when present
    for name in ("cbb.csv","cbb20.csv","cbb25.csv"):
        p = os.path.join(tmpdir, name)
        if os.path.exists(p): csv_candidates.append(p)

    if not csv_candidates:
        raise RuntimeError("No cbb*.csv files found in the Kaggle package.")

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    try:
        bootstrap_db(conn)
        for p in csv_candidates:
            load_csv(conn, p)
        conn.commit()
        print("✅ ETL complete. SQLite DB at", DB_PATH)
        print("   Loaded files:", [os.path.basename(p) for p in csv_candidates])
    finally:
        conn.close()

if __name__ == "__main__":
    main()
