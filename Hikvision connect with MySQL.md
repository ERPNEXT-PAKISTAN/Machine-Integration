# 🛠️ Install MySQL Server & Create Database/User

A concise guide for MySQL "Server Only" installation and basic setup.

---

## ✅ 1. Install MySQL Server Only

- Download and install **MySQL Server Only** from the [official MySQL website](https://dev.mysql.com/downloads/mysql/).
- During setup, remember the root (admin) password.

---

## ✅ 2. Create Database

Once MySQL is installed and running, open the **MySQL Command Line Client** and run:

```sql
CREATE DATABASE hikvision DEFAULT CHARACTER SET utf8mb4;
```

<details>
<summary><strong>Copy</strong></summary>

```
CREATE DATABASE hikvision DEFAULT CHARACTER SET utf8mb4;
```

</details>

---

### To See All Databases

```sql
SHOW DATABASES;
```

<details>
<summary><strong>Copy</strong></summary>

```
SHOW DATABASES;
```

</details>

---

## ✅ 3. Create User and Grant Privileges

```sql
CREATE USER 'frappe'@'%' IDENTIFIED BY 'Password#74751';
GRANT ALL PRIVILEGES ON hikvision_ivms.* TO 'frappe'@'%';
FLUSH PRIVILEGES;
```

<details>
<summary><strong>Copy</strong></summary>

```
CREATE USER 'frappe'@'%' IDENTIFIED BY 'Password#74751';
GRANT ALL PRIVILEGES ON hikvision_ivms.* TO 'frappe'@'%';
FLUSH PRIVILEGES;
```

</details>

---

- Replace `'Password#74751'` with your own secure password.
- For security, **only share actual passwords with trusted parties**.

---





# ✅ How to Check Users in MySQL

Learn how to find users and their privileges in MySQL!

---

## 1. Display All MySQL Users

Open **MySQL Command Line Client**, enter your password, then run:

```sql
SELECT user, host FROM mysql.user;
```

<details>
<summary><strong>Copy</strong></summary>

```
SELECT user, host FROM mysql.user;
```

</details>

This shows a list like:

```
+-----------+-----------+
| user      | host      |
+-----------+-----------+
| root      | localhost |
| ivms_user | %         |
| mysql.innodb ...      |
...
```

You should see the user you created:

```
ivms_user   %
```

---

## 2. Check User Privileges

To verify the permissions for `ivms_user`:

```sql
SHOW GRANTS FOR 'ivms_user'@'%';
```

<details>
<summary><strong>Copy</strong></summary>

```
SHOW GRANTS FOR 'ivms_user'@'%';
```

</details>

It should show something like:

```
GRANT ALL PRIVILEGES ON `hikvision`.* TO 'ivms_user'@'%';
```

- If yes → perfect ✔  
- If not → tell me the output and I will fix it.

---

## 🔧 If you want to see only your user

**Check if user exists:**

```sql
SELECT user FROM mysql.user WHERE user = 'ivms_user';
```

<details>
<summary><strong>Copy</strong></summary>

```
SELECT user FROM mysql.user WHERE user = 'ivms_user';
```

</details>

**Check user host binding:**

```sql
SELECT host FROM mysql.user WHERE user = 'ivms_user';
```

<details>
<summary><strong>Copy</strong></summary>

```
SELECT host FROM mysql.user WHERE user = 'ivms_user';
```

</details>


---
C:\Program Files\MySQL\MySQL Server 8.0\lib\libmysql.dll

---

```
Database type: "MySQL"
Configuration file: C:\Program Files\MySQL\MySQL Server 8.0\lib\libmysql.dll
Server IP Address: "172.169.12.88"
Port: "3306"
Database Name: "hikvision"
User Name: "frappe"
User Password: "Master@4202"
```
---


# 🗄️ MySQL Attendance Table Setup Guide

A clear, easy-to-copy reference for creating your attendance logs table for **iVMS-4200** & ERPNext integration.

---

## ✅ Step 1 — Select the Database

```sql
USE hikvision;
```
<details>
<summary><strong>Copy</strong></summary>

```
USE hikvision;
```

</details>

---

## ✅ Step 2 — Create the Attendance Table <br> <small>Recommended Name: <code>attlog</code></small>

Paste **this full SQL** to create your attendance log table:

```sql
CREATE TABLE attlog (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employeeID VARCHAR(50),
    authDateTime DATETIME,
    authDate DATE,
    authTime TIME,
    direction INT,
    deviceName VARCHAR(100),
    deviceSN VARCHAR(100),
    personName VARCHAR(100),
    cardNo VARCHAR(100)
);
```
<details>
<summary><strong>Copy</strong></summary>

```
CREATE TABLE attlog (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employeeID VARCHAR(50),
    authDateTime DATETIME,
    authDate DATE,
    authTime TIME,
    direction INT,
    deviceName VARCHAR(100),
    deviceSN VARCHAR(100),
    personName VARCHAR(100),
    cardNo VARCHAR(100)
);
```

</details>

---

### ✔️ Field Explanation

| Field        | Type           | Purpose                                 |
|--------------|----------------|-----------------------------------------|
| `id`         | INT, AUTO_INCREMENT | Unique row ID                      |
| `employeeID` | VARCHAR(50)    | Employee ID from device                |
| `authDateTime`| DATETIME      | Full timestamp from device             |
| `authDate`   | DATE           | Only date (for ERPNext filtering)      |
| `authTime`   | TIME           | Only time                              |
| `direction`  | INT            | 0 = IN, 1 = OUT                        |
| `deviceName` | VARCHAR(100)   | Name of iVMS-4200 device               |
| `deviceSN`   | VARCHAR(100)   | Device Serial Number                   |
| `personName` | VARCHAR(100)   | Person name                            |
| `cardNo`     | VARCHAR(100)   | Card number                            |

---

> 🔥 **Important:**  
> iVMS-4200 **will NOT create custom fields automatically**.  
> **You must create this table before connecting iVMS-4200.**

---

## 🔄 What Next?

Once created:

1. **Restart iVMS-4200**
2. Go to **DB Configuration**
3. **Test Connection**  
   **iVMS** will begin writing logs into `attlog`!

---

## 🚀 Optional: Create Employee Table

```sql
CREATE TABLE employee (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employeeID VARCHAR(50),
    personName VARCHAR(100),
    department VARCHAR(100),
    gender VARCHAR(10)
);
```
<details>
<summary><strong>Copy</strong></summary>

```
CREATE TABLE employee (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employeeID VARCHAR(50),
    personName VARCHAR(100),
    department VARCHAR(100),
    gender VARCHAR(10)
);
```

</details>

---

## ✅ Final Step: Verify Your Tables

See your tables with:

```sql
USE hikvision;
SHOW TABLES;
```
<details>
<summary><strong>Copy</strong></summary>

```
USE hikvision;
SHOW TABLES;
```

</details>

You should now see:

```
attlog
employee
```

---

## 🧑‍💻 Table Details: See Columns & Structure

### ✅ 1. Show Table Columns *(Recommended)*

```sql
DESCRIBE attlog;
```
or  
```sql
DESC attlog;
```
<details>
<summary><strong>Copy</strong></summary>

```
DESCRIBE attlog;
```

or

```
DESC attlog;
```
</details>

This will show:

| Field        | Type           | Null | Key | Default | Extra          |
|--------------|----------------|------|-----|---------|----------------|
| id           | int            | NO   | PRI | NULL    | auto_increment |
| employeeID   | varchar(50)    | YES  |     | NULL    |                |
| authDateTime | datetime       | YES  |     | NULL    |                |
| authDate     | date           | YES  |     | NULL    |                |
| authTime     | time           | YES  |     | NULL    |                |
| direction    | int            | YES  |     | NULL    |                |
| deviceName   | varchar(100)   | YES  |     | NULL    |                |
| deviceSN     | varchar(100)   | YES  |     | NULL    |                |
| personName   | varchar(100)   | YES  |     | NULL    |                |
| cardNo       | varchar(100)   | YES  |     | NULL    |                |

---

### ✅ 2. Show Full SQL Structure

```sql
SHOW CREATE TABLE attlog\G;
```
<details>
<summary><strong>Copy</strong></summary>

```
SHOW CREATE TABLE attlog\G;
```
</details>

---

### ✅ 3. List All Tables

```sql
SHOW TABLES;
```
<details>
<summary><strong>Copy</strong></summary>

```
SHOW TABLES;
```
</details>

---

**Example Usage:**
```sql
USE hikvision;
DESC attlog;
```
---

Need more?  
I can provide:
- 🔁 A trigger to split datetime → date + time
- 🔄 Auto-sync to ERPNext
- 🗂️ Table for devices
- ⏰ Table for shift assignment

**Just tell me “continue” if you want!**
