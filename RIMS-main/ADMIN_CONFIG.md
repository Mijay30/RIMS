# 🛠️ RIMS: Admin & System Configuration Manual

This document outlines the technical configuration and backend architecture of the Road Infrastructure Management System (RIMS).

---

## 🔑 Access Credentials (Development/Test)
Use these pre-configured accounts to test the triple-tier security system:
* **Administrator**: username: `admin` | password: `admin123`
* **Intervention Staff**: username: `staff` | password: `staff123`
* **Standard User**: username: `user` | password: `user123`

---

## 🏗️ Backend Architecture
* **Framework**: FastAPI (Python 3.12).
* **ORM**: SQLAlchemy with SQLite for local development.
* **Security**: OAuth2 with JWT (JSON Web Tokens) and passlib for password hashing.

## 🗄️ Database Schema Management
* **Table: 'users'**: Stores roles (Admin, Staff, User) and hashed credentials.
* **Table: 'incidents'**: Tracks hazard types, GPS coordinates, and lifecycle statuses.
* **Table: 'vehicles'**: Manages the specialized fleet and maintenance metadata.
* **Table: 'team_members'**: Stores HR data, including certification levels and availability.

## ⚙️ Role-Based Access Control (RBAC) Logic
* **Admin Access**: Full write/delete permissions on all tables.
* **Staff Access**: Update permissions for incident status and vehicle allocation.
* **User Access**: Write permissions only for reporting new incidents via the map.

## 🔄 Resource Management Automation
RIMS now features automated resource release logic (US 3 Logic) to streamline operations:
* **Automated Release**: When an incident status is transitioned to 'Completed' (via `LifecycleService`), the system automatically:
    * Sets the associated vehicle's `is_available` flag to `True`.
    * Resets the vehicle's `availability_status` to "Available".
    * Sets all assigned team members' `is_available` flag to `True`.
    * Resets team members' `availability_status` to "Active".
    * Updates the incident's `last_modified` timestamp.
* **CQ-19 Compliance**: All resource availability flags follow the `is_available` naming convention.

## 🚀 Environment Setup for macOS
1. **Python Environment**: Use `python3 -m venv .venv` and `source .venv/bin/activate`.
2. **Library Requirements**: Ensure `python-multipart` is installed.
3. **Database Reset**: Delete `rims_database.db` to trigger a fresh schema initialization.

---

## 👨‍💻 Development Team
* **Popa Mihai**: Security & Admin UI.
* **Stanel Mihai**: Backend & Mapping.
* **Stefan David**: Frontend & Fleet Management.
