
import random
import sqlite3
import time
import html
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ROLLS • Game", page_icon="🎲", layout="wide")

DB_PATH = Path(__file__).with_name("rolls_game.db")
ADMIN_CODE = "admin123"
ROLL_COST = 100
MAX_LUCK_PERCENT = 1_000_000

ITEMS = [
    {"name": "Roblox", "odds": 2, "rarity": "Common", "animation": "no", "emoji": "🟥"},
    {"name": "Enrique", "odds": 4, "rarity": "Common", "animation": "no", "emoji": "🎵"},
    {"name": "Unknown 1", "odds": 8, "rarity": "Common", "animation": "no", "emoji": "⚪"},
    {"name": "Unknown 2", "odds": 16, "rarity": "Common", "animation": "no", "emoji": "🔹"},
    {"name": "Unknown 3", "odds": 32, "rarity": "Common", "animation": "no", "emoji": "🔸"},
    {"name": "Unknown 4", "odds": 64, "rarity": "Common", "animation": "no", "emoji": "🟢"},
    {"name": "Unknown 5", "odds": 128, "rarity": "Uncommon", "animation": "no", "emoji": "🟩"},
    {"name": "Unknown 6", "odds": 264, "rarity": "Uncommon", "animation": "yes", "emoji": "💠"},
    {"name": "Unknown 7", "odds": 528, "rarity": "Uncommon", "animation": "yes", "emoji": "🔷"},
    {"name": "Unknown 8", "odds": 1048, "rarity": "Rare", "animation": "yes", "emoji": "💎"},
    {"name": "Unknown 9", "odds": 2500, "rarity": "Rare", "animation": "yes", "emoji": "🌠"},
    {"name": "Unknown 10", "odds": 5000, "rarity": "Rare", "animation": "yes", "emoji": "🌀"},
    {"name": "Unknown 11", "odds": 10000, "rarity": "Rare", "animation": "yes", "emoji": "⚡"},
    {"name": "Unknown 12", "odds": 25000, "rarity": "Legendary", "animation": "super", "emoji": "👑"},
    {"name": "Unknown 13", "odds": 50000, "rarity": "Legendary", "animation": "super", "emoji": "🔥"},
    {"name": "Unknown 14", "odds": 100000, "rarity": "Legendary", "animation": "super", "emoji": "☄️"},
    {"name": "Blackhole", "odds": 250000, "rarity": "Mythical", "animation": "super", "emoji": "🌌"},
    {"name": "Unknown 15", "odds": 500000, "rarity": "Mythical", "animation": "super", "emoji": "🪐"},
    {"name": "Unknown 16", "odds": 1000000, "rarity": "Mythical", "animation": "supersuper", "emoji": "🌑"},
]

RARITY_COLORS = {
    "Common": "#9ca3af",
    "Uncommon": "#34d399",
    "Rare": "#60a5fa",
    "Legendary": "#fbbf24",
    "Mythical": "#e879f9",
}


