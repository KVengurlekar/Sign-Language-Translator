import tkinter as tk
from tkinter import Entry, Label, Button, Toplevel, PhotoImage
import sqlite3
import re
import os
import sign_language_translator  # Import the translator module


# Check if database exists, do not delete it to preserve user data
if not os.path.exists("users.db"):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        email TEXT PRIMARY KEY,
                        password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Function to show errors in a new window
def show_error_window(title, message):
    error_window = Toplevel()
    error_window.title(title)
    error_window.configure(bg="#FFCDD2")
    Label(error_window, text=message, font=("Arial", 12), bg="#FFCDD2").pack(pady=10)
    Button(error_window, text="OK", font=("Arial", 12), bg="#C70039", fg="white", command=error_window.destroy).pack(pady=5)

class SignLanguageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Language Translator - Login")
        self.root.configure(bg="#FFDDC1")

        # Load Image
        self.logo = PhotoImage(file="logo.png")
        Label(root, image=self.logo, bg="#FFDDC1").pack()

        # Login Form
        Label(root, text="User Login", font=("Arial", 18, "bold"), bg="#FFDDC1").pack(pady=10)
        Label(root, text="Email:", font=("Arial", 12), bg="#FFDDC1").pack()
        self.email_entry = Entry(root, font=("Arial", 12))
        self.email_entry.pack(pady=5)
        
        Label(root, text="Password:", font=("Arial", 12), bg="#FFDDC1").pack()
        self.password_entry = Entry(root, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=5)
        
        # Frame for Login and Register buttons
        button_frame = tk.Frame(root, bg="#FFDDC1")
        button_frame.pack(pady=5)

        self.login_button = Button(button_frame, text="Login", font=("Arial", 12), bg="#FF5733", fg="white", command=self.login)
        self.login_button.grid(row=0, column=0, padx=5)

        self.register_button = Button(button_frame, text="Register", font=("Arial", 12), bg="#3498db", fg="white", command=self.open_register)
        self.register_button.grid(row=0, column=1, padx=5)

        self.quit_button = Button(root, text="Quit", font=("Arial", 12), bg="#C70039", fg="white", command=root.destroy)
        self.quit_button.pack(pady=10)
    
    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            self.open_translator()
        else:
            show_error_window("Login Failed", "Invalid credentials")
    
    def open_register(self):
        self.root.withdraw()  # Hide login window
        RegisterWindow(self.root)
    
    def open_translator(self):
        self.root.withdraw()  # Hide login window
        translator_window = Toplevel(self.root)
        translator_window.title("Sign Language Translator")
        translator_window.configure(bg="#E3F2FD")

        Label(translator_window, text="Sign Language Translator", font=("Arial", 18, "bold"), bg="#E3F2FD").pack(pady=10)

        # Create a frame to align buttons in one row
        button_frame = tk.Frame(translator_window, bg="#E3F2FD")
        button_frame.pack(pady=10)

        # Buttons in a single row
        speak_button = Button(button_frame, text="Speak", font=("Arial", 12), bg="#4CAF50", fg="white",
                          command=lambda: sign_language_translator.speak_function(translator_window))
        speak_button.grid(row=0, column=0, padx=5)

        text_button = Button(button_frame, text="Text", font=("Arial", 12), bg="#2196F3", fg="white",
                         command=lambda: getattr(sign_language_translator, "text_button")(translator_window))


        text_button.grid(row=0, column=1, padx=5)

        exit_button = Button(button_frame, text="Exit", font=("Arial", 12), bg="#C70039", fg="white",
                         command=translator_window.destroy)
        exit_button.grid(row=0, column=2, padx=5)
    
class RegisterWindow:
    def __init__(self, root):
        self.root = root
        self.window = Toplevel(root)
        self.window.title("Register")
        self.window.configure(bg="#E3F2FD")
        
        Label(self.window, text="Register", font=("Arial", 18, "bold"), bg="#E3F2FD").pack(pady=10)
        Label(self.window, text="Email:", font=("Arial", 12), bg="#E3F2FD").pack()
        self.email_entry = Entry(self.window, font=("Arial", 12))
        self.email_entry.pack(pady=5)
        
        Label(self.window, text="Password:", font=("Arial", 12), bg="#E3F2FD").pack()
        self.password_entry = Entry(self.window, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=5)
        
        Label(self.window, text="Confirm Password:", font=("Arial", 12), bg="#E3F2FD").pack()
        self.confirm_password_entry = Entry(self.window, show="*", font=("Arial", 12))
        self.confirm_password_entry.pack(pady=5)
        
        self.register_button = Button(self.window, text="Register", font=("Arial", 12), bg="#4CAF50", fg="white", command=self.register)
        self.register_button.pack(pady=10)
    
    def register(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        password_regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$'
        
        if not re.match(email_regex, email):
            show_error_window("Error", "Invalid email format")
            return
        
        if not re.match(password_regex, password):
            show_error_window("Error", "Password must be 8-16 characters long, include a number and a special character")
            return
        
        if password != confirm_password:
            show_error_window("Error", "Passwords do not match")
            return
if __name__ == "__main__":
    root = tk.Tk()
    app = SignLanguageApp(root)
    root.mainloop()

