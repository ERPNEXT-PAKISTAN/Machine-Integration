# ERPNext Biometric Integration App (Complete Guide) — v2

---

## 0 — Prerequisites (on Ubuntu / ERPNext server)

- **Ubuntu 22.04+** with sudo access  
- **Bench + ERPNext** installed and running  
- **Python 3.10+**  
- **Git** installed  
  ```bash
  sudo apt install git
  ```
- Basic knowledge of ERPNext custom app creation   
---

### Run under your bench folder (~/frappe-bench by default).   

#### Make sure bench & ERPNext are running and you can create / install apps.   

```
Install network tools:
```
---

#### Install Python pyzk libs inside bench env (important: install into bench env so ERPNext can import them):   

```
cd ~/frappe-bench
source env/bin/activate
pip install pyzk requests python-dateutil
deactivate
```
`(pyzk is the Python library to speak ZKTeco devices over port 4370.)`


---

## 1 — Create New Custom App

```bash
cd ~/frappe-bench
bench new-app biometric_integration
bench --site site1.local install-app biometric_integration
```
### update your site name `site1.local`
---

## 2 — App Folder Structure

```
biometric_integration/
   └── biometric_integration/
       ├── __init__.py
       ├── hooks.py
       ├── tasks.py
       ├── drivers/
       │     ├── __init__.py
       │     ├── zkteco.py
       │     ├── hikvision.py
       │     └── anviz.py
       └── doctype/
             ├── device_driver/
             │     └── device_driver.json
             ├── driver_parameter/
             │     └── driver_parameter.json
             ├── device_configuration/
             │     └── device_configuration.json
             ├── attendance_device/
             │     └── attendance_device.json
             └── attendance_log_temp/
                   └── attendance_log_temp.json
```

---

## 3 — Doctype Design (Parent & Child, v2) — FULL DETAIL

### A) Child Table: Driver Parameter

| Field Label    | Fieldname      | Field Type  | Options / Notes |
|----------------|--------------- |-------------|-----------------|
| parameter_key  | parameter_key  | Data        | key used in code (e.g., ip, port, username) (reqd) |
| label          | label          | Data        | human label e.g., "IP Address" |
| field_type     | field_type     | Select      | Data, Int, Password, Select, Bool |
| options        | options        | Small Text  | for Select field_type list choices (comma separated) |
| default_value  | default_value  | Data        | optional |
| required       | required       | Check       | whether device must set it |
| description    | description    | Small Text  | help text |

<details>
<summary>JSON for Driver Parameter</summary>

```json
{
  "doctype": "DocType",
  "name": "Driver Parameter",
  "module": "biometric_integration",
  "istable": 1,
  "custom": 1,
  "autoname": "field:parameter_key",
  "fields": [
    {"fieldname": "parameter_key", "fieldtype": "Data", "label": "Parameter Key", "reqd": 1},
    {"fieldname": "label", "fieldtype": "Data", "label": "Label"},
    {"fieldname": "field_type", "fieldtype": "Select", "label": "Field Type", "options": "Data\nInt\nPassword\nSelect\nBool"},
    {"fieldname": "options", "fieldtype": "Small Text", "label": "Options"},
    {"fieldname": "default_value", "fieldtype": "Data", "label": "Default Value"},
    {"fieldname": "required", "fieldtype": "Check", "label": "Required"},
    {"fieldname": "description", "fieldtype": "Small Text", "label": "Description"}
  ]
}
```
</details>

