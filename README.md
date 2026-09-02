# Assessment of Drinking Water Facility and Availability

A web-based Community Service Project (CSP) developed using **Python Flask, SQLite, HTML, CSS, and JavaScript** to assess drinking-water facility availability in villages and provide an easy way for people to report water-related problems.

The system provides water availability information, facility details, survey statistics, problem reporting, report tracking, village search, map-based facility locations, and an administrator dashboard.

---

## 📌 Project Overview

**Project Title:** Assessment of Drinking Water Facility and Availability

**Project Type:** Community Service Project (CSP)

**Technology:** Flask Web Application

**Primary Focus:** Drinking water facility availability and accessibility

The application is designed to help communities:

* Check the availability of drinking-water facilities.
* View the status of water facilities.
* Search for facilities and villages.
* View facility locations on a map.
* Report water-related problems.
* Track submitted complaints using a reference ID.
* View survey and household statistics.
* Allow administrators to update facility and complaint status.
* Use the website in **English and Telugu**.

---

## ✨ Features

### 🏠 Home Page

The homepage provides an overview of the water-facility situation.

It displays:

* Total water facilities
* Functional facilities
* Number of areas covered
* Number of households surveyed
* Quick access to water status
* Facility information
* Problem reporting

---

### 💧 Water Status

The Water Status page provides information about water facilities and their availability.

Users can view:

* Facility name
* Village
* Area
* Facility type
* Facility status
* Water availability
* Number of users served
* Last updated date
* Remarks

Availability categories include:

* Available
* Partially Available
* Not Available

Facility status includes:

* Functional
* Under Maintenance
* Non-functional

---

### 🏘️ Village and Area Information

The application supports village-based information.

Currently configured villages include:

* Bhimavaram
* Eluru
* Jalipudi
* Nuzvid
* Tadepalligudem
* Vijayawada

The primary survey/facility data is configured for **Jalipudi village**.

Jalipudi areas include:

* Main Street
* Riverside Colony
* North Hamlet
* School Road
* Market Road

---

### 🗺️ Map Integration

Water facilities and villages contain geographical coordinates.

The application can display facility locations using latitude and longitude information.

Example facility locations include:

* Main Street Tap
* Community Tank
* North Borewell
* School Facility
* Market Tap

---

### 🔎 Facility Search and Filtering

Users can search for facilities based on:

* Facility name
* Location/area
* Facility type

Facilities can also be filtered according to:

* Available
* Not Available
* Functional
* Non-functional

---

### 📢 Report a Problem

Users can report drinking-water-related problems through the reporting form.

The form supports:

* User name
* Location
* Problem category
* Problem description
* Date
* Optional image upload

After submission, the system generates a unique reference ID.

Example:

```text
WC-A1B2C3
```

This reference ID can be used to track the submitted report.

Supported image formats:

* JPG
* JPEG
* PNG
* WEBP

Maximum upload size:

```text
5 MB
```

---

### 🔍 Track Report

Users can enter their report reference ID to check the status of their complaint.

Report statuses include:

* Pending
* In Progress
* Resolved

Administrators can also add remarks to submitted reports.

---

### 📊 Survey Dashboard

The Survey page provides community-level statistics such as:

* Total households
* Households with regular water availability
* Households with irregular water availability
* Households experiencing shortage
* Functional facilities
* Non-functional facilities

Current survey categories include:

```text
Regular
Irregular
Shortage
```

---

### 👨‍💼 Admin Dashboard

The administrator dashboard allows authorized administrators to manage:

#### Reports

Administrators can:

* View submitted reports
* View report reference IDs
* View locations
* View categories
* View descriptions
* Change report status
* Add administrative remarks

#### Water Facilities

Administrators can update:

* Facility availability
* Facility status
* Last updated date

---

### 🌐 English and Telugu Support

The application supports two languages:

* English
* Telugu

Translation files are stored in:

```text
translations/en.json
translations/te.json
```

Users can switch between languages through the website.

---

## 🛠️ Technologies Used

### Frontend

* HTML5
* CSS3
* JavaScript
* Jinja2 Templates

### Backend

* Python
* Flask

### Database

* SQLite

### Other Technologies

* Browser Web Speech API
* Map/location data using latitude and longitude
* JSON-based translation files
* File upload functionality

---

## 📂 Project Structure

```text
Water/
│
├── app.py
├── database.db
├── requirements.txt
├── README.md
├── .gitignore
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       ├── main.js
│       └── map.js
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── water_status.html
│   ├── facilities.html
│   ├── report.html
│   ├── track.html
│   ├── survey.html
│   ├── login.html
│   └── admin.html
│
├── translations/
│   ├── en.json
│   └── te.json
│
└── uploads/
```

---

## 🗄️ Database

The project uses **SQLite** for storing application data.

The database contains the following main tables:

### `water_facilities`

Stores information about drinking-water facilities.

Important fields include:

* Facility name
* Location
* Facility type
* Status
* Availability
* Users served
* Last updated
* Remarks
* Latitude
* Longitude
* Village
* Area

### `reports`

Stores problems reported by users.

Important fields include:

* Reference ID
* User name
* Location
* Category
* Description
* Image
* Report date
* Status
* Admin remarks
* Created date

### `survey_data`

Stores community survey information.

Important fields include:

* Area
* Number of households
* Water availability
* Functional facilities
* Non-functional facilities
* Remarks

The application automatically initializes the required database tables when it starts.

---

## 🚀 Installation and Setup

### 1. Clone or Extract the Project

