import requests
from bs4 import BeautifulSoup
import json
import os

URL = "https://www.google.com/about/careers/applications/jobs/results/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)

print("Status Code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

jobs_found = []

if os.path.exists("google_jobs.json"):
    with open("google_jobs.json", "r") as file:
        previous_jobs = json.load(file)
else:
    previous_jobs = []

for link in soup.select("a[href]"):

    title = link.get_text(strip=True)
    href = link["href"]

    keywords = [
        "Product Manager",
        "Program Manager",
        "Technical Program Manager",
        "Fraud",
        "TPM",
        "WPC",
        "Risk",
        "Payments"
    ]

    if any(keyword.lower() in title.lower() for keyword in keywords):
        allowed_locations = [
            "Austin,TX",
            "Austin,Texas",
            "Austin",
            "Remote"
        
        ]

        page_text = soup.get_text()

        if any(location.lower() in page_text.lower() for location in allowed_locations):

            full_link = f"https://jobs.apple.com{href}"

            job_data = {
                "title": title,
                "link": full_link
            }

        if job_data not in previous_jobs:
            jobs_found.append(job_data)
            print("NEW JOB FOUND:", title)
if len(jobs_found) == 0:
    print("No new jobs found today.")
    
print("\nGOOGLE JOB RESULTS\n")

for job in jobs_found:
    print(f"🍎 TITLE: {job['title']}")
    print(f"🔗 LINK: {job['link']}")
    print("-" * 50)

with open("jobs.json", "w") as file:
    json.dump(jobs_found, file, indent=4)
