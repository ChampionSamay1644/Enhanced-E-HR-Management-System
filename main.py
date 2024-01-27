import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog, ttk
from PIL import Image, ImageTk
import os
import firebase_admin
from firebase_admin import db, credentials
import threading

# Initialize Firebase Admin SDK
cred = credentials.Certificate("credentials.json")  # Path: credentials.json
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://hr-management-system-f7c9f-default-rtdb.asia-southeast1.firebasedatabase.app/"
    },
)

class CreativeLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HR Management System")
        self.employee_original_image = None
        self.employee_img = None
        self.boss_original_image = None
        self.boss_img = None
        self.company_name_text = None  # Initialize company_name_text attribute

        # Construct the full path to the image file
        img_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "HR_background.png" #change jpg to png for main background
        )

        # Focus on window
        root.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(root)

        # create a canvas that resizes with the window
        self.company_logo_canvas = tk.Canvas(root, bg="white", highlightthickness=0)
        self.company_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        root.bind("<Configure>", self.on_window_resize_main)

        # import the image as the background on the canvas
        self.load_image_main(img_path)

        # Label for Username
        username_label = tk.Label(
            root, text="Username", font=("Helvetica", 12, "bold"), bg="white"
        )
        username_label.place(relx=0.5, rely=0.35, anchor="center")

        # Username entry
        self.username_entry = tk.Entry(root, font=("Helvetica", 12, "bold"))
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")
        self.username_entry.insert(0, "")  # Default text

        # Label for Password
        password_label = tk.Label(
            root, text="Password", font=("Helvetica", 12, "bold"), bg="white"
        )
        password_label.place(relx=0.5, rely=0.5, anchor="center")

        # Password entry
        self.password_entry = tk.Entry(root, show="*", font=("Helvetica", 12, "bold"))
        self.password_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.password_entry.insert(0, "")  # Default text

        # threading.Thread(target=self.load_image_main, args=(img_path,)).start()
        #this is to fix our gui time consuming problem
        
        # Login button
        self.login_button = tk.Button(
            root, text="Login", command=self.login, font=("Helvetica", 14)
        )
        self.login_button.place(
            relx=0.5, rely=0.65, anchor="center", width=100, height=30
        )

        # Exit button
        self.exit_button = tk.Button(
            root, text="Exit", command=root.destroy, font=("Helvetica", 14)
        )
        self.exit_button.place(
            relx=0.5, rely=0.75, anchor="center", width=100, height=30
        )

        # Credits button
        self.credits_button = tk.Button(
            root, text="Credits", command=self.show_credits, font=("Helvetica", 14)
        )
        self.credits_button.place(
            relx=0.5, rely=0.85, anchor="center", width=100, height=30
        )

        # Bind the Enter key to the login function
        root.bind("<Return>", lambda event: self.login())

        # Bind the Escape key to the exit function
        root.bind("<Escape>", lambda event: root.destroy())

    def load_image_main(self, img_path):
        # Load image and adjust canvas size
        self.original_company_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_main()

    def load_image_common(self):
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")
        self.original_common_image = Image.open(img_path)
        
    def resize_canvas_and_image_common(self):
            window_width = self.common_canvas.winfo_width()
            window_height = self.common_canvas.winfo_height()
            self.common_canvas.config(width=window_width, height=window_height)

            resized_image = self.original_common_image.resize((window_width, window_height))
            self.common_image = ImageTk.PhotoImage(resized_image)

            self.common_canvas.delete("all")
            self.common_canvas.create_image(0, 0, image=self.common_image, anchor="nw")
            
    def on_window_resize_common(self, event=None):
        self.resize_canvas_and_image_common()
    
    def create_common_window(self, title,):
        common_window = tk.Tk()
        common_window.geometry("800x600")
        common_window.title(title)

        self.common_canvas = tk.Canvas(common_window, bg="white", highlightthickness=0)
        self.common_canvas.pack(fill=tk.BOTH, expand=True)

        common_window.bind("<Configure>",lambda event:self.on_window_resize_common())

        self.load_image_common()
        self.resize_canvas_and_image_common()
        
        return common_window, self.common_canvas

    def center_window_all(self, window):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width / 2) - (900 / 2)
        y = (screen_height / 2) - (600 / 2)
        window.geometry("%dx%d+%d+%d" % (900, 600, x, y))
        
    def resize_canvas_and_image_main(self):
        # Get the current window size
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        # Resize the canvas to the current window size
        self.company_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_company_logo_image.resize(
            (window_width, window_height)
        )
        self.company_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.company_logo_canvas.delete("all")
        self.company_logo_canvas.create_image(
            0, 0, image=self.company_logo_image, anchor="nw"
        )

        # Redraw the company name text
        if hasattr(self, "company_name_text"):
            self.company_logo_canvas.delete(
                self.company_name_text
            )  # Remove the old text
        self.company_name_text = self.company_logo_canvas.create_text(
            window_width / 2,
            100,
            text="Ben Dover Inc",
            font=("Helvetica", 28, "bold"),
            fill="white",
        )

    def on_window_resize_main(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_main()

    def show_credits(self):
        # Create a new Toplevel window for the credits
        credits_dialog = tk.Toplevel(self.root)
        credits_dialog.title("Credits")

        # You can customize the credits information as per your needs
        credits_text = (
            "HR Management System\n\n"
            "Developed by: \n -Samay Pandey, \n-Armaan Nakhuda, \n-Sushant Navle, \n-Peeyush Karnik(assuming he does any work)\n\n"
            "Stage Completition: Stage 4 completed\n"
            "Date: 6th Feb 2024\n"
            "\nSpecial Thanks to:\n- Firebase\n- OpenAI\n- Yash Patil\n"
        )

        # Create a label for credits information
        credits_label = tk.Label(
            credits_dialog, text=credits_text, font=("Helvetica", 12)
        )
        credits_label.pack(padx=20, pady=20)

        # Center the credits dialog relative to the main application window
        credits_dialog.update_idletasks()

        app_x = self.root.winfo_x()
        app_y = self.root.winfo_y()
        app_width = self.root.winfo_width()
        app_height = self.root.winfo_height()

        credits_width = credits_dialog.winfo_width()
        credits_height = credits_dialog.winfo_height()

        x = app_x + (app_width - credits_width) // 2
        y = app_y + (app_height - credits_height) // 2

        credits_dialog.geometry(f"{credits_width}x{credits_height}+{x}+{y}")

        credits_dialog.mainloop()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if username or password is empty
        if not username or not password:
            messagebox.showerror(
                "Login Failed", "Username and password are required. Please enter both."
            )
            return

        admins_ref = db.reference("/admins")
        hr_ref = db.reference("/HR")
        boss_ref = db.reference("/boss")
        employee_ref = db.reference("/employee")

        if admins_ref.child(username).child("password").get() == password:
            role = admins_ref.child(username).child("role").get()
            messagebox.showinfo(
                "Login Successful",
                f"Welcome, {username}!\nYou are logged in as a {role}.",
            )
            self.open_admin_window(role, username)
            return

        if hr_ref.child(username).child("password").get() == password:
            role = hr_ref.child(username).child("role").get()
            messagebox.showinfo(
                "Login Successful",
                f"Welcome, {username}!\nYou are logged in as a {role}.",
            )
            self.open_hr_window(role, username)
            return

        if boss_ref.child(username).child("password").get() == password:
            role = boss_ref.child(username).child("role").get()
            messagebox.showinfo(
                "Login Successful",
                f"Welcome, {username}!\nYou are logged in as a {role}.",
            )
            self.open_boss_window(role, username)
            return

        if employee_ref.child(username).child("password").get() == password:
            role = employee_ref.child(username).child("role").get()
            messagebox.showinfo(
                "Login Successful",
                f"Welcome, {username}!\nYou are logged in as a {role}.",
            )
            self.open_employee_window(role, username)
            return

        messagebox.showerror(
            "Login Failed", "Invalid username or password. Please try again."
        )

    def open_admin_window(self, role, username):
        if hasattr(self, "root") and self.root.winfo_exists():
            self.root.destroy()  # Close the main login window
        text=None
        # admin_window = tk.Tk()  # Use Tk() to create a new window
        # admin_window.geometry("900x600")  # Set the window size
        # admin_window.title("Admin Window")
        admin_window,self.admin_logo_canvas=self.create_common_window("Admin Window")
        window_width = self.admin_logo_canvas.winfo_width()
        window_height = self.admin_logo_canvas.winfo_height()
         # create a canvas that resizes with the window
        # self.admin_logo_canvas = tk.Canvas(admin_window, bg="white", highlightthickness=0)
        # self.admin_logo_canvas.pack(fill=tk.BOTH, expand=True)
        
        #put a text onto the canvas and redraw the canvas
        self.admin_logo_canvas.create_text(
            window_width / 2,
            100,
            text=f"Welcome {username}!",
            font=("Helvetica", 28, "bold"),
            fill="white",
            tag="welcome_text"
        )
    # Raise the text to make sure it's on top
        self.admin_logo_canvas.tag_raise("welcome_text")
        # Force an immediate redraw
        self.admin_logo_canvas.update_idletasks()
        self.admin_logo_canvas.update()
        
        # bind window resize event to function
        admin_window.bind("<Configure>", lambda event: self.on_window_resize_common(event))

        #create a button on the canvas
        self.create_all_admin_button = tk.Button(
            self.admin_logo_canvas, text="Create HR Login", command=lambda:self.create_all_admin(), font=("Helvetica", 14)
        )
        self.create_all_admin_button.pack(
            pady=20
        )
        self.create_all_admin_button.place(
            relx=0.5, rely=0.5, anchor="center", width=200, height=30
        )
        self.remove_all_admin_button = tk.Button(
            self.admin_logo_canvas, text="Remove HR Login", command=lambda:self.remove_all_admin(), font=("Helvetica", 14)
        )
        self.remove_all_admin_button.pack(
            pady=20
        )
        self.remove_all_admin_button.place(
            relx=0.5, rely=0.6, anchor="center", width=200, height=30
        )
         # bind window resize event to function
        admin_window.bind("<Configure>", lambda event: self.on_window_resize_common(event))
        
         # import the image as the background on the canvas
        # self.load_image_admin(username)

        #create an exit button in canvas and place at bottom middle
        exit_button = tk.Button(
        self.admin_logo_canvas,
        text="Exit",
        command=admin_window.destroy,
        font=("Helvetica", 14),
        width=15,
        height=2,
        bd=0,
        fg="white",
        bg="#FF4500",
        activebackground="#FF6347",
    )
        exit_button.place(relx=0.5, rely=1.0, anchor="s")

        # focus on window
        admin_window.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(admin_window)

        # Bind the Escape key to the exit function
        admin_window.bind("<Escape>", lambda event: admin_window.destroy())

        # Run the main loop for the admin window
        admin_window.mainloop()

    def load_image_admin(self,username):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_admin_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_admin(username)
    
    def resize_canvas_and_image_admin(self,username):
        username_admin = username
        # Get the admin window size
        window_width = self.admin_logo_canvas.winfo_width()
        window_height = self.admin_logo_canvas.winfo_height()
       

        # Resize the canvas to the current window size
        self.admin_logo_canvas.config(width=window_width, height=window_height)


        # Resize the image if needed
        resized_image = self.original_company_logo_image.resize(
            (window_width, window_height)
        )
        self.admin_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.admin_logo_canvas.delete("all")
        self.admin_logo_canvas.create_image(
            0, 0, image=self.admin_logo_image, anchor="nw"
        )

         #redraw the admin name text    
        if hasattr(self, "admin_name_text"):
            self.admin_logo_canvas.delete(
                self.admin_name_text
            )  # Remove the old text
        self.admin_name_text = self.admin_logo_canvas.create_text(
            window_width / 2,
            100,
            text=f"Welcome {username_admin}!",
            font=("Helvetica", 28, "bold"),
            fill="white",
        )
    
    def on_window_resize_admin(self, event,username):
        # Handle window resize event
        self.resize_canvas_and_image_admin(username)

    def create_all_admin(self):
        # create a new window
        create_remove_hr_window = tk.Toplevel()
        create_remove_hr_window.geometry("800x600")  # Set the window size
        create_remove_hr_window.title("Create HR Login")

        #create a canvas that resizes with the window
        self.create_hr_logo_canvas = tk.Canvas(create_remove_hr_window, bg="white", highlightthickness=0)
        self.create_hr_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        create_remove_hr_window.bind("<Configure>", lambda event: self.on_window_resize_create_hr(event))

        # import the image as the background on the canvas
        self.load_image_create_hr()

        #create a new entry for username on canvas
        username_label = tk.Label(
            self.create_hr_logo_canvas,
            text="Username",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        username_label.pack(
            pady=20
        )
        username_label.place(relx=0.5, rely=0.35, anchor="center")
        self.username_entry = tk.Entry(
            self.create_hr_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.username_entry.pack(
            pady=20
        )
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")
        self.username_entry.insert(0, "")
        # create a new entry for password on canvas
        password_label = tk.Label(
            self.create_hr_logo_canvas,
            text="Password",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        password_label.pack(
            pady=20
        )
        password_label.place(relx=0.5, rely=0.5, anchor="center")
        self.password_entry = tk.Entry(
            self.create_hr_logo_canvas, show="", font=("Helvetica", 12, "bold")
        )
        self.password_entry.pack(
            pady=20
        )
        self.password_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.password_entry.insert(0, "")
        # create a new checkbox for role with options- HR, boss, employee on canvas
        role_label = tk.Label(
            self.create_hr_logo_canvas,
            text="Role",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        role_label.pack(
            pady=20
        )
        role_label.place(relx=0.5, rely=0.65, anchor="center")
        self.role_entry = ttk.Combobox(
            self.create_hr_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.role_entry["values"] = ("HR", "boss", "employee")
        self.role_entry.pack(
            pady=20
        )
        self.role_entry.place(relx=0.5, rely=0.7, anchor="center")
        self.role_entry.current(0)
        # create a new button for adding the new login on canvas
        add_button = tk.Button(
            self.create_hr_logo_canvas,
            text="Add",
            command=self.add_login_to_database,
            font=("Helvetica", 14),
        )
        add_button.pack(
            pady=20
        )
        add_button.place(relx=0.5, rely=0.8, anchor="center", width=100, height=30)
        # store the values in 3 variables when the button is pressed
        add_button.bind(
            "<Button-1>",
            lambda event: self.add_login_to_database(create_remove_hr_window),
        )
        # Bind the Escape key to the exit function
        create_remove_hr_window.bind(
            "<Escape>", lambda event: create_remove_hr_window.destroy()
        )
        # focus on window
        create_remove_hr_window.focus_force()
        # Center the window with function center_window_test
        self.center_window_all(create_remove_hr_window)
        # Run the main loop for the create_remove_hr_window
        create_remove_hr_window.mainloop()

    def load_image_create_hr(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_create_hr_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_create_hr()

    def resize_canvas_and_image_create_hr(self):
        # Get the create_hr window size
        window_width = self.create_hr_logo_canvas.winfo_width()
        window_height = self.create_hr_logo_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.create_hr_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_create_hr_logo_image.resize(
            (window_width, window_height)
        )
        self.create_hr_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.create_hr_logo_canvas.delete("all")
        self.create_hr_logo_canvas.create_image(
            0, 0, image=self.create_hr_logo_image, anchor="nw"
        )

    def on_window_resize_create_hr(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_create_hr()

    def remove_all_admin(self):
        # create a new window
        create_remove_hr_window = tk.Toplevel()
        create_remove_hr_window.geometry("800x600")  # Set the window size
        create_remove_hr_window.title("Remove HR Login")

        #create a canvas that resizes with the window
        self.remove_hr_logo_canvas = tk.Canvas(create_remove_hr_window, bg="white", highlightthickness=0)
        self.remove_hr_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        create_remove_hr_window.bind("<Configure>", lambda event: self.on_window_resize_remove_hr(event))

        # import the image as the background on the canvas
        self.load_image_remove_hr()

        #create a new entry for username on canvas
        username_label = tk.Label(
            self.remove_hr_logo_canvas,
            text="Username",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        username_label.pack(
            pady=20
        )
        username_label.place(relx=0.5, rely=0.35, anchor="center")
        self.username_entry = tk.Entry(
            self.remove_hr_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.username_entry.pack(
            pady=20
        )
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")
        self.username_entry.insert(0, "")
        # create a checkbox for role with options- HR, boss, employee on canvas
        role_label = tk.Label(
            self.remove_hr_logo_canvas,
            text="Role",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        role_label.pack(
            pady=20
        )
        role_label.place(relx=0.5, rely=0.5, anchor="center")
        self.role_entry = ttk.Combobox(
            self.remove_hr_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.role_entry["values"] = ("HR", "boss", "employee")
        self.role_entry.pack(
            pady=20
        )
        self.role_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.role_entry.current(0)
        # create a new button for removing the login on canvas
        remove_button = tk.Button(
            self.remove_hr_logo_canvas,
            text="Remove",
            command=self.remove_login_from_database,
            font=("Helvetica", 14),
        )
        remove_button.pack(
            pady=20
        )
        remove_button.place(relx=0.5, rely=0.65, anchor="center", width=100, height=30)
        # store the values in 2 variables when the button is pressed
        remove_button.bind(
            "<Button-1>",
            lambda event: self.remove_login_from_database(create_remove_hr_window),
        )
        # Bind the Escape key to the exit function
        create_remove_hr_window.bind(
            "<Escape>", lambda event: create_remove_hr_window.destroy()
        )
        # focus on window
        create_remove_hr_window.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(create_remove_hr_window)

    def load_image_remove_hr(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_remove_hr_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_remove_hr()

    def resize_canvas_and_image_remove_hr(self):
        # Get the remove_hr window size
        window_width = self.remove_hr_logo_canvas.winfo_width()
        window_height = self.remove_hr_logo_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.remove_hr_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_remove_hr_logo_image.resize(
            (window_width, window_height)
        )
        self.remove_hr_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.remove_hr_logo_canvas.delete("all")
        self.remove_hr_logo_canvas.create_image(
            0, 0, image=self.remove_hr_logo_image, anchor="nw"
        )

    def on_window_resize_remove_hr(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_remove_hr()

    def open_hr_window(self, role, username):
        self.root.destroy()  # Close the main login window
        hr_window = tk.Tk()  # Use Tk() to create a new window
        hr_window.geometry("800x600")  # Set the window size
        hr_window.title("HR Window")

        # create a canvas that resizes with the window
        self.hr_logo_canvas = tk.Canvas(hr_window, bg="white", highlightthickness=0)
        self.hr_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        hr_window.bind("<Configure>", lambda event: self.on_window_resize_hr(event,username))

        # import the image as the background on the canvas
        self.load_image_hr(username)


        #buttons of HR window
        self.salary_management_button = tk.Button(
            self.hr_logo_canvas, text="Salary Management", command=lambda:self.salary_management(), font=("Helvetica", 14)
        )
        self.salary_management_button.pack(
            pady=20
        )
        self.salary_management_button.place(
            relx=0.75, rely=0.3, anchor="center", width=200, height=30
        )
        self.employee_add_remove_button = tk.Button(
            self.hr_logo_canvas, text="Employee Add/Remove", command=lambda:self.employee_add_remove(), font=("Helvetica", 14)
        )
        self.employee_add_remove_button.pack(
            pady=20
        )
        self.employee_add_remove_button.place(
            relx=0.75, rely=0.375, anchor="center", width=230, height=30
        )
        self.approve_bonus_button = tk.Button(
            self.hr_logo_canvas, text="Approve Bonus", command=lambda:self.approve_bonus(), font=("Helvetica", 14)
        )
        self.approve_bonus_button.pack(
            pady=20
        )
        self.approve_bonus_button.place(

            relx=0.75, rely=0.450, anchor="center", width=200, height=30
        )
        self.approve_resignation_button = tk.Button(
            self.hr_logo_canvas, text="Approve Resignation", command=lambda:self.approve_resignation(), font=("Helvetica", 14)
        )
        self.approve_resignation_button.pack(
            pady=20
        )
        self.approve_resignation_button.place(
            relx=0.75, rely=0.525, anchor="center", width=200, height=30
        )
        self.check_hours_attended_button = tk.Button(
            self.hr_logo_canvas, text="Check Employee Hours Attended", command=lambda:self.check_hours_attended(), font=("Helvetica", 14)
        )
        self.check_hours_attended_button.pack(
            pady=20
        )
        self.check_hours_attended_button.place(
            relx=0.75, rely=0.6, anchor="center", width=300, height=30
        )
        self.survey_feedback_button = tk.Button(
            self.hr_logo_canvas, text="Survey/Feedback", command=lambda:self.survey_feedback(), font=("Helvetica", 14)
        )
        self.survey_feedback_button.pack(
            pady=20
        )
        self.survey_feedback_button.place(
            relx=0.75, rely=0.675, anchor="center", width=200, height=30
        )
        self.addbe_button = tk.Button(
            self.hr_logo_canvas, text="Add Boss/Employee", command=lambda:self.create_all_hr(), font=("Helvetica", 14)
        )
        self.addbe_button.pack(
            pady=20
        )
        self.addbe_button.place(
            relx=0.75, rely=0.750, anchor="center", width=300, height=30
        )
        self.removebe_button = tk.Button(
            self.hr_logo_canvas, text="Remove Boss/Employee", command=lambda:self.remove_all_hr(), font=("Helvetica", 14)
        )
        self.removebe_button.pack(
            pady=20
        )
        self.removebe_button.place(
            relx=0.75, rely=0.825, anchor="center", width=300, height=30
        )

        #create an exit button in canvas and place at bottom middle
        exit_button = tk.Button(
        self.hr_logo_canvas,
        text="Exit",
        command=hr_window.destroy,
        font=("Helvetica", 14),
        width=15,
        height=2,
        bd=0,
        fg="white",
        bg="#FF4500",
        activebackground="#FF6347",
    )
        exit_button.place(relx=0.5, rely=1.0, anchor="s")

        # focus on window
        hr_window.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(hr_window)

        # Bind the Escape key to the exit function
        hr_window.bind("<Escape>", lambda event: hr_window.destroy())

        #  Run the main loop for the HR window
        hr_window.mainloop()

    def load_image_hr(self,username):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_hr_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_hr(username)

    def resize_canvas_and_image_hr(self,username):
        username_hr = username
        # Get the hr window size
        window_width = self.hr_logo_canvas.winfo_width()
        window_height = self.hr_logo_canvas.winfo_height()
       

        # Resize the canvas to the current window size
        self.hr_logo_canvas.config(width=window_width, height=window_height)


        # Resize the image if needed
        resized_image = self.original_hr_logo_image.resize(
            (window_width, window_height)
        )
        self.hr_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.hr_logo_canvas.delete("all")
        self.hr_logo_canvas.create_image(
            0, 0, image=self.hr_logo_image, anchor="nw"
        )

         #redraw the hr name text    
        if hasattr(self, "hr_name_text"):
            self.hr_logo_canvas.delete(
                self.hr_name_text
            )
        self.hr_name_text = self.hr_logo_canvas.create_text(
            window_width / 2,
            100,
            text=f"Welcome {username_hr}!",
            font=("Helvetica", 28, "bold"),
            fill="white",
        )

    def on_window_resize_hr(self, event,username):
        # Handle window resize event
        self.resize_canvas_and_image_hr(username)

    def salary_management(self):
        messagebox.showinfo("HR Window", "Salary Management Button Pressed")

    def employee_add_remove(self):
        messagebox.showinfo("HR Window", "Employee Add/Remove Button Pressed")

    def approve_bonus(self):
        messagebox.showinfo("HR Window", "Approve Bonus Button Pressed")

    def approve_resignation(self):
        messagebox.showinfo("HR Window", "Approve Resignation Button Pressed")

    def check_hours_attended(self):
        messagebox.showinfo("HR Window", "Check Employee Hours Attended Button Pressed")

    def survey_feedback(self):
        messagebox.showinfo("HR Window", "Survey/Feedback Button Pressed")

    def create_all_hr(self):
        # create a new window
        create_remove_hr_window = tk.Toplevel()
        create_remove_hr_window.geometry("800x600")  # Set the window size
        create_remove_hr_window.title("Create Boss/Employee Login")

        #create a canvas that resizes with the window
        self.create_be_logo_canvas = tk.Canvas(create_remove_hr_window, bg="white", highlightthickness=0)
        self.create_be_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        create_remove_hr_window.bind("<Configure>", lambda event: self.on_window_resize_create_be(event))

        # import the image as the background on the canvas
        self.load_image_create_be()

        #create a new entry for username on canvas
        username_label = tk.Label(
            self.create_be_logo_canvas,
            text="Username",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        username_label.pack(
            pady=20
        )
        username_label.place(relx=0.5, rely=0.35, anchor="center")
        self.username_entry = tk.Entry(
            self.create_be_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.username_entry.pack(
            pady=20
        )
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")
        self.username_entry.insert(0, "")
        # create a new entry for password on canvas
        password_label = tk.Label(
            self.create_be_logo_canvas,
            text="Password",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        password_label.pack(
            pady=20
        )
        password_label.place(relx=0.5, rely=0.5, anchor="center")
        self.password_entry = tk.Entry(

            self.create_be_logo_canvas, show="", font=("Helvetica", 12, "bold")
        )
        self.password_entry.pack(
            pady=20
        )
        self.password_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.password_entry.insert(0, "")
        # create a checkbox for role with options- HR, boss, employee on canvas
        role_label = tk.Label(
            self.create_be_logo_canvas,
            text="Role",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        role_label.pack(
            pady=20
        )
        role_label.place(relx=0.5, rely=0.65, anchor="center")
        self.role_entry = ttk.Combobox(
            self.create_be_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.role_entry["values"] = ("boss", "employee")
        self.role_entry.pack(
            pady=20
        )
        self.role_entry.place(relx=0.5, rely=0.7, anchor="center")
        self.role_entry.current(0)
        # create a new button for adding the new login on canvas
        add_button = tk.Button(
            self.create_be_logo_canvas,
            text="Add",
            command=self.add_login_to_database,
            font=("Helvetica", 14),
        )
        add_button.pack(
            pady=20
        )
        add_button.place(relx=0.5, rely=0.8, anchor="center", width=100, height=30)
        # store the values in 3 variables when the button is pressed
        add_button.bind(
            "<Button-1>",
            lambda event: self.add_login_to_database(create_remove_hr_window),
        )
        # Bind the Escape key to the exit function
        create_remove_hr_window.bind(
            "<Escape>", lambda event: create_remove_hr_window.destroy()
        )
        # focus on window
        create_remove_hr_window.focus_force()
        # Center the window with function center_window_test
        self.center_window_all(create_remove_hr_window)
        # Run the main loop for the create_remove_hr_window
        create_remove_hr_window.mainloop()

    def load_image_create_be(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_create_be_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_create_be()

    def resize_canvas_and_image_create_be(self):
        # Get the create_be window size
        window_width = self.create_be_logo_canvas.winfo_width()
        window_height = self.create_be_logo_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.create_be_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_create_be_logo_image.resize(
            (window_width, window_height)
        )
        self.create_be_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.create_be_logo_canvas.delete("all")
        self.create_be_logo_canvas.create_image(
            0, 0, image=self.create_be_logo_image, anchor="nw"
        )

    def on_window_resize_create_be(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_create_be()

    def remove_all_hr(self):
        # create a new window
        create_remove_hr_window = tk.Toplevel()
        create_remove_hr_window.geometry("800x600")  # Set the window size
        create_remove_hr_window.title("Remove Boss/Employee Login")
      
        #create a canvas that resizes with the window
        self.remove_be_logo_canvas = tk.Canvas(create_remove_hr_window, bg="white", highlightthickness=0)
        self.remove_be_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        create_remove_hr_window.bind("<Configure>", lambda event: self.on_window_resize_remove_be(event))

        # import the image as the background on the canvas
        self.load_image_remove_be()

        #create a new entry for username on canvas
        username_label = tk.Label(
            self.remove_be_logo_canvas,
            text="Username",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        username_label.pack(
            pady=20
        )
        username_label.place(relx=0.5, rely=0.35, anchor="center")

        self.username_entry = tk.Entry(

            self.remove_be_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.username_entry.pack(
            pady=20
        )
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")
        self.username_entry.insert(0, "")
        # create a checkbox for role with options- HR, boss, employee on canvas
        role_label = tk.Label(
            self.remove_be_logo_canvas,
            text="Role",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        role_label.pack(
            pady=20
        )
        role_label.place(relx=0.5, rely=0.5, anchor="center")
        self.role_entry = ttk.Combobox(
            self.remove_be_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.role_entry["values"] = ("boss", "employee")
        self.role_entry.pack(
            pady=20
        )
        self.role_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.role_entry.current(0)
        # create a new button for removing the login on canvas
        remove_button = tk.Button(
            self.remove_be_logo_canvas,
            text="Remove",
            command=self.remove_login_from_database,
            font=("Helvetica", 14),
        )
        remove_button.pack(
            pady=20
        )
        remove_button.place(relx=0.5, rely=0.65, anchor="center", width=100, height=30)
        # store the values in 2 variables when the button is pressed
        remove_button.bind(

            "<Button-1>",
            lambda event: self.remove_login_from_database(create_remove_hr_window),
        )
        # Bind the Escape key to the exit function
        create_remove_hr_window.bind(
            "<Escape>", lambda event: create_remove_hr_window.destroy()
        )
        # focus on window
        create_remove_hr_window.focus_force()
        # Center the window with function center_window_test
        self.center_window_all(create_remove_hr_window)
        # Run the main loop for the create_remove_hr_window
        create_remove_hr_window.mainloop()

    def load_image_remove_be(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_remove_be_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_remove_be()

    def resize_canvas_and_image_remove_be(self):
        # Get the remove_be window size
        window_width = self.remove_be_logo_canvas.winfo_width()
        window_height = self.remove_be_logo_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.remove_be_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_remove_be_logo_image.resize(
            (window_width, window_height)
        )
        self.remove_be_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.remove_be_logo_canvas.delete("all")
        self.remove_be_logo_canvas.create_image(
            0, 0, image=self.remove_be_logo_image, anchor="nw"
        )

    def on_window_resize_remove_be(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_remove_be()

    def open_boss_window(self, role, username):
        self.root.destroy()  # Close the main login window
        boss_window = tk.Tk()  # Use Tk() to create a new window
        boss_window.geometry("800x600")  # Set the window size
        boss_window.title("Boss Window")


        # create a canvas that resizes with the window
        self.boss_logo_canvas = tk.Canvas(boss_window, bg="white", highlightthickness=0)
        self.boss_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        boss_window.bind("<Configure>", lambda event: self.on_window_resize_boss(event,username))

        # import the image as the background on the canvas
        self.load_image_boss(username)

        #buttons of Boss window
        self.perform_review_approval_button = tk.Button(
            self.boss_logo_canvas, text="Performance Review Approval", command=lambda:self.perform_review_approval(), font=("Helvetica", 14)
        )
        self.perform_review_approval_button.pack(
            pady=20
        )
        self.perform_review_approval_button.place(
            relx=0.5, rely=0.3, anchor="center", width=300, height=30
        )
        self.approve_vacations_sick_leaves_button = tk.Button(
            self.boss_logo_canvas, text="Approve Vacations and Sick Leaves", command=lambda:self.approve_vacations_sick_leaves(), font=("Helvetica", 14)
        )
        self.approve_vacations_sick_leaves_button.pack(
            pady=20
        )
        self.approve_vacations_sick_leaves_button.place(
            relx=0.5, rely=0.4, anchor="center", width=320, height=30
        )
        self.progress_on_task_button = tk.Button(
            self.boss_logo_canvas, text="Progress on Task", command=lambda:self.progress_on_task(), font=("Helvetica", 14)
        )
        self.progress_on_task_button.pack(
            pady=20
        )
        self.progress_on_task_button.place(
          relx=0.5, rely=0.5, anchor="center", width=200, height=30
        )
        self.approve_promotion_button = tk.Button(
            self.boss_logo_canvas, text="Approve Promotion", command=lambda:self.approve_promotion(), font=("Helvetica", 14)
        )
        self.approve_promotion_button.pack(
            pady=20
        )
        self.approve_promotion_button.place(
            relx=0.5, rely=0.6, anchor="center", width=200, height=30
        )
        self.approve_resignation_button = tk.Button(
            self.boss_logo_canvas, text="Approve Resignation", command=lambda:self.approve_resignation(), font=("Helvetica", 14)
        )
        self.approve_resignation_button.pack(
            pady=20
        )
        self.approve_resignation_button.place(
            relx=0.5, rely=0.7, anchor="center", width=200, height=30
        )
        self.request_bonus_button = tk.Button(
            self.boss_logo_canvas, text="Request for Bonus", command=lambda:self.request_bonus(), font=("Helvetica", 14)
        )
        self.request_bonus_button.pack(
            pady=20
        )
        self.request_bonus_button.place(
            relx=0.5, rely=0.8, anchor="center", width=200, height=30
        )

        #create an exit button in canvas and place at bottom middle
        exit_button = tk.Button(
        self.boss_logo_canvas,
        text="Exit",
        command=boss_window.destroy,
        font=("Helvetica", 14),
        width=15,
        height=2,
        bd=0,
        fg="white",
        bg="#FF4500",
        activebackground="#FF6347",
    )
        exit_button.place(relx=0.5, rely=1.0, anchor="s")

        # focus on window
        boss_window.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(boss_window)

        # Bind the Escape key to the exit function
        boss_window.bind("<Escape>", lambda event: boss_window.destroy())

        # Run the main loop for the boss window
        boss_window.mainloop()

    def load_image_boss(self,username):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_boss_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_boss(username)

    def resize_canvas_and_image_boss(self,username):
        username_boss = username
        # Get the boss window size
        window_width = self.boss_logo_canvas.winfo_width()
        window_height = self.boss_logo_canvas.winfo_height()
       
        # Resize the canvas to the current window size
        self.boss_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_boss_logo_image.resize(
            (window_width, window_height)
        )
        self.boss_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.boss_logo_canvas.delete("all")
        self.boss_logo_canvas.create_image(
            0, 0, image=self.boss_logo_image, anchor="nw"
        )

         #redraw the boss name text    
        if hasattr(self, "boss_name_text"):
            self.boss_logo_canvas.delete(
                self.boss_name_text
            )  # Remove the old text

        self.boss_name_text = self.boss_logo_canvas.create_text(
            window_width / 2,
            100,
            text=f"Welcome {username_boss}!",
            font=("Helvetica", 28, "bold"),
            fill="white",
        )

    def on_window_resize_boss(self, event,username):
        # Handle window resize event
        self.resize_canvas_and_image_boss(username)

    def perform_review_approval(self):
        messagebox.showinfo("Boss Window", "Performance Review Approval Button Pressed")

    def approve_vacations_sick_leaves(self):
        messagebox.showinfo(
            "Boss Window", "Approve Vacations and Sick Leaves Button Pressed"
        )

    def progress_on_task(self):
        messagebox.showinfo("Boss Window", "Progress on Task Button Pressed")

    def approve_promotion(self):
        messagebox.showinfo("Boss Window", "Approve Promotion Button Pressed")

    def approve_resignatin(self):
        messagebox.showinfo("Boss Window", "Approve Resignation Button Pressed")

    def request_bonus(self):
        messagebox.showinfo("Boss Window", "Request for Bonus Button Pressed")

    def open_employee_window(self, role, username):
        self.root.destroy()  # Close the main login window
        employee_window = tk.Tk()  # Use Tk() to create a new window
        employee_window.geometry("800x600")  # Set the window size
        employee_window.title("Employee Window")
        employee_ref = db.reference("/employee")
        emp_id = employee_ref.child(username).child("emp_id").get()
        designation = employee_ref.child(username).child("designation").get()
        salary = employee_ref.child(username).child("salary").get()
        sickdays = employee_ref.child(username).child("sick_days").get()
        vacationdays = employee_ref.child(username).child("vacation_days").get()
        bonus = employee_ref.child(username).child("bonus").get()
        hours_attended = employee_ref.child(username).child("hours_attended").get()

       # create a canvas that resizes with the window
        self.employee_logo_canvas = tk.Canvas(employee_window, bg="white", highlightthickness=0)
        self.employee_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        employee_window.bind("<Configure>", lambda event: self.on_window_resize_employee(event,username))

        # import the image as the background on the canvas
        self.load_image_employee(username)

        #buttons of Employee window to the right side of the screen
        self.apply_for_vacation_days_button = tk.Button(
            self.employee_logo_canvas, text="Apply for Vacation Days", command=lambda:self.apply_for_vacation_days(username), font=("Helvetica", 14)
        )
        self.apply_for_vacation_days_button.pack(
            pady=20
        )
        self.apply_for_vacation_days_button.place(
            relx=0.75, rely=0.3, anchor="center", width=300, height=30
        )

        self.apply_for_resignation_button = tk.Button(
            self.employee_logo_canvas, text="Apply for Resignation", command=lambda:self.apply_for_resignation(), font=("Helvetica", 14)
        )
        self.apply_for_resignation_button.pack(
            pady=20
        )
        self.apply_for_resignation_button.place(
            relx=0.75, rely=0.4, anchor="center", width=300, height=30
        )

        self.check_progress_on_tasks_button = tk.Button(
            self.employee_logo_canvas, text="Check and update Progress on Tasks", command=lambda:self.check_progress_on_tasks(), font=("Helvetica", 14)
        )
        self.check_progress_on_tasks_button.pack(
            pady=20
        )
        self.check_progress_on_tasks_button.place(
            relx=0.75, rely=0.5, anchor="center", width=350, height=30
        )

        self.submit_survey_button = tk.Button(
            self.employee_logo_canvas, text="View and Submit Survey", command=lambda:self.submit_survey(), font=("Helvetica", 14)
        )
        self.submit_survey_button.pack(
            pady=20
        )
        self.submit_survey_button.place(
            relx=0.75, rely=0.6, anchor="center", width=300, height=30
        )

        self.submit_feedback_button = tk.Button(
            self.employee_logo_canvas, text="View and Submit Feedback", command=lambda:self.submit_feedback(), font=("Helvetica", 14)
        )
        self.submit_feedback_button.pack(
            pady=20
        )
        self.submit_feedback_button.place(
            relx=0.75, rely=0.7, anchor="center", width=300, height=30
        )

        self.submit_complaint_button = tk.Button(

            self.employee_logo_canvas, text="Submit Complaint", command=lambda:self.submit_complaint(), font=("Helvetica", 14)
        )
        self.submit_complaint_button.pack(
            pady=20
        )
        self.submit_complaint_button.place(
            relx=0.75, rely=0.8, anchor="center", width=300, height=30
        )

        #create an exit button in canvas and place at bottom middle
        exit_button = tk.Button(
        self.employee_logo_canvas,
        text="Exit",
        command=employee_window.destroy,
        font=("Helvetica", 14),
        width=15,
        height=2,
        bd=0,
        fg="white",
        bg="#FF4500",
        activebackground="#FF6347",
    )
        exit_button.place(relx=0.5, rely=1.0, anchor="s")

        # focus on window
        employee_window.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(employee_window)

        # Bind the Escape key to the exit function
        employee_window.bind("<Escape>", lambda event: employee_window.destroy())

        # Run the main loop for the employee window
        employee_window.mainloop()
       
    def load_image_employee(self,username):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_employee_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_employee(username)

    def resize_canvas_and_image_employee(self,username):
        username_employee = username
        # Get the employee window size
        window_width = self.employee_logo_canvas.winfo_width()
        window_height = self.employee_logo_canvas.winfo_height()
        employee_ref = db.reference("/employee")
        emp_id = employee_ref.child(username).child("emp_id").get()
        designation = employee_ref.child(username).child("designation").get()
        salary = employee_ref.child(username).child("salary").get()
        sickdays = employee_ref.child(username).child("sick_days").get()
        vacationdays = employee_ref.child(username).child("vacation_days").get()
        bonus = employee_ref.child(username).child("bonus").get()
        hours_attended = employee_ref.child(username).child("hours_attended").get()

        # Resize the canvas to the current window size
        self.employee_logo_canvas.config(width=window_width, height=window_height)


        # Resize the image if needed
        resized_image = self.original_employee_logo_image.resize(
            (window_width, window_height)
        )
        self.employee_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.employee_logo_canvas.delete("all")
        self.employee_logo_canvas.create_image(
            0, 0, image=self.employee_logo_image, anchor="nw"
        )

        #redraw the employee name text    
        if hasattr(self, "employee_name_text"):
            self.employee_logo_canvas.delete(
                self.employee_name_text
            )

        self.employee_name_text = self.employee_logo_canvas.create_text(
            window_width / 2,
            100,
            text=f"Welcome {username_employee}!",
            font=("Helvetica", 28, "bold"),
            fill="white",
        )
        #redraw the employee details text
        if hasattr(self, "employee_details_text"):
            self.employee_logo_canvas.delete(
                self.employee_details_text
            )
        
        self.employee_details_text = self.employee_logo_canvas.create_text(
            #place it on the leftmost of the window
            10,
            window_height-10,
            text=f"Employee ID: {emp_id}\nDesignation: {designation}\nSalary: {salary}\nSick Days: {sickdays}\nVacation Days: {vacationdays}\nBonus: {bonus}\nHours Attended: {hours_attended}",
            font=("Helvetica", 18, "bold"),
            fill="white",
            anchor='sw',
        )
        
    def on_window_resize_employee(self, event,username):
        # Handle window resize event
        self.resize_canvas_and_image_employee(username)

    def apply_for_vacation_days(self,username):
        messagebox.showinfo("Employee Window", "Apply for Vacation Days Button Pressed")
        #create a new window over the employee window
        # apply_vacation_window = tk.Toplevel()
        # apply_vacation_window.geometry("800x600")  # Set the window size
        # apply_vacation_window.title("Apply for Vacation Days")
        
    def apply_for_resignation(self):
        messagebox.showinfo("Employee Window", "Apply for Resignation Button Pressed")

    def check_progress_on_tasks(self):
        messagebox.showinfo("Employee Window", "Check Progress on Tasks Button Pressed")

    def submit_survey(self):
        messagebox.showinfo("Employee Window", "Submit Survey Button Pressed")

    def submit_feedback(self):
        messagebox.showinfo("Employee Window", "Submit Feedback Button Pressed")

    def submit_complaint(self):
        messagebox.showinfo("Employee Window", "Submit Complaint Button Pressed")

    def center_window_all(self, window):
        # Get the width and height of the screen
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Calculate the x and y coordinates to center the main window
        x = (screen_width / 2) - (900 / 2)
        y = (screen_height / 2) - (600 / 2)

        # Set the dimensions of the screen and where it is placed
        window.geometry("%dx%d+%d+%d" % (900, 600, x, y))

    def add_login_to_database(self, create_remove_hr_window):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_entry.get()

        admins_ref = db.reference("/admins")
        hr_ref = db.reference("/HR")
        boss_ref = db.reference("/boss")
        employee_ref = db.reference("/employee")
        emp_id_ref = db.reference("/")
        emp_uni = emp_id_ref.child("emp_id").get()

        if (
            admins_ref.child(username).get()
            or hr_ref.child(username).get()
            or boss_ref.child(username).get()
            or employee_ref.child(username).get()
        ):
            messagebox.showinfo(
                "Add HR Login", "Username already exists. Choose a different username."
            )
        else:
            # Add the new login to the database
            if role == "HR":
                hr_ref.child(username).set(
                    {
                        "password": password,
                        "role": role,
                        "post:": "",
                        "salary": "",
                        "emp_id": emp_uni + 1,
                    }
                )
                emp_id_ref.child("emp_id").set(emp_uni + 1)
            elif role == "boss":
                boss_ref.child(username).set(
                    {
                        "password": password,
                        "role": role,
                        "designnation: ": "",
                        "salary": "",
                        "emp_ids": emp_uni + 1,
                    }
                )
                emp_id_ref.child("emp_id").set(emp_uni + 1)
            elif role == "employee":
                employee_ref.child(username).set(
                    {
                        "password": password,
                        "role": role,
                        "designation": "",
                        "emp_id": emp_uni + 1,
                        "salary": "",
                        "sick days": "",
                        "vacation days": "",
                        "bonus": "",
                        "hours attended": "",
                        "apply for resignation": "",
                        "apply for vacation": "",
                        "progress on task": "",
                        "survey": "",
                        "feedback": "",
                    }
                )
                emp_id_ref.child("emp_id").set(emp_uni + 1)
            messagebox.showinfo("Add HR Login", "Login added successfully.")
        # close the window
        create_remove_hr_window.destroy()

    def remove_login_from_database(self, create_remove_hr_window):
        username = self.username_entry.get()
        role = self.role_entry.get()
        admins_ref = db.reference("/admins")
        hr_ref = db.reference("/HR")
        boss_ref = db.reference("/boss")
        employee_ref = db.reference("/employee")
        if role == "HR":
            if hr_ref.child(username).get():
                # Remove the login from the database
                hr_ref.child(username).delete()
                messagebox.showinfo("Remove HR Login", "Login removed successfully.")
            else:
                messagebox.showinfo("Remove HR Login", "Username does not exist.")
        elif role == "boss":
            if boss_ref.child(username).get():
                # Remove the login from the database
                boss_ref.child(username).delete()
                messagebox.showinfo("Remove HR Login", "Login removed successfully.")
            else:
                messagebox.showinfo("Remove HR Login", "Username does not exist.")
        elif role == "employee":
            if employee_ref.child(username).get():
                # Remove the login from the database
                employee_ref.child(username).delete()
                messagebox.showinfo("Remove HR Login", "Login removed successfully.")
            else:
                messagebox.showinfo("Remove HR Login", "Username does not exist.")
        # close the window
        create_remove_hr_window.destroy()

def main():
    root = tk.Tk()
    root.geometry("900x600")  # Set the window size
    app = CreativeLoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
