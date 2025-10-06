# ===============================================================
# Hikvision → ERPNext Attendance Sync (ZKT-style robust version)
# ===============================================================
import os
import platform
import pyodbc
import requests
import json
from datetime import datetime
from collections import defaultdict

# ===============================================================
# CONFIGURATION
# ===============================================================
ERP_BASE = "https://192.168.1.100:8000"
CHECKIN_RESOURCE_URL = f"{ERP_BASE}/api/resource/Employee Checkin"
EMPLOYEE_RESOURCE_URL = f"{ERP_BASE}/api/resource/Employee"
ADD_LOG_METHOD_URL = f"{ERP_BASE}/api/method/hrms.hr.doctype.employee_checkin.employee_checkin.add_log_based_on_employee_field"

ERPNEXT_API_KEY = "6d1f2sdf2dfd23"
ERPNEXT_API_SECRET = "dfd5f5df5d4f5d5"

SQL_CONN = {
    "server": "192.168.1.100\\SQLExpress",
    "database": "Hikvision",
    "username": "sa",
    "password": "sa@12345"
}

# fallback coordinates (use these if geo lookup fails)
DEFAULT_LAT = 31.312872
DEFAULT_LON = 74.2220218

# timestamp file path
if "microsoft" in platform.uname().release.lower():
    TIMESTAMP_FILE = "/home/erpnext/last_imported_hikvision.txt"
else:
    TIMESTAMP_FILE = r"\\wsl.localhost\Ubuntu-22.04\home\erpnext\last_imported_hikvision.txt"

# ===============================================================
# UTILITIES
# ===============================================================
def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def get_geolocation():
    try:
        r = requests.get("https://ipinfo.io/json", timeout=5)
        if r.status_code == 200:
            d = r.json()
            loc = d.get("loc")
            if loc:
                lat, lon = loc.split(",")
                return float(lat), float(lon)
    except Exception as e:
        log(f"🌐 Geolocation fetch error: {e}")
    return DEFAULT_LAT, DEFAULT_LON

HEADERS = {
    "Authorization": f"token {ERPNEXT_API_KEY}:{ERPNEXT_API_SECRET}",
    "Content-Type": "application/json"
}

# fields to try for matching employee in ERPNext
CANDIDATE_EMP_FIELDS = [
    "attendance_device_id",
    "biometric_id",
    "biometric_device_id",
    "attendance_id",
    "device_id",
    "pin",
    "employee_number"
]

EMP_CACHE = {}

def find_employee_by_biometric(biometric_value):
    """Return Employee docname (name) if found, else None."""
    key = str(biometric_value)
    if key in EMP_CACHE:
        return EMP_CACHE[key]

    for field in CANDIDATE_EMP_FIELDS:
        try:
            params = {
                "filters": json.dumps([["Employee", field, "=", key]]),
                "fields": json.dumps(["name", "employee_name", field])
            }
            r = requests.get(EMPLOYEE_RESOURCE_URL, headers=HEADERS, params=params, timeout=8)
            if r.status_code == 200:
                data = r.json().get("data")
                if isinstance(data, list) and len(data) > 0:
                    emp_name = data[0].get("name")
                    EMP_CACHE[key] = emp_name
                    log(f"🔎 Found Employee for biometric {key} via field '{field}' -> {emp_name}")
                    return emp_name
        except Exception as e:
            log(f"⚠️ Employee lookup error for field '{field}': {e}")

    EMP_CACHE[key] = None
    log(f"❗ No Employee found in ERPNext for biometric id {key}")
    return None

def create_employee_checkin(employee_docname, ts_str, device_id, log_type, lat, lon):
    """Create Employee Checkin record directly."""
    payload = {
        "employee": employee_docname,
        "time": ts_str,
        "device_id": device_id,
        "log_type": log_type,
        "latitude": str(lat),
        "longitude": str(lon),
        "geo_latitude": str(lat),
        "geo_longitude": str(lon),
        "skip_auto_attendance": 0
    }
    try:
        r = requests.post(CHECKIN_RESOURCE_URL, json=payload, headers=HEADERS, timeout=12)
        return r
    except Exception as e:
        log(f"❌ Error creating checkin for {employee_docname} at {ts_str}: {e}")
        return None

