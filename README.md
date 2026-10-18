# Smart Food Delivery Order Tracking System

## 📌 Project Overview

The **Smart Food Delivery Order Tracking System** is a Python-based application designed to manage food orders and track their delivery status. It provides a simple graphical user interface (GUI) using Tkinter, allowing users to place orders, view order details, update delivery status, cancel eligible orders, and generate sales reports.

The project demonstrates the use of Python functions, nested lists, file handling, conditional statements, loops, and GUI programming.

## 🎯 Objectives

- Manage food orders efficiently.
- Track order status from placement to delivery.
- Calculate order totals and delivered revenue.
- Search and filter orders easily.
- Store order information in a local text file.
- Provide a simple and user-friendly graphical interface.

## ✨ Features

- **Dashboard:** Displays total orders, active orders, delivered orders, and delivered revenue.
- **Place Order:** Accepts customer name, food item, quantity, and price.
- **View Order Details:** Displays complete information about a selected order.
- **Update Order Status:** Progresses orders through Placed, Preparing, Out for Delivery, and Delivered.
- **Cancel Order:** Allows cancellation of orders that are still Placed or Preparing.
- **Search Orders:** Searches by order ID, customer name, or food item.
- **Filter Orders:** Filters orders according to their current status.
- **Sales Report:** Shows order counts, delivered revenue, active order value, and the highest-value order.
- **Data Persistence:** Saves order information in `orders.txt` so it can be loaded in future sessions.

## 🛠️ Technologies Used

- **Programming Language:** Python
- **GUI Library:** Tkinter
- **Data Structure:** Nested lists
- **File Handling:** Text file (`orders.txt`)
- **Development Environment:** Visual Studio Code / Python IDLE / Terminal

## 📂 Project Structure

```text
SmartFoodDelivery/
│
├── food_delivery.py
│   └── Console-based application
│
├── food_delivery_gui.py
│   └── Tkinter graphical application
│
├── orders.txt
│   └── Saved order records (created automatically)
│
└── README.md
    └── Project documentation
```

## ⚙️ Requirements

- Python 3.10 or later recommended.
- Tkinter, usually included with standard Python installations.
- No third-party Python packages are required for the GUI version.

## 🚀 Installation and Execution

### Step 1: Download or clone the project

Place the project files in a folder named `SmartFoodDelivery`.

### Step 2: Open the project folder

Open PowerShell or a terminal in the project directory.

### Step 3: Run the GUI application

```bash
python food_delivery_gui.py
```

### Step 4: Run the console application (optional)

```bash
python food_delivery.py
```

The GUI and console applications are separate entry points. They can share the same `orders.txt` file when they use the same order format.

## 📋 Order Status Workflow

```text
Placed
  ↓
Preparing
  ↓
Out for Delivery
  ↓
Delivered
```

Orders can be cancelled while their status is Placed or Preparing.

## 💾 Data Storage

Each order is stored as a nested list with the following structure:

```python
[order_id, customer_name, food_item, quantity, price, status]
```

Example:

```python
[1001, "Amit", "Burger", 2, 120.0, "Delivered"]
```

Order records are stored in `orders.txt` using a pipe-separated format. The application loads saved records when it starts.

## 🧮 Order Total Calculation

The total cost of an order is calculated as:

**Order Total = Quantity × Price per Item**

For example, if a customer orders 2 burgers at ₹120 each:

**Order Total = 2 × 120 = ₹240**

## 📚 Concepts Demonstrated

- Python lists and nested lists
- Functions and modular programming
- Loops and conditional statements
- Input validation
- Searching and filtering
- Sorting and aggregation
- File reading and writing
- Exception handling
- Tkinter widgets and event handling
- Basic GUI-based application design

## 🔮 Future Enhancements

- Add customer contact details.
- Introduce food categories and menu selection.
- Add estimated delivery time.
- Improve the interface with order-status colors.
- Export sales reports to CSV.
- Add user authentication and role-based access.
- Integrate a database for larger datasets.

## 👩‍💻 Author

**Nilakshi Kuldhar**

B.Tech – Information Technology (Honours in Cyber Security)

Sanjivani College of Engineering

## 📄 License

This project was developed for educational and academic purposes.
