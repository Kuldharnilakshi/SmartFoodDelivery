
# ============================================================
# PROJECT: SMART FOOD DELIVERY ORDER TRACKING SYSTEM
# Language: Python
# Data Structure: Lists
# Programming Style: Functions
# Storage: Plain-text file
# ============================================================

FILE_NAME = "orders.txt"

# Each order:
# [Order ID, Customer, Food, Quantity, Unit Price, Status]


# STEP 1: SAMPLE DATA AND HELPER FUNCTIONS
print("Food Delivery Project Started!")

def create_sample_orders():
    return [
        [1001, "Amit", "Veg Burger", 2, 120.0, "Delivered"],
        [1002, "Priya", "Pizza", 1, 350.0, "Preparing"],
        [1003, "Rahul", "Biryani", 2, 220.0, "Placed"],
        [1004, "Neha", "Pasta", 1, 180.0, "Out for Delivery"],
        [1005, "Arjun", "Sandwich", 3, 90.0, "Delivered"]
    ]


def find_order_index(orders, order_id):
    for i in range(len(orders)):
        if orders[i][0] == order_id:
            return i
    return -1


def next_order_id(orders):
    if len(orders) == 0:
        return 1001

    highest_id = orders[0][0]

    for order in orders:
        if order[0] > highest_id:
            highest_id = order[0]

    return highest_id + 1


def calculate_order_total(order):
    return order[3] * order[4]


# STEP 2: PLACE AND DISPLAY ORDERS

def place_order(orders, customer, food, quantity, price):
    customer = customer.strip()
    food = food.strip()

    if customer == "" or food == "":
        print("Customer name and food item are required.")
        return False

    if quantity <= 0 or price < 0:
        print("Quantity must be positive and price cannot be negative.")
        return False

    order = [
        next_order_id(orders),
        customer,
        food,
        quantity,
        price,
        "Placed"
    ]

    orders.append(order)

    print("\nOrder placed successfully!")
    print("Order ID:", order[0])
    print("Order total: Rs.", round(calculate_order_total(order), 2))
    return True


def display_orders(orders):
    if len(orders) == 0:
        print("\nNo orders available.")
        return

    print("-" * 105)
    print(
        f"{'ID':<8}{'CUSTOMER':<16}{'FOOD':<22}"
        f"{'QTY':<7}{'PRICE':<12}{'TOTAL':<12}{'STATUS':<22}"
    )
    print("-" * 105)

    for order in orders:
        total = calculate_order_total(order)

        print(
            f"{order[0]:<8}"
            f"{order[1][:15]:<16}"
            f"{order[2][:21]:<22}"
            f"{order[3]:<7}"
            f"{order[4]:<12.2f}"
            f"{total:<12.2f}"
            f"{order[5]:<22}"
        )

    print("-" * 105)


def view_single_order(orders, order_id):
    index = find_order_index(orders, order_id)

    if index == -1:
        print("Order not found.")
        return

    order = orders[index]

    print("\n========== ORDER DETAILS ==========")
    print("Order ID :", order[0])
    print("Customer :", order[1])
    print("Food     :", order[2])
    print("Quantity :", order[3])
    print("Price    : Rs.", round(order[4], 2))
    print("Total    : Rs.", round(calculate_order_total(order), 2))
    print("Status   :", order[5])
    print("===================================")


# STEP 3: UPDATE STATUS AND CANCEL ORDERS

def update_order_status(orders, order_id):
    index = find_order_index(orders, order_id)

    if index == -1:
        print("Order not found.")
        return False

    order = orders[index]
    current_status = order[5]

    if current_status == "Cancelled" or current_status == "Delivered":
        print("This order cannot be updated further.")
        return False

    print("\nCurrent status:", current_status)
    print("1. Preparing")
    print("2. Out for Delivery")
    print("3. Delivered")

    choice = input("Choose new status: ").strip()

    if choice == "1":
        new_status = "Preparing"
    elif choice == "2":
        new_status = "Out for Delivery"
    elif choice == "3":
        new_status = "Delivered"
    else:
        print("Invalid choice.")
        return False

    valid_transition = (
        (current_status == "Placed" and new_status == "Preparing")
        or
        (current_status == "Preparing" and new_status == "Out for Delivery")
        or
        (current_status == "Out for Delivery" and new_status == "Delivered")
    )

    if not valid_transition:
        if current_status == new_status:
            print("Order already has this status.")
        else:
            print("Invalid status transition. Follow the delivery sequence.")
        return False

    order[5] = new_status
    print("Order status updated to:", new_status)
    return True


def cancel_order(orders, order_id):
    index = find_order_index(orders, order_id)

    if index == -1:
        print("Order not found.")
        return False

    order = orders[index]

    if order[5] == "Placed" or order[5] == "Preparing":
        order[5] = "Cancelled"
        print("Order cancelled successfully.")
        return True

    print("Only Placed or Preparing orders can be cancelled.")
    return False