Open the project folder:

```text
Water
```

Open the folder in **Visual Studio Code**.

---

### 2. Check Python Installation

Make sure Python is installed.

Check using:

```powershell
python --version
```

---

### 3. Create a Virtual Environment

Run:

```powershell
python -m venv .venv
```

---

### 4. Activate the Virtual Environment

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If activation is successful, the terminal will show something similar to:

```text
(.venv)
```

---

### 5. Install Required Packages

Run:

```powershell
pip install -r requirements.txt
```

The main dependency is:

```text
Flask >= 3.0, < 4.0
```

---

### 6. Run the Application

Run:

```powershell
python app.py
```

The Flask development server will start.

Open the following address in your browser:

```text
http://127.0.0.1:5000/
```

---

## 🔐 Demo Administrator Login

The current application contains demo administrator credentials:

```text
Email: admin@watercare.demo
Password: admin123
```

> **Important:** These credentials are intended only for the demonstration/project version. For a real deployment, the password should be stored securely and authentication should be implemented using proper password hashing and user management.

---

## 🌐 Main Pages

| Page            | URL             | Purpose                         |
| --------------- | --------------- | ------------------------------- |
| Home            | `/`             | Project overview and statistics |
| Water Status    | `/water-status` | View water availability         |
| Facilities      | `/facilities`   | Search and filter facilities    |
| Report Problem  | `/report`       | Submit a water-related problem  |
| Track Report    | `/track`        | Track a submitted report        |
| Survey          | `/survey`       | View survey statistics          |
| Login           | `/login`        | Administrator login             |
| Admin Dashboard | `/admin`        | Manage reports and facilities   |
| Logout          | `/logout`       | End administrator session       |

---

## 📍 Sample Facility Data

The application contains demonstration data for Jalipudi village.

| Facility        | Area             | Type                     | Status            | Availability        |
| --------------- | ---------------- | ------------------------ | ----------------- | ------------------- |
| Main Street Tap | Main Street      | Public Water Tap         | Functional        | Available           |
| Community Tank  | Riverside Colony | Water Tank               | Functional        | Partially Available |
| North Borewell  | North Hamlet     | Borewell                 | Under Maintenance | Not Available       |
| School Facility | School Road      | Community Water Facility | Functional        | Available           |
| Market Tap      | Market Road      | Public Water Tap         | Non-functional    | Not Available       |

This data can be modified according to the actual field survey results.

---

## 🗣️ Language Support

Translation files are located at:

```text
translations/en.json
translations/te.json
```

English:

```text
en.json
```

Telugu:

```text
te.json
```

The application stores the selected language in the Flask session.

---

## 🎤 Voice Input

The reporting interface can use the browser's **Web Speech API** where supported.

This feature can help users who may find typing difficult, including users who are more comfortable speaking their problem.

Browser support may vary depending on the browser and device.

---

## 📸 Image Upload

Users can attach an image while reporting a problem.

Supported formats:

```text
.jpg
.jpeg
.png
.webp
```

Maximum file size:

```text
5 MB
```

Uploaded files are stored in:

```text
uploads/
```

---

## 🔄 Application Workflow

```text
User
  │
  ▼
Home Page
  │
  ├── Check Water Status
  │       │
  │       └── View Facilities / Map
  │
  ├── Search Facilities
  │
  ├── Report Problem
  │       │
  │       └── Generate Reference ID
  │
  └── Track Report
          │
          ▼
      Report Status


Administrator
     │
     ▼
   Login
     │
     ▼
Admin Dashboard
     │
     ├── Manage Reports
     │
     └── Update Facilities
```

---

## 🎯 Project Objectives

The major objectives of the project are:

1. To assess the availability of drinking-water facilities.
2. To provide easily accessible water-facility information.
3. To identify functional and non-functional facilities.
4. To collect and present community survey information.
5. To provide a simple problem-reporting mechanism.
6. To allow users to track their complaints.
7. To provide administrators with facility and complaint management.
8. To make information accessible through English and Telugu.
9. To provide location-based facility information.
10. To create a simple digital platform for community water-facility monitoring.

---

## 🌱 Community Benefits

The proposed system can help the community by:

* Improving access to water-facility information.
* Making it easier to report problems.
* Helping administrators identify reported issues.
* Providing a centralized record of water facilities.
* Supporting better monitoring of facility availability.
* Providing information in both English and Telugu.
* Making water-facility data easier to understand through statistics and visual presentation.

---

## 🔮 Future Enhancements

Possible future improvements include:

* Real-time government/public water department integration.
* Secure database authentication.
* Role-based access control.
* SMS or email notifications for complaint updates.
* Automatic GPS location detection.
* More advanced map functionality.
* Real-time facility availability updates.
* Mobile application version.
* Improved accessibility features.
* Additional Indian language support.
* Advanced analytics and reporting.
* Cloud database deployment.
* Secure production deployment using HTTPS.

---

## ⚠️ Important Note

The project currently contains **demonstration/sample data** in the database.

Before using the application for an actual community survey:

* Replace sample data with verified survey data.
* Update village and facility information.
* Change the demo administrator credentials.
* Configure a secure secret key.
* Review file-upload security.
* Use production-grade authentication.
* Disable Flask debug mode.

---

## 👩‍💻 Developed For

**Community Service Project (CSP)**

**Project:** Assessment of Drinking Water Facility and Availability

**Technology:** Flask + SQLite + HTML + CSS + JavaScript

---

## 📄 License

This project is intended for educational and academic purposes.
