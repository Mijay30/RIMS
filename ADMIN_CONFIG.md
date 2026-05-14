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

## 🚀 Environment Setup for macOS
1. **Python Environment**: Use `python3 -m venv .venv` and `source .venv/bin/activate`.
2. **Library Requirements**: Ensure `python-multipart` is installed.
3. **Database Reset**: Delete `rims_database.db` to trigger a fresh schema initialization.

---

## 👨‍💻 Development Team
* **Popa Mihai**: Security & Admin UI.
* **Stanel Mihai**: Backend & Mapping.
* **Stefan David**: Frontend & Fleet Management.
