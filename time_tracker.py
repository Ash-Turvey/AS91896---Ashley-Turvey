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
    #building a list with the ways people spend their time.
    activities = ["Study/Work", "Sport", "Music", "Screen", "Family/Friends", \
"Other"]
    
    #letting them pick one
    activities_select = easygui.choicebox("Which catagory would you like \
to make an entry for?", "activities_select", activities)
    
    #Checking to make sure they clicked one, and making them do it again
    #if not
    if activities_select is None:
        easygui.msgbox("Exiting...")
        home_page()

    #Ask for minutes, and make sure its valid using the valid input 
    #function
    else:
        activities_hours = validate_input(f"How many minutes did you spend \
doing {activities_select}?")
        
        #Making the timestamped entry
        if activities_hours is not None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry_list[timestamp] = {
                "activity": activities_select,
                "minutes": activities_hours,
            }
            time_checker = entry_list[timestamp][entry_list]
            print(time_checker)
            #Save the entry to the json file
            save_data(entry_list)

            #Loop back to home page after adding
            home_page()

#Show whole history
def history_page():
    history_pull = load_data() 
    grouped_data = defaultdict(list)

    #make the output look presentable by sorting everything by date, and
    #printing each days activitys together
    for timestamp, details in history_pull.items():
        date_only = timestamp.split(" ")[0] 
        activity_text = f"{details['activity']} ({details['minutes']} mins)"
        grouped_data[date_only].append(activity_text)

    final_output = ""

    #Loop through the grouped data, and append each section of the data
    #to final output, ready to be put in a msgbox
    for date, activities in grouped_data.items():
        final_output += f"Date: {date}\n"
        for action in activities:
            final_output += f"  - {action}\n"
        final_output += "\n"
        
    #put all the data from the previous loops into a msgbox
    msgbox(final_output)
    home_page()

#Show daily average for activities in the past 7 days, and show most
#done activities
def analytics_page(data):
    print("placeholder")

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



"""
history_pull = load_data() 
    
    # 1. Create a dictionary that automatically starts an empty list for new dates
    grouped_data = defaultdict(list)
    
    # 2. Loop through JSON keys (timestamps) and values (activity details)
    for timestamp, details in history_pull.items():
        # Split the string by space and take the first part: "2026-05-29"
        date_only = timestamp.split(" ")[0] 
        
        # Format how you want the individual activity text to look
        activity_text = f"{details['activity']} ({details['minutes']} mins)"
        
        # Add it to the list for that specific date
        grouped_data[date_only].append(activity_text)
        
    # 3. Build your single message box string
    final_output = ""
    for date, activities in grouped_data.items():
        final_output += f"Date: {date}\n"
        for act in activities:
            final_output += f"  - {act}\n"
        final_output += "\n" # Blank line between different dates
        
    msgbox(final_output)
"""