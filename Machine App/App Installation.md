# ERPNext Biometric Integration App (Complete Guide) — **v2**

---

## 0 — Prerequisites (on Ubuntu / ERPNext server)

- **Ubuntu 22.04+** with sudo access  
- **Bench + ERPNext** installed and running  
- **Python 3.10+**  
- **Git** installed  
  ```bash
  sudo apt install git
  ```
- Basic knowledge of ERPNext custom app creation

---

## 1 — Create New Custom App

```bash
cd ~/frappe-bench
bench new-app biometric_integration
bench --site yoursite install-app biometric_integration
```

---

## 2 — App Folder Structure

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
             └── doctype/
                   ├── device_driver/
                   │     └── device_driver.json
                   ├── driver_parameter/
                   │     └── driver_parameter.json
                   ├── device_configuration/
                   │     └── device_configuration.json
                   ├── attendance_device/
                   │     └── attendance_device.json
                   └── attendance_log_temp/
                         └── attendance_log_temp.json
```

---

## 3 — Doctype Design (Parent & Child, v2) — FULL DETAIL

### A) Child Table: **Driver Parameter**

| Field Label    | Fieldname      | Field Type  | Options / Notes |
|----------------|--------------- |-------------|-----------------|
| parameter_key  | parameter_key  | Data        | key used in code (e.g., ip, port, username) (reqd) |
| label          | label          | Data        | human label e.g., "IP Address" |
| field_type     | field_type     | Select      | Data, Int, Password, Select, Bool |
| options        | options        | Small Text  | for Select field_type list choices (comma separated) |
| default_value  | default_value  | Data        | optional |
| required       | required       | Check       | whether device must set it |
| description    | description    | Small Text  | help text |

**JSON:**
```json name=biometric_integration/doctype/driver_parameter/driver_parameter.json
{
  "doctype": "DocType",
  "name": "Driver Parameter",
  "module": "biometric_integration",
  "istable": 1,
  "custom": 1,
  "autoname": "field:parameter_key",
  "fields": [
    {"fieldname": "parameter_key", "fieldtype": "Data", "label": "Parameter Key", "reqd": 1},
    {"fieldname": "label", "fieldtype": "Data", "label": "Label"},
    {"fieldname": "field_type", "fieldtype": "Select", "label": "Field Type", "options": "Data\nInt\nPassword\nSelect\nBool"},
    {"fieldname": "options", "fieldtype": "Small Text", "label": "Options"},
    {"fieldname": "default_value", "fieldtype": "Data", "label": "Default Value"},
    {"fieldname": "required", "fieldtype": "Check", "label": "Required"},
    {"fieldname": "description", "fieldtype": "Small Text", "label": "Description"}
  ]
}
```

---

### B) Parent: **Device Driver**

| Label         | Fieldname      | Field Type  | Options/Notes |
|---------------|---------------|-------------|--------------|
| Driver Name   | driver_name    | Data        | reqd |
| Python Module | python_module  | Data        | e.g., biometric_integration.drivers.zkteco (reqd) |
| Connection Type | connection_type | Select   | SDK, API, SQL, CUSTOM |
| Default Port  | default_port   | Int         | e.g., 4370 |
| Notes         | notes          | Small Text  | documentation |
| Parameters    | parameters     | Table       | Options: Driver Parameter (child table) |

**JSON:**
```json name=biometric_integration/doctype/device_driver/device_driver.json
{
  "doctype": "DocType",
  "name": "Device Driver",
  "module": "biometric_integration",
  "custom": 1,
  "fields": [
    {"fieldname": "driver_name", "fieldtype": "Data", "label": "Driver Name", "reqd": 1},
    {"fieldname": "python_module", "fieldtype": "Data", "label": "Python Module", "reqd": 1},
    {"fieldname": "connection_type", "fieldtype": "Select", "options": "SDK\nAPI\nSQL\nCUSTOM", "label": "Connection Type"},
    {"fieldname": "default_port", "fieldtype": "Int", "label": "Default Port"},
    {"fieldname": "notes", "fieldtype": "Small Text", "label": "Notes"},
    {"fieldname": "parameters", "fieldtype": "Table", "label": "Parameters", "options": "Driver Parameter"}
  ]
}
```

---

### C) Child Table: **Device Configuration**

| Label        | Fieldname         | Field Type  | Notes |
|--------------|-------------------|-------------|-------|
| parameter_key| parameter_key     | Data        | same key as Driver Parameter.parameter_key |
| value        | value             | Data        | plain value |
| value_password | value_password  | Password    | for secrets (driver will prefer this if set) |

**JSON:**
```json name=biometric_integration/doctype/device_configuration/device_configuration.json
{
  "doctype": "DocType",
  "name": "Device Configuration",
  "module": "biometric_integration",
  "istable": 1,
  "custom": 1,
  "fields": [
    {"fieldname": "parameter_key", "fieldtype": "Data", "label": "Parameter Key", "reqd": 1},
    {"fieldname": "value", "fieldtype": "Data", "label": "Value"},
    {"fieldname": "value_password", "fieldtype": "Password", "label": "Value (Password)"}
  ]
}
```

---

### D) Parent: **Attendance Device**

| Label                | Fieldname            | Field Type    | Notes |
|----------------------|----------------------|---------------|-------|
| Device Name          | device_name          | Data          | reqd |
| Device ID            | device_id            | Data          | optional, unique ID you want |
| Device Driver        | device_driver        | Link          | Options: Device Driver (reqd) |
| IP Address           | ip_address           | Data          | convenience (optional) |
| Port                 | port                 | Int           | optional (falls back to driver default) |
| Active               | active               | Check         | default checked |
| Last Sync Time       | last_sync_time       | Datetime      | updated by scheduler |
| Device Configuration | device_configuration | Table         | Options: Device Configuration (child table) |

**JSON:**
```json name=biometric_integration/doctype/attendance_device/attendance_device.json
{
  "doctype": "DocType",
  "name": "Attendance Device",
  "module": "biometric_integration",
  "custom": 1,
  "fields": [
    {"fieldname": "device_name", "fieldtype": "Data", "label": "Device Name", "reqd": 1},
    {"fieldname": "device_id", "fieldtype": "Data", "label": "Device ID"},
    {"fieldname": "device_driver", "fieldtype": "Link", "label": "Device Driver", "options": "Device Driver", "reqd": 1},
    {"fieldname": "ip_address", "fieldtype": "Data", "label": "IP Address"},
    {"fieldname": "port", "fieldtype": "Int", "label": "Port"},
    {"fieldname": "active", "fieldtype": "Check", "label": "Active", "default": "1"},
    {"fieldname": "last_sync_time", "fieldtype": "Datetime", "label": "Last Sync Time"},
    {"fieldname": "device_configuration", "fieldtype": "Table", "label": "Device Configuration", "options": "Device Configuration"}
  ]
}
```

---

### E) (Optional) Table: **Attendance Log Temp**

| Label        | Fieldname       | Field Type        |
|--------------|-----------------|-------------------|
| device       | device          | Link → Attendance Device |
| employee_id  | employee_id     | Data              |
| punch_time   | punch_time      | Datetime          |
| direction    | direction       | Select            |
| synced       | synced          | Check             |

**JSON:**
```json name=biometric_integration/doctype/attendance_log_temp/attendance_log_temp.json
{
  "doctype": "DocType",
  "name": "Attendance Log Temp",
  "module": "biometric_integration",
  "custom": 1,
  "fields": [
    {"fieldname": "device", "fieldtype": "Link", "options": "Attendance Device", "label": "Device"},
    {"fieldname": "employee_id", "fieldtype": "Data", "label": "Employee ID"},
    {"fieldname": "punch_time", "fieldtype": "Datetime", "label": "Punch Time"},
    {"fieldname": "direction", "fieldtype": "Select", "label": "Direction", "options": "IN\nOUT"},
    {"fieldname": "synced", "fieldtype": "Check", "label": "Synced"}
  ]
}
```

---

## (Other Steps Unchanged: Hooks, Tasks, Drivers, Scheduler, etc.)

Continue with the rest of the steps (hooks.py, tasks.py, drivers, enable scheduler, configuration, testing, debugging, etc.) as in your original guide above.

---

✅ **Done. Now new device types, drivers, and device configurations can be added in ERPNext UI only (no script changes required!)**
