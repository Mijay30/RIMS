# 📖 RIMS User Manual

This guide provides instructions on how to navigate and use the Road Infrastructure Management System (RIMS).

---

## 👤 User Role (Citizens)
* **Goal**: Report road hazards to the authorities.
* **Actions**:
    1. Log in with your personal credentials.
    2. Use the map to locate a hazard.
    3. Click on the map to open the 'Report Incident' form.
    4. Fill in the Hazard Type (Pothole, Damaged Sign, etc.) and Description.
    5. Submit. The incident will appear on the map with a 'Reported' status.

## 👷 Staff Role (Intervention Teams)
* **Goal**: Manage and resolve reported incidents.
* **Actions**:
    1. Log in with your assigned Staff account.
    2. Click on a 'Reported' incident on the map.
    3. Use the **Allocate** button to assign a nearby team and vehicle.
    4. Advance the incident status using the **Start Intervention** and **Mark as Done** buttons.
    5. A success notification will appear once the status reaches 'Completed'.

## ⚡ Admin Role (Managers)
* **Goal**: System configuration and resource management.
* **Actions**:
    1. Log in with an Administrator account.
    2. Access the **Admin Dashboard** from the navigation bar.
    3. **Manage Fleet**: Add new specialized vehicles or check maintenance stats.
    4. **Manage Teams**: Add, deactivate, or update certifications for team members.
    5. View global statistics for infrastructure health.

---

## 🛠️ Troubleshooting
* **'No vehicle available nearby'**: Ensure you have added vehicles in the Admin Dashboard with coordinates near the incident location.
* **Missing Column Error**: If you see database errors, delete 'rims.db' and restart the server to trigger a fresh schema initialization.
