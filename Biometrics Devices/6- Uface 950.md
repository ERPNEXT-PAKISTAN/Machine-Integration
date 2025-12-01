<p align="center">
  <img width="350" height="100" alt="Dashboard Banner" src="https://github.com/user-attachments/assets/b6b12445-4a2b-4f34-92c4-7819e5c491cc" />
  <img src="https://img.icons8.com/color/100/fingerprint-scan.png" width="100" height="100" title="Attendance Biometric Machine" alt="Attendance Biometric Machine"/>
</p>

---

<h1 align="center">
  <!-- Device Icon for Heading (Attendance Device) -->
  <img src="https://img.icons8.com/color/96/fingerprint-scan.png" width="73" title="Biometric Device"/>
  Integrate Any Biometric Device with erpnext
  <img src="https://img.icons8.com/color/96/touch-id.png" width="73" title="Attendance Device"/>
</h1>

<p align="center">

  <!-- Hikvision Biometric Device -->
  <img src="https://img.icons8.com/color/96/face-id.png" width="73" title="Hikvision Device"/>
    <!-- Generic Biometric Reader -->
  <img src="https://img.icons8.com/color/96/fingerprint.png" width="73" title="Generic Biometric Device"/>
    <!-- Anviz Device or Iris Scanner -->
  <img src="https://img.icons8.com/color/96/iris-scan.png" width="73" title="Anviz Device or Iris Scanner"/>
    <!-- Suprema/Password Device -->
  <img src="https://img.icons8.com/color/96/keypad.png" width="73" title="Suprema/Password Device"/>
    <!-- Face Recognition Device (WORKING and reliable) -->
<img src="https://img.icons8.com/color/96/face-id.png" width="73" title="Face Recognition"/>
    <!-- Classic Device Terminal (Icons8: ATM, as a generic device/machine) -->
<img src="https://img.icons8.com/color/96/atm.png" width="73" title="Device Machine"/>

</p>

---
Quick facts (آپ نے دیئے)
Machine (device) IP: 192.168.10.195
ERPNext server local (listener) machine IP: 192.168.10.10 (یہی ہم ADMS Listener بنائیں گے)
Cloud ERPNext URL: 192.168.2.10:8000
Device Serial Number (آپ کی upload کی تصویر): /mnt/data/094c7024-385a-4d4b-a715-2011c4ef21ac.png (SN shown on image: BRMC224260030)
g (آپ نے image upload کی؛ میں نے وہ local path نوٹ کر لیا ہے — آپ کو یہ path بطور حوالہ چاہیے تو وہ یہی ہے.)

---

Step A — Device (uFace 950) configuration (on the device)

Device menu: Menu → Comm → Cloud Server Setting
Set these exact values:
Server Mode: ADMS
Enable Domain Name: OFF
Server Address: 192.168.10.10
Server Port: 5000
Enable Proxy Server: OFF

---




---

## 1️⃣ <img src="https://img.icons8.com/color/48/ubuntu--v1.png" width="25"/> Ubuntu Terminal Code:

<details>
<summary>1️⃣<img src="https://github.githubassets.com/images/icons/emoji/unicode/1f5c2.png" width="28"/> Create folder</summary> 
  
#### <summary><img src="https://img.icons8.com/color/48/000000/code-file.png" width="22"/> Create folder</summary>  
  
```Terminal
sudo mkdir -p /opt/zk_adms
```
```Terminal
sudo chown $USER:$USER /opt/zk_adms
```
```Terminal
cd /opt/zk_adms
```
</details>

<details>
<summary>2️⃣<img src="https://img.icons8.com/fluency/48/open-box.png" width="24"/> Create virtual environment </summary> 

### <summary><img src="https://img.icons8.com/color/48/000000/code-file.png" width="22"/> virtual environment</summary>

```Terminal
sudo apt update && sudo apt upgrade -y
```
```Terminal
sudo apt install python3 python3-venv python3-pip git -y
```
```Terminal
python3 -m venv .venv
```
```Terminal
source .venv/bin/activate
```
```Terminal
pip install --upgrade pip
```
```Terminal
pip install flask requests python-dateutil
```
Give ownership to `frappe` (optional but recommended):
```Terminal
sudo chown -R frappe:frappe /opt/zk_adms
```


