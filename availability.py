import pandas as pd
import datetime

# Check to see if an employee is available to work a certain shift
def checkAvailability(shiftStart: datetime.datetime, shiftEnd: datetime.datetime, empID: int, employees: pd.DataFrame):
    # Dictionary to convert int to day of week
    dayConvert = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
    # Account for shifts that extend into a different day
    if(shiftStart.date() == shiftEnd.date()):
        day = dayConvert.get(shiftStart.weekday())
        availability = employees[employees['empID'] == empID][day]

        # Check all availabilities
        for i in availability:
            for j in i:
                # If availability starts before shift start and ends after shift end, employee is available
                if(j[0] <= shiftStart.time() and j[1] >= shiftEnd.time()):
                    return True
        return False
    else:
        # TODO
        return False

# Loop through all employees to find those that are available to work a certain shift
def getAvailableEmployees(shiftStart: datetime.datetime, shiftEnd: datetime.datetime, employees: pd.DataFrame):
    availableEmployees = []

    for index, row in employees.iterrows():
        if(checkAvailability(shiftStart, shiftEnd, row['empID'], employees)):
            availableEmployees.append(row['empID'])

    return tuple(availableEmployees)
