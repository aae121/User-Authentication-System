import tkinter as tk
from tkinter import messagebox
from Auth import data

class AdminHomePage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Admin Home Page")
        self.root.geometry("600x600")

        tk.Label(self.root, text="Admin Home", font=("Arial", 24)).pack(pady=20)

        tk.Label(self.root, text="Choose a category:", font=("Arial", 20)).pack(pady=20, padx=20)

        # Create buttons for each category
        for category in data.categories.keys():
            button = tk.Button(self.root, text=category, font=("Arial", 20),
                               command=lambda c=category: self.go_to_category_page(category))
            button.pack(pady=10)

        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def go_to_category_page(self, category):
        CategoryAdminPage(self.root, category)

    def on_closing(self):
        if messagebox.askyesno(title="Quit", message="Are you sure you want to exit?"):
            self.root.destroy()

    def logout(self):
        self.root.destroy()
        from LoginPage import LoginPage  # Avoid circular import
        LoginPage()

class CategoryAdminPage:
    def __init__(self, parent, category_name):
        self.root = tk.Toplevel(parent)
        self.root.title(f"Manage {category_name}")
        self.root.geometry("600x600")

        self.category_name = category_name
        self.items = data.categories.get(category_name, [])

        self.item_widgets = []  # List to keep track of item labels and buttons
        self.widgets()

    def widgets(self):
        self.items_frame = tk.Frame(self.root)
        self.items_frame.pack(pady=10)

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=10)

        self.display_items()
        self.create_control_buttons()

    def display_items(self):
        # Clear existing widgets
        for widget in self.item_widgets:
            widget.destroy()

        self.item_widgets.clear()

        # Display all items in the category
        for item in self.items:
            item_text = f"{item['name']} - Price: {item['price']} - Brand: {item.get('brand', '')} - Model Year: {item.get('model year', '')}"
            item_label = tk.Label(self.items_frame, text=item_text)
            item_label.pack(pady=5)

            delete_button = tk.Button(self.items_frame, text="Delete", command=lambda i=item: self.delete_item(i))
            delete_button.pack(pady=5)

            update_button = tk.Button(self.items_frame, text="Update", command=lambda i=item: self.update_item(i))
            update_button.pack(pady=5)

            # Add the label and buttons to the list
            self.item_widgets.extend([item_label, delete_button, update_button])

    def create_control_buttons(self):
        add_button = tk.Button(self.control_frame, text="Add Item", command=self.add_item)
        add_button.pack(pady=10)

    def delete_item(self, item):
        if item in self.items:
            self.items.remove(item)
            self.display_items()
            messagebox.showinfo(title="Delete", message=f"Deleted {item['name']} from {self.category_name}.")

    def update_item(self, item):
        self.update_window = tk.Toplevel(self.root)
        self.update_window.title(f"Update {item['name']}")

        tk.Label(self.update_window, text="Update Price:").pack(pady=5)
        self.new_price_entry = tk.Entry(self.update_window)
        self.new_price_entry.pack(pady=5)

        tk.Button(self.update_window, text="Update", command=lambda: self.save_update(item)).pack(pady=5)

    def save_update(self, item):
        new_price = self.new_price_entry.get()
        if new_price.isdigit():
            item['price'] = int(new_price)
            self.update_window.destroy()
            self.display_items()
            messagebox.showinfo(title="Update", message=f"Updated {item['name']} price to {new_price}.")
        else:
            messagebox.showerror(title="Error", message="Please enter a valid price.")

    def add_item(self):
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title(f"Add Item to {self.category_name}")

        tk.Label(self.add_window, text="Item Name:").pack(pady=5)
        self.item_name_entry = tk.Entry(self.add_window)
        self.item_name_entry.pack(pady=5)

        tk.Label(self.add_window, text="Price:").pack(pady=5)
        self.item_price_entry = tk.Entry(self.add_window)
        self.item_price_entry.pack(pady=5)

        tk.Label(self.add_window, text="Brand:").pack(pady=5)
        self.item_brand_entry = tk.Entry(self.add_window)
        self.item_brand_entry.pack(pady=5)

        tk.Label(self.add_window, text="Model Year:").pack(pady=5)
        self.item_model_year_entry = tk.Entry(self.add_window)
        self.item_model_year_entry.pack(pady=5)

        tk.Button(self.add_window, text="Add", command=self.save_new_item).pack(pady=5)

    def save_new_item(self):
        name = self.item_name_entry.get()
        price = self.item_price_entry.get()
        brand = self.item_brand_entry.get()
        model_year = self.item_model_year_entry.get()

        if name and price.isdigit() and brand and model_year.isdigit():
            new_item = {
                "name": name,
                "price": int(price),
                "brand": brand,
                "model year": int(model_year)
            }
            self.items.append(new_item)
            self.add_window.destroy()
            self.display_items()
            messagebox.showinfo(title="Add Item", message=f"Added {name} to {self.category_name}.")
        else:
            messagebox.showerror(title="Error", message="Please provide valid item details.")