</details>

> **Note:**  
> Copy and paste in Terminal.
> `frappe is a user`

---


## <img src="https://img.icons8.com/color/48/000000/python--v1.png" width="25"/> Python Script
## ✔ STEP 4 — ADMS Listener (full robust script)

<details>
<summary><img src="https://img.icons8.com/color/48/000000/code-file.png" width="22"/> Copy Python</summary>

```python
Create file /opt/zk_adms/adms_listener.py with this content (exact):
```

```UPDATE python
nano /opt/zk_adms/adms_listener.py
```


```python
#!/usr/bin/env python3
"""
adms_listener.py (updated)

Purpose:
- Listen for ZKTeco uFace ADMS push requests on /iclock/cdata and /iclock/getrequest
- Parse ATTLOG and OPERLOG payloads sent by the device
- Resolve device PIN -> ERPNext Employee (by attendance_device_id or other candidate fields)
- Post Employee Checkin records to ERPNext with full timestamp
- Fallback to calling the server-side helper method if direct resource creation fails
- Robust logging and error handling suitable for running in WSL

Installation notes:
- Save to /opt/zk_adms/adms_listener.py (or keep at /mnt/data/adms_listener.py and copy to /opt/zk_adms/)
- Ensure the virtualenv is activated and dependencies installed (Flask, requests)
- Run with: ./.venv/bin/python adms_listener.py
- For background usage: nohup ./.venv/bin/python adms_listener.py > nohup.out 2>&1 &

Configuration (edit below constants if required):
- ERPNEXT_URL, ERPNEXT_API_KEY, ERPNEXT_API_SECRET
- LOG_FILE path

"""

import os
import json
import logging
from flask import Flask, request
from datetime import datetime
import requests

# --------------------------
# Configuration
# --------------------------
ERPNEXT_URL = "https://192.168.1xxx.22xx:8000"
ERPNEXT_API_KEY = "5dfsfdfsdfsdfdfsc0"
ERPNEXT_API_SECRET = "sfdfdfdfdsfdfdfd"

CHECKIN_URL = f"{ERPNEXT_URL}/api/resource/Employee Checkin"
EMPLOYEE_RESOURCE_URL = f"{ERPNEXT_URL}/api/resource/Employee"
ADD_LOG_METHOD_URL = f"{ERPNEXT_URL}/api/method/hrms.hr.doctype.employee_checkin.employee_checkin.add_log_based_on_employee_field"

LOG_FILE = "/opt/zk_adms/adms.log"
if not os.path.isdir(os.path.dirname(LOG_FILE)):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Candidate fields (priority order) in Employee doctype to try when resolving a PIN
CANDIDATE_EMP_FIELDS = [
    "attendance_device_id",
    "biometric_id",
    "biometric_device_id",
    "attendance_id",
    "device_id",
    "pin",
    "employee_number",
]

# --------------------------
# Logging
# --------------------------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logging.getLogger("werkzeug").setLevel(logging.WARNING)

logging.info("Loaded adms_listener (updated)")

# --------------------------
# Flask app
# --------------------------
app = Flask(__name__)

# --------------------------
# Helper: HTTP headers
# --------------------------
HEADERS = {
    "Authorization": f"token {ERPNEXT_API_KEY}:{ERPNEXT_API_SECRET}",
    "Content-Type": "application/json",
}

# --------------------------
# Simple in-memory cache to avoid repeated ERPNext queries
# --------------------------
EMP_CACHE = {}  # {pin_str: employee_docname_or_None}

# --------------------------
# Utilities
# --------------------------

def log(msg, level="info"):
    if level == "info":
        logging.info(msg)
    elif level == "warning":
        logging.warning(msg)
    elif level == "error":
        logging.error(msg)
    else:
        logging.debug(msg)


def find_employee_by_biometric(biometric_value):
    """
    Try to find an Employee docname by searching candidate fields.
    Returns docname (string) or None.
    Caches results in EMP_CACHE.
    """
    key = str(biometric_value)
    if key in EMP_CACHE:
        return EMP_CACHE[key]

    for field in CANDIDATE_EMP_FIELDS:
        try:
            params = {
                "filters": json.dumps([["Employee", field, "=", key]]),
                "fields": json.dumps(["name", "employee_name", field]),
            }
            r = requests.get(EMPLOYEE_RESOURCE_URL, headers=HEADERS, params=params, timeout=8)
            if r.status_code == 200:
                data = r.json().get("data")
                if isinstance(data, list) and data:
                    emp_docname = data[0].get("name")
                    EMP_CACHE[key] = emp_docname
                    log(f"Found Employee for biometric {key} via '{field}' -> {emp_docname}")
                    return emp_docname
            else:
                log(f"Employee query returned {r.status_code} for field {field}: {r.text}", level="warning")
        except Exception as e:
            log(f"Employee lookup error for field '{field}': {e}", level="warning")

    EMP_CACHE[key] = None
    log(f"No Employee found in ERPNext for biometric id {key} (checked fields: {CANDIDATE_EMP_FIELDS})", level="warning")
    return None


def post_checkin(employee_docname, timestamp_str, device_id, log_type="IN", latitude=None, longitude=None):
    """Post Employee Checkin to ERPNext resource endpoint.

    If employee_docname is None, do not attempt direct resource creation.
    """
    payload = {
        "time": timestamp_str,
        "device_id": device_id,
        "log_type": log_type,
        "skip_auto_attendance": 0,
    }

    # If we resolved the employee docname, send it
    if employee_docname:
        payload["employee"] = employee_docname
    # Also send attendance_device_id for traceability (ERPNext will use 'employee' docname if present)
    if "attendance_device_id" not in payload and employee_docname is None:
        # if employee_docname not resolved, we may pass attendance_device_id instead via fallback API
        pass

    if latitude is not None and longitude is not None:
        payload["latitude"] = str(latitude)
        payload["longitude"] = str(longitude)

    try:
        r = requests.post(CHECKIN_URL, json=payload, headers=HEADERS, timeout=12)
        log(f"[ERPNext Response] {r.status_code} {r.text}")
        return r
    except Exception as e:
        log(f"Error posting checkin to ERPNext: {e}", level="error")
        return None


def fallback_add_log_by_field(biometric_value, timestamp_str, device_id, log_type="IN", latitude=None, longitude=None):
    payload = {
        "employee_field_value": str(biometric_value),
        "timestamp": timestamp_str,
        "device_id": device_id,
        "log_type": log_type,
        "fetch_geolocation": 0,
        "skip_auto_attendance": 0,
    }
    if latitude is not None and longitude is not None:
        payload["latitude"] = str(latitude)
        payload["longitude"] = str(longitude)
        payload["geo_latitude"] = str(latitude)
        payload["geo_longitude"] = str(longitude)

    try:
        r = requests.post(ADD_LOG_METHOD_URL, json=payload, headers=HEADERS, timeout=12)
        log(f"[Fallback Response] {r.status_code} {r.text}")
        return r
    except Exception as e:
        log(f"Error calling fallback add_log_based_on_employee_field: {e}", level="error")
        return None


# --------------------------
# Flask routes
# --------------------------


@app.route("/iclock/getrequest", methods=["GET"])
def iclock_getrequest():
    params = dict(request.args)
    log(f"[GETREQUEST] {params}")
    return "OK"


@app.route("/iclock/cdata", methods=["POST"])
def iclock_cdata():
    params = dict(request.args)
    body = request.get_data(as_text=True)

    log(f"[CDAT] Params: {params}")
    log(f"[CDAT] Body:\n{body}\n")

    table = params.get("table", "").upper()
    sn = params.get("SN", "")

    # In many ADMS pushes, Stamp=9999 indicates the device is resending all logs
    # We will parse ATTLOG lines and post them to ERPNext

    if table == "ATTLOG":
        lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
        for line in lines:
            # Common ZKT ATTLOG format: PIN  YYYY-MM-DD HH:MM:SS  other fields...
            parts = line.split()
            if len(parts) < 2:
                continue

            pin = parts[0]
            date_part = parts[1] if len(parts) > 1 else ""
            time_part = parts[2] if len(parts) > 2 else "00:00:00"

            # If device has sent combined datetime in parts[1] (some devices), try to detect
            # If date_part already contains a time component, preserve it
            if len(parts) == 2 and " " in parts[1]:
                # rare case; already combined
                timestamp = parts[1]
            else:
                timestamp = f"{date_part} {time_part}".strip()

            # Normalize timestamp format if possible
            try:
                # Accept both 'YYYY-MM-DD HH:MM:SS' and 'YYYY/MM/DD HH:MM:SS'
                ts_dt = None
                try:
                    ts_dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                except Exception:
                    try:
                        ts_dt = datetime.strptime(timestamp, "%Y/%m/%d %H:%M:%S")
                    except Exception:
                        # if parsing fails, leave as string
                        ts_dt = None

                ts_str = ts_dt.strftime("%Y-%m-%d %H:%M:%S") if ts_dt else timestamp
            except Exception:
                ts_str = timestamp

            # Attempt to resolve the employee docname in ERPNext
            emp_docname = find_employee_by_biometric(pin)

            if emp_docname:
                # Post as resource using employee docname
                res = post_checkin(emp_docname, ts_str, sn, log_type="IN")
                if res is None or not str(res.status_code).startswith("2"):
                    log(f"Failed to create checkin using resource for {emp_docname} [{pin}] -> falling back", level="warning")
                    # fallback
                    fb = fallback_add_log_by_field(pin, ts_str, sn, log_type="IN")
                else:
                    log(f"Created checkin for employee {emp_docname} (pin={pin}) at {ts_str}")
            else:
                # No employee resolved — use fallback which locates by employee field value
                fb = fallback_add_log_by_field(pin, ts_str, sn, log_type="IN")
                if fb is not None and str(fb.status_code).startswith("2"):
                    log(f"Fallback created checkin for biometric {pin} at {ts_str}")
                else:
                    log(f"Fallback failed for biometric {pin} at {ts_str}", level="error")

        return "OK"

    # OPERLOG / other tables: log for audit purposes and return OK
    if table == "OPERLOG":
        log("[OPERLOG] Received (ignored)")
        return "OK"

    log("[CDAT] Unhandled table: %s" % table, level="warning")
    return "OK"


# --------------------------
# Run the app
# --------------------------
if __name__ == "__main__":
    log("Starting ADMS Listener (updated)")
    # Use 0.0.0.0 so device can reach the listener
    app.run(host="0.0.0.0", port=5000)







```


