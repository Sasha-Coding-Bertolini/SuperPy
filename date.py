import csv
from datetime import date, timedelta, datetime
from files import date_file


# Find and store current date in date.csv
def store_date():
    now = date.today()
    return now


# reset the date to today's date
def reset_date():
    with open(date_file, "w", newline="") as time:
        writer = csv.DictWriter(time, fieldnames=["current_date"])
        writer.writeheader()
        writer.writerow({"current_date": store_date()})


# set the date to a specific date
def set_date(date):
    with open(date_file, "w", newline="") as time:
        writer = csv.DictWriter(time, fieldnames=["current_date"])
        writer.writeheader()
        writer.writerow({"current_date": date})


# Read the current date
def read_date():
    with open(date_file, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            return list(row.values())[0]


# Create function that advances date by supplied days
def update_date(num_days):
    filename = date_file
    fieldnames = ["current_date"]

    # Read the current date from the CSV file
    with open(filename, "r") as file:
        reader = csv.DictReader(file, fieldnames=fieldnames)
        for row in reader:
            current_date = row["current_date"]

    # Parse the current date into a datetime object
    current_date = datetime.strptime(current_date, "%Y-%m-%d")

    new_date = current_date - timedelta(days=num_days)

    # Format the new date as a string
    new_date_str = datetime.strftime(new_date, "%Y-%m-%d")

    # Write the new date to the CSV file
    with open(filename, "w") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({"current_date": new_date_str})

    print(f"The date has been updated to {new_date_str}.")



# Create function that manipulates date, but doesn't change the current date in the program.
# This can be used for example when reporting on revenue or profit over specific time period.
def manipulate_date(num_days):
    with open(date_file, "r") as file:
        reader = csv.DictReader(file, fieldnames=["current_date"])
        for row in reader:
            current_date = row["current_date"]

        # Parse the current date into a datetime object
        current_date = datetime.strptime(current_date, "%Y-%m-%d")

        # subtract days to the current date

        new_date = current_date - timedelta(days=num_days)

        # Format the new date as a string
        new_date_str = datetime.strftime(new_date, "%Y-%m-%d")
        return new_date_str
