import json
from datetime import datetime

import requests

from utils import get_last_week_range

# Define API endpoints
first_api_url = "https://api.jobdiva.com/apiv2/bi/NewUpdatedJobUserRecords"
second_api_url = "https://api.jobdiva.com/apiv2/bi/JobsDetail"


def fetch_new_updated_job_user_records(auth_token):
    from_date, to_date = get_last_week_range()

    params = {
        "fromDate": from_date,
        "toDate": to_date,
        "alternateFormat": ""
    }
    response = requests.get(first_api_url, params=params,
                            headers={'Authorization': auth_token})
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error fetching data from {first_api_url}: {response.status_code}: {response.text}")
        return []


def fetch_jobs_detail(job_ids, auth_token):
    job_ids_param = "&".join([f"jobIds={job_id}" for job_id in job_ids])
    response = requests.get(f"{second_api_url}?{job_ids_param}", headers={'Authorization': auth_token})
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error fetching data from {second_api_url}: {response.status_code}")
        return []


def count_distinct_jobdivano_in_range(job_user_records, user_id, auth_token):
    from_date, to_date = get_last_week_range(add_day_to_to_date=True)
    from_date = datetime.strptime(from_date, "%m/%d/%Y")
    to_date = datetime.strptime(to_date, "%m/%d/%Y")
    job_ids = []
    for record in job_user_records:
        if record.get("USERID") == user_id and record.get("PRIMARYRECRUITER") == "1":
            job_ids.append(record.get("JOBID"))

    if job_ids:
        jobs_detail_data = fetch_jobs_detail(job_ids, auth_token=auth_token)
        filtered_jobs = [job for job in jobs_detail_data if
                         from_date <= datetime.strptime(job["DATEISSUED"], "%Y-%m-%dT%H:%M:%S") <= to_date]
        distinct_jobdivano_count = len(set(job.get("JOBDIVANO") for job in filtered_jobs))
        return distinct_jobdivano_count
    else:
        print(f"No jobs found for user_id {user_id} as primary recruiter.")
        return 0
