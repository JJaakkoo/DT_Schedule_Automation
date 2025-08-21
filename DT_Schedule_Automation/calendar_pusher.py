'''
Adds shifts to Google Calendar from a list of shifts in a format
Jako Zeng
August 14, 2025'''

from googleapiclient.errors import HttpError   

def add_shifts_to_calendar(calendar_service, shifts):
    print("Adding shifts to calendar...")

    failed_shifts = 0

    for shift in shifts:
        print(f"Adding: {shift.get('summary', "Unknown Shift")} at {shift.get("start", {}).get("dateTime", "Unknown Time")}...")

        try:
            event = calendar_service.events().insert(
                calendarId='primary', 
                body=shift
            ).execute()
            print(f"Shift added: {event.get('htmlLink')}")
            

        except HttpError as error:
            print(f"An error occurred: {error}")
            print("Failed to add shift.")
            failed_shifts += 1

    return failed_shifts