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
from flask import Flask, request, jsonify
import requests
import logging
import os
from datetime import datetime

# ------------------------------
# ERPNext API CONFIG
# ------------------------------
ERPNEXT_URL = "192.168.xxx.xxx:8000"
ERPNEXT_API_KEY = "515dfsfdfseec0"
ERPNEXT_API_SECRET = "82sfdfdsfdff5"

# Endpoint for Employee Checkin
CHECKIN_URL = f"{ERPNEXT_URL}/api/resource/Employee Checkin"

# ------------------------------
# LOGGING SETUP
# ------------------------------
LOG_FILE = "/opt/zk_adms/adms.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)

# ------------------------------
# FLASK APP
# ------------------------------
app = Flask(__name__)


# ============================================================
# 🔹 Route: /iclock/getrequest
# Device polls this URL every few seconds
# ============================================================
@app.route('/iclock/getrequest', methods=['GET'])
def iclock_getrequest():
    params = dict(request.args)
    logging.info(f"[GETREQUEST] {params}")
    return "OK"


# ============================================================
# 🔹 Route: /iclock/cdata
# This receives ATTLOG, OPLOG, FPLOG, etc.
# ============================================================
@app.route('/iclock/cdata', methods=['POST'])
def iclock_cdata():
    params = dict(request.args)
    body = request.get_data(as_text=True)

    logging.info(f"[CDAT] Params: {params}")
    logging.info(f"[CDAT] Body:\n{body}\n")

    table = params.get("table")

    # -------------------------
    # Handle ATTLOG
    # -------------------------
    if table == "ATTLOG":
        try:
            lines = body.strip().split("\n")
            for line in lines:
                parts = line.split()
                if len(parts) < 2:
                    continue

                pin = parts[0]                     # Device PIN (74, 107, 275…)
                timestamp = parts[1]              # "2025-11-22 20:21:31"

                # ERPNext Payload
                payload = {
                    "employee": pin,             # attendance_device_id MUST MATCH pin
                    "attendance_device_id": pin,
                    "time": timestamp,
                    "log_type": "IN",            # uFace950 does not send IN/OUT
                    "device_id": params.get("SN", "")
                }

                logging.info(f"[ERP Payload] {payload}")

                # Send to ERPNext
                res = requests.post(
                    CHECKIN_URL,
                    json=payload,
                    headers={
                        "Authorization": f"token {ERPNEXT_API_KEY}:{ERPNEXT_API_SECRET}"
                    },
                    timeout=10
                )

                logging.info(f"[ERPNext Response] {res.status_code} {res.text}")

        except Exception as e:
            logging.error(f"[ERROR] ATTLOG parsing failed: {e}")

    return "OK"


# ============================================================
# Flask Start
# ============================================================
if __name__ == '__main__':
    logging.info("Starting ADMS Listener")
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