def fallback_add_log_by_field(biometric_value, ts_str, device_id, log_type, lat, lon):
    """Fallback to add_log_based_on_employee_field."""
    payload = {
        "employee_field_value": str(biometric_value),
        "timestamp": ts_str,
        "device_id": device_id,
        "log_type": log_type,
        "latitude": str(lat),
        "longitude": str(lon),
        "geo_latitude": str(lat),
        "geo_longitude": str(lon),
        "fetch_geolocation": 0,
        "skip_auto_attendance": 0
    }
    try:
        r = requests.post(ADD_LOG_METHOD_URL, json=payload, headers=HEADERS, timeout=12)
        return r
    except Exception as e:
        log(f"❌ Error calling add_log_based_on_employee_field for {biometric_value} at {ts_str}: {e}")
        return None

# ===============================================================
# SCRIPT START
# ===============================================================
log("🏁========== SCRIPT STARTED (Hikvision) ==========")

# timestamp management
os.makedirs(os.path.dirname(TIMESTAMP_FILE), exist_ok=True)
if not os.path.exists(TIMESTAMP_FILE):
    open(TIMESTAMP_FILE, "w").close()
try:
    os.chmod(TIMESTAMP_FILE, 0o666)
except Exception:
    pass

try:
    with open(TIMESTAMP_FILE, "r") as f:
        last_timestamp = f.read().strip() or "2000-01-01 00:00:00"
except FileNotFoundError:
    last_timestamp = "2000-01-01 00:00:00"

log(f"🕓 Last imported timestamp: {last_timestamp}")

# connect to SQL Server
try:
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SQL_CONN['server']};DATABASE={SQL_CONN['database']};"
        f"UID={SQL_CONN['username']};PWD={SQL_CONN['password']}"
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    log("✅ Connected to SQL Server successfully.")
except Exception as e:
    log(f"❌ SQL connection failed: {e}")
    raise SystemExit

# fetch Hikvision logs
query = f"""
    SELECT employeeID, authDateTime, deviceName
    FROM [Hikvision].[dbo].[attlog]
    WHERE authDateTime > '{last_timestamp}'
    ORDER BY employeeID, authDateTime
"""
cursor.execute(query)
records = cursor.fetchall()
log(f"📦 {len(records)} record(s) fetched from SQL.")

latitude, longitude = get_geolocation()
log(f"📍 Using coordinates: {latitude}, {longitude}")

created = 0
fallback_used = 0
failed = 0
LATEST_TIMESTAMP = last_timestamp

# group by employee/date to find IN/OUT
grouped_logs = defaultdict(list)
for row in records:
    emp_id, auth_datetime, device_name = row
    grouped_logs[(emp_id, auth_datetime.date())].append((auth_datetime, device_name))

for (emp_id, _), logs in grouped_logs.items():
    logs.sort()
    first_log = logs[0]
    last_log = logs[-1]

    for log_type, ts, dev in (("IN", first_log[0], first_log[1]), ("OUT", last_log[0], last_log[1])):
        if not ts:
            continue
        ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")

        emp_docname = find_employee_by_biometric(emp_id)
        if emp_docname:
            resp = create_employee_checkin(emp_docname, ts_str, dev, log_type, latitude, longitude)
            if resp is not None and str(resp.status_code).startswith("2"):
                created += 1
                log(f"✅ Created checkin for {emp_docname} [{log_type}] at {ts_str}")
            else:
                failed += 1
                status = resp.status_code if resp else "ERR"
                text = resp.text[:200] if resp else ""
                log(f"❌ Failed checkin {emp_docname} [{log_type}] -> {status}: {text}")
        else:
            resp = fallback_add_log_by_field(emp_id, ts_str, dev, log_type, latitude, longitude)
            fallback_used += 1
            if resp is not None and str(resp.status_code).startswith("2"):
                created += 1
                log(f"✅ Fallback created for biometric {emp_id} [{log_type}] at {ts_str}")
            else:
                failed += 1
                status = resp.status_code if resp else "ERR"
                text = resp.text[:300] if resp else ""
                log(f"❌ Fallback failed for {emp_id} [{log_type}] -> {status}: {text}")

        # update timestamp
        try:
            if ts > datetime.strptime(LATEST_TIMESTAMP, "%Y-%m-%d %H:%M:%S"):
                LATEST_TIMESTAMP = ts_str
        except Exception:
            LATEST_TIMESTAMP = ts_str

# save timestamp
if records:
    try:
        with open(TIMESTAMP_FILE, "w") as f:
            f.write(LATEST_TIMESTAMP)
        log(f"✅ {len(records)} records processed. Latest timestamp saved: {LATEST_TIMESTAMP}")
    except Exception as e:
        log(f"⚠️ Failed to save timestamp: {e}")

log(f"📊 Summary: created={created}, fallback_used={fallback_used}, failed={failed}")

try:
    conn.close()
except:
    pass

log("🏁========== SCRIPT FINISHED (Hikvision) ==========\n")