```
{"name":"Driver Parameter","creation":"2025-09-27 06:13:53.502882","modified":"2025-09-27 06:27:27.400203","modified_by":"Administrator","owner":"Administrator","docstatus":0,"idx":0,"issingle":0,"is_virtual":0,"is_tree":0,"istable":1,"editable_grid":1,"track_changes":0,"module":"Biometric Integration","autoname":"field:parameter_key","naming_rule":"By fieldname","sort_field":"modified","sort_order":"DESC","read_only":0,"in_create":0,"allow_copy":0,"allow_rename":1,"allow_import":0,"hide_toolbar":0,"track_seen":0,"max_attachments":0,"document_type":"","engine":"InnoDB","is_submittable":0,"show_name_in_global_search":0,"custom":1,"beta":0,"has_web_view":0,"allow_guest_to_view":0,"email_append_to":0,"show_title_field_in_link":0,"translated_doctype":0,"is_calendar_and_gantt":0,"quick_entry":0,"grid_page_length":50,"track_views":0,"queue_in_background":0,"allow_events_in_timeline":0,"allow_auto_repeat":0,"make_attachments_public":0,"force_re_route_to_default_view":0,"show_preview_popup":0,"protect_attached_files":0,"index_web_pages_for_search":1,"row_format":"Dynamic","rows_threshold_for_grid_search":0,"doctype":"DocType","links":[],"states":[],"fields":[{"name":"pnqs962dek","creation":"2025-09-27 06:13:53.502882","modified":"2025-09-27 06:27:27.400203","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Driver Parameter","parentfield":"fields","parenttype":"DocType","idx":1,"fieldname":"parameter_key","label":"Parameter Key","fieldtype":"Data","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":1,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":1,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"pnqvj2ndjc","creation":"2025-09-27 06:13:53.502882","modified":"2025-09-27 06:27:27.400203","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Driver Parameter","parentfield":"fields","parenttype":"DocType","idx":2,"fieldname":"label","label":"Label","fieldtype":"Data","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":1,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"pnqa3did85","creation":"2025-09-27 06:13:53.502882","modified":"2025-09-27 06:27:27.400203","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Driver Parameter","parentfield":"fields","parenttype":"DocType","idx":3,"fieldname":"field_type","label":"Field Type","fieldtype":"Select","options":"\nData\nInt\nPassword\nSelect\nBool","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":1,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"pnq0sjt4b4","creation":"2025-09-27 06:13:53.502882","modified":"2025-09-27 06:27:27.400203","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Driver Parameter","parentfield":"fields","parenttype":"DocType","idx":4,"fieldname":"default_value","label":"Default Value","fieldtype":"Data","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":1,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"pnqis94ovg","creation":"2025-09-27 06:13:53.502882","modified":"2025-09-27 06:27:27.400203","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Driver Parameter","parentfield":"fields","parenttype":"DocType","idx":5,"fieldname":"column_break_qvow","label":"","fieldtype":"Column Break","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":0,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"pnqpphfi6v","creation":"2025-09-27 06:13:53.502882","modified":"2025-09-27 06:27:27.400203","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Driver Parameter","parentfield":"fields","parenttype":"DocType","idx":6,"fieldname":"options","label":"Options","fieldtype":"Small Text","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":1,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"pnqbqrqu76","creation":"2025-09-27 06:13:53.502882","modified":"2025-09-27 06:27:27.400203","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Driver Parameter","parentfield":"fields","parenttype":"DocType","idx":7,"fieldname":"required","label":"Required","fieldtype":"Check","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"default":"0","in_list_view":1,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"pnqe7qbijg","creation":"2025-09-27 06:13:53.502882","modified":"2025-09-27 06:27:27.400203","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Driver Parameter","parentfield":"fields","parenttype":"DocType","idx":8,"fieldname":"description","label":"Description","fieldtype":"Small Text","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":1,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"}],"actions":[],"permissions":[]}
```
---

### B) Parent: Device Driver

| Label         | Fieldname      | Field Type  | Options/Notes |
|---------------|---------------|-------------|--------------|
| Driver Name   | driver_name    | Data        | reqd |
| Python Module | python_module  | Data        | e.g., biometric_integration.drivers.zkteco (reqd) |
| Connection Type | connection_type | Select   | SDK, API, SQL, CUSTOM |
| Default Port  | default_port   | Int         | e.g., 4370 |
| Notes         | notes          | Small Text  | documentation |
| Parameters    | parameters     | Table       | Options: Driver Parameter (child table) |

<details>
<summary>JSON for Device Driver</summary>

```json
{
  "doctype": "DocType",
  "name": "Device Driver",
  "module": "biometric_integration",
  "custom": 1,
  "fields": [
    {"fieldname": "driver_name", "fieldtype": "Data", "label": "Driver Name", "reqd": 1},
    {"fieldname": "python_module", "fieldtype": "Data", "label": "Python Module", "reqd": 1},
    {"fieldname": "connection_type", "fieldtype": "Select", "options": "SDK\nAPI\nSQL\nCUSTOM", "label": "Connection Type"},
    {"fieldname": "default_port", "fieldtype": "Int", "label": "Default Port"},
    {"fieldname": "notes", "fieldtype": "Small Text", "label": "Notes"},
    {"fieldname": "parameters", "fieldtype": "Table", "label": "Parameters", "options": "Driver Parameter"}
  ]
}
```
</details>

