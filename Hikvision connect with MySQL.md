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
