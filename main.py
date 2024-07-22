# from datetime import datetime, timedelta
#
# from jobDiva.authenticate import authenticate_jobdiva
# from jobDiva.new_job_orders import get_new_job_records
# from utils import calculate_total_for_user, populate_objectives_data
# from jobDiva.users import get_user_id_by_email as get_jb_user_id_by_email
# from _15Five.objectives import create_objective, set_metric_value
# from _15Five.objectives import get_user_id_from_email as get_15Five_user_id_from_email
#
# _15Five_api_key = "0fd289d9a6374cbb85f42eca962b2657"
# team_map = {"SALES_TEAM": ["subhan.sm73@gmail.com"]}
#
#
# def main():
#     # Authenticate JobDiva
#     clientid = "1747"
#     username = "subhan.sm73@gmail.com"
#     password = "jq!RG-X6!kmF67t"
#     job_diva_auth_token = authenticate_jobdiva()
#     #  Get all new job records
#
#     response_data = get_new_job_records(job_diva_auth_token)
#
#     for user_email in emails_to_map:
#         # Get jobdiva user id by email
#         jd_user_id = get_jb_user_id_by_email(user_email, job_diva_auth_token)
#         # Calculate total new jobs for the user
#
#         jobs = calculate_total_for_user(response_data, "2516131", "JOBDIVANO", "PRIMARYSALESID")
#
#         print(f"Total new jobs in JobDiva for {user_email}: {jobs}")
#
#         # Get 15Five user id by email
#         _15five_user_id = get_15Five_user_id_from_email(_15Five_api_key, "subhan.sm73@gmail.com")
#
#         end_ts = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
#         start_ts = (datetime.now() - timedelta(days=0)).strftime("%Y-%m-%d")
#         team = "SALES_TEAM"
#         viewable_by_users = [get_15Five_user_id_from_email(_15Five_api_key, user) for user in team_map.get(team, [])]
#
#         # metrics to upload
#         key_results = [
#                 {
#                     "description": "New Jobs",
#                     "type": "number",
#                     "start_value": 0,
#                     "target_value": 5,
#                 }
#             ]
#         # Populate objectives data
#         objectives = populate_objectives_data(
#             viewable_by_users=viewable_by_users,
#             user_id=_15five_user_id,
#             objective_description=f"Test for Newly Updated Jobs  - 29 May",
#             start_ts=start_ts,
#             end_ts=end_ts,
#             key_results=key_results
#         )
#         print(viewable_by_users)
#         print(objectives)
#         # Create objective in 15Five
#         result_objective = create_objective(_15Five_api_key, objectives)
#         print(result_objective)
#         # print(result_objective[0]["key_results"])
#         # Set value of key result
#         fills_key_result_id = result_objective[0]["key_results"][0]["id"]
#
#         # Update key result value
#         set_metric_value(_15Five_api_key, fills_key_result_id, jobs)
#         # set_metric_value(_15Five_api_key, openings_key_result_id, openings)
#
#
#
# if __name__ == "__main__":
#     main()


from tasks.new_msa_sent_task import CreateNewMSAsSent
from tasks.client_meetings_conducted_task import CreateClientMeetingsConducted
from tasks.ring_central_dials_task import CreateRingCentralDials
from tasks.new_job_records_task import CreateNewJobRecords
from tasks.assigned_jobs_task import AssignedJobsRecord


# Uncomment below to run directly from this script.

# AssignedJobsRecord().run()
# CreateNewJobRecords().run()
# CreateNewMSAsSent().run()
# CreateClientMeetingsConducted().run()
# CreateRingCentralDials().run()
