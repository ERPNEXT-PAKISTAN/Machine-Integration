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
from flask import Flask, request
import requests
import logging
from datetime import datetime

app = Flask(__name__)

# ERPNext Configuration
ERPNEXT_URL = "192.168.xxx.xxx:8000"
API_KEY = "51fdfdfsdfdeec0"
API_SECRET = "826dgdfggfdfg739f5"

# Device Serial Number
DEVICE_SN = "BRMCdfdsdfs030"

logging.basicConfig(
    filename="/opt/zk_adms/adms.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)

# ----------------------------------------------------
# 1) Handle ATTLOG (attendance logs)
# ----------------------------------------------------
@app.route("/iclock/cdata", methods=['GET', 'POST'])
def iclock_cdata():
    params = request.args.to_dict()
    body = request.data.decode("utf-8", errors="ignore")

    logging.info(f"[CDAT] Params: {params}")
    logging.info(f"[CDAT] Body:\n{body}")

    # If attendance logs
    if params.get("table") == "ATTLOG":
        lines = body.strip().split("\n")

        for line in lines:
            parts = line.split("\t")
            if len(parts) >= 2:
                punch_time = parts[0].strip()
                uid = parts[1].strip()

                # Build Checkin Payload
                payload = {
                    "employee": uid,  # ERPNext Employee.biometric_id must equal UID
                    "time": punch_time,
                    "log_type": "IN",
                    "device_id": DEVICE_SN
                }

                logging.info(f"[ERP Payload] {payload}")

                try:
                    r = requests.post(
                        f"{ERPNEXT_URL}/api/resource/Employee Checkin",
                        json=payload,
                        headers={"Authorization": f"token {API_KEY}:{API_SECRET}"}
                    )
                    logging.info(f"[ERPNext Response] {r.status_code} {r.text}")
                except Exception as e:
                    logging.error(f"[ERP Error] {str(e)}")

    return "OK"

# ----------------------------------------------------
# 2) Device heartbeat handler (must return OK)
# ----------------------------------------------------
@app.route("/iclock/getrequest", methods=['GET'])
def iclock_getrequest():
    logging.info(f"[GETREQUEST] {request.args.to_dict()}")
    return "OK"

# ----------------------------------------------------
# Listener Root
# ----------------------------------------------------
@app.route("/")
def index():
    return "ZKTeco ADMS Listener Running"

# ----------------------------------------------------
if __name__ == "__main__":
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


