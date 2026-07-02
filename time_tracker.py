"""
Wiggles Time tracker.

This programme allows the user to track their time throughout the day,
view their previous days, and view their average times over the past 7
days.

They are given a selection of catagories to list their time under, and
pick one before entering how long in minutes theyve spend doing each
catagory.

The code saves all entries made to a Json file with a timestamp meaning
that all data can be grouped later in the history and analitics pages.

The goal of my code is to help people see if they have unhealthy time
managment to bring about awareness and productivity.
"""

import json
import easygui
import sys
from datetime import datetime

MINS_IN_DAY = 1440

def load_data():
    """
    Reads and returns the activity history data from the JSON
    file.
    """
    try:
        with open("activity_list.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_data(data):
    """
    Writes the current activity list data back to the JSON file.
    """
    
    with open("activity_list.json", "w") as file:
        json.dump(data, file, indent=4)


def validate_input(prompt_text):
    """
    Asks the user for a duration in minutes and validates the entry.
    Makes sure the input is a positive number under 1 day.
    Redirects to the home page if the user cancels.
    """
    while True:
        value = easygui.enterbox(prompt_text)

        # Check if they clicked the cancel or X button.
        if value is None:
            easygui.msgbox("Going home...")
            return None

        # Make sure they have inputted a valid input, and make sure the
        # amount they picked is no longer than a day.
        try:
            minutes = int(value)

            if minutes <= 0:
                easygui.msgbox("Cant enter negative numbers.")
                continue

            elif minutes >= MINS_IN_DAY:
                easygui.msgbox("Activity cannot be longer than 1 day.")
                continue
            else:
                # Give back the valid input to be used.
                return minutes

        except ValueError:
            easygui.msgbox("That's not a number. Try again.")


def add_activity_page():
    """
    Displays the activity selection menu and adds a valid entry to
    the database.
    """
    activities = ["Study/Work", "Sport", "Music", "Screen", "Family/Friends", 
                  "Other"]
    activities_select = easygui.choicebox(
        "Which catagory would you like to " "make an entry for?",
        "activities_select",
        activities,
    )

    if activities_select is None:
        easygui.msgbox("Exiting...")
        return None
    else:
        activities_hours = validate_input(
            f"How many minutes did you spend" f" doing {activities_select}?"
        )

        if activities_hours is not None:

            # Load data onto the variable entry_list.
            entry_list = load_data()

            # Add dictionary to the list.
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry_list.append(
                {
                    "timestamp": timestamp,
                    "activity": activities_select,
                    "minutes": activities_hours,
                }
            )

            # Save it back.
            save_data(entry_list)
            return None


def history_page():
    """
    Groups logged activity data by date and displays the history to the
    user.
    """
    history_pull = load_data()
    grouped_data = {}

    # Loop through the list items and add them to variables.
    for item in history_pull:
        date_only = item["timestamp"].split(" ")[0]
        activity_name = item["activity"]
        minutes = item["minutes"]

        # Make sure the date dictionary exists.
        if date_only not in grouped_data:
            grouped_data[date_only] = {}

        # Make sure the activity key exists under the date.
        if activity_name not in grouped_data[date_only]:
            grouped_data[date_only][activity_name] = 0

        # Add the minutes.
        grouped_data[date_only][activity_name] += minutes

    # Make the output text window.
    final_output = ""
    for date, activities in sorted(grouped_data.items()):
        final_output += f"Date: {date}\n"
        for action, mins in activities.items():
            final_output += f"  - {action}: {mins} mins\n"
        final_output += "\n"

    if not final_output:
        final_output = "No history found yet!"

    easygui.msgbox(final_output)
    return None


def analytics_page():
    """
    Calculates and displays daily average minutes per category and
    identifies the top activity.
    """
    # Making a variable that has my json file on it.
    activity_data = load_data()

    # Checking to see if they have any data inputted. If not, sending.
    # back to the home page.
    if not activity_data:
        easygui.msgbox("You have input data to view your analytics")
        return None

    # Make a list that will have the total minutes for each activity and
    # how many times each activity was used.

    totals = {
        "Screen": [0, 0],
        "Sport": [0, 0],
        "Study/Work": [0, 0],
        "Family/Friends": [0, 0],
        "Music": [0, 0],
        "Other": [0, 0],
    }

    now = datetime.now()
    has_recent_data = False

    # Go through the data, and add the minutes and amount of entries to
    # the appropriate lists if the entry is within 7 days.
    for entry in activity_data:
        entry_time = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
        days_ago = (now - entry_time).days
        category = entry["activity"]
        mins = entry["minutes"]

        # Match and update the specific category in the lists.
        if days_ago < 7:
            totals[category][0] += mins
            totals[category][1] += 1
            has_recent_data = True

    # If they have data, but none of it is from the last 7 days, display a message.
    if not has_recent_data:
        easygui.msgbox("No activity tracked in the past 7 days!")
        return None
        # Shows the total unupdated amount of times each activity was
        # entered.

    # Find the activity name with the most total minutes.
    highest_mins = -1
    popular_activity = "None"

    for activity_name, data_list in totals.items():
        
        # Extracting just the total minutes
        total_mins = data_list[0]
        if total_mins > highest_mins:
            highest_mins = total_mins
            popular_activity = activity_name

    # Build the text display so we can print it cleanly at the end.
    text = "Past 7 Days Analytics\n\n"
    text += "Daily Averages:\n"

    for activity_name, data_list in totals.items():

        # Extracting just the minutes before dividing by 7. (average over
        # past 7 days.)
        only_mins = data_list[0]
        daily_avg = only_mins / 7.0

        # Building each activities line and adding it to text.
        text += (f"  - {activity_name}: {daily_avg:.1f} mins a day\n")

    text += (f"\nMost Used Activity:\n")
    text += (f"  - {popular_activity} ({totals[popular_activity][0]}"
            " total mins)\n")

    # Display the results.
    easygui.msgbox(text, "Weekly Analytics")
    return None

def manage_entries_page():
    """
    Allows users to update or delete past log entries.
    """
    entry_list = load_data()

    if not entry_list:
        easygui.msgbox("No entries found to update or delete!")
        return None

    # Form a list of entries for selection.
    show_entries = []
    
    # Give each antry an index number so thay entries are numbered in 
    # order of date.
    for index, entry in enumerate(entry_list):
        show_entries.append(f"{index + 1}. [{entry['timestamp']}]"
                            f"{entry['activity']} - {entry['minutes']} mins")

    # Make the box be a button box if there is only one entry so that it
    # doesn't crash. But keep it as a choice box if there is more that 
    # one.
    if len(show_entries) == 1:
        selection = easygui.buttonbox("Select an entry to update or delete:", 
                                      "Manage Entries", show_entries)
    else:
        selection = easygui.choicebox("Select an entry to update or delete:", 
                                      "Manage Entries", show_entries)

    if selection is None:
        return None

    # Get the index number from the string chosen.
    selected_index = int(selection.split(".")[0]) - 1
    selected_entry = entry_list[selected_index]

    action = easygui.buttonbox(f"What would you like to do with this entry?"
                               f"\n\n{selection}","Select Action", 
                               ["Update Minutes", "Delete Entry", "Cancel"])
    
    if action == "Update Minutes":
        new_mins = validate_input(f"Enter new minutes for "
                                  f"{selected_entry['activity']}:")
        if new_mins is not None:
            entry_list[selected_index]["minutes"] = new_mins
            save_data(entry_list)
            easygui.msgbox("Entry successfully updated!")
            
    elif action == "Delete Entry":
        confirm = easygui.ynbox("Are you sure you want to permanently delete"
                                " this entry?", "Confirm Delete")
        if confirm:
            entry_list.pop(selected_index)
            save_data(entry_list)
            easygui.msgbox("Entry successfully deleted!")
            
    return None

def home_page():
    """
    Displays the all the pages that the user will need in my code.
    """
    pages = ["Add Entry", "View History", "Weekly Analytics", "Manage Entries",
             "Leave"]
    
    while True:
        home = easygui.buttonbox("Welcome to Wiggles Time Tracker!", "homepage"
                                 , pages)
        if home == "Add Entry":
            add_activity_page()
        elif home == "Manage Entries":
            manage_entries_page()
        elif home == "View History":
            history_page()
        elif home == "Weekly Analytics":
            analytics_page()
        else:
            easygui.msgbox("Thanks for using Wiggles Time Tracker :)")
            sys.exit()


home_page()
