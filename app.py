import sqlite3
from flask import Flask, request, render_template_string, jsonify

DB_PATH = "cbb.db"
app = Flask(__name__)

HTML = """
<!doctype html>
<html>
<head>
  <title>DataDunk — College Basketball</title>
  <style>
    body { font-family: system-ui, Arial, sans-serif; margin: 24px; }
    table { border-collapse: collapse; margin-top: 12px; }
    th, td { border: 1px solid #ccc; padding: 6px 10px; }
    form { margin-bottom: 12px; }
    .card { border: 1px solid #ddd; padding: 12px; border-radius: 6px; margin-bottom: 16px; }
    .title { font-weight: 600; }
    .note { color: #555; margin: 8px 0 16px; }
  </style>
  
</head>
<body>
  <h1>DataDunk — College Basketball Explorer</h1>
  <p class="note">Valid seasons for queries: <strong>2013–2024</strong>.</p>

  <div class="card">
    <div class="title">Top ADJOE (Offensive Efficiency) by Season</div>
    <form method="get">
      <input type="number" name="year1" value="{{year1 or ''}}" placeholder="e.g. 2024">
      <button>Run</button>
    </form>
    {% if top_off %}
    <table><tr><th>Team</th><th>Year</th><th>ADJOE</th></tr>
    {% for r in top_off %}<tr><td>{{r.team_name}}</td><td>{{r.year}}</td><td>{{"%.3f"|format(r.adjoe) if r.adjoe else ""}}</td></tr>{% endfor %}
    </table>{% endif %}
  </div>

  <div class="card">
    <div class="title">Avg BARTHAG by Conference (Season)</div>
    <form method="get">
      <input type="number" name="year2" value="{{year2 or ''}}" placeholder="e.g. 2024">
      <button>Run</button>
    </form>
    {% if conf_power %}
    <table><tr><th>Conference</th><th>Avg BARTHAG</th></tr>
    {% for r in conf_power %}<tr><td>{{r.conf_code}}</td><td>{{"%.3f"|format(r.avg_barthag) if r.avg_barthag else ""}}</td></tr>{% endfor %}
    </table>{% endif %}
  </div>

  <div class="card">
    <div class="title">Biggest YoY Win Improvement (Base Year → Next Year)</div>
    <form method="get">
      <input type="number" name="base" value="{{base or ''}}" placeholder="e.g. 2023">
      <button>Run</button>
    </form>
    {% if yoy %}
    <table><tr><th>Team</th><th>Base Year</th><th>Next Year</th><th>Δ Wins</th></tr>
    {% for r in yoy %}<tr><td>{{r.team_name}}</td><td>{{r.year}}</td><td>{{r.year+1}}</td><td>{{r.delta_w}}</td></tr>{% endfor %}
    </table>{% endif %}
  </div>

  <!-- New Query 4: Top ADJDE (lower is better) via API -->
  <div class="card">
    <div class="title">Top ADJDE (Defensive Efficiency, lower is better) by Season</div>
    <form id="form-adjde">
      <input type="number" id="year-adjde" placeholder="e.g. 2024">
      <button>Run</button>
    </form>
    <table id="tbl-adjde" style="display:none"><tr><th>Team</th><th>Year</th><th>ADJDE</th></tr><tbody></tbody></table>
  </div>

  <!-- New Query 5: Top Tempo (ADJ_T) via API -->
  <div class="card">
    <div class="title">Top Tempo (ADJ_T) by Season</div>
    <form id="form-tempo">
      <input type="number" id="year-tempo" placeholder="e.g. 2024">
      <button>Run</button>
    </form>
    <table id="tbl-tempo" style="display:none"><tr><th>Team</th><th>Year</th><th>ADJ_T</th></tr><tbody></tbody></table>
  </div>

  <script>
    async function runAdjde(e){
      e.preventDefault();
      const y = document.getElementById('year-adjde').value;
      const res = await fetch('/api/top_adjde?year=' + encodeURIComponent(y));
      const data = await res.json();
      const tbl = document.getElementById('tbl-adjde');
      const tb = tbl.querySelector('tbody');
      tb.innerHTML = '';
      (data.rows||[]).forEach(r => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${r.team_name}</td><td>${r.year}</td><td>${r.adjde?.toFixed(3) ?? ''}</td>`;
        tb.appendChild(tr);
      });
      tbl.style.display = (data.rows && data.rows.length) ? '' : 'none';
    }
    async function runTempo(e){
      e.preventDefault();
      const y = document.getElementById('year-tempo').value;
      const res = await fetch('/api/top_tempo?year=' + encodeURIComponent(y));
      const data = await res.json();
      const tbl = document.getElementById('tbl-tempo');
      const tb = tbl.querySelector('tbody');
      tb.innerHTML = '';
      (data.rows||[]).forEach(r => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${r.team_name}</td><td>${r.year}</td><td>${r.adj_t?.toFixed(3) ?? ''}</td>`;
        tb.appendChild(tr);
      });
      tbl.style.display = (data.rows && data.rows.length) ? '' : 'none';
    }
    document.getElementById('form-adjde').addEventListener('submit', runAdjde);
    document.getElementById('form-tempo').addEventListener('submit', runTempo);
  </script>
</body>
</html>
"""

