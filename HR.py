from datetime import timedelta 
import datetime
import tkinter as tk
from tkcalendar import Calendar, DateEntry
from tkinter import END, IntVar, Listbox, Radiobutton, messagebox
from tkinter import simpledialog, ttk,scrolledtext
from tkinter.simpledialog import SimpleDialog
from PIL import Image, ImageTk
import os
import firebase_admin
from firebase_admin import db, credentials
import threading
from tkinter import Label
from tkinter import Tk, Canvas, PhotoImage
from main import main as Main

class HR_class:
    def __init__(self):
        
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("HR Window")
    
    def center_window_all(self, window):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width / 2) - (900 / 2)
        y = (screen_height / 2) - (700 / 2)
        window.geometry("%dx%d+%d+%d" % (900, 700, x, y))

    def center_window_survey(self, window):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width / 2) - (1400 / 2)
        y = (screen_height / 2) - (700 / 2)
        window.geometry("%dx%d+%d+%d" % (1400,700, x, y))
       
    def getdata(self,username,role):
        if role=="admin":
            admin_ref = db.reference("/admins")
            list=[]
            list.append(admin_ref.child(username).child("emp_id").get())
            list.append(admin_ref.child(username).child("designation").get())
            list.append(admin_ref.child(username).child("salary").get())
            list.append(admin_ref.child(username).child("hours_attended").get())
            list.append(admin_ref.child(username).child("bonus").get())
            list.append(admin_ref.child(username).child("sick_days").get())
            list.append(admin_ref.child(username).child("vacation_days").get())
            list.append(admin_ref.child(username).child("survey").child("available").get())

            return list
        if role=="employee":
            emp_ref = db.reference("/employee")
            list=[]
            list.append(emp_ref.child(username).child("emp_id").get())
            list.append(emp_ref.child(username).child("designation").get())
            list.append(emp_ref.child(username).child("salary").get())
            list.append(emp_ref.child(username).child("hours_attended").get())
            list.append(emp_ref.child(username).child("bonus").get())
            list.append(emp_ref.child(username).child("sick_days").get())
            list.append(emp_ref.child(username).child("vacation_days").get())
            list.append(emp_ref.child(username).child("survey").child("available").get())
            
            return list
        elif role=="manager":
            manager_ref = db.reference("/manager")
            list=[]
            list.append(manager_ref.child(username).child("emp_id").get())
            list.append(manager_ref.child(username).child("designation").get())
            list.append(manager_ref.child(username).child("salary").get())
            list.append(manager_ref.child(username).child("hours_attended").get())
            list.append(manager_ref.child(username).child("bonus").get())
            list.append(manager_ref.child(username).child("sick_days").get())
            list.append(manager_ref.child(username).child("vacation_days").get())
            
            return list
        elif role=="HR":
            hr_ref = db.reference("/HR")
            list=[]
            list.append(hr_ref.child(username).child("emp_id").get())
            list.append(hr_ref.child(username).child("designation").get())
            list.append(hr_ref.child(username).child("salary").get())
            list.append(hr_ref.child(username).child("hours_attended").get())
            list.append(hr_ref.child(username).child("bonus").get())
            list.append(hr_ref.child(username).child("sick_days").get())
            list.append(hr_ref.child(username).child("vacation_days").get())
            
            return list
    
    def open_hr_window(self,role, username,uni_role):
        self.uni_role = uni_role
        # self.root.destroy()  # Close the main login window
        if hasattr(self, "root"):
            try:
                if self.root.winfo_exists():
                    self.root.destroy()  # Close the main login window
            except:
                pass

        # Create a new window
        hr_window = tk.Tk()  # Use Tk() to create a new window
        hr_window.geometry("800x600")  # Set the window size
        hr_window.title("HR Window")
        self.treeview = None
        self.selected_values = {}
        self.current_question_index = 0
        self.buttons_created_down = False
        self.buttons_created = False
        self.questions = [f"Question {i+1}" for i in range(22)]  # Assuming there are 10 questions
        self.answers = {}

        # Create a canvas that resizes with the window
        self.hr_logo_canvas = tk.Canvas(hr_window, bg="white", highlightthickness=0)
        self.hr_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # Import the image as the background on the canvas
        self.load_image_hr(username)

        # Bind window resize event to function
        hr_window.bind("<Configure>", lambda event: self.on_window_resize_hr(event, username))

        # Focus on window
        hr_window.focus_force()

        # Center the window with function center_window_all
        self.center_window_all(hr_window)

        # Bind the Escape key to the exit function
        hr_window.bind("<Escape>", lambda event: hr_window.destroy())

        # Buttons of HR window
        button_width = 300
        button_height = 50  # Increased height for bigger buttons

        self.salary_management_button = tk.Button(
            self.hr_logo_canvas, text="Employee Management", command=lambda: self.salary_management(), font=("Helvetica", 14)
        )
        self.salary_management_button.place(
            relx=0.1, rely=0.2, anchor="w", width=button_width, height=button_height
        )

        self.approve_bonus_button = tk.Button(
            self.hr_logo_canvas, text="Approve Bonus", command=lambda: self.approve_bonus(), font=("Helvetica", 14)
        )
        self.approve_bonus_button.place(
            relx=0.9, rely=0.2, anchor="e", width=button_width, height=button_height
        )

        self.approve_resignation_button = tk.Button(
            self.hr_logo_canvas, text="Approve Resignation", command=lambda: self.approve_resignation(), font=("Helvetica", 14)
        )
        self.approve_resignation_button.place(
            relx=0.1, rely=0.35, anchor="w", width=button_width, height=button_height
        )

        self.check_hours_attended_button = tk.Button(
            self.hr_logo_canvas, text="Check Employee Hours Attended", command=lambda: self.check_hours_attended(), font=("Helvetica", 14)
        )
        self.check_hours_attended_button.place(
            relx=0.9, rely=0.35, anchor="e", width=button_width, height=button_height
        )

        self.survey_feedback_button = tk.Button(
            self.hr_logo_canvas, text="Create Survey", command=lambda: self.survey_feedback(username), font=("Helvetica", 14)
        )
        self.survey_feedback_button.place(
            relx=0.1, rely=0.5, anchor="w", width=button_width, height=button_height
        )

        self.approve_promotion_button = tk.Button(
            self.hr_logo_canvas, text="Approve Promotion", command=lambda: self.approve_promotion(), font=("Helvetica", 14)
        )
        self.approve_promotion_button.place(
            relx=0.9, rely=0.5, anchor="e", width=button_width, height=button_height
        )

        self.apply_for_resignation_button = tk.Button(
            self.hr_logo_canvas, text="Apply for Resignation", command=lambda: self.apply_for_resignation(username), font=("Helvetica", 14)
        )
        self.apply_for_resignation_button.place(
            relx=0.1, rely=0.65, anchor="w", width=button_width, height=button_height
        )

        self.approve_review_button = tk.Button(
            self.hr_logo_canvas, text="Approve Review", command=lambda: self.approve_review(), font=("Helvetica", 14)
        )
        self.approve_review_button.place(
            relx=0.9, rely=0.65, anchor="e", width=button_width, height=button_height
        )

        self.review_complaints_button = tk.Button( 
            self.hr_logo_canvas, text="Review Complaints", command=lambda: self.review_complaints(), font=("Helvetica", 14)
        )
        self.review_complaints_button.place(
            relx=0.1, rely=0.8, anchor="w", width=button_width, height=button_height
        )

        self.view_survey_results_button = tk.Button(
            self.hr_logo_canvas, text="View Survey Results", command=lambda: self.view_survey_results(), font=("Helvetica", 14)
        )

        self.view_survey_results_button.place(
            relx=0.9, rely=0.8, anchor="e", width=button_width, height=button_height
        )

        profile_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "profile.png")
        profile_image = Image.open(profile_path)
        profile_image = profile_image.resize((50, 50))
        profile_image = ImageTk.PhotoImage(profile_image)
        profile_button = tk.Button(
            self.hr_logo_canvas,
            image=profile_image,
            command=lambda: self.profile(username,role),
            bd=0,
            bg="white",
            activebackground="white",
        )
        profile_button.image = profile_image
        profile_button.pack()
        profile_button.place(relx=0.95, rely=0.05, anchor="ne")

        # Logout button
        logout_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "logout.png")
        logout_image = Image.open(logout_path)
        logout_image = logout_image.resize((50, 50))
        logout_image = ImageTk.PhotoImage(logout_image)
        logout_button = tk.Button(
            self.hr_logo_canvas,
            image=logout_image,
            command=lambda: self.logout(hr_window),
            bd=0,
            bg="white",
            activebackground="white",
        )
        logout_button.image = logout_image
        logout_button.place(relx=0.95, rely=0.95, anchor="se")

        # Check resignation request status and show relevant message
        resignation_status = db.reference("/HR").child(username).child("resignation_request").child("resignation_status").get()
        if resignation_status == "Approved by Admin":
            resignation_date = db.reference("/HR").child(username).child("resignation_request").child("resignation_date").get()
            message_text = f"Resignation request has been approved by Admin.\nYou will be logged out on {resignation_date}"
            messagebox.showinfo("Resignation Request", message_text)
            if datetime.datetime.now().date() >= datetime.datetime.strptime(resignation_date, "%Y-%m-%d").date():
                messagebox.showinfo("Resignation Request", "You have been logged out as per your resignation request and cannot login again.")
                hr_window.destroy()
                return

        # Run the main loop for the HR window
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
            window_height / 10,
            text=f"Welcome {username_hr}!",
            font=("Helvetica", 28, "bold"),
            fill="white",
        )

    def on_window_resize_hr(self, event,username):
        # Handle window resize event
        self.resize_canvas_and_image_hr(username)

    def salary_management(self):
        #create a frame with clickable text
        salary_management_frame = tk.Toplevel()
        salary_management_frame.geometry("800x600")  # Set the window size
        salary_management_frame.title("Salary Management")
        
        # create a canvas that resizes with the window
        self.salary_management_canvas = tk.Canvas(salary_management_frame, bg="white", highlightthickness=0)
        self.salary_management_canvas.pack(fill=tk.BOTH, expand=True)
        
        # bind window resize event to function
        salary_management_frame.bind("<Configure>", lambda event: self.on_window_resize_salary_management(event))
        
        self.treeview = None
        
        # import the image as the background on the canvas
        self.load_image_salary_management()
        
        # create a scrollable frame
        self.scrollable_frame = tk.Frame(self.salary_management_canvas, bg="white")
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True)
        self.scrollable_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # create a treeview to display the employees
        if self.treeview is None:
            self.treeview = ttk.Treeview(
                self.scrollable_frame, columns=("Employee",), show="headings", selectmode="browse"
            )
            self.treeview.heading("Employee", text="Employee")
            self.treeview.column("Employee", width=200, anchor="center")
            self.treeview.tag_configure("clickable", foreground="blue", font=("Helvetica", 12, "underline"))
            self.treeview.bind("<Double-1>", lambda event: self.open_employee_details_window(self.treeview.item(self.treeview.selection())["values"][0]))
            #Call the enable_buttons function when a row is selected
            self.treeview.bind("<<TreeviewSelect>>", lambda event: self.enable_buttons())

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
            self.salary_management_canvas,
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
            self.salary_management_canvas, font=("Helvetica", 12, "bold")
        )
        self.role_entry_emp_mng["values"] = ("None","HR", "manager", "employee")
        self.role_entry_emp_mng.pack(
            pady=20
        )
        self.role_entry_emp_mng.place(relx=0.5, rely=0.2, anchor="center")
        self.role_entry_emp_mng.current(0)
        
        self.role_entry_emp_mng.bind("<<ComboboxSelected>>", self.role_selected)
        
        #Create a add login button to add the login of the employee
        add_login_button = tk.Button(
            self.salary_management_canvas,
            text="Add Login",
            command=lambda:self.add_login_from_hr_window(),
            font=("Helvetica", 14),
            width=15,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        add_login_button.place(relx=0.35, rely=0.9, anchor="s")
        #center the window
        self.center_window_all(salary_management_frame)
        
        try:
            #Create a remove login button to remove the login of the employee
            self.remove_login_button_new = tk.Button(
                self.salary_management_canvas,
                text="Remove Login",
                command=lambda:self.remove_login(salary_management_frame),
                font=("Helvetica", 14),
                width=15,
                height=2,
                bd=0,
                fg="white",
                bg="black",
                activebackground="black",
                state="disabled",
            )
            self.remove_login_button_new.place(relx=0.65, rely=0.9, anchor="s")
        #Display an error message saying to select a row
        except:
            print("Error")
            messagebox.showinfo("Error","Please select a row")
        
        #focus on window
        salary_management_frame.focus_force()
        
        #bind the escape key to the exit function
        salary_management_frame.bind("<Escape>", lambda event: salary_management_frame.destroy())
        
        # Run the main loop for the salary_management_frame
        salary_management_frame.mainloop()

    def enable_buttons(self):
        # Enable the remove login button if the role is not HR
        if hasattr(self, "remove_login_button_new") and self.remove_login_button_new is not None:
            print("Role:", self.role_entry_emp_mng)  # Debug print statement
            if self.role_entry_emp_mng.get() != "HR":  # Assuming role_entry_emp_mng is a tkinter StringVar
                self.remove_login_button_new.config(state="normal")
            else:
                self.remove_login_button_new.config(state="disabled")
            
    def role_selected(self, event):
        self.remove_login_button_new.config(state="disabled")
        if self.role_entry_emp_mng is not None:
            selected_role = self.role_entry_emp_mng.get()
            if selected_role:
                self.populate_employee_list(selected_role)
        else:
            print("Role entry is None")

    def populate_employee_list(self, role):
        self.remove_login_button_new.config(state="disabled")
        # Clear the existing items in the Treeview
        if self.treeview is not None:
            self.treeview.delete(*self.treeview.get_children())
        
        if role == "HR":
            employees = list(( db.reference("/HR").get()).keys())
            self.role_details = "HR"
        elif role == "manager":
            employees = list(( db.reference("/manager").get()).keys())
            self.role_details = "manager"
        elif role == "None":
            return
        else:
            employees = list(( db.reference("/employee").get()).keys())
            self.role_details = "employee"

        # Populate the Treeview with employee names
        for employee in employees:
            self.treeview.insert("", "end", values=(employee,), tags=("clickable",))

    def open_employee_details_window(self, employee_name):
        #Function to open another window with employee details
        employee_details_window = tk.Toplevel()
        employee_details_window.geometry("400x300")
        employee_details_window.title(f"Details for {employee_name}")
        employee_details_window.focus_force()
        
        #create a canvas that resizes with the window
        self.employee_details_canvas = tk.Canvas(employee_details_window, bg="white", highlightthickness=0)
        self.employee_details_canvas.pack(fill=tk.BOTH, expand=True)
        
        self.load_image_employee_details_new(employee_name)
        
        # bind window resize event to function
        employee_details_window.bind("<Configure>", lambda event: self.on_window_resize_employee_details_new(employee_name,event))
        
        #create a button to edit salary
        edit_salary_button = tk.Button(
            self.employee_details_canvas,
            text="Edit Salary",
            command=lambda:self.edit_salary(employee_name),
            font=("Helvetica", 14),
            width=15,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        edit_salary_button.place(relx=0.5, rely=0.9, anchor="s")
                
        #create an exit button in canvas and place at bottom middle
        exit_button = tk.Button(
        self.employee_details_canvas,
        text="Exit",
        command=employee_details_window.destroy,
        font=("Helvetica", 14),
        width=15,
        height=2,
        bd=0,
        fg="white",
        bg="#FF4500",
        activebackground="#FF6347",
    )
        exit_button.place(relx=0.5, rely=1.0, anchor="s")
        
        # Center the window with function center_window_test
        self.center_window_all(employee_details_window)
        
        # Bind the Escape key to the exit function
        employee_details_window.bind("<Escape>", lambda event: self.handle_employee_details_window_exit(event, employee_details_window))
        
        # Run the main loop for the employee details window
        employee_details_window.mainloop()
        
    def load_image_add_login_from_hr(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_add_login_from_hr_image = Image.open(img_path)
        self.resize_canvas_and_image_add_login_from_hr()

    def resize_canvas_and_image_add_login_from_hr(self):
        # Get the create_hr window size
        window_width = self.add_login_from_hr_canvas.winfo_width()
        window_height = self.add_login_from_hr_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.add_login_from_hr_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_add_login_from_hr_image.resize(
            (window_width, window_height)
        )
        self.add_login_from_hr_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.add_login_from_hr_canvas.delete("all")
        self.add_login_from_hr_canvas.create_image(
            0, 0, image=self.add_login_from_hr_image, anchor="nw"
        )

    def on_window_resize_add_login_from_hr(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_add_login_from_hr()
        
    def add_login_from_hr_window(self):
        # Create a new window
        add_login_from_hr_window = tk.Toplevel()
        add_login_from_hr_window.geometry("800x600")  # Set the window size
        add_login_from_hr_window.title("Add Login")

        # Create a canvas that resizes with the window
        self.add_login_from_hr_canvas = tk.Canvas(add_login_from_hr_window, bg="white", highlightthickness=0)
        self.add_login_from_hr_canvas.pack(fill=tk.BOTH, expand=True)

        # Import the image as the background on the canvas
        self.load_image_add_login_from_hr()

        # Bind window resize event to function
        add_login_from_hr_window.bind("<Configure>", lambda event: self.on_window_resize_add_login_from_hr(event))

        # focus on window
        add_login_from_hr_window.focus_force()
        # Center the window with function center_window_test
        self.center_window_all(add_login_from_hr_window)

        # Create a new entry for username on canvas
        username_label = tk.Label(
            self.add_login_from_hr_canvas,
            text="Username",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        username_label.pack(pady=10)
        username_label.place(relx=0.3, rely=0.2, anchor="center")
        self.username_entry = tk.Entry(
            self.add_login_from_hr_canvas, font=("Helvetica", 12)
        )
        self.username_entry.pack(pady=10)
        self.username_entry.place(relx=0.7, rely=0.2, anchor="center")
        self.username_entry.insert(0, "")

        # Create a new entry for password on canvas
        password_label = tk.Label(
            self.add_login_from_hr_canvas,
            text="Password",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        password_label.pack(pady=10)
        password_label.place(relx=0.3, rely=0.3, anchor="center")
        self.password_entry = tk.Entry(
            self.add_login_from_hr_canvas, show="*", font=("Helvetica", 12)
        )
        self.password_entry.pack(pady=10)
        self.password_entry.place(relx=0.7, rely=0.3, anchor="center")
        self.password_entry.insert(0, "")

        # Create a new checkbox for role with options- manager, employee on canvas
        role_label = tk.Label(
            self.add_login_from_hr_canvas,
            text="Role",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        role_label.pack(pady=10)
        role_label.place(relx=0.3, rely=0.4, anchor="center")
        self.role_entry = ttk.Combobox(
            self.add_login_from_hr_canvas, font=("Helvetica", 12), state="readonly"
        )
        self.role_entry["values"] = ("manager", "employee")
        self.role_entry.current(0)
        self.role_entry.pack(pady=10)
        self.role_entry.place(relx=0.7, rely=0.4, anchor="center")

        # Create an entry for new salary and designation
        self.new_salary_label = tk.Label(
            self.add_login_from_hr_canvas,
            text="New Salary",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        self.new_salary_label.pack(pady=10)
        self.new_salary_label.place(relx=0.3, rely=0.5, anchor="center")
        self.new_salary_label = tk.Entry(
            self.add_login_from_hr_canvas, font=("Helvetica", 12)
        )
        self.new_salary_label.pack(pady=10)
        self.new_salary_label.place(relx=0.7, rely=0.5, anchor="center")
        self.new_salary_label.insert(0, "")

        self.new_designation_label = tk.Label(
            self.add_login_from_hr_canvas,
            text="New Designation",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        self.new_designation_label.pack(pady=10)
        self.new_designation_label.place(relx=0.3, rely=0.6, anchor="center")
        self.new_designation_label = tk.Entry(
            self.add_login_from_hr_canvas, font=("Helvetica", 12)
        )
        self.new_designation_label.pack(pady=10)
        self.new_designation_label.place(relx=0.7, rely=0.6, anchor="center")
        self.new_designation_label.insert(0, "")

        # Create a new button for adding the new login on canvas
        add_button = tk.Button(
            self.add_login_from_hr_canvas,
            text="Add",
            command=lambda: self.add_login_to_database_hr_window(add_login_from_hr_window),
            font=("Helvetica", 14),
        )
        add_button.pack(pady=20)
        add_button.place(relx=0.5, rely=0.8, anchor="center", width=100, height=30)

        # Bind the Enter key to the submit button
        add_login_from_hr_window.bind(
            "<Return>", lambda event: self.add_login_to_database_hr_window(add_login_from_hr_window)
        )

        # Bind the Escape key to the exit function
        add_login_from_hr_window.bind(
            "<Escape>", lambda event: add_login_from_hr_window.destroy()
        )
        # Run the main loop for the add_login_from_hr_window
        add_login_from_hr_window.mainloop()

    def add_login_to_database_hr_window(self, add_login_from_hr_window):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
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
                "Add HR Login", "Username already exists. Choose a different username."
            )
        elif username == "" or password == "" or role == "" or designation == "" or salary == "":
            messagebox.showinfo("Add HR Login", "Please fill in all the fields.")
        elif not salary.isdigit():
            messagebox.showinfo("Add HR Login", "Salary should be a number.")
        else:
            # Add the new login to the database
            if role == "manager":
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
            messagebox.showinfo("Add HR Login", "Login added successfully.")
            
        # Close the window and focus on the salary management window
        add_login_from_hr_window.destroy()
        self.salary_management_canvas.focus_force()
            
    def remove_login(self,employee_details_window):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        #Function to remove the login of the employee or manager
        try:
            employee_name = self.treeview.item(self.treeview.selection())["values"][0]
        except:
            messagebox.showinfo("Error","Please select a row")
            return
        if employee_name == None:
            messagebox.showinfo("Error","Please select a row")
            return
        if messagebox.askyesno("Remove Login", f"Are you sure you want to remove the login of {employee_name}?"):
            #Remove the login from the database
            if db.reference("/employee").child(employee_name).get() is not None:
                db.reference("/employee").child(employee_name).delete()
            elif db.reference("/manager").child(employee_name).get() is not None:
                db.reference("/manager").child(employee_name).delete()
            messagebox.showinfo("Remove Login", "Login removed successfully.")
        #Close the window
        employee_details_window.destroy()
        self.salary_management_canvas.focus_force()
        
    def handle_employee_details_window_exit(self, event, employee_details_window):
        if hasattr(self, "salary_management_canvas") and self.salary_management_canvas.winfo_exists():
            self.salary_management_canvas.focus_force()
            
    def edit_salary(self, employee_name):
        #Create a window to edit the salary of the employee
        edit_salary_window = tk.Toplevel()
        edit_salary_window.geometry("300x150")
        edit_salary_window.title(f"Edit Salary for {employee_name}")
        #Center the window according to the screen
        #Do not use the center_window_all function
        edit_salary_window.update_idletasks()
        width = edit_salary_window.winfo_width()
        height = edit_salary_window.winfo_height()
        x = (edit_salary_window.winfo_screenwidth() // 2) - (width // 2)
        y = (edit_salary_window.winfo_screenheight() // 2) - (height // 2)
        edit_salary_window.geometry(f"{width}x{height}+{x}+{y}")
        
        #create an entry for new salary
        new_salary_label = tk.Label(
            edit_salary_window,
            text="New Salary",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        new_salary_label.pack(
            pady=20
        )
        new_salary_label.place(relx=0.5, rely=0.1, anchor="center")
        
        #Create an entry for the new salary
        self.new_salary_entry = tk.Entry(
            edit_salary_window, font=("Helvetica", 12, "bold")
        )
        self.new_salary_entry.pack(
            pady=20
        )
        self.new_salary_entry.place(relx=0.5, rely=0.3, anchor="center")
        self.new_salary_entry.insert(0, "")
        #create a submit button to change the salary
        submit_button = tk.Button(
            edit_salary_window,
            text="Submit",
            command=lambda:self.new_submit_salary(employee_name, edit_salary_window),
            font=("Helvetica", 14),
            width=7,
            height=1,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        submit_button.place(relx=0.5, rely=0.9, anchor="s")
        
        #bind the enter key to the submit button
        edit_salary_window.bind("<Return>", lambda event: self.new_submit_salary(employee_name, edit_salary_window))
        
        #bind the escape key to the exit function
        edit_salary_window.bind("<Escape>", lambda event: edit_salary_window.destroy())
        
        #focus on window
        edit_salary_window.focus_force()
        
        # Run the main loop for the edit_salary_window
        edit_salary_window.mainloop()
        
    def new_submit_salary(self, employee_name, edit_salary_window):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        #Get the new salary from the entry
        new_salary = self.new_salary_entry.get()
        if not new_salary.isdigit():
            messagebox.showinfo("Error", "Salary should be a number.")
            return
        if new_salary == "":
            messagebox.showinfo("Error", "Please enter a salary.")
            return
        if int(new_salary) < 0:
            messagebox.showinfo("Error", "Salary cannot be negative.")
            return
        #Ask for confirmation 
        if messagebox.askyesno("Confirm", f"Are you sure you want to change the salary of {employee_name} to {new_salary}?"):
            #Change the salary in the database
            db.reference("/employee").child(employee_name).child("salary").set(int(new_salary))
            messagebox.showinfo("Success", "Salary changed successfully.")
        #Close the window
        edit_salary_window.destroy()
        #focus on the salary management window
        self.employee_details_canvas.focus_force()

    def load_image_employee_details_new(self,employee_name):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_employee_details_image = Image.open(img_path)
        self.resize_canvas_and_image_employee_details_new(employee_name)
        
    def resize_canvas_and_image_employee_details_new(self,employee_name):
        # Get the employee details window size
        window_width = self.employee_details_canvas.winfo_width()
        window_height = self.employee_details_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.employee_details_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_employee_details_image.resize(
            (window_width, window_height)
        )
        self.employee_details_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.employee_details_canvas.delete("all")
        self.employee_details_canvas.create_image(
            0, 0, image=self.employee_details_image, anchor="nw"
        )
        
        #create text with employee name, role, salary, hours attended, bonus
        if self.role_details == "employee":
            employee_details_text="Employee Name: "+str(employee_name)+"\nRole: "+str(db.reference("/employee").child(employee_name).child("role").get())+"\nSalary: "+str(db.reference("/employee").child(employee_name).child("salary").get())+"\nHours Attended: "+str(db.reference("/employee").child(employee_name).child("hours_attended").get())+"\nBonus: "+str(db.reference("/employee").child(employee_name).child("bonus").get())
            self.employee_details_canvas.create_text(
                window_width / 2,
                window_height / 2,
                text=employee_details_text,
                font=("Helvetica", 14, "bold"),
                fill="white",
                tag="employee_details_text"
            )
        elif self.role_details == "manager":
            employee_details_text="Manager Name: "+str(employee_name)+"\nRole: "+str(db.reference("/manager").child(employee_name).child("role").get())+"\nSalary: "+str(db.reference("/manager").child(employee_name).child("salary").get())+"\nHours Attended: "+str(db.reference("/manager").child(employee_name).child("hours_attended").get())+"\nBonus: "+str(db.reference("/manager").child(employee_name).child("bonus").get())
            self.employee_details_canvas.create_text(
                window_width / 2,
                window_height / 2,
                text=employee_details_text,
                font=("Helvetica", 14, "bold"),
                fill="white",
                tag="employee_details_text"
            )
        elif self.role_details == "HR":
            employee_details_text="HR Name: "+str(employee_name)+"\nRole: "+str(db.reference("/HR").child(employee_name).child("role").get())+"\nSalary: "+str(db.reference("/HR").child(employee_name).child("salary").get())+"\nHours Attended: "+str(db.reference("/HR").child(employee_name).child("hours_attended").get())+"\nBonus: "+str(db.reference("/HR").child(employee_name).child("bonus").get())
            self.employee_details_canvas.create_text(
                window_width / 2,
                window_height / 2,
                text=employee_details_text,
                font=("Helvetica", 14, "bold"),
                fill="white",
                tag="employee_details_text"
            )

    def on_window_resize_employee_details_new(self,employee_name, event):
        # Handle window resize event
        self.resize_canvas_and_image_employee_details_new(employee_name)
        
    def load_image_salary_management(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_salary_management_image = Image.open(img_path)
        self.resize_canvas_and_image_salary_management()

    def resize_canvas_and_image_salary_management(self):
        # Get the salary_management window size
        window_width = self.salary_management_canvas.winfo_width()
        window_height = self.salary_management_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.salary_management_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_salary_management_image.resize(
            (window_width, window_height)
        )
        self.salary_management_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.salary_management_canvas.delete("all")
        self.salary_management_canvas.create_image(
            0, 0, image=self.salary_management_image, anchor="nw"
        )

        # #Add 2 notes saying "Double click on the employee to view details" and "Click on employee in order to remove login" at the bottom of the canvas
        # self.salary_management_canvas.create_text(
        #     window_width / 2,
        #     window_height - 50,
        #     text="*Double click on the employee to view details",
        #     font=("Helvetica", 14, "bold"),
        #     fill="white",
        # )
        # self.salary_management_canvas.create_text(
        #     window_width / 2,
        #     window_height - 30,
        #     text="*Click on employee in order to remove login",
        #     font=("Helvetica", 14, "bold"),
        #     fill="white",
        # )

    def on_window_resize_salary_management(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_salary_management()

    def approve_bonus(self):
        #Create a window to approve the bonus of the employee
        self.approve_bonus_window = tk.Toplevel()
        self.approve_bonus_window.geometry("400x300")
        self.approve_bonus_window.title("Approve Bonus")
        
        #Create a canvas that resizes with the window
        self.approve_bonus_canvas = tk.Canvas(self.approve_bonus_window, bg="white", highlightthickness=0)
        self.approve_bonus_canvas.pack(fill=tk.BOTH, expand=True)
        
        #Load the image as the background on the canvas
        self.load_image_approve_bonus()
        
        #Bind window resize event to function
        self.approve_bonus_window.bind("<Configure>", lambda event: self.on_window_resize_approve_bonus(event))

        #Center the window with function center_window_test
        self.center_window_all(self.approve_bonus_window)
        
        #focus on window
        self.approve_bonus_window.focus_force()
        
        self.treeview_bonus = None
        
        # create a scrollable frame
        self.scrollable_frame_bonus = tk.Frame(self.approve_bonus_canvas, bg="white")
        self.scrollable_frame_bonus.pack(fill=tk.BOTH, expand=True)
        self.scrollable_frame_bonus.place(relx=0.5, rely=0.5, anchor="center")
        
        # create a treeview to display the employees
        if self.treeview_bonus is None:
            self.treeview_bonus = ttk.Treeview(
                self.scrollable_frame_bonus, columns=("Employee",), show="headings", selectmode="browse"
            )
            self.treeview_bonus.heading("Employee", text="Employee")
            #Create columns for name,bonus amount,if role is employee then add a column for reason,hours attended,and 2 buttons for approve and deny
            self.treeview_bonus["columns"] = ("Employee", "Bonus", "Reason", "Hours Attended")
            self.treeview_bonus.column("Employee", width=100, anchor="center")
            self.treeview_bonus.column("Bonus", width=100, anchor="center")
            self.treeview_bonus.column("Reason", width=300, anchor="center")
            self.treeview_bonus.column("Hours Attended", width=100, anchor="center")
            self.treeview_bonus.heading("Employee", text="Employee")
            self.treeview_bonus.heading("Bonus", text="Bonus")
            self.treeview_bonus.heading("Reason", text="Reason")
            self.treeview_bonus.heading("Hours Attended", text="Hours Attended")
            self.treeview_bonus.tag_configure("selectable", foreground="blue", font=("Helvetica", 12, "underline"))
            # self.treeview_bonus.bind("<Double-1>", lambda event: self.open_employee_details_window(self.treeview_bonus.item(self.treeview_bonus.selection())["values"][0]))
            
            # Add a vertical scrollbar to the Treeview
            scrollbar_bonus_y = ttk.Scrollbar(self.scrollable_frame_bonus, orient="vertical", command=self.treeview_bonus.yview)
            scrollbar_bonus_y.pack(side="right", fill="y")
            self.treeview_bonus.configure(yscrollcommand=scrollbar_bonus_y.set)
            
            # Add a horizontal scrollbar to the Treeview
            scrollbar_bonus_x = ttk.Scrollbar(self.scrollable_frame_bonus, orient="horizontal", command=self.treeview_bonus.xview)
            scrollbar_bonus_x.pack(side="bottom", fill="x")
            self.treeview_bonus.configure(xscrollcommand=scrollbar_bonus_x.set)

            # Pack the Treeview to the scrollable frame
            self.treeview_bonus.pack(fill="both", expand=True)

        #Create 2 buttons for approve and deny that are disabled by default and enabled when a row is selected
        self.approve_bonus_button = tk.Button(
            self.approve_bonus_canvas,
            text="Approve Bonus",
            command=lambda:self.approve_bonus_btn(),
            font=("Helvetica", 14),
            width=15,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        self.approve_bonus_button.place(relx=0.3, rely=0.9, anchor="s")
        self.approve_bonus_button["state"] = "disabled"
        
        self.deny_bonus_button = tk.Button(
            self.approve_bonus_canvas,
            text="Deny Bonus",
            command=lambda:self.deny_bonus_btn(),
            font=("Helvetica", 14),
            width=15,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        self.deny_bonus_button.place(relx=0.7, rely=0.9, anchor="s")
        self.deny_bonus_button["state"] = "disabled"
        
        #Create a button named Grant Bonus to grant bonus to the managers
        self.grant_bonus_button = tk.Button(
            self.approve_bonus_canvas,
            text="Grant Bonus",
            command=lambda:self.grant_bonus(),
            font=("Helvetica", 14),
            width=15,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        self.grant_bonus_button.place(relx=0.5, rely=0.9, anchor="s")
        self.grant_bonus_button["state"] = "disabled"
        
        # Configure grid row and column weights
        self.scrollable_frame_bonus.grid_rowconfigure(0, weight=1)
        self.scrollable_frame_bonus.grid_columnconfigure(0, weight=1)

        # Now you can safely use self.treeview
        self.treeview_bonus.delete(*self.treeview_bonus.get_children())
        
        # create a tick box for role of the employee
        role_entry_bonus_label = tk.Label(
            self.approve_bonus_canvas,
            text="Role",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        role_entry_bonus_label.pack(
            pady=20
        )
        # place it Extreme top middle
        role_entry_bonus_label.place(relx=0.5, rely=0.1, anchor="center")
        self.role_entry_bonus = ttk.Combobox(
            self.approve_bonus_canvas, font=("Helvetica", 12, "bold")
        )
        self.role_entry_bonus["values"] = ("Select Role", "manager", "employee")
        self.role_entry_bonus.pack(
            pady=20
        )
        self.role_entry_bonus.place(relx=0.5, rely=0.2, anchor="center")
        self.role_entry_bonus.current(0)
        
        self.role_entry_bonus.bind("<<ComboboxSelected>>", self.role_selected_bonus)
        
        # bind the treeview select event to function
        self.treeview_bonus.bind("<<TreeviewSelect>>",self.on_treeview_select)
        
        #Bind the escape key to the exit function
        self.approve_bonus_window.bind("<Escape>", lambda event: self.approve_bonus_window.destroy())
        
        #Run the main loop for the self.approve_bonus_window
        self.approve_bonus_window.mainloop()
            
    def on_treeview_select(self, event):
        selected_items = self.treeview_bonus.selection()
        if selected_items:
            role= self.role_entry_bonus.get()
            if role == "manager":
                self.approve_bonus_button["state"] = "disabled"
                self.deny_bonus_button["state"] = "disabled"
                self.grant_bonus_button["state"] = "normal"
            else:
                self.approve_bonus_button["state"] = "normal"
                self.deny_bonus_button["state"] = "normal"
                self.grant_bonus_button["state"] = "disabled"
        else:
            # Disable buttons if no row is selected
            self.approve_bonus_button["state"] = "disabled"
            self.deny_bonus_button["state"] = "disabled"
        
    def role_selected_bonus(self, event):
        if self.role_entry_bonus != None:
            selected_role = self.role_entry_bonus.get()
            if selected_role:
                self.populate_employee_list_bonus(selected_role)
        else:
            print("Role entry is None")
            
    def populate_employee_list_bonus(self, role):
        # Clear the existing items in the Treeview
        if self.treeview_bonus is not None:
            self.treeview_bonus.delete(*self.treeview_bonus.get_children())
        
        if role == "manager":
            employees = list(( db.reference("/manager").get()).keys())

        elif role == "Select Role":
            self.treeview_bonus.delete(*self.treeview_bonus.get_children())
            return
        else:
            employees= self.get_employee_data_with_non_zero_bonus()

        # Populate the Treeview with employee names
        for employee in employees:
            # Add the employee name, bonus amount, reason, hours attended with tag selectable

            # self.treeview_bonus.insert("", "end", values=(employee, db.reference("/employee").child(employee).child("bonus_req").get(), db.reference("/employee").child(employee).child("bonus_reason").get(), db.reference("/employee").child(employee).child("hours_attended").get()), tags=("clickable",))
            
            self.treeview_bonus.insert("", "end", values=(
                employee,
                db.reference("/employee").child(employee).child("bonus_req").get(),
                db.reference("/employee").child(employee).child("bonus_reason").get(),
                db.reference("/employee").child(employee).child("hours_attended").get()
            ), tags=("selectable",))

    def get_employee_data_with_non_zero_bonus(self):
        emp_ref = db.reference("/employee")
        employee_data = [user for user in emp_ref.get() if self.get_employee_data(user, "bonus_req") > 0]
        return employee_data

    def get_employee_data(self, username, data_type):
        emp_ref = db.reference("/employee")
        data = emp_ref.child(username).child(data_type).get()
        return data if data is not None else 0
    
    def grant_bonus(self):
        #create a window to grant bonus to the managers
        grant_bonus_window = tk.Toplevel()
        grant_bonus_window.geometry("400x300")
        grant_bonus_window.title("Grant Bonus")
        
        #create a canvas that resizes with the window
        self.grant_bonus_canvas = tk.Canvas(grant_bonus_window, bg="white", highlightthickness=0)
        self.grant_bonus_canvas.pack(fill=tk.BOTH, expand=True)
        
        #load the image as the background on the canvas
        self.load_image_grant_bonus()
        
        #bind window resize event to function
        grant_bonus_window.bind("<Configure>", lambda event: self.on_window_resize_grant_bonus(event))
        
        #center the window with function center_window_test
        self.center_window_all(grant_bonus_window)
        
        #focus on window
        grant_bonus_window.focus_force()
        
        #create a label for the bonus amount
        bonus_amount_label = tk.Label(
            self.grant_bonus_canvas,
            text="Bonus Amount",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        bonus_amount_label.pack(
            pady=20
        )
        bonus_amount_label.place(relx=0.5, rely=0.3, anchor="center")
        
        #create an entry for the bonus amount
        self.bonus_amount_entry = tk.Entry(
            grant_bonus_window, font=("Helvetica", 12, "bold")
        )
        self.bonus_amount_entry.pack(
            pady=20
        )
        self.bonus_amount_entry.place(relx=0.5, rely=0.4, anchor="center")
        self.bonus_amount_entry.insert(0, "")
        
        #create a submit button to grant the bonus
        submit_button = tk.Button(
            self.grant_bonus_canvas,
            text="Submit",
            command=lambda:self.grant_bonus_to_manager(grant_bonus_window),
            font=("Helvetica", 14),
            width=15,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        submit_button.place(relx=0.5, rely=0.9, anchor="s")
        
        #bind the enter key to the submit button
        grant_bonus_window.bind("<Return>", lambda event: self.grant_bonus_to_manager(grant_bonus_window))
        
        #bind the escape key to the exit function
        grant_bonus_window.bind("<Escape>", lambda event: grant_bonus_window.destroy())
        
        #run the main loop for the grant_bonus_window
        grant_bonus_window.mainloop()
        
    def grant_bonus_to_manager(self, grant_bonus_window):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        #Get the bonus amount from the entry
        bonus_amount = self.bonus_amount_entry.get()
        #Ask for confirmation
        if bonus_amount == "":
            messagebox.showinfo("Grant Bonus", "Please enter the bonus amount.")
        elif not bonus_amount.isdigit():
            messagebox.showinfo("Grant Bonus", "Bonus amount should be a number.")
        elif messagebox.askyesno("Confirm", f"Are you sure you want to grant a bonus of {bonus_amount} to the manager?"):
            #Grant the bonus in the database
            db.reference("/manager").child(self.treeview_bonus.item(self.treeview_bonus.selection())["values"][0]).child("bonus").set(int(bonus_amount))
            messagebox.showinfo("Grant Bonus", "Bonus granted successfully.")
        #Close the window
        grant_bonus_window.destroy()
        #focus on the salary management window
        self.approve_bonus_window.focus_force()
        
    def load_image_grant_bonus(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_grant_bonus_image = Image.open(img_path)
        self.resize_canvas_and_image_grant_bonus()
        
    def resize_canvas_and_image_grant_bonus(self):
        # Get the grant_bonus window size
        window_width = self.grant_bonus_canvas.winfo_width()
        window_height = self.grant_bonus_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.grant_bonus_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_grant_bonus_image.resize(
            (window_width, window_height)
        )
        self.grant_bonus_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.grant_bonus_canvas.delete("all")
        self.grant_bonus_canvas.create_image(
            0, 0, image=self.grant_bonus_image, anchor="nw"
        )
        
    def on_window_resize_grant_bonus(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_grant_bonus()
        
    def approve_bonus_btn(self):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        #Get the selected employee
        selected_employee = self.treeview_bonus.item(self.treeview_bonus.selection())["values"][0]
        #Get the bonus amount
        bonus_amount = self.treeview_bonus.item(self.treeview_bonus.selection())["values"][1]
        
        #Ask for confirmation
        if messagebox.askyesno("Approve Bonus", f"Are you sure you want to approve the bonus of {selected_employee} for {bonus_amount}?"):
            #Approve the bonus in the database
            db.reference("/employee").child(selected_employee).child("bonus").set(int(bonus_amount))
            db.reference("/employee").child(selected_employee).child("bonus_req").set(0)
            db.reference("/employee").child(selected_employee).child("bonus_reason").set("")
            messagebox.showinfo("Approve Bonus", "Bonus approved successfully.")
            #Refresh the list
            self.populate_employee_list_bonus(self.role_entry_bonus.get())
            self.approve_bonus_button["state"] = "disabled"
            self.deny_bonus_button["state"] = "disabled"
        #focus on window
        self.approve_bonus_window.focus_force()    
        
    def deny_bonus_btn(self):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        #Get the selected employee
        selected_employee = self.treeview_bonus.item(self.treeview_bonus.selection())["values"][0]
        #Ask for reason for denying the bonus
        reason = simpledialog.askstring("Deny Bonus", f"Please enter the reason for denying the bonus of {selected_employee}")
        if reason is not None:
            #Deny the bonus in the database
            db.reference("/employee").child(selected_employee).child("bonus").set(0)
            db.reference("/employee").child(selected_employee).child("bonus_req").set(0)
            db.reference("/employee").child(selected_employee).child("bonus_deny_reason").set(reason)
            db.reference("/employee").child(selected_employee).child("bonus_reason").set("")
            messagebox.showinfo("Deny Bonus", "Bonus denied successfully.")
            #Refresh the list
            self.populate_employee_list_bonus(self.role_entry_bonus.get())
            self.approve_bonus_button["state"] = "disabled"
            self.deny_bonus_button["state"] = "disabled"
        else:
            messagebox.showinfo("Deny Bonus", "Reason not provided.")
        self.approve_bonus_window.focus_force()
        
    def load_image_approve_bonus(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_approve_bonus_image = Image.open(img_path)
        self.resize_canvas_and_image_approve_bonus()
                
    def resize_canvas_and_image_approve_bonus(self):
        # Get the approve_bonus window size
        window_width = self.approve_bonus_canvas.winfo_width()
        window_height = self.approve_bonus_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.approve_bonus_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_approve_bonus_image.resize(
            (window_width, window_height)
        )
        self.approve_bonus_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.approve_bonus_canvas.delete("all")
        self.approve_bonus_canvas.create_image(
            0, 0, image=self.approve_bonus_image, anchor="nw"
        )
        
    def on_window_resize_approve_bonus(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_approve_bonus()

    def approve_resignation(self):
        #Create a window to approve the resignation of the employee
        self.approve_resignation_window = tk.Toplevel()
        self.approve_resignation_window.geometry("400x300")
        self.approve_resignation_window.title("Approve Resignation")
        
        #Create a canvas that resizes with the window
        self.approve_resignation_canvas = tk.Canvas(self.approve_resignation_window, bg="white", highlightthickness=0)
        self.approve_resignation_canvas.pack(fill=tk.BOTH, expand=True)

        #Load the image as the background on the canvas
        self.load_image_approve_resignation()
        
        #Bind window resize event to function
        self.approve_resignation_window.bind("<Configure>", lambda event: self.on_window_resize_approve_resignation(event))
        
        #Center the window with function center_window_test
        self.center_window_all(self.approve_resignation_window)
        
        #focus on window
        self.approve_resignation_window.focus_force()
        
        #Create a label as heading for the treeview
        resignation_label = tk.Label(
            self.approve_resignation_canvas,
            text="Resignation Requests",
            font=("Helvetica", 14, "bold"),
            bg="white",
        )
        resignation_label.pack(
            pady=20
        )
        resignation_label.place(relx=0.5, rely=0.1, anchor="center")
        # create a scrollable frame
        self.scrollable_frame_resignation = tk.Frame(self.approve_resignation_canvas, bg="white")
        self.scrollable_frame_resignation.pack(fill=tk.BOTH, expand=True)
        self.scrollable_frame_resignation.place(width=600, height=400,relx=0.5, rely=0.5, anchor="center")
        
        # create a treeview to display the employees
        #if self.treeview_resignation is None:
        self.treeview_resignation = ttk.Treeview(
            self.scrollable_frame_resignation, columns=("Employee",), show="headings", selectmode="browse"
        )
        self.treeview_resignation.heading("Employee", text="Employee")
        #Create columns for name,reason,if role is employee then add a column for hours attended and a button for approve
        self.treeview_resignation["columns"] = ("Employee","Role", "Reason")
        self.treeview_resignation.column("Employee", width=200, anchor="center")
        self.treeview_resignation.column("Role", width=100, anchor="center")
        self.treeview_resignation.column("Reason", width=600, anchor="center")
        self.treeview_resignation.heading("Employee", text="Employee")
        self.treeview_resignation.heading("Role", text="Role")
        self.treeview_resignation.heading("Reason", text="Reason")
        #Place the reason heading to the left
        self.treeview_resignation.column("Reason", anchor="w")
        self.treeview_resignation.tag_configure("selectable", foreground="blue", font=("Helvetica", 12, "underline"))
        self.treeview_resignation.tag_configure("clickable", foreground="blue", font=("Helvetica", 12, "underline"))
        # self.treeview_resignation.bind("<Double-1>", lambda event: self.open_employee_details_window(self.treeview_resignation.item(self.treeview_resignation.selection())["values"][0]))
        
        # Add a vertical scrollbar to the Treeview
        scrollbar_resignation_y = ttk.Scrollbar(self.scrollable_frame_resignation, orient="vertical", command=self.treeview_resignation.yview)
        scrollbar_resignation_y.pack(side="right", fill="y")
        self.treeview_resignation.configure(yscrollcommand=scrollbar_resignation_y.set)
        
        # Add a horizontal scrollbar to the Treeview
        scrollbar_resignation_x = ttk.Scrollbar(self.scrollable_frame_resignation, orient="horizontal", command=self.treeview_resignation.xview)
        scrollbar_resignation_x.pack(side="bottom", fill="x")
        self.treeview_resignation.configure(xscrollcommand=scrollbar_resignation_x.set)
        
        # Pack the Treeview to the scrollable frame
        self.treeview_resignation.pack(fill="both", expand=True)
        
        #Bind the treeview select event to function
        self.treeview_resignation.bind("<<TreeviewSelect>>",self.on_treeview_select_resignation)   
        
        #Populate the list with who applied for resignation, execute only once
        self.populate_employee_list_resignation()

        #Create 2 buttons for approve and deny that are disabled by default and enabled when a row is selected
        self.approve_resignation_button = tk.Button(
            self.approve_resignation_canvas,
            text="Approve Resignation",
            command=lambda:self.approve_resignation_btn(),
            font=("Helvetica", 14),
            width=20,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        self.approve_resignation_button.place(relx=0.5, rely=0.9, anchor="s")
        self.approve_resignation_button["state"] = "disabled"
        
        # Configure grid row and column weights
        self.scrollable_frame_resignation.grid_rowconfigure(0, weight=1)
        self.scrollable_frame_resignation.grid_columnconfigure(0, weight=1)
                
        #Bind the escape key to the exit function
        self.approve_resignation_window.bind("<Escape>", lambda event: self.approve_resignation_window.destroy())
        
        #Run the main loop for the self.approve_resignation_window
        self.approve_resignation_window.mainloop()
        
    def on_treeview_select_resignation(self, event):
        selected_items = self.treeview_resignation.selection()
        if selected_items:
            # Enable buttons if a row is selected
            self.approve_resignation_button["state"] = "normal"
        else:
            # Disable buttons if no row is selected
            self.approve_resignation_button["state"] = "disabled"
        
    def populate_employee_list_resignation(self):
        # Clear the existing items in the Treeview
        if self.treeview_resignation is not None:
            self.treeview_resignation.delete(*self.treeview_resignation.get_children())
        
        # Get the keys of employees and managers who have applied for resignation
        employees = list(db.reference("/employee").get().keys())
        managers = list(db.reference("/manager").get().keys())
        employees_with_resignation = []
        managers_with_resignation = []

        # Check if employees or managers have applied for resignation
        for employee in employees:
            resignation_status = db.reference("/employee").child(employee).child("resignation_request").child("resignation_status").get()
            if resignation_status == "Approved by Manager" and resignation_status != None:
                employees_with_resignation.append(employee)
        for manager in managers:
            resignation_request = db.reference("/manager").child(manager).child("resignation_request").child("resignation_status").get()
            if resignation_request != "Approved by HR" and resignation_request != None:
                managers_with_resignation.append(manager)
        
        # Combine employees and managers who have applied for resignation
        people_with_resignation = employees_with_resignation + managers_with_resignation

        # Populate the Treeview with employee names, reasons, and roles
        for person in people_with_resignation:
            reason = ""
            role = ""
            if person in employees_with_resignation:
                reason = db.reference("/employee").child(person).child("resignation_request").child("resignation_reason").get()
                #Replace \n with space
                if reason is not None:
                    reason = reason.replace("\n", " ")
                role = "Employee"
            elif person in managers_with_resignation:
                reason = db.reference("/manager").child(person).child("resignation_request").child("resignation_reason").get()
                if reason is not None:
                    #Replace \n with space
                    reason = reason.replace("\n", " ")
                role = "Manager"

            # Add the employee name, reason, and role with tag selectable
            self.treeview_resignation.insert("", "end", values=(person, role, reason), tags=("clickable",))

        # #Populate the Treeview with employee names, reasons, and roles
        # for person in people_with_resignation:
        #     reason = ""
        #     role = ""
        #     if person in employees_with_resignation and db.reference("/employee").child(person).child("resignation_request").child("resignation_status").get() == "Approved by Manager":
        #         reason = db.reference("/employee").child(person).child("resignation_request").child("resignation_reason").get()
        #         #Replace \n with space
        #         if reason is not None:
        #             reason = reason.replace("\n", " ")
        #         role = "Employee"
        #     elif person in managers_with_resignation and db.reference("/manager").child(person).child("resignation_request").child("resignation_status").get() != "Approved by HR":
        #         print (db.reference("/manager").child(person).child("resignation_request").get())
        #         reason = db.reference("/manager").child(person).child("resignation_request").child("resignation_reason").get()
        #         if reason is not None:
        #             #Replace \n with space
        #             reason = reason.replace("\n", " ")
        #         role = "Manager"

        #     # Add the employee name, reason, and role with tag selectable
        #     self.treeview_resignation.insert("", "end", values=(person, role, reason), tags=("clickable",))

    def approve_resignation_btn(self):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        #Get the selected employee
        selected_employee = self.treeview_resignation.item(self.treeview_resignation.selection())["values"][0]
        role= self.treeview_resignation.item(self.treeview_resignation.selection())["values"][1]
        #Ask for confirmation
        if messagebox.askyesno("Approve Resignation", f"Are you sure you want to approve the resignation of {selected_employee}?"):
            #Approve the resignation in the database
            if role == "Employee" and db.reference("/employee").child(selected_employee).child("resignation_request").child("resignation_status").get() =="Approved by Manager":
                db.reference("/employee").child(selected_employee).child("resignation_request").child("resignation_status").set("Approved by HR")
                #Set the resigning date to 4 weeks from the current date
                current_datetime = datetime.datetime.now()
                new_date = current_datetime + datetime.timedelta(weeks=4)
                current_datetime = new_date.strftime('%Y-%m-%d')
                db.reference("/employee").child(selected_employee).child("resignation_request").child("resignation_date").set(current_datetime)
                messagebox.showinfo("Approve Resignation", "Resignation approved successfully.")
                #Refresh the list
                self.populate_employee_list_resignation()
                self.approve_resignation_button["state"] = "disabled"
            if role=="Manager" and db.reference("/manager").child(selected_employee).child("resignation_request").get() != "Approved by HR":
                db.reference("/manager").child(selected_employee).child("resignation_request").child("resignation_status").set("Approved by HR")
                #Set the resigning date to 4 weeks from the current date
                current_datetime = datetime.datetime.now()
                new_date = current_datetime + datetime.timedelta(weeks=4)
                current_datetime = new_date.strftime('%Y-%m-%d')
                db.reference("/manager").child(selected_employee).child("resignation_request").child("resignation_date").set(current_datetime)
                messagebox.showinfo("Approve Resignation", "Resignation approved successfully.")
                #Refresh the list
                self.populate_employee_list_resignation()
                self.approve_resignation_button["state"] = "disabled"
        #focus on window
        self.approve_resignation_window.focus_force()
        
    def deny_resignation_btn(self):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        #Get the selected employee
        selected_employee = self.treeview_resignation.item(self.treeview_resignation.selection())["values"][0]
        role= self.treeview_resignation.item(self.treeview_resignation.selection())["values"][1]
        #Ask for reason for denying the resignation
        reason = simpledialog.askstring("Deny Resignation", f"Please enter the reason for denying the resignation of {selected_employee}")
        if reason is not None:
            #Deny the resignation in the database
            if role == "Employee":
                db.reference("/employee").child(selected_employee).child("resignation_request").child("resignation_status").set("Denied by HR")
                db.reference("/employee").child(selected_employee).child("resignation_request").child("resignation_deny_reason").set(reason)
            if role == "Manager":
                db.reference("/manager").child(selected_employee).child("resignation_request").child("resignation_status").set("Denied by HR")
                db.reference("/manager").child(selected_employee).child("resignation_request").child("resignation_deny_reason").set(reason)
            messagebox.showinfo("Deny Resignation", "Resignation denied successfully.")
            #Refresh the list
            self.populate_employee_list_resignation()
            self.approve_resignation_button["state"] = "disabled"

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

    def check_hours_attended(self):
        #Create a window to check the hours attended by the employee
        self.check_hours_attended_window = tk.Toplevel()
        self.check_hours_attended_window.geometry("400x300")
        self.check_hours_attended_window.title("Check Hours Attended")
        
        #Create a canvas that resizes with the window
        self.check_hours_attended_canvas = tk.Canvas(self.check_hours_attended_window, bg="white", highlightthickness=0)
        self.check_hours_attended_canvas.pack(fill=tk.BOTH, expand=True)
        
        #Load the image as the background on the canvas
        self.load_image_check_hours_attended()
        
        #Bind window resize event to function
        self.check_hours_attended_window.bind("<Configure>", lambda event: self.on_window_resize_check_hours_attended(event))
        
        #Center the window with function center_window_test
        self.center_window_all(self.check_hours_attended_window)
        
        #focus on window
        self.check_hours_attended_window.focus_force()
        
        #Create the treeview to display the employees
        self.treeview_check_hours_attended = ttk.Treeview(
            self.check_hours_attended_canvas, columns=("Employee", "Hours Attended","Warned"), show="headings", selectmode="browse"
        )
        self.treeview_check_hours_attended.heading("Employee", text="Employee")
        self.treeview_check_hours_attended.heading("Hours Attended", text="Hours Attended")
        self.treeview_check_hours_attended.heading("Warned", text="Warned")
        self.treeview_check_hours_attended.tag_configure("selectable", foreground="blue", font=("Helvetica", 12, "underline"))
        # self.treeview_check_hours_attended.bind("<Double-1>", lambda event: self.open_employee_details_window(self.treeview_check_hours_attended.item(self.treeview_check_hours_attended.selection())["values"][0]))

        #Configure the x and y scrollbars
        scrollbar_check_hours_attended_y = ttk.Scrollbar(self.treeview_check_hours_attended, orient="vertical", command=self.treeview_check_hours_attended.yview)
        scrollbar_check_hours_attended_y.pack(side="right", fill="y")
        self.treeview_check_hours_attended.configure(yscrollcommand=scrollbar_check_hours_attended_y.set)

        scrollbar_check_hours_attended_x = ttk.Scrollbar(self.treeview_check_hours_attended, orient="horizontal", command=self.treeview_check_hours_attended.xview)
        scrollbar_check_hours_attended_x.pack(side="bottom", fill="x")
        self.treeview_check_hours_attended.configure(xscrollcommand=scrollbar_check_hours_attended_x.set)

        #Pack the Treeview to the canvas and make the size 500x500
        self.treeview_check_hours_attended.pack(fill="both", expand=True)
        self.treeview_check_hours_attended.place(width=700, height=400, relx=0.5, rely=0.5, anchor="center")

        #Create a combo box to select the role of the employee
        role_entry_check_hours_attended_label = tk.Label(
            self.check_hours_attended_canvas,
            text="Hours Attended",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        role_entry_check_hours_attended_label.pack(
            pady=20
        )
        role_entry_check_hours_attended_label.place(relx=0.5, rely=0.1, anchor="center")
        self.role_entry_check_hours_attended = ttk.Combobox(
            self.check_hours_attended_canvas, font=("Helvetica", 12, "bold")
        )
        self.role_entry_check_hours_attended["values"] = ("Select Role", "Manager", "Employee")
        self.role_entry_check_hours_attended.pack(
            pady=20
        )
        self.role_entry_check_hours_attended.place(relx=0.5, rely=0.15, anchor="center")
        self.role_entry_check_hours_attended.current(0)

        self.role_entry_check_hours_attended.bind("<<ComboboxSelected>>", self.role_selected_check_hours_attended)

        #Create a button to warn the employee
        self.warn_employee_button = tk.Button(
            self.check_hours_attended_canvas,
            text="Warn Employee",
            command=lambda:self.warn_employee(),
            font=("Helvetica", 14),
            width=15,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        self.warn_employee_button.place(relx=0.5, rely=0.9, anchor="s")
        self.warn_employee_button["state"] = "disabled"
        
        #Change the state of the warn_employee_button to normal if a row is selected
        self.treeview_check_hours_attended.bind("<<TreeviewSelect>>",self.on_treeview_select_check_hours_attended)
        #Bind the escape key to the exit function
        self.check_hours_attended_window.bind("<Escape>", lambda event: self.check_hours_attended_window.destroy())

        #Run the main loop for the self.check_hours_attended_window
        self.check_hours_attended_window.mainloop()

    def on_treeview_select_check_hours_attended(self, event):
        selected_items = self.treeview_check_hours_attended.selection()
        if selected_items:
            # Enable buttons if a row is selected
            self.warn_employee_button["state"] = "normal"
        else:
            # Disable buttons if no row is selected
            self.warn_employee_button["state"] = "disabled"

    def role_selected_check_hours_attended(self, event):
        if self.role_entry_check_hours_attended == "Select Role":
            self.treeview_check_hours_attended.delete(*self.treeview_check_hours_attended.get_children())
            return
        selected_role = self.role_entry_check_hours_attended.get()
        if selected_role == "Employee":
            self.populate_employee_list_check_hours_attended(selected_role)
        elif selected_role == "Manager":
            self.populate_employee_list_check_hours_attended(selected_role)

    def populate_employee_list_check_hours_attended(self, role):
        # Clear the existing items in the Treeview
        if self.treeview_check_hours_attended is not None:
            self.treeview_check_hours_attended.delete(*self.treeview_check_hours_attended.get_children())

        if role == "Manager":
            employees = list(( db.reference("/manager").get()).keys())
            # Populate the Treeview with employee names and hours attended
            for employee in employees:
                self.treeview_check_hours_attended.insert("", "end", values=(employee, db.reference("/manager").child(employee).child("hours_attended").get(),db.reference("/manager").child(employee).child("warning").get()), tags=("selectable",))
        elif role == "Select Role":
            return
        else:
            employees = list(( db.reference("/employee").get()).keys())
            # Populate the Treeview with employee names and hours attended
            for employee in employees:
                self.treeview_check_hours_attended.insert("", "end", values=(employee, db.reference("/employee").child(employee).child("hours_attended").get(),db.reference("/employee").child(employee).child("warning").get()), tags=("selectable",))

    def warn_employee(self):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            self.check_hours_attended_window.destroy()
            return
        #Get the selected employee
        selected_employee = self.treeview_check_hours_attended.item(self.treeview_check_hours_attended.selection())["values"][0]
        #Check if the employee has already been warned
        if self.treeview_check_hours_attended.item(self.treeview_check_hours_attended.selection())["values"][2] == "Warning issued by HR":
            messagebox.showinfo("Warn Employee", "Employee has already been warned.")
            self.check_hours_attended_window.focus_force()
            return
        #Ask for confirmation
        if messagebox.askyesno("Warn Employee", f"Are you sure you want to warn {selected_employee}?"):
            if self.role_entry_check_hours_attended.get() == "Employee":
                #Warn the employee in the database
                db.reference("/employee").child(selected_employee).child("warning").set("Warning issued by HR")
                messagebox.showinfo("Warn Employee", "Employee warned successfully.")
            elif self.role_entry_check_hours_attended.get() == "Manager":
                #Warn the manager in the database
                db.reference("/manager").child(selected_employee).child("warning").set("Warning issued by HR")
                messagebox.showinfo("Warn Employee", "Manager warned successfully.")
            #Refresh the list
            self.populate_employee_list_check_hours_attended(self.role_entry_check_hours_attended.get())
            self.warn_employee_button["state"] = "disabled"
        #focus on window
        self.check_hours_attended_window.focus_force()

    def load_image_check_hours_attended(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_check_hours_attended_image = Image.open(img_path)
        self.resize_canvas_and_image_check_hours_attended()

    def resize_canvas_and_image_check_hours_attended(self):
        # Get the check_hours_attended window size
        window_width = self.check_hours_attended_canvas.winfo_width()
        window_height = self.check_hours_attended_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.check_hours_attended_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_check_hours_attended_image.resize(
            (window_width, window_height)
        )
        self.check_hours_attended_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.check_hours_attended_canvas.delete("all")
        self.check_hours_attended_canvas.create_image(
            0, 0, image=self.check_hours_attended_image, anchor="nw"
        )

    def on_window_resize_check_hours_attended(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_check_hours_attended()
        
    def survey_feedback(self, username):
        if hasattr(self, "survey_feedback_window"):
            try:
                if self.survey_feedback_window.winfo_exists():
                    self.survey_feedback_window.destroy()
            except:
                pass

        survey_feedback_window = tk.Toplevel()
        survey_feedback_window.geometry("800x600")
        survey_feedback_window.title("Submit Survey")
        self.survey_feedback_window = survey_feedback_window

        self.survey_feedback_canvas = tk.Canvas(survey_feedback_window, bg="white", highlightthickness=0)
        self.survey_feedback_canvas.pack(fill=tk.BOTH, expand=True)

        self.current_question_index = 0

        self.total_questions_fill= self.questions

        survey_feedback_window.bind("<Configure>", lambda event: self.display_survey_questions())
        survey_feedback_window.bind("<Escape>", lambda event: survey_feedback_window.destroy())

        if not hasattr(self, 'buttons_created_down') or not self.buttons_created_down:
            button_frame = tk.Frame(self.survey_feedback_canvas, bg="white")
            button_frame.pack(pady=20, side=tk.BOTTOM)

            self.next_button = tk.Button(button_frame, text="Next", command=lambda: self.next_question(username))
            self.next_button.grid(row=0, column=1)

            self.previous_button = tk.Button(button_frame, text="Previous", command=lambda: self.previous_question(username),state="disabled")
            self.previous_button.grid(row=0, column=0)

            self.submit_button = tk.Button(button_frame, text="Submit", command=lambda: self.survey_feedback_request(username))
            self.submit_button.grid(row=0, column=2)

        self.buttons_created_down = True
        
        self.survey_feedback_window.bind("<Escape>", lambda event: self.survey_feedback_window.destroy())
            
        if self.current_question_index < len(self.questions) - 1:
            self.survey_feedback_window.bind("<Return>", lambda event: self.next_question(username))
        else:
            self.survey_feedback_window.bind("<Return>", lambda event: self.survey_feedback_request(username))
        
        survey_feedback_window.focus_force()

        self.center_window_all(survey_feedback_window)

        survey_feedback_window.mainloop()

    def resize_canvas_and_image_survey_feedback(self):
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")
        self.original_survey_feedback_logo_image = Image.open(img_path)

        window_width = self.survey_feedback_canvas.winfo_width()
        window_height = self.survey_feedback_canvas.winfo_height()

        resized_image = self.original_survey_feedback_logo_image.resize((window_width, window_height))
        self.survey_feedback_logo_image = ImageTk.PhotoImage(resized_image)

        self.survey_feedback_canvas.create_image(0, 0, image=self.survey_feedback_logo_image, anchor="nw")

    def display_survey_questions(self):
        self.survey_feedback_canvas.delete("all")
        self.resize_canvas_and_image_survey_feedback()

        if self.current_question_index < 0:
            self.current_question_index = 0
        elif self.current_question_index >= len(self.questions):
            self.current_question_index = len(self.questions) - 1

        question_text = self.questions[self.current_question_index]
        self.survey_feedback_canvas.create_text(10, 10, text=question_text, font=("Helvetica", 14, "bold"), fill="white", anchor="nw")

        if not hasattr(self, 'buttons_created') or not self.buttons_created:
            self.survey_question_entry = tk.Entry(self.survey_feedback_canvas, font=("Helvetica", 12, "bold"), width=80)
            self.survey_question_entry.pack(pady=20)
            self.survey_question_entry.place(relx=0.5, rely=0.2, anchor="center")
            
            # Display previously entered answer, if any
            answer = self.answers.get(self.current_question_index, "")
            self.survey_question_entry.insert(0, answer)

        self.buttons_created = True

    def next_question(self, username):
        # Store the answer for the current question
        answer = self.survey_question_entry.get()
        self.answers[self.current_question_index] = answer
        self.survey_question_entry.delete(0, tk.END)

        self.current_question_index += 1 

        self.disable_buttons()
     
        self.display_survey_questions()
        # Retrieve the answer for the next question, if any
        next_answer = self.answers.get(self.current_question_index, "")

        # Update the entry with the previous answer
        self.survey_question_entry.delete(0, tk.END)
        self.survey_question_entry.insert(0, next_answer)

    def previous_question(self, username):
        
        # Store the answer for the current question
        answer = self.survey_question_entry.get()
        self.answers[self.current_question_index] = answer

        self.current_question_index -= 1

        self.disable_buttons()

        # Display the previous question
        self.display_survey_questions()

        # Retrieve the answer for the previous question, if any
        previous_answer = self.answers.get(self.current_question_index, "")

        # Update the entry with the previous answer
        self.survey_question_entry.delete(0, tk.END)
        self.survey_question_entry.insert(0, previous_answer)

    def disable_buttons(self):
        if self.current_question_index == len(self.total_questions_fill)-1:
            self.next_button.config(state="disabled")
            return
        else:
            self.next_button.config(state="normal")

        if self.current_question_index == 0:
            self.previous_button.config(state="disabled")
            return
        else:
            self.previous_button.config(state="normal")

    def survey_feedback_request(self, username):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to the database.")
            return

        # Store the answer for the current question
        answer = self.survey_question_entry.get().strip()  # Remove leading/trailing whitespace
        if not answer:  # Skip blank answers
            return

        self.answers[self.current_question_index] = answer

        # Delete existing survey data
        db.reference("Survey_Qs").delete()

        # Push non-blank answers to the database with sequential index values
        index = 0
        for question_index in range(len(self.total_questions_fill)):
            answer = self.answers.get(question_index, "").strip()  # Remove leading/trailing whitespace
            if answer:  # Only push non-blank answers
                db.reference("Survey_Qs").child("questions").child(str(index)).set(answer)
                index += 1

        # Update the total number of questions in the database
        self.update_total_questions()

         # Set the survey as available to all employees
        emp_data = db.reference("employee").get()
        for employee_id, employee_data in emp_data.items():
            db.reference("employee").child(employee_id).child("survey").child("available").set("Yes")

        for employee_id, employee_data in emp_data.items():
            db.reference("employee").child(employee_id).child("survey").child("answers").delete()

        # Clean up and close the survey window
        self.buttons_created = False
        self.buttons_created_down = False
        self.survey_feedback_window.destroy()
        messagebox.showinfo("Survey Feedback", "Survey feedback submitted successfully.")

            

    def update_total_questions(self): 
        total_questions = sum(1 for answer in self.answers.values() if answer)
        db.reference("Survey_Qs").child("total_questions").set(total_questions)

        
    def approve_promotion(self):
        #Create a new window for the approve_promotion top level
        self.approve_promotion_window = tk.Toplevel()
        self.approve_promotion_window.geometry("800x600")
        self.approve_promotion_window.title("Approve Promotion")
        self.treeview_promotion = None
        
        #Create the canvas
        self.approve_promotion_canvas = tk.Canvas(self.approve_promotion_window, bg="white", highlightthickness=0)
        self.approve_promotion_canvas.pack(fill=tk.BOTH, expand=True)
        
        #Load the image
        self.load_image_approve_promotion()
        
        #Center the window
        self.center_window_all(self.approve_promotion_window)
        
        #Create a scrollable frame
        self.scrollable_frame_promotion = tk.Frame(self.approve_promotion_canvas, bg="white")
        self.scrollable_frame_promotion.pack(fill="both", expand=True)
        self.scrollable_frame_promotion.place(relx=0.5, rely=0.5, anchor="center",width=600, height=400)
        
        #Create a treeview to display the employees
        if self.treeview_promotion is None:
            self.treeview_promotion = ttk.Treeview(
                self.scrollable_frame_promotion, columns=("Employee", "New Role","New Designation","New salary","Comment","Request by"), show="headings", selectmode="browse"
            )
            self.treeview_promotion.heading("Employee", text="Employee")
            self.treeview_promotion.heading("New Role", text="Role")
            self.treeview_promotion.heading("New Designation", text="Designation")
            self.treeview_promotion.heading("New salary", text="Salary")
            self.treeview_promotion.heading("Comment", text="Comment")
            self.treeview_promotion.column("Comment", width=600)
            self.treeview_promotion.heading("Request by", text="Request by")
            self.treeview_promotion.tag_configure("selectable", foreground="blue", font=("Helvetica", 12, "underline"))
            #self.treeview_promotion.bind("<Double-1>", lambda event: self.open_employee_details_window(self.treeview_promotion.item(self.treeview_promotion.selection())["values"][0]))
            
            #Add a vertical scrollbar to the Treeview
            scrollbar_promotion_y = ttk.Scrollbar(self.scrollable_frame_promotion, orient="vertical", command=self.treeview_promotion.yview)
            scrollbar_promotion_y.pack(side="right", fill="y")
            self.treeview_promotion.configure(yscrollcommand=scrollbar_promotion_y.set)
            
            #Add a horizontal scrollbar to the Treeview
            scrollbar_promotion_x = ttk.Scrollbar(self.scrollable_frame_promotion, orient="horizontal", command=self.treeview_promotion.xview)
            scrollbar_promotion_x.pack(side="bottom", fill="x")
            self.treeview_promotion.configure(xscrollcommand=scrollbar_promotion_x.set)
            
            #Pack the Treeview to the scrollable frame
            self.treeview_promotion.pack(fill="both", expand=True)
            
        #Configure grid row and column weights
        self.scrollable_frame_promotion.grid_rowconfigure(0, weight=1)
        self.scrollable_frame_promotion.grid_columnconfigure(0, weight=1)
        
        #Now you can delete the treeview and add new items to it
        self.treeview_promotion.delete(*self.treeview_promotion.get_children())
        
        #Bind the treeview select event to function
        self.treeview_promotion.bind("<<TreeviewSelect>>", self.on_treeview_select_promotion)
        
        # Create a combo box for approve, promote to manager
        self.role_selected_promotion = tk.StringVar()
        self.role_selected_promotion.set("None")
        self.role_entry_promotion = ttk.Combobox(
            self.approve_promotion_canvas,
            textvariable=self.role_selected_promotion,
            values=("None","Approve Promotion","Promote to Manager", "Promote Manager"),
            font=("Helvetica", 12),
        )
        
        #Place the combo box
        self.role_entry_promotion.place(relx=0.5, rely=0.1, anchor="center")
        
        #Bind the role selected event to function
        # Bind the role selected event to function
        self.role_entry_promotion.bind("<<ComboboxSelected>>", self.role_selected_promotion_callback)
        
        #Create 2 buttons for approve and deny that are disabled by default and enabled when a row is selected
        self.approve_promotion_button = tk.Button(
            self.approve_promotion_canvas,
            text="Approve Promotion",
            
            command=lambda:self.approve_promotion_btn(),
            font=("Helvetica", 14),
            width=20,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        self.approve_promotion_button.place(relx=0.35, rely=0.9, anchor="s")
        self.approve_promotion_button["state"] = "disabled"
        
        self.deny_promotion_button = tk.Button(
            self.approve_promotion_canvas,
            text="Deny Promotion",
            command=lambda:self.deny_promotion_btn(),
            font=("Helvetica", 14),
            width=20,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        self.deny_promotion_button.place(relx=0.65, rely=0.9, anchor="s")
        self.deny_promotion_button["state"] = "disabled"
        
        #Bind the escape key to the exit function
        self.approve_promotion_window.bind("<Escape>", lambda event: self.approve_promotion_window.destroy())
        
        #Run the main loop for the approve_promotion_window
        self.approve_promotion_window.mainloop()
        
    def role_selected_promotion_callback(self, event):
        selected_role = self.role_selected_promotion.get()
        self.populate_employee_list_promotion(selected_role)
        
    def on_treeview_select_promotion(self, event):
        selected_items = self.treeview_promotion.selection()
        selected_role = self.role_selected_promotion.get()
        if selected_items:
            if selected_role == "Promote Manager":
                self.approve_promotion_button["state"] = "normal"
                self.deny_promotion_button["state"] = "disabled"
            elif selected_role == "Approve Promotion":
                self.approve_promotion_button["state"] = "normal"
                self.deny_promotion_button["state"] = "normal"
            elif selected_role == "Promote to Manager":
                self.approve_promotion_button["state"] = "normal"
                self.deny_promotion_button["state"] = "disabled"
        else:
            #Disable buttons if no row is selected
            self.approve_promotion_button["state"] = "disabled"
            self.deny_promotion_button["state"] = "disabled"
            
    def populate_employee_list_promotion(self,role):
        #Clear the existing items in the Treeview
        if self.treeview_promotion is not None:
            self.treeview_promotion.delete(*self.treeview_promotion.get_children())
        
        if role=="None":
            return
        elif role == "Approve Promotion":
            #Get only the keys of the employees that have applied for promotion
            employees = list(( db.reference("/employee").get()).keys())
            employees_with_promotion = []
            for employee in employees:
                #Check if apply_for_promotion value exists and is not empty
                if db.reference("/employee").child(employee).child("promotion_request").child("Request").get() =="Pending":
                    employees_with_promotion.append(employee)
            #Populate the Treeview with employee names
            for employee in employees_with_promotion:
                #Add the employee name,role with tag selectable
                new_role = db.reference("/employee").child(employee).child("role").get()
                new_designation = db.reference("/employee").child(employee).child("promotion_request").child("new_designation").get()
                new_salary = db.reference("/employee").child(employee).child("promotion_request").child("new_salary").get()
                comment = db.reference("/employee").child(employee).child("promotion_request").child("comment").get()
                request_by = db.reference("/employee").child(employee).child("promotion_request").child("request_by").get()
                self.treeview_promotion.insert("", "end", values=(employee, new_role,new_designation,new_salary,comment,request_by), tags=("selectable",))
        elif role == "Promote Manager":
            #List out all the managers present in the database
            managers = list(( db.reference("/manager").get()).keys())
            for manager in managers:
                #Get the salary,designation of the manager
                salary = db.reference("/manager").child(manager).child("salary").get()
                designation = db.reference("/manager").child(manager).child("designation").get()
                self.treeview_promotion.insert("", "end", values=(manager, "Manager",designation,salary), tags=("selectable",))
        elif role == "Promote to Manager":
            #List out all the employees present in the database
            employees = list(( db.reference("/employee").get()).keys())
            for employee in employees:
                #Get the salary,designation of the employee
                salary = db.reference("/employee").child(employee).child("salary").get()
                designation = db.reference("/employee").child(employee).child("designation").get()
                self.treeview_promotion.insert("", "end", values=(employee, "Employee",designation,salary), tags=("selectable",))
            
    def approve_promotion_btn(self):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        #Get the selected employee
        selected_employee = self.treeview_promotion.item(self.treeview_promotion.selection())["values"][0]
        selected_role = self.role_selected_promotion.get()
        print(selected_role)
        if selected_role == "None":
            messagebox.showinfo("Approve Promotion", "Please select a role.")
        elif selected_role == "Approve Promotion":
            #Ask for confirmation
            if messagebox.askyesno("Approve Promotion", f"Are you sure you want to approve the promotion of {selected_employee}?"):
                #Update the details in the database
                db.reference("/employee").child(selected_employee).child("promotion_request").child("Request").set("Approved")
                new_designation = db.reference("/employee").child(selected_employee).child("promotion_request").child("new_designation").get()
                new_salary = db.reference("/employee").child(selected_employee).child("promotion_request").child("new_salary").get()
                db.reference("/employee").child(selected_employee).child("designation").set(new_designation)
                db.reference("/employee").child(selected_employee).child("salary").set(new_salary)
                messagebox.showinfo("Approve Promotion", "Promotion approved successfully.")
                #Refresh the list
                self.populate_employee_list_promotion(selected_role)
                self.approve_promotion_button["state"] = "disabled"
                self.deny_promotion_button["state"] = "disabled"
        elif selected_role == "Promote Manager":
            self.promote_manager(selected_employee) 
        elif selected_role == "Promote to Manager":
            self.promote_to_manager(selected_employee)
        #Focus on window
        self.approve_promotion_window.focus_force()
        
    def deny_promotion_btn(self):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        #Get the selected employee
        selected_employee = self.treeview_promotion.item(self.treeview_promotion.selection())["values"][0]
        #Ask for confirmation
        if messagebox.askyesno("Deny Promotion", f"Are you sure you want to deny the promotion of {selected_employee}?"):
            #Deny the promotion in the database
            db.reference("/employee").child(selected_employee).child("promotion_request").child("Request").set("Denied")
            #Ask for reason for denying the promotion
            reason = simpledialog.askstring("Deny Promotion", f"Please enter the reason for denying the promotion of {selected_employee}")
            db.reference("/employee").child(selected_employee).child("promotion_request").child("Reason").set(reason)
            messagebox.showinfo("Deny Promotion", "Promotion denied successfully.")
            #Refresh the list
            self.populate_employee_list_promotion()
            self.approve_promotion_button["state"] = "disabled"
        #Focus on window
        self.approve_promotion_window.focus_force()
        
    def load_image_approve_promotion(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_approve_promotion_image = Image.open(img_path)
        self.resize_canvas_and_image_approve_promotion()

        # Bind window resize event to function
        self.approve_promotion_window.bind("<Configure>", self.on_window_resize_approve_promotion)

    def on_window_resize_approve_promotion(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_approve_promotion()

    def resize_canvas_and_image_approve_promotion(self):
        # Get the approve_promotion window size
        window_width = self.approve_promotion_window.winfo_width()
        window_height = self.approve_promotion_window.winfo_height()

        # Resize the canvas to the current window size
        self.approve_promotion_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_approve_promotion_image.resize((window_width, window_height))
        self.approve_promotion_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.approve_promotion_canvas.delete("all")
        self.approve_promotion_canvas.create_image(0, 0, image=self.approve_promotion_image, anchor="nw")

    def promote_manager(self,selected_employee):
        self.promote_manager_window = tk.Toplevel()
        self.promote_manager_window.geometry("400x300")
        self.promote_manager_window.title("Promote Manager")
        
        #Create a canvas that resizes with the window
        self.promote_manager_canvas = tk.Canvas(self.promote_manager_window, bg="white", highlightthickness=0)
        self.promote_manager_canvas.pack(fill=tk.BOTH, expand=True)
        
        #Load the image as the background on the canvas
        self.load_image_promote_manager()
        
        #Bind window resize event to function
        self.promote_manager_window.bind("<Configure>", lambda event: self.on_window_resize_promote_manager(event))
        
        #Center the window with function center_window_test
        self.center_window_all(self.promote_manager_window)
        
        #focus on window
        self.promote_manager_window.focus_force()
        
        #Create a label for employee name
        employee_name_label = tk.Label(
            self.promote_manager_canvas,
            text=f"Employee: {selected_employee}",
            font=("Helvetica", 12),
            bg="white",
        )
        employee_name_label.place(relx=0.5, rely=0.1, anchor="center")
        
        #Create a label for current role
        current_role_label = tk.Label(
            self.promote_manager_canvas,
            text="Current Role: Manager",
            font=("Helvetica", 12),
            bg="white",
        )
        current_role_label.place(relx=0.5, rely=0.2, anchor="center")
        
        #Create an entry for new salary and designation
        new_salary_label = tk.Label(
            self.promote_manager_canvas,
            text="New Salary:",
            font=("Helvetica", 12),
            bg="white",
        )
        new_salary_label.place(relx=0.3, rely=0.3, anchor="center")
        
        self.new_salary_entry = tk.Entry(self.promote_manager_canvas, font=("Helvetica", 12), width=20)
        self.new_salary_entry.place(relx=0.7, rely=0.3, anchor="center")
        
        #Create a designation entry
        self.new_designation_label = tk.Label(
            self.promote_manager_canvas,
            text="New Designation:",
            font=("Helvetica", 12),
            bg="white",
        )
        self.new_designation_label.place(relx=0.3, rely=0.35, anchor="center")
        
        self.new_designation_entry = tk.Entry(self.promote_manager_canvas, font=("Helvetica", 12), width=20)
        self.new_designation_entry.place(relx=0.7, rely=0.35, anchor="center")
        
        #Create a comment entry
        comment_label = tk.Label(
            self.promote_manager_canvas,
            text="Comment:",
            font=("Helvetica", 12),
            bg="white",
        )
        comment_label.place(relx=0.3, rely=0.4, anchor="center")
        
        self.comment_entry = tk.Entry(self.promote_manager_canvas, font=("Helvetica", 12), width=20)
        self.comment_entry.place(relx=0.7, rely=0.4, anchor="center")
        
        #Create a button for promote
        promote_button = tk.Button(
            self.promote_manager_canvas,
            text="Promote",
            command=lambda:self.promote_btn(selected_employee),
            font=("Helvetica", 14),
            width=20,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        promote_button.place(relx=0.5, rely=0.9, anchor="s")
        
        #Bind the escape key to the exit function
        self.promote_manager_window.bind("<Escape>", lambda event: self.promote_manager_window.destroy())
        
        #Run the main loop for the promote_manager_window
        self.promote_manager_window.mainloop()
        
    def promote_btn(self,selected_employee):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        #Get the new salary and comment
        new_designation = self.new_designation_entry.get()
        new_salary = self.new_salary_entry.get()
        comment = self.comment_entry.get()
        if new_designation == "" or new_salary == "" or comment == "":
            messagebox.showinfo("Promote Manager", "Please fill in all the details.")
            return
        if not new_salary.isdigit():
            messagebox.showinfo("Promote Manager", "Please enter a valid number for salary.")
            return
        #Ask for confirmation
        if messagebox.askyesno("Promote Manager", f"Are you sure you want to promote {selected_employee}?"):
            #Promote the manager in the database
            db.reference("/manager").child(selected_employee).child("designation").set(new_designation)
            db.reference("/manager").child(selected_employee).child("salary").set(new_salary)
            db.reference("/manager").child(selected_employee).child("comment_for_promotion").set(comment)
            messagebox.showinfo("Promote Manager", "Manager promoted successfully.")
            self.promote_manager_window.destroy()
        #Focus on window
        self.approve_promotion.focus_force()
        
    def load_image_promote_manager(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_promote_manager_image = Image.open(img_path)
        self.resize_canvas_and_image_promote_manager()
        
    def resize_canvas_and_image_promote_manager(self):
        # Get the promote_manager window size
        window_width = self.promote_manager_canvas.winfo_width()
        window_height = self.promote_manager_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.promote_manager_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_promote_manager_image.resize((window_width, window_height))
        self.promote_manager_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.promote_manager_canvas.delete("all")
        self.promote_manager_canvas.create_image(0, 0, image=self.promote_manager_image, anchor="nw")
        
    def on_window_resize_promote_manager(self, event):
        self.resize_canvas_and_image_promote_manager()
        
    def promote_to_manager(self,selected_employee):
        self.promote_to_manager_window = tk.Toplevel()
        self.promote_to_manager_window.geometry("400x300")
        self.promote_to_manager_window.title("Promote to Manager")
        
        #Create a canvas that resizes with the window
        self.promote_to_manager_canvas = tk.Canvas(self.promote_to_manager_window, bg="white", highlightthickness=0)
        self.promote_to_manager_canvas.pack(fill=tk.BOTH, expand=True)
        
        #Load the image as the background on the canvas
        self.load_image_promote_to_manager()
        
        #Bind window resize event to function
        self.promote_to_manager_window.bind("<Configure>", lambda event: self.on_window_resize_promote_to_manager(event))
        
        #Center the window with function center_window_test
        self.center_window_all(self.promote_to_manager_window)
        
        #focus on window
        self.promote_to_manager_window.focus_force()
        
        #Create a label for employee name
        employee_name_label = tk.Label(
            self.promote_to_manager_canvas,
            text=f"Employee: {selected_employee}",
            font=("Helvetica", 12),
            bg="white",
        )
        employee_name_label.place(relx=0.5, rely=0.1, anchor="center")
        
        #Create a label for current role
        current_role_label = tk.Label(
            self.promote_to_manager_canvas,
            text="Current Role: Employee",
            font=("Helvetica", 12),
            bg="white",
        )
        current_role_label.place(relx=0.5, rely=0.2, anchor="center")
        
        #Create an entry for new salary and designation
        new_salary_label = tk.Label(
            self.promote_to_manager_canvas,
            text="New Salary:",
            font=("Helvetica", 12),
            bg="white",
        )
        new_salary_label.place(relx=0.3, rely=0.3, anchor="center")
        
        self.new_salary_entry = tk.Entry(self.promote_to_manager_canvas, font=("Helvetica", 12), width=20)
        self.new_salary_entry.place(relx=0.7, rely=0.3, anchor="center")
        
        #Create a designation entry
        self.new_designation_label = tk.Label(
            self.promote_to_manager_canvas,
            text="New Designation:",
            font=("Helvetica", 12),
            bg="white",
        )
        self.new_designation_label.place(relx=0.3, rely=0.35, anchor="center")
        
        self.new_designation_entry = tk.Entry(self.promote_to_manager_canvas, font=("Helvetica", 12), width=20)
        self.new_designation_entry.place(relx=0.7, rely=0.35, anchor="center")
        
        #Create a comment entry
        comment_label = tk.Label(
            self.promote_to_manager_canvas,
            text="Comment:",
            font=("Helvetica", 12),
            bg="white",
        )
        comment_label.place(relx=0.3, rely=0.4, anchor="center")
        
        self.comment_entry = tk.Entry(self.promote_to_manager_canvas, font=("Helvetica", 12), width=20)
        self.comment_entry.place(relx=0.7, rely=0.4, anchor="center")
        
        #Create a button for promote
        promote_button = tk.Button(
            self.promote_to_manager_canvas,
            text="Promote",
            command=lambda:self.promote_to_manager_btn(selected_employee),
            font=("Helvetica", 14),
            width=20,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        promote_button.place(relx=0.5, rely=0.9, anchor="s")
        
        #Bind the escape key to the exit function
        self.promote_to_manager_window.bind("<Escape>", lambda event: self.promote_to_manager_window.destroy())
        
        #Run the main loop for the promote_to_manager_window
        self.promote_to_manager_window.mainloop()
        
    def promote_to_manager_btn(self,selected_employee):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        #Get the new salary and comment
        new_designation = self.new_designation_entry.get()
        new_salary = self.new_salary_entry.get()
        comment = self.comment_entry.get()
        if new_designation == "" or new_salary == "" or comment == "":
            messagebox.showinfo("Promote to Manager", "Please fill in all the details.")
            return
        if not new_salary.isdigit():
            messagebox.showinfo("Promote to Manager", "Please enter a valid number for salary.")
            return
        #Ask for confirmation
        if messagebox.askyesno("Promote to Manager", f"Are you sure you want to promote {selected_employee} to Manager?"):
            #Approve the promotion in the database by deleting the employee details from employee and adding to manager
            new_role = "manager"
            new_designation = self.new_designation_entry.get()
            new_salary = self.new_salary_entry.get()
            db.reference("/manager").child(selected_employee).set(db.reference("/employee").child(selected_employee).get())
            db.reference("/employee").child(selected_employee).delete()
            db.reference("/manager").child(selected_employee).child("role").set(new_role)
            db.reference("/manager").child(selected_employee).child("designation").set(new_designation)
            db.reference("/manager").child(selected_employee).child("salary").set(new_salary)
            db.reference("/manager").child(selected_employee).child("comment_for_promotion").set(comment)
            messagebox.showinfo("Promote to Manager", "Employee promoted to Manager successfully.")
            #Refresh the list
            self.populate_employee_list_promotion(self.role_selected_promotion.get())
            self.approve_promotion_button["state"] = "disabled"
        self.promote_to_manager_window.destroy()
        #Focus on promotion window
        self.approve_promotion_window.focus_force()
        
    def load_image_promote_to_manager(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_promote_to_manager_image = Image.open(img_path)
        self.resize_canvas_and_image_promote_to_manager()
        
    def resize_canvas_and_image_promote_to_manager(self):
        # Get the promote_to_manager window size
        window_width = self.promote_to_manager_canvas.winfo_width()
        window_height = self.promote_to_manager_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.promote_to_manager_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_promote_to_manager_image.resize((window_width, window_height))
        self.promote_to_manager_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.promote_to_manager_canvas.delete("all")
        self.promote_to_manager_canvas.create_image(0, 0, image=self.promote_to_manager_image, anchor="nw")
        
    def on_window_resize_promote_to_manager(self, event):
        self.resize_canvas_and_image_promote_to_manager()
    
    def apply_for_resignation(self,username):
        #Create a new window for the apply_for_resignation top level
        self.apply_for_resignation_window = tk.Toplevel()
        self.apply_for_resignation_window.geometry("800x600")
        self.apply_for_resignation_window.title("Apply for Resignation")
        
        #Create the canvas
        self.apply_for_resignation_canvas = tk.Canvas(self.apply_for_resignation_window, bg="white", highlightthickness=0)
        self.apply_for_resignation_canvas.pack(fill=tk.BOTH, expand=True)
        
        #Load the image
        self.load_image_apply_for_resignation()
        
        #Bind window resize event to function
        self.apply_for_resignation_window.bind("<Configure>", lambda event: self.on_window_resize_apply_for_resignation(event))
        
        #Center the window
        self.center_window_all(self.apply_for_resignation_window)
        
        self.reason_entry = tk.Text(self.apply_for_resignation_canvas, font=("Helvetica", 12), width=50, height=5)
        self.reason_entry.place(relx=0.5, rely=0.5, anchor="center")
        self.reason_entry.insert(tk.END, "Reason for resignation")
        self.reason_entry.bind("<FocusIn>", lambda event: self.reason_entry.delete("1.0", tk.END))
        
        #Create a button for apply for resignation
        apply_for_resignation_button = tk.Button(
            self.apply_for_resignation_canvas,
            text="Apply for Resignation",
            command=lambda:self.apply_for_resignation_btn(username),
            font=("Helvetica", 14),
            width=20,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        apply_for_resignation_button.place(relx=0.5, rely=0.9, anchor="s")
        
        #Bind the escape key to the exit function
        self.apply_for_resignation_window.bind("<Escape>", lambda event: self.apply_for_resignation_window.destroy())
        
        #Run the main loop for the apply_for_resignation_window
        self.apply_for_resignation_window.mainloop()
        
    def apply_for_resignation_btn(self,username):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        #Get the reason for resignation with \n at end of each line and store as string
        reason = self.reason_entry.get("1.0",tk.END)

        if db.reference("/HR").child(username).child("resignation_request").child("Request").get() == "pending":
            messagebox.showinfo("Apply for Resignation", "You have already applied for resignation.")
            return
        if reason == "Reason for resignation" or reason == "":
            messagebox.showinfo("Apply for Resignation", "Please enter the reason for resignation.")
            return
        #Ask for confirmation
        if messagebox.askyesno("Apply for Resignation", "Are you sure you want to apply for resignation?"):
            #Apply for resignation in the database
            db.reference("/HR").child(username).child("resignation_request").child("resignation_status").set("pending")
            db.reference("/HR").child(username).child("resignation_request").child("resignation_reason").set(reason)
            messagebox.showinfo("Apply for Resignation", "Resignation applied successfully.")
            self.apply_for_resignation_window.destroy()
        
    def load_image_apply_for_resignation(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_apply_for_resignation_image = Image.open(img_path)
        self.resize_canvas_and_image_apply_for_resignation()
        
    def resize_canvas_and_image_apply_for_resignation(self):
        # Get the apply_for_resignation window size
        window_width = self.apply_for_resignation_canvas.winfo_width()
        window_height = self.apply_for_resignation_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.apply_for_resignation_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_apply_for_resignation_image.resize((window_width, window_height))
        self.apply_for_resignation_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.apply_for_resignation_canvas.delete("all")
        self.apply_for_resignation_canvas.create_image(0, 0, image=self.apply_for_resignation_image, anchor="nw")
        
    def on_window_resize_apply_for_resignation(self, event):
        self.resize_canvas_and_image_apply_for_resignation()
     
    def approve_review(self):
        # Create a new window for the approve_review top level
        self.approve_review_window = tk.Toplevel()
        self.approve_review_window.geometry("800x600")
        self.approve_review_window.title("Approve Review")
        
        # Create the canvas
        self.approve_review_canvas = tk.Canvas(self.approve_review_window, bg="white", highlightthickness=0)
        self.approve_review_canvas.pack(fill=tk.BOTH, expand=True)

        # Load the image
        self.load_image_approve_review()
    
        # Bind window resize event to function
        self.approve_review_window.bind("<Configure>", lambda event: self.on_window_resize_approve_review(event))
        
        # Center the window
        self.center_window_all(self.approve_review_window)
        
        # Bind the escape key to the exit function
        self.approve_review_window.bind("<Escape>", lambda event: self.approve_review_window.destroy())
        
        # Create a scrollable frame for treeview
        self.approve_review_frame = tk.Frame(self.approve_review_canvas, bg="white")
        self.approve_review_frame.pack(fill=tk.BOTH, expand=True)
        self.approve_review_frame.place(width=600, height=400,relx=0.5, rely=0.5, anchor="center")

        # Add a vertical scrollbar to the Treeview
        treeview_scrollbar_y = ttk.Scrollbar(self.approve_review_frame, orient="vertical")
        treeview_scrollbar_y.pack(side="right", fill="y")

        # Add a horizontal scrollbar to the Treeview
        treeview_scrollbar_x = ttk.Scrollbar(self.approve_review_frame, orient="horizontal")
        treeview_scrollbar_x.pack(side="bottom", fill="x")

        # Create a Treeview widget
        self.treeview_approve_review = ttk.Treeview(self.approve_review_frame, columns=("Employee", "Role", "Type"), show="headings", selectmode="browse", yscrollcommand=treeview_scrollbar_y.set, xscrollcommand=treeview_scrollbar_x.set)
        self.treeview_approve_review.heading("Employee", text="Employee")
        self.treeview_approve_review.heading("Role", text="Role")
        self.treeview_approve_review.pack(fill="both", expand=True)
        self.treeview_approve_review.column("Employee", width=400)
        self.treeview_approve_review.column("Role", width=200)
        self.treeview_approve_review.tag_configure("selectable", background="white", foreground="blue")
        self.treeview_approve_review.bind("<Double-1>", lambda event:self.on_treeview_select_approve_review(event))

        # Configure the scrollbars to move with the Treeview
        treeview_scrollbar_y.config(command=self.treeview_approve_review.yview)
        treeview_scrollbar_x.config(command=self.treeview_approve_review.xview)
                
        # Create a combo box to select the type of performance review
        self.review_type = tk.StringVar()
        self.review_type.set("None")
        self.review_type_combo = ttk.Combobox(self.approve_review_window, textvariable=self.review_type, values=["None","Quarterly Review", "Annual Review"])
        self.review_type_combo.pack(pady=20)
        self.review_type_combo.place(relx=0.5,rely=0.15, anchor="center")  # Adjust the x and y coordinates as needed 
        self.review_type_combo.bind("<<ComboboxSelected>>", self.on_review_type_selected)

        # Configure grid row and column weights
        self.approve_review_frame.grid_rowconfigure(0, weight=1)
        self.approve_review_frame.grid_columnconfigure(0, weight=1)
        
        # Run the main loop for the approve_review_window
        self.approve_review_window.mainloop()

       
    def on_review_type_selected(self,event):
        if self.review_type.get() == "None":
            self.treeview_approve_review.delete(*self.treeview_approve_review.get_children())
        elif self.review_type.get() == "Quarterly Review":
            self.populate_employee_list_review("Quarterly Review")
        elif self.review_type.get() == "Annual Review":
            self.populate_employee_list_review("Annual Review")
        
    def populate_employee_list_review(self,review_type):
        self.treeview_approve_review.delete(*self.treeview_approve_review.get_children())
        if review_type == "Quarterly Review":
            employee_data_8 = list((db.reference("/employee").get()).keys())
            for employee in employee_data_8:
                if db.reference("/employee").child(employee).child("performance_review").child("Quarterly Review").child("status").get() == "Approved by Manager":
                    self.treeview_approve_review.insert("", "end", values=(employee, "Employee","Quarterly Review"), tags="selectable")
        elif review_type == "Annual Review":
            employee_data_9 = list((db.reference("/employee").get()).keys())
            for employee in employee_data_9:
                if db.reference("/employee").child(employee).child("performance_review").child("Annual Review").child("status").get() == "Approved by Manager":
                    self.treeview_approve_review.insert("", "end", values=(employee, "Employee","Annual Review"), tags="selectable")
                    
        if review_type == "Quarterly Review":
            manager_data_8 = list((db.reference("/manager").get()).keys())
            for manager in manager_data_8:
                if db.reference("/manager").child(manager).child("performance_review").child("Quarterly Review").child("status").get() == "filled":
                    self.treeview_approve_review.insert("", "end", values=(manager, "Manager","Quarterly Review"), tags="selectable")
        elif review_type == "Annual Review":
            manager_data_9 = list((db.reference("/manager").get()).keys())
            for manager in manager_data_9:
                if db.reference("/manager").child(manager).child("performance_review").child("Annual Review").child("status").get() == "filled":
                    self.treeview_approve_review.insert("", "end", values=(manager, "Manager","Annual Review"), tags="selectable") 
        
    def on_treeview_select_approve_review(self,event):
        try:
            #Get the selected employee
            selected_employee = self.treeview_approve_review.item(self.treeview_approve_review.selection())["values"][0]
            selected_role = self.treeview_approve_review.item(self.treeview_approve_review.selection())["values"][1]
            selected_review = self.treeview_approve_review.item(self.treeview_approve_review.selection())["values"][2]
            if db.reference("/manager").child(selected_employee).child("performance_review").child(selected_review).child("status").get() == "Approved by HR":
                messagebox.showinfo("Approve Review", "This review has already been approved by HR.")
                return
            # if db.reference("/employee").child(selected_employee).child("performance_review").child(selected_review).child("status").get() == "Approved by Manager":
            #     messagebox.showinfo("Approve Review", "This review has already been approved by Manager.")
            #     return
            self.open_review(selected_employee,selected_role,selected_review)
        except:
            pass
        
    def open_review(self,selected_employee,selected_role,selected_review):
        #Create a new window for the open_review top level
        self.open_review_window = tk.Toplevel()
        self.open_review_window.geometry("800x600")
        self.open_review_window.title("Open Review")
        
        #Create the canvas
        self.open_review_canvas = tk.Canvas(self.open_review_window, bg="white", highlightthickness=0)
        self.open_review_canvas.pack(fill=tk.BOTH, expand=True)
        
        #Load the image
        self.load_image_open_review()
        
        #Bind window resize event to function
        self.open_review_window.bind("<Configure>", lambda event: self.on_window_resize_open_review(event))
        
        #Center the window
        self.center_window_all(self.open_review_window)
        
        #focus on window
        self.open_review_window.focus_force()
        
        #bind the escape key to the exit function
        self.open_review_window.bind("<Escape>", lambda event: self.open_review_window.destroy())
        
        performance_review_label = tk.Label(
            self.open_review_canvas,
            text="Performance Review",
            font=("Helvetica", 16),
            bg="white",
        )
        performance_review_label.pack(pady=20)
        performance_review_label.place(relx=0.5, rely=0.15, anchor="center")
        
        self.performance_review_entry = tk.Text(self.open_review_canvas, font=("Helvetica", 12, "bold"),height=5)
        self.performance_review_entry.pack(pady=20)
        self.performance_review_entry.place(width=500, relx=0.5, rely=0.25, anchor="center")
        
        if selected_role == "Employee":
            performance_review = db.reference("/employee").child(selected_employee).child("performance_review").child(selected_review).child(
                "performance_review").get()
            self.performance_review_entry.insert(tk.END, performance_review)
        elif selected_role == "Manager":
            performance_review = db.reference("/manager").child(selected_employee).child("performance_review").child(selected_review).child(
                "performance_review").get()
            self.performance_review_entry.insert(tk.END, performance_review)
        self.performance_review_entry.configure(state="disabled")
        
        feedback_label = tk.Label(
            self.open_review_canvas,
            text="Constructed Feedback",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        feedback_label.pack(pady=20)
        feedback_label.place(relx=0.5, rely=0.35, anchor="center")
        
        self.feedback_entry = tk.Text(self.open_review_canvas, font=("Helvetica", 12, "bold"),height=5)
        self.feedback_entry.pack(pady=20)
        self.feedback_entry.place(width=500, relx=0.5, rely=0.45, anchor="center")
        
        if selected_role == "Employee":
            feedback = db.reference("/employee").child(selected_employee).child("performance_review").child(selected_review).child(
                "constructed_feedback").get()
            self.feedback_entry.insert(tk.END, feedback)
        elif selected_role == "Manager":
            feedback = db.reference("/manager").child(selected_employee).child("performance_review").child(selected_review).child(
                "constructed_feedback").get()
            self.feedback_entry.insert(tk.END, feedback)
        self.feedback_entry.configure(state="disabled")
        
        future_goals_label = tk.Label(
            self.open_review_canvas,
            text="Goals for Future",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        future_goals_label.pack(pady=20)
        future_goals_label.place(relx=0.5, rely=0.55, anchor="center")
        
        self.future_goals_entry = tk.Text(
            self.open_review_canvas, font=("Helvetica", 12, "bold"), height=5
        )
        self.future_goals_entry.pack(pady=20)
        self.future_goals_entry.place(width=500, relx=0.5, rely=0.65, anchor="center")
        
        if selected_role == "Employee":
            future_goals = db.reference("/employee").child(selected_employee).child("performance_review").child(selected_review).child(
                "goals_for_future").get()
            self.future_goals_entry.insert(tk.END, future_goals)
        elif selected_role == "Manager":
            future_goals = db.reference("/manager").child(selected_employee).child("performance_review").child(selected_review).child(
                "goals_for_future").get()
            self.future_goals_entry.insert(tk.END, future_goals)
        self.future_goals_entry.configure(state="disabled")

        # Create 2 buttons to approve or deny the performance review
        self.approve_button = tk.Button(
            self.open_review_window,
            text="Approve",
            command=lambda employee=selected_employee, type=type: self.approve_performance_review(employee, type),
            font=("Helvetica", 14),
        )
        self.approve_button.pack(
            pady=20
        )
        self.approve_button.place(relx=0.5, rely=0.8, anchor="center", width=100, height=30)
        
        self.deny_button = tk.Button(
            self.open_review_window,
            text="Deny",
            command=lambda employee=selected_employee, type=type: self.deny_performance_review(employee, type),
            font=("Helvetica", 14),
        )
        self.deny_button.pack(
            pady=20
        )
        self.deny_button.place(relx=0.5, rely=0.9, anchor="center", width=100, height=30)
        
        #Run the main loop for the open_review_window
        self.open_review_window.mainloop()
        
    def approve_performance_review(self,employee,type):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        #Ask for confirmation
        if messagebox.askyesno("Approve Review", "Are you sure you want to approve this review?"):
            if type == "Employee":
                db.reference("/employee").child(employee).child("performance_review").child("Quarterly Review").child("status").set("Approved by HR")
            elif type == "Manager":
                db.reference("/manager").child(employee).child("performance_review").child("Quarterly Review").child("status").set("Approved by HR")
            messagebox.showinfo("Approve Review", "Review approved successfully.")
            self.open_review_window.destroy()
        #Focus on window
        self.approve_review.focus_force()
        
    def deny_performance_review(self,employee,type):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        #Ask for confirmation
        if messagebox.askyesno("Deny Review", "Are you sure you want to deny this review?"):
            #Ask for the reason for denial
            reason = simpledialog.askstring("Deny Review", "Please enter the reason for denial.")
            if reason == None:
                return
            if type == "Employee":
                db.reference("/employee").child(employee).child("performance_review").child("Quarterly Review").child("status").set("Denied by HR")
                db.reference("/employee").child(employee).child("performance_review").child("Quarterly Review").child("denial_reason").set(reason)
            elif type == "Manager":
                db.reference("/manager").child(employee).child("performance_review").child("Quarterly Review").child("status").set("Denied by HR")
                db.reference("/manager").child(employee).child("performance_review").child("Quarterly Review").child("denial_reason").set(reason)
            messagebox.showinfo("Deny Review", "Review denied successfully.")
            self.open_review_window.destroy()
        #Focus on window
        self.approve_review.focus_force()
               
    def load_image_open_review(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_open_review_image = Image.open(img_path)
        self.resize_canvas_and_image_open_review()
        
    def resize_canvas_and_image_open_review(self):
        # Get the open_review window size
        window_width = self.open_review_canvas.winfo_width()
        window_height = self.open_review_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.open_review_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_open_review_image.resize((window_width, window_height))
        self.open_review_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.open_review_canvas.delete("all")
        self.open_review_canvas.create_image(0, 0, image=self.open_review_image, anchor="nw")
    
    def on_window_resize_open_review(self, event):
        self.resize_canvas_and_image_open_review()
        
    def load_image_approve_review(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_approve_review_image = Image.open(img_path)
        self.resize_canvas_and_image_approve_review()
        
    def resize_canvas_and_image_approve_review(self):
        # Get the approve_review window size
        window_width = self.approve_review_canvas.winfo_width()
        window_height = self.approve_review_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.approve_review_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_approve_review_image.resize((window_width, window_height))
        self.approve_review_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.approve_review_canvas.delete("all")
        self.approve_review_canvas.create_image(0, 0, image=self.approve_review_image, anchor="nw")
        
    def on_window_resize_approve_review(self, event):
        self.resize_canvas_and_image_approve_review()
          
    def entry_del(self,entry_widget, default_text):
        #Delete the default text in the entry widget
        if entry_widget.get() == default_text:
            entry_widget.delete(0, tk.END)
    
    def review_complaints(self):
        # Create a new window for the review_complaints top level
        self.review_complaints_window = tk.Toplevel()
        self.review_complaints_window.geometry("800x600")
        self.review_complaints_window.title("Review Complaints")
        
        # Create the canvas
        self.review_complaints_canvas = tk.Canvas(self.review_complaints_window, bg="white", highlightthickness=0)
        self.review_complaints_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Load the image
        self.load_image_review_complaints()
        
        # Bind window resize event to function
        self.review_complaints_window.bind("<Configure>", lambda event: self.on_window_resize_review_complaints(event))
        
        # Center the window
        self.center_window_all(self.review_complaints_window)

        # Create a Treeview widget
        self.treeview_review_complaints = ttk.Treeview(self.review_complaints_canvas, columns=("Employee","Role","Complaint","Complaint by"), show="headings", selectmode="browse")
        self.treeview_review_complaints.heading("Employee", text="Employee")
        self.treeview_review_complaints.heading("Role", text="Role")
        self.treeview_review_complaints.heading("Complaint", text="Complaint")
        self.treeview_review_complaints.heading("Complaint by", text="Complaint by")
        self.treeview_review_complaints.pack(fill="both", expand=True)
        self.treeview_review_complaints.column("Employee", width=150, anchor="center")
        self.treeview_review_complaints.column("Role", width=150, anchor="center")
        self.treeview_review_complaints.column("Complaint", width=400, anchor="center")
        self.treeview_review_complaints.column("Complaint by", width=150, anchor="center")
        self.treeview_review_complaints.tag_configure("selectable", background="white", foreground="blue")

        #Create a vertical scrollbar for the Treeview
        treeview_scrollbar_y = ttk.Scrollbar(self.treeview_review_complaints, orient="vertical")
        treeview_scrollbar_y.pack(side="right", fill="y")
        treeview_scrollbar_y.config(command=self.treeview_review_complaints.yview)

        #Create a horizontal scrollbar for the Treeview
        treeview_scrollbar_x = ttk.Scrollbar(self.treeview_review_complaints, orient="horizontal")
        treeview_scrollbar_x.pack(side="bottom", fill="x")
        treeview_scrollbar_x.config(command=self.treeview_review_complaints.xview)

        self.treeview_review_complaints.configure(yscrollcommand=treeview_scrollbar_y.set, xscrollcommand=treeview_scrollbar_x.set)

        #Place the treeview in the canvas
        self.treeview_review_complaints.place(width = 700, height = 500,relx=0.5, rely=0.5, anchor="center")
        # Populate the Treeview with the complaints
        self.populate_complaints_treeview()

        #Create a button to warn the employee
        self.warn_button = tk.Button(
            self.review_complaints_canvas,
            text="Warn",
            command=lambda:self.warn_employee_complaints(),
            font=("Helvetica", 14),
            width=20,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
            state="disabled",
        )
        self.warn_button.place(relx=0.5, rely=0.95, anchor="s")

        # Bind the Treeview selection event to the function
        self.treeview_review_complaints.bind("<ButtonRelease-1>", lambda event: self.on_treeview_select_review_complaints(event))

        # Bind the escape key to the exit function
        self.review_complaints_window.bind("<Escape>", lambda event: self.review_complaints_window.destroy())

        # Run the main loop for the review_complaints_window
        self.review_complaints_window.mainloop()

    def on_treeview_select_review_complaints(self,event):
        #Check if a row is selected
        if self.treeview_review_complaints.selection():
            self.warn_button["state"] = "normal"
        else:
            self.warn_button["state"] = "disabled"

    def populate_complaints_treeview(self):
        # Clear the Treeview
        self.treeview_review_complaints.delete(*self.treeview_review_complaints.get_children())
        # Get the data from the database
        emp_data = list((db.reference("/employee").get()).keys())
        mng_data = list((db.reference("/manager").get()).keys())
        for employee in emp_data:
            if db.reference("/employee").child(employee).child("complaint").child("status").get() == "pending":
                complaint = db.reference("/employee").child(employee).child("complaint").child("problem").get()
                #Replace \n with space
                complaint = complaint.replace("\n"," ")
                complaint_by = db.reference("/employee").child(employee).child("complaint").child("complaint_by").get()
                self.treeview_review_complaints.insert("", "end", values=(employee, "Employee", complaint, complaint_by), tags="selectable")
        for manager in mng_data:
            if db.reference("/manager").child(manager).child("complaint").child("status").get() == "pending":
                complaint = db.reference("/manager").child(manager).child("complaint").child("problem").get()
                #Replace \n with space
                complaint = complaint.replace("\n"," ")
                complaint_by = db.reference("/manager").child(manager).child("complaint").child("complaint_by").get()
                self.treeview_review_complaints.insert("", "end", values=(manager, "Manager", complaint, complaint_by), tags="selectable")

    def warn_employee_complaints(self):
        # Get the selected employee
        selected_employee = self.treeview_review_complaints.item(self.treeview_review_complaints.selection())["values"][0]
        print(selected_employee)
        #selected_role = self.treeview_review_complaints.item(self.treeview_review_complaints.selection())["values"][1]
        if db.reference("/employee").child(selected_employee).child("complaint").child("status").get() == "pending":
            db.reference("/employee").child(selected_employee).child("complaint").child("status").set("warned")
            messagebox.showinfo("Warn Employee", "Employee warned successfully.")
        elif db.reference("/manager").child(selected_employee).child("complaint").child("status").get() == "pending":
            db.reference("/manager").child(selected_employee).child("complaint").child("status").set("warned")
            messagebox.showinfo("Warn Employee", "Manager warned successfully.")
        self.populate_complaints_treeview()
        self.review_complaints_window.focus_force()

    def load_image_review_complaints(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_review_complaints_image = Image.open(img_path)
        self.resize_canvas_and_image_review_complaints()

    def resize_canvas_and_image_review_complaints(self):
        # Get the review_complaints window size
        window_width = self.review_complaints_canvas.winfo_width()
        window_height = self.review_complaints_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.review_complaints_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_review_complaints_image.resize((window_width, window_height))
        self.review_complaints_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.review_complaints_canvas.delete("all")
        self.review_complaints_canvas.create_image(0, 0, image=self.review_complaints_image, anchor="nw")

    def on_window_resize_review_complaints(self, event):
        self.resize_canvas_and_image_review_complaints()

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
        
        # Create a change password button in canvas and place at top right
        change_password_button = tk.Button(
            self.profile_canvas,
            text="Change Password",
            command=lambda:self.change_password(username),
            font=("Helvetica", 14),
            bd=0,
            fg="white",
            bg="black",  # You can change the color as needed
            activebackground="black",  # You can change the color as needed
        )
        change_password_button.place(relx=0.9, rely=0.1, anchor="center")
        
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

        list=self.getdata(username,self.uni_role)
        text1=f"EID: {list[0]}\nName: {username}\nRole: {self.uni_role}\nDesignation: {list[1]}\nSalary: {list[2]}\nHors Attended: {list[3]}\nBonus: {list[4]}\nSick Days: {list[5]}\nVacation Days: {list[6]}"
        if role=="HR":
            resigning_date=db.reference("/HR").child(username).child("resignation_request").child("resignation_date").get()
            if resigning_date is not None:
                text1+=f"\nResignation Date: {resigning_date}"
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
    
    def change_password(self,username):
        # Create a new window for the change_password top level
        self.change_password_window = tk.Toplevel()
        self.change_password_window.geometry("800x600")
        self.change_password_window.title("Change Password")
        
        # Create the canvas
        self.change_password_canvas = tk.Canvas(self.change_password_window, bg="white", highlightthickness=0)
        self.change_password_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Load the image
        self.change_password_load_image()
        
        # Create entry widgets for the old password, new password, and confirm new password
        entry_labels = ["Old Password", "New Password", "Confirm New Password"]
        entry_variables = [tk.StringVar() for _ in range(3)]
        entry_widgets = []

        for i in range(3):
            entry_widget = tk.Entry(self.change_password_canvas, width=50, font=("Helvetica", 14), textvariable=entry_variables[i])
            entry_widget.pack(pady=40, side=tk.TOP, anchor=tk.CENTER)
            entry_widget.insert(0, entry_labels[i])
            entry_widget.bind("<FocusIn>", lambda event, entry_widget=entry_widget, default_text=entry_labels[i]: self.entry_del(entry_widget, default_text))

            entry_widgets.append(entry_widget)
            
        # Create a button to submit the change password request
        submit_button = tk.Button(self.change_password_canvas, text="Submit", command=lambda: self.change_password_request(username, entry_variables, self.change_password_window))
        submit_button.pack(pady=20, side=tk.TOP, anchor=tk.CENTER)

        # Bind the Escape key to the exit function
        self.change_password_window.bind("<Escape>", lambda event: self.change_password_window.destroy())
        
        # bind window resize event to function
        self.change_password_window.bind("<Configure>", lambda event: self.on_window_resize_change_password(event))
        
        #Bind the return key to the submit button
        self.change_password_window.bind("<Return>", lambda event: self.change_password_request(username, entry_variables, self.change_password_window))
        
        # focus on window
        self.change_password_window.focus_force()
        
        # Center the window with function center_window_test
        self.center_window_all(self.change_password_window)
        
        # Run the main loop for the self.change_password_window
        self.change_password_window.mainloop()
    
    def change_password_load_image(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_change_password_image = Image.open(img_path)
        self.resize_canvas_and_image_change_password()
        
    def resize_canvas_and_image_change_password(self, event=None):
        # Get the change_password window size
        window_width = self.change_password_canvas.winfo_width()
        window_height = self.change_password_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.change_password_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_change_password_image.resize((window_width, window_height))
        self.change_password_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.change_password_canvas.delete("all")
        self.change_password_canvas.create_image(0, 0, image=self.change_password_image, anchor="nw")
        
    def on_window_resize_change_password(self, event=None):
        self.resize_canvas_and_image_change_password()
        
    def change_password_request(self, username, entry_variables, window):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        # Get the entered values from the Entry widgets
        old_password = entry_variables[0].get()
        new_password = entry_variables[1].get()
        confirm_new_password = entry_variables[2].get()
        
        #Check if the entered values are valid
        if old_password == "Old Password" or new_password == "New Password" or confirm_new_password == "Confirm New Password":
            messagebox.showerror("Error", "Please enter valid values for the password")
        elif old_password == "" or new_password == "" or confirm_new_password == "":
            messagebox.showerror("Error", "Please enter valid values for the password")
        elif old_password == new_password:
            messagebox.showerror("Error", "Old Password and New Password cannot be the same")
        elif new_password != confirm_new_password:
            messagebox.showerror("Error", "New Password and Confirm New Password do not match")
        else:
            # Update the database with the new password
            hr_ref = db.reference("/HR")
            hr_ref.child(username).update({"password": new_password})
            # Close the change password window
            window.destroy()
            # Show a message that the password has been changed
            messagebox.showinfo("Password Change", "Password Changed Successfully")
            self.change_password_window.destroy()
        self.change_password_window.destroy()
        self.profile_canvas.focus_force()
            
    def entry_del(self, entry_widget, default_text):
        current_content = entry_widget.get()
        if current_content == default_text:
            entry_widget.delete(0, tk.END)
          
    def logout(self,hr_window):
        #Close all windows
        hr_window.destroy()
        messagebox.showinfo("Logout", "You have been logged out successfully.")
        Main(True)
    
    def view_survey_results(self):
        # Create a new window for the view_survey_results top level
        self.view_survey_results_window = tk.Toplevel()
        self.view_survey_results_window.geometry("800x600")
        self.view_survey_results_window.title("View Survey Results")
        
        # Create the canvas
        self.view_survey_results_canvas = tk.Canvas(self.view_survey_results_window, bg="white", highlightthickness=0)
        self.view_survey_results_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Load the image
        self.load_image_view_survey_results()
        
        # Bind window resize event to function
        self.view_survey_results_window.bind("<Configure>", lambda event: self.on_window_resize_view_survey_results(event))
        
        # Center the window
        self.center_window_all(self.view_survey_results_window)
        
        # Create a Treeview widget
        self.treeview_survey_results = ttk.Treeview(self.view_survey_results_canvas, columns=("Employee",), show="headings", selectmode="browse")
        self.treeview_survey_results.heading("Employee", text="Employee")
        self.treeview_survey_results.pack(fill="both", expand=True)
        self.treeview_survey_results.column("Employee", width=400,anchor="center")
        self.treeview_survey_results.tag_configure("selectable", background="white", foreground="blue")
        
        self.treeview_text()

        # Create a vertical scrollbar for the Treeview
        treeview_scrollbar_y = ttk.Scrollbar(self.treeview_survey_results, orient="vertical")
        treeview_scrollbar_y.pack(side="right", fill="y")
        treeview_scrollbar_y.config(command=self.treeview_survey_results.yview)
        self.treeview_survey_results.configure(yscrollcommand=treeview_scrollbar_y.set)
        
        # Place the treeview in the canvas
        self.treeview_survey_results.place(width=400, height=600, relx=0.5, rely=0.5, anchor="center")
        
        
        # Populate the Treeview with the survey results
        self.populate_survey_results_treeview()

        # Bind the Escape key to the exit function
        self.view_survey_results_window.bind("<Escape>", lambda event: self.view_survey_results_window.destroy())

        # Run the main loop for the view_survey_results_window
        self.view_survey_results_window.mainloop()

    def populate_survey_results_treeview(self):
        # Clear the Treeview
        self.treeview_survey_results.delete(*self.treeview_survey_results.get_children())
        
        # Get the data from the database
        emp_data = db.reference("/employee").get()
        for employee, data in emp_data.items():
            # Check if the survey is not available
            survey_available = data.get("survey", {}).get("available")
            if survey_available == "No":
                # If survey is not available, insert the employee's name into the Treeview
                self.treeview_survey_results.insert("", "end", values=(employee,), tags="selectable")

                # Bind a function to the TreeviewSelect event to handle the click event
                self.treeview_survey_results.bind("<<TreeviewSelect>>", self.on_employee_select)

    def treeview_text(self):
        # Center all the text in the Treeview
        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=("Helvetica", 10))
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
       
    def load_image_view_survey_results(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_view_survey_results_image = Image.open(img_path)
        self.resize_canvas_and_image_view_survey_results()

    def resize_canvas_and_image_view_survey_results(self):
        # Get the view_survey_results window size
        window_width = self.view_survey_results_canvas.winfo_width()
        window_height = self.view_survey_results_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.view_survey_results_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_view_survey_results_image.resize((window_width, window_height))
        self.view_survey_results_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.view_survey_results_canvas.delete("all")
        self.view_survey_results_canvas.create_image(0, 0, image=self.view_survey_results_image, anchor="nw")

    def on_window_resize_view_survey_results(self, event):
        self.resize_canvas_and_image_view_survey_results()

    def on_employee_select(self, event):
        #create a new window which takes the employee name as reference and pulls it child survey answers
        # Create a new window for the survey_results top level
        self.survey_results_window = tk.Toplevel()
        self.survey_results_window.geometry("800x600")
        self.survey_results_window.title("Survey Results")
        selected_employee = self.treeview_survey_results.item(self.treeview_survey_results.selection())["values"][0]
        
       # Pull the Survey_Qs from the database along with its index values
        survey_questions= db.reference("/Survey_Qs").child("questions").get()  
        #survey_questions = [(index, question) for index, question in survey_qs.items()]


        # Pull the survey answers from the database along with its index values
        survey_answers_ref = db.reference("/employee").child(selected_employee).child("survey").child("answers")
        survey_answers = survey_answers_ref.get()
        survey_answers = [(index, answer) for index, answer in enumerate(survey_answers)]

        self.survey_questions = survey_questions
        self.survey_answers = survey_answers

        # Create the canvas
        self.survey_results_canvas = tk.Canvas(self.survey_results_window, bg="white", highlightthickness=0)
        self.survey_results_canvas.pack(fill=tk.BOTH, expand=True)

        # Load the image
        self.load_image_survey_results()

        # Bind window resize event to function
        self.survey_results_window.bind("<Configure>", lambda event: self.on_window_resize_survey_results(event))

        # Center the window
        self.center_window_survey(self.survey_results_window)

        #force focus on window
        self.survey_results_window.focus_force()
        
        #main loop for the survey_results_window
        self.survey_results_window.mainloop()

    def load_image_survey_results(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_survey_results_image = Image.open(img_path)
        self.resize_canvas_and_image_survey_results()

    def resize_canvas_and_image_survey_results(self):
        # Get the survey_results window size
        window_width = self.survey_results_canvas.winfo_width()
        window_height = self.survey_results_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.survey_results_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_survey_results_image.resize((window_width, window_height))
        self.survey_results_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.survey_results_canvas.delete("all")
        self.survey_results_canvas.create_image(0, 0, image=self.survey_results_image, anchor="nw")

        # Check if both survey_questions and survey_answers have the same length
        if len(self.survey_questions) != len(self.survey_answers):
            print("Error: Mismatch in the number of questions and answers")
            return

        # Divide the available width into two columns
        column_width = window_width // 2

        # Vertical position for displaying questions and answers
        y_position = 10

        # Track the current column
        current_column = 0

        # Create a label on the canvas for each question and answer pair
        for i in range(len(self.survey_questions)):
            question_number = i + 1
            question = self.survey_questions[i]
            answer = self.survey_answers[i][1]

            # Calculate the x-coordinate based on the current column
            x_position = current_column * column_width

            # Display question number and question in the current column
            self.survey_results_canvas.create_text(
                x_position + 10,  # X-coordinate (left)
                y_position,  # Y-coordinate
                font=("Helvetica", 12, "bold"),
                text=f"Q{question_number}. {question}",
                fill="white",
                anchor="nw"
            )
            y_position += 25  # Increment y_position for answer

            # Display answer in the current column
            self.survey_results_canvas.create_text(
                x_position + 10,  # X-coordinate (left)
                y_position,  # Y-coordinate
                font=("Helvetica", 12),
                text=f"Answer: {answer}",
                fill="white",
                anchor="nw"
            )

            # Increment y_position for next question
            y_position += 40

            # Switch to the next column if the current column is full
            if y_position >= window_height:
                current_column = 1
                y_position = 10  # Reset y_position for the next column


    def on_window_resize_survey_results(self, event):
        self.resize_canvas_and_image_survey_results()

    
def main(role,username):
    # Create a new window
    hr=HR_class()
    hr.open_hr_window(role,username,"HR")