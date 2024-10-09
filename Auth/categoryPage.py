import tkinter as tk
from tkinter import messagebox
from Auth import data

cart = []  # Items added to the cart
total_price = 0  # to store total price directly
DELIVERY_FEE = 50

# A simple LIFO stack class to handle back navigation
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return None if self.is_empty() else self.items.pop()

    def peek(self):
        return None if self.is_empty() else self.items[-1]


# Stack to store pages for "Back" functionality
page_stack = Stack()

class CategoryPage:
    def __init__(self, parent, category_name):
        self.root = tk.Toplevel(parent)  # Create a new window for the category page
        self.root.title(f"{category_name} Page")
        self.root.geometry("600x600")

        self.category_name = category_name
        self.items = data.categories.get(category_name, [])

        self.item_widgets = []  # Track the displayed items and their buttons

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.widgets()

        # Push the parent window to the stack
        page_stack.push(parent)

    def widgets(self):
        self.items_frame = tk.Frame(self.root)  # Frame for displaying the items
        self.items_frame.pack(pady=10)

        self.search_frame = tk.Frame(self.root)  # Frame for search entry and button
        self.search_frame.pack(pady=10)

        self.sort_frame = tk.Frame(self.root)  # Frame for sorting buttons
        self.sort_frame.pack(pady=10)

        self.control_frame = tk.Frame(self.root)  # Frame for control buttons like: view cart, back
        self.control_frame.pack(pady=10)

        self.display_items()
        self.create_search_widgets()
        self.create_sort_buttons()
        self.create_navigation_buttons()

    def display_items(self):
        for label, button in self.item_widgets:
            label.destroy()
            button.destroy()

        self.item_widgets.clear()

        # Display each item
        for item in self.items:
            item_text = f"{item['name']} - Price: {item['price']} - Brand: {item.get('brand', '')}"
            item_label = tk.Label(self.items_frame, text=item_text)
            item_label.pack(pady=5)

            add_to_cart_button = tk.Button(self.items_frame, text="Add to Cart", command=lambda i=item: self.add_to_cart(i))
            add_to_cart_button.pack(pady=5)

            self.item_widgets.append((item_label, add_to_cart_button))

    def create_search_widgets(self):
        search_label = tk.Label(self.search_frame, text="Search Item:")
        search_label.pack(side="left", padx=5)

        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.pack(side="left", padx=5)

        search_button = tk.Button(self.search_frame, text="Search", command=self.search_item)
        search_button.pack(side="left", padx=5)

    def create_sort_buttons(self):
        sort_asc_button = tk.Button(self.sort_frame, text="Sort Ascending", command=lambda: self.sort_items('asc'))
        sort_asc_button.pack(side="left", padx=5)

        sort_desc_button = tk.Button(self.sort_frame, text="Sort Descending", command=lambda: self.sort_items('desc'))
        sort_desc_button.pack(side="left", padx=5)

    def create_navigation_buttons(self):
        cart_button = tk.Button(self.control_frame, text="View Cart", command=self.view_cart)
        cart_button.pack(side="left", padx=5)

        back_button = tk.Button(self.control_frame, text="Back", command=self.go_back)
        back_button.pack(side="left", padx=5)

    def search_item(self):
        search_term = self.search_entry.get().strip().lower()
        if not search_term:
            messagebox.showinfo(title="Search", message="Please enter an item name.")
            return

        self.bubble_sort_by_name()

        index = self.binary_search(search_term, 0, len(self.items) - 1)

        if index != -1:
            item = self.items[index]
            item_text = f"{item['name']} - Price: {item['price']} - Brand: {item.get('brand', '')}"
            messagebox.showinfo("Search Result", item_text)
        else:
            messagebox.showinfo("Search Result", "Item not found.")

    def binary_search(self, target, left, right):
        while left <= right:
            mid = (left + right) // 2
            mid_item = self.items[mid]['name'].lower()

            if mid_item == target:
                return mid
            elif mid_item < target:
                left = mid + 1
            else:
                right = mid - 1

        return -1

    def sort_items(self, order):
        self.items = self.bubble_sort(self.items, order)
        self.display_items()

    def bubble_sort(self, items, order):
        n = len(items)
        for i in range(n):
            for j in range(0, n - i - 1):
                if (order == 'asc' and items[j]['price'] > items[j + 1]['price']) or (order == 'desc' and items[j]['price'] < items[j + 1]['price']):
                    items[j], items[j + 1] = items[j + 1], items[j]
        return items

    def bubble_sort_by_name(self):
        n = len(self.items)
        for i in range(n):
            for j in range(0, n - i - 1):
                if self.items[j]['name'].lower() > self.items[j + 1]['name'].lower():
                    self.items[j], self.items[j + 1] = self.items[j + 1], self.items[j]

    def add_to_cart(self, item):
        global total_price
        cart.append(item)
        total_price += item['price']  # Directly update total price
        messagebox.showinfo(title="Cart", message=f"Added {item['name']} to cart!")

    def view_cart(self):
        if not cart:
            messagebox.showinfo("Cart", "Your cart is empty.")
            return

        cart_window = tk.Toplevel(self.root)
        cart_window.title("Cart")
        cart_window.geometry("400x400")

        cart_items_frame = tk.Frame(cart_window)
        cart_items_frame.pack(pady=10)

        for item in cart:
            item_label = tk.Label(cart_items_frame, text=f"{item['name']} - Price: {item['price']} EGP")
            item_label.pack(pady=5)

        tk.Label(cart_window, text=f"Delivery Fee: {DELIVERY_FEE} EGP", font=("Arial", 14)).pack(pady=10)

        tk.Button(cart_window, text="Confirm the process", command=self.calculate_total).pack(pady=10)

    def calculate_total(self):
        if not cart:
            messagebox.showinfo("Total", "Your cart is empty.")
            return

        total_with_delivery = total_price + DELIVERY_FEE
        messagebox.showinfo("Total Price", f"Total: {total_price} EGP\nDelivery Fee: {DELIVERY_FEE} EGP\nGrand Total: {total_with_delivery} EGP")

    def go_back(self):
        # Close the current page and reopen the previous page
        self.root.destroy()
        previous_page = page_stack.pop()
        if previous_page:
            previous_page.deiconify()

    def on_closing(self):
        if messagebox.askyesno(title="Quit", message="Are you sure you want to exit?"):
            self.root.destroy()