</details>



> **Note:**
>> Save:
>> CTRL+O
>> ENTER
>> CTRL+X
> 
> ✔ Minimal Working ADMS Script    
> Supports SpeedFace-V5L, uFace, ZKTeco ADMS
>
> ### CHANGE THESE CONFIGURATION ONLY:
> 
> ERPNEXT_URL = "https://fibersoft.org"     -------  your site    
> ERPNEXT_API_KEY = "YOUR_API_KEY"          -------  CHANGE    
> ERPNEXT_API_SECRET = "YOUR_API_SECRET"    -------  CHANGE    
> PRIMARY_FIELD = "attendance_device_id"    -------  do not change    

---
✔ Make executable:
```Terminal
chmod +x /opt/zk_adms/adms_listener.py
```
### Step D — Create systemd service so listener auto-starts

Create /etc/systemd/system/adms_listener.service:
```
sudo nano /etc/systemd/system/adms_listener.service
```

```Terminal
[Unit]
Description=ZK ADMS Listener
After=network.target

[Service]
User=root
WorkingDirectory=/opt/zk_adms
Environment="PATH=/opt/zk_adms/.venv/bin"
ExecStart=/opt/zk_adms/.venv/bin/python /opt/zk_adms/adms_listener.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
---

### ▶️ Enable & Start

```Enter to Folder:
sudo systemctl daemon-reload
sudo systemctl enable adms_listener
sudo systemctl start adms_listener
sudo journalctl -u adms_listener -f
```

### ▶️ Check Status
```
sudo systemctl status adms_listener
```
### ▶️ Firewall & Networking checks

```
# Allow port 5000
sudo ufw allow 5000/tcp
sudo ufw reload
# or if not using ufw, ensure iptables or cloud firewall allows port 5000 inbound from device network
```

### ▶️ From another machine (or same server) test:
```
# from server itself (should succeed)
curl -v "http://127.0.0.1:5000/device/verify?uid=test&time=2025-01-01%2010:00:00&sn=BRMC224260030"
# you should see response "OK"
```

### ▶️ Test full flow (live)
```
sudo tcpdump -i any port 5000 -nn -A
```

### ▶️ On device: perform a sample check-in (face or fingerprint). Watch tcpdump for an incoming GET/POST request; expected form:

```
On device: perform a sample check-in (face or fingerprint). Watch tcpdump for an incoming GET/POST request; expected form:
```

### ▶️ Multiple Devices

Add all device SNs to ALLOWED_DEVICE_SN array in script.
Add each device record in ERPNext.



### ▶️ Provide a short tcpdump capture (run on 192.168.xx.xx after you perform a test punch on the device)
```
sudo tcpdump -i any port 5000 -nn -A -c 6
```

### ▶️ Ensure the virtualenv is active and dependencies are installed:

```
cd /opt/zk_adms
source .venv/bin/activate
pip install -r requirements.txt
# or at minimum:
pip install flask requests
```

### ▶️ To Run in Background
```
nohup ./.venv/bin/python /opt/zk_adms/adms_listener.py > /opt/zk_adms/nohup.out 2>&1 &
```

### ▶️ Test Background Testing
```
./.venv/bin/python /opt/zk_adms/adms_listener.py
```


### ▶️ Logs
```
cat /opt/zk_adms/adms.log
````