# STEP 4: SEARCH AND FILTER ORDERS

def search_by_customer(orders, customer):
    results = []
    customer = customer.strip().lower()

    for order in orders:
        if customer in order[1].lower():
            results.append(order)

    print("\nSearch results by customer:")
    display_orders(results)


def search_by_food(orders, food):
    results = []
    food = food.strip().lower()

    for order in orders:
        if food in order[2].lower():
            results.append(order)

    print("\nSearch results by food:")
    display_orders(results)


def filter_by_status(orders, status):
    results = []
    status = status.strip().lower()

    for order in orders:
        if order[5].lower() == status:
            results.append(order)

    print("\nOrders with status:", status)
    display_orders(results)


def filter_by_minimum_total(orders, minimum_total):
    results = []

    for order in orders:
        if calculate_order_total(order) >= minimum_total:
            results.append(order)

    print("\nOrders at or above Rs.", minimum_total)
    display_orders(results)


def search_menu(orders):
    print("\n========== SEARCH AND FILTER ==========")
    print("1. Search by customer")
    print("2. Search by food")
    print("3. Search by order ID")
    print("4. Filter by status")
    print("5. Filter by minimum order value")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        search_by_customer(orders, input("Customer name: "))

    elif choice == "2":
        search_by_food(orders, input("Food name: "))

    elif choice == "3":
        order_id = read_integer("Order ID: ")
        if order_id is not None:
            view_single_order(orders, order_id)

    elif choice == "4":
        print("Available statuses: Placed, Preparing, Out for Delivery, Delivered, Cancelled")
        status = input("Enter status: ")
        filter_by_status(orders, status)

    elif choice == "5":
        minimum = read_price("Minimum order total: ")
        if minimum is not None:
            filter_by_minimum_total(orders, minimum)

    else:
        print("Invalid choice.")


# STEP 5: DASHBOARD AND REPORTS

def show_dashboard(orders):
    total_orders = len(orders)
    delivered = 0
    pending = 0
    cancelled = 0
    delivered_revenue = 0.0
    active_order_value = 0.0

    for order in orders:
        status = order[5]
        total = calculate_order_total(order)

        if status == "Delivered":
            delivered += 1
            delivered_revenue += total

        elif status == "Cancelled":
            cancelled += 1

        else:
            pending += 1
            active_order_value += total

    print("\n========== FOOD DELIVERY DASHBOARD ==========")
    print("Total orders         :", total_orders)
    print("Pending / active     :", pending)
    print("Delivered orders     :", delivered)
    print("Cancelled orders     :", cancelled)
    print("Delivered revenue    : Rs.", round(delivered_revenue, 2))
    print("Active order value   : Rs.", round(active_order_value, 2))
    print("=============================================\n")


def show_high_value_orders(orders, minimum_total):
    results = []

    for order in orders:
        if calculate_order_total(order) >= minimum_total:
            results.append(order)

    print("\nOrders at or above Rs.", minimum_total)
    display_orders(results)


def show_most_expensive_order(orders):
    if len(orders) == 0:
        print("No orders available.")
        return

    highest_order = orders[0]

    for order in orders:
        if calculate_order_total(order) > calculate_order_total(highest_order):
            highest_order = order

    print("\n========== MOST EXPENSIVE ORDER ==========")
    view_single_order(orders, highest_order[0])


def show_sales_report(orders):
    total_delivered = 0.0
    total_cancelled = 0.0
    total_active = 0.0

    for order in orders:
        amount = calculate_order_total(order)

        if order[5] == "Delivered":
            total_delivered += amount
        elif order[5] == "Cancelled":
            total_cancelled += amount
        else:
            total_active += amount

    print("\n========== SALES REPORT ==========")
    print("Delivered revenue : Rs.", round(total_delivered, 2))
    print("Cancelled value   : Rs.", round(total_cancelled, 2))
    print("Active order value: Rs.", round(total_active, 2))
    print("==================================")


# STEP 6: DEMONSTRATE ALL 11 LIST METHODS

def demonstrate_list_methods():
    foods = ["Pizza", "Burger", "Pasta"]

    print("\nOriginal list:", foods)

    # 1. append()
    foods.append("Biryani")
    print("1. append():", foods)

    # 2. extend()
    foods.extend(["Sandwich", "Noodles"])
    print("2. extend():", foods)

    # 3. insert()
    foods.insert(1, "Dosa")
    print("3. insert():", foods)

    # 4. remove()
    foods.remove("Pasta")
    print("4. remove():", foods)

    # 5. pop()
    removed = foods.pop()
    print("5. pop() removed:", removed)
    print("   Current list:", foods)

    # 6. index()
    print("6. index() of Burger:", foods.index("Burger"))

    # 7. count()
    foods.append("Pizza")
    print("7. count() of Pizza:", foods.count("Pizza"))

    # 8. sort()
    foods.sort()
    print("8. sort():", foods)

    # 9. reverse()
    foods.reverse()
    print("9. reverse():", foods)

    # 10. copy()
    copied_foods = foods.copy()
    print("10. copy():", copied_foods)

    # 11. clear()
    copied_foods.clear()
    print("11. clear():", copied_foods)


