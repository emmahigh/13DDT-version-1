import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry

  
class ReflectionsPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Create a StringVar to hold the text in the Entry widget
        self.entry_reflection_date_text = tk.StringVar()
       
        label_reflection_date = DateEntry(
            font="courier",
            text="Reflections Date DD/MM/YY",
            master=self.scrollable_frame,
            textvariable=self.entry_reflection_date_text
        )
        label_reflection_date.pack(fill=tk.X, pady=5)

        # Attach the callback function to the StringVar using the trace method
        self.entry_reflection_date_text.trace_add("write", self.on_date_entry_change)

        label_grateful = ttk.Label(
            font="courier",
            text="Today I am grafeful for...",
            master=self.scrollable_frame
        )
        label_grateful.pack(fill=tk.X, pady=5)

        self.text_grateful = tk.Text(
            master=self.scrollable_frame
        )
        self.text_grateful.pack(fill=tk.BOTH, pady=5, expand=True)
       
        label_high = ttk.Label(
            font="courier",
            text="MY high of today was...",
            master=self.scrollable_frame
        )
        label_high.pack(fill=tk.X, pady=5)

        self.text_high = tk.Text(
            master=self.scrollable_frame
        )
        self.text_high.pack(fill=tk.BOTH, pady=5, expand=True)
        
        label_low = ttk.Label(
            font="courier",
            text="MY low of today was...",
            master=self.scrollable_frame
        )
        label_low.pack(fill=tk.X, pady=5)

        self.text_low = tk.Text(
            master=self.scrollable_frame
        )
        self.text_low.pack(fill=tk.BOTH, pady=5, expand=True)

        label_plans = ttk.Label(
            font="courier",
            text="What are my plans for tomorrow...",
            master=self.scrollable_frame
        )
        label_plans.pack(fill=tk.X, pady=5)

        self.text_plans = tk.Text(
            master=self.scrollable_frame
        )
        self.text_plans.pack(fill=tk.BOTH, pady=5, expand=True)

        self.btn_submit = tk.Button(self.scrollable_frame, text="Save", command=self.save)
        self.btn_submit.pack(pady=20)

    # Function to save user data
    def save(self):
        date = self.entry_reflection_date.get()
        grateful = self.text_grateful.get("0.0")
        high = self.text_high.get("0.0")
        low = self.text_low.get("0.0")
        plans = self.text_plans.get("0.0")
        
        if date and grateful and high and low and plans:
            conn = sqlite3.connect('./app/database/database.db')
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                INSERT INTO reflection (date, grateful, high, low, plans) VALUES (?, ?, ?, ?, ?)
                ''', (date, grateful, high, low, plans))
                conn.commit()
                messagebox.showinfo("Success", "Save successful! Reflection Added")
            except sqlite3.IntegrityError:  
                messagebox.showerror("Error", "A reflection already exists for this date")
            finally:
                conn.close()
        else:
            messagebox.showerror("Error", "Please enter all fields")

    def on_date_entry_change(self, *args):
        # Get the current value of the Entry widget
        date = self.entry_reflection_date_text.get()
        print(f"Entry value changed: {date}")

        conn = sqlite3.connect('./app/database/database.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT * FROM reflection WHERE date = ?
        ''', (date,))
        reflection = cursor.fetchone()
        if reflection:
            print(f"Test = {reflection[2]}")
            self.text_grateful.config(text=reflection[2])
            self.text_high.config(text=reflection[3])
            self.text_low.config(text=reflection[4])
            self.text_plans.config(text=reflection[5])
