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
import main as Main
from main import *

class Employee_class:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Employee Window")
        
    def open_employee_window(self, role, username,uni_role):
        self.uni_role = uni_role
        if hasattr(self, "root"):
            try:
                if self.root.winfo_exists():
                    self.root.destroy()  # Close the main login window
            except:
                pass

        employee_window = tk.Tk()  # Use Tk() to create a new window
        employee_window.geometry("900x600")  # Set the window size
        employee_window.title("Employee Window")
        
        self.current_question_index = 0  # Initialize the current question index
        self.selected_values = {}  # Initialize selected_values as an empty dictionary
        self.buttons_created = False  # Initialize the buttons_created flag as False
        
        #create a canvas that resizes with the window
        self.employee_logo_canvas = tk.Canvas(employee_window, bg="white", highlightthickness=0)
        self.employee_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # import the image as the background on the canvas
        self.load_image_employee(username)
        
        # bind window resize event to function
        employee_window.bind("<Configure>", lambda event: self.on_window_resize_employee(event,username))

        # focus on window
        employee_window.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(employee_window)
        
        #Check if Sick/Vacation Days are approved
        emp_ref = db.reference("/employee")
        vacation_approved = emp_ref.child(username).child("vacation_approved_denied").get()
        sick_approved = emp_ref.child(username).child("sick_approved_denied").get()
        if sick_approved != None and sick_approved == "Approved":
            messagebox.showinfo("Sick Days Approved", "Your Sick Days have been approved")
            emp_ref.child(username).update({"sick_approved_denied": "None"})
        if vacation_approved != None and vacation_approved == "Approved":
            messagebox.showinfo("Vacation Days Approved", "Your Vacation Days have been approved")
            emp_ref.child(username).update({"vacation_approved_denied": "None"})
        if sick_approved != None and sick_approved == "Denied":
            messagebox.showinfo("Sick Days Denied", "Your Sick Days have been denied")
            emp_ref.child(username).update({"sick_approved_denied": "None"})
        if vacation_approved != None and vacation_approved == "Denied":
            messagebox.showinfo("Vacation Days Denied", "Your Vacation Days have been denied")
            emp_ref.child(username).update({"vacation_approved_denied": "None"})
        if emp_ref.child(username).child("resignation_request").child("resignation_status").get() == "Approved by HR":
            date=emp_ref.child(username).child("resignation_request").child("resignation_date").get()
            messagebox.showinfo(f"Resignation Request", "Resignation request has been approved by Admin.\nYou will be logged out on "+date)
            
            #Check if the date is today or past
            #If yes, then logout the user
            if datetime.datetime.now().date() >= datetime.datetime.strptime(date, "%Y-%m-%d").date():
                messagebox.showinfo("Resignation Request", "You have been logged out as per your resignation request and cannot login again.")
                employee_window.destroy()
                return
        if emp_ref.child(username).child("resignation_request").child("resignation_status").get() == "Denied by HR":
            messagebox.showinfo(f"Resignation Request", "Resignation request has been denied by Admin for the following reason:\n"+emp_ref.child(username).child("resignation_request").child("resignation_reason").get())
            emp_ref.child(username).child("resignation_request").child("resignation_status").set("None")
            emp_ref.child(username).child("resignation_request").child("resignation_reason").set("None")
        if emp_ref.child(username).child("resignation_request").child("resignation_status").get() == "Denied by Manager":
            messagebox.showinfo(f"Resignation Request", "Resignation request has been denied by Manager for the following reason:\n"+emp_ref.child(username).child("resignation_request").child("resignation_reason").get())
            emp_ref.child(username).child("resignation_request").child("resignation_status").set("None")
            emp_ref.child(username).child("resignation_request").child("resignation_reason").set("None")
        if emp_ref.child(username).child("warning").get() == "Warning issued by HR":
            messagebox.showinfo(f"Warning", "Your attended hours are less than 80% of the total hours.\nYou have been issued a warning by HR.")
            emp_ref.child(username).update({"warning": "None"})
        if emp_ref.child(username).child("complaint").child("complaint_status").get() == "warned":
            messagebox.showinfo(f"Complaint", "You have been warned by HR because of a submitted complaint.")
            emp_ref.child(username).child("complaint").child("complaint_status").set("None")
        
        #add buttons and use a function to place them in the canvas
        self.add_buttons_to_canvas_employee(username)

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

        profile_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "profile.png" #change jpg to png for main background
        )
        profile_img = PhotoImage(file=profile_path)
        
        resized_profile_img = profile_img.subsample(4, 4)
        
        profile_btn = tk.Button(
            self.employee_logo_canvas, image=resized_profile_img, command=lambda:self.profile(username,role),borderwidth=0, font=("Helvetica", 14)
        )
        profile_btn.pack(
            pady=20
        )
        profile_btn.place(
            relx=0.95, rely=0.05, anchor="center", width=50, height=50
        )
        
        logout_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "logout.png")
        logout_image = Image.open(logout_path)
        logout_image = logout_image.resize((50, 50))
        logout_image = ImageTk.PhotoImage(logout_image)
        logout_button = tk.Button(
            self.employee_logo_canvas,
            image=logout_image,
            command=lambda: self.logout(employee_window),
            bd=0,
            bg="white",
            activebackground="white",
        )
        logout_button.image = logout_image
        logout_button.pack()
        logout_button.place(relx=0.95, rely=0.95, anchor="se")
        
        # Bind the Escape key to the exit function
        employee_window.bind("<Escape>", lambda event: employee_window.destroy())

        if db.reference("/employee").child(username).child("resignation_request").child("resignation_status").get() == "Approved by HR":
            date=db.reference("/employee").child(username).child("resignation_request").child("resignation_date").get()
            messagebox.showinfo(f"Resignation Request", "Resignation request has been approved by Admin.\nYou will be logged out on "+date)
            
            #Check if the date is today or past
            #If yes, then logout the user
            if datetime.datetime.now().date() >= datetime.datetime.strptime(date, "%Y-%m-%d").date():
                messagebox.showinfo("Resignation Request", "You have been logged out as per your resignation request and cannot login again.")
                employee_window.destroy()
                return
            
        # Run the main loop for the employee window
        employee_window.mainloop()

    def add_buttons_to_canvas_employee(self,username):
        #buttons of Employee window to the right side of the screen
        self.apply_for_vacation_days_button = tk.Button(
            self.employee_logo_canvas, text="Apply for Sick/Vacation Days", command=lambda:self.apply_for_vacation_days(username), font=("Helvetica", 14)
        )
        self.apply_for_vacation_days_button.pack(
            pady=20
        )
        self.apply_for_vacation_days_button.place(
            relx=0.25, rely=0.3, anchor="center", width=300, height=50
        )

        self.apply_for_resignation_button = tk.Button(
            self.employee_logo_canvas, text="Apply for Resignation", command=lambda:self.apply_for_resignation(username), font=("Helvetica", 14)
        )
        self.apply_for_resignation_button.pack(
            pady=20
        )
        self.apply_for_resignation_button.place(
            relx=0.75, rely=0.3, anchor="center", width=300, height=50
        )

        # self.check_progress_on_tasks_button = tk.Button(
        #     self.employee_logo_canvas, text="Check and update Progress on Tasks", command=lambda:self.check_progress_on_tasks(username), font=("Helvetica", 14)
        # )
        # self.check_progress_on_tasks_button.pack(
        #     pady=20
        # )
        # self.check_progress_on_tasks_button.place(
        #     relx=0.25, rely=0.5, anchor="center", width=350, height=50
        # )

        self.submit_survey_button = tk.Button(
            self.employee_logo_canvas, text="View and Submit Survey", command=lambda:self.submit_survey(username), font=("Helvetica", 14)
        )
        self.submit_survey_button.pack(
            pady=20
        )
        self.submit_survey_button.place(
            relx=0.25, rely=0.5, anchor="center", width=300, height=50
        )

        self.submit_complaint_button = tk.Button(

            self.employee_logo_canvas, text="Submit Complaint", command=lambda:self.submit_complaint(username), font=("Helvetica", 14)
        )
        self.submit_complaint_button.pack(
            pady=20
        )
        self.submit_complaint_button.place(
            relx=0.75, rely=0.5, anchor="center", width=300, height=50
        )

        self.submit_performance_review_button = tk.Button(
            self.employee_logo_canvas, text="Submit Performance Review", command=lambda:self.submit_performance_review(username), font=("Helvetica", 14)
        )
        self.submit_performance_review_button.pack(
            pady=20
        )
        self.submit_performance_review_button.place(
            relx=0.5, rely=0.7, anchor="center", width=300, height=50
        )

    def load_image_employee(self,username):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_employee_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_employee(username)

    def resize_canvas_and_image_employee(self, username):
        # Get the employee window size
        window_width = self.employee_logo_canvas.winfo_width()
        window_height = self.employee_logo_canvas.winfo_height()

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

        # Redraw the employee name text
        self.redraw_employee_name(username)

        # Redraw the employee details text
        # self.redraw_employee_details(username)

    def redraw_employee_name(self, username):
        username_employee = username
        window_width = self.employee_logo_canvas.winfo_width()
        
        # Check if the employee name text already exists and delete it
        if hasattr(self, "employee_name_text"):
            self.employee_logo_canvas.delete(self.employee_name_text)

        # Create and place the employee name text
        self.employee_name_text = self.employee_logo_canvas.create_text(
            window_width / 2,
            100,
            text=f"Welcome {username_employee}!",
            font=("Helvetica", 28, "bold"),
            fill="white",
        )

    # def redraw_employee_details(self, username):
    #     window_height = self.employee_logo_canvas.winfo_height()
    #     employee_ref = db.reference("/employee")
    #     emp_id = employee_ref.child(username).child("emp_id").get()
    #     designation = employee_ref.child(username).child("designation").get()
    #     salary = employee_ref.child(username).child("salary").get()
    #     sick_approved = employee_ref.child(username).child("sick_approved").get()
    #     vacation_approved = employee_ref.child(username).child("vacation_approved").get()
    #     bonus = employee_ref.child(username).child("bonus").get()
    #     hours_attended = employee_ref.child(username).child("hours_attended").get()
    #     survey = employee_ref.child(username).child("survey").child("available").get()
    #     vacation_a_d = employee_ref.child(username).child("vacation_approved_denied").get()
    #     sick_a_d = employee_ref.child(username).child("sick_approved_denied").get()

    #     # Check if the employee details text already exists and delete it
    #     if hasattr(self, "employee_details_text"):
    #         self.employee_logo_canvas.delete(self.employee_details_text)

    #     # Create and place the employee details text
    #     self.employee_details_text = self.employee_logo_canvas.create_text(
    #         # Place it on the leftmost of the window
    #         10,
    #         window_height - 10,
    #         text=f"Employee ID: {emp_id}\nDesignation: {designation}\nSalary: {salary}\nSick Days: {sick_approved}\nVacation Days: {vacation_approved}\nBonus: {bonus}\nHours Attended: {hours_attended}\nSurvey Available: {survey}\nVacation Approved/Denied: {vacation_a_d}\nSick Approved/Denied: {sick_a_d}\n\n\n\n\n",
    #         font=("Helvetica", 18, "bold"),
    #         fill="white",
    #         anchor="sw",
    #     )

    def on_window_resize_employee(self, event,username):
        # Handle window resize event
        self.resize_canvas_and_image_employee(username)

    def apply_for_vacation_days_load_image(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_apply_for_vacation_days_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_apply_for_vacation_days()

    def resize_canvas_and_image_apply_for_vacation_days(self):
        # Get the apply_for_vacation_days window size
        window_width = self.apply_for_vacation_days_canvas.winfo_width()
        window_height = self.apply_for_vacation_days_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.apply_for_vacation_days_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_apply_for_vacation_days_logo_image.resize(
            (window_width, window_height)
        )
        self.apply_for_vacation_days_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.apply_for_vacation_days_canvas.delete("all")
        self.apply_for_vacation_days_canvas.create_image(
            0, 0, image=self.apply_for_vacation_days_logo_image, anchor="nw"
        )

    def on_window_resize_apply_for_vacation_days(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_apply_for_vacation_days()  

    def apply_for_vacation_days(self, username):
        # Create a new window for the apply_for_vacation_days top level
        apply_for_vacation_days_window = tk.Toplevel()
        apply_for_vacation_days_window.geometry("800x600")  # Set the window size
        apply_for_vacation_days_window.title("Apply for Sick/Vacation Days")

        # create the canvas
        self.apply_for_vacation_days_canvas = tk.Canvas(apply_for_vacation_days_window, bg="white", highlightthickness=0)
        self.apply_for_vacation_days_canvas.pack(fill=tk.BOTH, expand=True)

        # load the image
        self.apply_for_vacation_days_load_image()

        # Create a dropdown menu for sick/vacation days
        options = ["Select Type", "Sick Days", "Vacation Days"]
        selected_option = tk.StringVar()
        selected_option.set(options[0])  # Set the default option

        dropdown_menu = tk.OptionMenu(self.apply_for_vacation_days_canvas, selected_option, *options)
        dropdown_menu.pack(pady=10, side=tk.TOP, anchor=tk.CENTER)

        # Create entry widgets for number of days and reason
        self.number_of_days_entry = tk.Entry(self.apply_for_vacation_days_canvas)
        self.number_of_days_entry.pack(pady=10, side=tk.TOP, anchor=tk.CENTER)
        self.number_of_days_entry.insert(0, "0")  # Default value
        self.number_of_days_entry.bind("<FocusIn>", lambda event: self.days_entry_del())  # Delete the default value when the user clicks on the entry widget

        self.reason_entry = tk.Entry(self.apply_for_vacation_days_canvas)
        self.reason_entry.pack(pady=10, side=tk.TOP, anchor=tk.CENTER)
        self.reason_entry.insert(0, "Vacation reason")  # Default value
        self.reason_entry.bind("<FocusIn>", lambda event: self.reason_entry_del())  # Delete the default value when the user clicks on the entry widget

        # Create a button to submit the vacation request
        submit_button = tk.Button(self.apply_for_vacation_days_canvas, text="Submit", command=lambda: self.submit_vacation_request(username, selected_option.get(), apply_for_vacation_days_window))
        submit_button.pack(pady=10, side=tk.TOP, anchor=tk.CENTER)

        # Bind the Escape key to the exit function
        apply_for_vacation_days_window.bind("<Escape>", lambda event: apply_for_vacation_days_window.destroy())

        # bind window resize event to function
        apply_for_vacation_days_window.bind("<Configure>", lambda event: self.on_window_resize_apply_for_vacation_days(event))

        # focus on window
        apply_for_vacation_days_window.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(apply_for_vacation_days_window)

        # Run the main loop for the apply_for_vacation_days_window
        apply_for_vacation_days_window.mainloop()

    def submit_vacation_request(self, username, selected_option, apply_for_vacation_days_window):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        # Retrieve the entered values
        number_of_days = self.number_of_days_entry.get()
        reason = self.reason_entry.get()

        # Check if the values are entered and valid
        if not number_of_days:
            messagebox.showinfo("Employee Window", "Please enter a number of days.")
        elif not number_of_days.isdigit():
            messagebox.showinfo("Employee Window", "Please enter a valid number of days.")
        elif not reason:
            messagebox.showinfo("Employee Window", "Please enter a reason.")
        elif number_of_days == "0" :
            messagebox.showinfo("Employee Window", "Please enter a number of days.")
        elif reason == "Vacation reason":
            messagebox.showinfo("Employee Window", "Please enter a reason.")
        elif selected_option == "Select Type":
            messagebox.showinfo("Employee Window", "Please select sick or vacation days.")
        elif selected_option == "Sick Days" and int(number_of_days) > (db.reference("sick_days_uni").get() - (self.get_employee_data(username, "sick_days"))):
            messagebox.showinfo("Employee Window", "You do not have enough sick days.")
        elif selected_option == "Vacation Days" and int(number_of_days) > (db.reference("vacation_uni").get() - (self.get_employee_data(username, "vacation_days"))):
            messagebox.showinfo("Employee Window", "You do not have enough vacation days.")
        else:
            # Convert number_of_days string to int
            number_of_days_int = int(number_of_days)

            # Check if the number of days is at least 1
            if number_of_days_int < 1:
                messagebox.showinfo("Employee Window", "Please enter at least 1 day.")
            else:
                # Update the database
                emp_ref = db.reference("/employee")
                if selected_option == "Sick Days":
                    emp_ref.child(username).update({"sick_days": self.get_employee_data(username, "sick_days") + number_of_days_int})
                    emp_ref.child(username).update({"sick_reason": reason})
                    #add pending approval for sick days in the database in approved/denied sick days
                    emp_ref.child(username).update({"sick_approved_denied": "pending"})
                else:
                    emp_ref.child(username).update({"vacation_days": self.get_employee_data(username, "vacation_days") + number_of_days_int})
                    emp_ref.child(username).update({"vacation_reason": reason})
                    emp_ref.child(username).update({"vacation_approved_denied": "pending"})

                # Show a message that the request has been submitted
                messagebox.showinfo("Employee Window", "Request submitted.")

                # Close the apply_for_vacation_days_window
                apply_for_vacation_days_window.destroy()

    def get_employee_data(self, username, data_type):
        emp_ref = db.reference("/employee")
        data = emp_ref.child(username).child(data_type).get()
        return data if data is not None else 0

    def apply_for_resignation(self,username):
        # Create a new window for the apply_for_resignation top level
        apply_for_resignation_window = tk.Toplevel()
        apply_for_resignation_window.geometry("800x600")  # Set the window size
        apply_for_resignation_window.title("Apply for Resignation")
        
        #create the canvas
        self.apply_for_resignation_canvas = tk.Canvas(apply_for_resignation_window, bg="white", highlightthickness=0)
        self.apply_for_resignation_canvas.pack(fill=tk.BOTH, expand=True)
        
        #load the image
        self.apply_for_resignation_load_image()
                
        # Create entry widget for reason of resignation (bigger size)
        self.reason_entry = tk.Entry(self.apply_for_resignation_canvas, width=50, font=("Helvetica", 14))
        self.reason_entry.pack(pady=20, side=tk.TOP, anchor=tk.CENTER)
        self.reason_entry.insert(0, "Reason for resignation")  # Default value
        self.reason_entry.bind("<FocusIn>", lambda event: self.reason_entry_del())  # Delete the default value when the user clicks on the entry widget

        # # Create a DateEntry widget for the resignation date (bigger size)
        # self.date_entry = DateEntry(
        # self.apply_for_resignation_canvas,
        # width=15,
        # background="darkblue",
        # foreground="white",
        # borderwidth=2,
        # year=2024,
        # font=("Helvetica", 14),
        # date_pattern='dd/mm/yyyy'  # Set the date format here
        # )
        # self.date_entry.pack(pady=20, side=tk.TOP, anchor=tk.CENTER)
        # self.date_entry.bind("<FocusIn>", lambda event: self.date_entry_del())  # Delete the default value when the user clicks on the entry widget

        # Create a button to submit the resignation request
        submit_button = tk.Button(self.apply_for_resignation_canvas, text="Submit", command=lambda: self.submit_resignation_request(apply_for_resignation_window, username))
        submit_button.pack(pady=20, side=tk.TOP, anchor=tk.CENTER)

        # bind window resize event to function
        apply_for_resignation_window.bind("<Configure>", lambda event: self.on_window_resize_apply_for_resignation(event))
        
        # Bind the Escape key to the exit function
        apply_for_resignation_window.bind("<Escape>", lambda event: apply_for_resignation_window.destroy())
        
        # focus on window
        apply_for_resignation_window.focus_force()
        
        # Center the window with function center_window_test
        self.center_window_all(apply_for_resignation_window)
        
        # Run the main loop for the apply_for_resignation_window
        apply_for_resignation_window.mainloop()

    def apply_for_resignation_load_image(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_apply_for_resignation_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_apply_for_resignation()

    def resize_canvas_and_image_apply_for_resignation(self):
        # Get the apply_for_resignation window size
        window_width = self.apply_for_resignation_canvas.winfo_width()
        window_height = self.apply_for_resignation_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.apply_for_resignation_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_apply_for_resignation_logo_image.resize(
            (window_width, window_height)
        )
        self.apply_for_resignation_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.apply_for_resignation_canvas.delete("all")
        self.apply_for_resignation_canvas.create_image(
            0, 0, image=self.apply_for_resignation_logo_image, anchor="nw"
        )

    def on_window_resize_apply_for_resignation(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_apply_for_resignation()
            
    def submit_resignation_request(self, apply_for_resignation_window, username):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        # Retrieve the entered values
        reason = self.reason_entry.get()
        #date = self.date_entry.get()

        # Check if the date is at least 2 weeks from now
        if not reason:
            messagebox.showinfo("Employee Window", "Please enter a reason.")
        # elif date == "Date of resignation":
        #     messagebox.showinfo("Employee Window", "Please enter a date.")
        elif db.reference("/employee").child(username).child("resignation_request").child("resignation_status").get() == "pending":
            messagebox.showinfo("Employee Window", "You have already applied for resignation.")
        else:
            # Convert date string to datetime object
            # date_format = "%d/%m/%Y"
            # date_obj = datetime.datetime.strptime(date, date_format)

            # # Convert datetime object back to string in the desired format
            # date_str_formatted = date_obj.strftime("%d/%m/%Y")

            # # Check if the date is at least 2 weeks from now
            # if date_obj < datetime.datetime.now() + datetime.timedelta(weeks=2):
            #     messagebox.showinfo("Employee Window", "Please enter a date at least 2 weeks from now.")
            #else:
                # Add the resignation request to the database
                #db.reference("/employee").child(username).child("resignation_request").child("apply_for_resignation").set(date_str_formatted)
                db.reference("/employee").child(username).child("resignation_request").child("resignation_reason").set(reason)
                db.reference("/employee").child(username).child("resignation_request").child("resignation_status").set("pending")
                messagebox.showinfo("Employee Window", "Resignation request submitted successfully.")

        apply_for_resignation_window.destroy()

    def check_progress_on_tasks(self, username):
        # Create a new window for the check_progress_on_tasks top level
        check_progress_on_tasks_window = tk.Toplevel()
        check_progress_on_tasks_window.geometry("800x600")  # Set the window size
        check_progress_on_tasks_window.title("Check Progress on Tasks")
        
        #create the canvas
        self.check_progress_on_tasks_canvas = tk.Canvas(check_progress_on_tasks_window, bg="white", highlightthickness=0)
        self.check_progress_on_tasks_canvas.pack(fill=tk.BOTH, expand=True)
        
        #load the image
        self.check_progress_on_tasks_load_image(username)

        # bind window resize event to function
        check_progress_on_tasks_window.bind("<Configure>", lambda event: self.on_window_resize_check_progress_on_tasks(username,event))
        
        # Bind the escape key to the exit function
        check_progress_on_tasks_window.bind("<Escape>", lambda event: check_progress_on_tasks_window.destroy())

        # Focus on window
        check_progress_on_tasks_window.focus_force()

        # Center the window
        self.center_window_all(check_progress_on_tasks_window)

        # Run the main loop for the check_progress_on_tasks_window
        check_progress_on_tasks_window.mainloop()
        
    def check_progress_on_tasks_load_image(self,username):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_check_progress_on_tasks_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_check_progress_on_tasks(username)

    def resize_canvas_and_image_check_progress_on_tasks(self,username):
        # Get the check_progress_on_tasks window size
        window_width = self.check_progress_on_tasks_canvas.winfo_width()
        window_height = self.check_progress_on_tasks_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.check_progress_on_tasks_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_check_progress_on_tasks_logo_image.resize(
            (window_width, window_height)
        )
        self.check_progress_on_tasks_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.check_progress_on_tasks_canvas.delete("all")
        self.check_progress_on_tasks_canvas.create_image(
            0, 0, image=self.check_progress_on_tasks_logo_image, anchor="nw"
        )
        
        # Information labels
        labels_info = [
            ("Project ID", db.reference("/employee").child(username).child("project").child("id").get()),
            ("Project Name", db.reference("/employee").child(username).child("project").child("name").get()),
            ("Project Description", db.reference("/employee").child(username).child("project").child("description").get()),
            ("Project Progress", str(db.reference("/employee").child(username).child("project").child("progress").get()) + "%"),
            ("Project Deadline", db.reference("/employee").child(username).child("project").child("deadline").get()),
            ("Task Description", db.reference("/employee").child(username).child("project").child("task").child("description").get()),
            ("Task Status", db.reference("/employee").child(username).child("project").child("task").child("status").get()),
        ]

        for i, (label_text, value) in enumerate(labels_info):
            #create text onto the canvas
            text_label=self.check_progress_on_tasks_canvas.create_text(
                window_width / 2,
                100 + i * 50,
                text=f"{label_text}: {value}",
                font=("Helvetica", 14, "bold"),
                fill="white",
            )
            if label_text == "Task Status" and value == "In Progress":
                set_task_status_to_completed_button = tk.Button(self.check_progress_on_tasks_canvas, text="Set Task Status to Completed", command=lambda: self.set_task_status_to_completed(username))
                set_task_status_to_completed_button.pack(pady=10, side=tk.TOP, anchor=tk.CENTER)
                set_task_status_to_completed_button.place(relx=0.5, rely=0.5, anchor="center", width=300, height=30)
                # Place the button next to the current label_text
                button_relx = self.check_progress_on_tasks_canvas.bbox(text_label)[2] + 10  # Get the right boundary of the text
                set_task_status_to_completed_button.place(relx=button_relx, rely=0.5, anchor="w", width=300, height=30)
            
        # Members label
        members_list = db.reference("/employee").child(username).child("project").child("members").get()
        members = "\n".join([f"{key}: {value}" for key, value in members_list.items()])

        self.check_progress_on_tasks_canvas.create_text(
            10,
            10,
            text=f"Members:\n{members}",
            font=("Helvetica", 14, "bold"),
            fill="white",
            anchor="nw",
        )
        
    def on_window_resize_check_progress_on_tasks(self,username, event):
        # Handle window resize event
        self.resize_canvas_and_image_check_progress_on_tasks(username)

    def set_task_status_to_completed(self,username):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        db.reference("/employee").child(username).child("project").child("task").child("status").set("Completed")
        db.reference("/employee").child(username).child("project").child("progress").set(db.reference("/employee").child(username).child("project").child("progress").get()+10)
        messagebox.showinfo("Employee Window", "Task Status set to Completed")
        

    def submit_survey(self, username):
        # Check if a submit survey window is already open, if it is open destroy it
        if hasattr(self, "self.submit_survey_window"):
            try:
                if self.submit_survey_window.winfo_exists():
                    self.submit_survey_window.destroy()  # Close the main login window
            except:
                pass

        # Create a new window for the submit_survey top level
        self.submit_survey_window = tk.Toplevel()
        self.submit_survey_window.geometry("800x600")  # Set the window size
        self.submit_survey_window.title("Submit Survey")
        self.submit_survey_window = self.submit_survey_window

        # Create the canvas
        self.submit_survey_canvas = tk.Canvas(self.submit_survey_window, bg="white", highlightthickness=0)
        self.submit_survey_canvas.pack(fill=tk.BOTH, expand=True)

        # Pull child classes from Survey_Qs in the db using the .get function
        survey_questions = db.reference("/Survey_Qs").get()
        
        # Get the total number of questions from the database
        total_questions = db.reference("/Survey_Qs").child("total_questions").get()
        self.total_questions = total_questions

        # total_questions_count = self.total_questions
        self.total_questions_count = int(total_questions)
        
        # Store the keys of the survey questions in a list
        survey_questions_keys = [str(i) for i in range(total_questions)]

        # Set the current question index to -1
        self.current_question_index = -1

        # Bind the window resize event to the function
        self.submit_survey_window.bind("<Configure>", lambda event: self.display_survey_questions(survey_questions_keys, survey_questions, username))
        
        # Bind the Escape key to the exit function
        self.submit_survey_window.bind("<Escape>", lambda event: self.submit_survey_window.destroy())

        # Check if buttons have already been created
        if not hasattr(self, 'buttons_created_down') or not self.buttons_created_down:
            # Create a frame within the canvas to contain the buttons
            button_frame = tk.Frame(self.submit_survey_canvas, bg="white")
            button_frame.pack(pady=20, side=tk.BOTTOM)

        
            # In the part where you create the next_button, make it an attribute of the class
            self.next_button = tk.Button(button_frame, text="Next", command=lambda: self.next_question(survey_questions_keys, survey_questions, username))
            self.next_button.grid(row=0, column=1)

            # Create a button to go to the previous question also pass the survey_questions_keys, survey_questions as arguments
            self.previous_button = tk.Button(button_frame, text="Previous", command=lambda: self.previous_question(survey_questions_keys, survey_questions, username))
            self.previous_button.grid(row=0, column=0)

            # Create a button to submit the survey at the bottom center of the window
            submit_button = tk.Button(button_frame, text="Submit", command=lambda: self.submit_survey_request(username))
            submit_button.grid(row=0, column=2)

        # Set the flag to indicate that buttons have been created
        self.buttons_created_down = True
        
        # Focus on the window
        self.submit_survey_window.focus_force()

        # Center the window
        self.center_window_all(self.submit_survey_window)

        # Main loop for the self.submit_survey_window
        self.submit_survey_window.mainloop()


    def resize_canvas_and_image_submit_survey(self,):

        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_submit_survey_logo_image = Image.open(img_path)

        # Get the submit_survey window size
        window_width = self.submit_survey_canvas.winfo_width()
        window_height = self.submit_survey_canvas.winfo_height()
            # Resize the image if needed
        resized_image = self.original_submit_survey_logo_image.resize(
            (window_width, window_height)
        )
        self.submit_survey_logo_image = ImageTk.PhotoImage(resized_image)

        # Redraw the image
        self.submit_survey_canvas.create_image(
            0, 0, image=self.submit_survey_logo_image, anchor="nw"
        )
        
    def display_survey_questions(self, survey_questions_keys, survey_questions, username):
        # Clear only the text from the canvas
        self.submit_survey_canvas.delete("all")
        
        # Resize canvas and image
        self.resize_canvas_and_image_submit_survey()

        # Check if the current question index is out of bounds
        if self.current_question_index < 0:
            self.current_question_index = 0
        elif self.current_question_index >= len(survey_questions_keys):
            self.current_question_index = len(survey_questions_keys) - 1

        # Get the current question key
        current_question_key = survey_questions_keys[self.current_question_index]

        # Display the question on the canvas
        question_text = f"Question {self.current_question_index + 1}: {survey_questions[current_question_key]}"
        self.submit_survey_canvas.create_text(
            10,
            10,
            text=question_text,
            font=("Helvetica", 14, "bold"),
            fill="white",
            anchor="nw",
        )

        # Check if buttons have already been created
        if not hasattr(self, 'buttons_created') or not self.buttons_created:
            # Create a frame within the canvas to contain the buttons
            button_frame = tk.Frame(self.submit_survey_canvas, bg="white")
            button_frame.pack(pady=20, side=tk.BOTTOM)

            # Create radio buttons for each question
            self.radio_var = tk.StringVar()
            self.radio_var.set(None)  # Set default value

            options = ["Very Poor", "Poor", "Average", "Good", "Very Good"]
            for i, option in enumerate(options):
                tk.Radiobutton(
                    self.submit_survey_canvas,
                    text=option,
                    variable=self.radio_var,
                    radio_var=None,
                    value=option,
                    command=lambda value=option: self.store_selected_value(value)
                ).place(x=20, y=50 + i * 30)


        # Set the flag to indicate that buttons have been created
        self.buttons_created = True


    def next_question(self,survey_questions_keys, survey_questions,username):

         # Increment the current question index
        self.current_question_index += 1     

            # Clear the selected radio button
        self.clear_selected_radio_button()

        # Display the next question
        self.display_survey_questions(survey_questions_keys, survey_questions,username)

    def previous_question(self,survey_questions_keys, survey_questions,username):
        # Decrement the current question index
        self.current_question_index -= 1

            # Clear the selected radio button
        self.clear_selected_radio_button()

        # Display the previous question
        self.display_survey_questions(survey_questions_keys, survey_questions,username)

    def clear_selected_radio_button(self):
        # Check if a value is selected for the current question
        stored_value = self.selected_values.get(self.current_question_index)

        if self.current_question_index == self.total_questions_count-1:
            self.next_button.config(state="disabled")
            return
        else:
            self.next_button.config(state="normal")

        if self.current_question_index == 0:
            self.previous_button.config(state="disabled")
            return
        else:
            self.previous_button.config(state="normal")

        # If a value is present, set the radio variable to that value
        if stored_value is not None and stored_value in ["Very Poor", "Poor", "Average", "Good", "Very Good"]:
            self.radio_var.set(stored_value)
        else:
            # Otherwise, clear the selected radio button by setting the variable to None
            self.radio_var.set(None)

    def on_window_resize_submit_survey(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_submit_survey()


    def submit_survey_request(self, username):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to the database.")
            return

        # Check if there are any unanswered questions
        if len(self.selected_values) != self.total_questions:
            messagebox.showinfo("Employee Window", "Please answer all questions.")
            return

        # Show a message that the survey has been submitted
        messagebox.showinfo("Employee Window", "Survey submitted successfully.")
        
        # Store the selected values in the database
        db.reference("/employee").child(username).child("survey").set(self.selected_values)

        # Set the value of the "available" key in the survey to False
        db.reference("/employee").child(username).child("survey").child("available").set("No")

        # Clear the selected values and reset the current question index
        self.buttons_created = False
        self.current_question_index = 0

        # Destroy the survey window
        self.submit_survey_window.destroy()

            
    def store_selected_value(self, value):
        #store the selected value in relation to the question index
        self.selected_values[self.current_question_index] = value

    def submit_complaint(self,username):
        # Create a new window for the submit_complaint top level
        submit_complaint_window = tk.Toplevel()
        submit_complaint_window.geometry("800x600")
        submit_complaint_window.title("Submit Complaint")
        
        #create the canvas
        self.submit_complaint_canvas = tk.Canvas(submit_complaint_window, bg="white", highlightthickness=0)
        self.submit_complaint_canvas.pack(fill=tk.BOTH, expand=True)
        
        #load the image
        self.submit_complaint_load_image()
        
        #create an entry to take the employees name whose complaint is being submitted
        self.employee_name_entry = tk.Entry(self.submit_complaint_canvas)
        self.employee_name_entry.pack(pady=10, side=tk.TOP, anchor=tk.CENTER)
        self.employee_name_entry.insert(0, "Complaint against Employee")
        self.employee_name_entry.bind("<FocusIn>", lambda event:self.employee_name_entry_del())
        
        # Create entry widget for complaint
        self.complaint_entry = tk.Entry(self.submit_complaint_canvas, width=50, font=("Helvetica", 14))
        self.complaint_entry.pack(pady=20, side=tk.TOP, anchor=tk.CENTER)
        self.complaint_entry.insert(0, "Complaint")
        self.complaint_entry.bind("<FocusIn>", lambda event: self.complaint_entry_del())  # Delete the default value when the user clicks on the entry widget
        
        # Create a button to submit the complaint
        submit_button = tk.Button(self.submit_complaint_canvas, text="Submit", command=lambda: self.submit_complaint_request(username,submit_complaint_window))
        submit_button.pack(pady=20, side=tk.TOP, anchor=tk.CENTER)
        
        # Bind the Escape key to the exit function
        submit_complaint_window.bind("<Escape>", lambda event: submit_complaint_window.destroy())
        
        # bind window resize event to function
        submit_complaint_window.bind("<Configure>", lambda event: self.on_window_resize_submit_complaint(event))
        
        # focus on window
        submit_complaint_window.focus_force()
        
        # Center the window with function center_window_test
        self.center_window_all(submit_complaint_window)
        
        # Run the main loop for the submit_complaint_window
        submit_complaint_window.mainloop()
        
    def submit_complaint_load_image(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_submit_complaint_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_submit_complaint()
        
    def resize_canvas_and_image_submit_complaint(self):
        # Get the submit_complaint window size
        window_width = self.submit_complaint_canvas.winfo_width()
        window_height = self.submit_complaint_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.submit_complaint_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_submit_complaint_logo_image.resize(
            (window_width, window_height)
        )
        self.submit_complaint_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.submit_complaint_canvas.delete("all")
        self.submit_complaint_canvas.create_image(
            0, 0, image=self.submit_complaint_logo_image, anchor="nw"
        )
        
    def on_window_resize_submit_complaint(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_submit_complaint()
        
    def submit_complaint_request(self,username, submit_complaint_window):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        # Retrieve the entered values
        employee_name = self.employee_name_entry.get()
        complaint = self.complaint_entry.get()
        manager= (db.reference("/manager").get()).keys()
        employee= (db.reference("/employee").get()).keys()
        if employee_name not in manager and employee_name not in employee:
            messagebox.showinfo("Employee Window", "Employee does not exist.")
        # Check if the complaint is valid
        if not employee_name or employee_name == "Complaint against Employee":
            messagebox.showinfo("Employee Window", "Please enter an employee name.")
        elif not complaint or complaint == "Complaint":
            messagebox.showinfo("Employee Window", "Please enter a complaint.")
        else:
            if employee_name in manager:
                if db.reference("/manager").child(employee_name).child("complaint").child("status").get() == "pending":
                    messagebox.showinfo("Employee Window", "A complaint against this employee is already pending.")
                    return
                if db.reference("/manager").child(employee_name).child("complaint").child("status").get() == "warned":
                    messagebox.showinfo("Employee Window", "This employee has already been warned.")
                    return
                # Add the complaint to the database
                db.reference("/manager").child(employee_name).child("complaint").child("problem").set(complaint)
                db.reference("/manager").child(employee_name).child("complaint").child("status").set("pending")
                db.reference("/manager").child(employee_name).child("complaint").child("complaint_by").set(username)
                messagebox.showinfo("Employee Window", "Complaint submitted successfully.")
                submit_complaint_window.destroy()
            else:
                if db.reference("/employee").child(employee_name).child("complaint").child("status").get() == "pending":
                    messagebox.showinfo("Employee Window", "A complaint against this employee is already pending.")
                    return
                if db.reference("/employee").child(employee_name).child("complaint").child("status").get() == "warned":
                    messagebox.showinfo("Employee Window", "This employee has already been warned.")
                    return
                # Add the complaint to the database
                db.reference("/employee").child(employee_name).child("complaint").child("problem").set(complaint)
                db.reference("/employee").child(employee_name).child("complaint").child("status").set("pending")
                db.reference("/employee").child(employee_name).child("complaint").child("complaint_by").set(username)
                messagebox.showinfo("Employee Window", "Complaint submitted successfully.")
                submit_complaint_window.destroy()
        
    def employee_name_entry_del(self):
        if self.employee_name_entry.get() == "Complaint against Employee":
            self.employee_name_entry.delete(0, tk.END)
            
    def complaint_entry_del(self):
        if self.complaint_entry.get() == "Complaint":
            self.complaint_entry.delete(0, tk.END)

    def submit_performance_review(self, username):
        # Create a new window for the submit_performance_review top level
        submit_performance_review_window = tk.Toplevel()
        submit_performance_review_window.geometry("900x600")
        submit_performance_review_window.title("Submit Performance Review")

        # Create the canvas
        self.submit_performance_review_canvas = tk.Canvas(submit_performance_review_window, bg="white", highlightthickness=0)
        self.submit_performance_review_canvas.pack(fill=tk.BOTH, expand=True)

        # Load the image
        self.submit_performance_review_load_image()

        # Create a dropdown menu for the performance review
        options = ["Select Type", "Quarterly Review", "Annual Review"]
        selected_option = tk.StringVar()
        selected_option.set(options[0])

        dropdown_menu = tk.OptionMenu(self.submit_performance_review_canvas, selected_option, *options)
        dropdown_menu.pack(pady=50, side=tk.TOP, anchor=tk.CENTER)

        # Create entry widgets for the performance review, constructed feedback, and goals
        entry_labels = ["Self Review", "Other Feedback", "Goals for the Future"]
        entry_variables = [tk.StringVar() for _ in range(3)]
        entry_widgets = []

        # for i in range(3):
        #     entry_widget = tk.Entry(self.submit_performance_review_canvas, width=50, font=("Helvetica", 14), textvariable=entry_variables[i])
        #     entry_widget.pack(pady=40, side=tk.TOP, anchor=tk.CENTER)
        #     entry_widget.insert(0, entry_labels[i])
        #     entry_widget.bind("<FocusIn>", lambda event, i=i: self.entry_del(entry_widget, entry_labels[i]))

        #     entry_widgets.append(entry_widget)

        for i in range(3):
            entry_widget = tk.Entry(self.submit_performance_review_canvas, width=50, font=("Helvetica", 14), textvariable=entry_variables[i])
            entry_widget.pack(pady=40, side=tk.TOP, anchor=tk.CENTER)
            entry_widget.insert(0, entry_labels[i])
            entry_widget.bind("<FocusIn>", lambda event, entry_widget=entry_widget, default_text=entry_labels[i]: self.entry_del(entry_widget, default_text))

            entry_widgets.append(entry_widget)


        # Create a button to submit the performance review
        submit_button = tk.Button(self.submit_performance_review_canvas, text="Submit", command=lambda: self.submit_performance_review_request(username, selected_option.get(), entry_variables, submit_performance_review_window))
        submit_button.pack(pady=20, side=tk.TOP, anchor=tk.CENTER)

        # Bind the Escape key to the exit function
        submit_performance_review_window.bind("<Escape>", lambda event: submit_performance_review_window.destroy())

        # bind window resize event to function
        submit_performance_review_window.bind("<Configure>", lambda event: self.on_window_resize_submit_performance_review(event))

        # focus on window
        submit_performance_review_window.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(submit_performance_review_window)

        # Run the main loop for the submit_performance_review_window
        submit_performance_review_window.mainloop()

    def submit_performance_review_load_image(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_submit_performance_review_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_submit_performance_review()

    def resize_canvas_and_image_submit_performance_review(self):
        # Get the submit_performance_review window size
        window_width = self.submit_performance_review_canvas.winfo_width()
        window_height = self.submit_performance_review_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.submit_performance_review_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_submit_performance_review_logo_image.resize(
            (window_width, window_height)
        )
        self.submit_performance_review_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.submit_performance_review_canvas.delete("all")
        self.submit_performance_review_canvas.create_image(
            0, 0, image=self.submit_performance_review_logo_image, anchor="nw"
        )

        # Information labels
        self.submit_performance_review_canvas.create_text(
            window_width / 2,
            20,
            text="Submit Performance Review",
            font=("Helvetica", 20, "bold"),
            fill="white",
        )

        self.submit_performance_review_canvas.create_text(
            window_width / 2,
            140,
            text="Self Review:",
            font=("Helvetica", 14, "bold"),
            fill="white",
        )

        self.submit_performance_review_canvas.create_text(
            window_width / 2,
            245,
            text="Feedback:",
            font=("Helvetica", 14, "bold"),
            fill="white",
        )

        self.submit_performance_review_canvas.create_text(
            window_width / 2,
            350,
            text="Goals:",
            font=("Helvetica", 14, "bold"),
            fill="white",
        )

    def on_window_resize_submit_performance_review(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_submit_performance_review()

    def entry_del(self, entry_widget, default_text):
        current_content = entry_widget.get()
        if current_content == default_text:
            entry_widget.delete(0, tk.END)

    def submit_performance_review_request(self, username, selected_option, entry_variables, submit_performance_review_window):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        # Retrieve the entered values
        performance_review = entry_variables[0].get()
        constructed_feedback = entry_variables[1].get()
        goals_for_future = entry_variables[2].get()

        # Check if the values are entered and valid
        if not performance_review or performance_review == "Performance Review":
            messagebox.showinfo("Employee Window", "Please enter a performance review.")
        elif not constructed_feedback or constructed_feedback == "Constructed Feedback":
            messagebox.showinfo("Employee Window", "Please enter constructed feedback.")
        elif not goals_for_future or goals_for_future == "Goals for the Future":
            messagebox.showinfo("Employee Window", "Please enter goals for the future.")
        elif selected_option == "Select Type":
            messagebox.showinfo("Employee Window", "Please select a type.")
        else:
            # Add the performance review details to the database
            db.reference("/employee").child(username).child("performance_review").child(selected_option).set({
                "performance_review": performance_review,
                "constructed_feedback": constructed_feedback,
                "goals_for_future": goals_for_future
            })
            db.reference("/employee").child(username).child("performance_review").child(selected_option).child("status").set("filled")
            messagebox.showinfo("Employee Window", "Performance review submitted successfully.")

            # Close the submit_performance_review_window
            submit_performance_review_window.destroy()
        
    def center_window_all(self, window):
        # Get the width and height of the screen
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Calculate the x and y coordinates to center the main window
        x = (screen_width / 2) - (900 / 2)
        y = (screen_height / 2) - (700 / 2)

        # Set the dimensions of the screen and where it is placed
        window.geometry("%dx%d+%d+%d" % (900, 700, x, y))

    def days_entry_del(self):
        if self.number_of_days_entry.get() == "0":
            self.number_of_days_entry.delete(0, tk.END)

    def reason_entry_del(self):
        if self.reason_entry.get() == "Vacation reason":
            self.reason_entry.delete(0, tk.END)
        if self.reason_entry.get() == "Reason for resignation":
            self.reason_entry.delete(0, tk.END)

    def date_entry_del(self):
        if self.date_entry.get() == "mm/dd/yyyy":
            self.date_entry.delete(0, tk.END)

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
        
        self.change_password_button = tk.Button(
            self.profile_canvas,
            text="Change Password",
            command=lambda: self.change_password(username),
            font=("Helvetica", 14),
            bd=0,
            fg="white",
            bg="black",
            activebackground="black",
        )
        #Place the button extreme top right of the screen
        self.change_password_button.place(relx=0.95, rely=0.05, anchor="ne")
        
        # Focus on window
        profile_dialog.focus_force()
        
        # Center the window with function center_window_test
        self.center_window_all(profile_dialog)
        
        # Bind the Escape key to the exit function
        profile_dialog.bind("<Escape>", lambda event: profile_dialog.destroy())
        
        # Run the main loop for the profile window
        profile_dialog.mainloop()
        
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
        self.original_change_password_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_change_password()
        
    def resize_canvas_and_image_change_password(self):
        # Get the change_password window size
        window_width = self.change_password_canvas.winfo_width()
        window_height = self.change_password_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.change_password_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_change_password_logo_image.resize(
            (window_width, window_height)
        )
        self.change_password_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.change_password_canvas.delete("all")
        self.change_password_canvas.create_image(
            0, 0, image=self.change_password_logo_image, anchor="nw"
        )
        
    def on_window_resize_change_password(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_change_password()
        
    def change_password_request(self, username, entry_variables, change_password_window):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        # Retrieve the entered values
        old_password = entry_variables[0].get()
        new_password = entry_variables[1].get()
        confirm_new_password = entry_variables[2].get()

        # Check if the values are entered and valid
        if not old_password or old_password == "Old Password":
            messagebox.showinfo("Employee Window", "Please enter the old password.")
        elif not new_password or new_password == "New Password":
            messagebox.showinfo("Employee Window", "Please enter the new password.")
        elif not confirm_new_password or confirm_new_password == "Confirm New Password":
            messagebox.showinfo("Employee Window", "Please confirm the new password.")
        elif new_password != confirm_new_password:
            messagebox.showinfo("Employee Window", "The new password and confirm new password do not match.")
        elif old_password == new_password:
            messagebox.showinfo("Employee Window", "The new password cannot be the same as the old password.")
        else:
            # Update the password in the database
            db.reference("/employee").child(username).child("password").set(new_password)
            messagebox.showinfo("Employee Window", "Password changed successfully.")

            # Close the self.change_password_window
            self.change_password_window.destroy()
    
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
        resigning_date=db.reference("/employee").child(username).child("resigning_date").get()
        text1=f"EID: {list[0]}\nName: {username}\nRole: {role}\nDesignation: {list[1]}\nSalary: {list[2]}\nHours Attended: {list[3]}\nBonus: {list[4]}\nSick Days: {list[5]}\nVacation Days: {list[6]}"
        if resigning_date is not None:
            text1+=f"\nResigning Date: {resigning_date}"
        if role=="employee":
            text1+=f"\nSurvey: {list[7]}"
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
        
    def logout(self,employee_window):
        #Close all windows
        employee_window.destroy()
        messagebox.showinfo("Employee Window", "You have been logged out.")
        Main.main(True)
        
def main(role,username):
    employee=Employee_class()
    employee.open_employee_window(role,username,"employee")
        