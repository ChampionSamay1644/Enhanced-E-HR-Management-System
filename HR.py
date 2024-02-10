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

class HR_class:
    def __init__(this):
        
        this.root = tk.Tk()
        this.root.geometry("800x600")
        this.root.title("HR Window")
        
    def load_image_common(this):
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        try:
            this.original_common_image = Image.open(img_path)
        except Exception as e:
            print(f"Error loading image: {e}")
        
        
    def on_window_resize_common(this,username,role, event=None):
        this.resize_canvas_and_image_common(username,role)

    def create_common_window(this, title,username,role):

        common_window = tk.Tk()
        common_window.geometry("800x600")
        common_window.title(title)

        this.common_canvas = tk.Canvas(common_window, bg="white", highlightthickness=0)
        this.common_canvas.pack(fill=tk.BOTH, expand=True)

        common_window.bind("<Configure>",lambda event,username=username,role=role:this.on_window_resize_common(username,role))

        this.load_image_common()
        this.resize_canvas_and_image_common(username,role)
        
        return common_window, this.common_canvas
        
    def center_window_all(this, window):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width / 2) - (900 / 2)
        y = (screen_height / 2) - (600 / 2)
        window.geometry("%dx%d+%d+%d" % (900, 600, x, y))
        
    def resize_canvas_and_image_common(this,username,role):
        window_width = this.common_canvas.winfo_width()
        window_height = this.common_canvas.winfo_height()
        this.common_canvas.config(width=window_width, height=window_height)

        resized_image = this.original_common_image.resize((window_width, window_height))
        this.common_image = ImageTk.PhotoImage(resized_image)

        this.common_canvas.delete("all")
        this.common_canvas.create_image(0, 0, image=this.common_image, anchor="nw")
        
        if username=="Default" or role=="Default":
            return
        # Add text to the top center of the canvas
        text_content = f"Hello, {username}"
        text_position = (window_width // 2, 20)  # Top center of the canvas
        this.common_canvas.create_text(text_position, text=text_content, anchor="center")
        this.common_canvas.itemconfig(this.common_canvas.find_all()[-1], fill="white")
        
        # if role=="employee":
        #     list=this.getdata(username)
        #     text1=f"EID: {list[0]}\nName: {username}\nDesignation: {list[1]}\nSalary: {list[2]}\nHours Attended: {list[3]}\nBonus: {list[4]}\nSick Days: {list[5]}\nVacation Days: {list[6]}\nSurvey: {list[7]}"
        #     this.common_canvas.create_text(
        #         10,  # X-coordinate (left)
        #         this.common_canvas.winfo_height() - 10,  # Y-coordinate (bottom)
        #         font=("Helvetica", 15, "bold"),
        #         text=text1,
        #         fill="white",
        #         anchor="sw"  # Anchor to bottom left
        #     )

    def open_hr_window(this,role, username):
        # this.root.destroy()  # Close the main login window
        # hr_window = tk.Tk()  # Use Tk() to create a new window
        # hr_window.geometry("800x600")  # Set the window size
        # hr_window.title("HR Window")
        if hasattr(this, "root"):
            try:
                if this.root.winfo_exists():
                    this.root.destroy()  # Close the main login window
            except:
                pass
            
        this.treeview = None
        
        hr_window,this.hr_logo_canvas=this.create_common_window("HR Window",username,role)
        
        # create a canvas that resizes with the window
        # this.hr_logo_canvas = tk.Canvas(hr_window, bg="white", highlightthickness=0)
        # this.hr_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        # hr_window.bind("<Configure>", lambda event: this.on_window_resize_hr(event,username))

        # import the image as the background on the canvas
        # this.load_image_hr(username)


        #buttons of HR window
        this.salary_management_button = tk.Button(
            this.hr_logo_canvas, text="Employee Management", command=lambda:this.salary_management(), font=("Helvetica", 14)
        )
        this.salary_management_button.pack(
            pady=20
        )
        this.salary_management_button.place(
            relx=0.75, rely=0.3, anchor="center", width=200, height=30
        )
        this.approve_bonus_button = tk.Button(
            this.hr_logo_canvas, text="Approve Bonus", command=lambda:this.approve_bonus(), font=("Helvetica", 14)
        )
        this.approve_bonus_button.pack(
            pady=20
        )
        this.approve_bonus_button.place(

            relx=0.75, rely=0.375, anchor="center", width=200, height=30
        )
        this.approve_resignation_button = tk.Button(
            this.hr_logo_canvas, text="Approve Resignation", command=lambda:this.approve_resignation(), font=("Helvetica", 14)
        )
        this.approve_resignation_button.pack(
            pady=20
        )
        this.approve_resignation_button.place(
            relx=0.75, rely=0.450, anchor="center", width=200, height=30
        )
        this.check_hours_attended_button = tk.Button(
            this.hr_logo_canvas, text="Check Employee Hours Attended", command=lambda:this.check_hours_attended(), font=("Helvetica", 14)
        )
        this.check_hours_attended_button.pack(
            pady=20
        )
        this.check_hours_attended_button.place(
            relx=0.75, rely=0.525, anchor="center", width=300, height=30
        )
        this.survey_feedback_button = tk.Button(
            this.hr_logo_canvas, text="Survey/Feedback", command=lambda:this.survey_feedback(), font=("Helvetica", 14)
        )
        this.survey_feedback_button.pack(
            pady=20
        )
        this.survey_feedback_button.place(
            relx=0.75, rely=0.6, anchor="center", width=200, height=30
        )
        # this.addbe_button = tk.Button(
        #     this.hr_logo_canvas, text="Add manager/Employee", command=lambda:this.create_all_hr(), font=("Helvetica", 14)
        # )
        # this.addbe_button.pack(
        #     pady=20
        # )
        # this.addbe_button.place(
        #     relx=0.75, rely=0.675, anchor="center", width=300, height=30
        # )
        # this.removebe_button = tk.Button(
        #     this.hr_logo_canvas, text="Remove manager/Employee", command=lambda:this.remove_all_hr(), font=("Helvetica", 14)
        # )
        # this.removebe_button.pack(
        #     pady=20
        # )
        # this.removebe_button.place(
        #     relx=0.75, rely=0.750, anchor="center", width=300, height=30
        # )

        #create an exit button in canvas and place at bottom middle
        exit_button = tk.Button(
        this.hr_logo_canvas,
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
        
        profile_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "profile.png" #change jpg to png for main background
        )
        profile_img = PhotoImage(file=profile_path)
        
        resized_profile_img = profile_img.subsample(4, 4)
        
        profile_btn = tk.Button(
            this.hr_logo_canvas, image=resized_profile_img, command=lambda:this.profile(username,role),borderwidth=0, font=("Helvetica", 14)
        )
        profile_btn.pack(
            pady=20
        )
        profile_btn.place(
            relx=0.95, rely=0.05, anchor="center", width=50, height=50
        )

        # focus on window
        hr_window.focus_force()

        # Center the window with function center_window_test
        this.center_window_all(hr_window)

        # Bind the Escape key to the exit function
        hr_window.bind("<Escape>", lambda event: hr_window.destroy())

        #  Run the main loop for the HR window
        hr_window.mainloop()
        
    def load_image_hr(this,username):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        this.original_hr_logo_image = Image.open(img_path)
        this.resize_canvas_and_image_hr(username)

    def resize_canvas_and_image_hr(this,username):
        username_hr = username
        # Get the hr window size
        window_width = this.hr_logo_canvas.winfo_width()
        window_height = this.hr_logo_canvas.winfo_height()
        

        # Resize the canvas to the current window size
        this.hr_logo_canvas.config(width=window_width, height=window_height)


        # Resize the image if needed
        resized_image = this.original_hr_logo_image.resize(
            (window_width, window_height)
        )
        this.hr_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        this.hr_logo_canvas.delete("all")
        this.hr_logo_canvas.create_image(
            0, 0, image=this.hr_logo_image, anchor="nw"
        )

            #redraw the hr name text    
        if hasattr(this, "hr_name_text"):
            this.hr_logo_canvas.delete(
                this.hr_name_text
            )
        this.hr_name_text = this.hr_logo_canvas.create_text(
            window_width / 2,
            100,
            text=f"Welcome {username_hr}!",
            font=("Helvetica", 28, "bold"),
            fill="white",
        )

    def on_window_resize_hr(this, event,username):
        # Handle window resize event
        this.resize_canvas_and_image_hr(username)

    def salary_management(this):
        #create a frame with clickable text
        salary_management_frame = tk.Toplevel()
        salary_management_frame.geometry("800x600")  # Set the window size
        salary_management_frame.title("Salary Management")
        
        # create a canvas that resizes with the window
        this.salary_management_canvas = tk.Canvas(salary_management_frame, bg="white", highlightthickness=0)
        this.salary_management_canvas.pack(fill=tk.BOTH, expand=True)
        
        # bind window resize event to function
        salary_management_frame.bind("<Configure>", lambda event: this.on_window_resize_salary_management(event))
        
        this.treeview = None
        
        # import the image as the background on the canvas
        this.load_image_salary_management()
        
        # create a scrollable frame
        this.scrollable_frame = tk.Frame(this.salary_management_canvas, bg="white")
        this.scrollable_frame.pack(fill=tk.BOTH, expand=True)
        this.scrollable_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # create a treeview to display the employees
        if this.treeview is None:
            this.treeview = ttk.Treeview(
                this.scrollable_frame, columns=("Employee",), show="headings", selectmode="browse"
            )
            this.treeview.heading("Employee", text="Employee")
            this.treeview.column("Employee", width=200, anchor="center")
            this.treeview.tag_configure("clickable", foreground="blue", font=("Helvetica", 12, "underline"))
            this.treeview.bind("<Double-1>", lambda event: this.open_employee_details_window(this.treeview.item(this.treeview.selection())["values"][0]))

            # Add a vertical scrollbar to the Treeview
            scrollbar = ttk.Scrollbar(this.scrollable_frame, orient="vertical", command=this.treeview.yview)
            scrollbar.pack(side="right", fill="y")
            this.treeview.configure(yscrollcommand=scrollbar.set)

            # Pack the Treeview to the scrollable frame
            this.treeview.pack(fill="both", expand=True)

        # Configure grid row and column weights
        this.scrollable_frame.grid_rowconfigure(0, weight=1)
        this.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Now you can safely use this.treeview
        this.treeview.delete(*this.treeview.get_children())
        
        # create a tick box for role of the employee
        role_label = tk.Label(
            this.salary_management_canvas,
            text="Role",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        role_label.pack(
            pady=20
        )
        # place it Extreme top middle
        role_label.place(relx=0.5, rely=0.1, anchor="center")
        this.role_entry_emp_mng = ttk.Combobox(
            this.salary_management_canvas, font=("Helvetica", 12, "bold")
        )
        this.role_entry_emp_mng["values"] = ("None","HR", "manager", "employee")
        this.role_entry_emp_mng.pack(
            pady=20
        )
        this.role_entry_emp_mng.place(relx=0.5, rely=0.2, anchor="center")
        this.role_entry_emp_mng.current(0)
        
        this.role_entry_emp_mng.bind("<<ComboboxSelected>>", this.role_selected)
        
        #Create a add login button to add the login of the employee
        add_login_button = tk.Button(
            this.salary_management_canvas,
            text="Add Login",
            command=lambda:this.add_login_from_hr_window(),
            font=("Helvetica", 14),
            width=15,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        add_login_button.place(relx=0.5, rely=0.9, anchor="s")
        #center the window
        this.center_window_all(salary_management_frame)
        
        #focus on window
        salary_management_frame.focus_force()
        
        #bind the escape key to the exit function
        salary_management_frame.bind("<Escape>", lambda event: salary_management_frame.destroy())
        
        # Run the main loop for the salary_management_frame
        salary_management_frame.mainloop()

    def role_selected(this, event):
        if this.role_entry_emp_mng is not None:
            selected_role = this.role_entry_emp_mng.get()
            if selected_role:
                this.populate_employee_list(selected_role)
        else:
            print("Role entry is None")

    def populate_employee_list(this, role):
        # Clear the existing items in the Treeview
        if this.treeview is not None:
            this.treeview.delete(*this.treeview.get_children())
        
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
            this.treeview.insert("", "end", values=(employee,), tags=("clickable",))

    def open_employee_details_window(this, employee_name):
        #Function to open another window with employee details
        employee_details_window = tk.Toplevel()
        employee_details_window.geometry("400x300")
        employee_details_window.title(f"Details for {employee_name}")
        employee_details_window.focus_force()
        
        #create a canvas that resizes with the window
        this.employee_details_canvas = tk.Canvas(employee_details_window, bg="white", highlightthickness=0)
        this.employee_details_canvas.pack(fill=tk.BOTH, expand=True)
        
        this.load_image_employee_details_new(employee_name)
        
        # bind window resize event to function
        employee_details_window.bind("<Configure>", lambda event: this.on_window_resize_employee_details_new(employee_name,event))
        
        #create a button to edit salary
        edit_salary_button = tk.Button(
            this.employee_details_canvas,
            text="Edit Salary",
            command=lambda:this.edit_salary(employee_name),
            font=("Helvetica", 14),
            width=15,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        edit_salary_button.place(relx=0.2, rely=0.9, anchor="s")
        
        #create an remove login button to remove the login of the employee
        remove_login_button = tk.Button(
            this.employee_details_canvas,
            text="Remove Login",
            command=lambda:this.remove_login(employee_name, employee_details_window),
            font=("Helvetica", 14),
            width=15,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        remove_login_button.place(relx=0.5, rely=0.9, anchor="s")
        
        #create an exit button in canvas and place at bottom middle
        exit_button = tk.Button(
        this.employee_details_canvas,
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
        this.center_window_all(employee_details_window)
        
        # Bind the Escape key to the exit function
        employee_details_window.bind("<Escape>", lambda event: this.handle_employee_details_window_exit(event, employee_details_window))
        
        # Run the main loop for the employee details window
        employee_details_window.mainloop()
        
    def load_image_add_login_from_hr(this):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        this.original_add_login_from_hr_image = Image.open(img_path)
        this.resize_canvas_and_image_add_login_from_hr()

    def resize_canvas_and_image_add_login_from_hr(this):
        # Get the create_hr window size
        window_width = this.add_login_from_hr_canvas.winfo_width()
        window_height = this.add_login_from_hr_canvas.winfo_height()

        # Resize the canvas to the current window size
        this.add_login_from_hr_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = this.original_add_login_from_hr_image.resize(
            (window_width, window_height)
        )
        this.add_login_from_hr_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        this.add_login_from_hr_canvas.delete("all")
        this.add_login_from_hr_canvas.create_image(
            0, 0, image=this.add_login_from_hr_image, anchor="nw"
        )

    def on_window_resize_add_login_from_hr(this, event):
        # Handle window resize event
        this.resize_canvas_and_image_add_login_from_hr()
        
    def add_login_from_hr_window(this):
        # Create a new window
        add_login_from_hr_window = tk.Toplevel()
        add_login_from_hr_window.geometry("800x600")  # Set the window size
        add_login_from_hr_window.title("Add Login")

        # Create a canvas that resizes with the window
        this.add_login_from_hr_canvas = tk.Canvas(add_login_from_hr_window, bg="white", highlightthickness=0)
        this.add_login_from_hr_canvas.pack(fill=tk.BOTH, expand=True)

        # Import the image as the background on the canvas
        this.load_image_add_login_from_hr()

        # Bind window resize event to function
        add_login_from_hr_window.bind("<Configure>", lambda event: this.on_window_resize_add_login_from_hr(event))

        # focus on window
        add_login_from_hr_window.focus_force()
        # Center the window with function center_window_test
        this.center_window_all(add_login_from_hr_window)

        # Create a new entry for username on canvas
        username_label = tk.Label(
            this.add_login_from_hr_canvas,
            text="Username",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        username_label.pack(pady=10)
        username_label.place(relx=0.3, rely=0.2, anchor="center")
        this.username_entry = tk.Entry(
            this.add_login_from_hr_canvas, font=("Helvetica", 12)
        )
        this.username_entry.pack(pady=10)
        this.username_entry.place(relx=0.7, rely=0.2, anchor="center")
        this.username_entry.insert(0, "")

        # Create a new entry for password on canvas
        password_label = tk.Label(
            this.add_login_from_hr_canvas,
            text="Password",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        password_label.pack(pady=10)
        password_label.place(relx=0.3, rely=0.3, anchor="center")
        this.password_entry = tk.Entry(
            this.add_login_from_hr_canvas, show="*", font=("Helvetica", 12)
        )
        this.password_entry.pack(pady=10)
        this.password_entry.place(relx=0.7, rely=0.3, anchor="center")
        this.password_entry.insert(0, "")

        # Create a new checkbox for role with options- manager, employee on canvas
        role_label = tk.Label(
            this.add_login_from_hr_canvas,
            text="Role",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        role_label.pack(pady=10)
        role_label.place(relx=0.3, rely=0.4, anchor="center")
        this.role_entry = ttk.Combobox(
            this.add_login_from_hr_canvas, font=("Helvetica", 12), state="readonly"
        )
        this.role_entry["values"] = ("manager", "employee")
        this.role_entry.current(0)
        this.role_entry.pack(pady=10)
        this.role_entry.place(relx=0.7, rely=0.4, anchor="center")

        # Create an entry for new salary and designation
        this.new_salary_label = tk.Label(
            this.add_login_from_hr_canvas,
            text="New Salary",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        this.new_salary_label.pack(pady=10)
        this.new_salary_label.place(relx=0.3, rely=0.5, anchor="center")
        this.new_salary_label = tk.Entry(
            this.add_login_from_hr_canvas, font=("Helvetica", 12)
        )
        this.new_salary_label.pack(pady=10)
        this.new_salary_label.place(relx=0.7, rely=0.5, anchor="center")
        this.new_salary_label.insert(0, "")

        this.new_designation_label = tk.Label(
            this.add_login_from_hr_canvas,
            text="New Designation",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        this.new_designation_label.pack(pady=10)
        this.new_designation_label.place(relx=0.3, rely=0.6, anchor="center")
        this.new_designation_label = tk.Entry(
            this.add_login_from_hr_canvas, font=("Helvetica", 12)
        )
        this.new_designation_label.pack(pady=10)
        this.new_designation_label.place(relx=0.7, rely=0.6, anchor="center")
        this.new_designation_label.insert(0, "")

        # Create a new button for adding the new login on canvas
        add_button = tk.Button(
            this.add_login_from_hr_canvas,
            text="Add",
            command=lambda: this.add_login_to_database_hr_window(add_login_from_hr_window),
            font=("Helvetica", 14),
        )
        add_button.pack(pady=20)
        add_button.place(relx=0.5, rely=0.8, anchor="center", width=100, height=30)

        # Bind the Enter key to the submit button
        add_login_from_hr_window.bind(
            "<Return>", lambda event: this.add_login_to_database_hr_window(add_login_from_hr_window)
        )

        # Bind the Escape key to the exit function
        add_login_from_hr_window.bind(
            "<Escape>", lambda event: add_login_from_hr_window.destroy()
        )
        # Run the main loop for the add_login_from_hr_window
        add_login_from_hr_window.mainloop()

    def add_login_to_database_hr_window(this, add_login_from_hr_window):
        username = this.username_entry.get()
        password = this.password_entry.get()
        role = this.role_entry.get()
        designation = this.new_designation_label.get()
        salary = this.new_salary_label.get()

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
                        "salary": salary,
                        "emp_ids": emp_uni + 1,
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
                        "salary": salary,
                        "sick_days": 0,
                        "vacation_days": 0,
                        "bonus": 0,
                        "hours_attended": 0,
                        "apply_for_resignation": "",
                        "apply_for_vacation": 0,
                        "progress_on_task": 0,
                        "survey": db.reference("survey_uni").child("available").get(),
                        "feedback": "",
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
        this.salary_management_canvas.focus_force()
            
    def remove_login(this, employee_name, employee_details_window):
        #Function to remove the login of the employee or manager
        if messagebox.askyesno("Remove Login", f"Are you sure you want to remove the login of {employee_name}?"):
            #Remove the login from the database
            if db.reference("/employee").child(employee_name).get() is not None:
                db.reference("/employee").child(employee_name).delete()
            elif db.reference("/manager").child(employee_name).get() is not None:
                db.reference("/manager").child(employee_name).delete()
            messagebox.showinfo("Remove Login", "Login removed successfully.")
        #Close the window
        employee_details_window.destroy()
        this.salary_management_canvas.focus_force()
        
    def handle_employee_details_window_exit(this, event, employee_details_window):
        if hasattr(this, "salary_management_canvas") and this.salary_management_canvas.winfo_exists():
            this.salary_management_canvas.focus_force()
            
    def edit_salary(this, employee_name):
        #Create a window to edit the salary of the employee
        edit_salary_window = tk.Toplevel()
        edit_salary_window.geometry("400x300")
        edit_salary_window.title(f"Edit Salary for {employee_name}")
        
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
        new_salary_label.place(relx=0.5, rely=0.3, anchor="center")
        
        #Create an entry for the new salary
        this.new_salary_entry = tk.Entry(
            edit_salary_window, font=("Helvetica", 12, "bold")
        )
        this.new_salary_entry.pack(
            pady=20
        )
        this.new_salary_entry.place(relx=0.5, rely=0.4, anchor="center")
        this.new_salary_entry.insert(0, "")
        #create a submit button to change the salary
        submit_button = tk.Button(
            edit_salary_window,
            text="Submit",
            command=lambda:this.new_submit_salary(employee_name, edit_salary_window),
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
        edit_salary_window.bind("<Return>", lambda event: this.new_submit_salary(employee_name, edit_salary_window))
        
        #bind the escape key to the exit function
        edit_salary_window.bind("<Escape>", lambda event: edit_salary_window.destroy())
        
        #center the window
        this.center_window_all(edit_salary_window)
        
        #focus on window
        edit_salary_window.focus_force()
        
        # Run the main loop for the edit_salary_window
        edit_salary_window.mainloop()
        
    def new_submit_salary(this, employee_name, edit_salary_window):
        #Get the new salary from the entry
        new_salary = this.new_salary_entry.get()
        #Ask for confirmation 
        if messagebox.askyesno("Confirm", f"Are you sure you want to change the salary of {employee_name} to {new_salary}?"):
            #Change the salary in the database
            db.reference("/employee").child(employee_name).child("salary").set(new_salary)
        #Close the window
        edit_salary_window.destroy()
        #focus on the salary management window
        this.employee_details_canvas.focus_force()

    def load_image_employee_details_new(this,employee_name):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        this.original_employee_details_image = Image.open(img_path)
        this.resize_canvas_and_image_employee_details_new(employee_name)
        
    def resize_canvas_and_image_employee_details_new(this,employee_name):
        # Get the employee details window size
        window_width = this.employee_details_canvas.winfo_width()
        window_height = this.employee_details_canvas.winfo_height()

        # Resize the canvas to the current window size
        this.employee_details_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = this.original_employee_details_image.resize(
            (window_width, window_height)
        )
        this.employee_details_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        this.employee_details_canvas.delete("all")
        this.employee_details_canvas.create_image(
            0, 0, image=this.employee_details_image, anchor="nw"
        )
        
        #create text with employee name, role, salary, hours attended, bonus
        employee_details_text="Employee Name: "+str(employee_name)+"\nRole: "+str(db.reference("/employee").child(employee_name).child("role").get())+"\nSalary: "+str(db.reference("/employee").child(employee_name).child("salary").get())+"\nHours Attended: "+str(db.reference("/employee").child(employee_name).child("hours_attended").get())+"\nBonus: "+str(db.reference("/employee").child(employee_name).child("bonus").get())
        this.employee_details_canvas.create_text(
            window_width / 2,
            window_height / 2,
            text=employee_details_text,
            font=("Helvetica", 14, "bold"),
            fill="white",
            tag="employee_details_text"
        )

    def on_window_resize_employee_details_new(this,employee_name, event):
        # Handle window resize event
        this.resize_canvas_and_image_employee_details_new(employee_name)
        
    def load_image_salary_management(this):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        this.original_salary_management_image = Image.open(img_path)
        this.resize_canvas_and_image_salary_management()

    def resize_canvas_and_image_salary_management(this):
        # Get the salary_management window size
        window_width = this.salary_management_canvas.winfo_width()
        window_height = this.salary_management_canvas.winfo_height()

        # Resize the canvas to the current window size
        this.salary_management_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = this.original_salary_management_image.resize(
            (window_width, window_height)
        )
        this.salary_management_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        this.salary_management_canvas.delete("all")
        this.salary_management_canvas.create_image(
            0, 0, image=this.salary_management_image, anchor="nw"
        )

    def on_window_resize_salary_management(this, event):
        # Handle window resize event
        this.resize_canvas_and_image_salary_management()

    def approve_bonus(this):
        #Create a window to approve the bonus of the employee
        approve_bonus_window = tk.Toplevel()
        approve_bonus_window.geometry("400x300")
        approve_bonus_window.title("Approve Bonus")
        
        #Create a canvas that resizes with the window
        this.approve_bonus_canvas = tk.Canvas(approve_bonus_window, bg="white", highlightthickness=0)
        this.approve_bonus_canvas.pack(fill=tk.BOTH, expand=True)
        
        #Load the image as the background on the canvas
        this.load_image_approve_bonus()
        
        #Bind window resize event to function
        approve_bonus_window.bind("<Configure>", lambda event: this.on_window_resize_approve_bonus(event))

        #Center the window with function center_window_test
        this.center_window_all(approve_bonus_window)
        
        #focus on window
        approve_bonus_window.focus_force()
        
        this.treeview_bonus = None
        
        # create a scrollable frame
        this.scrollable_frame_bonus = tk.Frame(this.approve_bonus_canvas, bg="white")
        this.scrollable_frame_bonus.pack(fill=tk.BOTH, expand=True)
        this.scrollable_frame_bonus.place(relx=0.5, rely=0.5, anchor="center")
        
        # create a treeview to display the employees
        if this.treeview_bonus is None:
            this.treeview_bonus = ttk.Treeview(
                this.scrollable_frame_bonus, columns=("Employee",), show="headings", selectmode="browse"
            )
            this.treeview_bonus.heading("Employee", text="Employee")
            #Create columns for name,bonus amount,if role is employee then add a column for reason,hours attended,and 2 buttons for approve and deny
            this.treeview_bonus["columns"] = ("Employee", "Bonus", "Reason", "Hours Attended")
            this.treeview_bonus.column("Employee", width=100, anchor="center")
            this.treeview_bonus.column("Bonus", width=100, anchor="center")
            this.treeview_bonus.column("Reason", width=100, anchor="center")
            this.treeview_bonus.column("Hours Attended", width=100, anchor="center")
            this.treeview_bonus.heading("Employee", text="Employee")
            this.treeview_bonus.heading("Bonus", text="Bonus")
            this.treeview_bonus.heading("Reason", text="Reason")
            this.treeview_bonus.heading("Hours Attended", text="Hours Attended")
            this.treeview_bonus.tag_configure("selectable", foreground="blue", font=("Helvetica", 12, "underline"))
            # this.treeview_bonus.bind("<Double-1>", lambda event: this.open_employee_details_window(this.treeview_bonus.item(this.treeview_bonus.selection())["values"][0]))
            
            # Add a vertical scrollbar to the Treeview
            scrollbar_bonus_y = ttk.Scrollbar(this.scrollable_frame_bonus, orient="vertical", command=this.treeview_bonus.yview)
            scrollbar_bonus_y.pack(side="right", fill="y")
            this.treeview_bonus.configure(yscrollcommand=scrollbar_bonus_y.set)
            
            # Add a horizontal scrollbar to the Treeview
            scrollbar_bonus_x = ttk.Scrollbar(this.scrollable_frame_bonus, orient="horizontal", command=this.treeview_bonus.xview)
            scrollbar_bonus_x.pack(side="bottom", fill="x")
            this.treeview_bonus.configure(xscrollcommand=scrollbar_bonus_x.set)

            # Pack the Treeview to the scrollable frame
            this.treeview_bonus.pack(fill="both", expand=True)

        # bind the treeview select event to function
        this.treeview_bonus.bind("<<TreeviewSelect>>", this.on_treeview_select)
        
        #Create 2 buttons for approve and deny that are disabled by default and enabled when a row is selected
        this.approve_bonus_button = tk.Button(
            this.approve_bonus_canvas,
            text="Approve Bonus",
            command=lambda:this.approve_bonus_btn(),
            font=("Helvetica", 14),
            width=15,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        this.approve_bonus_button.place(relx=0.3, rely=0.9, anchor="s")
        this.approve_bonus_button["state"] = "disabled"
        
        this.deny_bonus_button = tk.Button(
            this.approve_bonus_canvas,
            text="Deny Bonus",
            command=lambda:this.deny_bonus_btn(),
            font=("Helvetica", 14),
            width=15,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        this.deny_bonus_button.place(relx=0.7, rely=0.9, anchor="s")
        this.deny_bonus_button["state"] = "disabled"
        
        # Configure grid row and column weights
        this.scrollable_frame_bonus.grid_rowconfigure(0, weight=1)
        this.scrollable_frame_bonus.grid_columnconfigure(0, weight=1)

        # Now you can safely use this.treeview
        this.treeview_bonus.delete(*this.treeview_bonus.get_children())
        
        # create a tick box for role of the employee
        role_entry_bonus_label = tk.Label(
            this.approve_bonus_canvas,
            text="Role",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        role_entry_bonus_label.pack(
            pady=20
        )
        # place it Extreme top middle
        role_entry_bonus_label.place(relx=0.5, rely=0.1, anchor="center")
        this.role_entry_bonus = ttk.Combobox(
            this.approve_bonus_canvas, font=("Helvetica", 12, "bold")
        )
        this.role_entry_bonus["values"] = ("None", "manager", "employee")
        this.role_entry_bonus.pack(
            pady=20
        )
        this.role_entry_bonus.place(relx=0.5, rely=0.2, anchor="center")
        this.role_entry_bonus.current(0)
        
        this.role_entry_bonus.bind("<<ComboboxSelected>>", this.role_selected_bonus)
        
        #Bind the escape key to the exit function
        approve_bonus_window.bind("<Escape>", lambda event: approve_bonus_window.destroy())
        
        #Run the main loop for the approve_bonus_window
        approve_bonus_window.mainloop()
            
    def on_treeview_select(this, event):
        selected_items = this.treeview_bonus.selection()
        if selected_items:
            # Enable buttons if a row is selected
            this.approve_bonus_button["state"] = "normal"
            this.deny_bonus_button["state"] = "normal"
        else:
            # Disable buttons if no row is selected
            this.approve_bonus_button["state"] = "disabled"
            this.deny_bonus_button["state"] = "disabled"
        
    def role_selected_bonus(this, event):
        if this.role_entry_bonus is not None:
            selected_role = this.role_entry_bonus.get()
            if selected_role:
                this.populate_employee_list_bonus(selected_role)
        else:
            print("Role entry is None")
            
    def populate_employee_list_bonus(this, role):
        # Clear the existing items in the Treeview
        if this.treeview_bonus is not None:
            this.treeview_bonus.delete(*this.treeview_bonus.get_children())
        
        if role == "manager":
            employees = list(( db.reference("/manager").get()).keys())

        elif role == "None":
            return
        else:
            employees= this.get_employee_data_with_non_zero_bonus()
        #   #Get only the keys of the employees that have a non zero bonus
        #     employees = list(( db.reference("/employee").get()).keys())
        #     employees_with_bonus = []
        #     for employee in employees:
        #         if db.reference("/employee").child(employee).child("bonus").get() != 0 and db.reference("/employee").child(employee).child("bonus").get() != "":
        #             employees_with_bonus.append(employee)
        #     employees = employees_with_bonus


        #employees = employees_with_bonus
        #print(employees)
        # Populate the Treeview with employee names
        for employee in employees:
            # Add the employee name, bonus amount, reason, hours attended with tag selectable

            # this.treeview_bonus.insert("", "end", values=(employee, db.reference("/employee").child(employee).child("bonus_req").get(), db.reference("/employee").child(employee).child("bonus_reason").get(), db.reference("/employee").child(employee).child("hours_attended").get()), tags=("clickable",))
            
            this.treeview_bonus.insert("", "end", values=(
                employee,
                db.reference("/employee").child(employee).child("bonus_req").get(),
                db.reference("/employee").child(employee).child("bonus_reason").get(),
                db.reference("/employee").child(employee).child("hours_attended").get()
            ), tags=("selectable",))

    def get_employee_data_with_non_zero_bonus(this):
        emp_ref = db.reference("/employee")
        employee_data = [user for user in emp_ref.get() if this.get_employee_data(user, "bonus_req") > 0]
        return employee_data


    def get_employee_data(self, username, data_type):
        emp_ref = db.reference("/employee")
        data = emp_ref.child(username).child(data_type).get()
        return data if data is not None else 0
    
    def approve_bonus_btn(this):
        messagebox.showinfo("HR Window", "Approve Bonus Button Pressed")
        
    def deny_bonus_btn(this):
        messagebox.showinfo("HR Window", "Deny Bonus Button Pressed")
        
    def load_image_approve_bonus(this):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        this.original_approve_bonus_image = Image.open(img_path)
        this.resize_canvas_and_image_approve_bonus()
                
    def resize_canvas_and_image_approve_bonus(this):
        # Get the approve_bonus window size
        window_width = this.approve_bonus_canvas.winfo_width()
        window_height = this.approve_bonus_canvas.winfo_height()

        # Resize the canvas to the current window size
        this.approve_bonus_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = this.original_approve_bonus_image.resize(
            (window_width, window_height)
        )
        this.approve_bonus_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        this.approve_bonus_canvas.delete("all")
        this.approve_bonus_canvas.create_image(
            0, 0, image=this.approve_bonus_image, anchor="nw"
        )
        
    def on_window_resize_approve_bonus(this, event):
        # Handle window resize event
        this.resize_canvas_and_image_approve_bonus()

    def approve_resignation(this):
        #Create a window to approve the resignation of the employee
        approve_resignation_window = tk.Toplevel()
        approve_resignation_window.geometry("400x300")
        approve_resignation_window.title("Approve Resignation")
        
        #Create a canvas that resizes with the window
        this.approve_resignation_canvas = tk.Canvas(approve_resignation_window, bg="white", highlightthickness=0)
        this.approve_resignation_canvas.pack(fill=tk.BOTH, expand=True)

        #Load the image as the background on the canvas
        this.load_image_approve_resignation()
        
        #Bind window resize event to function
        approve_resignation_window.bind("<Configure>", lambda event: this.on_window_resize_approve_resignation(event))
        
        #Center the window with function center_window_test
        this.center_window_all(approve_resignation_window)
        
        #focus on window
        approve_resignation_window.focus_force()
        
        this.treeview_resignation = None
        
        # create a scrollable frame
        this.scrollable_frame_resignation = tk.Frame(this.approve_resignation_canvas, bg="white")
        this.scrollable_frame_resignation.pack(fill=tk.BOTH, expand=True)
        this.scrollable_frame_resignation.place(relx=0.5, rely=0.5, anchor="center")
        
        # create a treeview to display the employees
        if this.treeview_resignation is None:
            this.treeview_resignation = ttk.Treeview(
                this.scrollable_frame_resignation, columns=("Employee",), show="headings", selectmode="browse"
            )
            this.treeview_resignation.heading("Employee", text="Employee")
            #Create columns for name,reason,if role is employee then add a column for hours attended and a button for approve
            this.treeview_resignation["columns"] = ("Employee", "Reason")
            this.treeview_resignation.column("Employee", width=100, anchor="center")
            this.treeview_resignation.column("Reason", width=100, anchor="center")
            this.treeview_resignation.heading("Employee", text="Employee")
            this.treeview_resignation.heading("Reason", text="Reason")
            this.treeview_resignation.tag_configure("selectable", foreground="blue", font=("Helvetica", 12, "underline"))
            # this.treeview_resignation.bind("<Double-1>", lambda event: this.open_employee_details_window(this.treeview_resignation.item(this.treeview_resignation.selection())["values"][0]))
            
            # Add a vertical scrollbar to the Treeview
            scrollbar_resignation_y = ttk.Scrollbar(this.scrollable_frame_resignation, orient="vertical", command=this.treeview_resignation.yview)
            scrollbar_resignation_y.pack(side="right", fill="y")
            this.treeview_resignation.configure(yscrollcommand=scrollbar_resignation_y.set)
            
            # Add a horizontal scrollbar to the Treeview
            scrollbar_resignation_x = ttk.Scrollbar(this.scrollable_frame_resignation, orient="horizontal", command=this.treeview_resignation.xview)
            scrollbar_resignation_x.pack(side="bottom", fill="x")
            this.treeview_resignation.configure(xscrollcommand=scrollbar_resignation_x.set)

            # Pack the Treeview to the scrollable frame
            this.treeview_resignation.pack(fill="both", expand=True)
            
        # bind the treeview select event to function
        this.treeview_resignation.bind("<<TreeviewSelect>>", this.on_treeview_select_resignation)
        
        #Populate the list with who applied for resignation, execute only once
        this.populate_employee_list_resignation()

        #Create 2 buttons for approve and deny that are disabled by default and enabled when a row is selected
        this.approve_resignation_button = tk.Button(
            this.approve_resignation_canvas,
            text="Approve Resignation",
            command=lambda:this.approve_resignation_btn(),
            font=("Helvetica", 14),
            width=20,
            height=2,
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        this.approve_resignation_button.place(relx=0.5, rely=0.9, anchor="s")
        this.approve_resignation_button["state"] = "disabled"
        
        # Configure grid row and column weights
        this.scrollable_frame_resignation.grid_rowconfigure(0, weight=1)
        this.scrollable_frame_resignation.grid_columnconfigure(0, weight=1)
                
        #Bind the escape key to the exit function
        approve_resignation_window.bind("<Escape>", lambda event: approve_resignation_window.destroy())
        
        #Run the main loop for the approve_resignation_window
        approve_resignation_window.mainloop()
        
    def on_treeview_select_resignation(this, event):
        selected_items = this.treeview_resignation.selection()
        if selected_items:
            # Enable buttons if a row is selected
            this.approve_resignation_button["state"] = "normal"
        else:
            # Disable buttons if no row is selected
            this.approve_resignation_button["state"] = "disabled"
        
    def populate_employee_list_resignation(this):
        # Clear the existing items in the Treeview
        if this.treeview_resignation is not None:
            this.treeview_resignation.delete(*this.treeview_resignation.get_children())
        
        #Get only the keys of the employees,managers that have applied for resignation
        employees = list(( db.reference("/employee").get()).keys())
        managers = list(( db.reference("/manager").get()).keys())
        employees_with_resignation = []
        managers_with_resignation = []
        for employee in employees:
            #check if apply_fpr_resignation value exists and is not empty
            if db.reference("/employee").child(employee).child("apply_for_resignation").get() != "":
                employees_with_resignation.append(employee)
        for manager in managers:
            if db.reference("/manager").child(manager).child("apply_for_resignation").get() != "":
                managers_with_resignation.append(manager)
        #add the employees and managers to the list
        employees = employees_with_resignation + managers_with_resignation

        # Populate the Treeview with employee names
        for person in employees:
            # Determine if the person is an employee or a manager
            if person in employees_with_resignation:
                reason = db.reference("/employee").child(person).child("reason").get()
            else:
                reason = db.reference("/manager").child(person).child("reason").get()
            #Add the employee name,reason with tag selectable
            this.treeview_resignation.insert("", "end", values=(person, reason), tags=("clickable",))
            
    def approve_resignation_btn(this):
        messagebox.showinfo("HR Window", "Approve Resignation Button Pressed")
        
    def deny_resignation_btn(this):
        messagebox.showinfo("HR Window", "Deny Resignation Button Pressed")

    def load_image_approve_resignation(this):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        this.original_approve_resignation_image = Image.open(img_path)
        this.resize_canvas_and_image_approve_resignation()
        
    def resize_canvas_and_image_approve_resignation(this):
        # Get the approve_resignation window size
        window_width = this.approve_resignation_canvas.winfo_width()
        window_height = this.approve_resignation_canvas.winfo_height()

        # Resize the canvas to the current window size
        this.approve_resignation_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = this.original_approve_resignation_image.resize(
            (window_width, window_height)
        )
        this.approve_resignation_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        this.approve_resignation_canvas.delete("all")
        this.approve_resignation_canvas.create_image(
            0, 0, image=this.approve_resignation_image, anchor="nw"
        )
        
    def on_window_resize_approve_resignation(this, event):
        # Handle window resize event
        this.resize_canvas_and_image_approve_resignation()

    def check_hours_attended(this):
        messagebox.showinfo("HR Window", "Check Employee Hours Attended Button Pressed")

    def survey_feedback(this):
        messagebox.showinfo("HR Window", "Survey/Feedback Button Pressed")

    # def create_all_hr(this):
    #     # create a new window
    #     create_remove_hr_window = tk.Toplevel()
    #     create_remove_hr_window.geometry("800x600")  # Set the window size
    #     create_remove_hr_window.title("Create manager/Employee Login")

    #     #create a canvas that resizes with the window
    #     this.create_be_logo_canvas = tk.Canvas(create_remove_hr_window, bg="white", highlightthickness=0)
    #     this.create_be_logo_canvas.pack(fill=tk.BOTH, expand=True)

    #     # bind window resize event to function
    #     create_remove_hr_window.bind("<Configure>", lambda event: this.on_window_resize_create_be(event))

    #     # import the image as the background on the canvas
    #     this.load_image_create_be()

    #     #create a new entry for username on canvas
    #     username_label = tk.Label(
    #         this.create_be_logo_canvas,
    #         text="Username",
    #         font=("Helvetica", 12, "bold"),
    #         bg="white",
    #     )
    #     username_label.pack(
    #         pady=20
    #     )
    #     username_label.place(relx=0.5, rely=0.35, anchor="center")
    #     this.username_entry = tk.Entry(
    #         this.create_be_logo_canvas, font=("Helvetica", 12, "bold")
    #     )
    #     this.username_entry.pack(
    #         pady=20
    #     )
    #     this.username_entry.place(relx=0.5, rely=0.4, anchor="center")
    #     this.username_entry.insert(0, "")
    #     # create a new entry for password on canvas
    #     password_label = tk.Label(
    #         this.create_be_logo_canvas,
    #         text="Password",
    #         font=("Helvetica", 12, "bold"),
    #         bg="white",
    #     )
    #     password_label.pack(
    #         pady=20
    #     )
    #     password_label.place(relx=0.5, rely=0.5, anchor="center")
    #     this.password_entry = tk.Entry(

    #         this.create_be_logo_canvas, show="", font=("Helvetica", 12, "bold")
    #     )
    #     this.password_entry.pack(
    #         pady=20
    #     )
    #     this.password_entry.place(relx=0.5, rely=0.55, anchor="center")
    #     this.password_entry.insert(0, "")
    #     # create a checkbox for role with options- HR, manager, employee on canvas
    #     role_label = tk.Label(
    #         this.create_be_logo_canvas,
    #         text="Role",
    #         font=("Helvetica", 12, "bold"),
    #         bg="white",
    #     )
    #     role_label.pack(
    #         pady=20
    #     )
    #     role_label.place(relx=0.5, rely=0.65, anchor="center")
    #     this.role_entry = ttk.Combobox(
    #         this.create_be_logo_canvas, font=("Helvetica", 12, "bold")
    #     )
    #     this.role_entry["values"] = ("manager", "employee")
    #     this.role_entry.pack(
    #         pady=20
    #     )
    #     this.role_entry.place(relx=0.5, rely=0.7, anchor="center")
    #     this.role_entry.current(0)
    #     # create a new button for adding the new login on canvas
    #     add_button = tk.Button(
    #         this.create_be_logo_canvas,
    #         text="Add",
    #         command=this.add_login_to_database,
    #         font=("Helvetica", 14),
    #     )
    #     add_button.pack(
    #         pady=20
    #     )
    #     add_button.place(relx=0.5, rely=0.8, anchor="center", width=100, height=30)
    #     # store the values in 3 variables when the button is pressed
    #     add_button.bind(
    #         "<Button-1>",
    #         lambda event: this.add_login_to_database(create_remove_hr_window),
    #     )
    #     # Bind the Escape key to the exit function
    #     create_remove_hr_window.bind(
    #         "<Escape>", lambda event: create_remove_hr_window.destroy()
    #     )
    #     # focus on window
    #     create_remove_hr_window.focus_force()
    #     # Center the window with function center_window_test
    #     this.center_window_all(create_remove_hr_window)
    #     # Run the main loop for the create_remove_hr_window
    #     create_remove_hr_window.mainloop()

    # def load_image_create_be(this):
    #     # Construct the full path to the image file based on role and username
    #     img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

    #     # Load image and adjust canvas size
    #     this.original_create_be_logo_image = Image.open(img_path)
    #     this.resize_canvas_and_image_create_be()

    # def resize_canvas_and_image_create_be(this):
    #     # Get the create_be window size
    #     window_width = this.create_be_logo_canvas.winfo_width()
    #     window_height = this.create_be_logo_canvas.winfo_height()

    #     # Resize the canvas to the current window size
    #     this.create_be_logo_canvas.config(width=window_width, height=window_height)

    #     # Resize the image if needed
    #     resized_image = this.original_create_be_logo_image.resize(
    #         (window_width, window_height)
    #     )
    #     this.create_be_logo_image = ImageTk.PhotoImage(resized_image)

    #     # Update the image on the canvas
    #     this.create_be_logo_canvas.delete("all")
    #     this.create_be_logo_canvas.create_image(
    #         0, 0, image=this.create_be_logo_image, anchor="nw"
    #     )

    # def on_window_resize_create_be(this, event):
    #     # Handle window resize event
    #     this.resize_canvas_and_image_create_be()

    # def remove_all_hr(this):
    #     # create a new window
    #     create_remove_hr_window = tk.Toplevel()
    #     create_remove_hr_window.geometry("800x600")  # Set the window size
    #     create_remove_hr_window.title("Remove manager/Employee Login")
        
    #     #create a canvas that resizes with the window
    #     this.remove_be_logo_canvas = tk.Canvas(create_remove_hr_window, bg="white", highlightthickness=0)
    #     this.remove_be_logo_canvas.pack(fill=tk.BOTH, expand=True)

    #     # bind window resize event to function
    #     create_remove_hr_window.bind("<Configure>", lambda event: this.on_window_resize_remove_be(event))

    #     # import the image as the background on the canvas
    #     this.load_image_remove_be()

    #     #create a new entry for username on canvas
    #     username_label = tk.Label(
    #         this.remove_be_logo_canvas,
    #         text="Username",
    #         font=("Helvetica", 12, "bold"),
    #         bg="white",
    #     )
    #     username_label.pack(
    #         pady=20
    #     )
    #     username_label.place(relx=0.5, rely=0.35, anchor="center")

    #     this.username_entry = tk.Entry(

    #         this.remove_be_logo_canvas, font=("Helvetica", 12, "bold")
    #     )
    #     this.username_entry.pack(
    #         pady=20
    #     )
    #     this.username_entry.place(relx=0.5, rely=0.4, anchor="center")
    #     this.username_entry.insert(0, "")
    #     # create a checkbox for role with options- HR, manager, employee on canvas
    #     role_label = tk.Label(
    #         this.remove_be_logo_canvas,
    #         text="Role",
    #         font=("Helvetica", 12, "bold"),
    #         bg="white",
    #     )
    #     role_label.pack(
    #         pady=20
    #     )
    #     role_label.place(relx=0.5, rely=0.5, anchor="center")
    #     this.role_entry = ttk.Combobox(
    #         this.remove_be_logo_canvas, font=("Helvetica", 12, "bold")
    #     )
    #     this.role_entry["values"] = ("manager", "employee")
    #     this.role_entry.pack(
    #         pady=20
    #     )
    #     this.role_entry.place(relx=0.5, rely=0.55, anchor="center")
    #     this.role_entry.current(0)
    #     # create a new button for removing the login on canvas
    #     remove_button = tk.Button(
    #         this.remove_be_logo_canvas,
    #         text="Remove",
    #         command=this.remove_login_from_database,
    #         font=("Helvetica", 14),
    #     )
    #     remove_button.pack(
    #         pady=20
    #     )
    #     remove_button.place(relx=0.5, rely=0.65, anchor="center", width=100, height=30)
    #     # store the values in 2 variables when the button is pressed
    #     remove_button.bind(

    #         "<Button-1>",
    #         lambda event: this.remove_login_from_database(create_remove_hr_window),
    #     )
    #     # Bind the Escape key to the exit function
    #     create_remove_hr_window.bind(
    #         "<Escape>", lambda event: create_remove_hr_window.destroy()
    #     )
    #     # focus on window
    #     create_remove_hr_window.focus_force()
    #     # Center the window with function center_window_test
    #     this.center_window_all(create_remove_hr_window)
    #     # Run the main loop for the create_remove_hr_window
    #     create_remove_hr_window.mainloop()

    # def load_image_remove_be(this):
    #     # Construct the full path to the image file based on role and username
    #     img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

    #     # Load image and adjust canvas size
    #     this.original_remove_be_logo_image = Image.open(img_path)
    #     this.resize_canvas_and_image_remove_be()

    # def resize_canvas_and_image_remove_be(this):
    #     # Get the remove_be window size
    #     window_width = this.remove_be_logo_canvas.winfo_width()
    #     window_height = this.remove_be_logo_canvas.winfo_height()

    #     # Resize the canvas to the current window size
    #     this.remove_be_logo_canvas.config(width=window_width, height=window_height)

    #     # Resize the image if needed
    #     resized_image = this.original_remove_be_logo_image.resize(
    #         (window_width, window_height)
    #     )
    #     this.remove_be_logo_image = ImageTk.PhotoImage(resized_image)

    #     # Update the image on the canvas
    #     this.remove_be_logo_canvas.delete("all")
    #     this.remove_be_logo_canvas.create_image(
    #         0, 0, image=this.remove_be_logo_image, anchor="nw"
    #     )

    # def on_window_resize_remove_be(this, event):
    #     # Handle window resize event
    #     this.resize_canvas_and_image_remove_be()
        

def main(role,username):
    # Create a new window
    hr=HR_class()
    hr.open_hr_window(role,username)
