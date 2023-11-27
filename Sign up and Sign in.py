import customtkinter as ctk
import tkinter.messagebox as tkmb
from pymongo import MongoClient

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

client = MongoClient('mongodb://localhost:27017/')
db = client['user_database']
user_collection = db['user_collection']

app = ctk.CTk()
app.geometry("600x600")
app.title("Sign in and Sign up By Farhan")

d = {"admin": "QWERTY@123"}

user_pass = None

def signIn():
    new_window = ctk.CTkToplevel(app)
    new_window.title("Sign in")
    new_window.geometry("350x150")

    username = user_entry.get()
    password = user_pass.get()
    user_data = user_collection.find_one({'username':username,'password':password})
    if user_data:
        tkmb.showinfo(title="Login Successful", message="You have logged in successfully")
        ctk.CTkLabel(new_window, text="Login ho gaya bhaiyya!").pack()

    elif user_entry.get() in d and user_pass.get() != d[user_entry.get()]:
        tkmb.showinfo(title="Wrong Password", message="Please check your password")

    elif user_entry.get() not in d:
        tkmb.showinfo(title="Account not found", message="We couldn't find an account with this username. Please try again.")

def signUp():
    global user_pass

    new_window2 = ctk.CTkToplevel(app)
    new_window2.title("Sign Up")
    new_window2.geometry("600x600")

    label2 = ctk.CTkLabel(new_window2, text="Create a new account")
    label2.pack(pady=20)

    frame2 = ctk.CTkFrame(master=new_window2)
    frame2.pack(pady=20, padx=40, fill="both", expand=True)

    label2 = ctk.CTkLabel(master=frame2, text="Enter a new Username and password")
    label2.pack(pady=20, padx=10)

    user_entry2 = ctk.CTkEntry(master=frame2, placeholder_text="Username")
    user_entry2.pack(pady=12, padx=10)
    user_entry2.bind("<Return>", focusPasswordEntry)

    user_pass = ctk.CTkEntry(master=frame2, placeholder_text="Password")
    user_pass.pack(pady=12, padx=10)

    def checkAndSignUp():
        username = user_entry2.get()
        password = user_pass.get()

        existing_user = user_collection.find_one({'username': username})

        if existing_user:
                tkmb.showinfo(title="Username already exists", message="Account Already exists!")
        else:
                user_collection.insert_one({'username': username, 'password': password})
                tkmb.showinfo(title="Sign Up Successful", message="You have signed up successfully!")

        # Raise the main window to the top after sign up
        app.attributes('-topmost', True)
        app.after_idle(app.attributes, '-topmost', False)

    button3 = ctk.CTkButton(master=frame2, text="Sign Up", command=checkAndSignUp)
    button3.pack(pady=12, padx=10)

def focusPasswordEntry(event):
    user_pass.focus_set()

label = ctk.CTkLabel(app, text="Welcome to MYAPP")
label.pack(pady=20)

frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=40, fill='both', expand=True)

label = ctk.CTkLabel(master=frame, text='Sign in or Sign up')
label.pack(pady=12, padx=10)

user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username")
user_entry.pack(pady=12, padx=10)
user_entry.bind("<Return>", focusPasswordEntry)

user_pass = ctk.CTkEntry(master=frame, placeholder_text="Password")
user_pass.pack(pady=12, padx=10)

button = ctk.CTkButton(master=frame, text="Login", command=signIn)
button.pack(pady=12, padx=10)

or_label = ctk.CTkLabel(master=frame, text="OR")
or_label.pack(pady=2)

button2 = ctk.CTkButton(master=frame, text="Sign Up", command=signUp)
button2.pack(pady=12, padx=10)

checkbox = ctk.CTkCheckBox(master=frame, text='Remember Me')
checkbox.pack(pady=12, padx=10)

app.mainloop()
