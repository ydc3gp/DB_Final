# Laundry Management System

The back-end implementation of a Laundry Management System designed to simplify laundry management for college students. This system allows users to track laundry device usage, manage payments, submit feedback, and monitor machine status in campus buildings. Admins can manage users, resolve service requests, and oversee system performance.

---

## Features

### User Features:
- **Account Management**: Users can create and update their profiles.
- **Device Usage**: Students can start and monitor washer/dryer usage.
- **Payment System**: Supports payments for device usage with detailed history tracking.
- **Feedback System**: Users can submit feedback for system improvements.
- **Notifications**: Users receive important updates and notifications.

### Admin Features:
- **Service Requests**: Admins can manage and resolve service requests for devices.
- **User Management**: Manage student and admin accounts.
- **System Monitoring**: Track machine usage and status in real time.

---

## Database Schema

### Tables:
1. **Users**: Stores user information (email, phone number, profile picture).
2. **Student**: Extends `Users` with student-specific attributes (year, balance).
3. **Admin**: Extends `Users` with admin privileges.
4. **LaundryDevice**: Tracks washing and drying machines.
5. **WasherHistory**: Stores washing machine usage history.
6. **DryerHistory**: Stores drying machine usage history.
7. **Building**: Tracks campus buildings with laundry facilities.
8. **ServiceRequest**: Logs maintenance requests for machines.
9. **Feedback**: Captures user feedback for system improvements.
10. **Notification**: Sends notifications to users.
11. **Payment**: Logs payment details.
12. **Uses**: Tracks laundry device usage and associated payments.

---

## How to Run the Project

### Prerequisites:
- Python 3.x
- Flask
- SQL Server (or a compatible database system)
- Required Python libraries:
  - `requests`
  - `pyodbc`

### Steps:
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/laundry-management-system.git
   cd laundry-management-system
   ```

2. **Install Dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set Up the Database:**

- Execute the provided SQL schema in your SQL Server to create the required tables.
- Configure your database credentials in views.py and app.py under the connection string settings.

4. **Run the Flask Server:**
```bash
python app.py
```
5. **Access the API:**

- Open your browser or API testing tool (e.g., Postman) and navigate to http://127.0.0.1:5000.

6. **Test the Project:**
Use the Python utility functions in views.py to call the API endpoints and verify their functionality.
