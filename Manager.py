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

class Manager_class:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Manager Window")
        
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
    
    def open_manager_window(self, role, username,uni_role):
        self.uni_role=uni_role
        if hasattr(self, "root"):
            try:
                if self.root.winfo_exists():
                    self.root.destroy()  # Close the main login window
            except:
                pass    
        self.manager_window = tk.Tk()  # Use Tk() to create a new window
        self.manager_window.geometry("900x600")  # Set the window size
        self.manager_window.title("Manager Window")

        #create a canvas that resizes with the window
        self.manager_logo_canvas = tk.Canvas(self.manager_window, bg="white", highlightthickness=0)
        self.manager_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # import the image as the background on the canvas
        self.load_image_manager(username)

        #center the window with function center_window_test
        self.center_window_all(self.manager_window)

        # bind window resize event to function
        self.manager_window.bind("<Configure>", lambda event: self.on_window_resize_manager(event,username))

        # Buttons using grid manager
        self.perform_review_approval_button = tk.Button(
            self.manager_logo_canvas, text="Performance Review Approval", command=lambda:self.perform_review_approval(), font=("Helvetica", 14)
        )
        self.perform_review_approval_button.place(relx=0.25, rely=0.2, anchor="center", width=300, height=50)

        self.approve_vacations_sick_leaves_button = tk.Button(
            self.manager_logo_canvas, text="Approve Vacation/Sick Leaves", command=lambda:self.approve_vacations_sick_leaves(username,role), font=("Helvetica", 14)
        )
        self.approve_vacations_sick_leaves_button.place(relx=0.75, rely=0.2, anchor="center", width=300, height=50)

        self.progress_on_resignation_button = tk.Button(
            self.manager_logo_canvas, text="Apply for Resignation", command=lambda:self.apply_for_resignation(username), font=("Helvetica", 14)
        )
        self.progress_on_resignation_button.place(relx=0.25, rely=0.4, anchor="center", width=300, height=50)

        self.assign_promotion_button = tk.Button(
            self.manager_logo_canvas, text="Assign Promotion", command=lambda:self.assign_promotion(username), font=("Helvetica", 14)
        )
        self.assign_promotion_button.place(relx=0.75, rely=0.4, anchor="center", width=300, height=50)

        self.approve_resignation_button = tk.Button(
            self.manager_logo_canvas, text="Approve Resignation", command=lambda:self.approve_resignation(), font=("Helvetica", 14)
        )
        self.approve_resignation_button.place(relx=0.25, rely=0.6, anchor="center", width=300, height=50)

        self.request_bonus_button = tk.Button(
            self.manager_logo_canvas, text="Request for Bonus", command=lambda:self.request_bonus(), font=("Helvetica", 14)
        )
        self.request_bonus_button.place(relx=0.75, rely=0.6, anchor="center", width=300, height=50)

        self.submit_performance_review_button = tk.Button(
            self.manager_logo_canvas, text="Submit Performance Review", command=lambda:self.submit_performance_review(username), font=("Helvetica", 14)
        )
        self.submit_performance_review_button.place(relx=0.5, rely=0.8, anchor="center", width=300, height=50)

        profile_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "profile.png")
        profile_image = Image.open(profile_path)
        profile_image = profile_image.resize((50, 50))
        profile_image = ImageTk.PhotoImage(profile_image)
        profile_button = tk.Button(
            self.manager_logo_canvas,
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
            self.manager_logo_canvas,
            image=logout_image,
            command=lambda: self.logout(self.manager_window),
            bd=0,
            bg="white",
            activebackground="white",
        )
        logout_button.image = logout_image
        logout_button.pack()
        logout_button.place(relx=0.95, rely=0.95, anchor="se")
        
        # focus on window
        self.manager_window.focus_force()

        # Center the window with function center_window_test
        self.center_window_all(self.manager_window)

        # Bind the Escape key to the exit function
        self.manager_window.bind("<Escape>", lambda event: self.manager_window.destroy())

        if db.reference("/manager").child(username).child("resignation_request").child("resignation_status").get() == "Approved by HR":
            date=db.reference("/manager").child(username).child("resignation_request").child("resignation_date").get()
            messagebox.showinfo(f"Resignation Request", "Resignation request has been approved by Admin.\nYou will be logged out on "+date)
            
            #Check if the date is today or past
            #If yes, then logout the user
            if datetime.datetime.now().date() >= datetime.datetime.strptime(date, "%Y-%m-%d").date():
                messagebox.showinfo("Resignation Request", "You have been logged out as per your resignation request and cannot login again.")
                self.manager_window.destroy()
                return
        if db.reference("/manager").child(username).child("complaint").child("complaint_status").get() == "warned":
            messagebox.showinfo(f"Complaint", "You have been warned by HR because of a submitted complaint.")
            db.reference("/manager").child(username).child("complaint").child("complaint_status").set("None")
            
        # Run the main loop for the manager window
        self.manager_window.mainloop()

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
            50,
            text=f"Welcome {username_manager}!",
            font=("Helvetica", 28, "bold"),
            fill="white",
        )

    def on_window_resize_manager(self, event,username):
        # Handle window resize event
        self.resize_canvas_and_image_manager(username)

    def perform_review_approval(self):
        self.tree=None
        # create a new window to show the performance review approval
        self.review_approval_window = tk.Toplevel()
        self.review_approval_window.geometry("800x600")  # Set the window size
        self.review_approval_window.title("Performance Review Approval")

        #create a canvas that resizes with the window
        self.review_approval_logo_canvas = tk.Canvas(self.review_approval_window, bg="white", highlightthickness=0)
        self.review_approval_logo_canvas.pack(fill=tk.BOTH, expand=True)

        # bind window resize event to function
        self.review_approval_window.bind("<Configure>", lambda event: self.on_window_resize_review_approval(event))

        # import the image as the background on the canvas
        self.load_image_review_approval()

        # Bind the Escape key to the exit function
        self.review_approval_window.bind(
            "<Escape>", lambda event: self.review_approval_window.destroy()
        )
        # focus on window
        self.review_approval_window.focus_force()
        # Center the window with function center_window_test
        self.center_window_all(self.review_approval_window)

        #Create a treeview to hold the list of employees
        self.tree = ttk.Treeview(self.review_approval_logo_canvas, columns=("Employee", "Role", "Type"))
        self.tree.heading("Employee", text="Employee")
        self.tree.heading("Role", text="Role")
        self.tree.heading("Type", text="Type")
        self.tree.column("Employee", width=200)
        self.tree.column("Role", width=200)
        self.tree.column("Type", width=200)
        self.tree.tag_configure("selectable", background="white", foreground="blue")
        self.tree.bind("<Double-1>", lambda event: self.on_treeview_click(event))
        self.tree['show'] = 'headings'

        #Create 2 scrollbars for the treeview
        ysb = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        ysb.pack(side="right", fill="y")

        xsb = ttk.Scrollbar(self.tree, orient="horizontal", command=self.tree.xview)
        xsb.pack(side="bottom", fill="x")

        self.tree.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
        
        #Pack the treeview onto the scrollable frame
        self.tree.pack(fill="both", expand=True)
        
        #Place the treeview on the window
        self.tree.place(width=600, height=400, relx=0.5, rely=0.5, anchor="center")

        #Bind the treeview to the function to show employee details
        # self.tree.bind("<ButtonRelease-1>", self.on_treeview_click)
        
        #Create a combo box to select the type of performance review
        self.review_type = tk.StringVar()
        self.review_type.set("None")
        self.review_type_combo = ttk.Combobox(self.review_approval_window, textvariable=self.review_type, values=["None","Quarterly Review", "Annual Review"])
        self.review_type_combo.pack(pady=20)
        self.review_type_combo.place(relx=0.5, rely=0.1, anchor="center") 
        self.review_type_combo.bind("<<ComboboxSelected>>", self.on_review_type_selected)
         
        # Run the main loop for the create_remove_hr_window
        self.review_approval_window.mainloop()
    
    def on_treeview_click(self,event):
        #Get the selected employee from the treeview
        try:
            employee=self.tree.item(self.tree.selection())["values"][0]
            type=self.tree.item(self.tree.selection())["values"][2]
            if db.reference("/employee").child(employee).child("performance_review").child(type).child("status").get() == "Approved by Manager ":
                messagebox.showinfo("Performance Review Approval", "Performance Review has already been approved for "+employee)
                return
            self.open_employee_review(employee,type)
        except:
            pass
        
    def on_review_type_selected(self, event):
        if self.review_type.get() == "None":
            self.tree.delete(*self.tree.get_children())
            return
        elif self.review_type.get() == "Quarterly Review":
            self.populate_treeview("Quarterly Review")
        elif self.review_type.get() == "Annual Review":
            self.populate_treeview("Annual Review")
            
    def populate_treeview(self,type):
        self.tree.delete(*self.tree.get_children())
        if type == "Quarterly Review":
            employee_data_8 = list((db.reference("/employee").get()).keys())
            for employee in employee_data_8:
                if db.reference("/employee").child(employee).child("performance_review").child("Quarterly Review").child("status").get() == "filled":
                    self.tree.insert("", "end", values=(employee, "Employee","Quarterly Review"), tags="selectable")
                # self.tree.insert("", "end", values=(employee, "Employee","Quaterly Review"), tags="selectable")
                
        elif type == "Annual Review":
            employee_data_9 = list((db.reference("/employee").get()).keys())
            for employee in employee_data_9:
                if db.reference("/employee").child(employee).child("performance_review").child("Annual Review").child("status").get() == "filled":
                    self.tree.insert("", "end", values=(employee, "Employee","Annual Review"), tags="selectable")
                # self.tree.insert("", "end", values=(employee, "Employee","Annual Review"), tags="selectable")
        
    def open_employee_review(self, employee, type):
        # create a new window to show employee details along with 2 radio buttons to approve or deny the request
        self.employee_review_window = tk.Toplevel()
        self.employee_review_window.geometry("800x600")
        self.employee_review_window.title("Employee Review")
        
        # create a canvas that resizes with the window
        self.employee_review_logo_canvas = tk.Canvas(self.employee_review_window, bg="white", highlightthickness=0)
        self.employee_review_logo_canvas.pack(fill=tk.BOTH, expand=True)
        
        # load the image as the background on the canvas
        self.load_image_employee_review()
        
        # bind window resize event to function
        self.employee_review_window.bind("<Configure>", lambda event: self.on_window_resize_employee_review(event))
        
        # center the window with function center_window_test
        self.center_window_all(self.employee_review_window)
        
        # focus on window
        self.employee_review_window.focus_force()
        
        # bind the Escape key to the exit function
        self.employee_review_window.bind("<Escape>", lambda event: self.employee_review_window.destroy())
        
        performance_review_label = tk.Label(
            self.employee_review_logo_canvas,
            text="Performance Review",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        performance_review_label.pack(pady=20)
        performance_review_label.place(relx=0.5, rely=0.2, anchor="center")
        
        self.performance_review_entry = tk.Entry(
            self.employee_review_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.performance_review_entry.pack(pady=20)
        self.performance_review_entry.place(width=500, relx=0.5, rely=0.25, anchor="center")
        
        # Get the performance review from the employee data
        performance_review = db.reference("/employee").child(employee).child("performance_review").child(type).child(
            "performance_review").get()
        self.performance_review_entry.insert(0, performance_review)
        self.performance_review_entry.configure(state="readonly", justify="center")
        
        feedback_label = tk.Label(
            self.employee_review_logo_canvas,
            text="Constructed Feedback",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        feedback_label.pack(pady=20)
        feedback_label.place(relx=0.5, rely=0.35, anchor="center")
        
        self.feedback_entry = tk.Entry(
            self.employee_review_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.feedback_entry.pack(pady=20)
        self.feedback_entry.place(width=500, relx=0.5, rely=0.4, anchor="center")
        
        # Get the feedback from the employee data
        feedback = db.reference("/employee").child(employee).child("performance_review").child(type).child(
            "constructed_feedback").get()
        self.feedback_entry.insert(0, feedback)
        self.feedback_entry.configure(state="readonly", justify="center")
        
        future_goals_label = tk.Label(
            self.employee_review_logo_canvas,
            text="Goals for Future",
            font=("Helvetica", 12, "bold"),
            bg="white",
        )
        future_goals_label.pack(pady=20)
        future_goals_label.place(relx=0.5, rely=0.5, anchor="center")
        
        self.future_goals_entry = tk.Entry(
            self.employee_review_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.future_goals_entry.pack(pady=20)
        self.future_goals_entry.place(width=500, relx=0.5, rely=0.55, anchor="center")
        
        # Get the future goals from the employee data
        future_goals = db.reference("/employee").child(employee).child("performance_review").child(type).child(
            "goals_for_future").get()
        self.future_goals_entry.insert(0, future_goals)
        self.future_goals_entry.configure(state="readonly", justify="center")
        
        # Create 2 buttons to approve or deny the performance review
        self.approve_button = tk.Button(
            self.employee_review_window,
            text="Approve",
            command=lambda employee=employee, type=type: self.approve_performance_review(employee, type),
            font=("Helvetica", 14),
        )
        self.approve_button.pack(
            pady=20
        )
        self.approve_button.place(relx=0.5, rely=0.8, anchor="center", width=100, height=30)
        
        self.deny_button = tk.Button(
            self.employee_review_window,
            text="Deny",
            command=lambda employee=employee, type=type: self.deny_performance_review(employee, type),
            font=("Helvetica", 14),
        )
        self.deny_button.pack(
            pady=20
        )
        self.deny_button.place(relx=0.5, rely=0.9, anchor="center", width=100, height=30)
        
        # Run the main loop for the create_remove_hr_window
        self.employee_review_window.mainloop()
    
    def approve_performance_review(self,employee,type):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        #Ask for confirmation before approving the performance review
        if messagebox.askyesno("Performance Review Approval", "Are you sure you want to approve the performance review for "+employee+"?"):
            #Update the status of the performance review to Approved
            db.reference("/employee").child(employee).child("performance_review").child(type).update({"status":"Approved by Manager"})
            messagebox.showinfo("Performance Review Approval", "Performance Review has been approved for "+employee)
            
        self.employee_review_window.destroy()
        self.review_approval_window.focus_force()
    
    def deny_performance_review(self,employee,type):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        #ask for confirmation before denying the performance review using pyqt5 messagebox
        if messagebox.askyesno("Performance Review Approval", "Are you sure you want to deny the performance review for "+employee+"?"):
            #Ask for the reason for denying the performance review
            reason = simpledialog.askstring("Performance Review Approval", "Enter the reason for denying the performance review for "+employee)
            if reason == None or reason == "" or reason.isspace() or reason == " ":
                messagebox.showinfo("Performance Review Approval", "Please enter a reason for denying the performance review for "+employee)
                self.employee_review_window.destroy()
                self.review_approval_window.focus_force()
                return
            #Update the status of the performance review to Denied
            db.reference("/employee").child(employee).child("performance_review").child(type).update({"status":"Denied by Manager","reason":reason})
            messagebox.showinfo("Performance Review Approval", "Performance Review has been denied for "+employee)
            
        self.employee_review_window.destroy()
        self.review_approval_window.focus_force()
            
    def load_image_employee_review(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_employee_review_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_employee_review()
        
    def resize_canvas_and_image_employee_review(self):
        # Get the manager window size
        window_width = self.employee_review_logo_canvas.winfo_width()
        window_height = self.employee_review_logo_canvas.winfo_height()
        
        # Resize the canvas to the current window size
        self.employee_review_logo_canvas.config(width=window_width, height=window_height)
        
        # Resize the image if needed
        resized_image = self.original_employee_review_logo_image.resize(
            (window_width, window_height)
        )
        self.employee_review_logo_image = ImageTk.PhotoImage(resized_image)
        
        # Update the image on the canvas
        self.employee_review_logo_canvas.delete("all")
        self.employee_review_logo_canvas.create_image(
            0, 0, image=self.employee_review_logo_image, anchor="nw"
        )
        
    def on_window_resize_employee_review(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_employee_review()

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
            self.employee_details_logo_canvas, font=("Helvetica", 12, "bold"),justify="center",width=60
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
            self.employee_details_logo_canvas, font=("Helvetica", 12, "bold"),justify="center",width=60
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
            self.employee_details_logo_canvas, font=("Helvetica", 12, "bold"),justify="center",width=60
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
            self.employee_details_logo_canvas, font=("Helvetica", 12, "bold"),justify="center",width=60
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
            self.employee_details_logo_canvas, font=("Helvetica", 12, "bold"),justify="center",width=60
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
            self.employee_details_logo_canvas, font=("Helvetica", 12, "bold"),justify="center",width=60
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
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
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
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
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
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
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
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
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

    def apply_for_resignation(self,username):
        self.resignation_window = tk.Toplevel()
        self.resignation_window.geometry("800x600")  # Set the window size
        self.resignation_window.title("Resignation Progress")
        
        #create a canvas that resizes with the window
        self.resignation_logo_canvas = tk.Canvas(self.resignation_window, bg="white", highlightthickness=0)
        self.resignation_logo_canvas.pack(fill=tk.BOTH, expand=True)
        
        #load the image as the background on the canvas
        self.load_image_resignation()
        
        # bind window resize event to function
        self.resignation_window.bind("<Configure>", lambda event: self.on_window_resize_resignation(event))
        
        # bind the escape key to the exit function
        self.resignation_window.bind("<Escape>", lambda event: self.resignation_window.destroy())
        
        # focus on window
        self.resignation_window.focus_force()
        
        # Center the window with function center_window_test
        self.center_window_all(self.resignation_window)
        
        # Create an entry widget for the reason and align it to the center and make it multiple line entry with height 5 and scrollbar
        self.reason_for_resignation_entry = scrolledtext.ScrolledText(self.resignation_window, wrap=tk.WORD, width=40, height=5, font=("Helvetica", 12, "bold"))
        self.reason_for_resignation_entry.pack(pady=20)
        self.reason_for_resignation_entry.place(relx=0.5, rely=0.5, anchor="center")
        self.reason_for_resignation_entry.insert(tk.INSERT, "Enter reason for resignation")
        self.reason_for_resignation_entry.bind("<FocusIn>", lambda event: self.reason_for_resignation_entry.delete(1.0, tk.END))
        
        #Create a new button for submitting the resignation
        self.submit_resignation_button = tk.Button(
            self.resignation_window,
            text="Submit",
            command=lambda:self.submit_resignation(username),
            font=("Helvetica", 14),
        )
        self.submit_resignation_button.pack(
            pady=20
        )
        self.submit_resignation_button.place(relx=0.5, rely=0.6, anchor="center", width=100, height=30)
        
        # Run the main loop for the self.resignation_window
        self.resignation_window.mainloop()
        
    def submit_resignation(self,username):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        # Get the reason for resignation from the entry widget
        reason_for_resignation = self.reason_for_resignation_entry.get("1.0", tk.END)
        if db.reference("/manager").child(username).child("resignation_request").child("resignation_reason").get() == "pending":
            # Show an error message if the resignation is already pending
            messagebox.showerror("Error", "Your resignation is already pending.")
            return
        if not reason_for_resignation:
            # Show an error message if the reason is empty
            messagebox.showerror("Error", "Please enter a reason for resignation.")
            return
        if reason_for_resignation == "no":
            # Show an error message if the reason is empty
            messagebox.showerror("Error", "Please enter a reason for resignation.")
            return
        # Update the resignation reason in the database
        mng_ref = db.reference("/manager")
        mng_ref.child(username).child("resignation_request").child("resignation_reason").set(reason_for_resignation)
        mng_ref.child(username).child("resignation_request").child("resignation_status").set("pending")
        
        # Close the resignation window
        self.resignation_window.destroy()
        
        # Show a message that the resignation has been submitted
        messagebox.showinfo("Resignation Submitted", "Your resignation has been submitted successfully.")
        
    def load_image_resignation(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_resignation_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_resignation()
        
    def resize_canvas_and_image_resignation(self):
        # Get the resignation window size
        window_width = self.resignation_logo_canvas.winfo_width()
        window_height = self.resignation_logo_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.resignation_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_resignation_logo_image.resize(
            (window_width, window_height)
        )
        self.resignation_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.resignation_logo_canvas.delete("all")
        self.resignation_logo_canvas.create_image(
            0, 0, image=self.resignation_logo_image, anchor="nw"
        )
        
    def on_window_resize_resignation(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_resignation()

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

        # Create a new entry for new salary and designation
        self.new_salary_entry = tk.Entry(
            self.promote_employee_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.new_salary_entry.pack(pady=20)
        self.new_salary_entry.place(relx=0.5, rely=0.45, anchor="center")
        self.new_salary_entry.insert(0, "New Salary")
        
        #Delete the text in the entry widget when clicked
        self.new_salary_entry.bind("<Button-1>", lambda event: self.new_salary_entry.delete(0, tk.END))

        # Create a new entry for new designation
        self.new_designation_entry = tk.Entry(
            self.promote_employee_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.new_designation_entry.pack(pady=20)
        self.new_designation_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.new_designation_entry.insert(0, "New Designation")
        
        #Delete the text in the entry widget when clicked
        self.new_designation_entry.bind("<Button-1>", lambda event: self.new_designation_entry.delete(0, tk.END))

        # Create a comment box for the manager to add reason for promotion
        self.comment_box = tk.Text(
            self.promote_employee_logo_canvas, font=("Helvetica", 12, "bold")
        )
        self.comment_box.pack(pady=20)
        self.comment_box.place(relx=0.5, rely=0.7, anchor="center", relwidth=0.8, relheight=0.2)
        self.comment_box.insert(tk.END, "Reason for Promotion") 
        
        #Delete the text in the entry widget when clicked
        self.comment_box.bind("<Button-1>", lambda event: self.comment_box.delete("1.0", tk.END))

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
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        #Get the entered values from the self.promote_employee_window
        new_salary = self.new_salary_entry.get()
        new_designation = self.new_designation_entry.get()
        comment = self.comment_box.get("1.0", "end-1c")
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
                "request_by": username_mngr,
            })
            messagebox.showinfo("Promote Employee", "Employee Promotion Request Sent")
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
        
    def approve_resignation(self):
        # create a new window to show the resignation request
        self.approve_resignation_window = tk.Toplevel()
        self.approve_resignation_window.geometry("800x600")  # Set the window size
        self.approve_resignation_window.title("Approve Resignation")
        
        #create a canvas that resizes with the window
        self.approve_resignation_logo_canvas = tk.Canvas(self.approve_resignation_window, bg="white", highlightthickness=0)
        self.approve_resignation_logo_canvas.pack(fill=tk.BOTH, expand=True)
        
        # import the image as the background on the canvas
        self.load_image_approve_resignation()
        
        # bind window resize event to function
        self.approve_resignation_window.bind("<Configure>", lambda event: self.on_window_resize_approve_resignation(event))
        
        # bind the escape key to the exit function
        self.approve_resignation_window.bind("<Escape>", lambda event: self.approve_resignation_window.destroy())
        
        # focus on window
        self.approve_resignation_window.focus_force()
        
        # Center the window with function center_window_test
        self.center_window_all(self.approve_resignation_window)
        
        # Create a scrollable frame to hold the treeview
        scrollable_frame = tk.Frame(self.approve_resignation_window, bg="white")
        scrollable_frame.pack(fill="both", expand=True)
        scrollable_frame.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)
        
        # Create a new treeview to show the list of employees
        self.treeview_approve_resignation = ttk.Treeview(
            scrollable_frame, columns=("Employee","Reason"), show="headings", selectmode="browse"
        )
        self.treeview_approve_resignation.heading("Employee", text="Employee")
        self.treeview_approve_resignation.heading("Reason", text="Reason")
        self.treeview_approve_resignation.column("Employee", width=200, anchor="center")
        self.treeview_approve_resignation.column("Reason", width=600, anchor="center")
        self.treeview_approve_resignation.tag_configure("clickable", foreground="blue", font=("Helvetica", 12, "underline"))
        #self.treeview_approve_resignation.bind("<Double-1>", lambda event: self.open_employee_details_window(self.treeview_approve_resignation.item(self.treeview_approve_resignation.selection())["values"][0]))
        
        #bind the treeview to a function that enables the approve button
        self.treeview_approve_resignation.bind("<<TreeviewSelect>>", lambda event: self.enable_approve_resignation_button())
        
        # Add a vertical scrollbar to the Treeview
        scrollbar = ttk.Scrollbar(scrollable_frame, orient="vertical", command=self.treeview_approve_resignation.yview)
        scrollbar.pack(side="right", fill="y")
        self.treeview_approve_resignation.configure(yscrollcommand=scrollbar.set)
        
        # Add a horizontal scrollbar to the Treeview
        scrollbar = ttk.Scrollbar(scrollable_frame, orient="horizontal", command=self.treeview_approve_resignation.xview)
        scrollbar.pack(side="bottom", fill="x")
        self.treeview_approve_resignation.configure(xscrollcommand=scrollbar.set)
        
        # Pack the Treeview to the scrollable frame
        self.treeview_approve_resignation.pack(fill="both", expand=True)
        
        # Configure grid row and column weights
        scrollable_frame.grid_rowconfigure(0, weight=1)
        scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # Now you can safely use self.treeview
        self.treeview_approve_resignation.delete(*self.treeview_approve_resignation.get_children())
        
        # Populate the treeview with employee data
        self.populate_employee_resignation_list()
        
        # Create a new button for approving the resignation
        self.approve_button = tk.Button(
            self.approve_resignation_window,
            text="Approve",
            command=lambda:self.approve_resignation_request(),
            font=("Helvetica", 14),
            state="disabled",
        )
        self.approve_button.pack(
            pady=20
        )
        self.approve_button.place(relx=0.5, rely=0.9, anchor="center", width=100, height=30)
        
        # Run the main loop for the approve_resignation_window
        self.approve_resignation_window.mainloop()
    
    def enable_approve_resignation_button(self):
        self.approve_button.config(state="normal")
        
    def populate_employee_resignation_list(self):
        employees = list((db.reference("/employee").get()).keys())
        for employee in employees:
            if db.reference("/employee").child(employee).child("resignation_request").child("resignation_status").get() == "pending":
                reason = db.reference("/employee").child(employee).child("resignation_request").child("resignation_reason").get()
                #Conver the reason to a single line string
                reason = reason.replace("\n", " ")
                self.treeview_approve_resignation.insert("", "end", values=(employee,reason), tags=("clickable",))
        
    def approve_resignation_request(self):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        # get the selected employee from the treeview
        selected_employee = self.treeview_approve_resignation.item(self.treeview_approve_resignation.selection())["values"][0]
        if db.reference("/employee").child(selected_employee).child("resignation_request").child("resignation_status").get() == "Approved by Manager":
            messagebox.showinfo("Approve Resignation", "Resignation Request already approved")
            self.approve_resignation_window.focus_force()
            return
        if messagebox.askokcancel("Approve Resignation", "Are you sure you want to approve the resignation request?"):
            if db.reference("/employee").child(selected_employee).child("resignation_request").child("resignation_status").get() == "pending":
                #Update the resignation request in the database
                emp_ref = db.reference("/employee")
                emp_ref.child(selected_employee).child("resignation_request").update({"resignation_status": "Approved by Manager"})
                messagebox.showinfo("Approve Resignation", "Resignation Request Approved")
        self.approve_resignation_window.focus_force()
    
    def load_image_approve_resignation(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_approve_resignation_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_approve_resignation()
        
    def resize_canvas_and_image_approve_resignation(self):
        # Get the approve_resignation window size
        window_width = self.approve_resignation_logo_canvas.winfo_width()
        window_height = self.approve_resignation_logo_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.approve_resignation_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_approve_resignation_logo_image.resize(
            (window_width, window_height)
        )
        self.approve_resignation_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.approve_resignation_logo_canvas.delete("all")
        self.approve_resignation_logo_canvas.create_image(
            0, 0, image=self.approve_resignation_logo_image, anchor="nw"
        )
        
    def on_window_resize_approve_resignation(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_approve_resignation()

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
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        # Get the entered values from the Entry widgets
        amount_bonus = self.bonus_amount_entry.get()
        reason_bonus = self.reason_entry.get()
        
        if amount_bonus == "" or reason_bonus == "":
            messagebox.showerror("Error", "Please enter a valid amount and reason for the bonus")
            return
        if amount_bonus == "":
            messagebox.showerror("Error", "Please enter a valid amount for the bonus")
            return
        if amount_bonus.isnumeric() == False:
            messagebox.showerror("Error", "Please enter a valid amount for the bonus")
            return
        if db.reference("/employee").child(employee_name).child("bonus_req").get() != None:
            messagebox.showerror("Error", "Bonus Request already sent")
            return
        #put if conditions to handle non integer values, non input in the amount_bonus
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
            emp_ref.child(employee_name).update({"bonus_req": int(amount_bonus)})
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

    def submit_performance_review(self,username):
        # create a new window to show the performance review
        self.performance_review_window = tk.Toplevel()
        self.performance_review_window.geometry("800x600")
        self.performance_review_window.title("Submit Performance Review")
        
        # create a canvas that resizes with the window
        self.performance_review_logo_canvas = tk.Canvas(self.performance_review_window, bg="white", highlightthickness=0)
        self.performance_review_logo_canvas.pack(fill=tk.BOTH, expand=True)
        
        # import the image as the background on the canvas
        self.load_image_performance_review()
        
        # bind window resize event to function
        self.performance_review_window.bind("<Configure>", lambda event: self.on_window_resize_performance_review(event))
        
        # bind the escape key to the exit function
        self.performance_review_window.bind("<Escape>", lambda event: self.performance_review_window.destroy())
        
        # focus on window
        self.performance_review_window.focus_force()
        
        # Center the window with function center_window_test
        self.center_window_all(self.performance_review_window)
        
        # Create dropdown options for the performance review
        options=["Select Type", "Quarterly Review", "Annual Review"]
        selected_option = tk.StringVar()
        selected_option.set(options[0])
        dropdown = tk.OptionMenu(self.performance_review_window, selected_option, *options)
        dropdown.pack(pady=20)
        dropdown.place(relx=0.5, rely=0.1, anchor="center")
        
        # Create entry widgets for the performance review, constructed feedback, and goals
        entry_labels = ["Self Review", "Other Feedback", "Goals for the Future"]
        entry_variables = [tk.StringVar() for _ in range(3)]
        entry_widgets = []

        for i in range(3):
            #Place the entry widgets on the canvas below the dropdown
            #Also make the entry widgets bigger
            entry = tk.Entry(self.performance_review_logo_canvas, textvariable=entry_variables[i], font=("Helvetica", 12))
            entry.pack(pady=20)
            entry.place(relx=0.5, rely=0.2 + i * 0.1, anchor="center", relwidth=0.8, relheight=0.05)
            entry.insert(0, entry_labels[i])
            entry.bind("<Button-1>", lambda event, i=i: entry.delete(0, tk.END))
            entry_widgets.append(entry)

        # Create a button to submit the performance review
        submit_button = tk.Button(self.performance_review_logo_canvas, text="Submit", command=lambda: self.submit_performance_review_request(selected_option.get(), entry_variables,username), font=("Helvetica", 14))
        submit_button.pack(pady=20)
        submit_button.place(relx=0.5, rely=0.8, anchor="center", width=100, height=30)
        
        # Run the main loop for the performance_review_window
        self.performance_review_window.mainloop()
    
    def submit_performance_review_request(self, selected_option, entry_variables,username):
        if self.uni_role == "admin":
            messagebox.showerror("Error", "You are logged in as Admin.\nYou cannot make changes to database.")
            return
        # Retrieve the entered values
        self_review = entry_variables[0].get()
        other_feedback = entry_variables[1].get()
        goals = entry_variables[2].get()
        
        #Check if the values are valid
        if not self_review or self_review == "Performance Review":
            messagebox.showinfo("Manager Window", "Please enter a performance review.")
        elif not other_feedback or other_feedback == "Constructed Feedback":
            messagebox.showinfo("Manager Window", "Please enter constructed feedback.")
        elif not goals or goals == "Goals for the Future":
            messagebox.showinfo("Manager Window", "Please enter goals for the future.")
        elif selected_option == "Select Type":
            messagebox.showinfo("Manager Window", "Please select a type.")
        else:
            # Add the performance review details to the database
            db.reference("/manager").child(username).child("performance_review").child(selected_option).set({
                "performance_review": self_review,
                "constructed_feedback": other_feedback,
                "goals_for_future": goals
            })
            db.reference("/manager").child(username).child("performance_review").child(selected_option).child("status").set("filled")
            messagebox.showinfo("Manager Window", "Performance review submitted successfully.")

            # Close the submit_performance_review_window
            self.performance_review_window.destroy()
            
    def load_image_performance_review(self):
        # Construct the full path to the image file based on role and username
        img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "HR_background.png")

        # Load image and adjust canvas size
        self.original_performance_review_logo_image = Image.open(img_path)
        self.resize_canvas_and_image_performance_review()
        
    def resize_canvas_and_image_performance_review(self):
        # Get the performance_review window size
        window_width = self.performance_review_logo_canvas.winfo_width()
        window_height = self.performance_review_logo_canvas.winfo_height()

        # Resize the canvas to the current window size
        self.performance_review_logo_canvas.config(width=window_width, height=window_height)

        # Resize the image if needed
        resized_image = self.original_performance_review_logo_image.resize(
            (window_width, window_height)
        )
        self.performance_review_logo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas
        self.performance_review_logo_canvas.delete("all")
        self.performance_review_logo_canvas.create_image(
            0, 0, image=self.performance_review_logo_image, anchor="nw"
        )
        
    def on_window_resize_performance_review(self, event):
        # Handle window resize event
        self.resize_canvas_and_image_performance_review()
        
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

        list=self.getdata(username,self.uni_role)
        text1=f"EID: {list[0]}\nName: {username}\nRole: {role}\nDesignation: {list[1]}\nSalary: {list[2]}\nHours Attended: {list[3]}\nBonus: {list[4]}\nSick Days: {list[5]}\nVacation Days: {list[6]}"
        if self.uni_role == "manager":
            resigning_date=db.reference("/manager").child(username).child("resignation_request").child("resignation_date").get()
            if resigning_date != None:
                text1=text1+f"\nResignation Date: {resigning_date}"
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
            
    def logout(self,manager_window):
        #Close all windows
        self.manager_window.destroy()
        messagebox.showinfo("Logout", "You have been logged out")
        Main.main(True)
        
def main(role,username):
    manager=Manager_class()
    manager.open_manager_window(role,username,"manager")