# 🚀 ZKT Bio-Metric Device Installation On ERPNEXT

Step-by-step instructions to integrate the ZKT Bio-Metric Device with ERPNext.

---

## 1. 🖥️ Open Terminal

| Command | Copy |
|---------|------|
| `cd frappe-bench` | <button onclick="navigator.clipboard.writeText('cd frappe-bench')">📋</button> |
| `sudo apt update` | <button onclick="navigator.clipboard.writeText('sudo apt update')">📋</button> |
| `sudo apt install python3` | <button onclick="navigator.clipboard.writeText('sudo apt install python3')">📋</button> |
| `git clone https://github.com/frappe/biometric-attendance-sync-tool.git` | <button onclick="navigator.clipboard.writeText('git clone https://github.com/frappe/biometric-attendance-sync-tool.git')">📋</button> |
| `cd biometric-attendance-sync-tool` | <button onclick="navigator.clipboard.writeText('cd biometric-attendance-sync-tool')">📋</button> |
| `python3 -m venv venv` | <button onclick="navigator.clipboard.writeText('python3 -m venv venv')">📋</button> |
| `source venv/bin/activate` | <button onclick="navigator.clipboard.writeText('source venv/bin/activate')">📋</button> |
| `pip install -r requirements.txt` | <button onclick="navigator.clipboard.writeText('pip install -r requirements.txt')">📋</button> |

---

## 2. ⚙️ Configure the Tool

| Step | Copy |
|------|------|
| Locate the file `local_config.py.template` | <button onclick="navigator.clipboard.writeText('local_config.py.template')">📋</button> |
| Rename it to `local_config.py` | <button onclick="navigator.clipboard.writeText('local_config.py')">📋</button> |
| Fill in the required fields and save the file. | <button onclick="navigator.clipboard.writeText('Fill in the required fields and save the file.')">📋</button> |
| 📂 The file should be in: `frappe-bench/biometric-attendance-sync-tool/` | <button onclick="navigator.clipboard.writeText('frappe-bench/biometric-attendance-sync-tool/')">📋</button> |

---

## 3. ▶️ Run the Tool

| Command | Copy |
|---------|------|
| `cd frappe-bench` | <button onclick="navigator.clipboard.writeText('cd frappe-bench')">📋</button> |
| `cd biometric-attendance-sync-tool` | <button onclick="navigator.clipboard.writeText('cd biometric-attendance-sync-tool')">📋</button> |
| `source venv/bin/activate` | <button onclick="navigator.clipboard.writeText('source venv/bin/activate')">📋</button> |
| `python3 erpnext_sync.py` | <button onclick="navigator.clipboard.writeText('python3 erpnext_sync.py')">📋</button> |

---

## 🎥 Video Guide

[![Watch on YouTube](https://img.youtube.com/vi/KaMYfNCXShc/0.jpg)](https://www.youtube.com/watch?v=KaMYfNCXShc&t=701s)

---

## 📞 Need Help?

**Contact:** Taimoor  
**WhatsApp:** [wa.me/923009808900](https://wa.me/923009808900)

---

> 📝 For best results, ensure you have Python 3 installed and ERPNext running on your server.
