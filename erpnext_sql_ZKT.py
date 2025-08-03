import os
import platform
import pyodbc
import requests
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

log("========== SCRIPT STARTED (ZKT) ==========")

if "microsoft" in platform.uname().release.lower():
    timestamp_file_path = '/home/erpnext/last_imported_zkt.txt'
else:
    timestamp_file_path = r'\\wsl.localhost\Ubuntu-22.04\home\erpnext\last_imported_zkt.txt'

os.makedirs(os.path.dirname(timestamp_file_path), exist_ok=True)

if os.name == "posix":
    try:
        if not os.path.exists(timestamp_file_path):
            with open(timestamp_file_path, 'w') as f:
                f.write('')
        os.chmod(timestamp_file_path, 0o666)
    except Exception as e:
        log(f"Permission error: {e}")

try:
    with open(timestamp_file_path, 'r') as f:
        last_timestamp = f.read().strip()
        if not last_timestamp:
            last_timestamp = '2000-01-01 00:00:00'
except FileNotFoundError:
    last_timestamp = '2000-01-01 00:00:00'

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=192.168.1.20\\PAYROLL;DATABASE=CVAccess;UID=sa;PWD=sa@22022'
)
cursor = conn.cursor()

ERPNEXT_API_KEY = '85dfd8g92ddfd5ed45'
ERPNEXT_API_SECRET = 'dfder4hdfdf445dd'
ERPNEXT_URL = 'http://192.168.1.12/api/method/hrms.hr.doctype.employee_checkin.employee_checkin.add_log_based_on_employee_field'

headers = {
    "Authorization": f"token {ERPNEXT_API_KEY}:{ERPNEXT_API_SECRET}",
    "Content-Type": "application/json"
}

latitude = 31.287604
longitude = 74.169660

cursor.execute(f"""
    SELECT [pin], [name], [first_in_time], [last_out_time], [reader_name_in]
    FROM [CVAccess].[dbo].[acc_firstin_lastout]
    WHERE first_in_time > '{last_timestamp}' OR last_out_time > '{last_timestamp}'
    ORDER BY first_in_time
""")

latest_timestamp = last_timestamp
records = cursor.fetchall()

for row in records:
    employee_id, employee_name, first_in_time, last_out_time, reader_name_in = row

    if first_in_time:
        ts_in = first_in_time.strftime('%Y-%m-%d %H:%M:%S')
        data = {
            "employee_field_value": employee_id,
            "timestamp": ts_in,
            "device_id": reader_name_in,
            "log_type": 'IN',
            "latitude": latitude,
            "longitude": longitude,
            "fetch_geolocation": 0,
            "skip_auto_attendance": 0,
            "employee": employee_id,
            "employee_name": employee_name
        }
        response = requests.post(ERPNEXT_URL, json=data, headers=headers)
        log(f"[IN] {employee_id} → {response.status_code}: {response.text}")
        if first_in_time > datetime.strptime(latest_timestamp, '%Y-%m-%d %H:%M:%S'):
            latest_timestamp = ts_in

    if last_out_time:
        ts_out = last_out_time.strftime('%Y-%m-%d %H:%M:%S')
        data = {
            "employee_field_value": employee_id,
            "timestamp": ts_out,
            "device_id": reader_name_in,
            "log_type": 'OUT',
            "latitude": latitude,
            "longitude": longitude,
            "fetch_geolocation": 0,
            "skip_auto_attendance": 0,
            "employee": employee_id,
            "employee_name": employee_name
        }
        response = requests.post(ERPNEXT_URL, json=data, headers=headers)
        log(f"[OUT] {employee_id} → {response.status_code}: {response.text}")
        if last_out_time > datetime.strptime(latest_timestamp, '%Y-%m-%d %H:%M:%S'):
            latest_timestamp = ts_out

if records:
    with open(timestamp_file_path, 'w') as f:
        f.write(latest_timestamp)
    log(f"✅ {len(records)} records synced. Timestamp saved: {latest_timestamp}")
else:
    log("✅ No new records to sync.")

conn.close()
log("========== SCRIPT FINISHED (ZKT) ==========\n")
