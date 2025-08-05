# 🚀 ZKT Bio-Metric Device Installation On ERPNEXT

Step-by-step instructions to integrate the ZKT Bio-Metric Device with ERPNext.

---

## 1. 🖥️ Open Terminal

Copy each command below by clicking the copy button in the top-right of each code block:

```bash
cd frappe-bench
```
```bash
sudo apt update
```
```bash
sudo apt install python3
```
```bash
git clone https://github.com/frappe/biometric-attendance-sync-tool.git
```
```bash
cd biometric-attendance-sync-tool
```
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```
```bash
pip install -r requirements.txt
```

---

## 2. ⚙️ Configure the Tool

- Locate the file `local_config.py.template`
- Rename it to `local_config.py`
- Fill in the required fields and save the file.

```bash
# The configuration file should be here:
frappe-bench/biometric-attendance-sync-tool/local_config.py
```

---

## 3. ▶️ Run the Tool

```bash
cd frappe-bench
```
```bash
cd biometric-attendance-sync-tool
```
```bash
source venv/bin/activate
```
```bash
python3 erpnext_sync.py
```

---

## 🎥 Video Guide

[![Watch on YouTube](https://img.youtube.com/vi/KaMYfNCXShc/0.jpg)](https://www.youtube.com/watch?v=KaMYfNCXShc&t=701s)

---

## 📞 Need Help?

**Contact:** Taimoor  
**WhatsApp:** [wa.me/923009808900](https://wa.me/923009808900)

---

> 📝 For best results, ensure you have Python 3 installed and ERPNext running on your server.
