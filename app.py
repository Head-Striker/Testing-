import random
import sqlite3
import html
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

    common = [item for item in ITEMS if item["rarity"] == "Common"]
    return random.choice(common)


def show_reveal(item):
    rarity = item["rarity"]
    animation = item["animation"]
    color = RARITY_COLORS.get(rarity, "#ffffff")
    safe_name = html.escape(item["name"])
    safe_rarity = html.escape(rarity.upper())
    emoji = item["emoji"]

    if animation == "no":
        st.success(
            f"{emoji} **{item['name']}** — {rarity} — 1/{item['odds']}"
        )
        return

    if animation == "yes":
        body = f"""
        <div class="reveal normal" style="--glow:{color}">
          <div class="burst"></div>
          <div class="emoji">{emoji}</div>
          <div class="rarity">{safe_rarity}</div>
          <div class="name">{safe_name}</div>
          <div class="odds">1 IN {item['odds']:,}</div>
        </div>
        """
    elif animation == "super":
        body = f"""
        <div class="reveal super" style="--glow:{color}">
          <div class="scan"></div>
          <div class="rings"></div>
          <div class="burst"></div>
          <div class="emoji">{emoji}</div>
          <div class="rarity">{safe_rarity} DROP</div>
          <div class="name">{safe_name}</div>
          <div class="odds">1 IN {item['odds']:,}</div>
        </div>
        """
    else:
        body = f"""
        <div class="reveal ultra" style="--glow:{color}">
          <div class="stars"></div>
          <div class="portal"></div>
          <div class="shockwave"></div>
          <div class="blackout">REALITY BREAKING...</div>
          <div class="emoji">{emoji}</div>
          <div class="rarity">✦ MYTHICAL • ABSOLUTE RARITY ✦</div>
          <div class="name">{safe_name}</div>
          <div class="odds">1 IN {item['odds']:,}</div>
          <div class="final">THE IMPOSSIBLE HAS HAPPENED</div>
        </div>
        """

    components.html(f"""
    <style>
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        background: transparent;
        font-family: Arial, sans-serif;
        color: white;
      }}
      .reveal {{
        position: relative;
        height: 360px;
        overflow: hidden;
        border-radius: 22px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background: radial-gradient(ellipse at center, var(--glow), #05050a 72%);
        border: 1px solid var(--glow);
        box-shadow: 0 0 28px var(--glow), inset 0 0 55px #000;
      }}
      .emoji {{
        z-index: 2;
        font-size: 70px;
        animation: float 1.8s ease-in-out infinite, pop .8s ease-out both;
        filter: drop-shadow(0 0 20px var(--glow));
      }}
      .rarity {{
        z-index: 2;
        margin-top: 8px;
        font-size: 13px;
        letter-spacing: 5px;
        color: var(--glow);
        font-weight: 900;
      }}
      .name {{
        z-index: 2;
        margin-top: 8px;
        font-size: clamp(26px, 5vw, 46px);
        font-weight: 1000;
        text-align: center;
        text-shadow: 0 0 10px var(--glow), 0 0 28px var(--glow);
        animation: glitch .7s steps(2) 2;
      }}
      .odds {{
        z-index: 2;
        margin-top: 12px;
        font-size: 18px;
        letter-spacing: 3px;
        font-weight: 800;
      }}
      .burst {{
        position: absolute;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: var(--glow);
        box-shadow: 0 0 70px 35px var(--glow);
        animation: burst 2.4s ease-out both;
        opacity: .7;
      }}
      .rings {{
        position: absolute;
        width: 120px;
        height: 120px;
        border: 2px solid var(--glow);
        border-radius: 50%;
        box-shadow: 0 0 30px var(--glow);
        animation: ring 3s ease-out infinite;
      }}
      .scan {{
        position: absolute;
        inset: -80% 0;
        background: linear-gradient(transparent, #ffffff22, transparent);
        animation: scan 3s linear infinite;
      }}
      .super {{
        animation: shake .12s linear 5, hue 4s linear infinite;
      }}
      .ultra {{
        height: 430px;
        background: radial-gradient(circle at center, #26113d 0, #090714 36%, #020207 78%);
        animation: universe 13s ease-in-out both;
      }}
      .portal {{
        position: absolute;
        width: 120px;
        height: 120px;
        border: 5px solid white;
        border-radius: 50%;
        box-shadow: 0 0 25px #c084fc, 0 0 65px #8b5cf6;
        animation: portal 5s ease-in-out both;
      }}
      .shockwave {{
        position: absolute;
        width: 60px;
        height: 60px;
        border: 3px solid white;
        border-radius: 50%;
        animation: shock 4s 3s ease-out infinite;
      }}
      .stars {{
        position: absolute;
        inset: 0;
        opacity: .65;
        background-image:
          radial-gradient(2px 2px at 15% 25%, white 50%, transparent 60%),
          radial-gradient(2px 2px at 75% 20%, #f0abfc 50%, transparent 60%),
          radial-gradient(3px 3px at 40% 70%, white 50%, transparent 60%),
          radial-gradient(2px 2px at 88% 75%, #c4b5fd 50%, transparent 60%),
          radial-gradient(2px 2px at 22% 82%, white 50%, transparent 60%);
        animation: stars 2s ease-in-out infinite alternate;
      }}
      .blackout {{
        position: absolute;
        top: 22px;
        font-size: 11px;
        letter-spacing: 5px;
        color: #c4b5fd;
        animation: fadeout 3s both;
      }}
      .final {{
        z-index: 2;
        margin-top: 14px;
        color: #f5d0fe;
        font-size: 12px;
        letter-spacing: 3px;
        font-weight: 900;
        animation: fadein 2s 7s both;
      }}
      @keyframes float {{ 50% {{ transform: translateY(-12px) rotate(3deg); }} }}
      @keyframes pop {{
        from {{ transform: scale(.1); opacity: 0; }}
        to {{ transform: scale(1); opacity: 1; }}
      }}
      @keyframes burst {{
        0% {{ transform: scale(.1); opacity: 0; }}
        35% {{ opacity: .8; }}
        100% {{ transform: scale(15); opacity: 0; }}
      }}
      @keyframes ring {{
        from {{ transform: scale(.4); opacity: 1; }}
        to {{ transform: scale(4); opacity: 0; }}
      }}
      @keyframes scan {{ to {{ transform: translateY(100%); }} }}
      @keyframes shake {{
        0%, 100% {{ transform: translateX(0); }}
        25% {{ transform: translateX(-3px); }}
        75% {{ transform: translateX(3px); }}
      }}
      @keyframes hue {{ 50% {{ filter: hue-rotate(45deg); }} }}
      @keyframes glitch {{
        0%, 100% {{ transform: translate(0); }}
        30% {{ transform: translate(2px, -1px); }}
        60% {{ transform: translate(-2px, 1px); }}
      }}
      @keyframes portal {{
        0% {{ transform: scale(.05) rotate(0); opacity: 0; }}
        35% {{ opacity: 1; }}
        75% {{ transform: scale(5) rotate(240deg); opacity: .8; }}
        100% {{ transform: scale(8) rotate(360deg); opacity: 0; }}
      }}
      @keyframes shock {{ to {{ transform: scale(12); opacity: 0; }} }}
      @keyframes stars {{ to {{ opacity: 1; transform: scale(1.03); }} }}
      @keyframes fadeout {{
        0%, 60% {{ opacity: 1; }}
        100% {{ opacity: 0; }}
      }}
      @keyframes fadein {{
        from {{ opacity: 0; transform: translateY(12px); }}
        to {{ opacity: 1; transform: translateY(0); }}
      }}
      @keyframes universe {{
        0% {{ filter: brightness(.2); }}
        20% {{ filter: brightness(.6); }}
        45% {{ filter: brightness(1.5); }}
        55% {{ filter: brightness(.5); }}
        100% {{ filter: brightness(1); }}
      }}
    </style>
    {body}
    """, height=450 if animation == "supersuper" else 380, scrolling=False)


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
    background: rgba(17, 14, 35, .96);
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
    st.info("Tip: ga naar ROLLS om drops te verzamelen. De animatie start zodra je een drop krijgt.")

