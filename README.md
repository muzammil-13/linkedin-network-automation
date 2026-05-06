# WhatsApp-to-LinkedIn Connector Automation

A lightweight Python automation tool that helps extract LinkedIn profile URLs shared inside WhatsApp groups and streamline the networking workflow.

Built for situations where dozens of people share their LinkedIn profiles in communities, startup groups, AI circles, hackathons, or event groups, making manual searching and connecting repetitive and time-consuming.

---

## Problem

In active WhatsApp communities, many members share their LinkedIn profile URLs during introductions.

Manually:

* searching each profile
* opening links
* tracking who you connected with
* avoiding duplicates

becomes messy and inefficient.

Especially in:

* AI communities
* startup groups
* hackathons
* networking events
* tech meetups

---

## Solution

This project automates the repetitive parts of the workflow using Python.

The tool:

* extracts LinkedIn profile URLs from exported WhatsApp chats
* removes duplicates
* stores profiles in CSV format
* opens profiles automatically in browser one by one

### Manual steps intentionally kept manual

For platform safety and account protection:

* WhatsApp chat export → Manual
* Sending LinkedIn connection requests → Manual

This avoids violating platform automation policies and keeps networking personalized.

---

## Features

* Extract LinkedIn profile URLs from WhatsApp exported `.txt` chat
* Deduplicate repeated URLs
* Generate clean CSV tracking sheet
* Auto-open profiles sequentially in browser
* Lightweight and beginner-friendly
* No APIs required
* No browser automation frameworks required

---

## Tech Stack

* Python 3
* Regex (`re`)
* CSV handling
* Webbrowser module

---

## Workflow

```text
WhatsApp Group
      ↓
Export Chat (.txt)
      ↓
Python URL Extractor
      ↓
linkedin_profiles.csv
      ↓
Auto-open LinkedIn Profiles
      ↓
Manual Personalized Connect Requests
```

---

## Project Structure

```bash
linkedin-network-automation/
│
├── extract_links.py
├── open_profiles.py
├── linkedin_profiles.csv
├── README.md
└── sample_chat.txt
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/linkedin-network-automation.git

cd linkedin-network-automation
```

---

## Usage

### Step 1: Export WhatsApp Chat

From WhatsApp:

```text
Group → More → Export Chat → Without Media
```

Place the exported `.txt` file inside the project folder.

---

### Step 2: Extract LinkedIn URLs

Run:

```bash
python extract_links.py
```

Output:

```text
linkedin_profiles.csv
```

---

### Step 3: Open Profiles Automatically

Run:

```bash
python open_profiles.py
```

The script opens LinkedIn profiles one by one in your browser.

You manually:

* review profile
* personalize note
* send request

---

## Example Use Cases

* AI communities
* Startup founder groups
* Tech networking events
* Hackathon communities
* College alumni groups
* Developer communities

---

## Why I Built This

I often join AI and startup communities where people introduce themselves by sharing LinkedIn profile URLs.

After seeing dozens of profiles shared inside WhatsApp groups, I wanted a faster workflow to:

* discover builders
* connect with founders
* expand my professional network
* reduce repetitive manual effort

So I vibe-coded this lightweight automation tool using Python.

---

## Future Improvements

* GUI with Streamlit
* Auto-tagging profiles by role/company
* CRM-style connection tracker
* AI-generated personalized connection notes
* Chrome extension integration
* Google Sheets sync

---

## Disclaimer

This project does NOT automate:

* LinkedIn login
* Sending connection requests
* WhatsApp scraping

Users should follow LinkedIn’s platform policies and send personalized connection requests responsibly.

---

## Author

**Muzammil Ibrahim P M**
Application Developer Intern @ IBM CIC Bangalore
Tech Enthusiast | Automation Builder | AI & Product Curious

GitHub: `github.com/muzammil-13`
