import os
import requests
from dotenv import load_dotenv
from supabase import create_client

# Load variables from .env into this script's environment
load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create a connection to your Supabase database
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Adzuna's endpoint for UK job search, page 1
url = "https://api.adzuna.com/v1/api/jobs/gb/search/1"

params = {
    "app_id": APP_ID,
    "app_key": APP_KEY,
    "results_per_page": 10,
    "what": "graduate software engineer",
    "content-type": "application/json"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    jobs = data["results"]
    print(f"Found {len(jobs)} jobs:\n")

    for job in jobs:
        job_row = {
            "title": job["title"],
            "company": job["company"]["display_name"],
            "location": job["location"]["display_name"],
            "url": job["redirect_url"],
            "source": "adzuna"
        }

        # Insert this job into the 'jobs' table in Supabase
        supabase.table("jobs").insert(job_row).execute()
        print(f"Inserted: {job_row['title']} - {job_row['company']}")

else:
    print(f"Error {response.status_code}: {response.text}")