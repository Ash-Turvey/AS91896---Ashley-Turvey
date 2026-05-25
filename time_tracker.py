import json
import easygui
from easygui import *

#Pull data from json file
def load_data():
    print("placeholder")

#Save data to json file
def save_data(data):
    with open("activity_list.json", "w") as file:
        json.dump(data, file, indent = 2)

#Check to make sure that the input is able to be used
def validate_input(input):
    print("placeholder")

#Make a time entry
def add_activity(activity):
    print("placeholder")

#Show either todays daily summary or another days summary
def daily_summary():
    print("placeholder")

#Show daily average for activities in the past 7 days, and show most
#done activities
def analytics(data):
    print("placeholder")


