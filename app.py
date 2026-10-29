
import streamlit as st
import random
import time

st.set_page_config(
    page_title="My Game Shop",
    page_icon="🛍️",
    layout="wide"
)

# -------------------------
# SHOP ITEMS
# -------------------------

START_SHOP = {
    # Food
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

    # Electronics
    "headphones": [49.99, 10],
    "keyboard": [79.99, 8],
    "mouse": [39.99, 12],
    "monitor": [199.99, 5],
    "phone": [699.99, 4],
    "laptop": [999.99, 3],
    "gaming_pc": [1499.99, 2],
    "controller": [59.99, 10],

    # Clothing
    "tshirt": [19.99, 20],
    "hoodie": [49.99, 15],
    "jeans": [39.99, 18],
    "sneakers": [89.99, 10],
    "cap": [14.99, 20],

    # Gaming
    "minecraft": [29.99, 10],
    "gaming_chair": [249.99, 4],
    "gaming_desk": [179.99, 5],
    "microphone": [69.99, 8],
    "webcam": [49.99, 10],

    # Rare items
    "diamond": [499.99, 3],
    "gold_bar": [999.99, 2],
    "mystery_box": [24.99, 20],
    "legendary_trophy": [2499.99, 1],
}

CATEGORIES = {
    "🍔 Food & Drinks": [
        "bread", "cheese", "cola", "pancakes", "pizza",
        "burger", "fries", "chocolate", "cookie", "cake",
        "apple", "banana", "water", "energy_drink"
    ],
    "💻 Electronics": [
        "headphones", "keyboard", "mouse", "monitor",
        "phone", "laptop", "gaming_pc", "controller"
    ],
    "👕 Clothing": [
        "tshirt", "hoodie", "jeans", "sneakers", "cap"
    ],
    "🎮 Gaming": [
        "minecraft", "gaming_chair", "gaming_desk",
        "microphone", "webcam"
    ],
    "💎 Rare Items": [
        "diamond", "gold_bar", "mystery_box",
        "legendary_trophy"
    ],
}

ITEM_INFO = {
    "bread": ("🍞", "Fresh bread for your collection."),
    "cheese": ("🧀", "A tasty piece of cheese."),
    "cola": ("🥤", "A refreshing cola."),
    "pancakes": ("🥞", "A stack of delicious pancakes."),
    "pizza": ("🍕", "A classic pizza."),
    "burger": ("🍔", "A juicy burger."),
    "fries": ("🍟", "Crispy fries."),
    "chocolate": ("🍫", "Sweet chocolate."),
    "cookie": ("🍪", "A freshly baked cookie."),
    "cake": ("🍰", "A delicious slice of cake."),
    "apple": ("🍎", "A fresh apple."),
    "banana": ("🍌", "A ripe banana."),
    "water": ("💧", "A bottle of water."),
    "energy_drink": ("⚡", "An energy drink."),
    "headphones": ("🎧", "Listen to your favourite sounds."),
    "keyboard": ("⌨️", "A gaming keyboard."),
    "mouse": ("🖱️", "A precise gaming mouse."),
    "monitor": ("🖥️", "A computer monitor."),
    "phone": ("📱", "A modern phone."),
    "laptop": ("💻", "A portable computer."),
    "gaming_pc": ("🖥️", "A powerful gaming PC."),
    "controller": ("🎮", "A gaming controller."),
    "tshirt": ("👕", "A casual T-shirt."),
    "hoodie": ("🧥", "A comfortable hoodie."),
    "jeans": ("👖", "Classic jeans."),
    "sneakers": ("👟", "A pair of sneakers."),
    "cap": ("🧢", "A stylish cap."),
    "minecraft": ("⛏️", "A block-building adventure."),
    "gaming_chair": ("🪑", "A comfortable gaming chair."),
    "gaming_desk": ("🪵", "A desk for your gaming setup."),
    "microphone": ("🎙️", "A microphone for your setup."),
    "webcam": ("📷", "A webcam for video calls."),
    "diamond": ("💎", "A rare and valuable diamond."),
    "gold_bar": ("🥇", "A precious gold bar."),
    "mystery_box": ("🎁", "A mysterious box."),
    "legendary_trophy": ("🏆", "An extremely rare trophy."),
}

