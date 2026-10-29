import streamlit as st
import random
import time
import html
import sqlite3
import os

st.set_page_config(
    page_title="Game Shop",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# DATABASE: GLOBALE BERICHTEN
# ============================================================

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game_messages.db")


def init_database():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS global_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL,
                created_at REAL NOT NULL
            )
        """)


def send_global_message(message):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO global_messages (message, created_at) VALUES (?, ?)",
            (message, time.time()),
        )


def get_global_messages(limit=5):
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute(
            "SELECT message, created_at FROM global_messages ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()


init_database()

# ============================================================
# GAME SHOP
# ============================================================

START_SHOP = {
    "bread": [4.99, 15], "cheese": [6.99, 23],
    "cola": [2.67, 36], "pancakes": [3.25, 36],
    "pizza": [8.99, 20], "burger": [6.50, 25],
    "fries": [3.49, 30], "chocolate": [2.99, 40],
    "cookie": [1.25, 50], "cake": [5.99, 15],
    "apple": [0.75, 60], "banana": [0.60, 60],
    "water": [1.00, 50], "energy_drink": [3.50, 25],
    "headphones": [49.99, 10], "keyboard": [79.99, 8],
    "mouse": [39.99, 12], "monitor": [199.99, 5],
    "phone": [699.99, 4], "laptop": [999.99, 3],
    "gaming_pc": [1499.99, 2], "controller": [59.99, 10],
    "tshirt": [19.99, 20], "hoodie": [49.99, 15],
    "jeans": [39.99, 18], "sneakers": [89.99, 10],
    "cap": [14.99, 20], "minecraft": [29.99, 10],
    "gaming_chair": [249.99, 4], "gaming_desk": [179.99, 5],
    "microphone": [69.99, 8], "webcam": [49.99, 10],
    "diamond": [499.99, 3], "gold_bar": [999.99, 2],
    "mystery_box": [24.99, 20], "legendary_trophy": [2499.99, 1],
    "uranium": [1999.99, 1],
}

CATEGORIES = {
    "🍔 Food & Drinks": [
        "bread", "cheese", "cola", "pancakes", "pizza", "burger",
        "fries", "chocolate", "cookie", "cake", "apple", "banana",
        "water", "energy_drink",
    ],
    "💻 Electronics": [
        "headphones", "keyboard", "mouse", "monitor", "phone",
        "laptop", "gaming_pc", "controller",
    ],
    "👕 Clothing": ["tshirt", "hoodie", "jeans", "sneakers", "cap"],
    "🎮 Gaming": [
        "minecraft", "gaming_chair", "gaming_desk",
        "microphone", "webcam",
    ],
    "💎 Rare Items": [
        "diamond", "gold_bar", "mystery_box",
        "legendary_trophy", "uranium",
    ],
}

INFO = {
    "bread": ("🍞", "You can eat this."),
    "cheese": ("🧀", "A tasty snack."),
    "cola": ("🥤", "A refreshing drink."),
    "pancakes": ("🥞", "A stack of pancakes."),
    "pizza": ("🍕", "A delicious pizza."),
    "burger": ("🍔", "A classic burger."),
    "fries": ("🍟", "Crispy fries."),
    "chocolate": ("🍫", "Something sweet."),
    "cookie": ("🍪", "A freshly baked cookie."),
    "cake": ("🍰", "A slice of cake."),
    "apple": ("🍎", "A fresh apple."),
    "banana": ("🍌", "A ripe banana."),
    "water": ("💧", "Restores thirst."),
    "energy_drink": ("⚡", "Restores thirst."),
    "headphones": ("🎧", "Listen to your favourite sounds."),
    "keyboard": ("⌨️", "A keyboard for your setup."),
    "mouse": ("🖱️", "A gaming mouse."),
    "monitor": ("🖥️", "A computer monitor."),
    "phone": ("📱", "A modern phone."),
    "laptop": ("💻", "A portable computer."),
    "gaming_pc": ("🖥️", "A powerful gaming PC."),
    "controller": ("🎮", "A gaming controller."),
    "tshirt": ("👕", "A casual T-shirt."),
    "hoodie": ("🧥", "A comfortable hoodie."),
    "jeans": ("👖", "A pair of jeans."),
    "sneakers": ("👟", "A pair of sneakers."),
    "cap": ("🧢", "A cap for your character."),
    "minecraft": ("⛏️", "A block-building adventure."),
    "gaming_chair": ("🪑", "A chair for your setup."),
    "gaming_desk": ("🪵", "A desk for your setup."),
    "microphone": ("🎙️", "A microphone."),
    "webcam": ("📷", "A webcam."),
    "diamond": ("💎", "A rare diamond."),
    "gold_bar": ("🥇", "A precious gold bar."),
    "mystery_box": ("🎁", "What's inside? It's a mystery."),
    "legendary_trophy": ("🏆", "An extremely rare trophy."),
    "uranium": ("☢️", "Don't taste this."),
}

FOOD_ITEMS = {
    "bread", "cheese", "pancakes", "pizza", "burger", "fries",
    "chocolate", "cookie", "cake", "apple", "banana",
}
DRINK_ITEMS = {"cola", "water", "energy_drink"}

# ============================================================
# ROLLS ITEMS
# ============================================================

ROLL_ITEMS = [
    {"name": "Roblox", "odds": 2, "rarity": "Common", "animation": "no", "emoji": "🟥"},
    {"name": "Enrique", "odds": 4, "rarity": "Common", "animation": "no", "emoji": "🎵"},
    {"name": "Unknown I", "odds": 8, "rarity": "Common", "animation": "no", "emoji": "⚪"},
    {"name": "Unknown II", "odds": 16, "rarity": "Common", "animation": "no", "emoji": "🔹"},
    {"name": "Unknown III", "odds": 32, "rarity": "Common", "animation": "no", "emoji": "🔸"},
    {"name": "Unknown IV", "odds": 64, "rarity": "Common", "animation": "no", "emoji": "🟢"},
    {"name": "Unknown V", "odds": 128, "rarity": "Uncommon", "animation": "no", "emoji": "🟩"},
    {"name": "Unknown VI", "odds": 264, "rarity": "Uncommon", "animation": "yes", "emoji": "💠"},
    {"name": "Unknown VII", "odds": 528, "rarity": "Uncommon", "animation": "yes", "emoji": "🔷"},
    {"name": "Unknown VIII", "odds": 1048, "rarity": "Rare", "animation": "yes", "emoji": "💎"},
    {"name": "Unknown IX", "odds": 2500, "rarity": "Rare", "animation": "yes", "emoji": "🌠"},
    {"name": "Unknown X", "odds": 5000, "rarity": "Rare", "animation": "yes", "emoji": "🌀"},
    {"name": "Unknown XI", "odds": 1000, "rarity": "Rare", "animation": "yes", "emoji": "⚡"},
    {"name": "Unknown XII", "odds": 25000, "rarity": "Legendary", "animation": "super", "emoji": "👑"},
    {"name": "Unknown XIII", "odds": 50000, "rarity": "Legendary", "animation": "super", "emoji": "🔥"},
    {"name": "Unknown XIV", "odds": 100000, "rarity": "Legendary", "animation": "super", "emoji": "☄️"},
    {"name": "Blackhole", "odds": 250000, "rarity": "Mythical", "animation": "super", "emoji": "🌌"},
    {"name": "Unknown XV", "odds": 500000, "rarity": "Mythical", "animation": "super", "emoji": "🪐"},
    {"name": "Unknown XVI", "odds": 1000000, "rarity": "Mythical", "animation": "supersuper", "emoji": "♾️"},
]

RARITY_COLORS = {
    "Common": "#b5bac1",
    "Uncommon": "#57e389",
    "Rare": "#43a5ff",
    "Legendary": "#ffad33",
    "Mythical": "#d65cff",
}

# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "money": 250.00,
    "shop": {k: v.copy() for k, v in START_SHOP.items()},
    "inventory": {},
    "rolls_inventory": {},
    "rolls_count": 0,
    "rolls_spent": 0.0,
    "last_roll": None,
    "notice": None,
    "last_spin": None,
    "hunger": 100.0,
    "thirst": 100.0,
    "survival_updated_at": time.time(),
    "game_over": False,
    "admin_unlocked": False,
    "luck_multiplier": 1,
    "stats": {
        "items_bought": 0,
        "spins": 0,
        "money_earned": 0.0,
    },
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value.copy() if isinstance(value, dict) else value

for item, data in START_SHOP.items():
    st.session_state.shop.setdefault(item, data.copy())

# ============================================================
# SURVIVAL TIMER
# ============================================================

now = time.time()
elapsed = max(0, now - st.session_state.survival_updated_at)
st.session_state.survival_updated_at = now
st.session_state.hunger = max(0, st.session_state.hunger - elapsed * 0.12)
st.session_state.thirst = max(0, st.session_state.thirst - elapsed * 0.18)

if st.session_state.hunger <= 0 or st.session_state.thirst <= 0:
    st.session_state.game_over = True

# ============================================================
# NEON DESIGN
# ============================================================

st.markdown("""
<style>
.stApp {
    background-color:#10101b;
    background-image:
        radial-gradient(ellipse at 12% 8%,#51138a 0%,transparent 40%),
        radial-gradient(ellipse at 88% 75%,#07566a 0%,transparent 42%);
    background-attachment:fixed;
    color:#f7f2ff;
}
[data-testid="stAppViewContainer"] {background:transparent;}
[data-testid="stSidebar"] {
    background:rgba(25,19,41,.97);
    border-right:2px solid #8c36d9;
}
h1,h2,h3 {color:white;}
div[data-testid="stMetric"] {
    background:rgba(32,24,50,.94);
    border:1px solid #7338a8;
    padding:14px;
    border-radius:14px;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    background:rgba(31,23,49,.96);
    border:1px solid #563b78;
    border-radius:15px;
}
div.stButton > button {
    background:linear-gradient(110deg,#7727d5,#bd26a7);
    color:white;
    border:1px solid #d58cff;
    border-radius:10px;
    font-weight:650;
    transition:transform .18s ease,filter .18s ease;
}
div.stButton > button:hover {
    filter:brightness(1.2);
    transform:translateY(-2px);
    border-color:white;
}
.item-emoji {font-size:40px;margin-bottom:8px;}
.item-name {font-size:16px;font-weight:700;overflow-wrap:anywhere;}
.item-price {color:#50f0e1;font-weight:700;margin-top:6px;}
.item-stock {color:#c3b7d4;font-size:12px;margin-top:4px;}
.slot {
    background:linear-gradient(145deg,#251a3f,#121b34);
    border:2px solid #a84cff;border-radius:16px;
    padding:18px 3px;text-align:center;font-size:42px;
    min-height:95px;box-shadow:0 0 12px #6824a833;
}
.page-content {animation:page-enter .35s ease-out;}
@keyframes page-enter {
    from {opacity:.3;transform:translateY(8px);}
    to {opacity:1;transform:translateY(0);}
}
.roll-card {
    border:2px solid var(--glow);
    border-radius:22px;
    padding:25px;
    text-align:center;
    background:radial-gradient(circle at center,#30204a,#090914 80%);
    box-shadow:0 0 25px var(--glow);
    animation:reveal-in .8s cubic-bezier(.2,.8,.2,1);
    overflow:hidden;
}
.roll-emoji {
    font-size:76px;
    filter:drop-shadow(0 0 18px var(--glow));
    animation:float 1.7s ease-in-out infinite;
}
.roll-name {
    font-size:clamp(25px,5vw,43px);
    font-weight:1000;
    text-shadow:0 0 12px var(--glow),0 0 30px var(--glow);
    overflow-wrap:anywhere;
}
.roll-rarity {letter-spacing:5px;font-weight:900;color:var(--glow);}
.roll-odds {font-size:18px;letter-spacing:3px;margin-top:10px;}
.roll-super {
    background:radial-gradient(circle at center,#532078,#10091e 60%,#020207);
    animation:reveal-in 2s ease-out,super-glow 1.2s ease-in-out infinite alternate;
}
.roll-ultra {
    min-height:370px;
    background:radial-gradient(circle,#5b1685,#160d2b 35%,#020207 78%);
    animation:reveal-in 2s ease-out,universe 4s ease-in-out infinite alternate;
}
.roll-ultra .roll-emoji {font-size:100px;animation:portal 5s ease-in-out infinite;}
@keyframes reveal-in {
    0% {opacity:0;transform:scale(.1) rotate(-12deg);filter:brightness(4);}
    60% {opacity:1;transform:scale(1.08) rotate(3deg);}
    100% {opacity:1;transform:scale(1) rotate(0);filter:brightness(1);}
}
@keyframes float {
    0%,100% {transform:translateY(0);}
    50% {transform:translateY(-12px);}
}
@keyframes super-glow {
    from {box-shadow:0 0 15px #ffad33;}
    to {box-shadow:0 0 65px #ffdf70;}
}
@keyframes universe {
    0% {filter:brightness(.4) hue-rotate(0deg);}
    50% {filter:brightness(1.5) hue-rotate(35deg);}
    100% {filter:brightness(.8) hue-rotate(-25deg);}
}
@keyframes portal {
    0%,100% {transform:rotate(-8deg) scale(.9);}
    50% {transform:rotate(8deg) scale(1.15);}
}
.jackpot {
    background:linear-gradient(135deg,#541a8b,#a51b87,#df7914);
    border:2px solid #ffe56a;border-radius:18px;
    padding:24px;text-align:center;
    animation:super-glow .8s ease-in-out infinite alternate;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HELPERS
# ============================================================

def pretty_name(item):
    return item.replace("_", " ").title()


def emoji_for(item):
    return INFO.get(item, ("📦", ""))[0]


def buy_item(item, quantity):
    price, stock = st.session_state.shop[item]
    total = round(price * quantity, 2)

    if quantity < 1 or stock < quantity:
        st.session_state.notice = ("error", "Not enough stock.")
    elif st.session_state.money < total:
        st.session_state.notice = ("error", "Not enough money.")
    else:
        st.session_state.money = round(st.session_state.money - total, 2)
        st.session_state.shop[item][1] -= quantity
        st.session_state.inventory[item] = (
            st.session_state.inventory.get(item, 0) + quantity
        )
        st.session_state.stats["items_bought"] += quantity
        st.session_state.notice = (
            "success", f"Bought {quantity} × {pretty_name(item)}!"
        )


def use_item(item):
    quantity = st.session_state.inventory.get(item, 0)

    if quantity < 1:
        st.session_state.notice = ("error", "You don't own this item.")
        return

    if item == "uranium":
        st.session_state.inventory[item] -= 1
        if st.session_state.inventory[item] <= 0:
            del st.session_state.inventory[item]
        st.session_state.game_over = True
        st.rerun()

    if item in FOOD_ITEMS:
        st.session_state.hunger = min(100, st.session_state.hunger + 35)
        st.session_state.inventory[item] -= 1
        st.session_state.notice = ("success", f"You ate {pretty_name(item)}!")
    elif item in DRINK_ITEMS:
        st.session_state.thirst = min(100, st.session_state.thirst + 40)
        st.session_state.inventory[item] -= 1
        st.session_state.notice = ("success", f"You drank {pretty_name(item)}!")
    else:
        st.session_state.notice = (
            "info", INFO.get(item, ("", "You inspected this item."))[1]
        )

    if item in st.session_state.inventory and st.session_state.inventory[item] <= 0:
        del st.session_state.inventory[item]

    st.rerun()


# ============================================================
# ITEM POPUP
# Streamlit's dialog creates a modal with a dimmed background.
# ============================================================

@st.dialog("🛍️ Item details", width="small")
def show_item_dialog(item):
    price, stock = st.session_state.shop[item]
    emoji, description = INFO[item]

    st.markdown(
        f"<div style='text-align:center;font-size:70px'>{emoji}</div>",
        unsafe_allow_html=True,
    )
    st.subheader(pretty_name(item))
    st.write(description)
    st.markdown(f"**Price:** €{price:,.2f}")
    st.markdown(f"**Stock:** {stock}")

    if stock <= 0:
        st.error("Out of stock.")
        return

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        max_value=max(1, stock),
        value=1,
        key=f"modal_quantity_{item}",
    )

    st.markdown(f"**Total:** €{price * quantity:,.2f}")

    if st.button("🛒 Buy item", key=f"modal_buy_{item}", use_container_width=True):
        buy_item(item, quantity)
        st.rerun()


# ============================================================
# ADMIN POPUP
# ============================================================

@st.dialog("🔐 Admin Panel", width="small")
def show_admin_panel():
    st.caption("Admin controls")

    st.markdown("### 💰 Give yourself money")
    amount = st.number_input(
        "Amount to add (€)",
        min_value=0.0,
        max_value=100000000.0,
        value=1000.0,
        step=100.0,
        key="admin_money_amount",
    )

    if st.button("💰 Add money", key="admin_add_money", use_container_width=True):
        st.session_state.money = round(st.session_state.money + amount, 2)
        st.session_state.notice = (
            "success", f"Added €{amount:,.2f} to your balance!"
        )
        st.rerun()

    st.divider()
    st.markdown("### 🍀 Luck settings")

    current_luck = int(st.session_state.luck_multiplier)
    luck = st.slider(
        "Luck multiplier",
        min_value=1,
        max_value=1000,
        value=max(1, min(1000, current_luck)),
        step=1,
        key="admin_luck_slider",
    )

    st.caption(
        "1× = normal luck. 100× makes the rare drops much more likely. "
        "1000× gives an even bigger boost."
    )

    if st.button("✨ Apply luck", key="admin_apply_luck", use_container_width=True):
        st.session_state.luck_multiplier = luck
        st.session_state.notice = (
            "success", f"Luck multiplier set to {luck}×!"
        )
        st.rerun()

    st.divider()
    st.markdown("### 📢 Global message")

    message = st.text_area(
        "Message everyone can see",
        max_chars=300,
        key="admin_global_message",
        placeholder="Write your announcement here...",
    )

    if st.button("📢 Send to everyone", key="admin_send_message", use_container_width=True):
        if message.strip():
            send_global_message(message.strip())
            st.session_state.admin_global_message = ""
            st.session_state.notice = (
                "success", "Global message sent!"
            )
            st.rerun()
        else:
            st.warning("Write a message first.")


# ============================================================
# ROLLS LOGIC
# ============================================================

def perform_roll():
    cost = 100

    if st.session_state.money < cost:
        st.session_state.notice = ("error", "You need €100 to roll.")
        return

    st.session_state.money = round(st.session_state.money - cost, 2)
    st.session_state.rolls_spent += cost
    st.session_state.rolls_count += 1

    # Admin luck reduces the effective odds.
    luck = max(1, int(st.session_state.get("luck_multiplier", 1)))

    result = None

    # Check the rarest drops first.
    for item in sorted(ROLL_ITEMS, key=lambda x: x["odds"], reverse=True):
        effective_odds = max(1, int(item["odds"] / luck))

        if random.randint(1, effective_odds) == 1:
            result = item
            break

    if result is None:
        result = random.choice([
            x for x in ROLL_ITEMS if x["rarity"] == "Common"
        ])

    name = result["name"]
    st.session_state.rolls_inventory[name] = (
        st.session_state.rolls_inventory.get(name, 0) + 1
    )
    st.session_state.last_roll = result.copy()
    st.session_state.notice = None


def show_roll_reveal(item):
    rarity = item["rarity"]
    color = RARITY_COLORS[rarity]
    animation = item["animation"]

    st.markdown(
        f"""
        <div class="roll-card {'roll-super' if animation == 'super' else ''} {'roll-ultra' if animation == 'supersuper' else ''}"
             style="--glow:{color}">
            <div style="font-size:12px;letter-spacing:4px;margin-bottom:10px">
                {"🌌 REALITY IS BREAKING..." if animation == "supersuper" else "✨ DROP DISCOVERED ✨" if animation == "yes" else "⚡ LEGENDARY REVEAL ⚡" if animation == "super" else "DROP"}
            </div>
            <div class="roll-emoji">{item["emoji"]}</div>
            <div class="roll-rarity">{html.escape(rarity.upper())}</div>
            <div class="roll-name">{html.escape(item["name"])}</div>
            <div class="roll-odds">1 IN {item["odds"]:,}</div>
            <div style="margin-top:18px;font-size:12px;letter-spacing:2px">
                {"THE IMPOSSIBLE HAS HAPPENED" if animation == "supersuper" else "INCREDIBLE DROP!" if animation == "super" else "RARE DROP UNLOCKED" if animation == "yes" else "ADDED TO COLLECTION"}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if animation == "yes":
        st.balloons()
    elif animation == "super":
        st.snow()
        st.balloons()
    elif animation == "supersuper":
        stages = [
            "🌌 The dimension is breaking...",
            "🌀 Something is approaching...",
            "⚡ Reality is collapsing...",
            "♾️ THE MYTHICAL HAS ARRIVED!",
        ]
        reveal = st.empty()
        progress = st.progress(0)

        for i, stage in enumerate(stages):
            reveal.markdown(
                f"""
                <div style="padding:22px;text-align:center;border:2px solid #d65cff;
                border-radius:18px;background:radial-gradient(circle,#542078,#080510);
                font-size:25px;font-weight:900;box-shadow:0 0 30px #d65cff">
                    {stage}
                </div>
                """,
                unsafe_allow_html=True,
            )
            progress.progress(int((i + 1) / len(stages) * 100))
            time.sleep(1.2)

        st.balloons()
        st.snow()
        progress.empty()


# ============================================================
# NAVIGATION
# ============================================================

page = st.sidebar.radio(
    "NAVIGATION",
    ["Shop", "Gambling", "ROLLS", "Inventory", "Stats", "Codes"],
    format_func=lambda p: {
        "Shop": "🛍️   Shop",
        "Gambling": "🎰   Gambling",
        "ROLLS": "✨   ROLLS",
        "Inventory": "🎒   Inventory",
        "Stats": "📊   Stats",
        "Codes": "🔑   Codes",
    }[p],
)

st.sidebar.divider()
st.sidebar.metric("💰 Balance", f"€{st.session_state.money:,.2f}")

st.sidebar.markdown("### SURVIVAL")
st.sidebar.write(f"🍗 Hunger — {int(st.session_state.hunger)}%")
st.sidebar.progress(int(st.session_state.hunger))
st.sidebar.write(f"💧 Thirst — {int(st.session_state.thirst)}%")
st.sidebar.progress(int(st.session_state.thirst))
st.sidebar.caption("Food restores hunger. Drinks restore thirst.")

# Current luck status
st.sidebar.divider()
st.sidebar.caption(f"🍀 Luck multiplier: {st.session_state.luck_multiplier}×")

# ============================================================
# GLOBAL MESSAGES
# Visible to everyone, without a login.
# ============================================================

messages = get_global_messages(5)

if messages:
    with st.container(border=True):
        st.markdown("### 📢 Global messages")

        for message, created_at in reversed(messages):
            st.info(message)
            st.caption(time.strftime("%d-%m-%Y %H:%M", time.localtime(created_at)))

# ============================================================
# TOP STATUS
# ============================================================

top1, top2 = st.columns(2)

with top1:
    st.caption(f"🍗 HUNGER · {int(st.session_state.hunger)}%")
    st.progress(int(st.session_state.hunger))

with top2:
    st.caption(f"💧 THIRST · {int(st.session_state.thirst)}%")
    st.progress(int(st.session_state.thirst))

if st.session_state.hunger < 25:
    st.warning("Your hunger is low! Buy food and use it in your inventory.")

if st.session_state.thirst < 25:
    st.warning("Your thirst is low! Buy a drink and use it in your inventory.")

if st.session_state.notice:
    kind, message = st.session_state.notice

    if kind == "success":
        st.success(message)
    elif kind == "error":
        st.error(message)
    else:
        st.info(message)

    st.session_state.notice = None

# ============================================================
# GAME OVER
# ============================================================

if st.session_state.game_over:
    st.title("☠️ GAME OVER")
    st.error(
        "Your character ran out of hunger or thirst, "
        "or triggered the fictional uranium game-over effect."
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Balance", f"€{st.session_state.money:,.2f}")
    c2.metric("Items bought", st.session_state.stats["items_bought"])
    c3.metric("Rolls played", st.session_state.rolls_count)

    if st.button("Start a new game", use_container_width=True):
        st.session_state.money = 250.00
        st.session_state.inventory = {}
        st.session_state.rolls_inventory = {}
        st.session_state.rolls_count = 0
        st.session_state.rolls_spent = 0.0
        st.session_state.last_roll = None
        st.session_state.hunger = 100.0
        st.session_state.thirst = 100.0
        st.session_state.survival_updated_at = time.time()
        st.session_state.game_over = False
        st.session_state.shop = {k: v.copy() for k, v in START_SHOP.items()}
        st.session_state.last_spin = None
        st.session_state.luck_multiplier = 1
        st.session_state.stats = {
            "items_bought": 0,
            "spins": 0,
            "money_earned": 0.0,
        }
        st.rerun()

# ============================================================
# SHOP
# ============================================================

elif page == "Shop":
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.title("🛍️ Shop")
    st.caption("Browse categories and click an item for details.")

    query = st.text_input(
        "Search items",
        placeholder="Try Bre, key, ura...",
    ).strip().casefold()

    category_choice = st.selectbox(
        "Category",
        ["All categories"] + list(CATEGORIES.keys()),
    )

    categories = (
        CATEGORIES.items()
        if category_choice == "All categories"
        else [(category_choice, CATEGORIES[category_choice])]
    )

    found = 0

    for category, items in categories:
        filtered = [
            item for item in items
            if query in pretty_name(item).casefold()
        ]

        if not filtered:
            continue

        st.divider()
        st.subheader(category)

        for start in range(0, len(filtered), 3):
            columns = st.columns(3)

            for column, item in zip(columns, filtered[start:start + 3]):
                found += 1
                price, stock = st.session_state.shop[item]

                with column:
                    with st.container(border=True):
                        st.markdown(
                            f"""
                            <div class="item-emoji">{emoji_for(item)}</div>
                            <div class="item-name">{pretty_name(item)}</div>
                            <div class="item-price">€{price:,.2f}</div>
                            <div class="item-stock">{stock} available</div>
                            """,
                            unsafe_allow_html=True,
                        )

                        if st.button(
                            "View item ↗",
                            key=f"view_{item}",
                            use_container_width=True,
                        ):
                            show_item_dialog(item)

    if found == 0:
        st.info("No items found. Try another search.")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# GAMBLING
# ============================================================

elif page == "Gambling":
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.title("🎰 Gambling")
    st.write("Free spins. Three reels. One big jackpot.")
    st.caption("Reel 1: 1.5s · Reel 2: 3.0s · Reel 3: 4.5s")
    st.warning("Virtual game money only.")

    if st.button("🎰 SPIN — FREE", use_container_width=True):
        symbols = ["🍋", "🍒", "🍇", "🍉", "⭐", "💎", "🔔", "🍊"]
        final_symbols = [random.choice(symbols) for _ in range(3)]

        if random.random() < 0.025:
            final_symbols = ["🍋", "🍋", "🍋"]

        reels = [st.empty() for _ in range(3)]
        start_time = time.time()
        stop_times = [1.5, 3.0, 4.5]

        while True:
            elapsed = time.time() - start_time

            for i, reel in enumerate(reels):
                symbol = (
                    random.choice(symbols)
                    if elapsed < stop_times[i]
                    else final_symbols[i]
                )
                reel.markdown(
                    f'<div class="slot">{symbol}</div>',
                    unsafe_allow_html=True,
                )

            if elapsed >= 4.5:
                break

            time.sleep(0.04)

        if final_symbols == ["🍋", "🍋", "🍋"]:
            reward = 1000
            st.markdown(
                '<div class="jackpot"><h1>🍋 JACKPOT 🍋</h1>'
                '<h2>+ €1,000</h2><h3>PERFECT MATCH!</h3></div>',
                unsafe_allow_html=True,
            )
            st.balloons()
        elif len(set(final_symbols)) == 1:
            reward = 500
        elif len(set(final_symbols)) == 2:
            reward = 100
        else:
            reward = 0

        st.session_state.money = round(st.session_state.money + reward, 2)
        st.session_state.stats["money_earned"] += reward
        st.session_state.stats["spins"] += 1
        st.session_state.last_spin = {
            "symbols": final_symbols,
            "reward": reward,
        }

        st.success(
            f"{' '.join(final_symbols)} — You won €{reward:,.2f}!"
        )
        st.metric("Updated balance", f"€{st.session_state.money:,.2f}")

    if st.session_state.last_spin:
        st.divider()
        st.caption("LAST RESULT")
        st.write(
            "  ".join(st.session_state.last_spin["symbols"])
            + f" · €{st.session_state.last_spin['reward']:,.2f}"
        )

    st.caption(
        "🍋 🍋 🍋 = €1,000 · Other triple = €500 · "
        "Double = €100 · Other = €0"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# ROLLS
# ============================================================

elif page == "ROLLS":
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.title("✨ R O L L S")
    st.caption("Roll for rare items. Every roll costs €100.")
    st.warning("Virtual game money only. Drops are random.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Rolls made", st.session_state.rolls_count)
    c2.metric("Money spent", f"€{st.session_state.rolls_spent:,.2f}")
    c3.metric("Unique drops", len(st.session_state.rolls_inventory))

    st.markdown(
        '<div style="padding:24px;border:1px solid #8b5cf6;border-radius:18px;'
        'background:linear-gradient(120deg,#21143e,#101a30);text-align:center">'
        '<h2>🎲 Ready to roll?</h2>'
        '<p>Common → Uncommon → Rare → Legendary → Mythical</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    if st.button("✨ ROLL NOW — €100", type="primary", use_container_width=True):
        if st.session_state.money < 100:
            st.error("Not enough money! You need €100.")
        else:
            with st.spinner("Rolling..."):
                time.sleep(0.7)
                perform_roll()
            st.rerun()

    if st.session_state.last_roll:
        st.divider()
        show_roll_reveal(st.session_state.last_roll)

    st.divider()
    st.subheader("📖 Drop collection")

    for rarity in ["Common", "Uncommon", "Rare", "Legendary", "Mythical"]:
        color = RARITY_COLORS[rarity]
        st.markdown(
            f"<h3 style='color:{color}'>{rarity}</h3>",
            unsafe_allow_html=True,
        )

        for item in [x for x in ROLL_ITEMS if x["rarity"] == rarity]:
            owned = st.session_state.rolls_inventory.get(item["name"], 0)

            animation_label = {
                "no": "",
                "yes": " ✨",
                "super": " 🌟",
                "supersuper": " 🌌💥",
            }[item["animation"]]

            st.write(
                f"{item['emoji']} **{item['name']}** — 1 in {item['odds']:,}"
                f"{animation_label} · Owned: {owned}"
            )

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# INVENTORY
# ============================================================

elif page == "Inventory":
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.title("🎒 Inventory")
    st.caption(
        "Use food and drinks to survive. "
        "Your ROLLS drops are collected here too."
    )

    if not st.session_state.inventory and not st.session_state.rolls_inventory:
        st.info("Your inventory is empty. Visit the shop or ROLLS.")
    else:
        if st.session_state.inventory:
            st.subheader("🛍️ Shop items")

            for item, quantity in list(st.session_state.inventory.items()):
                if quantity <= 0:
                    continue

                with st.container(border=True):
                    col1, col2, col3 = st.columns([1, 3, 1])

                    with col1:
                        st.markdown(
                            f"<div style='font-size:38px'>{emoji_for(item)}</div>",
                            unsafe_allow_html=True,
                        )

                    with col2:
                        st.markdown(f"**{pretty_name(item)}**")
                        st.caption(INFO[item][1])
                        st.caption(f"Quantity: {quantity}")

                        if item in FOOD_ITEMS:
                            st.caption("🍗 Restores 35 hunger")
                        elif item in DRINK_ITEMS:
                            st.caption("💧 Restores 40 thirst")

                    with col3:
                        button_label = (
                            "Use"
                            if item in FOOD_ITEMS
                            or item in DRINK_ITEMS
                            or item == "uranium"
                            else "Inspect"
                        )

                        if st.button(
                            button_label,
                            key=f"use_{item}",
                            use_container_width=True,
                        ):
                            use_item(item)

        st.divider()
        st.subheader("✨ ROLLS collection")

        if not st.session_state.rolls_inventory:
            st.caption("No ROLLS drops yet.")

        for item in ROLL_ITEMS:
            quantity = st.session_state.rolls_inventory.get(item["name"], 0)

            if quantity:
                color = RARITY_COLORS[item["rarity"]]

                st.markdown(
                    f"<div style='padding:12px;margin:6px 0;border:1px solid {color};"
                    f"border-radius:12px;background:#171329'>"
                    f"{item['emoji']} <b>{html.escape(item['name'])}</b> — "
                    f"<span style='color:{color}'>{item['rarity']}</span>"
                    f" · 1 in {item['odds']:,} · Owned: {quantity}</div>",
                    unsafe_allow_html=True,
                )

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# STATS
# ============================================================

elif page == "Stats":
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.title("📊 Statistics")

    c1, c2 = st.columns(2)
    c1.metric("Current balance", f"€{st.session_state.money:,.2f}")
    c2.metric("Shop items bought", st.session_state.stats["items_bought"])

    c3, c4 = st.columns(2)
    c3.metric("Gambling spins", st.session_state.stats["spins"])
    c4.metric(
        "Gambling earnings",
        f"€{st.session_state.stats['money_earned']:,.2f}",
    )

    st.divider()
    st.subheader("✨ ROLLS statistics")

    r1, r2, r3 = st.columns(3)
    r1.metric("Rolls made", st.session_state.rolls_count)
    r2.metric("Money spent", f"€{st.session_state.rolls_spent:,.2f}")
    r3.metric("Unique drops", len(st.session_state.rolls_inventory))

    st.divider()
    st.subheader("Survival status")
    st.write(f"Hunger: {int(st.session_state.hunger)}%")
    st.progress(int(st.session_state.hunger))
    st.write(f"Thirst: {int(st.session_state.thirst)}%")
    st.progress(int(st.session_state.thirst))

    st.divider()
    st.subheader("Drop collection")

    if st.session_state.rolls_inventory:
        for item in ROLL_ITEMS:
            quantity = st.session_state.rolls_inventory.get(item["name"], 0)

            if quantity:
                st.write(
                    f"{item['emoji']} {item['name']} × {quantity} "
                    f"— {item['rarity']} — 1/{item['odds']:,}"
                )
    else:
        st.caption("No ROLLS drops collected yet.")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# CODES + ADMIN
# ============================================================

elif page == "Codes":
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.title("🔑 Codes")
    st.caption("Enter a code to unlock special features.")

    code = st.text_input(
        "Enter code",
        type="password",
        placeholder="Enter your code...",
        key="code_entry",
    )

    if st.button("🎟️ Redeem code", use_container_width=True):
        if code.strip() == "admin123":
            st.session_state.admin_unlocked = True
            st.success("Admin access unlocked!")
        else:
            st.error("Invalid code.")

    st.divider()

    if st.session_state.admin_unlocked:
        st.success("🔓 Admin access is active.")
        st.write("Open the admin panel to manage your game.")

        if st.button("🔐 Open Admin Panel", use_container_width=True):
            show_admin_panel()

        if st.button("Log out of admin", use_container_width=True):
            st.session_state.admin_unlocked = False
            st.session_state.luck_multiplier = 1
            st.success("Admin mode turned off.")
            st.rerun()
    else:
        st.info("Redeem the admin code to unlock the admin panel.")

    st.markdown("</div>", unsafe_allow_html=True)
