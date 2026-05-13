import requests
from bs4 import BeautifulSoup
import json
import os

URLS = [
    "https://jobs.apple.com/en-us/search?location=austin-AST",
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

keywords = [
    "Product Manager",
    "Program Manager",
    "Technical Program Manager",
    "TPM"
]

allowed_locations = [
    "Austin",
    "Remote"
]

if os.path.exists("jobs.json"):
    with open("jobs.json", "r") as file:
        previous_jobs = json.load(file)
else:
    previous_jobs = []

jobs_found = []

def is_recent(text):

    text = text.lower()

    if "today" in text or "just posted" in text:
        return True

    if "day" in text:

        try:
            days = int(text.split()[0])

            return days <= 7

        except:
            return False

    return False

for URL in URLS:

    response = requests.get(URL, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    page_text = soup.get_text()

    for link in soup.select("a[href]"):

        title = link.get_text(strip=True)
        href = link["href"]

        if any(keyword.lower() in title.lower() for keyword in keywords):

            if any(location.lower() in page_text.lower() for location in allowed_locations):

                full_link = f"https://jobs.apple.com{href}"

                job_data = {
                    "title": title,
                    "link": full_link
                }

                if job_data not in previous_jobs:

                    jobs_found.append(job_data)

print("\nNEW JOB RESULTS\n")

if len(jobs_found) == 0:
    print("No new jobs found today.")

for job in jobs_found:

    print(f"🍎 TITLE: {job['title']}")
    print(f"🔗 LINK: {job['link']}")
    print("-" * 50)

with open("jobs.json", "w") as file:
    json.dump(jobs_found, file, indent=4)
