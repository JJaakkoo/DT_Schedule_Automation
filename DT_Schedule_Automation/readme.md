Dream Tea Schedule Automation
This project automates the process of extracting work schedules from Gmail attachments and synchronizing them directly to Google Calendar. It eliminates the need for manual data entry by parsing Excel files and creating calendar events automatically.

Prerequisites
Before running the scripts, ensure you have the following installed and configured:

Python 3.x: This project is built using Python (tested on version 3.13).

Google Cloud Project: A project created in the Google Cloud Console with the following APIs enabled:

Gmail API

Google Calendar API

OAuth Credentials: A credentials.json file downloaded from your Google Cloud Project (OAuth 2.0 Client ID).

Installation
1. Clone or Copy the Files
Ensure the following files are in your project directory:

main.py: The entry point of the application.

auth.py: Handles the Google API authentication flow.

email_extractor.py: Searches and downloads the schedule from Gmail.

schedule_processor.py: Processes the Excel data.

calendar_adder.py: Uploads events to Google Calendar.

2. Install Required Libraries
Run the following command in your terminal to install the necessary Python packages:

Bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib pandas openpyxl httplib2
Setup and Configuration
Google Cloud Authentication
Place your credentials.json file in the root folder of the project.

The first time you run the script, a browser window will open asking you to log in to your Google account.

Once authorized, a token.json file will be created automatically. This file stores your login session so you do not have to log in every time.

Customization
Open email_extractor.py and ensure the search_query matches the sender and subject line of the emails you receive:

Python
search_query = 'from:dreamteahousejacky@gmail.com subject:"Schedule" has:attachment'
Usage
To start the automation, run the main script from your terminal:

Bash
python main.py
The script will perform the following steps:

Authenticate with Google Services.

Search Gmail for the latest schedule email.

Download the Excel attachment.

Parse the shifts and dates.

Add the shifts to your Google Calendar.

Clean up the downloaded Excel file to keep your folder organized.

Troubleshooting
Timeout Errors: If the script fails to connect, it includes a retry logic and a 10 second timeout setting to handle network fluctuations.

Authentication Issues: If you experience login loops, delete the token.json file and run the script again to force a fresh login.