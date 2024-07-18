import json

import requests
from datetime import datetime, timedelta

from utils import get_last_week_range


def get_new_job_records(auth_token):
    # Calculate fromDate and toDate
    from_date, to_date = get_last_week_range()

    url = "https://api.jobdiva.com/apiv2/bi/NewUpdatedJobRecords"
    params = {
        "fromDate": from_date,
        "toDate": to_date
    }
    headers = {
        "Authorization": auth_token
    }
    response = requests.get(url, params=params, headers=headers)
    return response.json()
