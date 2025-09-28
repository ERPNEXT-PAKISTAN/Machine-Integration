<p align="center">
  <img src="https://img.icons8.com/external-flatart-icons-outline-flatarticons/64/000000/external-biometric-fingerprint-flatart-icons-outline-flatarticons.png" alt="Biometric Icon" width="80"/>
  <h1 align="center">ERPNext Biometric Integration App</h1>
  <p align="center"><em>Complete Guide</em></p>
</p>

---

## 📝 0 — Prerequisites (on Ubuntu / ERPNext server)

- <img src="https://img.icons8.com/ios-filled/18/228BE6/linux.png"/> **Ubuntu 22.04+** with sudo access  
- <img src="https://img.icons8.com/ios-filled/18/228BE6/console.png"/> **Bench + ERPNext** installed and running  
- <img src="https://img.icons8.com/ios-filled/18/228BE6/python.png"/> **Python 3.10+**  
- <img src="https://img.icons8.com/ios-filled/18/228BE6/git.png"/> **Git** installed  
  ```bash
  sudo apt install git
  ```
- <img src="https://img.icons8.com/ios-filled/18/228BE6/mind-map.png"/> Basic knowledge of ERPNext custom app creation

---

## 🛠️ 1 — Create New Custom App

```bash
cd ~/frappe-bench
bench new-app biometric_integration
bench --site yoursite install-app biometric_integration
```

---

## 📁 2 — App Folder Structure

```
biometric_integration/
   └── biometric_integration/
       ├── __init__.py
       ├── hooks.py
       ├── tasks.py
       ├── drivers/
       │     ├── __init__.py
       │     ├── zkteco.py
       │     ├── hikvision.py
       │     └── anviz.py
       └── biometric_integration/
             ├── doctype/
             │     ├── device_driver/
             │     │     └── device_driver.json
             │     └── attendance_device/
             │           └── attendance_device.json
```

---

## 🧩 3 — Device Driver Doctype (Child / Logic Config)

**Path:** `biometric_integration/doctype/device_driver/device_driver.json`

<details>
<summary><b>Show JSON <img src="https://img.icons8.com/material-rounded/16/228BE6/copy.png"/></b></summary>

```json
{
 "doctype": "DocType",
 "name": "Device Driver",
 "module": "Biometric Integration",
 "custom": 1,
 "fields": [
   {"fieldname": "driver_name", "fieldtype": "Data", "label": "Driver Name", "reqd": 1},
   {"fieldname": "python_module", "fieldtype": "Data", "label": "Python Module Path", "reqd": 1},
   {"fieldname": "connection_type", "fieldtype": "Select", "options": "SDK\nAPI\nSQL", "label": "Connection Type"},
   {"fieldname": "default_port", "fieldtype": "Int", "label": "Default Port"},
   {"fieldname": "notes", "fieldtype": "Small Text", "label": "Notes"}
 ]
}
```
</details>

---

## 🖧 4 — Attendance Device Doctype (Parent / Actual Device)

**Path:** `biometric_integration/doctype/attendance_device/attendance_device.json`

<details>
<summary><b>Show JSON <img src="https://img.icons8.com/material-rounded/16/228BE6/copy.png"/></b></summary>

```json
{
 "doctype": "DocType",
 "name": "Attendance Device",
 "module": "Biometric Integration",
 "custom": 1,
 "fields": [
   {"fieldname": "device_name", "fieldtype": "Data", "label": "Device Name", "reqd": 1},
   {"fieldname": "ip_address", "fieldtype": "Data", "label": "IP Address", "reqd": 1},
   {"fieldname": "port", "fieldtype": "Int", "label": "Port"},
   {"fieldname": "device_driver", "fieldtype": "Link", "options": "Device Driver", "label": "Device Driver"},
   {"fieldname": "location", "fieldtype": "Data", "label": "Location"},
   {"fieldname": "active", "fieldtype": "Check", "label": "Active"},
   {"fieldname": "last_sync_time", "fieldtype": "Datetime", "label": "Last Sync Time"}
 ]
}
```
</details>

---

## 🗂️ 5 — Optional Temp Log Doctype

**Path:** `biometric_integration/doctype/attendance_log_temp/attendance_log_temp.json`

<details>
<summary><b>Show JSON <img src="https://img.icons8.com/material-rounded/16/228BE6/copy.png"/></b></summary>

