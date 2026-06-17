import json
import easygui
from easygui import *
import sys
from datetime import datetime


def load_data():
    """
    Reads and returns the activity history data from the JSON
    file.
    """
    with open("activity_list.json", "r") as file:
        return json.load(file)


def save_data(data):
    """
    Writes the current activity list data back to the JSON file.
    """
    with open("activity_list.json", "w") as file:
        json.dump(data, file, indent=4)


def validate_input(input_):
    """
    Asks the user for a duration in minutes and validates the entry.
    Makes sure the input is a positive number under 1 day.
    Redirects to the home page if the user cancels.
    """
    while True:
        value=easygui.enterbox(input_)

        # Check if they clicked the cancel or X button.
        if value is None:
            msgbox("Going home...")
            home_page()

        # Make sure they have inputted a valid input, and make sure the
        # amount they picked is no longer than a day.
        try:
            minutes=int(value)

            if minutes <= 0:
                msgbox("Cant enter negative numbers.")
                continue

            elif minutes >= 1440:
                msgbox("Activity cannot be longer than 1 day.")
                continue
            else:
                # Give back the valid input to be used.
                return minutes

        except ValueError:
            msgbox("That's not a number. Try again.")


def add_activity_page():
    """
    Displays the activity selection menu and adds a valid entry to
    the database.
    """
    activities=["Study/Work", "Sport", "Music", "Screen", "Family/Friends", \
"Other"]
    activities_select=easygui.choicebox("Which catagory would you like to \
make an entry for?", "activities_select", activities)
    
    if activities_select is None:
        easygui.msgbox("Exiting...")
        home_page()
    else:
        activities_hours=validate_input(f"How many minutes did you spend \
doing {activities_select}?")
        
        if activities_hours is not None:

            # Load data onto the variable entry_list.
            entry_list=load_data()

            # Add dictionary to the list.
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry_list.append({
                "timestamp": timestamp,
                "activity": activities_select,
                "minutes": activities_hours
            })

            # Save it back.
            save_data(entry_list)
            home_page()


def history_page():
    """
    Groups logged activity data by date and displays the history to the
    user.
    """
    history_pull=load_data() 
    grouped_data={}

    # Loop through the list items and add them to variables.
    for item in history_pull:
        date_only=item["timestamp"].split(" ")[0]
        activity_name=item["activity"]
        minutes=item["minutes"]
        
        # Make sure the date dictionary exists.
        if date_only not in grouped_data:
            grouped_data[date_only]={}
            
        # Make sure the activity key exists under the date.
        if activity_name not in grouped_data[date_only]:
            grouped_data[date_only][activity_name]=0
            
        # Add the minutes.
        grouped_data[date_only][activity_name] += minutes

    # Make the output text window.
    final_output=""
    for date, activities in sorted(grouped_data.items()):
        final_output += f"Date: {date}\n"
        for action, mins in activities.items():
            final_output += f"  - {action}: {mins} mins\n"
        final_output += "\n"
        
    if not final_output:
        final_output="No history found yet!"

    msgbox(final_output)
    home_page()


def analytics_page():
    """
    Calculates and displays daily average minutes per category and 
    identifies the top activity.
    """
    # Making a variable that has my json file on it.
    activity_data=load_data()

    # Checking to see if they have any data inputted. If not, sending.
    # back to the home page.
    if not activity_data:
        msgbox("You have input data to view your analytics")
        home_page()

    # Make a list that will have the total minutes for each activity and
    # how many times each activity was used.
    screen=[0, 0]
    sport=[0, 0]
    work=[0, 0]
    family=[0, 0]
    music=[0, 0]
    other=[0, 0]

    data=False

    # Go through the data, and add the minutes and amount of entries to
    # the appropiate lists.
    for entry in activity_data:
        data=True
        category=entry["activity"]
        mins=entry["minutes"]

        # Match and update the specific category in the lists.
        if category == "Screen":
            screen[0] += mins
            screen[1] += 1
        elif category == "Sport":
            sport[0] += mins
            sport[1] += 1
        elif category == "Study/Work":
            work[0] += mins
            work[1] += 1
        elif category == "Family/Friends":
            family[0] += mins
            family[1] += 1
        elif category == "Music":
            music[0] += mins
            music[1] += 1
        elif category == "Other":
            other[0] += mins
            other[1] += 1

        # If they input data just not in the last 7 days, then display
        # message.
        if not data:
            msgbox("No activity tracked in the past 7 days!")
            return home_page()
        
        # Shows the total unupdated amount of times each activity was 
        # entered.
        totals={
        "Screen": screen[0],
        "Sport": sport[0],
        "Study/Work": work[0],
        "Family/Friends": family[0],
        "Music": music[0],
        "Other": other[0]
    }

    # Find the activity name with the most total minutes.
    popular_activity=max(totals, key=totals.get)

    # Build the text display so we can print it cleanly at the end.
    text="Past 7 Days Analytics\n\n"
    text += "Daily Averages:\n"
    
    for activity_name, total_mins in totals.items():

        # Dividing the total minutes of the past 7 days by 7.  
        daily_avg=total_mins / 7.0
        
        # Building each activities line and adding it to text.
        text += f"  - {activity_name}: {daily_avg:.1f} mins a day\n"

    text += f"\nMost Used Activity:\n"
    text += f"  - {popular_activity} ({totals[popular_activity]} \
total mins)\n"

    # Display the results.
    msgbox(text, "Weekly Analytics")
    home_page()


def home_page():
    """ 
    Displays the all the pages that the user will need in my code.
    """
    pages=["Add Entry", "View History", "Weekly Analytics", "Leave"]
    home=easygui.buttonbox("Welcome to Wiggles Time Tracker!", "homepage",\
pages)
    if home == "Add Entry":
        return add_activity_page()
    elif home == "View History":
        history_page()
    elif home == "Weekly Analytics":
        analytics_page()
    else:
        easygui.msgbox("Thanks for using Wiggles Time T racker :)")
        sys.exit()


home_page()