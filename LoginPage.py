import tkinter as tk
from tkinter import messagebox
import json
from Auth.adminHomepage import AdminHomePage
from Auth.userHomepage import UserHomePage
from RegistrationPage import RegistrationPage

class LoginPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login Page")
        self.root.geometry("500x600")

        tk.Label(self.root, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack(pady=20)

        self.register_button = tk.Button(self.root, text="Register", command=self.open_registration)
        self.register_button.pack(pady=5)

        self.root.mainloop()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email == "admin@gmail.com" and password == "admin123":
            self.root.destroy()
            AdminHomePage()
            return

        # Check the JSON file
        try:
            with open("db.json", "r") as file:
                data = json.load(file)
                users = data.get("users", [])
        except FileNotFoundError:
            messagebox.showerror("Error", "user not found")
            return

        # Validate user
        for user in users:
            if user["email"] == email and user["password"] == password:
                self.root.destroy()
                UserHomePage(user["name"])
                return

        messagebox.showerror("Error", "Invalid email or password")

    def open_registration(self):
        self.root.destroy()
        RegistrationPage()


LoginPage()
