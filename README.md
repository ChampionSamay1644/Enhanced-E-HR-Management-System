
# ENHANCED E-HR MANAGEMENT SYSTEM

The Enhanced E-HR system is a user-friendly HR software made with Python. It helps manage HR tasks easily, with secure login and different access levels for users. The design adjusts to different screen sizes and stores data safely using Firebase. Different users have different functions, like admins, HR staff, managers, and employees. They can access their specific tools after logging in. Admins can control user details centrally using Firebase.

## Features

We have 4 hierarchies in our project:

1. **Admin:**
   - Create & Remove HR logins
   - Admin can log in as HR/Manager/Employee

2. **HR:**
   - Salary Management
   - Employee Add/Remove
   - Approve bonus/promotion/resignations
   - Employee hours attended
   - Survey/feedbacks/complaints checking

3. **Manager:**
   - Performance review
   - Approve vacation & resignations
   - Apply for promotion of Employee
   - Request for bonus

4. **Employee:**
   - Sick/Personal Leave
   - Apply for vacation & resignations
   - Submit Survey/feedbacks/complaints

## Roadmap

1. **Initialization:** Login screen helps to identify if the user is Admin, HR, Manager, or Employee.
2. **Database:** The user is then given the features with respect to its login details.
3. **Features:** These are differentiated between Admin, HR, Manager, and Employee respectively.
4. **Admin:** This user can remove or add login details of HR/Manager/Employee, sign in as per what permission level is desired, and approve resignation.
5. **HR:** This user can Add or remove manager/employee, manage salary and approve feedbacks, etc.
6. **Manager:** This user can View performance, approve for vacation/sick leaves or resignations, bonus or promotions, etc.
7. **Employee:** This user can check progress, apply for leaves, submit survey, or apply for vacations, etc.

## Optimizations

We have used Python 3.12 with pil for better optimizations and tkinter to provide smooth functioning of the interface to our system. Tkinter is used to create widgets like buttons, combo box, tables, labels, etc.

We have used Firebase for storing and accessing the database into our system.

## Setup Instructions for Specific Database

To run our project using your specific database, follow these steps:

1. **Install Python and Required Modules:**
   - Install Python 3.12 or higher on your system.
   - Install the necessary Python modules:
     - `firebase_admin`: Use `pip install firebase_admin` to install this module.
     - `tkinter`: This module is typically included in standard Python installations.
     - `pillow`: Use `pip install pillow` to install this module.

2. **Create Your Database in Firebase:**
   - Sign in to your Firebase account or create a new one at [Firebase Console](https://console.firebase.google.com/).
   - Create a new project and set up a Firebase Realtime Database for storing data.
   - Obtain your Firebase project credentials (API key, database URL, etc.) from the Firebase Console.

3. **Replace Links in the Main File:**
   - Open the main Python file (`main.py` or similar) in your project.
   - Replace the Firebase configuration details in the file with your own Firebase project credentials. Example:
     ```python
     # Initialize Firebase with your credentials
     cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
     firebase_admin.initialize_app(cred, {
         'databaseURL': 'https://your-firebase-project.firebaseio.com/'
     })
     ```

4. **Run the Main File:**
   - Once you have installed Python, set up the modules, created your Firebase database, and updated the main file with your credentials, you can run the main Python file.
   - Use the command `python main.py` (replace `main.py` with your actual main file name) to execute the HR Management System application.

## System Requirements

### Hardware:
- **Minimum Requirements:**
  - Processor: Dual-core processor @2.4Ghz
  - RAM: 4GB RAM
  - Storage: 2GB free space
  - Internet Speed: 3mbps

- **Recommended Requirements:**
  - Processor: Quad-core processor @2.8Ghz
  - RAM: 8GB RAM
  - Storage: 4GB free space
  - Internet Speed: 6mbps

### Software:
- **Minimum Requirements:**
  - OS: Windows 10 22H2
  - Python: Version 3.11 with pil, firebase, firebase_admin, and tkcalendar modules installed

- **Recommended Requirements:**
  - OS: Windows 11 22H2
  - Python: Version 3.12 with pil, firebase, firebase_admin, and tkcalendar modules installed

## Download and Installation
1. Go to the [Releases](https://github.com/ChampionSamay1644/Sem_4_Mini_Project/releases) section of this repository.
2. Download the latest executable file (Enhanced.E-HR.Management.System.exe).
3. Double-click the downloaded file to launch the application.

## Usage
1. Log in with appropriate credentials based on user role.
2. Explore the functionalities tailored for Admin, HR, Manager, and Employee users.
3. Report any issues or bugs on the GitHub repository.

## Contributing

1. **Armaan Nakhuda:**
   - Exit and Credits button on the login screen
   - Resizing, centering, and focusing of all windows
   - Manager Window
   - 50% of

 Employee window
   - Documentation and ppt (error checking)
   - Research Paper

2. **Sushant Navle:**
   - Basic Login page and admin login screen (no buttons)
   - Documentation
   - PPT
   - Research Paper

3. **Samay Pandey:**
   - Implementation and connection of DB
   - Dynamic name on every window
   - Admin window
   - HR window
   - 50% of Employee window
   - Documentation and ppt (flowcharts error checking)
   - Research Paper

4. **Peeyush Karnik:**
   - Documentation
   - PPT

## 🔗 Links
Individual Profile Links:
- [Armaan Nakhuda](https://github.com/Armaan4477)
- [Sushant Navle](https://github.com/Sushant305)
- [Samay Pandey](https://github.com/ChampionSamay1644)

## Appendix
The motivation behind the development of the Enhanced E-HR system stems from the growing need for organizations to optimize and modernize their human resource management processes. As businesses evolve in today's dynamic environment, efficient HR management becomes crucial for organizational success. Traditional manual methods are often time-consuming, prone to errors, and lack scalability. The Enhanced E-HR system aims to address these challenges by providing a comprehensive, user-friendly, and technologically advanced solution.
