import json
import easygui
from easygui import *
import sys
from datetime import datetime
from collections import defaultdict

entry_list = {
    
}

#Pull data from json file
def load_data():
    with open("activity_list.json", "r") as file:
        return json.load(file)

#Save data to json file
def save_data(data):
    with open("activity_list.json", "w") as file:
        json.dump(data, file, indent = 4)

#Check to make sure that the input is able to be used
def validate_input(input_):
    while True:
        value = easygui.enterbox(input_)

        #check if they clicked the cancel or X button
        if value is None:
            msgbox("Going home...")
            home_page()

        #Make sure they have inputted a valid input, and make sure the
        #amount they picked is no longer than a day.
        try:
            minutes = int(value)

            if minutes <= 0:
                msgbox("Cant enter negative numbers.")
                continue

            elif minutes >= 1440:
                msgbox("Activity cannot be longer than 1 day.")
                continue
            else:
                        #give back the valid input to be used
                return minutes

        except ValueError:
            msgbox("That's not a number. Try again.")

#Make a time entry
def add_activity_page():
    activities = ["Study/Work", "Sport", "Music", "Screen", "Family/Friends", \
"Other"]
    activities_select = easygui.choicebox("Which catagory would you like to \
make an entry for?", "activities_select", activities)
    
    if activities_select is None:
        easygui.msgbox("Exiting...")
        home_page()
    else:
        activities_hours = validate_input(f"How many minutes did you spend \
doing {activities_select}?")
        
        if activities_hours is not None:
            #Load data
            entry_list = load_data()

            #Add dictionary to the list
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry_list.append({
                "timestamp": timestamp,
                "activity": activities_select,
                "minutes": activities_hours
            })

            #Save it back
            save_data(entry_list)
            home_page()

#Show whole history
def history_page():
    history_pull = load_data() 
    grouped_data = {}

    # 1. Simple, clean loop through the list items
    for item in history_pull:
        date_only = item["timestamp"].split(" ")[0]
        activity_name = item["activity"]
        minutes = item["minutes"]
        
        #Make sure the date dictionary exists
        if date_only not in grouped_data:
            grouped_data[date_only] = {}
            
        #Make sure the activity key exists under the date
        if activity_name not in grouped_data[date_only]:
            grouped_data[date_only][activity_name] = 0
            
        #Add the minutes
        grouped_data[date_only][activity_name] += minutes

    #Make the output text window
    final_output = ""
    for date, activities in sorted(grouped_data.items()):
        final_output += f"Date: {date}\n"
        for action, mins in activities.items():
            final_output += f"  - {action}: {mins} mins\n"
        final_output += "\n"
        
    if not final_output:
        final_output = "No history found yet!"

    msgbox(final_output)
    home_page()

#Show daily average for activities in the past 7 days, and show most
#done activities
def analytics_page():
    activity_data = load_data()
    screen = [0, 0]
    sport = [0, 0]
    work = [0, 0]
    family = [0, 0]
    music = [0, 0]
    other = [0, 0]
    for mean_activity in activity_data:

    for mean_time in activity_data():
#The page where the other pages can be accessed from.
def home_page():
    pages = ["Add Entry", "View History", "Weekly Analytics", "Leave"]
    home = easygui.buttonbox("Welcome to Wiggles Time Tracker!", "homepage",\
pages)
    if home == "Add Entry":
        return add_activity_page()
    elif home == "View History":
        history_page()
    elif home == "Weekly Analytics":
        analytics_page()
    else:
        sys.exit()

home_page()



#I need to continue the analytics page. 