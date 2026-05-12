import requests
from bs4 import BeautifulSoup

URL = "https://jobs.apple.com/en-us/search"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)

print("Status Code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

jobs_found = []

for link in soup.select("a[href]"):

    title = link.get_text(strip=True)
    href = link["href"]

    keywords = [
        "Product Manager",
        "Program Manager",
        "Technical Program Manager",
        "Fraud",
        "Risk",
        "Payments"
    ]

    if any(keyword.lower() in title.lower() for keyword in keywords):

        full_link = f"https://jobs.apple.com{href}"

        job_data = {
            "title": title,
            "link": full_link
        }

        if job_data not in jobs_found:
            jobs_found.append(job_data)

print("\nAPPLE JOB RESULTS\n")

for job in jobs_found:
    print(f"TITLE: {job['title']}")
    print(f"LINK: {job['link']}")
    print("-" * 50)
