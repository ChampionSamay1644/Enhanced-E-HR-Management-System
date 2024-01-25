import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog, ttk
from PIL import Image, ImageTk
import os
import firebase_admin
from firebase_admin import db, credentials

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
        self.root.destroy()  # Close the main login window
        admin_window = tk.Tk()  # Use Tk() to create a new window
        admin_window.geometry("900x600")  # Set the window size
        admin_window.title("Admin Window")

        
         # create a canvas that resizes with the window
        self.admin_logo_canvas = tk.Canvas(admin_window, bg="white", highlightthickness=0)
        self.admin_logo_canvas.pack(fill=tk.BOTH, expand=True)

         # bind window resize event to function
        admin_window.bind("<Configure>", lambda event: self.on_window_resize_admin(event))


         # import the image as the background on the canvas
        self.load_image_admin()

        # # Background image for the admin window
        # admin_img_path = os.path.join(
        #     os.path.dirname(os.path.realpath(__file__)), "HR_background.png"
        # )
        # admin_original_image = Image.open(admin_img_path)
        # admin_img = ImageTk.PhotoImage(admin_original_image)

        # admin_background_label = tk.Label(admin_window, image=admin_img, bg="white")
        # admin_background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # # Welcome message for the admin
        # welcome_label = tk.Label(
        #     admin_window,
        #     text="Welcome Admin!",
        #     font=("Helvetica", 18, "bold"),
        #     fg="white",
        #     bg="black",
        # )
        # welcome_label.pack(pady=20)

        # Buttons for Admin window
        buttons1_info = [
            (
                (
                    "Create HR Login",
                    lambda: self.create_all_admin(button_create_all_admin),
                )
            ),  # Use lambda to delay the method call
        ]

        admin_buttons_frame = tk.Frame(
            admin_window, bg="black"
        )  # Define admin_buttons_frame
        admin_buttons_frame.pack(pady=20)

        for i, (button_text, button_command) in enumerate(buttons1_info):
            button_create_all_admin = tk.Button(
                admin_buttons_frame,
                text=button_text,
                command=button_command,
                font=("Helvetica", 14),
                width=20,
                height=2,
                bd=0,
                fg="white",
                bg="#2E4053",
                activebackground="#566573",
            )
            button_create_all_admin.grid(row=i // 2, column=i % 2, padx=10, pady=10)

        # Create a 2nd button for remove HR login
        buttons2_info = [
            (
                (
                    "Remove HR Login",
                    lambda: self.remove_all_admin(button_remove_all_admin),
                )
            ),  # Use lambda to delay the method call
        ]

        for i, (button_text, button_command) in enumerate(buttons2_info):
            button_remove_all_admin = tk.Button(
                admin_buttons_frame,
                text=button_text,
                command=button_command,
                font=("Helvetica", 14),
                width=20,
                height=2,
                bd=0,
                fg="white",
                bg="#2E4053",
                activebackground="#566573",
            )
            button_remove_all_admin.grid(
                row=i // 2 + 1, column=i % 2, padx=10, pady=10
            )  # Adjusted row value

        exit_button = tk.Button(
            admin_window,
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
        exit_button.place(relx=0.5, rely=0.95, anchor="center")

        # focus on window
        admin_window.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(admin_window)

        # Bind the Escape key to the exit function
        admin_window.bind("<Escape>", lambda event: admin_window.destroy())

     

        # Run the main loop for the admin window
        admin_window.mainloop()



    def load_image_admin(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_admin_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_admin()
    # def load_image_admin(self,img_path,role,username):
    #     # Load image and adjust canvas size
    #     self.original_admin_logo_image = Image.open(img_path)
    #     self.resize_canvas_and_image_admin()

    def resize_canvas_and_image_admin(self):
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

        # Redraw the company name text
        if hasattr(self, "admin_name_text"):
            self.admin_logo_canvas.delete(
                self.admin_name_text
            )  # Remove the old text
        self.admin_name_text = self.admin_logo_canvas.create_text(
            window_width / 2,
            100,
            text="Welcome {username}!",
            font=("Helvetica", 28, "bold"),
            fill="white",
        )
    
    def on_window_resize_admin(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_admin()


    def create_all_admin(self, button1):
        # create a new window
        create_remove_hr_window = tk.Toplevel()
        create_remove_hr_window.geometry("800x600")  # Set the window size
        create_remove_hr_window.title("Create HR Login")
        # create a new entry for username
        username_label = tk.Label(
            create_remove_hr_window,
            text="Username",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        username_label.place(relx=0.5, rely=0.35, anchor="center")
        self.username_entry = tk.Entry(
            create_remove_hr_window, font=("Helvetica", 12, "bold")
        )
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")
        self.username_entry.insert(0, "")
        # create a new entry for password
        password_label = tk.Label(
            create_remove_hr_window,
            text="Password",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        password_label.place(relx=0.5, rely=0.5, anchor="center")
        self.password_entry = tk.Entry(
            create_remove_hr_window, show="", font=("Helvetica", 12, "bold")
        )
        self.password_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.password_entry.insert(0, "")
        # create a new checkbox for role with options- HR, boss, employee
        role_label = tk.Label(
            create_remove_hr_window,
            text="Role",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        role_label.place(relx=0.5, rely=0.65, anchor="center")
        self.role_entry = ttk.Combobox(
            create_remove_hr_window, font=("Helvetica", 12, "bold")
        )
        self.role_entry["values"] = ("HR", "boss", "employee")
        self.role_entry.place(relx=0.5, rely=0.7, anchor="center")
        self.role_entry.current(0)
        # create a new button for adding the new login
        add_button = tk.Button(
            create_remove_hr_window,
            text="Add",
            command=self.add_login_to_database,
            font=("Helvetica", 14),
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

    def remove_all_admin(self, button2):
        # create a new window
        create_remove_hr_window = tk.Toplevel()
        create_remove_hr_window.geometry("800x600")  # Set the window size
        create_remove_hr_window.title("Remove HR Login")
        # create a new entry for username
        username_label = tk.Label(
            create_remove_hr_window,
            text="Username",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        username_label.place(relx=0.5, rely=0.35, anchor="center")
        self.username_entry = tk.Entry(
            create_remove_hr_window, font=("Helvetica", 12, "bold")
        )
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")
        self.username_entry.insert(0, "")
        # create a checkbox for role with options- HR, boss, employee
        role_label = tk.Label(
            create_remove_hr_window,
            text="Role",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        role_label.place(relx=0.5, rely=0.5, anchor="center")
        self.role_entry = ttk.Combobox(
            create_remove_hr_window, font=("Helvetica", 12, "bold")
        )
        self.role_entry["values"] = ("HR", "boss", "employee")
        self.role_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.role_entry.current(0)
        # create a new button for removing the login
        remove_button = tk.Button(
            create_remove_hr_window,
            text="Remove",
            command=self.remove_login_from_database,
            font=("Helvetica", 14),
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

    def open_hr_window(self, role, username):
        self.root.destroy()  # Close the main login window
        hr_window = tk.Tk()  # Use Tk() to create a new window
        hr_window.geometry("800x600")  # Set the window size
        hr_window.title("HR Window")

        # Background image for the HR window
        hr_img_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "HR_background.png"
        )
        hr_original_image = Image.open(hr_img_path)
        self.hr_img = ImageTk.PhotoImage(hr_original_image)

        hr_background_label = tk.Label(hr_window, image=self.hr_img, bg="white")
        hr_background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Welcome message for the HR
        welcome_label = tk.Label(
            hr_window,
            text="Welcome HR!",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="black",
        )
        welcome_label.pack(pady=20)

        buttons_info = [
            ("Salary Management", self.salary_management),
            ("Employee Add/Remove", self.employee_add_remove),
            ("Approve Bonus", self.approve_bonus),
            ("Approve Resignation", self.approve_resignation),
            ("Check Employee Hours", self.check_hours_attended),
            ("Survey/Feedback", self.survey_feedback),
            ("Add Boss/Employees", self.create_all_hr),
            ("Remove Boss/Employees", self.remove_all_hr),
        ]

        hr_buttons_frame = tk.Frame(hr_window, bg="black")  # Define hr_buttons_frame
        hr_buttons_frame.pack(pady=20)

        for i, (button_text, button_command) in enumerate(buttons_info):
            button = tk.Button(
                hr_buttons_frame,
                text=button_text,
                command=button_command,
                font=("Helvetica", 14),
                width=30,
                height=2,
                bd=0,
                fg="white",
                bg="#2E4053",
                activebackground="#566573",
            )
            button.grid(row=i // 2, column=i % 2, padx=10, pady=10)

            # Add an Exit button at the bottom
            exit_button = tk.Button(
                hr_window,
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
            exit_button.place(relx=0.5, rely=0.95, anchor="center")

        # focus on window
        hr_window.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(hr_window)

        # Bind the Escape key to the exit function
        hr_window.bind("<Escape>", lambda event: hr_window.destroy())

        # Bind the window resize event for the HR window
        hr_window.bind(
            "<Configure>",
            lambda event, img=self.hr_img, label=hr_background_label: self.resize_image(
                event, img, label
            ),
        )

        #  Run the main loop for the HR window
        hr_window.mainloop()

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

    def addremovebe(self):
        messagebox.showinfo("HR Window", "Add/Remove Boss/Employee Button Pressed")

    def create_all_hr(self):
        # create a new window
        create_remove_hr_window = tk.Toplevel()
        create_remove_hr_window.geometry("800x600")  # Set the window size
        create_remove_hr_window.title("Create Boss/Employee Login")
        # create a new entry for username
        username_label = tk.Label(
            create_remove_hr_window,
            text="Username",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        username_label.place(relx=0.5, rely=0.35, anchor="center")
        self.username_entry = tk.Entry(
            create_remove_hr_window, font=("Helvetica", 12, "bold")
        )
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")
        self.username_entry.insert(0, "")
        # create a new entry for password
        password_label = tk.Label(
            create_remove_hr_window,
            text="Password",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        password_label.place(relx=0.5, rely=0.5, anchor="center")
        self.password_entry = tk.Entry(
            create_remove_hr_window, show="", font=("Helvetica", 12, "bold")
        )
        self.password_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.password_entry.insert(0, "")
        # create a new checkbox for role with options- HR, boss, employee
        role_label = tk.Label(
            create_remove_hr_window,
            text="Role",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        role_label.place(relx=0.5, rely=0.65, anchor="center")
        self.role_entry = ttk.Combobox(
            create_remove_hr_window, font=("Helvetica", 12, "bold")
        )
        self.role_entry["values"] = ("boss", "employee")
        self.role_entry.place(relx=0.5, rely=0.7, anchor="center")
        self.role_entry.current(0)
        # create a new button for adding the new login
        add_button = tk.Button(
            create_remove_hr_window,
            text="Add",
            command=self.add_login_to_database,
            font=("Helvetica", 14),
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

    def remove_all_hr(self):
        # create a new window
        create_remove_hr_window = tk.Toplevel()
        create_remove_hr_window.geometry("800x600")  # Set the window size
        create_remove_hr_window.title("Remove Boss/Employee Login")
        # create a new entry for username
        username_label = tk.Label(
            create_remove_hr_window,
            text="Username",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        username_label.place(relx=0.5, rely=0.35, anchor="center")
        self.username_entry = tk.Entry(
            create_remove_hr_window, font=("Helvetica", 12, "bold")
        )
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")
        self.username_entry.insert(0, "")
        # create a checkbox for role with options- HR, boss, employee
        role_label = tk.Label(
            create_remove_hr_window,
            text="Role",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        role_label.place(relx=0.5, rely=0.5, anchor="center")
        self.role_entry = ttk.Combobox(
            create_remove_hr_window, font=("Helvetica", 12, "bold")
        )
        self.role_entry["values"] = ("boss", "employee")
        self.role_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.role_entry.current(0)
        # create a new button for removing the login
        remove_button = tk.Button(
            create_remove_hr_window,
            text="Remove",
            command=self.remove_login_from_database,
            font=("Helvetica", 14),
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

    def open_boss_window(self, role, username):
        self.root.destroy()  # Close the main login window
        boss_window = tk.Tk()  # Use Tk() to create a new window
        boss_window.geometry("800x600")  # Set the window size
        boss_window.title("Boss Window")

        # Background image for the boss window
        boss_img_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "HR_background.png"
        )
        self.boss_original_image = Image.open(boss_img_path)
        self.boss_img = ImageTk.PhotoImage(self.boss_original_image)

        boss_background_label = tk.Label(boss_window, image=self.boss_img, bg="white")
        boss_background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Welcome message for the boss
        welcome_label = tk.Label(
            boss_window,
            text="Welcome Boss!",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="black",
        )
        welcome_label.pack(pady=20)

        buttons_info = [
            ("Performance Review Approval", self.perform_review_approval),
            ("Approve Vacations and Sick Leaves", self.approve_vacations_sick_leaves),
            ("Progress on Task", self.progress_on_task),
            ("Approve Promotion", self.approve_promotion),
            ("Approve Resignation", self.approve_resignatin),
            ("Request for Bonus", self.request_bonus),
        ]

        boss_buttons_frame = tk.Frame(
            boss_window, bg="black"
        )  # Define boss_buttons_frame
        boss_buttons_frame.pack(pady=20)

        for i, (button_text, button_command) in enumerate(buttons_info):
            button = tk.Button(
                boss_buttons_frame,
                text=button_text,
                command=button_command,
                font=("Helvetica", 14),
                width=30,
                height=2,
                bd=0,
                fg="white",
                bg="#2E4053",
                activebackground="#566573",
            )
            button.grid(row=i // 2, column=i % 2, padx=10, pady=10)

        # Add an Exit button at the bottom
        exit_button = tk.Button(
            boss_window,
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
        exit_button.place(relx=0.5, rely=0.95, anchor="center")

        # focus on window
        boss_window.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(boss_window)

        # Bind the Escape key to the exit function
        boss_window.bind("<Escape>", lambda event: boss_window.destroy())

        # Bind the window resize event for the boss window
        boss_window.bind(
            "<Configure>",
            lambda event, img=self.boss_img, label=boss_background_label: self.resize_image(
                event, img, label
            ),
        )

        # Run the main loop for the boss window
        boss_window.mainloop()

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

        # Background image for the employee window
        employee_img_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "HR_background.png"
        )
        self.employee_original_image = Image.open(employee_img_path)
        self.employee_img = ImageTk.PhotoImage(self.employee_original_image)

        employee_background_label = tk.Label(
            employee_window, image=self.employee_img, bg="white"
        )
        employee_background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Welcome message for the employee along with username
        welcome_label = tk.Label(
            employee_window,
            text=f"Welcome Employee, {username}!",
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="black",
        )
        welcome_label.pack(pady=20)

        # Show the details pulled from the db on the left side of the window
        details_frame = tk.Frame(employee_window, bg="white", padx=20)
        details_frame.pack(side=tk.LEFT, fill=tk.Y)

        details_labels = [
            ("Employee ID: ", emp_id),
            ("Designation: ", designation),
            ("Salary: ", salary),
            ("Sick Days: ", sickdays),
            ("Vacation Days: ", vacationdays),
            ("Bonus: ", bonus),
            ("Hours Attended: ", hours_attended),
        ]

        for label_text, detail_value in details_labels:
            label = tk.Label(
                details_frame,
                text=label_text,
                font=("Helvetica", 12, "bold"),
                bg="white",
            )
            label.grid(sticky="w")
            value_label = tk.Label(
                details_frame, text=detail_value, font=("Helvetica", 12), bg="white"
            )
            value_label.grid(
                row=details_labels.index((label_text, detail_value)),
                column=1,
                sticky="w",
            )

        # Buttons on the right side of the window
        buttons_frame = tk.Frame(employee_window, bg="black", padx=20)
        buttons_frame.pack(side=tk.RIGHT, fill=tk.Y)

        buttons_info = [
            ("Apply for Vacation Days", self.apply_for_vacation_days),
            ("Apply for Resignation", self.apply_for_resignation),
            ("Check and update Progress on Tasks", self.check_progress_on_tasks),
            ("View and Submit Survey", self.submit_survey),
            ("View and Submit Feedback", self.submit_feedback),
            ("Submit Complaint", self.submit_complaint),
        ]

        for i, (button_text, button_command) in enumerate(buttons_info):
            button = tk.Button(
                buttons_frame,
                text=button_text,
                command=button_command,
                font=("Helvetica", 14),
                width=30,
                height=2,
                bd=0,
                fg="white",
                bg="#2E4053",
                activebackground="#566573",
            )
            button.grid(row=i, column=0, pady=10)

        # Add an Exit button at the bottom
        exit_button = tk.Button(
            employee_window,
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
        exit_button.place(relx=0.5, rely=0.95, anchor="center")

        # focus on window
        employee_window.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(employee_window)

        # Bind the Escape key to the exit function
        employee_window.bind("<Escape>", lambda event: employee_window.destroy())

        # # Bind the window resize event for the employee window
        # employee_window.bind("<Configure>", lambda event, img=self.employee_img, label=employee_background_label: self.resize_image(event, img, label))

        # Run the main loop for the employee window
        employee_window.mainloop()

    def apply_for_vacation_days(self):
        messagebox.showinfo("Employee Window", "Apply for Vacation Days Button Pressed")

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
                        "emp_id": emp_uni + 1,
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