# -------------------------
# SESSION STATE
# -------------------------

if "money" not in st.session_state:
    st.session_state.money = 250.00

if "shop" not in st.session_state:
    st.session_state.shop = {
        key: value.copy() for key, value in START_SHOP.items()
    }

if "inventory" not in st.session_state:
    st.session_state.inventory = {}

if "notice" not in st.session_state:
    st.session_state.notice = None

if "last_spin" not in st.session_state:
    st.session_state.last_spin = None

# -------------------------
# DESIGN
# -------------------------

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at top left, #18233e 0%, transparent 45%),
        #0d111c;
    color: #f4f6ff;
}

h1, h2, h3 {
    letter-spacing: -0.5px;
}

div[data-testid="stMetric"] {
    background: #171e30;
    border: 1px solid #2b3650;
    padding: 16px;
    border-radius: 16px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #151c2c;
    border-color: #2b3650;
    border-radius: 16px;
}

div.stButton > button {
    border-radius: 10px;
    border: 1px solid #354363;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    border-color: #8b9dff;
    transform: translateY(-2px);
}

.shop-item {
    text-align: center;
    padding: 8px 0 2px 0;
}

.item-emoji {
    font-size: 42px;
    line-height: 1.5;
}

.item-name {
    font-weight: 700;
    font-size: 16px;
    overflow-wrap: anywhere;
}

.item-price {
    color: #9daeff;
    font-weight: 700;
    font-size: 15px;
}

.item-stock {
    color: #9ba6bd;
    font-size: 12px;
}

