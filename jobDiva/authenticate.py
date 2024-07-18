import requests

from settings import jobdiva_clientid, jobdiva_username, jobdiva_password


def authenticate_jobdiva():
    url = "https://api.jobdiva.com/apiv2/authenticate"
    params = {
        "clientid": jobdiva_clientid,
        "username": jobdiva_username,
        "password": jobdiva_password
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.text
        else:
            return {"error": f"Failed to authenticate. Status code: {response.status_code}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


# clientid = "1747"
# username = "subhan.sm73@gmail.com"
# password = "jq!RG-X6!kmF67t"
# auth_response = authenticate_jobdiva(clientid, username, password)
# print(auth_response)
