import os
from collections import Counter

# ------------------------------
# Generator: memory safe reading
# ------------------------------
def read_logs(filename, start_line=0):
    with open(filename, "r", encoding="utf-8", errors="ignore") as file:
        for line_no, line in enumerate(file):
            if line_no < start_line:
                continue
            yield line_no, line.strip()


# ------------------------------
# Safe parser
# Format assumed:
# 2026-01-19 INFO User login success
# ------------------------------
def parse_log(line):
    parts = line.split(" ", 2)

    if len(parts) < 3:
        raise ValueError("Corrupted log format")

    date = parts[0]
    level = parts[1]
    message = parts[2]

    return date, level, message


# ------------------------------
# Main Analyzer
# ------------------------------
def analyze_logs(
    logfile,
    checkpoint_file="checkpoint.txt",
    corrupted_file="corrupted.log",
    report_file="report.txt"
):
    # Resume from checkpoint
    start_line = 0
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, "r") as cp:
            start_line = int(cp.read().strip())
        print(f"✅ Resuming from line: {start_line}")

    counts = Counter()
    error_messages = Counter()
    corrupted_count = 0

    # open corrupted file in append mode
    with open(corrupted_file, "a", encoding="utf-8") as bad_logs:
        try:
            for line_no, line in read_logs(logfile, start_line):

                try:
                    date, level, message = parse_log(line)
                    counts[level] += 1

                    # store error messages frequency
                    if level == "ERROR":
                        error_messages[message] += 1

                except Exception:
                    corrupted_count += 1
                    bad_logs.write(f"{line_no}: {line}\n")
                    continue

                # Save checkpoint every 50000 lines
                if line_no % 50000 == 0 and line_no != 0:
                    with open(checkpoint_file, "w") as cp:
                        cp.write(str(line_no))
                    print(f"💾 Checkpoint saved at line {line_no}")

        except KeyboardInterrupt:
            print("⛔ Interrupted manually, saving checkpoint...")
            with open(checkpoint_file, "w") as cp:
                cp.write(str(line_no))

        except Exception as e:
            print("❌ Unexpected crash:", e)
            with open(checkpoint_file, "w") as cp:
                cp.write(str(line_no))
            raise

    # Remove checkpoint if completed
    if os.path.exists(checkpoint_file):
        os.remove(checkpoint_file)

    # Write report
    with open(report_file, "w", encoding="utf-8") as rep:
        rep.write("✅ LOG ANALYSIS REPORT\n")
        rep.write("=" * 30 + "\n\n")

        rep.write("Log Level Counts:\n")
        for level, c in counts.items():
            rep.write(f"{level}: {c}\n")

        rep.write("\nCorrupted Lines Count: " + str(corrupted_count) + "\n\n")

        rep.write("Top 10 ERROR Messages:\n")
        for msg, freq in error_messages.most_common(10):
            rep.write(f"{freq} times -> {msg}\n")

    # Print summary
    print("\n✅ LOG ANALYSIS COMPLETE")
    print("Log Level Counts:", dict(counts))
    print("Corrupted Lines:", corrupted_count)
    print("📌 Report saved in:", report_file)
    print("📌 Corrupted logs saved in:", corrupted_file)


# ------------------------------
# Run
# ------------------------------
if __name__ == "__main__":
    analyze_logs("server.log")
import os
import csv
from collections import Counter

# ------------------------------
# Generator: memory safe reading
# ------------------------------
def read_logs(filename, start_line=0):
    with open(filename, "r", encoding="utf-8", errors="ignore") as file:
        for line_no, line in enumerate(file):
            if line_no < start_line:
                continue
            yield line_no, line.strip()


# ------------------------------
# Safe parser
# Format assumed:
# 2026-01-19 INFO User login success
# ------------------------------
def parse_log(line):
    parts = line.split(" ", 2)

    if len(parts) < 3:
        raise ValueError("Corrupted log format")

    date = parts[0]
    level = parts[1]
    message = parts[2]

    return date, level, message