```
{"name":"Device Driver","creation":"2025-09-27 06:21:12.466762","modified":"2025-09-27 06:27:27.567807","modified_by":"Administrator","owner":"Administrator","docstatus":0,"idx":0,"issingle":0,"is_virtual":0,"is_tree":0,"istable":0,"editable_grid":0,"track_changes":0,"module":"Biometric Integration","autoname":"field:driver_name","naming_rule":"By fieldname","sort_field":"modified","sort_order":"DESC","read_only":0,"in_create":0,"allow_copy":0,"allow_rename":1,"allow_import":0,"hide_toolbar":0,"track_seen":0,"max_attachments":0,"document_type":"","engine":"InnoDB","is_submittable":0,"show_name_in_global_search":0,"custom":1,"beta":0,"has_web_view":0,"allow_guest_to_view":0,"email_append_to":0,"show_title_field_in_link":0,"translated_doctype":0,"is_calendar_and_gantt":0,"quick_entry":0,"grid_page_length":50,"track_views":0,"queue_in_background":0,"allow_events_in_timeline":0,"allow_auto_repeat":0,"make_attachments_public":0,"force_re_route_to_default_view":0,"show_preview_popup":0,"protect_attached_files":0,"index_web_pages_for_search":1,"row_format":"Dynamic","rows_threshold_for_grid_search":0,"doctype":"DocType","links":[],"states":[],"fields":[{"name":"p1fadeudso","creation":"2025-09-27 06:21:12.466762","modified":"2025-09-27 06:26:35.676655","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Device Driver","parentfield":"fields","parenttype":"DocType","idx":1,"fieldname":"driver_name","label":"Driver Name","fieldtype":"Data","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":1,"bold":0,"in_global_search":0,"collapsible":0,"unique":1,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":1,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"p1ff6qcmu1","creation":"2025-09-27 06:21:12.466762","modified":"2025-09-27 06:26:35.676655","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Device Driver","parentfield":"fields","parenttype":"DocType","idx":2,"fieldname":"python_module","label":"Python Module","fieldtype":"Data","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":1,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"description":"biometric_integration.drivers.zkteco","in_list_view":1,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"p1fq2kqvg1","creation":"2025-09-27 06:21:12.466762","modified":"2025-09-27 06:26:35.676655","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Device Driver","parentfield":"fields","parenttype":"DocType","idx":3,"fieldname":"connection_type","label":"Connection Type","fieldtype":"Select","options":"SDK\nAPI\nSQL\nCUSTOM","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":0,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"p1f93jjmp7","creation":"2025-09-27 06:21:12.466762","modified":"2025-09-27 06:26:35.676655","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Device Driver","parentfield":"fields","parenttype":"DocType","idx":4,"fieldname":"column_break_ccuy","label":"","fieldtype":"Column Break","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":0,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"p1fu7l1tpt","creation":"2025-09-27 06:21:12.466762","modified":"2025-09-27 06:26:35.676655","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Device Driver","parentfield":"fields","parenttype":"DocType","idx":5,"fieldname":"default_port","label":"Default Port","fieldtype":"Int","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"description":"e.g., 4370","in_list_view":0,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"p1fsfk4k0f","creation":"2025-09-27 06:21:12.466762","modified":"2025-09-27 06:26:35.676655","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Device Driver","parentfield":"fields","parenttype":"DocType","idx":6,"fieldname":"notes","label":"Notes","fieldtype":"Small Text","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":0,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"p1fsfelkaa","creation":"2025-09-27 06:21:12.466762","modified":"2025-09-27 06:26:35.676655","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Device Driver","parentfield":"fields","parenttype":"DocType","idx":7,"fieldname":"section_break_jnll","label":"","fieldtype":"Section Break","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":0,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"p1fgsrn5fd","creation":"2025-09-27 06:21:12.466762","modified":"2025-09-27 06:26:35.676655","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Device Driver","parentfield":"fields","parenttype":"DocType","idx":8,"fieldname":"parameters","label":"Parameters","fieldtype":"Table","options":"Driver Parameter","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":0,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"}],"actions":[],"permissions":[{"name":"m2kfaqcjh3","creation":"2025-09-27 06:21:12.466762","modified":"2025-09-27 06:26:35.676655","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Device Driver","parentfield":"permissions","parenttype":"DocType","idx":1,"permlevel":0,"role":"System Manager","read":1,"write":1,"create":1,"submit":0,"cancel":0,"delete":1,"amend":0,"report":1,"export":1,"import":0,"share":1,"print":1,"email":1,"if_owner":0,"select":0,"doctype":"DocPerm"}]}
```
---

