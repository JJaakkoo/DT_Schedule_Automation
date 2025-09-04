'''
Adds shifts to Google Calendar from a list of shifts in a format
Jako Zeng
August 14, 2025'''

from googleapiclient.errors import HttpError   

def add_events_to_calendar(calendar_service, events):
    print("Adding events to calendar...")

    failed_events = 0

    for event in events:
        print(f"Adding: {event.get('summary', "Unknown Shift")} at {event.get("start", {}).get("dateTime", "Unknown Time")}...")

        try:
            event = calendar_service.events().insert(
                calendarId='primary', 
                body=event
            ).execute()
            print(f"Shift added: {event.get('htmlLink')}")
            

        except HttpError as error:
            print(f"An error occurred: {error}")
            print("Failed to add shift.")
            failed_events += 1

    return failed_events