```json
{
 "doctype": "DocType",
 "name": "Attendance Log Temp",
 "module": "Biometric Integration",
 "custom": 1,
 "fields": [
   {"fieldname": "employee_id", "fieldtype": "Data", "label": "Employee ID"},
   {"fieldname": "punch_time", "fieldtype": "Datetime", "label": "Punch Time"},
   {"fieldname": "direction", "fieldtype": "Select", "options": "IN\nOUT", "label": "Direction"},
   {"fieldname": "device", "fieldtype": "Link", "options": "Attendance Device", "label": "Device"},
   {"fieldname": "synced_to_erpnext", "fieldtype": "Check", "label": "Synced to ERPNext"}
 ]
}
```
</details>

---

## 🔗 6 — <code>hooks.py</code>

**Path:** `biometric_integration/hooks.py`

```python
from . import __version__ as app_version

app_name = "biometric_integration"
app_title = "Biometric Integration"
app_publisher = "Your Name"
app_description = "Integrate Biometric Attendance Devices"
app_email = "you@example.com"
app_license = "MIT"

scheduler_events = {
    "cron": {
        "*/10 * * * *": ["biometric_integration.tasks.sync_all_devices"]
    }
}
```

---

## 🔄 7 — <code>tasks.py</code>

**Path:** `biometric_integration/tasks.py`

```python
import importlib
import frappe

def sync_all_devices():
    devices = frappe.get_all("Attendance Device", filters={"active": 1}, fields="*")
    for d in devices:
        driver = frappe.db.get_value("Device Driver", d.device_driver, ["python_module"], as_dict=True)
        if not driver:
            continue
        try:
            module = importlib.import_module(driver["python_module"])
            logs = module.sync(d)
            for log in logs:
                frappe.get_doc({
                    "doctype": "Employee Checkin",
                    "employee": log["employee_id"],
                    "time": log["timestamp"],
                    "log_type": log["direction"]
                }).insert(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(message=str(e), title=f"Sync failed for {d.device_name}")
```

---

## 🟢 8 — Driver: ZKTeco

**Path:** `biometric_integration/drivers/zkteco.py`

```python
def sync(device_config):
    return [
        {"employee_id": "E001", "timestamp": "2025-09-28 08:30:00", "direction": "IN"},
        {"employee_id": "E002", "timestamp": "2025-09-28 08:35:00", "direction": "IN"}
    ]
```

---

## 🟦 9 — Driver: Hikvision

**Path:** `biometric_integration/drivers/hikvision.py`

```python
def sync(device_config):
    # Example: query SQL Server or API
    return []
```

---

## 🟧 10 — Driver: Anviz

**Path:** `biometric_integration/drivers/anviz.py`

```python
def sync(device_config):
    # Example: REST API call
    return []
```

---

## ⏰ 11 — Enable Scheduler

```bash
bench --site yoursite set-config enable_scheduler true
bench restart
```

---

## ⚙️ 12 — Configure ERPNext

1. **Device Driver Doctype** → Create entries:
    - <img src="https://img.icons8.com/color/16/228BE6/fingerprint-scan.png"/> ZKTeco SDK → `biometric_integration.drivers.zkteco`
    - <img src="https://img.icons8.com/color/16/228BE6/cctv.png"/> Hikvision SQL → `biometric_integration.drivers.hikvision`
    - <img src="https://img.icons8.com/color/16/228BE6/fingerprint.png"/> Anviz API → `biometric_integration.drivers.anviz`
2. **Attendance Device Doctype** → Add each device with IP/Port/Driver/Active.
3. Scheduler will sync every 10 minutes → Logs saved to Employee Checkin.

---

## 🧪 13 — Test Manual Sync

Open bench console:

```bash
bench --site yoursite console
```

Then run:

```python
import biometric_integration.tasks as t
t.sync_all_devices()
```

---

## 🐞 14 — Debugging

- Errors logged via `frappe.log_error()` → ERPNext Error Log  
- Check running bench worker:
  ```bash
  bench worker
  ```

---

## 🗂️ 15 — Quick File List & Copy/Paste Instructions

| File/Folder Path                                                  | Description                |
|-------------------------------------------------------------------|----------------------------|
| `hooks.py`                                                        | Scheduler config           |
| `tasks.py`                                                        | Sync logic                 |
| `drivers/zkteco.py`                                               | ZKTeco logic               |
| `drivers/hikvision.py`                                            | Hikvision logic            |
| `drivers/anviz.py`                                                | Anviz logic                |
| `doctype/device_driver/device_driver.json`                        | Device Driver schema       |
| `doctype/attendance_device/attendance_device.json`                | Attendance Device schema   |
| `doctype/attendance_log_temp/attendance_log_temp.json` *(opt)*    | Temp Log schema (optional) |

---

<p align="center">
  <img src="https://img.icons8.com/fluency/48/ok.png" alt="Done"/><br/>
  <b>Done. Now new devices can be added in ERPNext UI only (no script changes).</b>
</p>
