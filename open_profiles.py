import argparse
import csv
import time
import webbrowser


DEFAULT_CSV_FILE = "linkedin_profiles.csv"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Open pending LinkedIn profiles from a tracking CSV."
    )
    parser.add_argument(
        "-c",
        "--csv",
        default=DEFAULT_CSV_FILE,
        help=f"CSV file to read and update. Defaults to {DEFAULT_CSV_FILE}",
    )
    parser.add_argument(
        "-d",
        "--delay",
        type=float,
        default=8,
        help="Seconds to wait between opening profiles. Defaults to 8.",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=None,
        help="Maximum number of pending profiles to open this session.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print profiles that would open without launching the browser or updating CSV.",
    )
    return parser.parse_args()


def read_profiles(csv_file):
    with open(csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader), reader.fieldnames or []


def write_profiles(csv_file, rows, fieldnames):
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def open_pending_profiles(rows, limit, delay, dry_run):
    opened_count = 0

    for row in rows:
        if row.get("status") != "pending":
            continue

        if limit is not None and opened_count >= limit:
            break

        url = row.get("linkedin_url", "").strip()
        if not url:
            continue

        print(url)
        if not dry_run:
            webbrowser.open(url)
            row["status"] = "opened"
            time.sleep(delay)

        opened_count += 1

    return opened_count


def main():
    args = parse_args()
    rows, fieldnames = read_profiles(args.csv)

    required_fields = ["linkedin_url", "status", "note"]
    missing_fields = [field for field in required_fields if field not in fieldnames]
    if missing_fields:
        missing = ", ".join(missing_fields)
        raise SystemExit(f"Missing required CSV columns: {missing}")

    opened_count = open_pending_profiles(rows, args.limit, args.delay, args.dry_run)

    if not args.dry_run:
        write_profiles(args.csv, rows, fieldnames)

    action = "Would open" if args.dry_run else "Opened"
    print(f"{action} {opened_count} pending profiles")


if __name__ == "__main__":
    main()
