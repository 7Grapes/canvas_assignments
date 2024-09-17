# Import the Canvas class
from datetime import datetime
from canvasapi import Canvas
import pandas as pd
import pytz
from datetime import datetime, timedelta
from pytz import timezone
from dotenv import load_dotenv
import os
load_dotenv()
env = os.environ
# Canvas API URL
API_URL = "https://canvas.vt.edu/"
# Canvas API key
#retreive api key from .env file
API_KEY = env.get("API_KEY")

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)
# find user id with this guide: https://support.cidilabs.com/knowledgebase/what-is-the-canvas-user-id
userID = 202822
user = canvas.get_user(userID)
# courses = user.get_courses(enrollment_status='active') <-- this line doesnt work as intended idk why
# course id is the 6 digit number at the end of a course home page "https://canvas.vt.edu/courses/XXXXXX"
Embedded_Systems = canvas.get_course(196132)
Signals_and_Systems = canvas.get_course(196144)
Integrated_Design_Project = canvas.get_course(196173)
Physical_Electronics = canvas.get_course(196101)
Data_Structures_and_Algorithms = canvas.get_course(196002)

courses = [Embedded_Systems, Signals_and_Systems, Integrated_Design_Project, Physical_Electronics, Data_Structures_and_Algorithms]
# ece_2564_assignments = ece_2564.get_assignments()
# ece_2714_assignments = ece_2714.get_assignments()
# ece_2214_assignments = ece_2214.get_assignments()
# cs_2114_assignments = cs_2114.get_assignments()
# ece_2804_assignments = ece_2804.get_assignments()
#getting the assignment names for each course
def get_assignment_names(course):
    assignment_names = []
    for assignment in course.get_assignments():
        assignment_names.append(assignment.name)
    return assignment_names
def export_course_assignments(course, course_name):
    for assignment in course.get_assignments():
        #only append assignments whos due date has not passed yet
        if assignment.due_at is not None:
            # convert utc due date to est
            utc_due_date = datetime.strptime(assignment.due_at, "%Y-%m-%dT%H:%M:%SZ")
            est_tz = pytz.timezone('US/Eastern')
            est_due_date = utc_due_date.astimezone(est_tz)
            due_date = est_tz.normalize(est_due_date)
            due_date = due_date - timedelta(hours=4)  # Subtract 4 hours from the due date
            due_date = due_date.strftime("%m/%d/%y %I:%M %p")
            #separate date and time
            due_date_parts = due_date.split()
            if len(due_date_parts) >= 3:
                due_date = due_date_parts[0]
                due_time = due_date_parts[1] + " " + due_date_parts[2]
            else:
                due_date = ""
                due_time = ""
            # print(utc_due_date)
            # print(est_due_date)
            if datetime.strptime(assignment.due_at, "%Y-%m-%dT%H:%M:%SZ") > datetime.now():
                data.append([course_name, assignment.name, due_date, due_time])
                
data = []
for course in courses:
    # trying to get the course name from the course object
    export_course_assignments(course, course.name.split("Fall")[0].split(":")[0])
    
df = pd.DataFrame(data, columns=['Course', 'Assignments', 'Due Date', 'Due_Time'])
#sort the rows in the dataframe by due date
df = df.sort_values(by=['Due Date'])

# print(df)
# print(data)
#export df to csv
#test
df.to_csv('assignments.csv', index=False)