.slot {
    background: linear-gradient(145deg, #202b45, #111827);
    border: 2px solid #6177bc;
    border-radius: 18px;
    text-align: center;
    padding: 22px 4px;
    font-size: 48px;
    min-height: 110px;
}

.slot-label {
    text-align: center;
    color: #aab7d8;
    font-size: 12px;
    margin-bottom: 6px;
}

.machine-box {
    background: #151c2c;
    border: 1px solid #354363;
    border-radius: 22px;
    padding: 24px;
}

@keyframes glow {
    0% { box-shadow: 0 0 4px #667eea; }
    50% { box-shadow: 0 0 22px #667eea; }
    100% { box-shadow: 0 0 4px #667eea; }
}

.spinning {
    animation: glow 0.5s infinite;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# HELPERS
# -------------------------

def pretty_name(item):
    return item.replace("_", " ").title()

def item_emoji(item):
    return ITEM_INFO.get(item, ("📦", ""))[0]

def buy_item(item, quantity):
    price, stock = st.session_state.shop[item]
    total = round(price * quantity, 2)

    if quantity < 1:
        st.session_state.notice = ("error", "Choose at least 1 item.")
    elif stock < quantity:
        st.session_state.notice = ("error", "Not enough stock!")
    elif st.session_state.money < total:
        st.session_state.notice = ("error", "Not enough money!")
    else:
        st.session_state.money = round(
            st.session_state.money - total, 2
        )
        st.session_state.shop[item][1] -= quantity
        st.session_state.inventory[item] = (
            st.session_state.inventory.get(item, 0) + quantity
        )
        st.session_state.notice = (
            "success",
            f"Bought {quantity}x {pretty_name(item)}!"
        )

# -------------------------
# ITEM POP-UP
# -------------------------

@st.dialog("Item details", width="small")
def show_item(item):
    price, stock = st.session_state.shop[item]
    emoji, description = ITEM_INFO.get(item, ("📦", ""))

    st.markdown(
        f"<div style='text-align:center;font-size:90px'>{emoji}</div>",
        unsafe_allow_html=True
    )
    st.subheader(pretty_name(item))
    st.write(description)

    st.markdown(f"### €{price:.2f}")
    st.write(f"Available in stock: **{stock}**")

    if stock > 0:
        quantity = st.number_input(
            "Quantity",
            min_value=1,
            max_value=stock,
            value=1,
            step=1,
            key=f"detail_quantity_{item}"
        )

        if st.button("🛒 Buy now", key=f"detail_buy_{item}",
                     use_container_width=True):
            buy_item(item, quantity)
            st.rerun()
    else:
        st.warning("This item is out of stock.")

# -------------------------
# HEADER
# -------------------------

st.title("🛍️ My Game Shop")
st.caption("Collect items, manage your money and try the Money Machine.")

header1, header2 = st.columns([2, 1])
with header1:
    st.metric("💰 Your money", f"€{st.session_state.money:,.2f}")
with header2:
    st.metric(
        "🎒 Unique items owned",
        len(st.session_state.inventory)
    )

if st.session_state.notice:
    kind, message = st.session_state.notice
    if kind == "success":
        st.success(message)
    else:
        st.error(message)
    st.session_state.notice = None

# -------------------------
# NAVIGATION
# -------------------------

page = st.sidebar.radio(
    "Navigation",
    ["🛍️ Shop", "🎰 Money Machine", "🎒 Inventory"]
)

st.sidebar.divider()
st.sidebar.metric("💰 Balance", f"€{st.session_state.money:,.2f}")

# -------------------------
# SHOP
# -------------------------

if page == "🛍️ Shop":
    st.header("Explore the shop")
    st.write("Choose a category, then click an item to see more details.")

    search = st.text_input(
        "🔎 Search items",
        placeholder="Search for pizza, keyboard, diamond..."
    )

    category_choice = st.selectbox(
        "Category",
        ["All categories"] + list(CATEGORIES.keys())
    )

    categories_to_show = (
        CATEGORIES.items()
        if category_choice == "All categories"
        else [(category_choice, CATEGORIES[category_choice])]
    )

    found_items = 0

    for category_name, items in categories_to_show:
        matching_items = [
            item for item in items
            if search.lower() in pretty_name(item).lower()
        ]

        if not matching_items:
            continue

        st.markdown("---")
        st.subheader(category_name)

        # Three item cards per row
        for start in range(0, len(matching_items), 3):
            group = matching_items[start:start + 3]
            columns = st.columns(3)

            for column, item in zip(columns, group):
                found_items += 1
                price, stock = st.session_state.shop[item]
                emoji = item_emoji(item)

                with column:
                    with st.container(border=True):
                        st.markdown(
                            f"""
                            <div class="shop-item">
                                <div class="item-emoji">{emoji}</div>
                                <div class="item-name">
                                    {pretty_name(item)}
                                </div>
                                <div class="item-price">
                                    €{price:.2f}
                                </div>
                                <div class="item-stock">
                                    Stock: {stock}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        if st.button(
                            "View item",
                            key=f"view_{item}",
                            use_container_width=True
                        ):
                            show_item(item)

    if found_items == 0:
        st.info("No items found. Try another search.")

# -------------------------
# MONEY MACHINE
# -------------------------

elif page == "🎰 Money Machine":
    st.header("🎰 Money Machine")
    st.write(
        "Spin for free! Match symbols to earn bonus money. "
        "It costs nothing to play."
    )

    st.markdown('<div class="machine-box">', unsafe_allow_html=True)

    st.markdown("### ✨ Three-symbol bonus machine")
    st.caption(
        "The first reel stops at 5 seconds, the second at 10 seconds, "
        "and the final reel at 20 seconds."
    )

    symbols = ["🍋", "🍒", "🍇", "🍉", "⭐", "💎", "🔔", "🍊"]

    # Select the final result before animation starts.
    if st.button("🎰 SPIN — FREE", use_container_width=True):
        final_symbols = [random.choice(symbols) for _ in range(3)]

        # A matching triple of lemons always wins €100.
        if random.random() < 0.12:
            final_symbols = ["🍋", "🍋", "🍋"]

        start_time = time.time()

        reel_placeholders = st.columns(3)
        slot_boxes = []

        for i, col in enumerate(reel_placeholders):
            with col:
                st.markdown(
                    f'<div class="slot-label">REEL {i + 1}</div>',
                    unsafe_allow_html=True
                )
                slot_boxes.append(st.empty())

        progress = st.progress(0)
        status = st.empty()

        stop_times = [5, 10, 20]

        while True:
            elapsed = time.time() - start_time

            for i, box in enumerate(slot_boxes):
                if elapsed < stop_times[i]:
                    symbol = random.choice(symbols)
                    css_class = "slot spinning"
                else:
                    symbol = final_symbols[i]
                    css_class = "slot"

                box.markdown(
                    f'<div class="{css_class}">{symbol}</div>',
                    unsafe_allow_html=True
                )

            progress.progress(min(int(elapsed / 20 * 100), 100))

            if elapsed < 5:
                status.info("🎰 All three reels are spinning...")
            elif elapsed < 10:
                status.info("✅ Reel 1 stopped! Reels 2 and 3 are spinning...")
            elif elapsed < 20:
                status.info("✅ Reel 2 stopped! Final reel is spinning...")
            else:
                break

            time.sleep(0.10)

        # Calculate the reward.
        if final_symbols == ["🍋", "🍋", "🍋"]:
            reward = 100
            result_message = "🍋 🍋 🍋 — JACKPOT! You won €100!"
        elif len(set(final_symbols)) == 1:
            reward = 25
            result_message = "🎉 Triple match! You won €25!"
        elif len(set(final_symbols)) == 2:
            reward = 10
            result_message = "✨ Two symbols match! You won €10!"
        else:
            reward = 0
            result_message = "No match this time. Try again for free!"

        st.session_state.money = round(
            st.session_state.money + reward, 2
        )
        st.session_state.last_spin = {
            "symbols": final_symbols,
            "reward": reward
        }

        progress.progress(100)
        status.success("The machine has stopped!")

        st.markdown(
            f"""
            <div style="
                text-align:center;
                background:#202b45;
                padding:18px;
                border-radius:16px;
                margin-top:14px;
                font-size:20px;
                font-weight:bold;">
                {result_message}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.metric("💰 New balance", f"€{st.session_state.money:,.2f}")

    if st.session_state.last_spin:
        st.divider()
        st.write("**Last spin:**")
        st.markdown(
            " ".join(st.session_state.last_spin["symbols"])
            + f" — Reward: €{st.session_state.last_spin['reward']:.2f}"
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.caption(
        "Rewards: 🍋🍋🍋 = €100 · Other triple = €25 · "
        "Two matching symbols = €10 · No match = €0"
    )

# -------------------------
# INVENTORY
# -------------------------

elif page == "🎒 Inventory":
    st.header("🎒 Your inventory")

    if not st.session_state.inventory:
        st.info("Your inventory is empty. Visit the shop to buy items!")
    else:
        for item, quantity in st.session_state.inventory.items():
            emoji = item_emoji(item)
            price = st.session_state.shop[item][0]

            with st.container(border=True):
                col1, col2, col3 = st.columns([1, 3, 1])

                with col1:
                    st.markdown(
                        f"<div style='font-size:36px'>{emoji}</div>",
                        unsafe_allow_html=True
                    )
                with col2:
                    st.markdown(f"**{pretty_name(item)}**")
                    st.caption(f"Value per item: €{price:.2f}")
                with col3:
                    st.metric("Owned", quantity)

st.sidebar.divider()
st.sidebar.caption("Your game shop • Save your progress by keeping this session open.")