def db_connect():
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    with db_connect() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS players (
                username TEXT PRIMARY KEY,
                money REAL NOT NULL DEFAULT 1000,
                luck REAL NOT NULL DEFAULT 0,
                infinite_money INTEGER NOT NULL DEFAULT 0,
                inventory TEXT NOT NULL DEFAULT ''
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS rolls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                item_name TEXT NOT NULL,
                odds INTEGER NOT NULL,
                rarity TEXT NOT NULL,
                rolled_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


def clean_username(value):
    value = "".join(
        ch for ch in value.strip()
        if ch.isalnum() or ch in "_- "
    )
    return value[:24].strip()


def ensure_player(username):
    with db_connect() as con:
        con.execute(
            "INSERT OR IGNORE INTO players(username, money) VALUES (?, 1000)",
            (username,)
        )


def get_player(username):
    with db_connect() as con:
        row = con.execute(
            "SELECT * FROM players WHERE username = ?",
            (username,)
        ).fetchone()
    return dict(row) if row else None


def update_player(username, **fields):
    allowed = {"money", "luck", "infinite_money", "inventory"}
    fields = {k: v for k, v in fields.items() if k in allowed}

    if not fields:
        return

    assignments = ", ".join(f"{key} = ?" for key in fields)
    values = list(fields.values()) + [username]

    with db_connect() as con:
        con.execute(
            f"UPDATE players SET {assignments} WHERE username = ?",
            values
        )


def all_players():
    with db_connect() as con:
        rows = con.execute(
            "SELECT username, money, luck, infinite_money "
            "FROM players ORDER BY username"
        ).fetchall()
    return [dict(row) for row in rows]


def add_inventory_item(username, item_name):
    player = get_player(username)
    inventory = [
        x for x in (player["inventory"] or "").split("|") if x
    ]
    inventory.append(item_name)
    update_player(username, inventory="|".join(inventory))


def save_roll(username, item):
    with db_connect() as con:
        con.execute(
            "INSERT INTO rolls(username, item_name, odds, rarity) "
            "VALUES (?, ?, ?, ?)",
            (username, item["name"], item["odds"], item["rarity"])
        )


def recent_rolls(username, limit=20):
    with db_connect() as con:
        rows = con.execute(
            "SELECT item_name, odds, rarity, rolled_at FROM rolls "
            "WHERE username = ? ORDER BY id DESC LIMIT ?",
            (username, limit)
        ).fetchall()
    return [dict(row) for row in rows]


def roll_item(luck_percent):
    multiplier = 1 + max(
        0, min(float(luck_percent), MAX_LUCK_PERCENT)
    ) / 100

    rarest_first = sorted(
        ITEMS, key=lambda item: item["odds"], reverse=True
    )

    for item in rarest_first:
        denominator = max(1, int(item["odds"] / multiplier))
        if random.randint(1, denominator) == 1:
            return item

    common = [
        item for item in ITEMS if item["rarity"] == "Common"
    ]
    return random.choice(common)


def show_reveal(item):
    """Cinematic aura roll met bewegende particles en een reveal."""
    rarity = item["rarity"]
    color = RARITY_COLORS.get(rarity, "#ffffff")

    safe_name = html.escape(item["name"])
    safe_rarity = html.escape(rarity.upper())
    emoji = html.escape(item["emoji"])
    odds = f"1 IN {item['odds']:,}"

    duration_ms = {
        "no": 4200,
        "yes": 5200,
        "super": 6500,
        "supersuper": 8200,
    }.get(item["animation"], 4200)

    cycling_names = [
        "Unknown", "Solar", "Starlight", "Voltage",
        "Celestial", "Eclipse", "Genesis", "Astral",
        "Cosmic", "Void"
    ]

    cycling_json = json.dumps(cycling_names)
    final_json = json.dumps({
        "name": item["name"],
        "rarity": rarity.upper(),
        "emoji": item["emoji"],
        "odds": odds,
        "color": color,
    }, ensure_ascii=False)

    components.html(f"""
    <div id="rng-root" class="rng-root" style="--glow:{color}">
      <canvas id="particle-canvas"></canvas>

      <div class="topline">
        <span class="live-dot"></span>
        ROLLING SYSTEM <span class="top-sep">/</span> AURA DISCOVERY
      </div>

      <div class="scene" id="scene">
        <div class="ambient ambient-a"></div>
        <div class="ambient ambient-b"></div>
        <div class="orbit orbit-one"></div>
        <div class="orbit orbit-two"></div>
        <div class="orbit orbit-three"></div>

        <div class="rune rune-one">✦</div>
        <div class="rune rune-two">✧</div>

        <div class="core-wrap">
          <div class="core-halo"></div>
          <div class="core-ring"></div>
          <div class="core" id="core">
            <span id="rolling-emoji">✦</span>
          </div>
        </div>

        <div class="energy-line line-one"></div>
        <div class="energy-line line-two"></div>

        <div class="roll-label" id="roll-label">
          INITIALIZING AURA...
        </div>

        <div class="rolling-name" id="rolling-name">UNKNOWN</div>

        <div class="meter">
          <div id="meter-fill"></div>
        </div>

        <div class="roll-sub" id="roll-sub">
          SCANNING POSSIBILITIES
        </div>

        <div class="final-card" id="final-card">
          <div class="final-kicker">✦ AURA DISCOVERED ✦</div>
          <div class="final-emoji" id="final-emoji">{emoji}</div>
          <div class="final-rarity" id="final-rarity">{safe_rarity}</div>
          <div class="final-name" id="final-name">{safe_name}</div>
          <div class="final-odds" id="final-odds">{odds}</div>
          <div class="final-stamp">ROLL COMPLETE</div>
        </div>

        <div class="flash" id="flash"></div>
      </div>

      <div class="bottomline">
        <span>RNG ENGINE</span>
        <span class="bottom-progress"><i id="bottom-progress"></i></span>
        <span id="percent">0%</span>
      </div>
    </div>

    <style>
      * {{ box-sizing: border-box; }}

      html, body {{
        margin: 0;
        padding: 0;
        background: transparent;
        color: #fff;
        font-family: Inter, system-ui, sans-serif;
      }}

      .rng-root {{
        height: 500px;
        position: relative;
        overflow: hidden;
        border: 1px solid #383052;
        border-radius: 22px;
        background: radial-gradient(
          ellipse at 50% 46%, #1a1530 0%, #0b0a16 48%, #05050b 100%
        );
        isolation: isolate;
        box-shadow: 0 18px 55px #0008, inset 0 0 70px #0009;
      }}

      #particle-canvas {{
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        z-index: 1;
        pointer-events: none;
      }}

      .topline, .bottomline {{
        position: absolute;
        left: 22px;
        right: 22px;
        display: flex;
        align-items: center;
        gap: 10px;
        z-index: 5;
        color: #9994b8;
        font-size: 9px;
        font-weight: 900;
        letter-spacing: 2px;
      }}

      .topline {{ top: 18px; }}
      .bottomline {{ bottom: 17px; }}

      .live-dot {{
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #67e8f9;
        box-shadow: 0 0 12px #67e8f9;
        animation: blink .8s infinite;
      }}

      .top-sep {{ color: #4b4565; }}

      .scene {{
        position: absolute;
        inset: 42px 0;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        overflow: hidden;
      }}

      .ambient {{
        position: absolute;
        width: 240px;
        height: 240px;
        border-radius: 50%;
        filter: blur(45px);
        opacity: .2;
        background: var(--glow);
        transition: background .3s, opacity .3s;
      }}

      .ambient-a {{
        animation: ambientPulse 2.4s ease-in-out infinite;
      }}

      .ambient-b {{
        width: 150px;
        height: 150px;
        opacity: .12;
        transform: translate(110px, 55px);
        background: #60a5fa;
        animation: ambientPulse 3s ease-in-out infinite reverse;
      }}

      .orbit {{
        position: absolute;
        border: 1px solid var(--glow);
        border-radius: 50%;
        width: 190px;
        height: 190px;
        opacity: .65;
        transition: border-color .3s;
      }}

      .orbit-one {{
        animation: orbitA 7s linear infinite;
      }}

      .orbit-two {{
        width: 245px;
        height: 95px;
        transform: rotate(48deg);
        border-style: dashed;
        animation: orbitB 5s linear infinite;
      }}

      .orbit-three {{
        width: 260px;
        height: 260px;
        border-color: #ffffff18;
        border-left-color: var(--glow);
        border-right-color: var(--glow);
        animation: orbitA 10s linear infinite reverse;
      }}

      .core-wrap {{
        position: absolute;
        top: 42px;
        width: 126px;
        height: 126px;
        display: grid;
        place-items: center;
        transition: all .5s;
      }}

      .core-halo {{
        position: absolute;
        inset: -24px;
        border-radius: 50%;
        background: var(--glow);
        filter: blur(24px);
        opacity: .28;
        animation: halo 1.2s ease-in-out infinite alternate;
      }}

      .core-ring {{
        position: absolute;
        inset: -9px;
        border-radius: 50%;
        border: 2px solid var(--glow);
        box-shadow: 0 0 25px var(--glow), inset 0 0 20px var(--glow);
        animation: orbitA 3s linear infinite;
      }}

      .core {{
        position: relative;
        width: 100px;
        height: 100px;
        border-radius: 50%;
        display: grid;
        place-items: center;
        font-size: 43px;
        background: radial-gradient(circle at 32% 25%, #fff8, var(--glow) 26%, #090811 76%);
        border: 1px solid #ffffffa0;
        box-shadow: 0 0 30px var(--glow), inset 0 0 28px #fff2;
        animation: coreBeat .7s ease-in-out infinite alternate;
      }}

      #rolling-emoji {{
        filter: drop-shadow(0 0 12px var(--glow));
        transition: transform .15s;
      }}

      .rune {{
        position: absolute;
        color: var(--glow);
        font-size: 25px;
        text-shadow: 0 0 20px var(--glow);
        opacity: .8;
      }}

      .rune-one {{
        top: 64px;
        left: calc(50% - 125px);
        animation: floatRune 2s ease-in-out infinite;
      }}

      .rune-two {{
        top: 120px;
        right: calc(50% - 130px);
        animation: floatRune 2.5s ease-in-out infinite reverse;
      }}

      .energy-line {{
        position: absolute;
        width: 180%;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--glow), #fff, transparent);
        opacity: 0;
        box-shadow: 0 0 12px var(--glow);
      }}

      .line-one {{
        transform: rotate(25deg);
        animation: energy 2.2s ease-in-out infinite;
      }}

      .line-two {{
        transform: rotate(-25deg);
        animation: energy 2.2s .7s ease-in-out infinite;
      }}

      .roll-label {{
        position: absolute;
        top: 205px;
        color: #c4b5fd;
        font-size: 9px;
        font-weight: 1000;
        letter-spacing: 4px;
        text-align: center;
      }}

      .rolling-name {{
        position: absolute;
        top: 225px;
        max-width: 90%;
        font-size: clamp(20px, 4vw, 32px);
        font-weight: 1000;
        letter-spacing: 2px;
        text-align: center;
        text-shadow: 0 0 20px var(--glow);
        animation: nameFlicker .13s linear infinite;
      }}

      .meter {{
        position: absolute;
        top: 274px;
        width: min(280px, 72%);
        height: 4px;
        background: #ffffff16;
        border-radius: 10px;
        overflow: hidden;
      }}

      #meter-fill {{
        height: 100%;
        width: 0;
        background: linear-gradient(90deg, #8b5cf6, #67e8f9, #fff);
        box-shadow: 0 0 14px #a78bfa;
        transition: width .12s linear;
      }}

      .roll-sub {{
        position: absolute;
        top: 290px;
        color: #77718f;
        font-size: 8px;
        font-weight: 900;
        letter-spacing: 3px;
      }}

      .final-card {{
        position: absolute;
        inset: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        text-align: center;
        opacity: 0;
        transform: scale(.75);
        pointer-events: none;
        z-index: 4;
        padding: 25px;
        transition: opacity .45s, transform .55s cubic-bezier(.2, 1.5, .4, 1);
      }}

      .final-card.show {{
        opacity: 1;
        transform: scale(1);
      }}

      .final-kicker {{
        color: var(--glow);
        font-size: 10px;
        font-weight: 1000;
        letter-spacing: 4px;
        text-shadow: 0 0 18px var(--glow);
      }}

      .final-emoji {{
        font-size: 72px;
        line-height: 1.1;
        margin: 9px 0;
        filter: drop-shadow(0 0 20px var(--glow));
        animation: finalFloat 1.8s ease-in-out infinite;
      }}

      .final-rarity {{
        font-size: 10px;
        letter-spacing: 5px;
        font-weight: 1000;
        color: var(--glow);
        margin-top: 3px;
      }}

      .final-name {{
        font-size: clamp(27px, 5vw, 44px);
        font-weight: 1000;
        line-height: 1.15;
        margin-top: 8px;
        text-shadow: 0 0 12px var(--glow), 0 0 35px var(--glow);
        overflow-wrap: anywhere;
      }}

      .final-odds {{
        margin-top: 12px;
        font-size: 15px;
        font-weight: 900;
        letter-spacing: 3px;
        color: #e9e7ff;
      }}

      .final-stamp {{
        margin-top: 15px;
        padding: 7px 13px;
        border: 1px solid var(--glow);
        border-radius: 999px;
        font-size: 8px;
        letter-spacing: 3px;
        color: #c4b5d5;
        background: #ffffff08;
      }}

      .flash {{
        position: absolute;
        inset: 0;
        background: #fff;
        opacity: 0;
        pointer-events: none;
        z-index: 6;
      }}

      .bottomline {{ gap: 12px; }}

      .bottom-progress {{
        height: 3px;
        flex: 1;
        background: #ffffff12;
        border-radius: 10px;
        overflow: hidden;
      }}

      #bottom-progress {{
        display: block;
        width: 0;
        height: 100%;
        background: linear-gradient(90deg, #8b5cf6, #67e8f9);
        box-shadow: 0 0 10px #67e8f9;
      }}

      #percent {{
        width: 28px;
        text-align: right;
      }}

      .rng-root.revealed .core-wrap,
      .rng-root.revealed .orbit,
      .rng-root.revealed .rune,
      .rng-root.revealed .energy-line,
      .rng-root.revealed .roll-label,
      .rng-root.revealed .rolling-name,
      .rng-root.revealed .meter,
      .rng-root.revealed .roll-sub {{
        opacity: 0;
        transform: scale(.6);
        transition: opacity .3s, transform .3s;
      }}

      .rng-root.revealed .ambient {{ opacity: .35; }}

      @keyframes orbitA {{ to {{ transform: rotate(360deg); }} }}
      @keyframes orbitB {{ to {{ transform: rotate(408deg); }} }}
      @keyframes halo {{ to {{ transform: scale(1.35); opacity: .48; }} }}
      @keyframes coreBeat {{ to {{ transform: scale(1.08) rotate(3deg); }} }}
      @keyframes ambientPulse {{ to {{ transform: scale(1.35); opacity: .32; }} }}
      @keyframes floatRune {{ 50% {{ transform: translateY(-13px) rotate(18deg); }} }}

      @keyframes energy {{
        0%, 100% {{ opacity: 0; transform: scaleX(.2) rotate(25deg); }}
        45% {{ opacity: .65; transform: scaleX(1) rotate(25deg); }}
      }}

      @keyframes nameFlicker {{ 50% {{ opacity: .55; filter: blur(.4px); }} }}
      @keyframes blink {{ 50% {{ opacity: .3; }} }}
      @keyframes finalFloat {{ 50% {{ transform: translateY(-8px) scale(1.05); }} }}

      @media(max-width:500px) {{
        .rng-root {{ height: 470px; }}
        .orbit-three {{ width: 210px; height: 210px; }}
        .topline, .bottomline {{ left: 12px; right: 12px; letter-spacing: 1px; }}
      }}
    </style>

    <script>
      (() => {{
        const root = document.getElementById('rng-root');
        if (!root) return;

        const final = {final_json};
        const names = {cycling_json};
        const total = {duration_ms};
        const start = performance.now();

        const scene = document.getElementById('scene');
        const nameEl = document.getElementById('rolling-name');
        const emojiEl = document.getElementById('rolling-emoji');
        const meter = document.getElementById('meter-fill');
        const bottom = document.getElementById('bottom-progress');
        const percent = document.getElementById('percent');
        const label = document.getElementById('roll-label');
        const sub = document.getElementById('roll-sub');
        const canvas = document.getElementById('particle-canvas');
        const ctx = canvas.getContext('2d');

        let w = 0, h = 0, particles = [];

        function resize() {{
          const rect = root.getBoundingClientRect();
          w = rect.width;
          h = rect.height;

          canvas.width = Math.floor(w * devicePixelRatio);
          canvas.height = Math.floor(h * devicePixelRatio);
          ctx.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0);

          particles = Array.from({{length: 95}}, () => ({{
            x: Math.random() * w,
            y: Math.random() * h,
            vx: (Math.random() - .5) * .7,
            vy: (Math.random() - .5) * .7,
            size: Math.random() * 2 + .4,
            alpha: Math.random() * .8 + .15
          }}));
        }}

        resize();
        window.addEventListener('resize', resize);

        function draw() {{
          ctx.clearRect(0, 0, w, h);

          for (const p of particles) {{
            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0) p.x = w;
            if (p.x > w) p.x = 0;
            if (p.y < 0) p.y = h;
            if (p.y > h) p.y = 0;

            ctx.globalAlpha = p.alpha;
            ctx.fillStyle = Math.random() > .94 ? '#ffffff' : final.color;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
          }}

          ctx.globalAlpha = 1;

          if (!root.classList.contains('finished')) {{
            requestAnimationFrame(draw);
          }}
        }}

        draw();

        let cycle = 0;

        const ticker = setInterval(() => {{
          if (root.classList.contains('finished')) return;

          cycle++;
          nameEl.textContent =
            names[Math.floor(Math.random() * names.length)].toUpperCase();

          emojiEl.textContent =
            ['✦', '✧', '◇', '✺', '☄', '✹'][cycle % 6];

          const hue = (cycle * 47) % 360;
          root.style.setProperty('--glow', `hsl(${{hue}} 95% 68%)`);

          const elapsed = performance.now() - start;
          const progress = Math.min(96, (elapsed / total) * 100);

          meter.style.width = progress + '%';
          bottom.style.width = progress + '%';
          percent.textContent = Math.floor(progress) + '%';

          if (progress > 58) {{
            label.textContent = 'STABILIZING ENERGY...';
            sub.textContent = 'LOCKING ONTO AURA';
          }}

          if (progress > 82) {{
            label.textContent = 'FINALIZING ROLL';
            sub.textContent = 'REVEAL IMMINENT';
          }}
        }}, 75);

        setTimeout(() => {{
          clearInterval(ticker);

          root.style.setProperty('--glow', final.color);
          root.classList.add('revealed', 'finished');

          document.getElementById('final-emoji').textContent = final.emoji;
          document.getElementById('final-rarity').textContent = final.rarity;
          document.getElementById('final-name').textContent = final.name;
          document.getElementById('final-odds').textContent = final.odds;

          nameEl.textContent = final.name.toUpperCase();
          label.textContent = 'AURA LOCKED';
          sub.textContent = 'DROP SUCCESSFULLY GENERATED';

          meter.style.width = '100%';
          bottom.style.width = '100%';
          percent.textContent = '100%';

          const flash = document.getElementById('flash');

          flash.animate(
            [
              {opacity: 0},
              {opacity: .95, offset: .18},
              {opacity: 0}
            ],
            {duration: 650, easing: 'ease-out'}
          );

          scene.animate(
            [
              {transform: 'scale(1)'},
              {transform: 'scale(1.025)'},
              {transform: 'scale(1)'}
            ],
            {duration: 650, easing: 'ease-out'}
          );

          document.getElementById('final-card').classList.add('show');

          for (let i = 0; i < 70; i++) {{
            particles.push({{
              x: w / 2,
              y: h / 2,
              vx: (Math.random() - .5) * 5,
              vy: (Math.random() - .5) * 5,
              size: Math.random() * 3 + 1,
              alpha: 1
            }});
          }}

          setTimeout(() => window.removeEventListener('resize', resize), 12000);
        }}, total);
      }})();
    </script>
    """, height=510, scrolling=False)


init_db()

if "username" not in st.session_state:
    st.session_state.username = ""

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "last_drop" not in st.session_state:
    st.session_state.last_drop = None

st.markdown("""
<style>
  .stApp {
    background:
      radial-gradient(circle at 8% 0%, rgba(125, 55, 255, .22), transparent 28%),
      radial-gradient(circle at 95% 18%, rgba(0, 220, 255, .15), transparent 25%),
      #090914;
    background-attachment: fixed;
    color: #f7f7ff;
  }

  [data-testid="stSidebar"] {
    background: rgba(17,14,35,.96);
    border-right: 1px solid #292348;
  }

  h1, h2, h3 { letter-spacing: -.5px; }

  div.stButton > button {
    border: 1px solid #8b5cf6;
    border-radius: 12px;
    font-weight: 800;
  }

  div.stButton > button:hover {
    border-color: #22d3ee;
    color: #67e8f9;
    box-shadow: 0 0 18px #7c3aed55;
  }

  .hero {
    padding: 24px;
    border-radius: 20px;
    border: 1px solid #443078;
    background: linear-gradient(120deg, #21143e, #101a30);
    box-shadow: 0 0 30px #6d28d922;
  }

  .muted { color: #b7b4d5; }
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("# 🎮 GAME HUB")
st.sidebar.caption("Neon edition")

player_name = st.sidebar.text_input(
    "Playernaam",
    value=st.session_state.username,
    max_chars=24,
    key="player_name_input"
)

if st.sidebar.button("Gebruik deze speler", use_container_width=True):
    name = clean_username(player_name)

    if not name:
        st.sidebar.error("Vul een geldige spelernaam in.")
    else:
        ensure_player(name)
        st.session_state.username = name
        st.session_state.last_drop = None
        st.rerun()

if not st.session_state.username:
    st.markdown(
        '<div class="hero"><h1>🎲 Welkom bij ROLLS</h1>'
        '<p class="muted">Kies links een spelernaam om te beginnen. '
        'Nieuwe spelers starten met 1.000 money.</p></div>',
        unsafe_allow_html=True
    )
    st.stop()

username = st.session_state.username
ensure_player(username)
player = get_player(username)

st.sidebar.markdown("---")
st.sidebar.markdown(f"### 👤 {html.escape(username)}")

if player["infinite_money"]:
    st.sidebar.metric("Money", "∞")
else:
    st.sidebar.metric("Money", f"€{player['money']:,.0f}")

st.sidebar.metric("Luck boost", f"{player['luck']:,.0f}%")

pages = ["Home", "Shop", "Gambling", "ROLLS", "Inventory", "Stats", "Code"]
page = st.sidebar.radio("NAVIGATIE", pages, label_visibility="collapsed")

if page == "Home":
    st.markdown(
        '<div class="hero"><h1>⚡ GAME HUB</h1>'
        '<p class="muted">Shop, roll zeldzame drops en bouw je collectie op.</p></div>',
        unsafe_allow_html=True
    )

    a, b, c = st.columns(3)
    a.metric("Money", "∞" if player["infinite_money"] else f"€{player['money']:,.0f}")
    b.metric("Luck", f"{player['luck']:,.0f}%")
    c.metric("Rolls gedaan", len(recent_rolls(username, 1000)))

    st.info("Tip: ga naar ROLLS om drops te verzamelen.")

elif page == "Shop":
    st.title("🛍️ Shop")
    st.caption("Koop game-items met je virtuele money.")

    shop_items = [
        ("🍞 Bread", 5), ("🧀 Cheese", 7), ("🥤 Cola", 3),
        ("🍕 Pizza", 9), ("🍔 Burger", 7), ("🍟 Fries", 4),
        ("🍫 Chocolate", 3), ("🍎 Apple", 1),
        ("🎧 Headphones", 50), ("⌨️ Keyboard", 80),
        ("🖱️ Mouse", 40), ("🎮 Controller", 60),
        ("💎 Diamond", 500), ("🎁 Mystery Box", 25),
    ]

    cols = st.columns(3)

    for i, (name, price) in enumerate(shop_items):
        with cols[i % 3]:
            with st.container(border=True):
                st.subheader(name)
                st.write(f"**€{price}**")

                if st.button(f"Koop {name}", key=f"shop_{i}", use_container_width=True):
                    current = get_player(username)

                    if current["infinite_money"] or current["money"] >= price:
                        if not current["infinite_money"]:
                            update_player(username, money=current["money"] - price)

                        add_inventory_item(username, name)
                        st.success(f"{name} gekocht!")
                        st.rerun()
                    else:
                        st.error("Niet genoeg money.")

elif page == "Gambling":
    st.title("🎰 Gambling")
    st.warning("Alleen virtuele game-money; geen echt geld.")

    if "gamble_last" not in st.session_state:
        st.session_state.gamble_last = None

    if st.button("🎰 Spin — €50", type="primary"):
        current = get_player(username)

        if not current["infinite_money"] and current["money"] < 50:
            st.error("Niet genoeg money.")
        else:
            if not current["infinite_money"]:
                update_player(username, money=current["money"] - 50)

            symbols = ["🍋", "🍒", "💎", "⭐", "🍀", "7️⃣"]
            result = [random.choice(symbols) for _ in range(3)]

            if result == ["🍋", "🍋", "🍋"]:
                prize = 1000
            elif len(set(result)) == 1:
                prize = 500
            elif len(set(result)) == 2:
                prize = 100
            else:
                prize = 0

            current = get_player(username)

            if prize and not current["infinite_money"]:
                update_player(username, money=current["money"] + prize)

            st.session_state.gamble_last = (result, prize)

    if st.session_state.gamble_last:
        result, prize = st.session_state.gamble_last

        st.markdown(
            f"<div class='hero' style='text-align:center;font-size:42px'>"
            f"{'　'.join(result)}</div>",
            unsafe_allow_html=True
        )

        st.subheader(f"Je won €{prize}!" if prize else "Geen prijs deze keer.")

elif page == "ROLLS":
    st.title("✨ R O L L S")
    st.caption("Roll voor 100 money. Hoe hoger de odds, hoe zeldzamer de drop.")

    current = get_player(username)

    c1, c2, c3 = st.columns(3)
    c1.metric("Roll price", "100 money")
    c2.metric("Luck", f"{current['luck']:,.0f}%")
    c3.metric(
        "Items in collectie",
        len([x for x in (current["inventory"] or "").split("|") if x])
    )

    st.markdown(
        '<div class="hero"><h2>🎲 Klaar voor je roll?</h2>'
        '<p class="muted">Common → Uncommon → Rare → Legendary → Mythical</p></div>',
        unsafe_allow_html=True
    )

    if st.button("🎲 ROLL — 100 MONEY", type="primary", use_container_width=True):
        current = get_player(username)

        if not current["infinite_money"] and current["money"] < ROLL_COST:
            st.error("Je hebt niet genoeg money voor een roll.")
        else:
            if not current["infinite_money"]:
                update_player(username, money=current["money"] - ROLL_COST)

            drop = roll_item(current["luck"])
            add_inventory_item(username, drop["name"])
            save_roll(username, drop)
            st.session_state.last_drop = drop
            st.rerun()

    if st.session_state.last_drop:
        show_reveal(st.session_state.last_drop)

    st.markdown("### 📖 Drop index")

    for rarity in ["Common", "Uncommon", "Rare", "Legendary", "Mythical"]:
        subset = [item for item in ITEMS if item["rarity"] == rarity]

        with st.expander(f"{rarity} ({len(subset)} drops)"):
            for item in subset:
                st.write(
                    f"{item['emoji']} **{item['name']}** — "
                    f"1/{item['odds']:,}"
                )

elif page == "Inventory":
    st.title("🎒 Inventory")

    current = get_player(username)
    inventory = [
        x for x in (current["inventory"] or "").split("|") if x
    ]

    if not inventory:
        st.info("Je inventory is nog leeg. Ga naar Shop of ROLLS.")
    else:
        counts = {}

        for item in inventory:
            counts[item] = counts.get(item, 0) + 1

        for name, count in sorted(counts.items()):
            st.write(f"• **{name}** × {count}")

    st.markdown("### Recentste ROLLS")
    history = recent_rolls(username)

    if history:
        for roll in history:
            color = RARITY_COLORS.get(roll["rarity"], "#ffffff")

            st.markdown(
                f"<div style='padding:10px;margin:6px 0;"
                f"border:1px solid {color};border-radius:10px'>"
                f"<b>{html.escape(roll['item_name'])}</b> · "
                f"{html.escape(roll['rarity'])} · "
                f"1/{roll['odds']:,}<br>"
                f"<small>{html.escape(roll['rolled_at'])}</small></div>",
                unsafe_allow_html=True
            )
    else:
        st.caption("Je hebt nog geen ROLLS gedaan.")

elif page == "Stats":
    st.title("📊 Stats")

    current = get_player(username)
    history = recent_rolls(username, 10000)

    st.metric("Totaal opgeslagen rolls", len(history))
    st.metric(
        "Verschillende drops",
        len(set(x["item_name"] for x in history))
    )
    st.metric("Luck boost", f"{current['luck']:,.0f}%")

    if history:
        st.markdown("### Laatste 10 drops")

        for roll in history[:10]:
            st.write(
                f"{roll['item_name']} — {roll['rarity']} — "
                f"1/{roll['odds']:,}"
            )

elif page == "Code":
    st.title("🔐 Code")
    st.caption("Voer de admin-code in om het adminpanel te openen.")

    if not st.session_state.admin_logged_in:
        with st.form("admin_login"):
            code = st.text_input(
                "Admin code",
                type="password",
                placeholder="Voer code in..."
            )
            submitted = st.form_submit_button("Unlock admin")

        if submitted:
            if code == ADMIN_CODE:
                st.session_state.admin_logged_in = True
                st.success("Adminpanel ontgrendeld.")
                st.rerun()
            else:
                st.error("Verkeerde code.")

    else:
        st.success("Adminpanel actief")

        if st.button("Uitloggen als admin"):
            st.session_state.admin_logged_in = False
            st.rerun()

        st.markdown("## 💰 Money geven")

        players = all_players()
        names = [p["username"] for p in players]

        if not names:
            st.info("Nog geen spelers.")
        else:
            target = st.selectbox("Kies speler", names, key="admin_money_target")
            amount = st.number_input(
                "Bedrag om toe te voegen",
                min_value=0,
                max_value=10**12,
                value=1000,
                step=100
            )

            if st.button("Geef money", type="primary"):
                target_player = get_player(target)

                if target_player and not target_player["infinite_money"]:
                    update_player(
                        target,
                        money=target_player["money"] + amount
                    )

                st.success(f"€{amount:,.0f} toegevoegd aan {target}.")
                st.rerun()

        st.markdown("## 🍀 Luck boosten")

        players = all_players()
        names = [p["username"] for p in players]

        if names:
            target_luck = st.selectbox(
                "Kies speler voor luck",
                names,
                key="admin_luck_target"
            )

            luck_value = st.number_input(
                "Luck boost (%)",
                min_value=0,
                max_value=MAX_LUCK_PERCENT,
                value=100,
                step=100
            )

            if st.button("Sla luck op"):
                update_player(target_luck, luck=float(luck_value))
                st.success(
                    f"{target_luck} heeft nu {luck_value:,.0f}% luck."
                )
                st.rerun()

        st.markdown("## ♾️ Infinite money")

        own_player = get_player(username)

        enable_inf = st.toggle(
            "Zet infinite money aan voor mijn speler",
            value=bool(own_player["infinite_money"])
        )

        if st.button("Bewaar infinite money-instelling"):
            update_player(username, infinite_money=int(enable_inf))
            st.success("Infinite money-instelling bijgewerkt.")
            st.rerun()

        st.markdown("## 🧾 Spelersoverzicht")
        st.dataframe(all_players(), use_container_width=True, hide_index=True)

        st.markdown("## 🎲 Drops aanpassen")
        st.caption(
            "De drops en odds staan bovenaan in de ITEMS-lijst in app.py. "
            "Pas die lijst aan om namen en kansen te wijzigen."
        )

st.sidebar.markdown("---")
st.sidebar.caption("Demo build • virtuele game-economie")
