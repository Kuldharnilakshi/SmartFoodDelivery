
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from pathlib import Path

# Smart Food Delivery Order Tracking System
# Primary data structure: Nested list
# Order format: [ID, Customer, Food, Quantity, Price, Status]

STATUSES = ["Placed", "Preparing", "Out for Delivery", "Delivered"]
FILE_PATH = Path(__file__).with_name("orders.txt")

orders = []
next_order_id = 1001


def create_sample_orders():
    return [
        [1001, "Amit", "Burger", 2, 120.0, "Delivered"],
        [1002, "Priya", "Pizza", 1, 350.0, "Preparing"],
        [1003, "Rahul", "Biryani", 2, 220.0, "Out for Delivery"],
        [1004, "Sneha", "Pasta", 1, 180.0, "Placed"]
    ]


def find_order_index(order_id):
    for i in range(len(orders)):
        if orders[i][0] == order_id:
            return i
    return -1


def save_orders():
    try:
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            for order in orders:
                file.write("|".join(map(str, order)) + "\n")
    except OSError as error:
        messagebox.showerror("File Error", str(error))


def load_orders():
    global orders, next_order_id

    if not FILE_PATH.exists():
        orders = create_sample_orders()
        save_orders()
    else:
        loaded = []
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as file:
                for line in file:
                    fields = line.strip().split("|")
                    if len(fields) != 6:
                        continue
                    try:
                        order = [
                            int(fields[0]), fields[1], fields[2],
                            int(fields[3]), float(fields[4]), fields[5]
                        ]
                        if order[5] in STATUSES:
                            loaded.append(order)
                    except ValueError:
                        continue
            orders = loaded
        except OSError:
            orders = create_sample_orders()

    next_order_id = max(
        [order[0] for order in orders], default=1000
    ) + 1


class FoodDeliveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Food Delivery Order Tracking System")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)
        self.root.configure(bg="#f3f5f9")

        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="All")
        self.build_ui()
        self.refresh_orders()

    def build_ui(self):
        header = tk.Frame(self.root, bg="#172554", pady=16)
        header.pack(fill="x")

        tk.Label(
            header, text="SMART FOOD DELIVERY",
            font=("Segoe UI", 22, "bold"),
            fg="white", bg="#172554"
        ).pack()

        tk.Label(
            header, text="Order Tracking and Management System",
            font=("Segoe UI", 10),
            fg="#dbeafe", bg="#172554"
        ).pack(pady=(3, 0))

        cards = tk.Frame(self.root, bg="#f3f5f9", pady=12)
        cards.pack(fill="x", padx=18)

        self.total_label = self.make_card(cards, "TOTAL ORDERS")
        self.active_label = self.make_card(cards, "ACTIVE ORDERS")
        self.delivered_label = self.make_card(cards, "DELIVERED")
        self.revenue_label = self.make_card(cards, "DELIVERED REVENUE")

        toolbar = tk.Frame(self.root, bg="#f3f5f9")
        toolbar.pack(fill="x", padx=18, pady=5)

        tk.Button(
            toolbar, text="+ Place Order", command=self.place_order,
            bg="#2563eb", fg="white", font=("Segoe UI", 10, "bold"),
            padx=12, pady=7
        ).pack(side="left", padx=(0, 6))

        tk.Button(
            toolbar, text="View Details", command=self.view_order,
            padx=10, pady=7
        ).pack(side="left", padx=3)

        tk.Button(
            toolbar, text="Update Status", command=self.update_status,
            padx=10, pady=7
        ).pack(side="left", padx=3)

        tk.Button(
            toolbar, text="Cancel Order", command=self.cancel_order,
            padx=10, pady=7
        ).pack(side="left", padx=3)

        tk.Button(
            toolbar, text="Sales Report", command=self.sales_report,
            padx=10, pady=7
        ).pack(side="left", padx=3)

        searchbar = tk.Frame(self.root, bg="#f3f5f9")
        searchbar.pack(fill="x", padx=18, pady=8)

        tk.Label(
            searchbar, text="Search:",
            bg="#f3f5f9", font=("Segoe UI", 10)
        ).pack(side="left")

        search_entry = ttk.Entry(
            searchbar, textvariable=self.search_var, width=30
        )
        search_entry.pack(side="left", padx=7)
        search_entry.bind("<KeyRelease>", lambda event: self.refresh_orders())

        tk.Label(
            searchbar, text="Status:",
            bg="#f3f5f9", font=("Segoe UI", 10)
        ).pack(side="left", padx=(12, 4))

        status_filter = ttk.Combobox(
            searchbar, textvariable=self.status_var,
            values=["All"] + STATUSES, state="readonly", width=20
        )
        status_filter.pack(side="left")
        status_filter.bind(
            "<<ComboboxSelected>>", lambda event: self.refresh_orders()
        )

        table_frame = tk.Frame(self.root, bg="white")
        table_frame.pack(fill="both", expand=True, padx=18, pady=(4, 18))

        columns = (
            "id", "customer", "food", "quantity",
            "total", "status"
        )

        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=15
        )

        headings = [
            ("id", "Order ID", 85),
            ("customer", "Customer", 150),
            ("food", "Food Item", 180),
            ("quantity", "Qty", 65),
            ("total", "Total (Rs.)", 120),
            ("status", "Delivery Status", 190)
        ]

        for col, heading, width in headings:
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", lambda event: self.view_order())

        self.root.bind("<Return>", lambda event: self.refresh_orders())

    def make_card(self, parent, title):
        card = tk.Frame(
            parent, bg="white", padx=18, pady=12,
            highlightbackground="#dce2ed", highlightthickness=1
        )
        card.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(
            card, text=title, bg="white", fg="#64748b",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")

        value = tk.Label(
            card, text="0", bg="white", fg="#172554",
            font=("Segoe UI", 19, "bold")
        )
        value.pack(anchor="w", pady=(5, 0))
        return value

    def refresh_orders(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        query = self.search_var.get().strip().lower()
        selected_status = self.status_var.get()

        for order in orders:
            searchable = (
                str(order[0]) + " " + order[1] + " " + order[2]
            ).lower()

            if query and query not in searchable:
                continue

            if selected_status != "All" and order[5] != selected_status:
                continue

            total = order[3] * order[4]

            self.tree.insert(
                "", "end", iid=str(order[0]),
                values=(
                    order[0], order[1], order[2],
                    order[3], f"{total:.2f}", order[5]
                )
            )

        active = sum(
            1 for order in orders if order[5] != "Delivered"
        )
        delivered = sum(
            1 for order in orders if order[5] == "Delivered"
        )
        revenue = sum(
            order[3] * order[4]
            for order in orders if order[5] == "Delivered"
        )

        self.total_label.config(text=str(len(orders)))
        self.active_label.config(text=str(active))
        self.delivered_label.config(text=str(delivered))
        self.revenue_label.config(text=f"Rs. {revenue:.2f}")

    def selected_order(self):
        selection = self.tree.selection()

        if not selection:
            messagebox.showwarning(
                "Select Order", "Please select an order from the table."
            )
            return None

        order_id = int(selection[0])
        index = find_order_index(order_id)

        if index == -1:
            messagebox.showerror("Error", "Order not found.")
            return None

        return orders[index]

    def place_order(self):
        customer = simpledialog.askstring(
            "New Order", "Enter customer name:", parent=self.root
        )
        if customer is None:
            return

        customer = customer.strip()
        if not customer:
            messagebox.showwarning("Invalid Input", "Name cannot be empty.")
            return

        food = simpledialog.askstring(
            "New Order", "Enter food item:", parent=self.root
        )
        if food is None:
            return

        food = food.strip()
        if not food:
            messagebox.showwarning(
                "Invalid Input", "Food item cannot be empty."
            )
            return

        quantity = simpledialog.askinteger(
            "New Order", "Enter quantity:", minvalue=1, parent=self.root
        )
        if quantity is None:
            return

        price = simpledialog.askfloat(
            "New Order", "Enter price per item (Rs.):",
            minvalue=0.01, parent=self.root
        )
        if price is None:
            return

        global next_order_id
        order = [
            next_order_id, customer, food, quantity, price, "Placed"
        ]
        orders.append(order)
        next_order_id += 1

        save_orders()
        self.refresh_orders()

        messagebox.showinfo(
            "Order Placed",
            f"Order ID: {order[0]}\n"
            f"Total: Rs. {quantity * price:.2f}"
        )

    def view_order(self):
        order = self.selected_order()
        if order is None:
            return

        total = order[3] * order[4]

        messagebox.showinfo(
            f"Order #{order[0]}",
            f"Order ID: {order[0]}\n"
            f"Customer: {order[1]}\n"
            f"Food: {order[2]}\n"
            f"Quantity: {order[3]}\n"
            f"Price per item: Rs. {order[4]:.2f}\n"
            f"Total: Rs. {total:.2f}\n"
            f"Status: {order[5]}"
        )

    def update_status(self):
        order = self.selected_order()
        if order is None:
            return

        current_index = STATUSES.index(order[5])

        if current_index == len(STATUSES) - 1:
            messagebox.showinfo(
                "Order Complete", "This order is already delivered."
            )
            return

        next_status = STATUSES[current_index + 1]

        if messagebox.askyesno(
            "Update Status",
            f"Change order #{order[0]} from '{order[5]}' "
            f"to '{next_status}'?"
        ):
            order[5] = next_status
            save_orders()
            self.refresh_orders()

    def cancel_order(self):
        order = self.selected_order()
        if order is None:
            return

        if order[5] not in ["Placed", "Preparing"]:
            messagebox.showwarning(
                "Cannot Cancel",
                "Only Placed or Preparing orders can be cancelled."
            )
            return

        if messagebox.askyesno(
            "Cancel Order", f"Cancel order #{order[0]}?"
        ):
            orders.remove(order)
            save_orders()
            self.refresh_orders()
            messagebox.showinfo("Cancelled", "Order cancelled successfully.")

    def sales_report(self):
        total_orders = len(orders)
        delivered_orders = [
            order for order in orders if order[5] == "Delivered"
        ]

        revenue = sum(
            order[3] * order[4] for order in delivered_orders
        )
        pending_value = sum(
            order[3] * order[4]
            for order in orders if order[5] != "Delivered"
        )

        if orders:
            highest = max(orders, key=lambda order: order[3] * order[4])
            highest_text = (
                f"#{highest[0]} - {highest[2]} "
                f"(Rs. {highest[3] * highest[4]:.2f})"
            )
        else:
            highest_text = "No orders"

        report = (
            "SALES REPORT\n"
            "------------------------------\n"
            f"Total orders: {total_orders}\n"
            f"Delivered orders: {len(delivered_orders)}\n"
            f"Active orders: {total_orders - len(delivered_orders)}\n"
            f"Delivered revenue: Rs. {revenue:.2f}\n"
            f"Active order value: Rs. {pending_value:.2f}\n"
            f"Highest value order: {highest_text}"
        )

        messagebox.showinfo("Sales Report", report)


if __name__ == "__main__":
    load_orders()
    root = tk.Tk()
    app = FoodDeliveryApp(root)
    root.mainloop()
