from datetime import timedelta, datetime

from celery import Task

from _15Five.objectives import create_objective, set_metric_value
from celery_app import app
import logging

from jobDiva.authenticate import authenticate_jobdiva
from jobDiva.ring_central_dials import get_outgoing_calls
from settings import team_map
from utils import count_outgoing_calls, populate_objectives_data, get_last_week_range, get_obj_data_range

from jobDiva.users import get_user_id_by_email as get_jb_user_id_by_email
from _15Five.objectives import get_user_id_from_email as get_15Five_user_id_from_email

logger = logging.getLogger(__name__)


class CreateRingCentralDials(Task):
    def run(self):
        try:
            print("\n\nCreating Ring Central Dials ...")
            team = "SALES_TEAM"
            job_diva_auth_token = authenticate_jobdiva()
            #  Get all new job records

            response_data = get_outgoing_calls(job_diva_auth_token)
            # print(response_data)
            for member in team_map[team]:
                # Get jobdiva user id by email
                jd_user_id = get_jb_user_id_by_email(member, job_diva_auth_token)

                # Calculate total new jobs for the user
                dials = count_outgoing_calls(response_data, jd_user_id)

                print(f"Total ring central dials by {member}: {dials}")

                # Get 15Five user id by email
                _15five_user_id = get_15Five_user_id_from_email(member)
                if not _15five_user_id:
                    continue
                start_ts, end_ts = get_last_week_range("%Y-%m-%d")
                start_ts = "2024-07-12"
                end_ts = "2024-07-22"
                # viewable_by_users = [get_15Five_user_id_from_email(user) for user in
                #                      team_map.get(team, [])]
                # viewable_by_users = [user for user in viewable_by_users if user]
                # viewable_by_users = [11790663, 10968120, 11036004, 10982134, 12058109, 12398093, 12516049, 12608216,
                #                      10907478]
                viewable_by_users = [11790663, 11036004, 10982134, 12058109, 12608216,
                                     10907478]
                # metrics to upload
                key_results = [
                    {
                        "description": "Dials",
                        "type": "number",
                        "start_value": 0,
                        "target_value": 150,
                    }
                ]
                # Format the date range
                date_range = get_obj_data_range()
                # Populate objectives data
                objectives = populate_objectives_data(
                    viewable_by_users=viewable_by_users,
                    user_id=_15five_user_id,
                    objective_description=f"Ring Central Dials - {date_range}",
                    start_ts=start_ts,
                    end_ts=end_ts,
                    key_results=key_results
                )

                # Create objective in 15Five
                result_objective = create_objective(objectives)
                # print(result_objective)
                # print(result_objective[0]["key_results"])
                # Set value of key result
                fills_key_result_id = result_objective[0]["key_results"][0]["id"]

                # Update key result value
                set_metric_value(fills_key_result_id, dials)

        except Exception as e:
            logger.error(f"Error in CreateClientMeetingsConducted task: {str(e)}")


create_ring_central_dials_task = app.register_task(CreateRingCentralDials())
