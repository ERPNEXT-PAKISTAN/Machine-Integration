# ===============================================================
# ZKT → ERPNext Attendance Sync (robust: resolves employee & posts checkin)
# ===============================================================
import os
import platform
import pyodbc
import requests
import json
from datetime import datetime

# ===============================================================
# CONFIGURATION (your credentials & DB)
# ===============================================================
ERP_BASE = "https://192.168.1.100:8000"
CHECKIN_RESOURCE_URL = f"{ERP_BASE}/api/resource/Employee Checkin"
EMPLOYEE_RESOURCE_URL = f"{ERP_BASE}/api/resource/Employee"
ADD_LOG_METHOD_URL = f"{ERP_BASE}/api/method/hrms.hr.doctype.employee_checkin.employee_checkin.add_log_based_on_employee_field"

ERPNEXT_API_KEY = "0df45d4f5d4fd5"
ERPNEXT_API_SECRET = "es4f5d4f5d4fdf5f5"

SQL_CONN = {
    "server": "192.168.1.100\\SQLExpress",
    "database": "CVAccess",
    "username": "sa",
    "password": "sa@12345"
}

# fallback coordinates (use these if geo lookup fails)
DEFAULT_LAT = 31.4812872
DEFAULT_LON = 74.2520218

# timestamp file (WSL vs plain linux)
if "microsoft" in platform.uname().release.lower():
    TIMESTAMP_FILE = "/home/erpnext/last_imported_zkt.txt"
else:
    TIMESTAMP_FILE = r"\\wsl.localhost\Ubuntu-22.04\home\erpnext\last_imported_zkt.txt"

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

# ===============================================================
# HTTP helpers & endpoints
# ===============================================================
HEADERS = {
    "Authorization": f"token {ERPNEXT_API_KEY}:{ERPNEXT_API_SECRET}",
    "Content-Type": "application/json"
}

# Candidate employee fields to search by (priority order)
CANDIDATE_EMP_FIELDS = [
    "attendance_device_id",
    "biometric_id",
    "biometric_device_id",
    "attendance_id",
    "device_id",
    "pin",  # sometimes used
    "employee_number"
]

# Cache to avoid repeated lookups { machine_id: employee_docname or None }
EMP_CACHE = {}

def find_employee_by_biometric(biometric_value):
    """Return Employee docname (name) if found, else None. Caches results."""
    key = str(biometric_value)
    if key in EMP_CACHE:
        return EMP_CACHE[key]

    for field in CANDIDATE_EMP_FIELDS:
        try:
            params = {
                "filters": json.dumps([[ "Employee", field, "=", key ]]),
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
    log(f"❗ No Employee found in ERPNext for biometric id {key} (checked fields: {CANDIDATE_EMP_FIELDS})")
    return None

def create_employee_checkin(employee_docname, ts_str, device_id, log_type, lat, lon):
    """Create Employee Checkin using /api/resource/Employee Checkin (accepts latitude)."""
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
    """Fallback to original HRMS helper (keeps older behavior)."""
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
log("🏁========== SCRIPT STARTED (ZKT) ==========")

# Ensure timestamp path
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

# DB connection
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

# fetch records
query = f"""
    SELECT [pin], [name], [first_in_time], [last_out_time], [reader_name_in]
    FROM [CVAccess].[dbo].[acc_firstin_lastout]
    WHERE first_in_time > '{last_timestamp}' OR last_out_time > '{last_timestamp}'
    ORDER BY first_in_time
"""
cursor.execute(query)
records = cursor.fetchall()
log(f"📦 {len(records)} record(s) fetched from SQL.")

# prepare geolocation (one-time)
latitude, longitude = get_geolocation()
log(f"📍 Using coordinates: {latitude}, {longitude}")

# counters
created = 0
fallback_used = 0
failed = 0

LATEST_TIMESTAMP = last_timestamp

# process rows
for row in records:
    employee_machine_id, employee_name, first_in_time, last_out_time, reader_name_in = row

    for log_type, ts in (("IN", first_in_time), ("OUT", last_out_time)):
        if not ts:
            continue
        ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")
        device_id = reader_name_in or "ZKT"

        emp_docname = find_employee_by_biometric(employee_machine_id)

        if emp_docname:
            resp = create_employee_checkin(emp_docname, ts_str, device_id, log_type, latitude, longitude)
            if resp is not None and str(resp.status_code).startswith("2"):
                created += 1
                log(f"✅ Created checkin (resource) for {emp_docname} [{log_type}] at {ts_str} -> {resp.status_code}")
            else:
                failed += 1
                status = resp.status_code if resp is not None else "ERR"
                text = resp.text if resp is not None else ""
                log(f"❌ Failed to create checkin for {emp_docname} [{log_type}] at {ts_str} -> {status}: {text[:200]}")
        else:
            resp = fallback_add_log_by_field(employee_machine_id, ts_str, device_id, log_type, latitude, longitude)
            fallback_used += 1
            if resp is not None and str(resp.status_code).startswith("2"):
                created += 1
                log(f"✅ Fallback add_log created for biometric {employee_machine_id} [{log_type}] at {ts_str} -> {resp.status_code}")
            else:
                failed += 1
                status = resp.status_code if resp is not None else "ERR"
                text = resp.text if resp is not None else ""
                log(f"❌ Fallback failed for biometric {employee_machine_id} [{log_type}] at {ts_str} -> {status}: {text[:300]}")
                if "No Employee found" in text or "No employee found" in text:
                    log(f"   ℹ️ Suggestion: add biometric {employee_machine_id} to Employee (field like attendance_device_id) in ERPNext or adjust HR Settings employee identification field.")

        try:
            if ts > datetime.strptime(LATEST_TIMESTAMP, "%Y-%m-%d %H:%M:%S"):
                LATEST_TIMESTAMP = ts_str
        except Exception:
            LATEST_TIMESTAMP = ts_str

# write timestamp back
if records:
    try:
        with open(TIMESTAMP_FILE, "w") as f:
            f.write(LATEST_TIMESTAMP)
        log(f"✅ {len(records)} records processed. Latest timestamp saved: {LATEST_TIMESTAMP}")
    except Exception as e:
        log(f"⚠️ Failed to save timestamp: {e}")

# summary
log(f"📊 Summary: created={created}, fallback_used={fallback_used}, failed={failed}")

try:
    conn.close()
except:
    pass

log("🏁========== SCRIPT FINISHED (ZKT) ==========\n")
