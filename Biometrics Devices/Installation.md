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
sudo apt update
```
```Terminal
sudo apt install python3-venv -y
```
```Terminal
python3 -m venv .venv
```
```Terminal
source .venv/bin/activate
```
```Terminal
pip install flask requests
```
✔ STEP 3 — Create log directory
```Terminal
mkdir -p /opt/zk_adms/logs
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
## ✔ STEP 4 — Create File adms_listener.py

<details>
<summary><img src="https://img.icons8.com/color/48/000000/code-file.png" width="22"/> Copy Python</summary>

```python
nano /opt/zk_adms/adms_listener.py
```
```python
#!/usr/bin/env python3
# Minimal ADMS listener for SpeedFace / ZKT
# Maps Employee.attendance_device_id → ERPNext Employee Checkin

from flask import Flask, request, Response
import requests, json
import logging

# -------------------------------------------------------
# CONFIG (CHANGE THESE ONLY)
# -------------------------------------------------------
ERPNEXT_URL = "https://fibersoft.org"    |------|    `your site`
ERPNEXT_API_KEY = "YOUR_API_KEY"         |------|    `CHANGE`
ERPNEXT_API_SECRET = "YOUR_API_SECRET"   |------|    `CHANGE`
PRIMARY_FIELD = "attendance_device_id"   |------|    `do not change`

# -------------------------------------------------------
# Logging
# -------------------------------------------------------
logging.basicConfig(
    filename="/opt/zk_adms/logs/adms.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)

app = Flask(__name__)

def erp_headers():
    return {
        "Authorization": f"token {ERPNEXT_API_KEY}:{ERPNEXT_API_SECRET}",
        "Content-Type": "application/json"
    }

# -------------------------------------------------------
# Find ERPNext Employee by device PIN
# -------------------------------------------------------
def find_employee(pin):
    try:
        url = f"{ERPNEXT_URL}/api/resource/Employee"
        params = {
            "filters": json.dumps([[ "Employee", PRIMARY_FIELD, "=", str(pin) ]]),
            "fields": json.dumps(["name", "employee_name"])
        }
        r = requests.get(url, headers=erp_headers(), params=params, timeout=5)
        if r.status_code == 200:
            data = r.json().get("data", [])
            if data:
                return data[0]["name"]
        return None
    except:
        return None

def create_checkin(emp, ts, device):
    url = f"{ERPNEXT_URL}/api/resource/Employee Checkin"
    payload = {
        "employee": emp,
        "time": ts,
        "log_type": "IN",
        "device_id": device
    }
    return requests.post(url, headers=erp_headers(), json=payload)

# -------------------------------------------------------
# Mandatory endpoint for SpeedFace ADMS
# -------------------------------------------------------
@app.route("/iclock/getrequest", methods=["GET"])
def get_request():
    sn = request.args.get("SN")
    logging.info(f"[GETREQUEST] SN={sn}")
    return Response("OK", 200)

@app.route("/iclock/cdata", methods=["POST", "GET"])
def cdata():
    args = request.args.to_dict()
    body = request.get_data(as_text=True)

    logging.info(f"[CDAT PARAMS] {args}")
    logging.info(f"[CDAT BODY]\n{body}")

    lines = [l.strip() for l in body.splitlines() if l.strip()]
    sn = args.get("SN", "UNKNOWN")

    for line in lines:
        parts = line.split()
        if len(parts) < 2:
            continue

        pin = parts[0]
        date = parts[1]
        time_part = parts[2] if len(parts) > 2 else "00:00:00"

        ts = f"{date} {time_part}"

        emp = find_employee(pin)
        if not emp:
            logging.info(f"[NO MATCH] No ERP Employee for PIN={pin}")
            continue

        r = create_checkin(emp, ts, sn)
        logging.info(f"[ERPNext Response] {r.status_code} {r.text[:150]}")

    return Response("OK", 200)

if __name__ == "__main__":
    logging.info("Starting ADMS listener on port 5000")
    app.run(host="0.0.0.0", port=5000, debug=False)

```


</details>

> **Note:**   
> ✔ Minimal Working ADMS Script    
> Supports SpeedFace-V5L, uFace, ZKTeco ADMS
>
> # CHANGE THESE CONFIGURATION ONLY:
> 
> ERPNEXT_URL = "https://fibersoft.org"      # your site    
> ERPNEXT_API_KEY = "YOUR_API_KEY"           # CHANGE    
> ERPNEXT_API_SECRET = "YOUR_API_SECRET"     # CHANGE    
> PRIMARY_FIELD = "attendance_device_id"     # do not change    

---
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
---

## <img src="https://img.icons8.com/fluency/48/code.png" width="25"/> Code Snippets

- <img src="https://img.icons8.com/ios-filled/50/source-code.png" width="21"/> Source Code
- <img src="https://img.icons8.com/fluency/48/copy.png" width="21"/> Copy
- <img src="https://img.icons8.com/material-outlined/48/copy.png" width="21"/> Copy

---

## <img src="https://img.icons8.com/fluency/48/report-card.png" width="25"/> Report View

- <img src="https://img.icons8.com/office/48/report-card.png" width="21"/> Office
- <img src="https://img.icons8.com/fluency/48/document.png" width="21"/> Document

---

## <img src="https://img.icons8.com/color/48/css3.png" width="25"/> CSS Code
## <img src="https://img.icons8.com/color/48/000000/microsoft-sql-server.png" width="25"/> SQL Query
## <img src="https://img.icons8.com/fluency/48/report-card.png" width="25"/> Report Name Setting
## <img src="https://img.icons8.com/fluency/48/combo-chart.png" width="25"/> <img src="https://img.icons8.com/color/48/marker.png" width="21"/> Dashboard Indicators

---

## 🔍 🧹 🔄 Set Filters in JavaScript

- 🔍 Filter
- 🧹 Clear Filter
- 🔄 Reset Filter

### <img src="https://img.icons8.com/fluency/48/folder.png" width="28"/> Folder
### <img src="https://img.icons8.com/color/48/folder.png" width="28"/> Folder
### <img src="https://img.icons8.com/fluency/48/open-folder.png" width="28"/> Open Folder
### <img src="https://img.icons8.com/fluency/48/folder-add.png" width="28"/> New Folder
### <img src="https://img.icons8.com/fluency/48/folder-lock.png" width="28"/> Locked Folder
### <img src="https://img.icons8.com/fluency/48/folder-invoices.png" width="28"/> Folder with files

### <img src="https://github.githubassets.com/images/icons/emoji/unicode/1f4c1.png" width="28"/> Folder (emoji image)
### <img src="https://github.githubassets.com/images/icons/emoji/unicode/1f5c2.png" width="28"/> Card index (grouped folders)

### <img src="https://img.icons8.com/fluency/48/open-box.png" width="24"/> <img src="https://img.icons8.com/color/48/python--v1.png" width="24"/> Create virtual environment
### <img src="https://img.icons8.com/fluency/48/open-box.png" width="24"/> <img src="https://img.icons8.com/color/48/python--v1.png" width="24"/> Create virtual environment



<p align="center">
  <img src="https://img.icons8.com/fluency/48/folder.png" width="34"/>  
  <b>Project Files</b>
</p>


---

> ✨ **Tip:**  
> You can switch, copy, or export code and data using the icons above.
