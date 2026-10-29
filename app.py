
import streamlit as st
import random
import time

st.set_page_config(page_title="Game Shop", page_icon="🎮", layout="wide")

# -------------------- SHOP DATA --------------------

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
    "🍔 Food & Drinks": [
        "bread", "cheese", "cola", "pancakes", "pizza",
        "burger", "fries", "chocolate", "cookie", "cake",
        "apple", "banana", "water", "energy_drink",
    ],
    "💻 Electronics": [
        "headphones", "keyboard", "mouse", "monitor",
        "phone", "laptop", "gaming_pc", "controller",
    ],
    "👕 Clothing": [
        "tshirt", "hoodie", "jeans", "sneakers", "cap",
    ],
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
    "uranium": ("☢️", "Don't taste this.", False),
}

# -------------------- SESSION STATE --------------------

if "money" not in st.session_state:
    st.session_state.money = 250.00

if "shop" not in st.session_state:
    st.session_state.shop = {
        key: value.copy() for key, value in START_SHOP.items()
    }

# Add new items to existing sessions too.
for item, data in START_SHOP.items():
    st.session_state.shop.setdefault(item, data.copy())

if "inventory" not in st.session_state:
    st.session_state.inventory = {}

if "notice" not in st.session_state:
    st.session_state.notice = None

if "last_spin" not in st.session_state:
    st.session_state.last_spin = None

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "death_sequence_done" not in st.session_state:
    st.session_state.death_sequence_done = False

if "stats" not in st.session_state:
    st.session_state.stats = {
        "items_bought": 0,
        "spins": 0,
        "money_earned": 0.0,
    }

# -------------------- CSS DESIGN --------------------

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at top left, #38106a 0%, transparent 38%),
        radial-gradient(ellipse at bottom right, #063e54 0%, transparent 38%),
        #10101b;
    color: #f7f2ff;
}

[data-testid="stSidebar"] {
    background: #191329;
    border-right: 2px solid #8c36d9;
}

h1, h2, h3 {
    color: #ffffff;
    letter-spacing: -0.5px;
}

div[data-testid="stMetric"] {
    background: #201832;
    border: 1px solid #7338a8;
    padding: 16px;
    border-radius: 14px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(31, 23, 49, 0.94);
    border: 1px solid #563b78;
    border-radius: 15px;
}