### C) Child Table: Device Configuration

| Label        | Fieldname         | Field Type  | Notes |
|--------------|-------------------|-------------|-------|
| parameter_key| parameter_key     | Data        | same key as Driver Parameter.parameter_key |
| value        | value             | Data        | plain value |
| value_password | value_password  | Password    | for secrets (driver will prefer this if set) |

<details>
<summary>JSON for Device Configuration</summary>

```json
{
  "doctype": "DocType",
  "name": "Device Configuration",
  "module": "biometric_integration",
  "istable": 1,
  "custom": 1,
  "fields": [
    {"fieldname": "parameter_key", "fieldtype": "Data", "label": "Parameter Key", "reqd": 1},
    {"fieldname": "value", "fieldtype": "Data", "label": "Value"},
    {"fieldname": "value_password", "fieldtype": "Password", "label": "Value (Password)"}
  ]
}
```
</details>

```
{"name":"Device Configuration","creation":"2025-09-27 06:29:25.939314","modified":"2025-09-27 06:31:58.874739","modified_by":"Administrator","owner":"Administrator","docstatus":0,"idx":0,"issingle":0,"is_virtual":0,"is_tree":0,"istable":1,"editable_grid":1,"track_changes":0,"module":"Biometric Integration","naming_rule":"","sort_field":"modified","sort_order":"DESC","read_only":0,"in_create":0,"allow_copy":0,"allow_rename":1,"allow_import":0,"hide_toolbar":0,"track_seen":0,"max_attachments":0,"document_type":"","engine":"InnoDB","is_submittable":0,"show_name_in_global_search":0,"custom":1,"beta":0,"has_web_view":0,"allow_guest_to_view":0,"email_append_to":0,"show_title_field_in_link":0,"translated_doctype":0,"is_calendar_and_gantt":0,"quick_entry":0,"grid_page_length":50,"track_views":0,"queue_in_background":0,"allow_events_in_timeline":0,"allow_auto_repeat":0,"make_attachments_public":0,"force_re_route_to_default_view":0,"show_preview_popup":0,"protect_attached_files":0,"index_web_pages_for_search":1,"row_format":"Dynamic","rows_threshold_for_grid_search":0,"doctype":"DocType","links":[],"states":[],"fields":[{"name":"sck17c2f4d","creation":"2025-09-27 06:29:25.939314","modified":"2025-09-27 06:31:58.874739","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Device Configuration","parentfield":"fields","parenttype":"DocType","idx":1,"fieldname":"parameter_key","label":"Parameter Key","fieldtype":"Data","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":1,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"scku1pmtnd","creation":"2025-09-27 06:29:25.939314","modified":"2025-09-27 06:31:58.874739","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Device Configuration","parentfield":"fields","parenttype":"DocType","idx":2,"fieldname":"value","label":"Value","fieldtype":"Data","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":1,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"sckrblc8da","creation":"2025-09-27 06:29:25.939314","modified":"2025-09-27 06:31:58.874739","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Device Configuration","parentfield":"fields","parenttype":"DocType","idx":3,"fieldname":"value_password","label":"Value Password","fieldtype":"Password","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":1,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"}],"actions":[],"permissions":[]}
```
---

### D) Parent: Attendance Device

| Label                | Fieldname            | Field Type    | Notes |
|----------------------|----------------------|---------------|-------|
| Device Name          | device_name          | Data          | reqd |
| Device ID            | device_id            | Data          | optional, unique ID you want |
| Device Driver        | device_driver        | Link          | Options: Device Driver (reqd) |
| IP Address           | ip_address           | Data          | convenience (optional) |
| Port                 | port                 | Int           | optional (falls back to driver default) |
| Active               | active               | Check         | default checked |
| Last Sync Time       | last_sync_time       | Datetime      | updated by scheduler |
| Device Configuration | device_configuration | Table         | Options: Device Configuration (child table) |

