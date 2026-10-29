
import random


shop = {
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


money = 250.00


def show_shop():
    print("\n===== SHOP =====")

    for item, stats in shop.items():
        price = stats[0]
        stock = stats[1]

        print(f"{item}: €{price:.2f} | {stock} in stock")


def buy_item():
    global money

    show_shop()

    items_wanted = input(
        "\nChoose an item (or type back): "
    ).lower().strip()

    if items_wanted == "back":
        return

    if items_wanted not in shop:
        print("This item is not in the shop.")
        return

    price = shop[items_wanted][0]
    stock = shop[items_wanted][1]

    print(f"Price: €{price:.2f}")
    print(f"In stock: {stock}")

    try:
        amount_wanted = int(
            input("How many do you want? ")
        )
    except ValueError:
        print("Please enter a valid whole number.")
        return

    if amount_wanted <= 0:
        print("You must buy at least 1 item.")
        return

    if amount_wanted > stock:
        print("There is not enough of this item.")
        return

    total = round(price * amount_wanted, 2)

    if total > money:
        print(f"You need €{total - money:.2f} more.")
        return

    confirm = input(
        f"Total: €{total:.2f}. Type buy to confirm: "
    ).lower().strip()

    if confirm != "buy":
        print("Purchase cancelled.")
        return

    money = round(money - total, 2)
    shop[items_wanted][1] -= amount_wanted

    print(f"You bought {amount_wanted}x {items_wanted}!")
    print(f"Money left: €{money:.2f}")


def money_machine():
    global money

    print("\n===== MONEY MACHINE =====")
    print("Free to use!")
    print("You cannot lose money.")
    input("Press ENTER to spin the machine...")

    reward = random.randint(1, 100)

    if reward <= 40:
        winnings = 5.00
    elif reward <= 70:
        winnings = 10.00
    elif reward <= 90:
        winnings = 20.00
    elif reward <= 98:
        winnings = 50.00
    else:
        winnings = 100.00

    money = round(money + winnings, 2)

    print("\nThe machine stopped!")
    print(f"You won €{winnings:.2f}!")
    print(f"Your balance is now €{money:.2f}")


def show_inventory():
    print("\n===== INVENTORY / SHOP STOCK =====")

    for item, stats in shop.items():
        print(f"{item}: {stats[1]} left in the shop")

    print(f"\nYour money: €{money:.2f}")


# MAIN GAME LOOP
while True:
    print("\n==========================")
    print(f"       MONEY: €{money:.2f}")
    print("==========================")
    print("1. Shop")
    print("2. Free Money Machine")
    print("3. View Stock")
    print("4. Quit")

    choice = input("\nChoose an option: ").strip()

    if choice == "1":
        buy_item()

    elif choice == "2":
        money_machine()

    elif choice == "3":
        show_inventory()

    elif choice == "4":
        print("Thanks for playing!")
        break

    else:
        print("Invalid option. Choose 1, 2, 3 or 4.")
