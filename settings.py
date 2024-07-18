import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
jobdiva_clientid = os.getenv("JOBDIVA_CLIENTID")
jobdiva_username = os.getenv("JOBDIVA_USERNAME")
jobdiva_password = os.getenv("JOBDIVA_PASSWORD")

_15Five_api_key = os.getenv("API_KEY_15FIVE")

team_map = {
    "SALES_TEAM": ["CaitlinR@ursusinc.com",
                   "JoshE@ursusinc.com", "AshleyN@ursusinc.com", "KyleQ@ursusinc.com", "MariamF@ursusinc.com",
                   "JenA@ursusinc.com", "BethB@ursusinc.com", "AndrewP@ursusinc.com", "NancyB@ursusinc.com",
                   "Meganr@ursusinc.com",
                   "NancyC@ursusinc.com"
                   ]}
