'''
Pulls shifts from my calendar
Jako Zeng
August 26, 2025
'''

from datetime import datetime, timezone
from googleapiclient.errors import HttpError

def get_existing_shifts(calendar_service, start_date, end_date):
    print("Checking for existing shifts in calendar...")
    try:
        print(datetime.now(timezone.utc))
    except HttpError as e:
        print(f"An error occurred: {e}")
        return []
    
if __name__ == "__main__":
    get_existing_shifts(None, None, None)