# Hikvision Insatallation

## Step-1
```
cd ~/frappe-bench
```
## Step-2
```
bench get-app https://github.com/nilpatel42/biometric_integration.git
```
## Step-3
```
bench --site site1.local install-app biometric_integration
```
## Step-4
```
bench --site site1.local migrate
```
## Step-5
```
bench build
```
## Step-6
```
bench restart
```
