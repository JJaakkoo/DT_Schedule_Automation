'''
Processes the excel schedule file and returns a list of shifts in a format
Jako Zeng
August 19, 2025
'''

import pandas as pd
from datetime import datetime

def get_lower_bound_period(lower_bound, upper_bound):
    try:
        if type(lower_bound) != int:
            lower_bound = int(lower_bound.split(":")[0])
        if type(upper_bound) != int:
            upper_bound = int(upper_bound.split(":")[0])
        lower_bound, upper_bound = int(lower_bound), int(upper_bound)
        if 9 <= lower_bound < 12:
            return "am"
        else:
            return "pm"

    except ValueError:
        print("int conversion error")
        return "pm"
    
def process_time_cell(cell):
    #print(f"Processing cell: {cell}")
    # clean up the cell and splits it into start and end times
    cell = str(cell).strip()
    cell_times = cell.split("-")

    # get the location
    for i, cell_time in enumerate(cell_times):
        holder = 0
        location_holder = []
        for j,char in enumerate(cell_time):
            if type(char) == str and char.isalpha():
                location_holder.append(char)
        if location_holder != []:
            location = "".join(location_holder)
            holder = len(location)
        cell_times[i] = cell_times[i][holder:]

    #print(f"location: {location}, cell_times: {cell_times}")
    return location, cell_times

def process_schedule_file(file_path,name="jako"):

    print(f"Processing schedule file for {name}...")

    name = str(name).lower().strip()
    locations = {
        "H": "Heritage Square",
        "S": "Whyte Avenue",
        "N": "North Location",
        "DT": "Downtown"
        }
    year = str(file_path).split(" ")[5]

    try:

        shifts = []
        format_code = "%I:%M%p %d %b"
        added_shifts = False

        df = pd.read_excel(file_path)
        #print("Excel File read successfully")

        # Finds the coloumn my name is in
        my_col = None
        for i,cell in enumerate(df.iloc[0]):
            try:
                if cell.lower().strip() == name:
                    #print(f"Found {name} in column {i}: {cell.lower().strip()}")
                    my_col = i
                    break
            except AttributeError:
                continue
        if my_col is None:
            return f"Could not find {name} in the schedule"

        # processes the individual shifts and puts it into a list
        

        for i, cell in enumerate(df.iloc[:,my_col]):
            if "-" in str(cell).lower():

                location, time_bounds = process_time_cell(cell)
                #print(f"time_bounds: {time_bounds}")
                if ":" not in time_bounds[0]:
                    #print(f"adding :00 to {time_bounds[0]}")
                    time_bounds[0] = time_bounds[0]+":00"
                if ":" not in time_bounds[1]:
                    #print(f"adding :00 to {time_bounds[1]}")
                    time_bounds[1] = time_bounds[1]+":00"
                try:

                    #print(time_bounds)
                    start_time = f"{datetime.strptime(
                                start := f"{time_bounds[0]}{get_lower_bound_period(time_bounds[0],time_bounds[1])} {df.iloc[i,0]} {year}", 
                                f"{format_code} %Y"
                                )}"
                    end_time = f"{datetime.strptime(
                                end := f"{time_bounds[1]}pm {df.iloc[i,0]} {year}", 
                                f"{format_code} %Y"
                                )}"
                    
                    start_time = start_time.replace(" ", "T")
                    end_time = end_time.replace(" ", "T")

                    shifts.append({
                        "summary": f"Work at {locations[location]}",
                        "start": {
                            "dateTime": start_time,
                            "timeZone": "America/Edmonton"
                        },
                        "end": {
                            "dateTime": end_time,
                            "timeZone": "America/Edmonton"
                        },
                        "colorId": "11"
                    })
                    added_shifts = True
                    #print(f"{start} to {end}")
                    print(f"{df.iloc[i,0]} {time_bounds[0]}{get_lower_bound_period(time_bounds[0],time_bounds[1])}-{time_bounds[1]}pm ({locations[location]})")
                except KeyError:
                    continue
        if not added_shifts:  
            return f"Could not find any shifts for {name}"
        
        return shifts
    
    except FileNotFoundError:
        print(f"couldnt find the file: {file_path}")
    #except Exception as e:
        #print(f"An error occured: {e}")

if __name__ == "__main__":
    test_string = "Bobby, Kim, Hyo, Kristen, Chelsey, Jeremy, Sonja, Reane, Yujung, Tricia, Katrina, Jason, Jako, Nick, Alina, Sophia.H, Katelyn, Michael, Jessie, Emily, Phoebe, Terence, Amy, Ervin, Holly, Jacky, Rocky, Gian, Thomas, Sherry, Natalie, Rachel, Cathy".split(", ")
    file_name = "Dream Tea Schedule Aug 16-31 2025 Final for all locationstest.xlsx"
    if False:
        for test_name in test_string:
            process_schedule_file(file_name, name=test_name)
            print("\n")
    else:
        process_schedule_file(file_name, name="katrina")  