<details>
<summary>JSON for Attendance Device</summary>

```json
{
  "doctype": "DocType",
  "name": "Attendance Device",
  "module": "biometric_integration",
  "custom": 1,
  "fields": [
    {"fieldname": "device_name", "fieldtype": "Data", "label": "Device Name", "reqd": 1},
    {"fieldname": "device_id", "fieldtype": "Data", "label": "Device ID"},
    {"fieldname": "device_driver", "fieldtype": "Link", "label": "Device Driver", "options": "Device Driver", "reqd": 1},
    {"fieldname": "ip_address", "fieldtype": "Data", "label": "IP Address"},
    {"fieldname": "port", "fieldtype": "Int", "label": "Port"},
    {"fieldname": "active", "fieldtype": "Check", "label": "Active", "default": "1"},
    {"fieldname": "last_sync_time", "fieldtype": "Datetime", "label": "Last Sync Time"},
    {"fieldname": "device_configuration", "fieldtype": "Table", "label": "Device Configuration", "options": "Device Configuration"}
  ]
}
```
</details>

```
{"name":"Attendance Device","creation":"2025-09-27 06:32:37.426311","modified":"2025-09-27 06:37:09.959620","modified_by":"Administrator","owner":"Administrator","docstatus":0,"idx":0,"issingle":0,"is_virtual":0,"is_tree":0,"istable":0,"editable_grid":0,"track_changes":0,"module":"Biometric Integration","autoname":"field:device_name","naming_rule":"By fieldname","sort_field":"modified","sort_order":"DESC","read_only":0,"in_create":0,"allow_copy":0,"allow_rename":1,"allow_import":0,"hide_toolbar":0,"track_seen":0,"max_attachments":0,"document_type":"","engine":"InnoDB","is_submittable":0,"show_name_in_global_search":0,"custom":1,"beta":0,"has_web_view":0,"allow_guest_to_view":0,"email_append_to":0,"show_title_field_in_link":0,"translated_doctype":0,"is_calendar_and_gantt":0,"quick_entry":1,"grid_page_length":50,"track_views":0,"queue_in_background":0,"allow_events_in_timeline":0,"allow_auto_repeat":0,"make_attachments_public":0,"force_re_route_to_default_view":0,"show_preview_popup":0,"protect_attached_files":0,"index_web_pages_for_search":1,"row_format":"Dynamic","rows_threshold_for_grid_search":0,"doctype":"DocType","links":[],"states":[],"fields":[{"name":"vdr3fee4hd","creation":"2025-09-27 06:32:37.426311","modified":"2025-09-27 06:37:09.959620","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Attendance Device","parentfield":"fields","parenttype":"DocType","idx":1,"fieldname":"device_information_section","label":"Device Information","fieldtype":"Section Break","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":0,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"vdrb6574q6","creation":"2025-09-27 06:32:37.426311","modified":"2025-09-27 06:37:09.959620","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Attendance Device","parentfield":"fields","parenttype":"DocType","idx":2,"fieldname":"device_name","label":"Device Name","fieldtype":"Data","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":1,"bold":0,"in_global_search":0,"collapsible":0,"unique":1,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":1,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"vdrdpr2kap","creation":"2025-09-27 06:32:37.426311","modified":"2025-09-27 06:37:09.959620","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Attendance Device","parentfield":"fields","parenttype":"DocType","idx":3,"fieldname":"device_id","label":"Device ID","fieldtype":"Data","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":0,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"vdrpgu3q9v","creation":"2025-09-27 06:32:37.426311","modified":"2025-09-27 06:37:09.959620","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Attendance Device","parentfield":"fields","parenttype":"DocType","idx":4,"fieldname":"device_driver","label":"Device Driver","fieldtype":"Link","options":"Device Driver","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":0,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"vdrchejrlc","creation":"2025-09-27 06:32:37.426311","modified":"2025-09-27 06:37:09.959620","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Attendance Device","parentfield":"fields","parenttype":"DocType","idx":5,"fieldname":"column_break_bcwq","label":"","fieldtype":"Column Break","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":0,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"vdrdujm1o0","creation":"2025-09-27 06:32:37.426311","modified":"2025-09-27 06:37:09.959620","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Attendance Device","parentfield":"fields","parenttype":"DocType","idx":6,"fieldname":"ip_address","label":"IP Address","fieldtype":"Data","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":0,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"vdrktpeop6","creation":"2025-09-27 06:32:37.426311","modified":"2025-09-27 06:37:09.959620","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Attendance Device","parentfield":"fields","parenttype":"DocType","idx":7,"fieldname":"port","label":"Port","fieldtype":"Int","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":0,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"vdrbcerumn","creation":"2025-09-27 06:32:37.426311","modified":"2025-09-27 06:37:09.959620","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Attendance Device","parentfield":"fields","parenttype":"DocType","idx":8,"fieldname":"active","label":"Active","fieldtype":"Check","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"default":"0","in_list_view":0,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"vdr2jhg6bd","creation":"2025-09-27 06:32:37.426311","modified":"2025-09-27 06:37:09.959620","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Attendance Device","parentfield":"fields","parenttype":"DocType","idx":9,"fieldname":"last_sync_time","label":"Last Sync Time","fieldtype":"Datetime","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":0,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"vdr24vkec2","creation":"2025-09-27 06:32:37.426311","modified":"2025-09-27 06:37:09.959620","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Attendance Device","parentfield":"fields","parenttype":"DocType","idx":10,"fieldname":"device_configuration_setting_section","label":"Device Configuration Setting","fieldtype":"Section Break","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":0,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"vdr24e4jqv","creation":"2025-09-27 06:32:37.426311","modified":"2025-09-27 06:37:09.959620","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Attendance Device","parentfield":"fields","parenttype":"DocType","idx":11,"fieldname":"device_configuration","label":"Device Configuration","fieldtype":"Table","options":"Device Configuration","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":0,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"}],"actions":[],"permissions":[{"name":"som7rddcdc","creation":"2025-09-27 06:32:37.426311","modified":"2025-09-27 06:37:09.959620","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Attendance Device","parentfield":"permissions","parenttype":"DocType","idx":1,"permlevel":0,"role":"System Manager","read":1,"write":1,"create":1,"submit":0,"cancel":0,"delete":1,"amend":0,"report":1,"export":1,"import":0,"share":1,"print":1,"email":1,"if_owner":0,"select":0,"doctype":"DocPerm"}]}
```
---

