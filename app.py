
import random
import streamlit as st

st.set_page_config(
    page_title="My Shop",
    page_icon="🛒",
    layout="wide"
)

# ---------- GAME DATA ----------

if "money" not in st.session_state:
    st.session_state.money = 250.00

if "shop" not in st.session_state:
    st.session_state.shop = {
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
        "legendary_trophy": [2499.99, 1]
    }

if "inventory" not in st.session_state:
    st.session_state.inventory = {}

if "history" not in st.session_state:
    st.session_state.history = []

# ---------- DESIGN ----------

st.markdown("""
<style>
.stApp {
    background-color: #0b1020;
}
h1, h2, h3 {
    color: #93c5fd;
}
div[data-testid="stMetric"] {
    background: #17233d;
    padding: 16px;
    border-radius: 12px;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #334155;
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

st.title("🛒 My Shop")
st.caption("Buy items, earn money and build your collection.")

st.metric(
    "💰 Your money",
    f"€{st.session_state.money:,.2f}"
)

page = st.sidebar.radio(
    "Navigation",
    ["Shop", "Money Machine", "Inventory"]
)

# ---------- SHOP ----------

if page == "Shop":
    st.header("🛍️ Store")

    search = st.text_input("🔎 Search for an item")

    categories = {
        "All items": list(st.session_state.shop.keys()),
        "Food": [
            "bread", "cheese", "cola", "pancakes",
            "pizza", "burger", "fries", "chocolate",
            "cookie", "cake", "apple", "banana",
            "water", "energy_drink"
        ],
        "Electronics": [
            "headphones", "keyboard", "mouse", "monitor",
            "phone", "laptop", "gaming_pc", "controller"
        ],
        "Clothing": [
            "tshirt", "hoodie", "jeans", "sneakers", "cap"
        ],
        "Gaming": [
            "minecraft", "gaming_chair", "gaming_desk",
            "microphone", "webcam"
        ],
        "Rare items": [
            "diamond", "gold_bar", "mystery_box",
            "legendary_trophy"
        ]
    }

    category = st.selectbox(
        "Category",
        list(categories.keys())
    )

    items = [
        name for name in categories[category]
        if search.lower() in name.lower()
    ]

    if not items:
        st.info("No items found.")

    for start in range(0, len(items), 3):
        columns = st.columns(3)

        for col, name in zip(columns, items[start:start + 3]):
            with col:
                price, stock = st.session_state.shop[name]

                with st.container(border=True):
                    st.subheader(name.replace("_", " ").title())
                    st.markdown(f"### €{price:.2f}")
                    st.write(f"📦 Stock: {stock}")

                    quantity = st.number_input(
                        "Quantity",
                        min_value=1,
                        max_value=max(1, stock),
                        value=1,
                        step=1,
                        key=f"quantity_{name}",
                        disabled=stock == 0
                    )

                    if stock == 0:
                        st.error("Out of stock")

                    if st.button(
                        "Buy item",
                        key=f"buy_{name}",
                        use_container_width=True,
                        disabled=stock == 0
                    ):
                        total = round(price * quantity, 2)

                        if total > st.session_state.money:
                            st.error(
                                f"You need €{total - st.session_state.money:.2f} more."
                            )
                        else:
                            st.session_state.money = round(
                                st.session_state.money - total, 2
                            )

                            st.session_state.shop[name][1] -= quantity

                            inventory = st.session_state.inventory
                            inventory[name] = (
                                inventory.get(name, 0) + quantity
                            )

                            st.session_state.history.append(
                                f"Bought {quantity}x {name} for €{total:.2f}"
                            )

                            st.session_state.notice = (
                                f"Successfully bought {quantity}x "
                                f"{name.replace('_', ' ')}!"
                            )
                            st.rerun()

    if "notice" in st.session_state:
        st.success(st.session_state.pop("notice"))

# ---------- FREE MONEY MACHINE ----------

elif page == "Money Machine":
    st.header("💰 Free Money Machine")
    st.write("Spin for free. You cannot lose money!")

    st.info("Every spin gives you at least €5.")

    if st.button("🎰 SPIN THE MACHINE", use_container_width=True):
        reward = random.choices(
            [5, 10, 20, 50, 100],
            weights=[40, 30, 20, 8, 2]
        )[0]

        st.session_state.money = round(
            st.session_state.money + reward, 2
        )

        st.session_state.history.append(
            f"Money Machine: +€{reward:.2f}"
        )

        st.success(f"You earned €{reward:.2f}!")
        st.rerun()

# ---------- INVENTORY ----------

elif page == "Inventory":
    st.header("🎒 Your Inventory")

    inventory = st.session_state.inventory

    if not inventory:
        st.info("Your inventory is empty. Buy something in the shop!")
    else:
        for name, quantity in inventory.items():
            st.write(
                f"**{name.replace('_', ' ').title()}** × {quantity}"
            )

    st.divider()
    st.subheader("📦 Remaining Shop Stock")

    for name, (price, stock) in st.session_state.shop.items():
        st.write(
            f"{name.replace('_', ' ').title()} — "
            f"€{price:.2f} — {stock} left"
        )

    st.divider()
    st.subheader("📜 Transaction History")

    if st.session_state.history:
        for entry in reversed(st.session_state.history):
            st.write(f"• {entry}")
    else:
        st.info("No transactions yet.")
