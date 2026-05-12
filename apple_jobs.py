import requests
from bs4 import BeautifulSoup
import json
import os

URL = "https://jobs.apple.com/en-us/search?search=product%20manager"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

jobs = []

for link in soup.find_all("a"):
    text = link.get_text(strip=True)

    if "Product" in text or "Program" in text:
        jobs.append(text)

print("Found Jobs:")
for job in jobs:
    print(job)
