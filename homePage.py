import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class HomePage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        
        # Load and resize the image
        original_image = Image.open("./app/img/homepage.png")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        resized_image = original_image.resize((screen_width, screen_height), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(resized_image)
        
        # Create a label to hold the image
        homepage = ttk.Label(self, image=self.image)
        homepage.pack(fill='both', expand=True)  # Fill the whole frame and expand

        # Update the image when the window is resized
        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        screen_width = self.winfo_width()
        screen_height = self.winfo_height()
        
        # Resize the image according to the new window size
        original_image = Image.open("./app/img/homepage.png")
        resized_image = original_image.resize((screen_width, screen_height), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(resized_image)
        
        # Update the label with the new image
        self.winfo_children()[0].configure(image=self.image)

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")  # Set initial window size
    page = HomePage(root)
    page.pack(fill='both', expand=True)
    root.mainloop()
      