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
def validate_input(input):
    print("placeholder")


#Make a time entry
def add_activity_page():
    activities = ["Study/Work", "Sport", "Music", "Screen", "Family/Friends", \
"Other"]
    activities_select = easygui.choicebox("Which catagory would you like\
 to make an entry for?", "activities_select", activities)
    activities_hours = easygui.enterbox(f"How many minutes did you spend doing\
 {activities_select}?")

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