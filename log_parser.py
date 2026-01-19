import re
from exceptions import InvalidLogLineError

# ✅ Apache/Nginx Common Log Format Regex
# Example:
# 127.0.0.1 - - [19/Jan/2026:10:20:30 +0530] "GET /home HTTP/1.1" 200 1024
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+)\s+\S+\s+\S+\s+\[(?P<time>[^\]]+)\]\s+'
    r'"(?P<method>\S+)\s+(?P<endpoint>\S+)\s+(?P<protocol>[^"]+)"\s+'
    r'(?P<status>\d{3})\s+(?P<size>\S+)'
)


def read_log_file(file_path):
    """Generator: reads huge log file line-by-line (memory efficient)"""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line_no, line in enumerate(f, start=1):
            yield line_no, line.strip()


def parse_log_line(line):
    """Parse one log line into dictionary"""
    match = LOG_PATTERN.match(line)

    if not match:
        raise InvalidLogLineError("Invalid log format")

    data = match.groupdict()

    # Convert status into integer
    data["status"] = int(data["status"])

    # Convert size (sometimes '-' occurs)
    if data["size"] == "-":
        data["size"] = 0
    else:
        data["size"] = int(data["size"])

    return data
