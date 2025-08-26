'''
MAIN MAIN MAIN
Jako Zeng
August 14, 2025
'''
import os
from auth import authenticate
from email_puller import FDprocess
from schedule_processor import process_schedule_file
from calendar_pusher import add_shifts_to_calendar

def main():
    # Authentication
    gmail_service, calendar_service = authenticate()

    if gmail_service and calendar_service:
        print("Authentication successful!\n")
    else:
        print("Authentication failed, exiting")
        return
    
    # Pull excel file from email
    downloaded_file = FDprocess(gmail_service)
    if downloaded_file:
        print(f"Success! {downloaded_file} has been downloaded\n")
    else:
        print("Failed to download schedule file, exiting")
        return

    # Process excel file
    shifts = process_schedule_file(downloaded_file, name="jako")
    os.remove(downloaded_file)
    if shifts and type(shifts) == list:
        print(f"Success! Processed {len(shifts)} shifts\n")
    else:
        print(f"Failed to process schedule file: {shifts}, exiting")
        return
    # Check if there are already shifts in the calendar that are within the date range
    
    # Push shifts to calendar
    
    '''shift_fails = add_shifts_to_calendar(calendar_service, shifts)
    if shift_fails == 0:
        print("Successfully added shifts to calendar!")
    else:
        print(f"Failed to add {shift_fails} shifts to calendar, exiting")
        return
    '''

    
if __name__ == "__main__":
    main()