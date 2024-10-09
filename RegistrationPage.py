import tkinter as tk
from tkinter import messagebox
import json
import LoginPage as loginPage

class RegistrationPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Registration Page")
        self.root.geometry("500x600")

        tk.Label(self.root, text="Name:").pack(pady=5)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=5)

        tk.Label(self.root, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Label(self.root, text="National ID:").pack(pady=5)
        self.national_id_entry = tk.Entry(self.root)
        self.national_id_entry.pack(pady=5)

        tk.Label(self.root, text="Age:").pack(pady=5)
        self.age_entry = tk.Entry(self.root)
        self.age_entry.pack(pady=5)

        tk.Label(self.root, text="Gender:").pack(pady=5)
        self.gender_entry = tk.Entry(self.root)
        self.gender_entry.pack(pady=5)

        tk.Label(self.root, text="Governorate:").pack(pady=5)
        self.governorate_entry = tk.Entry(self.root)
        self.governorate_entry.pack(pady=5)

        self.register_button = tk.Button(self.root, text="Register", command=self.register)
        self.register_button.pack(pady=20)

        self.login_button = tk.Button(self.root, text="Go to Login", command=self.open_login)
        self.login_button.pack(pady=5)

        self.root.mainloop()

    def register(self):
        user_data = {
            "name": self.name_entry.get(),
            "email": self.email_entry.get(),
            "password": self.password_entry.get(),
            "national_id": self.national_id_entry.get(),
            "age": self.age_entry.get(),
            "gender": self.gender_entry.get(),
            "governorate": self.governorate_entry.get(),
        }

        if not all(user_data.values()):
            messagebox.showwarning("Input Error", "Please fill in all fields")
            return

        try:
            with open("db.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {"users": []}

        data["users"].append(user_data)

        with open("db.json", "w") as file:
            json.dump(data, file, indent=4)

        messagebox.showinfo("Registration Success", "You have registered successfully!")
        self.open_login()

    def open_login(self):
        self.root.destroy()
        loginPage.LoginPage()

