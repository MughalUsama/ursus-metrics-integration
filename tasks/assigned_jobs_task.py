from celery import Task

from _15Five.objectives import create_objective, set_metric_value
from celery_app import app
import logging

from jobDiva.authenticate import authenticate_jobdiva
from jobDiva.assigned_jobs import fetch_new_updated_job_user_records,count_distinct_jobdivano_in_range
from settings import team_map
from utils import populate_objectives_data, get_last_week_range, get_obj_data_range

from jobDiva.users import get_user_id_by_email as get_jb_user_id_by_email
from _15Five.objectives import get_user_id_from_email as get_15Five_user_id_from_email
import logging

from celery import Task

from _15Five.objectives import create_objective, set_metric_value
from _15Five.objectives import get_user_id_from_email as get_15Five_user_id_from_email
from celery_app import app
from jobDiva.assigned_jobs import fetch_new_updated_job_user_records, count_distinct_jobdivano_in_range
from jobDiva.authenticate import authenticate_jobdiva
from jobDiva.users import get_user_id_by_email as get_jb_user_id_by_email
from settings import team_map
from utils import populate_objectives_data, get_last_week_range, get_obj_data_range

logger = logging.getLogger(__name__)


class AssignedJobsRecord(Task):
    def run(self):
        try:
            team = "RECRUITING_TEAM"
            job_diva_auth_token = authenticate_jobdiva()
            #  Get all new job records
            print("\n\nCreating assigned job records ...")
            response_data = fetch_new_updated_job_user_records(job_diva_auth_token)
            viewable_by_users = [get_15Five_user_id_from_email(user) for user in
                                 team_map.get(team, [])]
            viewable_by_users = [user for user in viewable_by_users if user]

            for member in team_map[team]:
                # Get jobdiva user id by email
                jd_user_id = get_jb_user_id_by_email(member, job_diva_auth_token)

                # Calculate total new jobs for the user
                jobs = count_distinct_jobdivano_in_range(response_data, jd_user_id, job_diva_auth_token)

                print(f"Total assigned jobs in JobDiva for {member}: {jobs}")
                # Get 15Five user id by email
                _15five_user_id = get_15Five_user_id_from_email(member)
                if not _15five_user_id:
                    print(f"USER NOT FOUND: {member}")
                    continue

                start_ts, end_ts = get_last_week_range("%Y-%m-%d")
                start_ts = "2024-07-15"
                end_ts = "2024-07-24"

                # metrics to upload
                key_results = [
                    {
                        "description": "Assigned Jobs",
                        "type": "number",
                        "start_value": 0,
                        "target_value": 5,
                    }
                ]

                # Format the date range
                date_range = get_obj_data_range()

                # Populate objectives data
                objectives = populate_objectives_data(
                    viewable_by_users=viewable_by_users,
                    user_id=_15five_user_id,
                    objective_description=f"Test Assigned Jobs - {date_range}",
                    start_ts=start_ts,
                    end_ts=end_ts,
                    key_results=key_results
                )
                print(objectives)
                # # Create objective in 15Five
                # result_objective = create_objective(objectives)
                # # print(result_objective)
                # # print(result_objective[0]["key_results"])
                # # Set value of key result
                # fills_key_result_id = result_objective[0]["key_results"][0]["id"]
                #
                # # Update key result value
                # set_metric_value(fills_key_result_id, jobs)

        except Exception as e:
            print(f"Error occurred: {e}")


assigned_jobs_task = app.register_task(AssignedJobsRecord())
