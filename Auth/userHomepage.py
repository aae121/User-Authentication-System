import tkinter as tk
from tkinter import messagebox
from Auth import data
from Auth.categoryPage import CategoryPage

class UserHomePage:
    def __init__(self, username):
        self.root = tk.Tk()
        self.root.title("User Home Page")
        self.root.geometry("600x600")

        tk.Label(self.root, text=f"Welcome {username}", font=("Arial", 24)).pack(pady=20)

        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=10)
        self.label = tk.Label(self.root, text="Choose a category:", font=("Arial", 20))
        self.label.pack(pady=20, padx=20)

        for category in data.categories.keys():
            button = tk.Button(self.root, text=category, font=("Arial", 20), command=lambda c=category: self.go_to_category_page(c))
            button.pack(pady=20, padx=20)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def go_to_category_page(self, category):
        CategoryPage(self.root, category)  # Pass the parent (self.root) and the category

    def on_closing(self):
        if messagebox.askyesno(title="Quit", message="Are you sure you want to exit?"):
            self.root.destroy()

    def logout(self):
        self.root.destroy()
        from LoginPage import LoginPage  # Avoid circular import
        LoginPage()


