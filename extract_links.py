import argparse
import csv
import re
from urllib.parse import urlparse


DEFAULT_OUTPUT_FILE = "linkedin_profiles.csv"
LINKEDIN_PROFILE_PATTERN = re.compile(
    r"https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9\-_%]+/?(?:\?[^\s<>\"]*)?",
    re.IGNORECASE,
)


def normalize_linkedin_url(url):
    parsed = urlparse(url.strip())
    path = parsed.path.rstrip("/")
    return f"https://www.linkedin.com{path}/"


def extract_profile_urls(text):
    urls = {
        normalize_linkedin_url(match.group(0))
        for match in LINKEDIN_PROFILE_PATTERN.finditer(text)
    }
    return sorted(urls, key=str.lower)


def write_profiles_csv(links, output_file):
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["linkedin_url", "status", "note"])
        for link in links:
            writer.writerow([link, "pending", ""])


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract LinkedIn profile URLs from an exported WhatsApp chat."
    )
    parser.add_argument("input_file", help="Path to the exported WhatsApp .txt file")
    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_OUTPUT_FILE,
        help=f"CSV output path. Defaults to {DEFAULT_OUTPUT_FILE}",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    with open(args.input_file, "r", encoding="utf-8") as f:
        text = f.read()

    links = extract_profile_urls(text)
    write_profiles_csv(links, args.output)

    print(f"Found {len(links)} LinkedIn profiles")
    print(f"Saved to {args.output}")


if __name__ == "__main__":
    main()
