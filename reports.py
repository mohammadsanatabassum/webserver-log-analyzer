import os
import json
import csv


def generate_reports(summary, invalid_lines, report_dir="reports"):
    """
    Generates:
    ✅ summary_report.json
    ✅ error_report.json
    ✅ status_code_report.csv
    ✅ full_report.json
    ✅ cleaned_logs.log will be saved from app.py
    """
    os.makedirs(report_dir, exist_ok=True)

    # ✅ summary_report.json
    summary_path = os.path.join(report_dir, "summary_report.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)

    # ✅ error_report.json
    error_path = os.path.join(report_dir, "error_report.json")
    with open(error_path, "w", encoding="utf-8") as f:
        json.dump({"invalid_lines": invalid_lines}, f, indent=4)

    # ✅ status_code_report.csv
    status_csv_path = os.path.join(report_dir, "status_code_report.csv")
    with open(status_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["status_code", "count"])

        # summary["status_counts"] is a dict like {"200": 5, "404": 1}
        for code, count in summary.get("status_counts", {}).items():
            writer.writerow([code, count])

    # ✅ full_report.json
    full_report_path = os.path.join(report_dir, "full_report.json")
    full_report = {
        "summary": summary,
        "invalid_lines": invalid_lines
    }
    with open(full_report_path, "w", encoding="utf-8") as f:
        json.dump(full_report, f, indent=4)

    return {
        "summary_report": "summary_report.json",
        "error_report": "error_report.json",
        "status_csv": "status_code_report.csv",
        "full_report": "full_report.json"
    }
