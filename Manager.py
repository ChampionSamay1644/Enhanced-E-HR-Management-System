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

class Manager_class:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Manager Window")
        
    def getdata(self,username,role):
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
            list.append(manager_ref.child(username).child("manager_id").get())
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
            list.append(hr_ref.child(username).child("hr_id").get())
            list.append(hr_ref.child(username).child("designation").get())
            list.append(hr_ref.child(username).child("salary").get())
            list.append(hr_ref.child(username).child("hours_attended").get())
            list.append(hr_ref.child(username).child("bonus").get())
            list.append(hr_ref.child(username).child("sick_days").get())
            list.append(hr_ref.child(username).child("vacation_days").get())
            
            return list
    
    def open_manager_window(self, role, username):
        if hasattr(self, "root"):
            try:
                if self.root.winfo_exists():
                    self.root.destroy()  # Close the main login window
            except:
                pass    
        manager_window = tk.Tk()  # Use Tk() to create a new window
        manager_window.geometry("900x600")  # Set the window size
        manager_window.title("Manager Window")

        #create a canvas that resizes with the window
        self.manager_logo_canvas = tk.Canvas(manager_window, bg="white", highlightthickness=0)
        self.manager_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # import the image as the background on the canvas
        self.load_image_manager(username)

        # bind window resize event to function
        manager_window.bind("<Configure>", lambda event: self.on_window_resize_manager(event,username))

        #buttons of manager window
        self.perform_review_approval_button = tk.Button(
            self.manager_logo_canvas, text="Performance Review Approval", command=lambda:self.perform_review_approval(), font=("Helvetica", 14)
        )
        self.perform_review_approval_button.pack(
            pady=20
        )
        self.perform_review_approval_button.place(
            relx=0.5, rely=0.3, anchor="center", width=300, height=30
        )
        self.approve_vacations_sick_leaves_button = tk.Button(
            self.manager_logo_canvas, text="Approve Vacations and Sick Leaves", command=lambda:self.approve_vacations_sick_leaves(username,role), font=("Helvetica", 14)
        )
        self.approve_vacations_sick_leaves_button.pack(
            pady=20
        )
        self.approve_vacations_sick_leaves_button.place(
            relx=0.5, rely=0.4, anchor="center", width=320, height=30
        )
        self.progress_on_task_button = tk.Button(
            self.manager_logo_canvas, text="Progress on Task", command=lambda:self.progress_on_task(), font=("Helvetica", 14)
        )
        self.progress_on_task_button.pack(
            pady=20
        )
        self.progress_on_task_button.place(
            relx=0.5, rely=0.5, anchor="center", width=200, height=30
        )
        self.assign_promotion_button = tk.Button(
            self.manager_logo_canvas, text="Assign Promotion", command=lambda:self.assign_promotion(username), font=("Helvetica", 14)
        )
        self.assign_promotion_button.pack(
            pady=20
        )
        self.assign_promotion_button.place(
            relx=0.5, rely=0.6, anchor="center", width=200, height=30
        )
        self.approve_resignation_button = tk.Button(
            self.manager_logo_canvas, text="Approve Resignation", command=lambda:self.approve_resignation(), font=("Helvetica", 14)
        )
        self.approve_resignation_button.pack(
            pady=20
        )
        self.approve_resignation_button.place(
            relx=0.5, rely=0.7, anchor="center", width=200, height=30
        )
        self.request_bonus_button = tk.Button(
            self.manager_logo_canvas, text="Request for Bonus", command=lambda:self.request_bonus(), font=("Helvetica", 14)
        )
        self.request_bonus_button.pack(
            pady=20
        )
        self.request_bonus_button.place(
            relx=0.5, rely=0.8, anchor="center", width=200, height=30
        )

        #create an exit button in canvas and place at bottom middle
        exit_button = tk.Button(
        self.manager_logo_canvas,
        text="Exit",
        command=manager_window.destroy,
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
            self.manager_logo_canvas, image=resized_profile_img, command=lambda:self.profile(username,role),borderwidth=0, font=("Helvetica", 14)
        )
        profile_btn.pack(
            pady=20
        )
        profile_btn.place(
            relx=0.95, rely=0.05, anchor="center", width=50, height=50
        )
        
        # focus on window
        manager_window.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(manager_window)

        # Bind the Escape key to the exit function
        manager_window.bind("<Escape>", lambda event: manager_window.destroy())

        # Run the main loop for the manager window
        manager_window.mainloop()

    def load_image_manager(self,username):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_manager_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_manager(username)

    def resize_canvas_and_image_manager(self,username):
        username_manager = username
        # Get the manager window size
        window_width = self.manager_logo_canvas.winfo_width()
        window_height = self.manager_logo_canvas.winfo_height()
        
        # Resize the canvas to the current window size
        self.manager_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_manager_logo_image.resize(
            (window_width, window_height)
        )
        self.manager_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.manager_logo_canvas.delete("all")
        self.manager_logo_canvas.create_image(
            0, 0, image=self.manager_logo_image, anchor="nw"
        )

            #redraw the manager name text    
        if hasattr(self, "manager_name_text"):
            self.manager_logo_canvas.delete(
                self.manager_name_text
            )  # Remove the old text

        self.manager_name_text = self.manager_logo_canvas.create_text(
            window_width / 2,
            100,
            text=f"Welcome {username_manager}!",
            font=("Helvetica", 28, "bold"),
            fill="white",
        )

    def on_window_resize_manager(self, event,username):
        # Handle window resize event
        self.resize_canvas_and_image_manager(username)

    def perform_review_approval(self):
        # create a new window to show the performance review approval
        review_approval_window = tk.Toplevel()
        review_approval_window.geometry("800x600")  # Set the window size
        review_approval_window.title("Performance Review Approval")

        #create a canvas that resizes with the window
        self.review_approval_logo_canvas = tk.Canvas(review_approval_window, bg="white", highlightthickness=0)
        self.review_approval_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        review_approval_window.bind("<Configure>", lambda event: self.on_window_resize_review_approval(event))

        # import the image as the background on the canvas
        self.load_image_review_approval()

        # Assuming you have values for the employee data
        employee_data_8 = self.get_employee_data_with_quarter_review()
        employee_data_9 = self.get_employee_data_with_half_yearly_review()


        # Call the method with different rely values and click handlers for each list
        self.display_employee_list_on_canvas(
            self.review_approval_logo_canvas,
            employee_data_8,
            rely=0.5,
            click_handler=self.open_employee_details_window_review
        )

        self.display_employee_list_on_canvas(
            self.review_approval_logo_canvas,
            employee_data_9,
            rely=0.8,
            click_handler=self.open_employee_details_window_review
        )


        # Bind the Escape key to the exit function
        review_approval_window.bind(
            "<Escape>", lambda event: review_approval_window.destroy()
        )
        # focus on window
        review_approval_window.focus_force()
        # Center the window with function center_window_test
        self.center_window_all(review_approval_window)
        # Run the main loop for the create_remove_hr_window
        review_approval_window.mainloop()

    def load_image_review_approval(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_review_approval_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_review_approval()

    def resize_canvas_and_image_review_approval(self):
        # Get the manager window size
        window_width = self.review_approval_logo_canvas.winfo_width()
        window_height = self.review_approval_logo_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.review_approval_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_review_approval_logo_image.resize(
            (window_width, window_height)
        )
        self.review_approval_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.review_approval_logo_canvas.delete("all")
        self.review_approval_logo_canvas.create_image(
            0, 0, image=self.review_approval_logo_image, anchor="nw"
        )

    def on_window_resize_review_approval(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_review_approval()

    def get_employee_data_review(self, username, data_type):
        emp_ref = db.reference("/employee")
        data = emp_ref.child(username).child(data_type).get()
        return data if data is not None else "no"
    
    def get_employee_data_with_quarter_review(self):
        emp_ref = db.reference("/employee")
        employee_data_8 = [user for user in emp_ref.get() if self.has_performance_review_available(user, "Quarterly Review")]
        return employee_data_8

    def get_employee_data_with_half_yearly_review(self):
        emp_ref = db.reference("/employee")
        employee_data_9 = [user for user in emp_ref.get() if self.has_performance_review_available(user, "Annual Review")]
        return employee_data_9

    def has_performance_review_available(self, username, review_type):
        emp_ref = db.reference("/employee")
        performance_review_data = emp_ref.child(username).child("performance_review").get()
        return performance_review_data is not None and review_type in performance_review_data

    def open_employee_details_window_review(self, employee_info):
        # create a new window to show employee details along with 2 radio buttons to approve or deny the request
        employee_details_window = tk.Toplevel()
        employee_details_window.geometry("800x600")  # Set the window size

        #create a canvas that resizes with the window
        self.employee_details_logo_canvas = tk.Canvas(employee_details_window, bg="white", highlightthickness=0)
        self.employee_details_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        employee_details_window.bind("<Configure>", lambda event: self.on_window_resize_employee_details(event))

        # import the image as the background on the canvas
        self.load_image_employee_details()

        # show the username of the employee using label on the canvas
        username_label = tk.Label(
            self.employee_details_logo_canvas,
            text="Username",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        username_label.pack(pady=20)
        username_label.place(relx=0.5, rely=0.35, anchor="center")

        self.username_entry = tk.Entry(
            self.employee_details_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.username_entry.pack(pady=20)
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")

        # Get the username from the employee data
        username_data = employee_info
        self.username_entry.insert(0, username_data)

        # Make the entry widget read-only
        self.username_entry.configure(state="readonly")

        # show the reason for performance review of the employee using label on the canvas
        reason_for_performance_review_label = tk.Label(
            self.employee_details_logo_canvas,
            text="Reason for Performance Review",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        reason_for_performance_review_label.pack(pady=20)
        reason_for_performance_review_label.place(relx=0.5, rely=0.5, anchor="center")

        self.reason_for_performance_review_entry = tk.Entry(
            self.employee_details_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.reason_for_performance_review_entry.pack(pady=20)
        self.reason_for_performance_review_entry.place(relx=0.5, rely=0.55, anchor="center")

        # Get the reason for performance review from the employee data
        reason_for_performance_review = self.get_employee_data(employee_info, "performance_review_reason")

        # Insert the text into the entry widget
        self.reason_for_performance_review_entry.insert(0, reason_for_performance_review)

        # Make the entry widget read-only
        self.reason_for_performance_review_entry.configure(state="readonly")

    def approve_vacations_sick_leaves(self, role, username):
        approve_window = tk.Toplevel()  # Use Tk() to create a new window
        approve_window.geometry("800x600")  # Set the window size
        approve_window.title("Approve Vacations and Sick Leaves")


        #create a canvas that resizes with the window
        self.approve_leaves_logo_canvas = tk.Canvas(approve_window, bg="white", highlightthickness=0)
        self.approve_leaves_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        approve_window.bind("<Configure>", lambda event: self.on_window_resize_approve_leaves(event,username))

        # import the image as the background on the canvas
        self.load_image_approve_leaves(username)


        # Assuming you have values for the employee data
        employee_data_with_provisional_vacation_above_zero = self.get_employee_data_with_provisional_vacation_above_zero(username)
        employee_data_with_sick_days_above_zero = self.get_employee_data_with_sick_days_above_zero(username)

        # Call the method with different rely values and click handlers for each list
        self.display_employee_list_on_canvas(
            self.approve_leaves_logo_canvas,
            employee_data_with_provisional_vacation_above_zero,
            rely=0.2,
            click_handler=self.show_employee_details_vacation
        )

        self.display_employee_list_on_canvas(
            self.approve_leaves_logo_canvas,
            employee_data_with_sick_days_above_zero,
            rely=0.7,
            click_handler=self.show_employee_details_sick
        )



        # Bind the Escape key to the exit function
        approve_window.bind(
            "<Escape>", lambda event: approve_window.destroy()
        )
        # focus on window
        approve_window.focus_force()
        # Center the window with function center_window_test
        self.center_window_all(approve_window)
        # Run the main loop for the create_remove_hr_window
        approve_window.mainloop()
                
    def load_image_approve_leaves(self,username):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_approve_leaves_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_approve_leaves(username)

    def resize_canvas_and_image_approve_leaves(self,username):
        # Get the manager window size
        window_width = self.approve_leaves_logo_canvas.winfo_width()
        window_height = self.approve_leaves_logo_canvas.winfo_height()
        
        # Resize the canvas to the current window size
        self.approve_leaves_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_approve_leaves_logo_image.resize(
            (window_width, window_height)
        )
        self.approve_leaves_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.approve_leaves_logo_canvas.delete("all")
        self.approve_leaves_logo_canvas.create_image(
            0, 0, image=self.approve_leaves_logo_image, anchor="nw"
        )

        #redraw the text vacation days and sick days
        if hasattr(self, "vacation_days_text"):
            self.approve_leaves_logo_canvas.delete(
                self.vacation_days_text
            )
        self.vacation_days_text = self.approve_leaves_logo_canvas.create_text(
            window_width / 2,
            100,
            text=f"Vacation Days",
            font=("Helvetica", 18, "bold"),
            fill="white",
        )
        if hasattr(self, "sick_days_text"):
            self.approve_leaves_logo_canvas.delete(
                self.sick_days_text
            )
        self.sick_days_text = self.approve_leaves_logo_canvas.create_text(
            window_width / 2,
            400,
            text=f"Sick Days",
            font=("Helvetica", 18, "bold"),
            fill="white",
        )

    def on_window_resize_approve_leaves(self, event,username):
        # Handle window resize event
        self.resize_canvas_and_image_approve_leaves(username)

    def get_employee_data_with_provisional_vacation_above_zero(self, username):
        emp_ref = db.reference("/employee")
        employee_data_1 = [user for user in emp_ref.get() if self.get_employee_data(user, "vacation_days") > 0]
        return employee_data_1

    def get_employee_data_with_sick_days_above_zero(self, username):
        emp_ref = db.reference("/employee")
        employee_data_2 = [user for user in emp_ref.get() if self.get_employee_data(user, "sick_days") > 0]
        return employee_data_2

    def display_employee_list_on_canvas(self, canvas, employee_data, rely, click_handler=None):
        if len(employee_data) > 0:
            employee_list = Listbox(canvas, font=("Helvetica", 12, "bold"), bg="white", fg="black", width=30, height=5)
            employee_list.pack(pady=20)
            employee_list.place(relx=0.5, rely=rely + 0.09, anchor="center")

            def on_employee_click(event):
                # Clear previous selection
                employee_list.selection_clear(0, tk.END)

                # Get the selected item
                selected_index = employee_list.nearest(event.y)
                employee_info = employee_data[selected_index]

                # Set the selection to the clicked item
                employee_list.selection_set(selected_index)

                # Bind click event to the provided handler function, if available
                if click_handler:
                    click_handler(employee_info)

            # Bind the click event to the custom function
            employee_list.bind("<ButtonRelease-1>", on_employee_click)

            # Insert employee names into the listbox
            for employee_info in employee_data:
                employee_list.insert(tk.END, employee_info)
        else:
            self.display_no_employee_message(canvas, "No employees to approve")

    def display_no_employee_message(self, canvas, message):
        no_employee_label = Label(canvas, text=message, font=("Helvetica", 12, "bold"), bg="white")
        no_employee_label.pack(pady=20)
        no_employee_label.place(relx=0.5, rely=0.5, anchor="center")

    def get_employee_data(self, username, data_type):
        emp_ref = db.reference("/employee")
        data = emp_ref.child(username).child(data_type).get()
        return data if data is not None else 0

    def show_employee_details_vacation(self, employee_data_1):
        # create a new window to show employee details along with 2 radio buttons to approve or deny the request
        employee_details_window = tk.Toplevel()
        employee_details_window.geometry("800x600")  # Set the window size
        employee_details_window.title("Vacation Approve/Deny")

        #create a canvas that resizes with the window
        self.employee_details_logo_canvas = tk.Canvas(employee_details_window, bg="white", highlightthickness=0)
        self.employee_details_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        employee_details_window.bind("<Configure>", lambda event: self.on_window_resize_employee_details(event))

        # import the image as the background on the canvas
        self.load_image_employee_details()

        # show the username of the employee using label on the canvas
        username_label = tk.Label(
            self.employee_details_logo_canvas,
            text="Username",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        username_label.pack(pady=20)
        username_label.place(relx=0.5, rely=0.35, anchor="center")

        self.username_entry = tk.Entry(
            self.employee_details_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.username_entry.pack(pady=20)
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")

        # Get the username from the employee data
        username_data = employee_data_1  # Assuming username data is directly available in employee_data_1
        self.username_entry.insert(0, username_data)

        # Make the entry widget read-only
        self.username_entry.configure(state="readonly")

        # show the reason for vacation days of the employee using label on the canvas
        provisional_vacation_days_label = tk.Label(
            self.employee_details_logo_canvas,
            text="Vacation Days",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        provisional_vacation_days_label.pack(pady=20)
        provisional_vacation_days_label.place(relx=0.5, rely=0.5, anchor="center")

        self.provisional_vacation_days_entry = tk.Entry(
            self.employee_details_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.provisional_vacation_days_entry.pack(pady=20)
        self.provisional_vacation_days_entry.place(relx=0.5, rely=0.55, anchor="center")

        # Get the vacation days from the employee data
        provisional_vacation_days = self.get_employee_data(employee_data_1, "vacation_days")
        self.provisional_vacation_days_entry.insert(0, provisional_vacation_days)

        # Make the entry widget read-only
        self.provisional_vacation_days_entry.configure(state="readonly")

        # show the reason for vacation days of the employee using label on the canvas
        reason_for_vacation_days_label = tk.Label(
            self.employee_details_logo_canvas,
            text="Reason for Vacation Days",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        reason_for_vacation_days_label.pack(pady=20)
        reason_for_vacation_days_label.place(relx=0.5, rely=0.65, anchor="center")

        self.reason_for_vacation_days_entry = tk.Entry(
            self.employee_details_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.reason_for_vacation_days_entry.pack(pady=20)
        self.reason_for_vacation_days_entry.place(relx=0.5, rely=0.7, anchor="center")

        # Get the reason for vacation days from the employee data
        reason_for_vacation_days = self.get_employee_data(employee_data_1, "vacation_reason")

        # Insert the text into the entry widget
        self.reason_for_vacation_days_entry.insert(0, reason_for_vacation_days)

        # Make the entry widget read-only
        self.reason_for_vacation_days_entry.configure(state="readonly")

        # create a new button for approving the vacation days on canvas
        approve_button = tk.Button(
            self.employee_details_logo_canvas,
            text="Approve",
            command=lambda:self.approve_vacation_days(employee_data_1),
            font=("Helvetica", 14),
        )
        approve_button.pack(
            pady=20
        )
        approve_button.place(relx=0.5, rely=0.8, anchor="center", width=100, height=30)
        # store the values in 2 variables when the button is pressed
        approve_button.bind(
            "<Button-1>",
            lambda event: self.approve_vacation_days(employee_data_1),
        )
        # create a new button for denying the vacation days on canvas
        deny_button = tk.Button(
            self.employee_details_logo_canvas,
            text="Deny",
            command=lambda:self.deny_vacation_days(employee_data_1),
            font=("Helvetica", 14),
        )
        deny_button.pack(
            pady=20
        )
        deny_button.place(relx=0.5, rely=0.9, anchor="center", width=100, height=30)
        # store the values in 2 variables when the button is pressed
        deny_button.bind(
            "<Button-1>",
            lambda event: self.deny_vacation_days(employee_data_1),
        )
        # Bind the Escape key to the exit function
        employee_details_window.bind(
            "<Escape>", lambda event: employee_details_window.destroy()
        )
        # focus on window
        employee_details_window.focus_force()
        # Center the window with function center_window_test
        self.center_window_all(employee_details_window)
        # Run the main loop for the create_remove_hr_window
        employee_details_window.mainloop()

    def show_employee_details_sick(self, employee_data_2):
        # create a new window to show employee details along with 2 radio buttons to approve or deny the request
        employee_details_window = tk.Toplevel()
        employee_details_window.geometry("800x600")  # Set the window size
        employee_details_window.title("Sick Approve/Deny")

        #create a canvas that resizes with the window
        self.employee_details_logo_canvas = tk.Canvas(employee_details_window, bg="white", highlightthickness=0)
        self.employee_details_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        employee_details_window.bind("<Configure>", lambda event: self.on_window_resize_employee_details(event))

        # import the image as the background on the canvas
        self.load_image_employee_details()

        # show the username of the employee using label on the canvas
        username_label = tk.Label(
            self.employee_details_logo_canvas,
            text=f"Username",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        username_label.pack(pady=20)
        username_label.place(relx=0.5, rely=0.35, anchor="center")

        self.username_entry = tk.Entry(
            self.employee_details_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.username_entry.pack(pady=20)
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")

        # Get the username from the employee data
        username_data = employee_data_2  # Assuming username data is directly available in employee_data_2
        self.username_entry.insert(0, username_data)

        # Make the entry widget read-only
        self.username_entry.configure(state="readonly")

        # show the reason for sick days of the employee using label on the canvas
        provisional_vacation_days_label = tk.Label(
            self.employee_details_logo_canvas,
            text="Sick Days",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        provisional_vacation_days_label.pack(pady=20)
        provisional_vacation_days_label.place(relx=0.5, rely=0.5, anchor="center")

        self.provisional_vacation_days_entry = tk.Entry(
            self.employee_details_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.provisional_vacation_days_entry.pack(pady=20)
        self.provisional_vacation_days_entry.place(relx=0.5, rely=0.55, anchor="center")

        # Get the sick days from the employee data
        provisional_vacation_days = self.get_employee_data(employee_data_2, "sick_days")
        self.provisional_vacation_days_entry.insert(0, provisional_vacation_days)

        # Make the entry widget read-only
        self.provisional_vacation_days_entry.configure(state="readonly")

        # show the reason for sick days of the employee using label on the canvas
        reason_for_sick_days_label = tk.Label(
            self.employee_details_logo_canvas,
            text="Reason for Sick Days",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        reason_for_sick_days_label.pack(pady=20)
        reason_for_sick_days_label.place(relx=0.5, rely=0.65, anchor="center")

        self.reason_for_sick_days_entry = tk.Entry(
            self.employee_details_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.reason_for_sick_days_entry.pack(pady=20)
        self.reason_for_sick_days_entry.place(relx=0.5, rely=0.7, anchor="center")

        # Get the reason for sick days from the employee data
        reason_for_sick_days = self.get_employee_data(employee_data_2, "sick_reason")

        # Insert the text into the entry widget
        self.reason_for_sick_days_entry.insert(0, reason_for_sick_days)

        # Make the entry widget read-only
        self.reason_for_sick_days_entry.configure(state="readonly")

        # create a new button for approving the vacation days on canvas
        approve_button = tk.Button(
            self.employee_details_logo_canvas,
            text="Approve",
            command=lambda:self.approve_sick_days(employee_data_2),
            font=("Helvetica", 14),
        )
        approve_button.pack(
            pady=20
        )
        approve_button.place(relx=0.5, rely=0.8, anchor="center", width=100, height=30)
        # store the values in 2 variables when the button is pressed
        approve_button.bind(
            "<Button-1>",
            lambda event: self.approve_sick_days(employee_data_2),
        )
        # create a new button for denying the vacation days on canvas
        deny_button = tk.Button(
            self.employee_details_logo_canvas,
            text="Deny",
            command=lambda:self.deny_sick_days(employee_data_2),
            font=("Helvetica", 14),
        )
        deny_button.pack(
            pady=20
        )
        deny_button.place(relx=0.5, rely=0.9, anchor="center", width=100, height=30)
        # store the values in 2 variables when the button is pressed
        deny_button.bind(
            "<Button-1>",
            lambda event: self.deny_sick_days(employee_data_2),
        )
        # Bind the Escape key to the exit function
        employee_details_window.bind(
            "<Escape>", lambda event: employee_details_window.destroy()
        )
        # focus on window
        employee_details_window.focus_force()
        # Center the window with function center_window_test
        self.center_window_all(employee_details_window)
        # Run the main loop for the create_remove_hr_window
        employee_details_window.mainloop()

    def load_image_employee_details(self):

        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_employee_details_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_employee_details()

    def resize_canvas_and_image_employee_details(self):
        # Get the employee_details window size
        window_width = self.employee_details_logo_canvas.winfo_width()
        window_height = self.employee_details_logo_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.employee_details_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_employee_details_logo_image.resize(
            (window_width, window_height)
        )
        self.employee_details_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.employee_details_logo_canvas.delete("all")
        self.employee_details_logo_canvas.create_image(
            0, 0, image=self.employee_details_logo_image, anchor="nw"
        )

    def on_window_resize_employee_details(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_employee_details()

    def approve_vacation_days(self, employee_data):
        # get the username, provisional vacation days and reason for vacation days from the employee details window
        username = self.username_entry.get()
        provisional_vacation_days = self.provisional_vacation_days_entry.get()
        reason_for_vacation_days = self.reason_for_vacation_days_entry.get()
        # update the provisional vacation days in the database for the employee
        emp_ref = db.reference("/employee")
        emp_ref.child(employee_data).update({"vacation_days": 0})
        # update the reason for vacation days in the database for the employee
        emp_ref.child(employee_data).update({"reason_for_vacation_days": reason_for_vacation_days})
        # update the vacation days in the database for the employee
        emp_ref.child(employee_data).update({"vacation_approved": provisional_vacation_days})
        emp_ref.child(employee_data).update({"vacation_approved_denied": "Approved"})
        # close the employee details window
        self.employee_details_logo_canvas.destroy()
        # show a message that the vacation days have been approved
        messagebox.showinfo("Approve Vacation Days", "Vacation Days Approved")

    def deny_vacation_days(self, employee_data):
        # get the username, provisional vacation days and reason for vacation days from the employee details window
        username = self.username_entry.get()
        provisional_vacation_days = self.provisional_vacation_days_entry.get()
        reason_for_vacation_days = self.reason_for_vacation_days_entry.get()
        # update the provisional vacation days in the database for the employee
        emp_ref = db.reference("/employee")
        emp_ref.child(employee_data).update({"vacation_days": 0})
        # update the reason for vacation days in the database for the employee
        emp_ref.child(employee_data).update({"reason_for_vacation_days": reason_for_vacation_days})
        emp_ref.child(employee_data).update({"vacation_approved_denied": "Denied"})
        # close the employee details window
        self.employee_details_logo_canvas.destroy()
        # show a message that the vacation days have been denied
        messagebox.showinfo("Deny Vacation Days", "Vacation Days Denied")

    def approve_sick_days(self, employee_data):
        # get the username, provisional vacation days and reason for vacation days from the employee details window
        username = self.username_entry.get()
        provisional_vacation_days = self.provisional_vacation_days_entry.get()
        reason_for_vacation_days = self.reason_for_sick_days_entry.get()
        # update the provisional vacation days in the database for the employee
        emp_ref = db.reference("/employee")
        emp_ref.child(employee_data).update({"sick_days": 0})
        # update the reason for vacation days in the database for the employee
        emp_ref.child(employee_data).update({"reason_for_sick_days": reason_for_vacation_days})
        # update the vacation days in the database for the employee
        emp_ref.child(employee_data).update({"sick_approved": provisional_vacation_days})
        emp_ref.child(employee_data).update({"sick_approved_denied": "Approved"})
        # close the employee details window
        self.employee_details_logo_canvas.destroy()
        # show a message that the vacation days have been approved
        messagebox.showinfo("Approve Sick Days", "Sick Days Approved")

    def deny_sick_days(self, employee_data):
        # get the username, provisional vacation days and reason for vacation days from the employee details window
        username = self.username_entry.get()
        provisional_vacation_days = self.provisional_vacation_days_entry.get()
        reason_for_vacation_days = self.reason_for_sick_days_entry.get()
        # update the provisional vacation days in the database for the employee
        emp_ref = db.reference("/employee")
        emp_ref.child(employee_data).update({"sick_days": 0})
        # update the reason for vacation days in the database for the employee
        emp_ref.child(employee_data).update({"reason_for_sick_days": reason_for_vacation_days})
        emp_ref.child(employee_data).update({"sick_approved_denied": "Denied"})
        # close the employee details window
        self.employee_details_logo_canvas.destroy()
        # show a message that the vacation days have been denied
        messagebox.showinfo("Deny Sick Days", "Sick Days Denied")

    def progress_on_task(self):
        messagebox.showinfo("manager Window", "Progress on Task Button Pressed")

    def assign_promotion(self,username):
        self.treeview_promotion_request=None
        # create a new window to show the promotion request
        self.promotion_request_window = tk.Toplevel()
        self.promotion_request_window.geometry("800x600")  # Set the window size
        self.promotion_request_window.title("Request for Promotion")
        
        #create a canvas that resizes with the window
        self.promotion_request_logo_canvas = tk.Canvas(self.promotion_request_window, bg="white", highlightthickness=0)
        self.promotion_request_logo_canvas.pack(fill=tk.BOTH, expand=True)
        
        #load the image as the background on the canvas
        self.load_image_promotion_request()
        
        # bind window resize event to function
        self.promotion_request_window.bind("<Configure>", lambda event: self.on_window_resize_promotion_request(event))
        
        # bind the escape key to the exit function
        self.promotion_request_window.bind("<Escape>", lambda event: self.promotion_request_window.destroy())
        
        # focus on window
        self.promotion_request_window.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(self.promotion_request_window)
        
        # Create a scrollable frame to hold the treeview
        scrollable_frame = tk.Frame(self.promotion_request_logo_canvas, bg="white")
        scrollable_frame.pack(fill="both", expand=True)
        scrollable_frame.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)

        # Create a new treeview to show the list of employees
        if self.treeview_promotion_request is None:
            self.treeview_promotion_request = ttk.Treeview(
                scrollable_frame, columns=("Employee",), show="headings", selectmode="browse"
            )
            self.treeview_promotion_request.heading("Employee", text="Employee")
            self.treeview_promotion_request.column("Employee", width=200, anchor="center")
            self.treeview_promotion_request.tag_configure("clickable", foreground="blue", font=("Helvetica", 12, "underline"))

            # Add a vertical scrollbar to the Treeview
            scrollbar = ttk.Scrollbar(scrollable_frame, orient="vertical", command=self.treeview_promotion_request.yview)
            scrollbar.pack(side="right", fill="y")
            self.treeview_promotion_request.configure(yscrollcommand=scrollbar.set)

            # Pack the Treeview to the scrollable frame
            self.treeview_promotion_request.pack(fill="both", expand=True)
            self.treeview_promotion_request.bind("<<TreeviewSelect>>", self.enable_promotion_request_button)

        # Configure grid row and column weights
        scrollable_frame.grid_rowconfigure(0, weight=1)
        scrollable_frame.grid_columnconfigure(0, weight=1)

        # Now you can safely use self.treeview
        self.treeview_promotion_request.delete(*self.treeview_promotion_request.get_children())

        # Populate the treeview with employee data
        self.populate_employee_list("employee")
        
        #Create a new button for promoting the employee
        self.promote_button = tk.Button(
            self.promotion_request_window,
            text="Promote",
            command=lambda:self.promote_employee(username),
            state="disabled",
            font=("Helvetica", 14),
        )
        self.promote_button.pack(
            pady=20
        )
        self.promote_button.place(relx=0.5, rely=0.9, anchor="center", width=100, height=30)

        # Run the main loop for the self.promotion_request_window
        self.promotion_request_window.mainloop()
        
    def load_image_promotion_request(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_promotion_request_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_promotion_request()
        
    def resize_canvas_and_image_promotion_request(self):
        # Get the promotion_request window size
        window_width = self.promotion_request_logo_canvas.winfo_width()
        window_height = self.promotion_request_logo_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.promotion_request_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_promotion_request_logo_image.resize(
            (window_width, window_height)
        )
        self.promotion_request_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.promotion_request_logo_canvas.delete("all")
        self.promotion_request_logo_canvas.create_image(
            0, 0, image=self.promotion_request_logo_image, anchor="nw"
        )
        
    def on_window_resize_promotion_request(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_promotion_request()

    def populate_employee_list(self, role):
        employees = list((db.reference("/employee").get()).keys())
        for employee in employees:
            self.treeview_promotion_request.insert("", "end", values=(employee,), tags=("clickable",))
            
    def enable_promotion_request_button(self, event):
        self.promote_button.config(state="normal")
        
    def promote_employee(self,username):
        # get the selected employee from the treeview
        selected_employee = self.treeview_promotion_request.item(self.treeview_promotion_request.selection())["values"][0]
        if db.reference("/employee").child(selected_employee).child("promotion_request").child("Request").get() == "Pending":
            messagebox.showinfo("Promote Employee", "Promotion Request already sent")
            self.promotion_request_window.focus_force()
            return
        elif db.reference("/employee").child(selected_employee).child("promotion_request").child("Request").get() == "Approved":
            messagebox.showinfo("Promote Employee", "Employee already promoted")
            self.promotion_request_window.focus_force()
            return
        elif db.reference("/employee").child(selected_employee).child("promotion_request").child("Request").get() == "Denied":
            messagebox.showinfo("Promote Employee", "Promotion Request Denied")
            self.promotion_request_window.focus_force()
            return
        # create a new window to show the promotion request
        self.promote_employee_window = tk.Toplevel()
        self.promote_employee_window.geometry("800x600")  # Set the window size
        self.promote_employee_window.title("Promote Employee")
        
        #create a canvas that resizes with the window
        self.promote_employee_logo_canvas = tk.Canvas(self.promote_employee_window, bg="white", highlightthickness=0)
        self.promote_employee_logo_canvas.pack(fill=tk.BOTH, expand=True)
        
        # import the image as the background on the canvas
        self.load_image_promote_employee()
        
        # bind window resize event to function
        self.promote_employee_window.bind("<Configure>", lambda event: self.on_window_resize_promote_employee(event))
        
        # bind the escape key to the exit function
        self.promote_employee_window.bind("<Escape>", lambda event: self.promote_employee_window.destroy())
        
        # focus on window
        self.promote_employee_window.focus_force()
        
        # Center the window with function center_window_test
        self.center_window_all(self.promote_employee_window)
        
        # Create a new label to show the employee name
        self.employee_name_label = tk.Label(
            self.promote_employee_logo_canvas,
            text=f"Employee Name: {selected_employee}",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        self.employee_name_label.pack(pady=20)
        self.employee_name_label.place(relx=0.5, rely=0.15, anchor="center")

        # Create a new label to show the employee's current role
        self.current_role_label = tk.Label(
            self.promote_employee_logo_canvas,
            text="Current Role: Employee",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        self.current_role_label.pack(pady=20)
        self.current_role_label.place(relx=0.5, rely=0.25, anchor="center")

        # Create a checkbutton to select if the employee should be promoted to manager
        self.promote_to_manager = tk.IntVar()
        self.promote_to_manager_checkbutton = tk.Checkbutton(
            self.promote_employee_logo_canvas,
            text="Promote to Manager",
            variable=self.promote_to_manager,
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        self.promote_to_manager_checkbutton.pack(pady=20)
        self.promote_to_manager_checkbutton.place(relx=0.5, rely=0.35, anchor="center")

        # Create a new entry for new salary and designation
        self.new_salary_entry = tk.Entry(
            self.promote_employee_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.new_salary_entry.pack(pady=20)
        self.new_salary_entry.place(relx=0.5, rely=0.45, anchor="center")
        self.new_salary_entry.insert(0, "New Salary")

        # Create a new entry for new designation
        self.new_designation_entry = tk.Entry(
            self.promote_employee_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.new_designation_entry.pack(pady=20)
        self.new_designation_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.new_designation_entry.insert(0, "New Designation")

        # Create a comment box for the manager to add reason for promotion
        self.comment_box = tk.Text(
            self.promote_employee_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.comment_box.pack(pady=20)
        self.comment_box.place(relx=0.5, rely=0.7, anchor="center", relwidth=0.8, relheight=0.2)
        self.comment_box.insert(tk.END, "Reason for Promotion")

        # Create a new button for promoting the employee
        promote_button = tk.Button(
            self.promote_employee_logo_canvas,
            text="Promote",
            command=lambda:self.promote_employee_request(username),
            font=("Helvetica", 14),
        )
        promote_button.pack(pady=20)
        promote_button.place(relx=0.5, rely=0.9, anchor="center", width=100, height=30)

    
        # Run the main loop for the self.promote_employee_window
        self.promote_employee_window.mainloop()
        
    def promote_employee_request(self,username_mngr):
        #Get the entered values from the self.promote_employee_window
        new_salary = self.new_salary_entry.get()
        new_designation = self.new_designation_entry.get()
        comment = self.comment_box.get("1.0", "end-1c")
        if self.promote_to_manager.get() == 1:
            new_role = "Manager"
        else:
            new_role = "Employee"
        username=self.treeview_promotion_request.item(self.treeview_promotion_request.selection())["values"][0]
        #Ask for confirmation before promoting the employee
        if messagebox.askokcancel("Promote Employee", "Are you sure you want to promote the employee?"):
            #Update the promotion request in the database
            emp_ref = db.reference("/employee")
            emp_ref.child(username).child("promotion_request").set({
                "Request": "Pending",
                "new_salary": new_salary,
                "new_designation": new_designation,
                "comment": comment,
                "new_role": new_role,
                "request_by": username_mngr,
            })
            messagebox.showinfo("Promote Employee", "Employee Promoted")
        self.promote_employee_window.destroy()
        self.promotion_request_window.focus_force()
        
    def load_image_promote_employee(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_promote_employee_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_promote_employee()
        
    def resize_canvas_and_image_promote_employee(self):
        # Get the promote_employee window size
        window_width = self.promote_employee_logo_canvas.winfo_width()
        window_height = self.promote_employee_logo_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.promote_employee_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_promote_employee_logo_image.resize(
            (window_width, window_height)
        )
        self.promote_employee_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.promote_employee_logo_canvas.delete("all")
        self.promote_employee_logo_canvas.create_image(
            0, 0, image=self.promote_employee_logo_image, anchor="nw"
        )
        
    def on_window_resize_promote_employee(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_promote_employee()
        
    def approve_resignatin(self):
        messagebox.showinfo("manager Window", "Approve Resignation Button Pressed")

    def request_bonus(self):
        # create a new window to show the bonus request
        bonus_request_window = tk.Toplevel()
        bonus_request_window.geometry("800x600")  # Set the window size
        bonus_request_window.title("Request for Bonus")

        # create a canvas that resizes with the window
        self.bonus_request_logo_canvas = tk.Canvas(bonus_request_window, bg="white", highlightthickness=0)
        self.bonus_request_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        bonus_request_window.bind("<Configure>", lambda event: self.on_window_resize_bonus_request(event))

        self.treeview2 = None

        # import the image as the background on the canvas
        self.load_image_bonus_request()

        #create a scrollable frame to hold the employee list
        self.scrollable_frame2 = tk.Frame(bonus_request_window, bg="white")
        self.scrollable_frame2.pack(fill="both", expand=True)
        self.scrollable_frame2.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)

        
        # create a treeview to display the employees
        if self.treeview2 is None:
            self.treeview2 = ttk.Treeview(
                self.scrollable_frame2, columns=("Employee",), show="headings", selectmode="browse"
            )
            self.treeview2.heading("Employee", text="Employee")
            self.treeview2.column("Employee", width=200, anchor="center")
            self.treeview2.tag_configure("clickable", foreground="blue", font=("Helvetica", 12, "underline"))
            self.treeview2.bind("<Double-1>", lambda event: self.open_employee_details_window2(self.treeview2.item(self.treeview2.selection())["values"][0]))

            # Add a vertical scrollbar to the Treeview
            scrollbar = ttk.Scrollbar(self.scrollable_frame2, orient="vertical", command=self.treeview2.yview)
            scrollbar.pack(side="right", fill="y")
            self.treeview2.configure(yscrollcommand=scrollbar.set)

            # Pack the Treeview to the scrollable frame
            self.treeview2.pack(fill="both", expand=True)

        # Configure grid row and column weights
        self.scrollable_frame2.grid_rowconfigure(0, weight=1)
        self.scrollable_frame2.grid_columnconfigure(0, weight=1)

        # Now you can safely use self.treeview
        self.treeview2.delete(*self.treeview2.get_children())

        # Populate the treeview with employee data
        self.populate_employee_list_2("employee")
        
            # bind the escape key to the exit function
        bonus_request_window.bind("<Escape>", lambda event: bonus_request_window.destroy())

        # focus on window
        bonus_request_window.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(bonus_request_window)

        # Run the main loop for the bonus_request_window
        bonus_request_window.mainloop()
        
    def load_image_bonus_request(self):
            
            # Construct the full path to the image file based on role and username
            img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

            # Load image and adjust canvas size
            self.original_bonus_request_logo_image = Image.open(img_path)
            self.resize_canvas_and_image_bonus_request()

    def resize_canvas_and_image_bonus_request(self):
        # Get the bonus_request window size
        window_width = self.bonus_request_logo_canvas.winfo_width()
        window_height = self.bonus_request_logo_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.bonus_request_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_bonus_request_logo_image.resize(
            (window_width, window_height)
        )
        self.bonus_request_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.bonus_request_logo_canvas.delete("all")
        self.bonus_request_logo_canvas.create_image(
            0, 0, image=self.bonus_request_logo_image, anchor="nw"
        )

    def on_window_resize_bonus_request(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_bonus_request()

    def populate_employee_list_2(self, role):
        employees = list((db.reference("/employee").get()).keys())
        for employee in employees:
            self.treeview2.insert("", "end", values=(employee,), tags=("clickable",))

    def open_employee_details_window2(self, employee_name):
        #Function to open another window with employee details
        employee_details_window2 = tk.Toplevel()
        employee_details_window2.geometry("400x300")
        employee_details_window2.title(f"Details for {employee_name}")
        employee_details_window2.focus_force()
                
        #create a canvas that resizes with the window
        self.employee_details_canvas = tk.Canvas(employee_details_window2, bg="white", highlightthickness=0)
        self.employee_details_canvas.pack(fill=tk.BOTH, expand=True)
        
        self.load_image_employee_details_new2(employee_name)
        
        # bind window resize event to function
        employee_details_window2.bind("<Configure>", lambda event: self.on_window_resize_employee_details_new2(employee_name,event))
        
            # Create Entry widgets for text input
        self.bonus_amount_entry = tk.Entry(
            self.employee_details_canvas, font=("Helvetica", 12, "bold")
        )
        self.bonus_amount_entry.place(relx=0.5, rely=0.4, anchor="center")

        self.reason_entry = tk.Entry(
            self.employee_details_canvas, font=("Helvetica", 12, "bold")
        )
        self.reason_entry.place(relx=0.5, rely=0.6, anchor="center")

            # Create a Submit Request button
        submit_button = tk.Button(
            self.employee_details_canvas,
            text="Submit Request",
            command=lambda: self.submit_bonus_request(employee_name),
            font=("Helvetica", 14),
            width=15,
            height=2,
            bd=0,
            fg="white",
            bg="green",  # You can change the color as needed
            activebackground="dark green",  # You can change the color as needed
        )
        submit_button.place(relx=0.5, rely=0.8, anchor="center")

            
        
        #create an exit button in canvas and place at bottom middle
        exit_button = tk.Button(
        self.employee_details_canvas,
        text="Exit",
        command=employee_details_window2.destroy,
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
        self.center_window_all(employee_details_window2)
        
        # Bind the Escape key to the exit function
        employee_details_window2.bind("<Escape>", lambda event: self.handle_employee_details_window_exit(event, employee_details_window2))
        
        # Run the main loop for the employee details window
        employee_details_window2.mainloop()

    def submit_bonus_request(self, employee_name):
        # Get the entered values from the Entry widgets
        amount_bonus = self.bonus_amount_entry.get()
        reason_bonus = self.reason_entry.get()
        

        #put if conditions to handle non integer values, non input in the amount_bonus
        if amount_bonus == "":
            messagebox.showerror("Error", "Please enter a valid amount for the bonus")
        else:
            try:
                amount_bonus = int(amount_bonus)
                if amount_bonus < 0:
                    messagebox.showerror("Error", "Please enter a valid amount for the bonus")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount for the bonus")

        #put if conditions to handle non input in the reason_bonus
        if reason_bonus == "":
            messagebox.showerror("Error", "Please enter a reason for the bonus")
        else:
            # Update the database with the bonus request
            emp_ref = db.reference("/employee")
            emp_ref.child(employee_name).update({"bonus_req": amount_bonus})
            emp_ref.child(employee_name).update({"bonus_reason": reason_bonus})
            # Close the employee details window
            self.employee_details_canvas.destroy()
            # Show a message that the bonus request has been submitted
            messagebox.showinfo("Bonus Request", "Bonus Request Submitted")
            
    def load_image_employee_details_new2(self,employee_name):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_employee_details_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_employee_details_new2(employee_name)

    def resize_canvas_and_image_employee_details_new2(self,employee_name):
        # Get the employee_details window size
        window_width = self.employee_details_canvas.winfo_width()
        window_height = self.employee_details_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.employee_details_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_employee_details_logo_image.resize(
            (window_width, window_height)
        )
        self.employee_details_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.employee_details_canvas.delete("all")
        self.employee_details_canvas.create_image(
            0, 0, image=self.employee_details_logo_image, anchor="nw"
        )
        
            #show the employee name on the canvas
        self.employee_details_canvas.create_text(
            window_width / 2,
            100,
            text=f"Employee Name: {employee_name}",
            font=("Helvetica", 18, "bold"),
            fill="white",
        )

        self.employee_details_canvas.create_text(
            window_width / 2,
            200,
            text="Amount of Bonus to be Requested:",
            font=("Helvetica", 18, "bold"),
            fill="white",
        )

        self.employee_details_canvas.create_text(
            window_width / 2,
            320,
            text="Reason for Bonus:",
            font=("Helvetica", 18, "bold"),
            fill="white",
        )

    def on_window_resize_employee_details_new2(self,employee_name, event):
        # Handle window resize event
        self.resize_canvas_and_image_employee_details_new2(employee_name)

    def center_window_all(self, window):
        # Get the width and height of the screen
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Calculate the x and y coordinates to center the main window
        x = (screen_width / 2) - (900 / 2)
        y = (screen_height / 2) - (700 / 2)

        # Set the dimensions of the screen and where it is placed
        window.geometry("%dx%d+%d+%d" % (900, 700, x, y))
        
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
        text1=f"EID: {list[0]}\nName: {username}\nRole: {role}\nDesignation: {list[1]}\nSalary: {list[2]}\nHours Attended: {list[3]}\nBonus: {list[4]}\nSick Days: {list[5]}\nVacation Days: {list[6]}"
        self.profile_canvas.create_text(
            # Place the text in the bottom left corner
            10,
            window_height - 10,
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
            mng_ref = db.reference("/manager")
            mng_ref.child(username).update({"password": new_password})
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
            
def main(role,username):
    manager=Manager_class()
    manager.open_manager_window(role,username)