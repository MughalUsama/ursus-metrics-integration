import requests
from datetime import datetime, timedelta

from utils import get_last_week_range


def fetch_contact_note_records(auth_token):

    # Calculate dates for the last 7 days
    from_date, to_date  = get_last_week_range()

    # URL
    url = f'https://api.jobdiva.com/apiv2/bi/NewUpdatedContactNoteRecords?fromDate={from_date}&toDate={to_date}'

    # Make the request
    response = requests.get(url, headers={'Authorization': auth_token, 'accept': 'application/json'})

    # Check for response status
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