elif page == "Shop":
    st.title("🛍️ Shop")
    st.caption("Een simpele demo-shop. Koop eten, drankjes en game-items met je virtuele money.")
    shop_items = [
        ("🍞 Bread", 5), ("🧀 Cheese", 7), ("🥤 Cola", 3), ("🍕 Pizza", 9),
        ("🍔 Burger", 7), ("🍟 Fries", 4), ("🍫 Chocolate", 3), ("🍎 Apple", 1),
        ("🎧 Headphones", 50), ("⌨️ Keyboard", 80), ("🖱️ Mouse", 40),
        ("🎮 Controller", 60), ("💎 Diamond", 500), ("🎁 Mystery Box", 25),
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
    st.write("Dit is de oude Money Machine-tab, nu hernoemd naar Gambling.")

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
                    f"1/{item['odds']:,} — animation: {item['animation']}"
                )

elif page == "Inventory":
    st.title("🎒 Inventory")
    current = get_player(username)
    inventory = [x for x in (current["inventory"] or "").split("|") if x]

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
                f"{html.escape(roll['rarity'])} · 1/{roll['odds']:,}<br>"
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
    st.metric("Verschillende drops", len(set(x["item_name"] for x in history)))
    st.metric("Luck boost", f"{current['luck']:,.0f}%")

    if history:
        st.markdown("### Laatste 10 drops")
        for roll in history[:10]:
            st.write(f"{roll['item_name']} — {roll['rarity']} — 1/{roll['odds']:,}")

elif page == "Code":
    st.title("🔐 Code")
    st.caption("Voer de admin-code in om het adminpanel te openen.")

    if not st.session_state.admin_logged_in:
        with st.form("admin_login"):
            code = st.text_input("Admin code", type="password", placeholder="Voer code in...")
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
                    update_player(target, money=target_player["money"] + amount)
                st.success(f"€{amount:,.0f} toegevoegd aan {target}.")
                st.rerun()

        st.markdown("## 🍀 Luck boosten")
        players = all_players()
        names = [p["username"] for p in players]

        if names:
            target_luck = st.selectbox("Kies speler voor luck", names, key="admin_luck_target")
            luck_value = st.number_input(
                "Luck boost (%)",
                min_value=0,
                max_value=MAX_LUCK_PERCENT,
                value=100,
                step=100
            )
            if st.button("Sla luck op"):
                update_player(target_luck, luck=float(luck_value))
                st.success(f"{target_luck} heeft nu {luck_value:,.0f}% luck.")
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
