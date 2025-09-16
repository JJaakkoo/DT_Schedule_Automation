'''
MAIN MAIN MAIN
Jako Zeng
August 14, 2025
'''
import os
from auth import authenticate
from email_puller import FDprocess
from schedule_processor import process_schedule_file, map_shifts, shift_sync_instructions
from calendar_pusher import add_events_to_calendar, delete_events_from_calendar
from calendar_puller import get_existing_events, find_existing_shifts

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
    shifts, start, end = process_schedule_file(downloaded_file, name="jako")
    os.remove(downloaded_file)
    if shifts and type(shifts) == list:
        print(f"Success! Processed {len(shifts)} shifts\n")
    else:
        print(f"Failed to process schedule file: {shifts}, exiting")
        return

    print(f"start date: {start}, end date: {end}")
    start_date = int(start.split(" ")[0])
    end_date = int(end.split(" ")[0])

    # Check if there are already shifts in the calendar that are within the date range
    current_shifts = find_existing_shifts(get_existing_events(calendar_service, start, end))
    
    #Given shifts

    print("\nShifts found in the given schedule:")
    given_shifts = []
    for shift in shifts: 
        given_shifts.append(f"{shift["start"]["dateTime"]} to {shift["end"]["dateTime"]}: {shift["summary"]}")
    print("Mapped shifts:")
    mapped_given_shifts = map_shifts(start_date, end_date, given_shifts)
    for day in mapped_given_shifts:
        print(f"{day}: {mapped_given_shifts[day]}")

    # Existing shifts

    print("\nShifts already in calendar:")
    print("Mapped shifts:")
    mapped_current_shifts = map_shifts(start_date, end_date, current_shifts)
    for day in mapped_current_shifts:
        print(f"{day}: {mapped_current_shifts[day]}")

    
    # Push shifts to calendar first time
    if len(current_shifts) == 0:
        shift_fails = add_events_to_calendar(calendar_service, given_shifts)
        if shift_fails == 0:
            print("Successfully added shifts to calendar!")
        else:
            print(f"Failed to add {shift_fails} shifts to calendar, exiting")
            return
    else:
    # Create instructions for syncing shifts
        print("\nCreating sync shift instructions...")
        sync_instructions = shift_sync_instructions(mapped_given_shifts, mapped_current_shifts)

    # Execute instructions
        print("\nExecuting sync instructions...")
        if True:
            for instruction in sync_instructions:
                if instruction["instruction"] == "add":
                    shift_fails = add_events_to_calendar(calendar_service, [instruction["event"]])
                    if shift_fails == 0:
                        print("Successfully added shift to calendar!\n")
                    else:
                        print(f"Failed to add shift to calendar")
                elif instruction["instruction"] == "delete":
                    shift_fails = delete_events_from_calendar(calendar_service, [instruction])
                    if shift_fails > 0:
                        print(f"Failed to delete {shift_fails} shifts from calendar")
                else:
                    print(f"Unknown instruction: {instruction}")
    
if __name__ == "__main__":
    main()