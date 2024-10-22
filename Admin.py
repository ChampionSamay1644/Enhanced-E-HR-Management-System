import datetime
import tkinter as tk
from tkcalendar import Calendar, DateEntry
from tkinter import END, IntVar, Listbox, Radiobutton, messagebox
from tkinter import simpledialog, ttk,scrolledtext
from PIL import Image, ImageTk
import os
import firebase_admin
from firebase_admin import db, credentials
import threading
from tkinter import Label
from tkinter import Tk, Canvas, PhotoImage
from HR import *
from Manager import *
from Employee import *
from main import main as Main

class Admin_class():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Admin Window")

    def load_image_common(self):
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        try:
            self.original_common_image = Image.open(img_path)
        except Exception as e:
            print(f"Error loading image: {e}")
        
    def on_window_resize_common(self,username,role, event=None):
        self.resize_canvas_and_image_common(username,role)

    def create_common_window(self, title,username,role):

        common_window = tk.Tk()
        common_window.geometry("800x600")
        common_window.title(title)

        self.common_canvas = tk.Canvas(common_window, bg="white", highlightthickness=0)
        self.common_canvas.pack(fill=tk.BOTH, expand=True)

        common_window.bind("<Configure>",lambda event,username=username,role=role:self.on_window_resize_common(username,role))

        self.load_image_common()
        self.resize_canvas_and_image_common(username,role)
        
        return common_window, self.common_canvas
        
    def center_window_all(self, window):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width / 2) - (900 / 2)
        y = (screen_height / 2) - (700 / 2)
        window.geometry("%dx%d+%d+%d" % (900, 700, x, y))
        
    def resize_canvas_and_image_common(self,username,role):
        window_width = self.common_canvas.winfo_width()
        window_height = self.common_canvas.winfo_height()
        self.common_canvas.config(width=window_width, height=window_height)

        resized_image = self.original_common_image.resize((window_width, window_height))
        self.common_image = ImageTk.PhotoImage(resized_image)

        self.common_canvas.delete("all")
        self.common_canvas.create_image(0, 0, image=self.common_image, anchor="nw")
        
        if username=="Default" or role=="Default":
            return
        # Add text to the top center of the canvas
        text_content = f"Hello, {username}"
        text_position = (window_width // 2, 20)  # Top center of the canvas
        self.common_canvas.create_text(text_position, text=text_content, anchor="center")
        self.common_canvas.itemconfig(self.common_canvas.find_all()[-1], fill="white")
        
    def open_admin_window(self, role, username):
        if hasattr(self, "root") and self.root.winfo_exists():
            self.root.destroy()  # Close the main login window
        admin_window = tk.Tk()  # Use Tk() to create a new window
        admin_window.geometry("900x600")  # Set the window size
        admin_window.title("Admin Window")
        self.treeview = None
        #create a canvas that resizes with the window
        self.admin_logo_canvas = tk.Canvas(admin_window, bg="white", highlightthickness=0)
        self.admin_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # import the image as the background on the canvas
        self.load_image_admin(username)
        
        # bind window resize event to function
        admin_window.bind("<Configure>", lambda event: self.on_window_resize_admin(username,role))
        
        #create a button on the canvas
        self.create_all_admin_button = tk.Button(
            self.admin_logo_canvas, text="Create/Remove Login", command=lambda:self.manage_login(), font=("Helvetica", 14)
        )
        self.create_all_admin_button.pack(
            pady=20
        )
        self.create_all_admin_button.place(
            relx=0.5, rely=0.4, anchor="center", width=300, height=30
        )
        
        self.approve_resignation_button = tk.Button(
            self.admin_logo_canvas, text="Approve Resignation", command=lambda:self.approve_resignation(), font=("Helvetica", 14)
        )
        self.approve_resignation_button.pack(
            pady=20
        )
        self.approve_resignation_button.place(
            relx=0.5, rely=0.5, anchor="center", width=300, height=30
        )

        #create combo box to select the role
        self.role_entry = ttk.Combobox(
            self.admin_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.role_entry["values"] = ("HR", "manager", "employee")
        self.role_entry.pack(
            pady=20
        )
        self.role_entry.place(relx=0.5, rely=0.6, anchor="center")
        self.role_entry.current(0)

        #create a new button to login as the selected role
        self.login_as_button = tk.Button(
            self.admin_logo_canvas, text="Login as selected role", command=lambda:self.login_as_selected_role(username,admin_window), font=("Helvetica", 14)
        )
        self.login_as_button.pack(
            pady=20
        )
        self.login_as_button.place(
            relx=0.5, rely=0.7, anchor="center", width=200, height=30
        )
        
        profile_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "profile.png")
        profile_image = Image.open(profile_path)
        profile_image = profile_image.resize((50, 50))
        profile_image = ImageTk.PhotoImage(profile_image)
        profile_button = tk.Button(
            self.admin_logo_canvas,
            image=profile_image,
            command=lambda: self.profile(username,role),
            bd=0,
            bg="white",
            activebackground="white",
        )
        profile_button.image = profile_image
        profile_button.pack()
        profile_button.place(relx=0.95, rely=0.05, anchor="ne")

        logout_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "logout.png")
        logout_image = Image.open(logout_path)
        logout_image = logout_image.resize((50, 50))
        logout_image = ImageTk.PhotoImage(logout_image)
        logout_button = tk.Button(
            self.admin_logo_canvas,
            image=logout_image,
            command=lambda: self.logout(admin_window),
            bd=0,
            bg="white",
            activebackground="white",
        )
        logout_button.image = logout_image
        logout_button.pack()
        logout_button.place(relx=0.95, rely=0.95, anchor="se")

        # focus on window
        admin_window.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(admin_window)

        # Bind the Escape key to the exit function
        admin_window.bind("<Escape>", lambda event: admin_window.destroy())

        # Run the main loop for the admin window
        admin_window.mainloop()

    def manage_login(self):
        self.create_remove_hr_window = tk.Toplevel()
        self.create_remove_hr_window.geometry("800x600")
        self.create_remove_hr_window.title("Create/Remove HR Login")
        
        #create a canvas that resizes with the window
        self.create_hr_logo_canvas = tk.Canvas(self.create_remove_hr_window, bg="white", highlightthickness=0)
        self.create_hr_logo_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Load image and adjust canvas size
        self.load_image_create_hr()
        
        # Bind window resize event to function
        self.create_remove_hr_window.bind("<Configure>", lambda event: self.on_window_resize_create_hr(event))
        
        #Create a scrollable frame
        self.scrollable_frame = tk.Frame(self.create_remove_hr_window)
        self.scrollable_frame.pack(fill="both", expand=True)
        self.scrollable_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # create a treeview to display the employees
        if self.treeview is None:
            self.treeview = ttk.Treeview(
                self.scrollable_frame, columns=("Employee",), show="headings", selectmode="browse"
            )
            self.treeview.heading("Employee", text="Employee")
            self.treeview.column("Employee", width=200, anchor="center")
            self.treeview.tag_configure("clickable", foreground="blue", font=("Helvetica", 12, "underline"))
            #Set the treeview rows to be selectable when clciked once
            self.treeview.bind("<Button-1>", lambda event: self.treeview.focus_set())

            # Add a vertical scrollbar to the Treeview
            scrollbar = ttk.Scrollbar(self.scrollable_frame, orient="vertical", command=self.treeview.yview)
            scrollbar.pack(side="right", fill="y")
            self.treeview.configure(yscrollcommand=scrollbar.set)

            # Pack the Treeview to the scrollable frame
            self.treeview.pack(fill="both", expand=True)

        # Configure grid row and column weights
        self.scrollable_frame.grid_rowconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Now you can safely use self.treeview
        self.treeview.delete(*self.treeview.get_children())
        
        # create a tick box for role of the employee
        role_label = tk.Label(
            self.create_hr_logo_canvas,
            text="Role",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        role_label.pack(
            pady=20
        )
        # place it Extreme top middle
        role_label.place(relx=0.5, rely=0.1, anchor="center")
        self.role_entry_emp_mng = ttk.Combobox(
            self.create_hr_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.role_entry_emp_mng["values"] = ("None","HR", "manager", "employee")
        self.role_entry_emp_mng.pack(
            pady=20
        )
        self.role_entry_emp_mng.place(relx=0.5, rely=0.2, anchor="center")
        self.role_entry_emp_mng.current(0)
        
        self.role_entry_emp_mng.bind("<<ComboboxSelected>>", self.role_selected)
        
        #Create a new button for add and remove login
        add_login_button = tk.Button(
            self.create_hr_logo_canvas, text="Add Login", command=lambda:self.add_login_from_admin_window(), font=("Helvetica", 14)
        )
        add_login_button.pack(
            pady=20
        )
        add_login_button.place(
            relx=0.4, rely=0.9, anchor="center", width=100, height=30
        )
        
        #Set the state of the remove button to disabled initially
        remove_login_button = tk.Button(
            self.create_hr_logo_canvas, text="Remove Login", command=lambda:self.remove_login(), font=("Helvetica", 14),state="disabled"
        )
        remove_login_button.pack(
            pady=20
        )
        remove_login_button.place(
            relx=0.6, rely=0.9, anchor="center", width=150, height=30
        )
        
        #Enable the remove button only if a row is selected in the treeview
        self.treeview.bind("<<TreeviewSelect>>", lambda event: remove_login_button.config(state="normal"))
        
        #Center the window with function center_window_test
        self.center_window_all(self.create_remove_hr_window)
        
        #bind the escape key to the exit function
        self.create_remove_hr_window.bind("<Escape>", lambda event: self.create_remove_hr_window.destroy())
        
        # Run the main loop for the self.create_remove_hr_window
        self.create_remove_hr_window.mainloop()
        
    def role_selected(self,event):
        role = self.role_entry_emp_mng.get()
        self.populate_employee_list(role)
        
    def populate_employee_list(self, role):
        # Clear the existing items in the Treeview
        if self.treeview is not None:
            self.treeview.delete(*self.treeview.get_children())
        
        if role == "HR":
            employees = list(( db.reference("/HR").get()).keys())
        elif role == "manager":
            employees = list(( db.reference("/manager").get()).keys())
        elif role == "None":
            return
        else:
            employees = list(( db.reference("/employee").get()).keys())

        # Populate the Treeview with employee names
        for employee in employees:
            self.treeview.insert("", "end", values=(employee,), tags=("clickable",))
        
    def load_image_add_login_from_hr(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_add_login_from_adminimage = Image.open(img_path)
        self.resize_canvas_and_image_add_login_from_hr()

    def resize_canvas_and_image_add_login_from_hr(self):
        # Get the create_hr window size
        window_width = self.add_login_from_admincanvas.winfo_width()
        window_height = self.add_login_from_admincanvas.winfo_height()

        # Resize the canvas to the current window size
        self.add_login_from_admincanvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_add_login_from_adminimage.resize(
            (window_width, window_height)
        )
        self.add_login_from_adminimage = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.add_login_from_admincanvas.delete("all")
        self.add_login_from_admincanvas.create_image(
            0, 0, image=self.add_login_from_adminimage, anchor="nw"
        )

    def on_window_resize_add_login_from_hr(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_add_login_from_hr()
        
    def add_login_from_admin_window(self):
        # Create a new window
        add_login_from_admin_window = tk.Toplevel()
        add_login_from_admin_window.geometry("800x600")  # Set the window size
        add_login_from_admin_window.title("Add Login")

        # Create a canvas that resizes with the window
        self.add_login_from_admincanvas = tk.Canvas(add_login_from_admin_window, bg="white", highlightthickness=0)
        self.add_login_from_admincanvas.pack(fill=tk.BOTH, expand=True)

        # Import the image as the background on the canvas
        self.load_image_add_login_from_hr()

        # Bind window resize event to function
        add_login_from_admin_window.bind("<Configure>", lambda event: self.on_window_resize_add_login_from_hr(event))

        # focus on window
        add_login_from_admin_window.focus_force()
        # Center the window with function center_window_test
        self.center_window_all(add_login_from_admin_window)

        # Create a new entry for username on canvas
        username_label = tk.Label(
            self.add_login_from_admincanvas,
            text="Username",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        username_label.pack(pady=10)
        username_label.place(relx=0.3, rely=0.2, anchor="center")
        self.username_entry = tk.Entry(
            self.add_login_from_admincanvas, font=("Helvetica", 12)
        )
        self.username_entry.pack(pady=10)
        self.username_entry.place(relx=0.7, rely=0.2, anchor="center")
        self.username_entry.insert(0, "")

        # Create a new entry for password on canvas
        password_label = tk.Label(
            self.add_login_from_admincanvas,
            text="Password",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        password_label.pack(pady=10)
        password_label.place(relx=0.3, rely=0.3, anchor="center")
        self.password_entry = tk.Entry(
            self.add_login_from_admincanvas, show="*", font=("Helvetica", 12)
        )
        self.password_entry.pack(pady=10)
        self.password_entry.place(relx=0.7, rely=0.3, anchor="center")
        self.password_entry.insert(0, "")

        # Create a new checkbox for role with options- manager, employee on canvas
        role_label = tk.Label(
            self.add_login_from_admincanvas,
            text="Role",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        role_label.pack(pady=10)
        role_label.place(relx=0.3, rely=0.4, anchor="center")
        self.role_entry = ttk.Combobox(
            self.add_login_from_admincanvas, font=("Helvetica", 12), state="readonly"
        )
        self.role_entry["values"] = ("None","HR","manager", "employee")
        self.role_entry.current(0)
        self.role_entry.pack(pady=10)
        self.role_entry.place(relx=0.7, rely=0.4, anchor="center")

        # Create an entry for new salary and designation
        self.new_salary_label = tk.Label(
            self.add_login_from_admincanvas,
            text="New Salary",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        self.new_salary_label.pack(pady=10)
        self.new_salary_label.place(relx=0.3, rely=0.5, anchor="center")
        self.new_salary_label = tk.Entry(
            self.add_login_from_admincanvas, font=("Helvetica", 12)
        )
        self.new_salary_label.pack(pady=10)
        self.new_salary_label.place(relx=0.7, rely=0.5, anchor="center")
        self.new_salary_label.insert(0, "")

        self.new_designation_label = tk.Label(
            self.add_login_from_admincanvas,
            text="New Designation",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        self.new_designation_label.pack(pady=10)
        self.new_designation_label.place(relx=0.3, rely=0.6, anchor="center")
        self.new_designation_label = tk.Entry(
            self.add_login_from_admincanvas, font=("Helvetica", 12)
        )
        self.new_designation_label.pack(pady=10)
        self.new_designation_label.place(relx=0.7, rely=0.6, anchor="center")
        self.new_designation_label.insert(0, "")

        # Create a new button for adding the new login on canvas
        add_button = tk.Button(
            self.add_login_from_admincanvas,
            text="Add",
            command=lambda: self.add_login_to_database_admin_window(add_login_from_admin_window),
            font=("Helvetica", 14),
        )
        add_button.pack(pady=20)
        add_button.place(relx=0.5, rely=0.8, anchor="center", width=100, height=30)

        # Bind the Enter key to the submit button
        add_login_from_admin_window.bind(
            "<Return>", lambda event: self.add_login_to_database_admin_window(add_login_from_admin_window)
        )

        # Bind the Escape key to the exit function
        add_login_from_admin_window.bind(
            "<Escape>", lambda event: add_login_from_admin_window.destroy()
        )
        # Run the main loop for the add_login_from_admin_window
        add_login_from_admin_window.mainloop()

    def add_login_to_database_admin_window(self, add_login_from_admin_window):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_entry.get()
        salary = self.new_salary_label.get()
        designation = self.new_designation_label.get()

        if role == "None" or username == "" or password == "" or salary == "" or designation == "":
            messagebox.showinfo(
                "Add Login", "Please fill in all the fields."
            )
        elif role == "HR":
            hr_ref = db.reference("/HR")
            if hr_ref.child(username).get():
                messagebox.showinfo(
                    "Add Login", "Username already exists. Choose a different username."
                )
            else:
                hr_ref.child(username).set(
                    {
                        "password": password,
                        "role": role,
                        "designation": designation,
                        "salary": salary,
                    }
                )
                messagebox.showinfo(
                    "Add Login", "HR login added successfully!"
                )
        elif role == "manager":
            manager_ref = db.reference("/manager")
            if manager_ref.child(username).get():
                messagebox.showinfo(
                    "Add Login", "Username already exists. Choose a different username."
                )
            else:
                manager_ref.child(username).set(
                    {
                        "password": password,
                        "role": role,
                        "designation": designation,
                        "salary": salary,
                    }
                )
                messagebox.showinfo(
                    "Add Login", "Manager login added successfully!"
                )
        elif role == "employee":
            employee_ref = db.reference("/employee")
            if employee_ref.child(username).get():
                messagebox.showinfo(
                    "Add Login", "Username already exists. Choose a different username."
                )
            else:
                employee_ref.child(username).set(
                    {
                        "password": password,
                        "role": role,
                        "designation": designation,
                        "salary": salary,
                    }
                )
                messagebox.showinfo(
                    "Add Login", "Employee login added successfully!"
                )

        add_login_from_admin_window.destroy()
        
    def remove_login(self):
        # Check if a row is selected in the Treeview
        if self.treeview.selection():
            # Get the selected row
            selected_row = self.treeview.selection()[0]
            # Get the username from the selected row
            username = self.treeview.item(selected_row)["values"][0]
            #Ask for confirmation before removing the login
            confirmation = messagebox.askyesno(
                "Remove Login", f"Are you sure you want to remove the login for {username}?"
            )
            if confirmation:
                role = self.role_entry_emp_mng.get()
                if role == "HR":
                    hr_ref = db.reference("/HR")
                    hr_ref.child(username).delete()
                elif role == "manager":
                    manager_ref = db.reference("/manager")
                    manager_ref.child(username).delete()
                elif role == "employee":
                    employee_ref = db.reference("/employee")
                    employee_ref.child(username).delete()
                # Remove the selected row from the Treeview
                self.treeview.delete(selected_row)
                # Show a success message
                messagebox.showinfo("Remove Login", "Login removed successfully!")
        else:
            # Show an error message if no row is selected
            messagebox.showerror("Remove Login", "Please select a login to remove.")
        self.create_remove_hr_window.focus_force()
            
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
        
    def approve_resignation(self):
        # Create a new window
        self.approve_resignation_window = tk.Toplevel()
        self.approve_resignation_window.geometry("800x600")
        self.approve_resignation_window.title("Approve Resignation")
        
        # Create a canvas that resizes with the window
        self.approve_resignation_canvas = tk.Canvas(self.approve_resignation_window, bg="white", highlightthickness=0)
        self.approve_resignation_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Import the image as the background on the canvas
        self.load_image_approve_resignation()
        
        # Bind window resize event to function
        self.approve_resignation_window.bind("<Configure>", lambda event: self.on_window_resize_approve_resignation(event))\
            
        # Center the window with function center_window_test
        self.center_window_all(self.approve_resignation_window)
        
        # Create a scrollable frame
        self.scrollable_frame = tk.Frame(self.approve_resignation_window)
        self.scrollable_frame.pack(fill="both", expand=True)
        self.scrollable_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Create a Treeview widget
        self.treeview = ttk.Treeview(
            self.scrollable_frame, columns=("Employee", "Role","Reason"), show="headings", selectmode="browse")
        self.treeview.heading("Employee", text="Employee")
        self.treeview.heading("Role", text="Role")
        self.treeview.heading("Reason", text="Reason")
        self.treeview.column("Employee", width=200, anchor="center")
        self.treeview.column("Role", width=100, anchor="center")
        self.treeview.column("Reason", width=400, anchor="center")
        self.treeview.tag_configure("clickable", foreground="blue", font=("Helvetica", 12, "underline"))
        # Set the treeview rows to be selectable when clicked once
        self.treeview.bind("<Button-1>", lambda event: self.treeview.focus_set())
        
        # Add a vertical scrollbar to the Treeview
        scrollbar = ttk.Scrollbar(self.scrollable_frame, orient="vertical", command=self.treeview.yview)
        scrollbar.pack(side="right", fill="y")
        
        self.treeview.configure(yscrollcommand=scrollbar.set)
        
        #Create a horizontal scrollbar
        horizontal_scrollbar = ttk.Scrollbar(self.scrollable_frame, orient="horizontal", command=self.treeview.xview)
        horizontal_scrollbar.pack(side="bottom", fill="x")
        
        self.treeview.configure(xscrollcommand=horizontal_scrollbar.set)
        
        # Pack the Treeview to the scrollable frame
        self.treeview.pack(fill="both", expand=True)
            
        # Configure grid row and column weights
        self.scrollable_frame.grid_rowconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # Now you can safely use self.treeview
        self.treeview.delete(*self.treeview.get_children())
        
        # Populate the Treeview with employee names
        self.populate_hr_resignation_list()
        
        # Create a new button for approving the resignation
        approve_button = tk.Button(
            self.approve_resignation_canvas, text="Approve Resignation", command=lambda:self.approve_resignation_selected(), font=("Helvetica", 14)
        )
        approve_button.pack(pady=20)
        approve_button.place(relx=0.5, rely=0.9, anchor="center", width=200, height=30)
        
        # Enable the approve button only if a row is selected in the Treeview
        self.treeview.bind("<<TreeviewSelect>>", lambda event: approve_button.config(state="normal"))
        
        # Bind the Escape key to the exit function
        #self.approve_resignation_window.bind("<Escape>", lambda event: self.approve_resignation_window.destroy())
        
        # Run the main loop for the approve_resignation_window
        self.approve_resignation_window.mainloop()
        
    def load_image_approve_resignation(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_approve_resignation_image = Image.open(img_path)
        self.resize_canvas_and_image_approve_resignation()
        
    def resize_canvas_and_image_approve_resignation(self):
        # Get the approve_resignation window size
        window_width = self.approve_resignation_canvas.winfo_width()
        window_height = self.approve_resignation_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.approve_resignation_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_approve_resignation_image.resize(
            (window_width, window_height)
        )
        self.approve_resignation_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.approve_resignation_canvas.delete("all")
        self.approve_resignation_canvas.create_image(
            0, 0, image=self.approve_resignation_image, anchor="nw"
        )
        
    def on_window_resize_approve_resignation(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_approve_resignation()
        
    def populate_hr_resignation_list(self):
        # Clear the existing items in the Treeview
        self.treeview.delete(*self.treeview.get_children())
            
        # Get the list of employees who have resigned
        hr_ref = db.reference("/HR")
        #Get the keys of the all the HR
        hr_list = list(hr_ref.get().keys())
        print(hr_list)
        
        for hr in hr_list:
            #print(db.reference("/HR").child(hr).get())
            if db.reference("/HR").child(hr).child("resignation_request").child("resignation_status").get()=="pending":
                reason=db.reference("/HR").child(hr).child("resignation_request").child("resignation_reason").get()
                self.treeview.insert("", "end", values=(hr, "HR", reason), tags=("clickable",))
                
    def approve_resignation_selected(self):
        # Check if a row is selected in the Treeview
        if self.treeview.selection():
            # Get the selected row
            selected_row = self.treeview.selection()[0]
            # Get the username from the selected row
            username = self.treeview.item(selected_row)["values"][0]
            # Get the role from the selected row
            role = self.treeview.item(selected_row)["values"][1]
            # Get the reason from the selected row
            reason = self.treeview.item(selected_row)["values"][2]
            # Ask for confirmation before approving the resignation
            confirmation = messagebox.askyesno(
                "Approve Resignation", f"Are you sure you want to approve the resignation for {username}?"
            )
            if confirmation:
                if role == "HR":
                    hr_ref = db.reference("/HR")
                    hr_ref.child(username).child("resignation_request").update({"resignation_status": "Approved by Admin"})
                    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    new_date = datetime.datetime.now() + datetime.timedelta(weeks=4)
                    current_date = new_date.strftime('%Y-%m-%d')
                    hr_ref.child(username).child("resignation_request").child("resignation_date").set(current_date)
                    
                # Remove the selected row from the Treeview
                self.treeview.delete(selected_row)
                # Show a success message
                messagebox.showinfo("Approve Resignation", "Resignation approved successfully!")
        else:
            # Show an error message if no row is selected
            messagebox.showerror("Approve Resignation", "Please select a resignation to approve.")
        self.approve_resignation_window.focus_force()
        
    def login_as_selected_role(self,username,admin_window):
        role = self.role_entry.get()
        admin_window.destroy()
        if role == "HR":
            # Create an instance of HR_class
            hr_instance = HR_class()
            # Call the open_hr_window method on the instance
            hr_instance.open_hr_window(role, username,"admin")
        elif role == "manager":
            manager_instance = Manager_class()
            manager_instance.open_manager_window(role, username,"admin")
        elif role == "employee":
            employee_instance = Employee_class()
            employee_instance.open_employee_window(role, username,"admin")
            
    def load_image_admin(self, username):
        try:
            # Construct the full path to the image file based on role and username
            img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

            # Load image and adjust canvas size
            self.original_admin_logo_image = Image.open(img_path)
            self.resize_canvas_and_image_admin(username)
        except Exception as e:
            print(f"Error loading admin image: {e}")
        
    def resize_canvas_and_image_admin(self,username):
        # Get the admin window size
        window_width = self.admin_logo_canvas.winfo_width()
        window_height = self.admin_logo_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.admin_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_admin_logo_image.resize(
            (window_width, window_height)
        )
        self.admin_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.admin_logo_canvas.delete("all")
        self.admin_logo_canvas.create_image(
            0, 0, image=self.admin_logo_image, anchor="nw"
        )

        # Add text to the top center of the canvas
        text_content = f"Hello, {username}"
        text_position = (window_width // 2, 20)  # Top center of the canvas
        self.admin_logo_canvas.create_text(text_position, text=text_content, anchor="center")
        self.admin_logo_canvas.itemconfig(self.admin_logo_canvas.find_all()[-1], fill="white")

    def on_window_resize_admin(self,username,role, event=None):
        # Handle window resize event
        self.resize_canvas_and_image_admin(username)

    def add_login_to_database_admin_window(self, add_login_from_admin_window):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_entry.get()
        designation = self.new_designation_label.get()
        salary = self.new_salary_label.get()

        admins_ref = db.reference("/admins")
        hr_ref = db.reference("/HR")
        manager_ref = db.reference("/manager")
        employee_ref = db.reference("/employee")
        emp_id_ref = db.reference("/")
        emp_uni = emp_id_ref.child("emp_id").get()

        if username in list(admins_ref.get().keys()) or username in list(hr_ref.get().keys()) or username in list(manager_ref.get().keys()) or username in list(employee_ref.get().keys()):
            messagebox.showinfo(
                "Add Login", "Username already exists. Choose a different username."
            )
        elif username == "" or password == "" or role == "None" or designation == "" or salary == "":
            messagebox.showinfo("Add HR Login", "Please fill in all the fields.")
        elif not salary.isdigit():
            messagebox.showinfo("Add HR Login", "Salary should be a number.")
        else:
            # Add the new login to the database
            if role == "HR":
                hr_ref.child(username).set(
                    {
                        "password": password,
                        "role": role,
                        "designation": designation,
                        "salary": int(salary),
                        "emp_id": emp_uni + 1,
                    }
                )
                emp_id_ref.child("emp_id").set(emp_uni + 1)
            elif role == "manager":
                manager_ref.child(username).set(
                    {
                        "password": password,
                        "role": role,
                        "designnation: ": designation,
                        "salary": int(salary),
                        "emp_id": emp_uni + 1,
                    }
                )
                emp_id_ref.child("emp_id").set(emp_uni + 1)
            elif role == "employee":
                employee_ref.child(username).set(
                    {
                        "password": password,
                        "role": role,
                        "designation": designation,
                        "emp_id": emp_uni + 1,
                        "salary": int(salary),
                        "sick_days": 0,
                        "vacation_days": 0,
                        "bonus": 0,
                        "hours_attended": 0,
                        "apply_for_vacation": 0,
                        "survey": db.reference("survey_uni").child("available").get(),
                        "vacation_reason": "",
                        "vacation_approved": 0,
                        "sick_approved": 0,
                        "sick_reason": "",
                        "vacation_approved_denied": "",
                        "sick_approved_denied": "",
                        
                    }
                )
                emp_id_ref.child("emp_id").set(emp_uni + 1)
            messagebox.showinfo("Add Login", "Login added successfully.")
            
        # Close the window and focus on the salary management window
        add_login_from_admin_window.destroy()
        self.create_remove_hr_window.focus_force()
             
    def center_window_all(self, window):
        # Get the width and height of the screen
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Calculate the x and y coordinates to center the main window
        x = (screen_width / 2) - (900 / 2)
        y = (screen_height / 2) - (600 / 2)

        # Set the dimensions of the screen and where it is placed
        window.geometry("%dx%d+%d+%d" % (900, 600, x, y))

    def profile(self,username,role):
        # Create a new Toplevel window for the profile
        profile_dialog = tk.Toplevel()
        profile_dialog.title("Profile")
        profile_dialog.geometry("800x600")
        
        # Create a canvas that resizes with the window
        self.profile_canvas = tk.Canvas(profile_dialog, bg="white", highlightthickness=0)
        self.profile_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Import the image as the background on the canvas
        self.load_image_profile(username,role)
        
        # Bind window resize event to function
        profile_dialog.bind("<Configure>", lambda event: self.on_window_resize_profile(username,role, event))
        
        # Create an exit button in canvas and place at middle of screen
        exit_button = tk.Button(
            self.profile_canvas,
            text="Exit",
            command=profile_dialog.destroy,
            font=("Helvetica", 14),
            width=15,
            height=2,
            bd=0,
            fg="white",
            bg="#FF4500",
            activebackground="#FF6347",
        )
        exit_button.place(relx=0.5, rely=1.0, anchor="s")
        
        # Focus on window
        profile_dialog.focus_force()
        
        # Center the window with function center_window_test
        self.center_window_all(profile_dialog)
        
        # Bind the Escape key to the exit function
        profile_dialog.bind("<Escape>", lambda event: profile_dialog.destroy())
        
        # Run the main loop for the profile window
        profile_dialog.mainloop()
        
    def load_image_profile(self,username,role):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_profile_image = Image.open(img_path)
        self.resize_canvas_and_image_profile(username,role)
        
    def resize_canvas_and_image_profile(self,username,role, event=None):
        # Get the profile window size
        window_width = self.profile_canvas.winfo_width()
        window_height = self.profile_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.profile_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_profile_image.resize((window_width, window_height))
        self.profile_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.profile_canvas.delete("all")
        self.profile_canvas.create_image(0, 0, image=self.profile_image, anchor="nw")

        list=self.getdata(username,role)
        text1=f"EID: {list[0]}\nName: {username}\nRole: {role}\nDesignation: {list[1]}\nSalary: {list[2]}\nHours Attended: {list[3]}"
        self.profile_canvas.create_text(
            10,  # X-coordinate (left)
            self.profile_canvas.winfo_height() - 10,  # Y-coordinate (bottom)
            font=("Helvetica", 15, "bold"),
            text=text1,
            fill="white",
            anchor="sw"  # Anchor to bottom left
        )
        
    def on_window_resize_profile(self,username,role, event=None):
        self.resize_canvas_and_image_profile(username,role)

    def logout(self,admin_window):
        #Close all windows
        admin_window.destroy()
        messagebox.showinfo("Logout", "You have been logged out successfully!")
        Main(True)

    def getdata(self,username,role):
        admin_ref = db.reference("/admins")
        list=[]
        list.append(admin_ref.child(username).child("emp_id").get())
        list.append(admin_ref.child(username).child("designation").get())
        list.append(admin_ref.child(username).child("salary").get())
        list.append(admin_ref.child(username).child("hours_attended").get())

        return list
        
def main(role, username):
    admin = Admin_class()
    admin.open_admin_window(role, username)