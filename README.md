
# 📊 Web Server Log Analyzer (Flask Dashboard)

A professional **Web Server Log Analyzer** built using **Python + Flask** that can analyze huge web server log files efficiently, handle corrupted/malformed logs safely, generate reports, and display results in an interactive dashboard with charts.

This project demonstrates real-world concepts like:

✅ File Operations (large file handling)  
✅ Exception Handling  
✅ Context Managers  
✅ Logging & Debugging  
✅ Report Generation (JSON + CSV)  
✅ Web Dashboard using Flask + Chart.js  

---

## 🚀 Project Highlights

### ✅ Core Features
- Reads huge log files **line-by-line** (memory efficient)
- Extracts log details:
  - IP Address
  - Timestamp
  - HTTP Method
  - Endpoint
  - Status Code
  - Response Size
- Calculates:
  - Total Requests
  - Total Bytes transferred
  - Status Code counts
  - Top Endpoints
  - Top IP addresses
- Handles **corrupted/malformed logs safely** (no crash)
- Generates structured **reports (JSON + CSV)**

---

## 🛡️ Error Handling
- Custom Exception: `InvalidLogLineError`
- Invalid lines are stored in `error_report.json` with:
  - line number
  - error reason
  - line preview

---

## 📁 Reports Generated
After uploading and analyzing a log file, the project generates:

- `summary_report.json` → overall statistics
- `error_report.json` → invalid/corrupted lines report
- `status_code_report.csv` → status code frequency
- `full_report.json` → combined report
- `cleaned_logs.log` → only valid log lines

---

## 🌐 Flask Dashboard (UI Features)
- Upload `.log` file from browser
- Dashboard contains:
  - Summary Cards
  - Bar Chart (Status Code Counts)
  - Pie Chart (Status Code Distribution)
  - Top Endpoints Chart
  - Top IPs Chart
  - Invalid Lines Preview Table

---

## 🧠 Problem Statement
A startup’s web server generates massive log files (GBs). They need to analyze them but:

- Files are huge → cannot load into memory
- Some logs are corrupted → analysis should not crash
- Need accurate statistics and reports
- Need visualization/dashboard for monitoring

---

## 🗂️ Project Structure
webserver-log-analyzer/
│── app.py
│── log_parser.py
│── reports.py
│── exceptions.py
│
├── templates/
│ └── index.html
│
├── static/
│ └── style.css
│
├── uploads/
└── reports/

📌 Sample Log Format Supported (Apache/Nginx)

Example supported log line:

127.0.0.1 - - [19/Jan/2026:10:20:30 +0530] "GET /home HTTP/1.1" 200 1024

 Run the Flask App
python app.py

✅ Technologies Used

Python

Flask

Chart.js

HTML / CSS

Regular Expressions (Regex)

JSON + CSV report generation
