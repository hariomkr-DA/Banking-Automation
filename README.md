**Banking Automation System (Python GUI + SQLite)**

Project Overview

This is a GUI-based Banking Management System built using Python's Tkinter for the interface and SQLite for data storage.
The system provides login-based access for two roles: Admin and User. 
Each has their own dashboard with a dedicated set of functionalities. 
Email notifications are used for sending account details and password recovery.


---

User Roles
==================
Admin Features:
------------------------

	Open New Account

	Delete Existing Account

	View All Accounts

	Add Balance to a User Account

	Update System Email or Password

	View User Issues or Complaints

	Logout


User Features:
------------------------
	Profile Picture Display

	Welcome Message

	View Personal Account Details include password or balance

	Update Personal Information

	Withdraw Money

	Transfer Money to Another Account

	View Transaction History

	Logout



---

Login Screen Features
========================
	Dropdown to select role: Admin or User

	Input fields: Account Number, Password

	CAPTCHA field

  **Buttons**:

		Login

		Forgot Password

		Open New Account

		Clear All Fields




---

**Project Folder Structure**

**project/**
├── main_project.py         # Main application GUI logic
├── mail_messages.py        # Email sending and message formatting
├── project_table.py        # Database table creation and query logic
├── My_bank_Database.sqlite # SQLite database storing all records
└── Images/                 # Folder containing images/icons/profile photos


---

Technologies Used

Component	Technology

Programming	Python 3.x
GUI Framework	Tkinter
Database	SQLite
Email Service	smtplib (SMTP)
Image Handling	PIL, Tkinter
Input Validation	Regex, Manual



---

**Functional Flow (Outline)**

**1. Login Flow**

	User selects role (Admin/User)

	Enters account number, password, and CAPTCHA

	If credentials match:

	Redirect to Admin Dashboard or User Dashboard

	Else: Show login error message



**2. Admin Dashboard**

	Add or remove user accounts

	View list of all users

	Add balance to a specific account

	Update system-wide email/password

	View and respond to user-submitted issues

	Logout option


**3. User Dashboard**

	Welcome message with profile photo
	
	Change Profile Pic

	View own account details

	Update name, phone, email etc.

	Withdraw funds

	Transfer money to another user

	View past transaction history

	Logout option


**4. Account Creation (User)**

	Fill form: Name, Aadhaar, PAN, Email, Mobile, Address

	Input validation performed on fields

	Account number and password generated

	Information sent via email


**5. Forgot Password**

	User enters valid account number

	Credentials are verified

	OTP sent to the email address



---

Email Notification System

When a new account is opened, the system sends:

Account Number

Password


For password recovery, system sends credentials to registered email

Uses smtplib for sending secure messages



---

Security Features

CAPTCHA validation at login screen

Input format validation (Aadhaar, PAN, mobile, email)

Password fields are masked on screen

Email is only sent to the verified address on file



