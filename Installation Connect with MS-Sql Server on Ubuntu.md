<p align="center">
  <img src="https://raw.githubusercontent.com/ERPNEXT-PAKISTAN/Machine-Integration/main/assets/logo.png" alt="ERPNext SQL Integration" width="180"/>
</p>

<h1 align="center">ERPNext SQL Integration Guide</h1>

<p align="center">
  <b>Seamlessly integrate Microsoft SQL Server data with ERPNext using Python</b>
</p>

---

## 🚀 Quick Start

Follow these step-by-step instructions to set up your environment and connect SQL Server to ERPNext.  
All commands feature a convenient "Copy" button for easy usage!

---

### <img src="https://img.icons8.com/color/48/000000/python--v1.png" width="28"/> Step 1: Create Virtual Environment & Install Dependencies

```bash
# Update Ubuntu packages
sudo apt update
```
```bash
# Install Python venv module
sudo apt install python3.10-venv
```
```bash
# Create a virtual environment
python3 -m venv venv
```
```bash
# Activate the virtual environment
source venv/bin/activate
```
```bash
# Install required Python packages
pip install pyodbc requests
```

---

### <img src="https://img.icons8.com/color/48/000000/microsoft-sql-server.png" width="28"/> Step 2: Configure SQL Server (Install ODBC Driver)

```bash
# Add Microsoft repository key
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
```
```bash
# Add Microsoft SQL Server repository
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
```
```bash
# Update package lists
sudo apt-get update
```
```bash
# Install ODBC driver and related packages
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev
```
```bash
# Confirm ODBC driver installation
odbcinst -q -d -n "ODBC Driver 17 for SQL Server"
```
```bash
# (Repeat if needed)
sudo apt-get install unixodbc-dev msodbcsql17
```

> **Note:**  
> Ensure your SQL Server allows remote connections and is accessible from your Ubuntu environment.

---

### <img src="https://img.icons8.com/color/48/000000/key-security.png" width="28"/> Step 3: Generate API Key & API Secret for ERPNext

1. **Log in to ERPNext as Administrator.**  
2. **Go to User Settings and generate an API Key & Secret.**  
3. **Save these credentials securely.**  
   - You will use them to authenticate API requests in your script.

---

### <img src="https://img.icons8.com/color/48/000000/code-file.png" width="28"/> Step 4: Create Python Script

Create a file named `erpnext_sql.py` in your desired directory.

You can copy sample code from:

- [thiscodeworks.com](https://www.thiscodeworks.com/embed/66f3fc60f4dcb900149d8681)
- [erpnext_sql_Hikvision.py](https://github.com/ERPNEXT-PAKISTAN/Machine-Integration/blob/main/erpnext_sql_Hikvision.py)
- [erpnext_sql_ZKT.py](https://github.com/ERPNEXT-PAKISTAN/Machine-Integration/blob/main/erpnext_sql_ZKT.py)

#### Using nano to create and edit the file:

```bash
nano erpnext_sql.py
```

- Copy the code from the above links.
- Configure your API & SQL settings.
- Save and exit nano:
  - Press `CTRL + O` to save.
  - Press `Enter` to confirm filename.
  - Press `CTRL + X` to exit.

> Customize the Python script as needed for your SQL Server import logic and ERPNext API usage.

---

### <img src="https://img.icons8.com/color/48/000000/document--v1.png" width="28"/> Step 5: Create Timestamp File

Create a file named `last_imported_timestamp.txt`:

```bash
touch last_imported_timestamp.txt
```

Define the timestamp file path in your script:
```python
timestamp_file_path = '/home/erpnext/last_imported_timestamp.txt'
default_timestamp = '2000-01-01 00:00:00'
```

---

### <img src="https://img.icons8.com/color/48/000000/play.png" width="28"/> Step 6: Run the Python Script

```bash
source venv/bin/activate
python3 erpnext_sql.py
```

Or simply:

```bash
python3 erpnext_sql.py
```

---

## 📚 Resources

- [ERPNext API Docs](https://frappeframework.com/docs/v13/user/en/api/rest)
- [pyODBC Documentation](https://github.com/mkleehammer/pyodbc/wiki)
- [ERPNext Machine Integration Repo](https://github.com/ERPNEXT-PAKISTAN/Machine-Integration)

---

## 🖼️ Logo

If you want to use a custom logo, place your logo image in `assets/logo.png` and update the `<img src=...>` link at the top of this README.

---

## 💡 Support

For queries and contributions, open an [Issue](https://github.com/ERPNEXT-PAKISTAN/Machine-Integration/issues) or [Pull Request](https://github.com/ERPNEXT-PAKISTAN/Machine-Integration/pulls).

---

<p align="center">
  <img src="https://img.shields.io/github/stars/ERPNEXT-PAKISTAN/Machine-Integration?style=social">
  <img src="https://img.shields.io/github/forks/ERPNEXT-PAKISTAN/Machine-Integration?style=social">
</p>