# STEP 7: SAVE AND LOAD ORDERS USING A TEXT FILE

def save_orders(orders):
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            for order in orders:
                customer = order[1].replace("|", "/").replace("\n", " ")
                food = order[2].replace("|", "/").replace("\n", " ")

                line = (
                    f"{order[0]}|{customer}|{food}|{order[3]}|"
                    f"{order[4]}|{order[5]}\n"
                )
                file.write(line)

        print("Orders saved successfully.")
        return True

    except OSError:
        print("Error: Could not save orders.")
        return False


def load_orders():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            orders = []

            for line in file:
                fields = line.rstrip("\n").split("|")

                if len(fields) != 6:
                    print("Skipping invalid order record.")
                    continue

                try:
                    order = [
                        int(fields[0]),
                        fields[1],
                        fields[2],
                        int(fields[3]),
                        float(fields[4]),
                        fields[5]
                    ]

                    valid_statuses = [
                        "Placed", "Preparing", "Out for Delivery",
                        "Delivered", "Cancelled"
                    ]

                    if (
                        order[0] <= 0
                        or order[1].strip() == ""
                        or order[2].strip() == ""
                        or order[3] <= 0
                        or order[4] < 0
                        or order[5] not in valid_statuses
                    ):
                        print("Skipping invalid order record.")
                        continue

                    if find_order_index(orders, order[0]) != -1:
                        print("Skipping duplicate order ID.")
                        continue

                    orders.append(order)

                except ValueError:
                    print("Skipping invalid order record.")

            return orders

    except FileNotFoundError:
        orders = create_sample_orders()
        save_orders(orders)
        return orders

    except OSError:
        print("Could not read the file. Loading sample orders.")
        return create_sample_orders()


# STEP 8: INPUT VALIDATION AND CONSOLE MENU

def read_integer(message):
    try:
        return int(input(message))
    except ValueError:
        print("Please enter a valid integer.")
        return None


def read_price(message):
    try:
        value = float(input(message))

        if value < 0:
            print("Price cannot be negative.")
            return None

        return value

    except ValueError:
        print("Please enter a valid amount.")
        return None


def show_menu():
    print("""
=========================================
    FOOD DELIVERY ORDER TRACKING
=========================================
1.  Dashboard
2.  View all orders
3.  Place a new order
4.  View one order
5.  Update order status
6.  Cancel an order
7.  Search and filter orders
8.  Sort orders by ID
9.  Sort orders by total value
10. Show sales report
11. Demonstrate list methods
12. Save orders
13. Show high-value orders
14. Show most expensive order
0.  Save and exit
=========================================
""")


def main():
    orders = load_orders()

    print("\nWelcome to the Smart Food Delivery System!")

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_dashboard(orders)

        elif choice == "2":
            display_orders(orders)

        elif choice == "3":
            customer = input("Customer name: ")
            food = input("Food item: ")

            quantity = read_integer("Quantity: ")

            if quantity is None:
                continue

            price = read_price("Price per item: ")

            if price is None:
                continue

            if place_order(orders, customer, food, quantity, price):
                save_orders(orders)

        elif choice == "4":
            order_id = read_integer("Order ID: ")
            if order_id is not None:
                view_single_order(orders, order_id)

        elif choice == "5":
            order_id = read_integer("Order ID: ")

            if order_id is not None:
                if update_order_status(orders, order_id):
                    save_orders(orders)

        elif choice == "6":
            order_id = read_integer("Order ID: ")

            if order_id is not None:
                if cancel_order(orders, order_id):
                    save_orders(orders)

        elif choice == "7":
            search_menu(orders)

        elif choice == "8":
            orders.sort(key=lambda order: order[0])
            print("\nOrders sorted by ID:")
            display_orders(orders)
            save_orders(orders)

        elif choice == "9":
            orders.sort(
                key=lambda order: calculate_order_total(order),
                reverse=True
            )
            print("\nOrders sorted by total value, highest first:")
            display_orders(orders)
            save_orders(orders)

        elif choice == "10":
            show_sales_report(orders)

        elif choice == "11":
            demonstrate_list_methods()

        elif choice == "12":
            save_orders(orders)

        elif choice == "13":
            minimum = read_price("Minimum order total: ")

            if minimum is not None:
                show_high_value_orders(orders, minimum)

        elif choice == "14":
            show_most_expensive_order(orders)

        elif choice == "0":
            save_orders(orders)
            print("Thank you for using the application!")
            break

        else:
            print("Invalid choice. Please try again.")


# PROGRAM ENTRY POINT

if __name__ == "__main__":
    main()