### E) (Optional) Table: Attendance Log Temp

| Label        | Fieldname       | Field Type        |
|--------------|-----------------|-------------------|
| device       | device          | Link → Attendance Device |
| employee_id  | employee_id     | Data              |
| punch_time   | punch_time      | Datetime          |
| direction    | direction       | Select            |
| synced       | synced          | Check             |

<details>
<summary>JSON for Attendance Log Temp</summary>

```json
{
  "doctype": "DocType",
  "name": "Attendance Log Temp",
  "module": "biometric_integration",
  "custom": 1,
  "fields": [
    {"fieldname": "device", "fieldtype": "Link", "options": "Attendance Device", "label": "Device"},
    {"fieldname": "employee_id", "fieldtype": "Data", "label": "Employee ID"},
    {"fieldname": "punch_time", "fieldtype": "Datetime", "label": "Punch Time"},
    {"fieldname": "direction", "fieldtype": "Select", "label": "Direction", "options": "IN\nOUT"},
    {"fieldname": "synced", "fieldtype": "Check", "label": "Synced"}
  ]
}
```
</details>

```
{"name":"Attendance Log Temp","creation":"2025-09-27 06:44:41.877764","modified":"2025-09-27 06:50:44.706051","modified_by":"Administrator","owner":"Administrator","docstatus":0,"idx":0,"issingle":0,"is_virtual":0,"is_tree":0,"istable":0,"editable_grid":0,"track_changes":0,"module":"Biometric Integration","autoname":"field:device","naming_rule":"By fieldname","sort_field":"modified","sort_order":"DESC","read_only":0,"in_create":0,"allow_copy":0,"allow_rename":1,"allow_import":0,"hide_toolbar":0,"track_seen":0,"max_attachments":0,"document_type":"","engine":"InnoDB","is_submittable":0,"show_name_in_global_search":0,"custom":1,"beta":0,"has_web_view":0,"allow_guest_to_view":0,"email_append_to":0,"show_title_field_in_link":0,"translated_doctype":0,"is_calendar_and_gantt":0,"quick_entry":0,"grid_page_length":50,"track_views":0,"queue_in_background":0,"allow_events_in_timeline":0,"allow_auto_repeat":0,"make_attachments_public":0,"force_re_route_to_default_view":0,"show_preview_popup":0,"protect_attached_files":0,"index_web_pages_for_search":1,"row_format":"Dynamic","rows_threshold_for_grid_search":0,"doctype":"DocType","links":[],"states":[],"fields":[{"name":"6q4q2gcplv","creation":"2025-09-27 06:44:41.877764","modified":"2025-09-27 06:50:44.706051","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Attendance Log Temp","parentfield":"fields","parenttype":"DocType","idx":1,"fieldname":"device","label":"Device","fieldtype":"Link","options":"Attendance Device","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":1,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":0,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"6q4la3rttr","creation":"2025-09-27 06:44:41.877764","modified":"2025-09-27 06:50:44.706051","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Attendance Log Temp","parentfield":"fields","parenttype":"DocType","idx":2,"fieldname":"employee_id","label":"Employee ID","fieldtype":"Data","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":0,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"6q4pk223od","creation":"2025-09-27 06:44:41.877764","modified":"2025-09-27 06:50:44.706051","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Attendance Log Temp","parentfield":"fields","parenttype":"DocType","idx":3,"fieldname":"punch_time","label":"Punch Time","fieldtype":"Datetime","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":0,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"6q46e8n5n5","creation":"2025-09-27 06:44:41.877764","modified":"2025-09-27 06:50:44.706051","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Attendance Log Temp","parentfield":"fields","parenttype":"DocType","idx":4,"fieldname":"column_break_urjt","label":"","fieldtype":"Column Break","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":0,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"6q423ohck2","creation":"2025-09-27 06:44:41.877764","modified":"2025-09-27 06:50:44.706051","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Attendance Log Temp","parentfield":"fields","parenttype":"DocType","idx":5,"fieldname":"direction","label":"Direction","fieldtype":"Data","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"in_list_view":0,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"},{"name":"6q4flsvj84","creation":"2025-09-27 06:44:41.877764","modified":"2025-09-27 06:50:44.706051","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Attendance Log Temp","parentfield":"fields","parenttype":"DocType","idx":6,"fieldname":"synced","label":"Synced","fieldtype":"Check","search_index":0,"show_dashboard":0,"hidden":0,"set_only_once":0,"allow_in_quick_entry":0,"print_hide":0,"report_hide":0,"reqd":0,"bold":0,"in_global_search":0,"collapsible":0,"unique":0,"no_copy":0,"allow_on_submit":0,"show_preview_popup":0,"permlevel":0,"ignore_user_permissions":0,"columns":0,"default":"0","in_list_view":0,"fetch_if_empty":0,"in_filter":0,"remember_last_selected_value":0,"ignore_xss_filter":0,"print_hide_if_no_value":0,"allow_bulk_edit":0,"in_standard_filter":0,"in_preview":0,"read_only":0,"precision":"","length":0,"translatable":0,"hide_border":0,"hide_days":0,"hide_seconds":0,"non_negative":0,"is_virtual":0,"sort_options":0,"show_on_timeline":0,"make_attachment_public":0,"doctype":"DocField"}],"actions":[],"permissions":[{"name":"3r2ftmv7d7","creation":"2025-09-27 06:44:41.877764","modified":"2025-09-27 06:50:44.706051","modified_by":"Administrator","owner":"Administrator","docstatus":0,"parent":"Attendance Log Temp","parentfield":"permissions","parenttype":"DocType","idx":1,"permlevel":0,"role":"System Manager","read":1,"write":1,"create":1,"submit":0,"cancel":0,"delete":1,"amend":0,"report":1,"export":1,"import":0,"share":1,"print":1,"email":1,"if_owner":0,"select":0,"doctype":"DocPerm"}]}
```
---