def rows(cur):
    cols = [c[0] for c in cur.description]
    return [type("R", (), dict(zip(cols, row))) for row in cur.fetchall()]

@app.route("/", methods=["GET"])
def home():
  year1 = request.args.get("year1", type=int)
  year2 = request.args.get("year2", type=int)
  base = request.args.get("base", type=int)

  top_off = conf_power = yoy = None

  with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()

    if year1:
      cur.execute(
        """
        SELECT t.team_name, s.year, s.adjoe
        FROM SeasonStat s
        JOIN Team t ON t.team_id = s.team_id
        WHERE s.year = ?
        ORDER BY (s.adjoe IS NULL), s.adjoe DESC
        LIMIT 15;
        """,
        (year1,),
      )
      top_off = rows(cur)

    if year2:
      cur.execute(
        """
        SELECT t.conf_code, AVG(s.barthag) AS avg_barthag
        FROM SeasonStat s
        JOIN Team t ON t.team_id = s.team_id
        WHERE s.year = ?
        GROUP BY t.conf_code
        ORDER BY (avg_barthag IS NULL), avg_barthag DESC;
        """,
        (year2,),
      )
      conf_power = rows(cur)

    if base:
      cur.execute(
        """
        SELECT t.team_name, s1.year, (s2.w - s1.w) AS delta_w
        FROM SeasonStat s1
        JOIN SeasonStat s2
          ON s1.team_id = s2.team_id
         AND s2.year = s1.year + 1
        JOIN Team t ON t.team_id = s1.team_id
        WHERE s1.year = ?
        ORDER BY delta_w DESC
        LIMIT 15;
        """,
        (base,),
      )
      yoy = rows(cur)

  return render_template_string(
    HTML, year1=year1, top_off=top_off, year2=year2, conf_power=conf_power, base=base, yoy=yoy
  )

# --------------------- API endpoints (JSON) ---------------------

def _json_rows(cur):
  cols = [c[0] for c in cur.description]
  return [dict(zip(cols, row)) for row in cur.fetchall()]

@app.get("/api/top_adjoe")
def api_top_adjoe():
  year = request.args.get("year", type=int)
  if not year:
    return jsonify({"error":"year required"}), 400
  with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()
    cur.execute(
      """
      SELECT t.team_name, s.year, s.adjoe
      FROM SeasonStat s
      JOIN Team t ON t.team_id = s.team_id
      WHERE s.year = ?
      ORDER BY (s.adjoe IS NULL), s.adjoe DESC
      LIMIT 15;
      """,
      (year,),
    )
    return jsonify({"rows": _json_rows(cur)})

@app.get("/api/avg_barthag_by_conf")
def api_avg_barthag_by_conf():
  year = request.args.get("year", type=int)
  if not year:
    return jsonify({"error":"year required"}), 400
  with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()
    cur.execute(
      """
      SELECT t.conf_code, AVG(s.barthag) AS avg_barthag
      FROM SeasonStat s
      JOIN Team t ON t.team_id = s.team_id
      WHERE s.year = ?
      GROUP BY t.conf_code
      ORDER BY (avg_barthag IS NULL), avg_barthag DESC;
      """,
      (year,),
    )
    return jsonify({"rows": _json_rows(cur)})

@app.get("/api/yoy_win_improvement")
def api_yoy_win_improvement():
  base = request.args.get("base", type=int)
  if not base:
    return jsonify({"error":"base year required"}), 400
  with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()
    cur.execute(
      """
      SELECT t.team_name, s1.year, (s2.w - s1.w) AS delta_w
      FROM SeasonStat s1
      JOIN SeasonStat s2
        ON s1.team_id = s2.team_id
       AND s2.year = s1.year + 1
      JOIN Team t ON t.team_id = s1.team_id
      WHERE s1.year = ?
      ORDER BY delta_w DESC
      LIMIT 15;
      """,
      (base,),
    )
    return jsonify({"rows": _json_rows(cur)})

@app.get("/api/top_adjde")
def api_top_adjde():
  year = request.args.get("year", type=int)
  if not year:
    return jsonify({"error":"year required"}), 400
  with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()
    cur.execute(
      """
      SELECT t.team_name, s.year, s.adjde
      FROM SeasonStat s
      JOIN Team t ON t.team_id = s.team_id
      WHERE s.year = ?
      ORDER BY (s.adjde IS NULL), s.adjde ASC
      LIMIT 15;
      """,
      (year,),
    )
    return jsonify({"rows": _json_rows(cur)})

@app.get("/api/top_tempo")
def api_top_tempo():
  year = request.args.get("year", type=int)
  if not year:
    return jsonify({"error":"year required"}), 400
  with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()
    cur.execute(
      """
      SELECT t.team_name, s.year, s.adj_t
      FROM SeasonStat s
      JOIN Team t ON t.team_id = s.team_id
      WHERE s.year = ?
      ORDER BY (s.adj_t IS NULL), s.adj_t DESC
      LIMIT 15;
      """,
      (year,),
    )
    return jsonify({"rows": _json_rows(cur)})

if __name__ == "__main__":
    app.run(debug=True)
