
import streamlit as st
import random
import time

st.set_page_config(
    page_title="Game Shop",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- SHOP --------------------

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
    "water": ("💧", "Drink this to restore thirst."),
    "energy_drink": ("⚡", "A drink that restores thirst."),

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

# Food restores hunger; drinks restore thirst.
FOOD_ITEMS = {
    "bread", "cheese", "pancakes", "pizza", "burger", "fries",
    "chocolate", "cookie", "cake", "apple", "banana",
}
DRINK_ITEMS = {"cola", "water", "energy_drink"}

# -------------------- SESSION STATE --------------------

if "money" not in st.session_state:
    st.session_state.money = 250.00

if "shop" not in st.session_state:
    st.session_state.shop = {
        k: v.copy() for k, v in START_SHOP.items()
    }

# Add new items to existing sessions.
for item, data in START_SHOP.items():
    st.session_state.shop.setdefault(item, data.copy())

if "inventory" not in st.session_state:
    st.session_state.inventory = {}

if "notice" not in st.session_state:
    st.session_state.notice = None

if "last_spin" not in st.session_state:
    st.session_state.last_spin = None

if "hunger" not in st.session_state:
    st.session_state.hunger = 100.0

if "thirst" not in st.session_state:
    st.session_state.thirst = 100.0

if "survival_updated_at" not in st.session_state:
    st.session_state.survival_updated_at = time.time()

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "stats" not in st.session_state:
    st.session_state.stats = {
        "items_bought": 0,
        "spins": 0,
        "money_earned": 0.0,
    }

# -------------------- SURVIVAL TIMER --------------------

# Hunger and thirst decrease with real elapsed time.
now = time.time()
elapsed = max(0, now - st.session_state.survival_updated_at)
st.session_state.survival_updated_at = now

st.session_state.hunger = max(
    0, st.session_state.hunger - elapsed * 0.12
)
st.session_state.thirst = max(
    0, st.session_state.thirst - elapsed * 0.18
)

if st.session_state.hunger <= 0 or st.session_state.thirst <= 0:
    st.session_state.game_over = True

# -------------------- NEON DESIGN --------------------

st.markdown("""
<style>
.stApp {
    background-color: #10101b;
    background-image:
        radial-gradient(ellipse at 12% 8%, #51138a 0%, transparent 40%),
        radial-gradient(ellipse at 88% 75%, #07566a 0%, transparent 42%);
    background-attachment: fixed;
    color: #f7f2ff;
}

[data-testid="stAppViewContainer"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: rgba(25, 19, 41, 0.97);
    border-right: 2px solid #8c36d9;
}

h1, h2, h3 {
    color: #ffffff;
}

div[data-testid="stMetric"] {
    background: rgba(32, 24, 50, 0.94);
    border: 1px solid #7338a8;
    padding: 14px;
    border-radius: 14px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(31, 23, 49, 0.96);
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
    border-color: white;
}

.item-emoji {
    font-size: 40px;
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
    color: #c3b7d4;
    font-size: 12px;
    margin-top: 4px;
}

.slot {
    background: linear-gradient(145deg, #251a3f, #121b34);
    border: 2px solid #a84cff;
    border-radius: 16px;
    padding: 18px 3px;
    text-align: center;
    font-size: 42px;
    min-height: 95px;
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
    0%, 100% { box-shadow: 0 0 8px #ffdd45; }
    50% { box-shadow: 0 0 38px #ff9d00; }
}

.jackpot {
    background: linear-gradient(135deg, #541a8b, #a51b87, #df7914);
    border: 2px solid #ffe56a;
    border-radius: 18px;
    padding: 24px;
    text-align: center;
    animation: jackpot-glow 0.8s ease-in-out infinite;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HELPERS --------------------

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
        st.session_state.money = round(
            st.session_state.money - total, 2
        )
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
        st.session_state.notice = None
        st.rerun()

    if item in FOOD_ITEMS:
        st.session_state.hunger = min(
            100, st.session_state.hunger + 35
        )
        st.session_state.inventory[item] -= 1
        st.session_state.notice = (
            "success", f"You ate {pretty_name(item)}. Hunger restored!"
        )

    elif item in DRINK_ITEMS:
        st.session_state.thirst = min(
            100, st.session_state.thirst + 40
        )
        st.session_state.inventory[item] -= 1
        st.session_state.notice = (
            "success", f"You drank {pretty_name(item)}. Thirst restored!"
        )

    else:
        st.session_state.notice = (
            "info", INFO.get(item, ("", "You inspected this item."))[1]
        )

    if item in st.session_state.inventory:
        if st.session_state.inventory[item] <= 0:
            del st.session_state.inventory[item]

    st.rerun()

# -------------------- ITEM DETAILS --------------------

@st.dialog("Item details", width="small")
def item_dialog(item):
    price, stock = st.session_state.shop[item]
    emoji, description = INFO[item]

    st.markdown(
        f"<div style='font-size:80px;text-align:center'>{emoji}</div>",
        unsafe_allow_html=True,
    )
    st.subheader(pretty_name(item))
    st.write(description)

    if item == "uranium":
        st.warning("☢️ Don't taste this.")

    if item in FOOD_ITEMS:
        st.caption("🍽️ Using this restores hunger.")
    elif item in DRINK_ITEMS:
        st.caption("💧 Using this restores thirst.")

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

# Survival indicators
st.sidebar.markdown("### SURVIVAL")

st.sidebar.write(f"🍗 Hunger — {int(st.session_state.hunger)}%")
st.sidebar.progress(int(st.session_state.hunger))

st.sidebar.write(f"💧 Thirst — {int(st.session_state.thirst)}%")
st.sidebar.progress(int(st.session_state.thirst))

st.sidebar.caption("Food restores hunger. Drinks restore thirst.")

# Main-page survival status
top1, top2 = st.columns(2)

with top1:
    st.caption(f"🍗 HUNGER · {int(st.session_state.hunger)}%")
    st.progress(int(st.session_state.hunger))

with top2:
    st.caption(f"💧 THIRST · {int(st.session_state.thirst)}%")
    st.progress(int(st.session_state.thirst))

if st.session_state.hunger < 25:
    st.warning("Your hunger is low! Buy food and eat it in your inventory.")

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

# -------------------- GAME OVER --------------------

if st.session_state.game_over:
    st.title("☠️ GAME OVER")
    st.error(
        "Your character ran out of hunger or thirst, "
        "or triggered the fictional uranium game-over effect."
    )

    st.subheader("Session statistics")
    c1, c2, c3 = st.columns(3)
    c1.metric("Balance", f"€{st.session_state.money:,.2f}")
    c2.metric("Items bought", st.session_state.stats["items_bought"])
    c3.metric("Spins played", st.session_state.stats["spins"])

    if st.button("Start a new game", use_container_width=True):
        st.session_state.money = 250.00
        st.session_state.inventory = {}
        st.session_state.hunger = 100.0
        st.session_state.thirst = 100.0
        st.session_state.survival_updated_at = time.time()
        st.session_state.game_over = False
        st.session_state.shop = {
            k: v.copy() for k, v in START_SHOP.items()
        }
        st.session_state.last_spin = None
        st.session_state.stats = {
            "items_bought": 0,
            "spins": 0,
            "money_earned": 0.0,
        }
        st.rerun()

# -------------------- SHOP --------------------

elif page == "Shop":
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.title("🛍️ Shop")
    st.caption("Browse categories and click an item for details.")

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
    st.caption("Reel 1: 1.5s · Reel 2: 3.0s · Reel 3: 4.5s")

    if st.button("🎰 SPIN — FREE", use_container_width=True):
        symbols = ["🍋", "🍒", "🍇", "🍉", "⭐", "💎", "🔔", "🍊"]

        final_symbols = [random.choice(symbols) for _ in range(3)]
        stop_times = [1.5, 3.0, 4.5]

        # A rare special jackpot.
        if random.random() < 0.025:
            final_symbols = ["🍋", "🍋", "🍋"]

        # Create three columns so reels stay side by side.
        reel_columns = st.columns(3)
        reels = []

        for col in reel_columns:
            with col:
                reels.append(st.empty())

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

            if elapsed >= 4.5:
                break

            time.sleep(0.04)

        if final_symbols == ["🍋", "🍋", "🍋"]:
            reward = 1000
            result_text = "🍋 JACKPOT! You won €1,000!"
            st.balloons()

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

        elif len(set(final_symbols)) == 1:
            reward = 500
            result_text = "🎉 Triple match! You won €500!"

        elif len(set(final_symbols)) == 2:
            reward = 100
            result_text = "✨ Double match! You won €100!"

        else:
            reward = 0
            result_text = "No match. You won €0."

        st.session_state.money = round(
            st.session_state.money + reward, 2
        )
        st.session_state.stats["money_earned"] += reward
        st.session_state.stats["spins"] += 1
        st.session_state.last_spin = {
            "symbols": final_symbols,
            "reward": reward,
        }

        st.success(result_text)
        st.metric("Updated balance", f"€{st.session_state.money:,.2f}")

    if st.session_state.last_spin:
        st.divider()
        st.caption("LAST RESULT")
        st.write(
            "  ".join(st.session_state.last_spin["symbols"])
            + f"   ·   €{st.session_state.last_spin['reward']:,.2f}"
        )

    st.caption(
        "🍋 🍋 🍋 = €1,000 jackpot · Other triple = €500 · "
        "Double = €100 · Other = €0"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- INVENTORY --------------------

elif page == "Inventory":
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.title("🎒 Inventory")
    st.caption("Use your food and drinks to survive.")

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

                    if item in FOOD_ITEMS:
                        st.caption("🍗 Restores 35 hunger")
                    elif item in DRINK_ITEMS:
                        st.caption("💧 Restores 40 thirst")

                with col3:
                    if item in FOOD_ITEMS or item in DRINK_ITEMS or item == "uranium":
                        button_label = "Use item"
                    else:
                        button_label = "Inspect"

                    if st.button(
                        button_label,
                        key=f"use_{item}",
                        use_container_width=True,
                    ):
                        use_item(item)

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- STATS --------------------

elif page == "Stats":
    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.title("📊 Statistics")

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
    st.subheader("Survival status")
    st.write(f"Hunger: {int(st.session_state.hunger)}%")
    st.progress(int(st.session_state.hunger))
    st.write(f"Thirst: {int(st.session_state.thirst)}%")
    st.progress(int(st.session_state.thirst))

    st.divider()
    st.subheader("Collection")
    st.write(f"Unique items: {len(st.session_state.inventory)}")
    st.write(
        f"Total quantity: {sum(st.session_state.inventory.values())}"
    )

    st.markdown("</div>", unsafe_allow_html=True)
