import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
  
class JournalPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        
        self.label_journal_date = ttk.Label(
            font="courier",
            text="Journal Date DD/MM/YY",
            master=self
        )
        self.label_journal_date.pack(fill=tk.X, pady=5)
        self.entry_journal_date = ttk.Entry(self)
        self.entry_journal_date.pack(fill=tk.X, pady=5)

        self.label_journal = ttk.Label(
            font="courier",
            text="Journal Entry",
            master=self
        )
        self.label_journal.pack(fill=tk.X, pady=5)

        self.entry_journal_text = tk.Text(
            master=self
        )
        self.entry_journal_text.pack(fill=tk.X, pady=5)

        self.btn_submit = tk.Button(self, text="Save", command=self.save)
        self.btn_submit.pack(pady=20)

    # Function to save user data
    def save(self):
        date = self.entry_journal_date.get()
        entry = self.entry_journal_text.get("0.0")
        
        if date and entry:
            conn = sqlite3.connect('./app/database/database.db')
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                INSERT INTO journal (date, entry) VALUES (?, ?)
                ''', (date, entry))
                conn.commit()
                messagebox.showinfo("Success", "Save successful! Journal Added")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Journal already exists for this date")
            finally:
                conn.close()
        else:
            messagebox.showerror("Error", "Please enter both date and an entry")
