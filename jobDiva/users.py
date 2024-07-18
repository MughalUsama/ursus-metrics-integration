import requests


def get_user_id_by_email(email, authorization_header):
    url = f'https://api.jobdiva.com/apiv2/bi/UserDetail?userEmail={email}'
    headers = {
        'Authorization': authorization_header,
        'accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get('data'):
            user_data = data['data'][0]
            user_id = user_data.get('USERID')
            return user_id
    return None
