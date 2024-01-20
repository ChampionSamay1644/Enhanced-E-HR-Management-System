import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import firebase_admin
from firebase_admin import db, credentials

# Initialize Firebase Admin SDK
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://your-firebase-project-id.firebaseio.com/'})

class CreativeLoginApp:
    def __init__(self, root):
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.realpath(__file__))
        print("Script directory:", script_dir)

        self.root = root
        self.root.title("Creative Login App")

        # Construct the full path to the image file
        img_path = os.path.join(script_dir, "HR_background.png")

        # Load and set background image
        self.original_image = Image.open(img_path)
        self.img = ImageTk.PhotoImage(self.original_image)

        # Create and place a label with the background image
        self.background_label = tk.Label(root, image=self.img, bg='white')
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Bind the window resize event
        root.bind("<Configure>", self.resize_image)

        # Label for Username
        username_label = tk.Label(root, text="Username", font=("Helvetica", 12, "bold"), bg='white')
        username_label.place(relx=0.5, rely=0.35, anchor="center")

        # Username entry
        self.username_entry = tk.Entry(root, font=("Helvetica", 12, "bold"))
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")
        self.username_entry.insert(0, "")  # Default text

        # Label for Password
        password_label = tk.Label(root, text="Password", font=("Helvetica", 12, "bold"), bg='white')
        password_label.place(relx=0.5, rely=0.5, anchor="center")

        # Password entry
        self.password_entry = tk.Entry(root, show="*", font=("Helvetica", 12, "bold"))
        self.password_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.password_entry.insert(0, "")  # Default text

        # Login button
        self.login_button = tk.Button(root, text="Login", command=self.login, font=("Helvetica", 14))
        self.login_button.place(relx=0.5, rely=0.65, anchor="center")

        # Exit button
        self.exit_button = tk.Button(root, text="Exit", command=root.destroy, font=("Helvetica", 14))
        self.exit_button.place(relx=0.5, rely=0.75, anchor="center")

        # Load credentials from the database
        self.credentials = self.load_credentials_from_database()

    def resize_image(self, event):
        new_width = event.width
        new_height = event.height

        # Resize the original image
        resized_image = self.original_image.resize((new_width, new_height))

        # Create a new PhotoImage object
        self.img = ImageTk.PhotoImage(resized_image)

        # Update the label
        self.background_label.config(image=self.img)
        self.background_label.image = self.img  # Keep a reference to avoid garbage collection

    def load_credentials_from_database(self):
        try:
            admins_ref = db.reference('admins')
            admins_data = admins_ref.get()
            return admins_data
        except Exception as e:
            print("Error loading credentials from the database:", e)
            return {}

    def login(self):
      username = self.username_entry.get()
      password = self.password_entry.get()

      if not username or not password:
        messagebox.showerror("Login Failed", "Please enter both username and password.")
        return

      if username in self.credentials and 'password' in self.credentials[username]:
        if self.credentials[username]['password'] == password:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        else:
            messagebox.showerror("Login Failed", "Invalid password. Please try again.")
      else:
        messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")


def main():
    root = tk.Tk()
    root.geometry("800x600")  # Set the window size
    app = CreativeLoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
