# How-To: Troubleshooting & Operation Recipe Template

**Category:** DevOps / Backend / Database  
**Target System:** `clinic-booking-app-backend`  

---

## 🎯 Goal
Clear 1-sentence description of what this guide resolves or accomplishes.

---

## 🚨 Problem Symptoms & Logs
Paste the error log, stack trace, or symptom observed:
```text
Error: connect ETIMEDOUT 127.0.0.1:5432
    at TCPConnectWrap.afterConnect [as oncomplete] (net.js:1146:16)
```

---

## 🛠️ Step-by-Step Solution Recipe

### Step 1: Diagnose Active Process / Connection
Run the diagnostic command:
```bash
docker ps | grep postgres
```

### Step 2: Apply Resolution Fix
Execute the fix:
```bash
npx knex migrate:latest --env production
```

### Step 3: Verify Resolution
Check that health endpoint returns HTTP 200:
```bash
curl -I http://localhost:5000/api/health
```