### ✔ STEP 2 — Confirm with quick test
```
cd /opt/zk_adms
./.venv/bin/python adms_listener.py
```

### ▶️ Restart Listener in PowerShell

```PowerShell
pkill -f adms_listener
```

```
cd /opt/zk_adms
./.venv/bin/python adms_listener.py
```

```
Running on http://192.168.xx.xx:5000
```
### ▶️ Logs
```
cat /opt/zk_adms/adms.log
````

### ▶️  Replay / re-import old logs
```
sudo systemctl stop adms_listener
sudo rm /opt/zk_adms/adms.log
sudo systemctl start adms_listener
```

### OR If Running Manually:
```
pkill -f adms_listener
rm /opt/zk_adms/adms.log
./.venv/bin/python adms_listener.py
```

### ▶️ Remove Logs
```
rm /opt/zk_adms/adms.log
```

```
ls -l /opt/zk_adms/
```

```
rm adms.log
```




اس کا مطلب یہ ہے کہ:

✔ آپ کا ZKTeco uFace 950 صحیح طریقے سے ADMS/iClock پروٹوکول پر listener کو push کر رہا ہے
✔ Listener تک data پہنچ رہا ہے
✔ Device کا SN (BRMC224260030) صحیح آ رہا ہے
✔ ہم اب exactly right protocol کو handle کر سکتے ہیں

لیکن…






---
### ▶️ Run the Listener (as frappe user)

```Enter to Folder:
cd /opt/zk_adms
```
```Start Virtual Enviroment:
source .venv/bin/activate
```
```Terminal
nohup ./adms_listener.py > /opt/zk_adms/nohup.out 2>&1 &
```
---
### ⭐ Check Running:
```Terminal
ps aux | grep adms_listener
```

### ✨ Check Logs:
```Terminal
tail -f /opt/zk_adms/logs/adms.log
```

#### You Should See Like This.
```
[CDAT BODY]
107 2025-11-22 21:32:54 0 1 0 0 0 0
[ERPNext Response] 200 {"data": {"name":...}}
```


