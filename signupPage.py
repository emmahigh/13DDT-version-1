import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
  
class SignupPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        
        # First name label and entry
        self.label_firstname = tk.Label(self, text="First name")
        self.label_firstname.pack(pady=5)
        self.entry_firstname = tk.Entry(self)
        self.entry_firstname.pack(pady=5)

        # Last name label and entry
        self.label_lastname = tk.Label(self, text="Last name")
        self.label_lastname.pack(pady=5)
        self.entry_lastname = tk.Entry(self)
        self.entry_lastname.pack(pady=5)

        # Username label and entry
        self.label_username = tk.Label(self, text="Username")
        self.label_username.pack(pady=5)
        self.entry_username = tk.Entry(self)
        self.entry_username.pack(pady=5)

        # Password label and entry
        self.label_password = tk.Label(self, text="Password")
        self.label_password.pack(pady=5)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(pady=5)

        # Signup button
        self.btn_signup = tk.Button(self, text="Signup", command=self.signup)
        self.btn_signup.pack(pady=20)
    
    # Function to save user data
    def signup(self):
        firstname = self.entry_firstname.get()
        lastname = self.entry_lastname.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if username and password:
            conn = sqlite3.connect('./app/database/database.db')
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                INSERT INTO users (firstname, lastname, username, password) VALUES (?, ?, ?, ?)
                ''', (firstname, lastname, username, password))
                conn.commit()
                messagebox.showinfo("Success", "Signup successful! please login")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists")
            finally:
                conn.close()
        else:
            messagebox.showerror("Error", "Please enter both username and password")


        