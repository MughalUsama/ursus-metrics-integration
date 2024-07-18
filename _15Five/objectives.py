import requests
from settings import _15Five_api_key


def create_objective(objectives_data):
    # Check if objectives_data is a non-empty list
    if not isinstance(objectives_data, list) or not objectives_data:
        raise ValueError("Objectives data must be a non-empty list")

    # Check if all objectives have the required fields
    for objective in objectives_data:
        required_fields = ["description", "start_ts", "end_ts", "scope", "user_id"]
        missing_fields = [field for field in required_fields if field not in objective]
        if missing_fields:
            raise ValueError(f"Missing required fields for objective: {missing_fields}")

        # Check if values are from provided options
        allowed_scopes = ["company-wide", "group-type", "individual", "self-development"]
        if "scope" in objective and objective["scope"] not in allowed_scopes:
            raise ValueError(f"Invalid scope value for objective: {objective['scope']}")

        if 'visibility' in objective:
            valid_visibilities = ["public", "report", "custom"]
            if objective['visibility'] not in valid_visibilities:
                raise ValueError("Invalid value for 'visibility' field")

    # Perform API request
    url = 'https://my.15five.com/api/public/objective/'
    headers = {
        'Authorization': f'bearer {_15Five_api_key}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=objectives_data)
    # Check response status
    if response.status_code != 200:
        print(response.json())
        print(response.text)

        raise ValueError(f"Failed to create objective. Status code: {response.status_code}")

    return response.json()


def get_user_id_from_email(email:str):
    url = 'https://my.15five.com/api/public/user'
    headers = {
        'Authorization': f'bearer {_15Five_api_key}',
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(response.text)
        raise ValueError(f"Failed to retrieve user data. Status code: {response.status_code}")

    users = response.json().get('results', [])
    for user in users:
        if user.get('email').lower() == email.lower():
            if user.get('is_active'):
                return user.get('id')
            return None

    raise ValueError(f"User with email '{email}' not found")


def get_group_id_from_email(api_key, email):
    url = 'https://my.15five.com/api/public/user'
    headers = {
        'Authorization': f'bearer {api_key}',
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise ValueError(f"Failed to retrieve user data. Status code: {response.status_code}")

    users = response.json().get('results', [])
    for user in users:
        if user.get('email') == email:
            return user.get('company_groups_ids', [])

    raise ValueError(f"User with email '{email}' not found")


def set_metric_value(key_result_id, value):
    # Perform API request
    url = f'https://my.15five.com/api/public/key-result/{key_result_id}/update-value/'
    headers = {
        'Authorization': f'bearer {_15Five_api_key}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json={"current_value": value})
    # Check response status
    if response.status_code != 200:
        raise ValueError(f"Failed to update value. Status code: {response.status_code}")

    return response.json()

#
# objectives_data = [
#     {
#         # Description of the objective
#         "description": "Another test objective",
#
#         # Start date of the objective
#         "start_ts": "2024-05-01",
#
#         # End date of the objective
#         "end_ts": "2024-12-31",
#
#         # Visibility of the objective (options: "public", "report", "custom")
#         "visibility": "custom",
#
#         # Scope of the objective (options: "company-wide", "group-type", "individual", "self-development")
#         "scope": "individual",
#
#         # User ID of the owner of the objective
#         "user_id": user_id,
#
#         # List of user IDs who can view the objective
#         "viewable_by_users": [
#             user_id
#         ],
#
#         # Key results associated with the objective
#         "key_results": [
#             {
#                 # Description of the key result
#                 "description": "Increase revenue to $20000",
#
#                 # Type of key result (options: "currency", "boolean", "number", "percent")
#                 "type": "number",
#
#                 # Start value for the key result
#                 "start_value": 1000,
#
#                 # Target value for the key result
#                 "target_value": 2000,
#
#                 # Owner user's ID for the key result
#                 "owner_id": user_id
#             }
#         ]
#     }
# ]
#
# try:
#     response = create_objective(api_key, objectives_data)
#     print("Created Objective:", response)
# except ValueError as e:
#     print("Error:", e)