## 4 — Sample hooks.py

**Path:** `biometric_integration/hooks.py`
```python
from . import __version__ as app_version

app_name = "biometric_integration"
app_title = "Biometric Integration"
app_publisher = "Taimoor"
app_description = "Integrate Biometric Attendance Devices"
app_email = "taimoor986@gmail.com"
app_license = "MIT"

scheduler_events = {
    "cron": {
        "*/10 * * * *": ["biometric_integration.tasks.sync_all_devices"]
    }
}
```

---

## 5 — Sample tasks.py

**Path:** `biometric_integration/tasks.py`
```python
import importlib
import frappe

def sync_all_devices():
    devices = frappe.get_all("Attendance Device", filters={"active": 1}, fields="*")
    for d in devices:
        driver = frappe.db.get_value("Device Driver", d.device_driver, ["python_module"], as_dict=True)
        if not driver:
            continue
        try:
            module = importlib.import_module(driver["python_module"])
            # collect config as dict from child table
            config = {}
            rows = frappe.get_all("Device Configuration", filters={"parent": d.name, "parenttype": "Attendance Device"}, fields=["parameter_key","value","value_password"])
            for row in rows:
                config[row.parameter_key] = row.value_password or row.value
            logs = module.sync(config)
            for log in logs:
                frappe.get_doc({
                    "doctype": "Employee Checkin",
                    "employee": log["employee_id"],
                    "time": log["timestamp"],
                    "log_type": log["direction"]
                }).insert(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(message=str(e), title=f"Sync failed for {d.device_name}")
```

