# RIMS: Road Infrastructure Management System 🛠️
**RIMS** is a comprehensive, full-stack solution designed for municipal authorities to manage, track, and resolve urban infrastructure issues efficiently.

## ✨ Key Features
### 🏢 Fleet & Team Management (US 1 & 4)
* Specialized Units: Management of heavy machinery like Asphalt-laying and Snow-removal vehicles.
* HR Module: Tracking of staff certifications (Senior/Junior) and real-time availability.

### 📍 Interactive Hazard Mapping (US 2)
* Incident Reporting: Citizens can report potholes, damaged signs, or fallen trees.
* Smart Allocation: Proximity-based algorithm for resource assignment.

### 🔄 Intervention Lifecycle (US 3)
* State Machine: Follows 'Reported' ➔ 'Assigned' ➔ 'In Progress' ➔ 'Completed'.
* Audit Trail: Automatic timestamping for operational transparency.

### 🔐 Multi-Tier Security
* RBAC Architecture: Distinct roles for Admin, Staff, and User.
* JWT Authentication: Secure login with encrypted password hashing.

## 🛠️ Tech Stack
* Backend: Python / FastAPI
* Database: SQLite with SQLAlchemy ORM (Chosen over MongoDB to ensure the requirement of 'running in any environment without external dependencies' for final evaluation)
* Frontend: HTML5, CSS3, JavaScript

## 📥 Installation
1. Clone the repo.
2. Run 'pip install -r requirements.txt'.
3. Run 'uvicorn app.main:app --reload'.

## 👥 Contributors
* **Popa Mihai** - Administrative Module Specialist: Responsible for the secure Login system, User Authentication logic, and UI Security integration.
* **Stanel Mihai** - Backend & Database Architect: Responsible for the SQL database schema, Mapping API integration, and Server-side logic for RIMS.
* **Stefan David** - Frontend & UI/UX Developer: Responsible for the Interactive Dashboard, Map visualization, Fleet statistics, and Responsive Design.