# ------------------------------
# Main Analyzer
# ------------------------------
def analyze_logs(
    logfile,
    checkpoint_file="checkpoint.txt",
    corrupted_file="corrupted.log",
    report_file="report.txt",
    csv_file="logs_output.csv",
    errors_file="errors.log",
    warnings_file="warnings.log",
    info_file="info.log"
):
    # Resume from checkpoint
    start_line = 0
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, "r") as cp:
            start_line = int(cp.read().strip())
        print(f"✅ Resuming from line: {start_line}")

    counts = Counter()
    error_messages = Counter()
    corrupted_count = 0

    # Prepare CSV file (write header only if not exists / fresh run)
    write_header = not os.path.exists(csv_file) or start_line == 0

    # Open files using context manager
    with open(corrupted_file, "a", encoding="utf-8") as bad_logs, \
         open(errors_file, "a", encoding="utf-8") as err_logs, \
         open(warnings_file, "a", encoding="utf-8") as warn_logs, \
         open(info_file, "a", encoding="utf-8") as info_logs, \
         open(csv_file, "a", newline="", encoding="utf-8") as csv_out:

        writer = csv.writer(csv_out)

        if write_header:
            writer.writerow(["line_no", "date", "level", "message"])

        try:
            for line_no, line in read_logs(logfile, start_line):

                try:
                    date, level, message = parse_log(line)

                    # Count levels
                    counts[level] += 1

                    # Store error messages
                    if level == "ERROR":
                        error_messages[message] += 1
                        err_logs.write(line + "\n")

                    elif level == "WARNING":
                        warn_logs.write(line + "\n")

                    elif level == "INFO":
                        info_logs.write(line + "\n")

                    # Write structured row into CSV
                    writer.writerow([line_no, date, level, message])

                except Exception:
                    corrupted_count += 1
                    bad_logs.write(f"{line_no}: {line}\n")
                    continue

                # Save checkpoint every 50000 lines
                if line_no % 50000 == 0 and line_no != 0:
                    with open(checkpoint_file, "w") as cp:
                        cp.write(str(line_no))
                    print(f"💾 Checkpoint saved at line {line_no}")

        except KeyboardInterrupt:
            print("⛔ Interrupted manually, saving checkpoint...")
            with open(checkpoint_file, "w") as cp:
                cp.write(str(line_no))

        except Exception as e:
            print("❌ Unexpected crash:", e)
            with open(checkpoint_file, "w") as cp:
                cp.write(str(line_no))
            raise

    # Remove checkpoint if completed
    if os.path.exists(checkpoint_file):
        os.remove(checkpoint_file)

    # Write report
    with open(report_file, "w", encoding="utf-8") as rep:
        rep.write("✅ LOG ANALYSIS REPORT\n")
        rep.write("=" * 35 + "\n\n")

        rep.write("Log Level Counts:\n")
        for level, c in counts.items():
            rep.write(f"{level}: {c}\n")

        rep.write("\nCorrupted Lines Count: " + str(corrupted_count) + "\n\n")

        rep.write("Top 10 ERROR Messages:\n")
        rep.write("-" * 35 + "\n")
        for msg, freq in error_messages.most_common(10):
            rep.write(f"{freq} times -> {msg}\n")

    # Print summary
    print("\n✅ LOG ANALYSIS COMPLETE 🎉")
    print("Log Level Counts:", dict(counts))
    print("Corrupted Lines:", corrupted_count)

    print("\n📌 Output Files Generated:")
    print("✅ report.txt")
    print("✅ corrupted.log")
    print("✅ logs_output.csv")
    print("✅ errors.log")
    print("✅ warnings.log")
    print("✅ info.log")


# ------------------------------
# Run
# ------------------------------
if __name__ == "__main__":
    analyze_logs("server.log")
