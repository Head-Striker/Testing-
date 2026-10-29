
import streamlit as st
import random
import time

st.set_page_config(
    page_title="Game Shop",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# DATA
# -----------------------------

START_SHOP = {
    "bread": [4.99, 15],
    "cheese": [6.99, 23],
    "cola": [2.67, 36],
    "pancakes": [3.25, 36],
    "pizza": [8.99, 20],
    "burger": [6.50, 25],
    "fries": [3.49, 30],
    "chocolate": [2.99, 40],
    "cookie": [1.25, 50],
    "cake": [5.99, 15],
    "apple": [0.75, 60],
    "banana": [0.60, 60],
    "water": [1.00, 50],
    "energy_drink": [3.50, 25],

    "headphones": [49.99, 10],
    "keyboard": [79.99, 8],
    "mouse": [39.99, 12],
    "monitor": [199.99, 5],
    "phone": [699.99, 4],
    "laptop": [999.99, 3],
    "gaming_pc": [1499.99, 2],
    "controller": [59.99, 10],

    "tshirt": [19.99, 20],
    "hoodie": [49.99, 15],
    "jeans": [39.99, 18],
    "sneakers": [89.99, 10],
    "cap": [14.99, 20],

    "minecraft": [29.99, 10],
    "gaming_chair": [249.99, 4],
    "gaming_desk": [179.99, 5],
    "microphone": [69.99, 8],
    "webcam": [49.99, 10],

    "diamond": [499.99, 3],
    "gold_bar": [999.99, 2],
    "mystery_box": [24.99, 20],
    "legendary_trophy": [2499.99, 1],
    "uranium": [1999.99, 1],
}

CATEGORIES = {
    "Food & Drinks": [
        "bread", "cheese", "cola", "pancakes", "pizza",
        "burger", "fries", "chocolate", "cookie", "cake",
        "apple", "banana", "water", "energy_drink",
    ],
    "Electronics": [
        "headphones", "keyboard", "mouse", "monitor",
        "phone", "laptop", "gaming_pc", "controller",
    ],
    "Clothing": [
        "tshirt", "hoodie", "jeans", "sneakers", "cap",
    ],
    "Gaming": [
        "minecraft", "gaming_chair", "gaming_desk",
        "microphone", "webcam",
    ],
    "Rare & Unusual": [
        "diamond", "gold_bar", "mystery_box",
        "legendary_trophy", "uranium",
    ],
}

INFO = {
    "bread": ("🍞", "You can eat this.", True),
    "cheese": ("🧀", "A tasty snack.", True),
    "cola": ("🥤", "A refreshing drink.", True),
    "pancakes": ("🥞", "A stack of pancakes.", True),
    "pizza": ("🍕", "A delicious pizza.", True),
    "burger": ("🍔", "A classic burger.", True),
    "fries": ("🍟", "Crispy fries.", True),
    "chocolate": ("🍫", "Something sweet.", True),
    "cookie": ("🍪", "A freshly baked cookie.", True),
    "cake": ("🍰", "A slice of cake.", True),
    "apple": ("🍎", "A fresh apple.", True),
    "banana": ("🍌", "A ripe banana.", True),
    "water": ("💧", "A bottle of water.", True),
    "energy_drink": ("⚡", "An energy drink.", True),

    "headphones": ("🎧", "Listen to your favourite sounds.", False),
    "keyboard": ("⌨️", "A keyboard for your setup.", False),
    "mouse": ("🖱️", "A gaming mouse.", False),
    "monitor": ("🖥️", "A computer monitor.", False),
    "phone": ("📱", "A modern phone.", False),
    "laptop": ("💻", "A portable computer.", False),
    "gaming_pc": ("🖥️", "A powerful gaming PC.", False),
    "controller": ("🎮", "A gaming controller.", False),

    "tshirt": ("👕", "A casual T-shirt.", False),
    "hoodie": ("🧥", "A comfortable hoodie.", False),
    "jeans": ("👖", "A pair of jeans.", False),
    "sneakers": ("👟", "A pair of sneakers.", False),
    "cap": ("🧢", "A cap for your character.", False),

    "minecraft": ("⛏️", "A block-building adventure.", False),
    "gaming_chair": ("🪑", "A chair for your gaming setup.", False),
    "gaming_desk": ("🪵", "A desk for your setup.", False),
    "microphone": ("🎙️", "A microphone.", False),
    "webcam": ("📷", "A webcam.", False),

    "diamond": ("💎", "A rare and valuable diamond.", False),
    "gold_bar": ("🥇", "A precious gold bar.", False),
    "mystery_box": ("🎁", "What's inside? It's a mystery.", False),
    "legendary_trophy": ("🏆", "An extremely rare trophy.", False),
    "uranium": ("☢️", "Don't taste this. Fictional game item.", False),
}

# -----------------------------
# SESSION STATE
# -----------------------------

if "money" not in st.session_state:
    st.session_state.money = 250.00

if "shop" not in st.session_state:
    st.session_state.shop = {
        k: v.copy() for k, v in START_SHOP.items()
    }

if "inventory" not in st.session_state:
    st.session_state.inventory = {}

if "notice" not in st.session_state:
    st.session_state.notice = None

if "last_spin" not in st.session_state:
    st.session_state.last_spin = None

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "stats" not in st.session_state:
    st.session_state.stats = {
        "items_bought": 0,
        "spins": 0,
        "money_earned": 0.0,
    }

# -----------------------------
# CLEAN DESIGN
# -----------------------------

st.markdown("""
<style>
.stApp {
    background: #111310;
    color: #e8e9e3;
}

[data-testid="stSidebar"] {
    background: #191b17;
    border-right: 1px solid #30332c;
}

[data-testid="stSidebar"] * {
    color: #e8e9e3;
}

h1, h2, h3 {
    letter-spacing: -0.7px;
    color: #f0f0e9;
}

p, label {
    color: #c2c5ba;
}

div[data-testid="stMetric"] {
    background: #1c1f19;
    border: 1px solid #35392f;
    padding: 16px;
    border-radius: 12px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #191c17;
    border: 1px solid #30342c;
    border-radius: 14px;
}

div.stButton > button {
    background: #282c24;
    color: #eeeeE7;
    border: 1px solid #454a3e;
    border-radius: 9px;
    transition: background 0.2s ease, transform 0.2s ease;
}

div.stButton > button:hover {
    background: #373d30;
    border-color: #929982;
    transform: translateY(-1px);
}

.shop-item {
    text-align: left;
    padding: 5px 2px;
}

.item-emoji {
    font-size: 35px;
    margin-bottom: 9px;
}

.item-name {
    font-size: 16px;
    font-weight: 650;
    overflow-wrap: anywhere;
}

.item-price {
    margin-top: 6px;
    font-size: 14px;
    color: #c3c9ad;
}

.item-stock {
    color: #93988b;
    font-size: 12px;
    margin-top: 4px;
}

.slot {
    background: #20231c;
    border: 1px solid #646c52;
    border-radius: 12px;
    padding: 18px 3px;
    text-align: center;
    font-size: 45px;
    min-height: 100px;
}

@keyframes page-enter {
    from { opacity: 0.35; transform: translateY(5px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes jackpot-glow {
    0%, 100% { box-shadow: 0 0 0 #d6db9d; }
    50% { box-shadow: 0 0 28px #d6db9d; }
}

@keyframes green-nausea {
    0% { filter: hue-rotate(0deg); transform: translateX(0); }
    25% { filter: hue-rotate(75deg); transform: translateX(-3px); }
    50% { filter: hue-rotate(135deg); transform: translateX(3px); }
    75% { filter: hue-rotate(65deg); transform: translateX(-2px); }
    100% { filter: hue-rotate(0deg); transform: translateX(0); }
}

@keyframes fade-to-black {
    from { background: #242b1c; opacity: 0.15; }
    to { background: #000000; opacity: 1; }
}

.page-content {
    animation: page-enter 0.35s ease-out;
}

.jackpot {
    border: 1px solid #d6db9d;
    border-radius: 16px;
    padding: 22px;
    text-align: center;
    animation: jackpot-glow 1s ease-in-out infinite;
}

.game-over {
    background: #050505;
    color: white;
    padding: 42px 22px;
    text-align: center;
    border: 1px solid #353535;
    border-radius: 12px;
}

div[role="radiogroup"] {
    gap: 8px;
}

div[role="radiogroup"] label {
    background: #20231c;
    border: 1px solid #34382f;
    padding: 10px 12px;
    border-radius: 9px;
}

hr {
    border-color: #30342c;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HELPERS
# -----------------------------

def pretty_name(item):
    return item.replace("_", " ").title()

def emoji_for(item):
    return INFO.get(item, ("📦", "", False))[0]

def buy_item(item, quantity):
    price, stock = st.session_state.shop[item]
    total = round(price * quantity, 2)

    if stock < quantity:
        st.session_state.notice = ("error", "Not enough stock.")
    elif st.session_state.money < total:
        st.session_state.notice = ("error", "Not enough money.")
    else:
        st.session_state.money = round(
            st.session_state.money - total, 2
        )
        st.session_state.shop[item][1] -= quantity
        st.session_state.inventory[item] = (
            st.session_state.inventory.get(item, 0) + quantity
        )
        st.session_state.stats["items_bought"] += quantity
        st.session_state.notice = (
            "success", f"Bought {quantity} × {pretty_name(item)}."
        )

def use_item(item):
    quantity = st.session_state.inventory.get(item, 0)

    if quantity < 1:
        st.session_state.notice = ("error", "You don't own this item.")
        return

    if item == "uranium":
        # Fictional game effect only; no real-world instructions.
        st.session_state.inventory[item] -= 1
        if st.session_state.inventory[item] <= 0:
            del st.session_state.inventory[item]
        st.session_state.game_over = True
        st.rerun()

    can_eat = INFO.get(item, ("", "", False))[2]

    if can_eat:
        st.session_state.inventory[item] -= 1
        if st.session_state.inventory[item] <= 0:
            del st.session_state.inventory[item]
        st.session_state.notice = (
            "success", f"You used {pretty_name(item)}."
        )
    else:
        st.session_state.notice = (
            "info", INFO.get(item, ("", "You inspected this item.", False))[1]
        )

# -----------------------------
# ITEM DETAIL DIALOG
# -----------------------------

@st.dialog("Item details", width="small")
def item_dialog(item):
    price, stock = st.session_state.shop[item]
    emoji, description, consumable = INFO[item]

    st.markdown(
        f"<div style='font-size:75px;text-align:center'>{emoji}</div>",
        unsafe_allow_html=True
    )
    st.subheader(pretty_name(item))
    st.write(description)
    st.markdown(f"**€{price:,.2f}**")
    st.caption(f"{stock} in stock")

    if item == "uranium":
        st.warning("Don't taste this. This is a fictional game item.")

    if stock > 0:
        qty = st.number_input(
            "Quantity",
            min_value=1,
            max_value=stock,
            value=1,
            key=f"qty_{item}"
        )

        if st.button("Buy item", use_container_width=True):
            buy_item(item, qty)
            st.rerun()

# -----------------------------
# HEADER
# -----------------------------

if not st.session_state.game_over:
    top_left, top_right = st.columns([3, 1])

    with top_left:
        st.markdown("# ◈ GAME SHOP")
        st.caption("A little shop. A bigger collection.")

    with top_right:
        st.metric("BALANCE", f"€{st.session_state.money:,.2f}")

    if st.session_state.notice:
        kind, message = st.session_state.notice
        if kind == "success":
            st.success(message)
        elif kind == "error":
            st.error(message)
        else:
            st.info(message)
        st.session_state.notice = None

# -----------------------------
# NAVIGATION
# -----------------------------

page = st.sidebar.radio(
    "MENU",
    ["Shop", "Money Machine", "Inventory", "Stats"],
    format_func=lambda p: {
        "Shop": "◈   Shop",
        "Money Machine": "◎   Money Machine",
        "Inventory": "▤   Inventory",
        "Stats": "▥   Stats",
    }[p],
)

st.sidebar.divider()
st.sidebar.caption("YOUR ACCOUNT")
st.sidebar.metric("Balance", f"€{st.session_state.money:,.2f}")
st.sidebar.caption("Your progress is stored for this session.")

# -----------------------------
# GAME OVER EFFECT
# -----------------------------

if st.session_state.game_over:
    st.markdown("# ")
    effect = st.empty()

    st.markdown(
        """
        <div style="
            position:fixed; inset:0; z-index:9999;
            background:#000; pointer-events:none;
            animation:fade-to-black 10s linear forwards;">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            background:#27301c;
            color:#e4e8d9;
            padding:30px;
            border-radius:12px;
            text-align:center;
            animation:green-nausea 0.45s infinite;">
            <h1>⚠ GAME STATUS CRITICAL</h1>
            <p>Fictional status effect activated.</p>
            <p>Preparing game-over screen...</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Green screen effect for 10 seconds.
    for second in range(10):
        effect.markdown(
            f"""
            <div style="
                background:rgba(80,110,30,{0.12 + (second % 3) * 0.06});
                border:1px solid #555f36;
                padding:8px;border-radius:8px;text-align:center;">
                SYSTEM FAILURE · {second + 1}/10
            </div>
            """,
            unsafe_allow_html=True
        )
        time.sleep(1)

    # Black fade remains for the final five seconds.
    effect.markdown(
        """
        <div style="
            background:#000;color:#aaa;
            padding:20px;text-align:center;
            animation:fade-to-black 1s forwards;">
            CONNECTION LOST
        </div>
        """,
        unsafe_allow_html=True
    )
    time.sleep(5)

    st.markdown(
        """
        <div class="game-over">
            <div style="font-size:13px;letter-spacing:5px;color:#aaa">
                GAME SESSION ENDED
            </div>
            <h1 style="font-size:44px;margin-top:20px">
                WASTED
            </h1>
            <p>Character status: eliminated</p>
            <hr>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("SESSION STATISTICS")
    c1, c2, c3 = st.columns(3)
    c1.metric("Final balance", f"€{st.session_state.money:,.2f}")
    c2.metric("Items bought", st.session_state.stats["items_bought"])
    c3.metric("Spins played", st.session_state.stats["spins"])

    st.caption("This is a fictional game-over screen, not a real-world effect.")

    if st.button("Return to shop", use_container_width=True):
        st.session_state.game_over = False
        st.rerun()

# -----------------------------
# SHOP
# -----------------------------

elif page == "Shop":
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.header("Explore")
    st.caption("Browse a category and select an item to see its details.")

    search = st.text_input(
        "Search",
        placeholder="Find an item...",
        label_visibility="collapsed"
    )

    selected_category = st.selectbox(
        "Category",
        ["All categories"] + list(CATEGORIES.keys())
    )

    categories = (
        CATEGORIES.items()
        if selected_category == "All categories"
        else [(selected_category, CATEGORIES[selected_category])]
    )

    count = 0

    for category, items in categories:
        filtered = [
            item for item in items
            if search.lower() in pretty_name(item).lower()
        ]

        if not filtered:
            continue

        st.divider()
        st.subheader(category)

        for start in range(0, len(filtered), 3):
            cols = st.columns(3)

            for col, item in zip(cols, filtered[start:start + 3]):
                count += 1
                price, stock = st.session_state.shop[item]

                with col:
                    with st.container(border=True):
                        st.markdown(
                            f"""
                            <div class="shop-item">
                                <div class="item-emoji">{emoji_for(item)}</div>
                                <div class="item-name">{pretty_name(item)}</div>
                                <div class="item-price">€{price:,.2f}</div>
                                <div class="item-stock">{stock} available</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        if st.button(
                            "View details ↗",
                            key=f"view_{item}",
                            use_container_width=True
                        ):
                            item_dialog(item)

    if count == 0:
        st.info("No items found.")

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# MONEY MACHINE
# -----------------------------

elif page == "Money Machine":
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.header("Money Machine")
    st.caption("A free spin. No cost to play.")

    st.markdown(
        """
        <div style="
            background:#191c17;
            border:1px solid #373b30;
            padding:22px;border-radius:16px;">
            <div style="font-size:12px;letter-spacing:3px;color:#aeb39f">
                THREE REELS · FREE PLAY
            </div>
            <h3>Try your luck.</h3>
            <p style="color:#aeb39f">
                Match symbols to collect bonus money.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if st.button("SPIN  ↗", use_container_width=True):
        symbols = ["🍋", "🍒", "🍇", "🍉", "⭐", "💎", "🔔", "🍊"]

        # Make the jackpot rare but possible.
        if random.random() < 0.04:
            final_symbols = ["🍋", "🍋", "🍋"]
        else:
            final_symbols = [random.choice(symbols) for _ in range(3)]

        start = time.time()
        stops = [2, 5, 10]
        columns = st.columns(3)
        reels = []

        for col in columns:
            with col:
                reels.append(st.empty())

        # No progress bar. Each reel stops at its own time.
        while True:
            elapsed = time.time() - start

            for i, reel in enumerate(reels):
                symbol = (
                    random.choice(symbols)
                    if elapsed < stops[i]
                    else final_symbols[i]
                )

                reel.markdown(
                    f'<div class="slot">{symbol}</div>',
                    unsafe_allow_html=True
                )

            if elapsed >= 10:
                break

            time.sleep(0.08)

        if final_symbols == ["🍋", "🍋", "🍋"]:
            reward = 1000
            st.session_state.money += reward
            st.session_state.stats["money_earned"] += reward
            st.markdown(
                """
                <div class="jackpot">
                    <div style="font-size:12px;letter-spacing:4px">
                        JACKPOT
                    </div>
                    <div style="font-size:58px">🍋 🍋 🍋</div>
                    <h1>+ €1,000</h1>
                    <p>PERFECT MATCH</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.balloons()
        elif len(set(final_symbols)) == 1:
            reward = 25
            st.session_state.money += reward
            st.session_state.stats["money_earned"] += reward
            st.success(f"Triple match! You won €{reward}.")
        elif len(set(final_symbols)) == 2:
            reward = 10
            st.session_state.money += reward
            st.session_state.stats["money_earned"] += reward
            st.success(f"Two symbols match! You won €{reward}.")
        else:
            reward = 0
            st.info("No match this time. Better luck next spin!")

        st.session_state.stats["spins"] += 1
        st.session_state.last_spin = {
            "symbols": final_symbols,
            "reward": reward,
        }

        st.metric("Updated balance", f"€{st.session_state.money:,.2f}")

    if st.session_state.last_spin:
        st.divider()
        st.caption("LAST RESULT")
        st.write(
            "  ".join(st.session_state.last_spin["symbols"])
            + f"   ·   €{st.session_state.last_spin['reward']:,.2f}"
        )

    st.caption("🍋 🍋 🍋 = €1,000 · Triple = €25 · Pair = €10 · Other = €0")
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# INVENTORY
# -----------------------------

elif page == "Inventory":
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.header("Inventory")
    st.caption("Everything you own, in one place.")

    if not st.session_state.inventory:
        st.info("Your inventory is empty. Visit the shop to collect items.")
    else:
        for item, quantity in list(st.session_state.inventory.items()):
            with st.container(border=True):
                c1, c2, c3 = st.columns([1, 3, 1])

                with c1:
                    st.markdown(
                        f"<div style='font-size:36px'>{emoji_for(item)}</div>",
                        unsafe_allow_html=True
                    )

                with c2:
                    st.markdown(f"**{pretty_name(item)}**")
                    st.caption(INFO[item][1])
                    st.caption(f"Quantity: {quantity}")

                with c3:
                    if item == "uranium":
                        button_text = "Use item"
                    elif INFO[item][2]:
                        button_text = "Eat / use"
                    else:
                        button_text = "Inspect"

                    if st.button(
                        button_text,
                        key=f"use_{item}",
                        use_container_width=True
                    ):
                        use_item(item)
                        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# STATS
# -----------------------------

elif page == "Stats":
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.header("Statistics")
    st.caption("Your progress this session.")

    c1, c2 = st.columns(2)
    c1.metric("Current balance", f"€{st.session_state.money:,.2f}")
    c2.metric("Items bought", st.session_state.stats["items_bought"])

    c3, c4 = st.columns(2)
    c3.metric("Spins played", st.session_state.stats["spins"])
    c4.metric(
        "Money earned from machine",
        f"€{st.session_state.stats['money_earned']:,.2f}"
    )

    st.divider()
    st.subheader("Inventory summary")
    st.write(f"Unique items owned: {len(st.session_state.inventory)}")
    st.write(
        "Total item quantity: "
        + str(sum(st.session_state.inventory.values()))
    )

    st.markdown("</div>", unsafe_allow_html=True)
