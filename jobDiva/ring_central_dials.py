import requests

from utils import get_last_week_range


def get_outgoing_calls(auth_token):
    from_date, to_date = get_last_week_range()
    url = f'https://api.jobdiva.com/apiv2/bi/NewUpdatedContactNoteRecords?fromDate={from_date}&toDate={to_date}'
    headers = {
        'Authorization': auth_token
    }

    response = requests.get(url, headers=headers)
    data = response.json().get('data', [])
    return data