---

## 6 — Sample Driver Modules

**Path:** `biometric_integration/drivers/zkteco.py`
```python
def sync(device_config):
    # device_config dict contains all needed fields
    # Example: {'ip': '192.168.1.10', 'port': '4370', ...}
    return [
        {"employee_id": "E001", "timestamp": "2025-09-28 08:30:00", "direction": "IN"},
        {"employee_id": "E002", "timestamp": "2025-09-28 08:35:00", "direction": "IN"}
    ]
```

**Path:** `biometric_integration/drivers/hikvision.py`
```python
def sync(device_config):
    # Example: query SQL Server or API
    return []
```

**Path:** `biometric_integration/drivers/anviz.py`
```python
def sync(device_config):
    # Example: REST API call
    return []
```

---

## 7 — Enable Scheduler

```bash
bench --site site1.local set-config enable_scheduler true
bench restart
```

---

## 8 — Configure Device Drivers

1. **Device Driver Doctype** → Create entries:
    - ZKTeco SDK → `biometric_integration.drivers.zkteco`
    - Hikvision SQL → `biometric_integration.drivers.hikvision`
    - Anviz API → `biometric_integration.drivers.anviz`
2. **Add Driver Parameter child rows** for all config fields required by each driver (e.g. ip, port, secret, etc.)

---

## 9 — Add Attendance Devices

- **Attendance Device Doctype** → Add each device (name, driver, ip, port, etc)
- Add Device Configuration rows for each parameter (key + value/password)

---

## 10 — Sync Schedule

- Scheduler will sync every 10 minutes.
- Logs saved to Employee Checkin.

---

## 11 — Test Manual Sync

Open bench console:

```bash
bench --site site1.local console
```
Then run:

```python
import biometric_integration.tasks as t
t.sync_all_devices()
```

---

## 12 — Debugging

- Errors logged via `frappe.log_error()` → ERPNext Error Log
- Check running bench worker:
  ```bash
  bench worker
  ```

---

## 13 — Quick File List & Copy/Paste Instructions

| File/Folder Path                                                  | Description                |
|-------------------------------------------------------------------|----------------------------|
| `hooks.py`                                                        | Scheduler config           |
| `tasks.py`                                                        | Sync logic                 |
| `drivers/zkteco.py`                                               | ZKTeco logic               |
| `drivers/hikvision.py`                                            | Hikvision logic            |
| `drivers/anviz.py`                                                | Anviz logic                |
| `doctype/device_driver/device_driver.json`                        | Device Driver schema       |
| `doctype/driver_parameter/driver_parameter.json`                  | Driver Parameter schema    |
| `doctype/device_configuration/device_configuration.json`           | Device Configuration schema|
| `doctype/attendance_device/attendance_device.json`                | Attendance Device schema   |
| `doctype/attendance_log_temp/attendance_log_temp.json` *(opt)*    | Temp Log schema (optional) |

---

## 14 — (Optional) Attendance Log Temp

- Use this if you want to store raw logs before mapping to Employee Checkin.
- Table and JSON included above.

---

## 15 — UI-Driven Expansion

✅ **Now, all device types, drivers, and config are UI-driven: no code changes required for new devices!**

---
