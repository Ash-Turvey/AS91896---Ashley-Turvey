import json
import easygui
from easygui import *
import sys

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

        if value is None:
            msgbox("Going home...")
            home_page()
        


        try:
            minutes = float(value)

            if minutes <= 0:
                msgbox("Cant enter negative numbers.")
                continue

            elif minutes >= 1440:


        except ValueError:
            counter += 1
            if counter < 5:
                msgbox("That's not a number. Try again.")



#Make a time entry
def add_activity_page():
    #building a list with the ways people spend their time.
    activities = ["Study/Work", "Sport", "Music", "Screen", "Family/Friends", \
"Other"]
    
    #letting them pick one
    activities_select = easygui.choicebox("Which catagory would you like \
to make an entry for?", "activities_select", activities)
    
    #checking to make sure they clicked one, and making them do it again
    #if not
    if activities_select is None:
        easygui.msgbox("Exiting...")
        home_page()

    else:
        activities_hours = validate_input(f"How many minutes did you spend \
doing {activities_select}?")
        
        if activities_hours is None:
            print("none")
        else:
            return activities_hours, activities_select


    return activities_select, activities_hours

#Show either todays daily summary or another days summary
def history_page():
    print("placeholder")

#Show daily average for activities in the past 7 days, and show most
#done activities
def analytics_page(data):
    print("placeholder")

def home_page():
    pages = ["Add Entry", "View History", "Weekly Analytics", "Leave"]
    home = easygui.buttonbox("Welcome to Wiggles Time Tracker!", "homepage",\
pages)
    if home == "Add Entry":
        add_activity_page()
    elif home == "View History":
        history_page()
    elif home == "Weekly Analytics":
        analytics_page()
    else:
        sys.exit()
home_page()