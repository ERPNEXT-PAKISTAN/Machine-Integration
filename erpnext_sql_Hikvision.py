import os
import platform
import pyodbc
import requests
from datetime import datetime
from collections import defaultdict

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

log("========== SCRIPT STARTED (Hikvision) ==========")

# Auto-detect environment
if "microsoft" in platform.uname().release.lower():
    timestamp_file_path = '/home/erpnext/last_imported_hikvision.txt'
else:
    timestamp_file_path = r'\\wsl.localhost\Ubuntu-22.04\home\erpnext\last_imported_hikvision.txt'

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
            last_timestamp = '2025-01-01 00:00:00'
except FileNotFoundError:
    last_timestamp = '2025-01-01 00:00:00'

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=192.168.1.20\\PAYROLL;DATABASE=Hikvision;UID=sa;PWD=sa@22022'
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
    SELECT employeeID, authDateTime, deviceName
    FROM [Hikvision].[dbo].[attlog]
    WHERE authDateTime > '{last_timestamp}'
    ORDER BY employeeID, authDateTime
""")
records = cursor.fetchall()

grouped_logs = defaultdict(list)
for row in records:
    employee_id, auth_datetime, device_name = row
    date_key = auth_datetime.date()
    grouped_logs[(employee_id, date_key)].append((auth_datetime, device_name))

for (employee_id, date), logs in grouped_logs.items():
    if not logs:
        continue

    first_log = logs[0]
    last_log = logs[-1]

    checkin_time = first_log[0].strftime('%Y-%m-%d %H:%M:%S')
    data_in = {
        "employee_field_value": employee_id,
        "timestamp": checkin_time,
        "device_id": first_log[1],
        "log_type": "IN",
        "latitude": latitude,
        "longitude": longitude,
        "fetch_geolocation": 1,
        "skip_auto_attendance": 0,
        "employee": employee_id,
        "employee_name": employee_id
    }
    response_in = requests.post(ERPNEXT_URL, json=data_in, headers=headers)
    log(f"[IN] {employee_id} → {response_in.status_code}: {response_in.text}")

    if first_log != last_log:
        checkout_time = last_log[0].strftime('%Y-%m-%d %H:%M:%S')
        data_out = {
            **data_in,
            "timestamp": checkout_time,
            "device_id": last_log[1],
            "log_type": "OUT"
        }
        response_out = requests.post(ERPNEXT_URL, json=data_out, headers=headers)
        log(f"[OUT] {employee_id} → {response_out.status_code}: {response_out.text}")

if records:
    latest_timestamp = max(r[1] for r in records).strftime('%Y-%m-%d %H:%M:%S')
    with open(timestamp_file_path, 'w') as f:
        f.write(latest_timestamp)
    log(f"✅ {len(records)} records synced. Timestamp saved: {latest_timestamp}")
else:
    log("✅ No new records to sync.")

conn.close()
log("========== SCRIPT FINISHED (Hikvision) ==========\n")
