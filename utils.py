import json
from datetime import datetime, timedelta


def get_last_week_range(use_iso_format=False, add_day_to_to_date=False, format=None):
    """
    Get the date range for the last week
    :param use_iso_format:
    :param add_day_to_to_date:
    """
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    # Calculate how many days to subtract to get the last Monday
    days_since_last_monday = (today.weekday() - 6) % 7
    last_monday = today - timedelta(days=days_since_last_monday + 7)
    last_sunday = last_monday + timedelta(days=6)
    from_date = "07/07/2024"
    to_date = "07/13/2024"
    last_monday = datetime.strptime(from_date, "%m/%d/%Y")
    last_sunday = datetime.strptime(to_date, "%m/%d/%Y")
    # Select the date format based on the boolean parameter
    if use_iso_format:
        date_format = "%Y-%m-%dT%H:%M:%S"
    elif format:
        date_format = format
    else:
        date_format = "%m/%d/%Y"

    # Format the dates as strings using the selected format
    from_date = last_monday.strftime(date_format)
    to_date = last_sunday.strftime(date_format)

    # Add one day to to_date if the parameter is True
    if add_day_to_to_date:
        to_date_dt = last_sunday + timedelta(days=1)
        to_date = to_date_dt.strftime(date_format)

    return from_date, to_date


def calculate_total_for_field(data, user_id, field_name):
    from_date, to_date = get_last_week_range(add_day_to_to_date=True)
    from_date = datetime.strptime(from_date, "%m/%d/%Y")
    to_date = datetime.strptime(to_date, "%m/%d/%Y")
    total = 0
    for record in data["data"]:
        if record.get("USERID") == user_id and from_date <= datetime.strptime(record["ACTION_DATE"],
                                                                              "%Y-%m-%dT%H:%M:%S") < to_date:
            total += int(record.get(field_name, 0))  # Assuming the field contains integer values
    return total


def calculate_total_for_user(data, jd_user_id, field_name, id_type="USERID"):
    """
    Caculates total unique records of certain type
    :param data: list of objects to process
    :param jd_user_id: user_id for which total is being calculated
    :param field_name: unique field to count
    :param id_type: name of user_id field in object
    :return: count of unique field for a user
    """
    unique_values = set()
    from_date, to_date = get_last_week_range(add_day_to_to_date=True)
    from_date = datetime.strptime(from_date, "%m/%d/%Y")
    to_date = datetime.strptime(to_date, "%m/%d/%Y")
    count = 0
    for record in data["data"]:
        if record.get(id_type, None) == jd_user_id:
            value = record.get(field_name, None)
            if value is not None and from_date <= datetime.strptime(record["ISSUEDATE"],
                                                                    "%Y-%m-%dT%H:%M:%S") < to_date and record[
                "JOBSTATUS"] != "IGNORED":
                unique_values.add(value)
    return len(unique_values)


def populate_objectives_data(viewable_by_users, user_id, objective_description, start_ts, end_ts, key_results):
    objectives_data = [
        {
            "description": objective_description,
            "start_ts": start_ts,
            "end_ts": end_ts,
            "visibility": "public",
            "scope": "individual",
            "user_id": user_id,
            "viewable_by_users": viewable_by_users,
            "key_results": key_results
        }
    ]
    return objectives_data


def count_outgoing_calls(data, user_id):
    valid_types = ["Outgoing Call", "Incoming Call", "LinkedIn Hiring Manager Outreach", "Outgoing Text Message"]
    from_date, to_date = get_last_week_range(add_day_to_to_date=True)
    from_date = datetime.strptime(from_date, "%m/%d/%Y")
    to_date = datetime.strptime(to_date, "%m/%d/%Y")
    count = 0
    for record in data:
        if record["RECORD_OWNER_USERID"] == user_id:
            if record["ACTIONTYPE"] in valid_types and from_date <= datetime.strptime(
                    record["ACTION_DATE"], "%Y-%m-%dT%H:%M:%S") < to_date:
                count += 1
    return count


def count_client_meetings(data, user_id):
    count = 0
    from_date, to_date = get_last_week_range(add_day_to_to_date=True)
    from_date = datetime.strptime(from_date, "%m/%d/%Y")
    to_date = datetime.strptime(to_date, "%m/%d/%Y")
    for record in data["data"]:
        if record["RECORD_OWNER_USERID"] == user_id and "Client Meeting" in record["ACTIONTYPE"].strip():
            if from_date <= datetime.strptime(record["ACTION_DATE"], "%Y-%m-%dT%H:%M:%S") < to_date:
                count += 1
    return count


def count_msa(data, user_id):
    count = 0
    from_date, to_date = get_last_week_range(add_day_to_to_date=True)
    from_date = datetime.strptime(from_date, "%m/%d/%Y")
    to_date = datetime.strptime(to_date, "%m/%d/%Y")
    for record in data["data"]:
        if record["RECORD_OWNER_USERID"] == user_id and record["ACTIONTYPE"].strip() == "MSA - Sent to Client":
            if from_date <= datetime.strptime(record["ACTION_DATE"], "%Y-%m-%dT%H:%M:%S") < to_date:
                count += 1
    return count


def get_obj_data_range():
    return "-".join(get_last_week_range(format="%d-%m-%Y"))
