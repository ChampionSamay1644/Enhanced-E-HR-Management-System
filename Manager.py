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
            self.manager_logo_canvas, text="Assign Promotion", command=lambda:self.assign_promotion(), font=("Helvetica", 14)
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
        messagebox.showinfo("manager Window", "Performance Review Approval Button Pressed")

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

    def assign_promotion(self):
        messagebox.showinfo("manager Window", "Approve Promotion Button Pressed")

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
        text1=f"EID: {list[0]}\nName: {username}\nRole: {role}\nDesignation: {list[1]}\nSalary: {list[2]}\nHours Attended: {list[3]}\nBonus: {list[4]}\nSick Days: {list[5]}\nVacation Days: {list[6]}"
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
def main(role,username):
    manager=Manager_class()
    manager.open_manager_window(role,username)