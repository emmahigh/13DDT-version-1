import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
#import sqlite for database functionality
import sqlite3
#import sqlite to work with files and folders
from pathlib import Path
from userSession import UserSession
from homePage import HomePage
from journalPage import JournalPage
from reflectionsPage import ReflectionsPage
from signupPage import SignupPage 
from loginPage import LoginPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Journal Application")
        self.geometry("800x600")

        # Create a style
        style = ttk.Style(self)

        # Set the theme with the theme_use method
        style.theme_use('clam')  # put the theme name here, that you want to use

        #create a global variable to check whether the user is logged in
        self.logged_in = tk.BooleanVar(value=False)  # Default to False for example

        self.logged_in.trace_add("write", self.update_button_state)

        self.create_database()

        self.create_widgets()

    def create_database(self):
        # Connect to the database (or create it if it doesn't exist)
        # Ensure folder exists
        Path("./app/database").mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect('./app/database/database.db')

        # Create a cursor object
        cursor = conn.cursor()

        # Create a table for user data
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL
        )
        ''')

        # Create a table for journal data
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL UNIQUE,
            entry TEXT NOT NULL
        )
        ''')

        # Create a table for reflections data
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS reflection (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL UNIQUE,
            grateful TEXT NOT NULL,
            high TEXT NOT NULL,
            low TEXT NOT NULL,
            plans TEXT NOT NULL
        )
        ''')

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    def create_widgets(self):
        global logged_in
        # Configure the main frame to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create the main frame
        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Configure the main frame to expand
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Create the sidebar frame
        sidebar_frame = ttk.Frame(main_frame, width=50, )
        sidebar_frame.grid(row=0, column=0, sticky="ns")

        # Create the content frame
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.grid(row=0, column=1, sticky="nsew")

        # Add buttons to the sidebar
        btn_home = ttk.Button(sidebar_frame, width=10,text="Homepage", command=self.show_homepage)
        btn_home.pack(fill=tk.X, pady=5)
       
        self.btn_journal = ttk.Button(sidebar_frame, text="Journal", state=tk.DISABLED, command=self.show_journal)
        self.btn_journal.pack(fill=tk.X, pady=5)

        self.btn_reflections = ttk.Button(sidebar_frame, text="Reflections", state=tk.DISABLED, command=self.show_reflections)
        self.btn_reflections.pack(fill=tk.X, pady=5)

        self.btn_login = ttk.Button(sidebar_frame, text="Login", command=self.show_login)
        self.btn_login.pack(fill=tk.X, pady=5)
        
        self.btn_signup = ttk.Button(sidebar_frame, text="Signup", command=self.show_signup)
        self.btn_signup.pack(fill=tk.X, pady=5)
        
        self.user_icon = Image.open("./app/img/user.png")
        self.user_icon = self.user_icon.resize((24, 24), Image.Resampling.LANCZOS)  # Resize image to 24x24 pixel
        self.user_icon = ImageTk.PhotoImage(self.user_icon)
        self.btn_logout = ttk.Button(sidebar_frame, text="Log out", image=self.user_icon, compound="left", style='Flat.TButton', command=self.logout)
        #self.btn_logout.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        self.btn_logout.pack_forget()

        self.label_welcome = tk.Label(sidebar_frame, text="Welcome!")
        #self.label_welcome.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        self.label_welcome.pack_forget()

        # Display the initial content
        self.show_homepage()

    def show_page(self, page_class):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        page = page_class(self.content_frame, self)
        page.pack(fill=tk.BOTH, expand=True)

    def show_homepage(self):
        self.show_page(HomePage)

    def show_journal(self):
        self.show_page(JournalPage)

    def show_reflections(self):
        self.show_page(ReflectionsPage)
    
    def show_signup(self):
        self.show_page(SignupPage)

    def show_login(self):
        self.show_page(LoginPage)

    def logout(self):
        self.logged_in.set(False)

    def update_button_state(self, *args):
        # Update the button state based on the global variable
        if self.logged_in.get() == False:
            self.btn_reflections.config(state=tk.DISABLED)
            self.btn_journal.config(state=tk.DISABLED)
            self.btn_login.pack(fill=tk.X, pady=5)
            self.btn_signup.pack(fill=tk.X, pady=5)
            self.btn_logout.pack_forget()
            self.label_welcome.pack_forget()
        else:
            session = UserSession()
            self.user = session.get_user()
            self.btn_reflections.config(state=tk.NORMAL)
            self.btn_journal.config(state=tk.NORMAL)
            self.btn_login.pack_forget()
            self.btn_signup.pack_forget()
            self.btn_logout.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
            self.label_welcome.config(text=f"Welcome {self.user.firstname}!")
            self.label_welcome.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

app = App()

app.mainloop()
