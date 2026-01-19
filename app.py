import os
from flask import Flask, render_template, request
from collections import Counter

from log_parser import read_log_file, parse_log_line
from exceptions import InvalidLogLineError
from reports import generate_reports

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    dashboard_data = None

    if request.method == "POST":
        file = request.files.get("logfile")

        # Basic upload validation
        if not file or file.filename == "":
            return render_template("index.html", error="Please upload a .log file")

        # Save uploaded file
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Stats
        total_requests = 0
        total_bytes = 0

        status_counts = Counter()
        endpoint_counts = Counter()
        ip_counts = Counter()

        invalid_lines = []
        cleaned_lines = []

        # Parse logs
        for line_no, line in read_log_file(filepath):
            try:
                data = parse_log_line(line)

                total_requests += 1
                total_bytes += data["size"]

                status_counts[str(data["status"])] += 1
                endpoint_counts[data["endpoint"]] += 1
                ip_counts[data["ip"]] += 1

                cleaned_lines.append(line)

            except InvalidLogLineError as e:
                invalid_lines.append({
                    "line_no": line_no,
                    "error": str(e),
                    "preview": line[:120]
                })

        # Save cleaned logs file
        cleaned_path = os.path.join(REPORT_FOLDER, "cleaned_logs.log")
        with open(cleaned_path, "w", encoding="utf-8") as f:
            for cl in cleaned_lines:
                f.write(cl + "\n")

        # Summary dictionary
        summary = {
            "file_uploaded": file.filename,
            "total_requests": total_requests,
            "total_bytes": total_bytes,
            "status_counts": dict(status_counts),
            "top_endpoints": endpoint_counts.most_common(10),
            "top_ips": ip_counts.most_common(10),
            "invalid_count": len(invalid_lines)
        }

        # Generate report files
        report_files = generate_reports(summary, invalid_lines, report_dir=REPORT_FOLDER)

        # Prepare chart labels/values
        top_endpoints = summary["top_endpoints"]
        top_ips = summary["top_ips"]

        dashboard_data = {
            "summary": summary,

            # show only few invalid lines on UI
            "invalid_lines": invalid_lines[:15],

            # chart data for status
            "status_labels": list(summary["status_counts"].keys()),
            "status_values": list(summary["status_counts"].values()),

            # chart data for endpoints
            "endpoint_labels": [x[0] for x in top_endpoints],
            "endpoint_values": [x[1] for x in top_endpoints],

            # chart data for IPs
            "ip_labels": [x[0] for x in top_ips],
            "ip_values": [x[1] for x in top_ips],

            "reports": report_files
        }

    return render_template("index.html", dashboard_data=dashboard_data)


if __name__ == "__main__":
    app.run(debug=True)