div.stButton > button {
    background: linear-gradient(110deg, #7727d5, #bd26a7);
    color: white;
    border: 1px solid #d58cff;
    border-radius: 10px;
    font-weight: 650;
    transition: transform 0.18s ease, filter 0.18s ease;
}

div.stButton > button:hover {
    filter: brightness(1.2);
    transform: translateY(-2px);
    border-color: #ffffff;
}

.item-emoji {
    font-size: 42px;
    margin-bottom: 8px;
}

.item-name {
    font-size: 16px;
    font-weight: 700;
    overflow-wrap: anywhere;
}

.item-price {
    color: #50f0e1;
    font-weight: 700;
    margin-top: 6px;
}

.item-stock {
    color: #b5a9ca;
    font-size: 12px;
    margin-top: 4px;
}

.slot {
    background: linear-gradient(145deg, #251a3f, #121b34);
    border: 2px solid #a84cff;
    border-radius: 16px;
    padding: 18px 3px;
    text-align: center;
    font-size: 48px;
    min-height: 110px;
    box-shadow: 0 0 12px #6824a833;
}

@keyframes page-enter {
    from { opacity: 0.3; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

.page-content {
    animation: page-enter 0.35s ease-out;
}

@keyframes jackpot-glow {
    0%, 100% {
        box-shadow: 0 0 8px #ffdd45;
        transform: scale(1);
    }
    50% {
        box-shadow: 0 0 38px #ff9d00;
        transform: scale(1.015);
    }
}

.jackpot {
    background: linear-gradient(135deg, #541a8b, #a51b87, #df7914);
    border: 2px solid #ffe56a;
    border-radius: 18px;
    padding: 24px;
    text-align: center;
    animation: jackpot-glow 0.8s ease-in-out infinite;
}

@keyframes nausea {
    0% { filter: hue-rotate(0deg); transform: translateX(0); }
    25% { filter: hue-rotate(100deg); transform: translateX(-3px); }
    50% { filter: hue-rotate(180deg); transform: translateX(3px); }
    75% { filter: hue-rotate(80deg); transform: translateX(-2px); }
    100% { filter: hue-rotate(0deg); transform: translateX(0); }
}

.nausea-screen {
    background: #243d19;
    color: #eaffd9;
    padding: 28px;
    border-radius: 15px;
    border: 2px solid #91d62e;
    animation: nausea 0.5s infinite;
    text-align: center;
}

.game-over {
    background: #050505;
    color: white;
    padding: 45px 22px;
    text-align: center;
    border: 1px solid #333;
    border-radius: 12px;
}

div[role="radiogroup"] {
    gap: 8px;
}

div[role="radiogroup"] label {
    background: #211831;
    border: 1px solid #633b91;
    padding: 10px;
    border-radius: 9px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HELPERS --------------------

def pretty_name(item):
    return item.replace("_", " ").title()

def emoji_for(item):
    return INFO.get(item, ("📦", "", False))[0]

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
        # Fictional game-over effect.
        st.session_state.inventory[item] -= 1
        if st.session_state.inventory[item] <= 0:
            del st.session_state.inventory[item]
        st.session_state.game_over = True
        st.session_state.death_sequence_done = False
        st.rerun()

    can_eat = INFO.get(item, ("", "", False))[2]

    if can_eat:
        st.session_state.inventory[item] -= 1
        if st.session_state.inventory[item] <= 0:
            del st.session_state.inventory[item]
        st.session_state.notice = (
            "success", f"You used {pretty_name(item)}!"
        )
    else:
        st.session_state.notice = (
            "info", INFO.get(item, ("", "You inspected this item.", False))[1]
        )

# -------------------- ITEM POP-UP --------------------

@st.dialog("Item details", width="small")
def item_dialog(item):
    price, stock = st.session_state.shop[item]
    emoji, description, _ = INFO[item]

    st.markdown(
        f"<div style='font-size:80px;text-align:center'>{emoji}</div>",
        unsafe_allow_html=True
    )
    st.subheader(pretty_name(item))
    st.write(description)

    if item == "uranium":
        st.warning("☢️ Don't taste this.")

    st.markdown(f"### €{price:,.2f}")
    st.caption(f"{stock} available in stock")

    if stock > 0:
        quantity = st.number_input(
            "Quantity",
            min_value=1,
            max_value=stock,
            value=1,
            key=f"quantity_{item}",
        )
        if st.button("🛒 Buy item", use_container_width=True):
            buy_item(item, quantity)
            st.rerun()

# -------------------- NAVIGATION --------------------

page = st.sidebar.radio(
    "NAVIGATION",
    ["Shop", "Money Machine", "Inventory", "Stats"],
    format_func=lambda p: {
        "Shop": "🛍️   Shop",
        "Money Machine": "🎰   Money Machine",
        "Inventory": "🎒   Inventory",
        "Stats": "📊   Stats",
    }[p],
)

st.sidebar.divider()
st.sidebar.metric("💰 Balance", f"€{st.session_state.money:,.2f}")
st.sidebar.caption("Your game. Your collection.")

# -------------------- GAME OVER --------------------

if st.session_state.game_over:
    st.markdown("# ☢️ Critical game status")

    if not st.session_state.death_sequence_done:
        screen = st.empty()

        # The green nausea effect lasts 15 seconds.
        for second in range(15):
            if second < 10:
                screen.markdown(
                    f"""
                    <div class="nausea-screen">
                        <h2>SYSTEM FAILURE</h2>
                        <p>Fictional game effect...</p>
                        <h3>{second + 1}/15</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                # Black fade begins after 10 seconds.
                opacity = min((second - 9) / 5, 1)
                screen.markdown(
                    f"""
                    <div style="
                        background:rgba(0,0,0,{opacity});
                        color:white;padding:40px;text-align:center;
                        border-radius:12px;min-height:180px;">
                        <h2>CONNECTION LOST</h2>
                        <p>Game session ending...</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            time.sleep(1)

        st.session_state.death_sequence_done = True
        st.rerun()

    st.markdown(
        """
        <div class="game-over">
            <div style="letter-spacing:5px;color:#aaa">GAME SESSION ENDED</div>
            <h1 style="font-size:56px;margin-top:25px">WASTED</h1>
            <p>Character eliminated · Fictional game screen</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("SESSION STATISTICS")
    c1, c2, c3 = st.columns(3)
    c1.metric("Final balance", f"€{st.session_state.money:,.2f}")
    c2.metric("Items bought", st.session_state.stats["items_bought"])
    c3.metric("Spins played", st.session_state.stats["spins"])

    if st.button("Return to shop", use_container_width=True):
        st.session_state.game_over = False
        st.session_state.death_sequence_done = False
        st.rerun()

# -------------------- SHOP --------------------

elif page == "Shop":
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.title("🛍️ Shop")
    st.caption("Browse categories and click an item to view its details.")

    if st.session_state.notice:
        kind, message = st.session_state.notice
        if kind == "success":
            st.success(message)
        elif kind == "error":
            st.error(message)
        else:
            st.info(message)
        st.session_state.notice = None

    search = st.text_input(
        "Search items",
        placeholder="Try Bre, key, ura...",
    )
    query = search.strip().casefold()

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
                            item_dialog(item)

    if found == 0:
        st.info("No items found. Try another search.")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- MONEY MACHINE --------------------

elif page == "Money Machine":
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.title("🎰 Money Machine")
    st.write("Free spins. Three reels. One big jackpot.")
    st.caption("Reel 1 stops at 3.3s · Reel 2 at 6.6s · Reel 3 at 9.9s")

    # This button's callback runs a single complete spin.
    # Streamlit cannot process a second click while the spin is running.
    if st.button("🎰 SPIN — FREE", use_container_width=True):
        symbols = ["🍋", "🍒", "🍇", "🍉", "⭐", "💎", "🔔", "🍊"]

        if random.random() < 0.04:
            final_symbols = ["🍋", "🍋", "🍋"]
        else:
            final_symbols = [random.choice(symbols) for _ in range(3)]

        stop_times = [3.3, 6.6, 9.9]
        reels = [st.empty(), st.empty(), st.empty()]
        start_time = time.time()

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

            if elapsed >= 9.9:
                break

            time.sleep(0.05)

        if final_symbols == ["🍋", "🍋", "🍋"]:
            reward = 1000
            st.session_state.money = round(st.session_state.money + reward, 2)
            st.session_state.stats["money_earned"] += reward

            st.markdown(
                """
                <div class="jackpot">
                    <div style="letter-spacing:5px">JACKPOT</div>
                    <div style="font-size:60px;margin:10px">🍋 🍋 🍋</div>
                    <h1>+ €1,000</h1>
                    <h3>PERFECT MATCH!</h3>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.balloons()

        elif len(set(final_symbols)) == 1:
            reward = 25
            st.session_state.money += reward
            st.session_state.stats["money_earned"] += reward
            st.success("🎉 Triple match! You won €25!")

        elif len(set(final_symbols)) == 2:
            reward = 10
            st.session_state.money += reward
            st.session_state.stats["money_earned"] += reward
            st.success("✨ Two symbols match! You won €10!")

        else:
            reward = 0
            st.info("No match this time!")

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
            + f"   ·   Reward: €{st.session_state.last_spin['reward']:,.2f}"
        )

    st.caption("🍋 🍋 🍋 = €1,000 · Triple = €25 · Pair = €10 · Other = €0")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- INVENTORY --------------------

elif page == "Inventory":
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.title("🎒 Inventory")
    st.caption("Everything you own.")

    if st.session_state.notice:
        kind, message = st.session_state.notice
        if kind == "success":
            st.success(message)
        elif kind == "error":
            st.error(message)
        else:
            st.info(message)
        st.session_state.notice = None

    if not st.session_state.inventory:
        st.info("Your inventory is empty. Visit the shop to buy items.")
    else:
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

                with col3:
                    if INFO[item][2] or item == "uranium":
                        button_label = "Use item"
                    else:
                        button_label = "Inspect"

                    if st.button(
                        button_label,
                        key=f"use_{item}",
                        use_container_width=True,
                    ):
                        use_item(item)
                        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- STATS --------------------

elif page == "Stats":
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.title("📊 Statistics")
    st.caption("Your progress this session.")

    c1, c2 = st.columns(2)
    c1.metric("Current balance", f"€{st.session_state.money:,.2f}")
    c2.metric("Items bought", st.session_state.stats["items_bought"])

    c3, c4 = st.columns(2)
    c3.metric("Spins played", st.session_state.stats["spins"])
    c4.metric(
        "Machine earnings",
        f"€{st.session_state.stats['money_earned']:,.2f}",
    )

    st.divider()
    st.subheader("Collection")
    st.write(f"Unique items: {len(st.session_state.inventory)}")
    st.write(f"Total quantity: {sum(st.session_state.inventory.values())}")

    st.markdown("</div>", unsafe_allow_html=True)
