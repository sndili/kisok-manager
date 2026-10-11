
import os

# -----------------------------
# 1. INVENTORY AND SALES DATA
# -----------------------------

stock = {
    "Bread": {"price": 65, "quantity": 20},
    "Milk": {"price": 60, "quantity": 15},
    "Sugar": {"price": 150, "quantity": 10},
    "Rice": {"price": 200, "quantity": 8}
}

sales_log = []
unique_products_sold = set()


# -----------------------------
# 2. WELCOME MESSAGE
# -----------------------------

def welcome():
    kiosk_name = input("Enter kiosk name: ").strip().title()
    owner_name = input("Enter owner's name: ").strip().title()

    if not kiosk_name:
        kiosk_name = "My Kiosk"

    if not owner_name:
        owner_name = "Kiosk Owner"

    print("=" * 40)
    print(f"Welcome to {kiosk_name}'s Kiosk Manager")
    print(f"Run by {owner_name}")
    print("=" * 40)

    return owner_name


# -----------------------------
# 3. LOAD SAVED INVENTORY
# -----------------------------

def load_inventory():
    if os.path.exists("inventory.txt"):
        with open("inventory.txt", "r") as file:
            saved_stock = {}

            for line in file:
                parts = line.strip().split(",")

                if len(parts) == 3:
                    name = parts[0]
                    price = int(parts[1])
                    quantity = int(parts[2])

                    saved_stock[name] = {
                        "price": price,
                        "quantity": quantity
                    }

            if saved_stock:
                stock.clear()
                stock.update(saved_stock)

    print("Inventory loaded successfully.")


# -----------------------------
# 4. VIEW STOCK
# -----------------------------

def view_stock():
    print("\n" + "=" * 40)
    print(f"{'Product':<15}{'Price (KES)':>12}{'Quantity':>12}")
    print("-" * 40)

    for name, details in stock.items():
        print(
            f"{name:<15}"
            f"{details['price']:>12}"
            f"{details['quantity']:>12}"
        )

    print("=" * 40)


# -----------------------------
# 5. VALIDATE WHOLE NUMBERS
# -----------------------------

def get_positive_integer(prompt):
    while True:
        value = input(prompt).strip()

        if value.isdigit() and int(value) > 0:
            return int(value)

        print("Please enter a valid whole number greater than zero.")


# -----------------------------
# 6. ADD OR RESTOCK PRODUCT
# -----------------------------

def restock_product():
    name = input("Enter product name: ").strip().title()

    if not name:
        print("Product name cannot be empty.")
        return

    if name in stock:
        quantity = get_positive_integer("Quantity to add: ")
        stock[name]["quantity"] += quantity
        print(f"{name} restocked successfully.")
        print(f"New quantity: {stock[name]['quantity']}")

    else:
        price = get_positive_integer("Enter price per unit (KES): ")
        quantity = get_positive_integer("Enter starting quantity: ")

        stock[name] = {
            "price": price,
            "quantity": quantity
        }

        print(f"{name} added to inventory successfully.")


# -----------------------------
# 7. SELL A PRODUCT
# -----------------------------

def sell_product():
    name = input("Enter product name: ").strip().title()

    if not name:
        print("Product name cannot be empty.")
        return

    if name not in stock:
        print("Product not found in inventory.")
        return

    quantity = get_positive_integer("How many units? ")

    if quantity <= stock[name]["quantity"]:
        total = stock[name]["price"] * quantity
        stock[name]["quantity"] -= quantity

        sale = (name, quantity, total)
        sales_log.append(sale)
        unique_products_sold.add(name)

        print(f"Sold {quantity} {name} for KES {total}.")
        print(f"Remaining stock: {stock[name]['quantity']}")

    else:
        print("Insufficient stock. No sale was recorded.")


# -----------------------------
# 8. VIEW SALES REPORT
# -----------------------------

def sales_report():
    print("\n========== SALES REPORT ==========")

    if not sales_log:
        print("No sales recorded in this session.")
        return

    print(f"{'Product':<15}{'Quantity':>10}{'Total (KES)':>15}")
    print("-" * 40)

    revenue = 0
    quantities_sold = {}

    for sale in sales_log:
        name, quantity, total = sale

        print(f"{name:<15}{quantity:>10}{total:>15}")

        revenue += total

        if name in quantities_sold:
            quantities_sold[name] += quantity
        else:
            quantities_sold[name] = quantity

    best_seller = max(quantities_sold, key=quantities_sold.get)

    print("-" * 40)
    print(f"Total revenue: KES {revenue}")
    print(f"Unique products sold: {len(unique_products_sold)}")
    print(f"Best-selling product: {best_seller}")
    print("==================================")


# -----------------------------
# 9. SEARCH PRODUCTS
# -----------------------------

def search_products():
    search_term = input("Enter product name or part of it: ").strip().lower()

    if not search_term:
        print("Please enter a search term.")
        return

    found = False

    for name, details in stock.items():
        if search_term in name.lower():
            print(
                f"{name}: KES {details['price']} per unit, "
                f"Quantity: {details['quantity']}"
            )
            found = True

    if not found:
        print("No matching products found.")


# -----------------------------
# 10. SAVE INVENTORY
# -----------------------------

def save_inventory():
    with open("inventory.txt", "w") as file:
        for name, details in stock.items():
            file.write(
                f"{name},{details['price']},{details['quantity']}\n"
            )

    print("Inventory saved successfully.")


# -----------------------------
# 11. SAVE SALES HISTORY
# -----------------------------

def save_sales():
    if sales_log:
        with open("sales.txt", "a") as file:
            for sale in sales_log:
                name, quantity, total = sale
                file.write(f"{name},{quantity},{total}\n")

        print("Sales history saved.")


# -----------------------------
# 12. MAIN MENU
# -----------------------------

def main_menu():
    print("\n========== MAIN MENU ==========")
    print("1. View Stock")
    print("2. Add/Restock a Product")
    print("3. Sell a Product")
    print("4. View Sales Report")
    print("5. Search Products")
    print("6. Exit")
    print("=" * 32)

    choice = input("Enter your choice: ").strip()

    if choice.isdigit():
        return int(choice)

    print("Invalid input. Please enter a number from 1 to 6.")
    return 0


# -----------------------------
# 13. RUN THE PROGRAM
# -----------------------------

def run_kiosk():
    owner_name = welcome()
    load_inventory()

    while True:
        choice = main_menu()

        if choice == 1:
            view_stock()

        elif choice == 2:
            restock_product()

        elif choice == 3:
            sell_product()

        elif choice == 4:
            sales_report()

        elif choice == 5:
            search_products()

        elif choice == 6:
            save_inventory()
            save_sales()
            print(f"Goodbye, {owner_name}!")
            break

        else:
            print("Please choose an option between 1 and 6.")


run_kiosk()
