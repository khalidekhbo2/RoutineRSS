from xml.etree.ElementTree import Element, SubElement, tostring
import datetime
import pytz
import subprocess

# Get current date and day name in Bangladesh time
bd_tz = pytz.timezone('Asia/Dhaka')
current_date_time_bd = datetime.datetime.now(bd_tz)
current_date = current_date_time_bd.strftime('%Y-%m-%d')
current_day_name = current_date_time_bd.strftime('%A')

# Check if it's past 2:30 PM
is_past_afternoon = current_date_time_bd.hour >= 14 and current_date_time_bd.minute >= 30

# Create an RSS feed XML structure
rss = Element("rss", version="2.0")
channel = SubElement(rss, "channel")

# Set the title of the RSS feed to "Routine"
title = SubElement(channel, "title")
title.text = "Routine"

# Add the current day as the first item
first_item = SubElement(channel, "item")

first_item_title = SubElement(first_item, "title")
first_item_title.text = current_day_name

first_item_description = SubElement(first_item, "description")
first_item_description.text = f"{current_day_name}'s Routine"

# Define class routines for each day
class_routines = {
    "Saturday": [
        {"name": "Orthosurgery/Urology", "time": "7:00AM - 8:00AM"},
        {"name": "Pharmacology", "time": "8:00AM - 9:00AM"},
        {"name": "Break", "time": "9:00AM - 9:30AM"},
        {"name": "Ward", "time": "9:30AM - 11:30AM"},
        {"name": "Microbiology", "time": "11:30AM - 12:30PM"},
        {"name": "Microbiology", "time": "12:30PM - 2:30PM"}
    ],
    "Sunday": [
        {"name": "Medicine", "time": "7:00AM - 8:00AM"},
        {"name": "Microbiology", "time": "8:00AM - 9:00AM"},
        {"name": "Break", "time": "9:00AM - 9:30AM"},
        {"name": "Ward", "time": "9:30AM - 11:30AM"},
        {"name": "Break", "time": "11:30AM - 12:30PM"},
        {"name": "Pathology", "time": "12:30PM - 2:30PM"}
    ],
    "Monday": [
        {"name": "Pathology", "time": "7:00AM - 8:00AM"},
        {"name": "Pharmacology", "time": "8:00AM - 9:00AM"},
        {"name": "Break", "time": "9:00AM - 9:30AM"},
        {"name": "Ward", "time": "9:30AM - 11:30AM"},
        {"name": "Microbiology", "time": "11:30AM - 12:30PM"},
        {"name": "Pharmacology", "time": "12:30PM - 2:30PM"}
    ],
    "Tuesday": [
        {"name": "Pediatrics", "time": "7:00AM - 8:00AM"},
        {"name": "Pathology", "time": "8:00AM - 9:00AM"},
        {"name": "Break", "time": "9:00AM - 9:30AM"},
        {"name": "Ward", "time": "9:30AM - 11:30AM"},
        {"name": "Pharmacology", "time": "11:30AM - 12:30PM"},
        {"name": "Microbiology", "time": "12:30PM - 2:30PM"}
    ],
    "Wednesday": [
        {"name": "Surgery", "time": "7:00AM - 8:00AM"},
        {"name": "Microbiology", "time": "8:00AM - 9:00AM"},
        {"name": "Break", "time": "9:00AM - 9:30AM"},
        {"name": "Ward", "time": "9:30AM - 11:30AM"},
        {"name": "Pathology", "time": "11:30AM - 12:30PM"},
        {"name": "Pathology", "time": "12:30PM - 2:30PM"}
    ],
    "Thursday": [
        {"name": "Obs. & Gyne", "time": "7:00AM - 8:00AM"},
        {"name": "Pharmacology", "time": "8:00AM - 9:00AM"},
        {"name": "Break", "time": "9:00AM - 9:30AM"},
        {"name": "Ward", "time": "9:30AM - 11:30AM"},
        {"name": "Pathology", "time": "11:30AM - 12:30PM"},
        {"name": "Pharmacology", "time": "12:30PM - 2:30PM"}
    ]
}

# Determine the routines to add based on the time of day
target_day = current_day_name if not is_past_afternoon else (current_date_time_bd + datetime.timedelta(days=1)).strftime('%A')

if target_day and target_day in class_routines:
    # Add class routines for the target day to the RSS feed
    for class_info in class_routines[target_day]:
        item = SubElement(channel, "item")

        class_title = SubElement(item, "title")
        class_title.text = class_info["name"]

        class_description = SubElement(item, "description")
        class_description.text = class_info["time"]

    # Convert the XML structure to a string
    rss_feed_str = tostring(rss, encoding="utf-8").decode("utf-8")

    # Write the RSS feed to a file
    rss_filename = f'rss_feed.xml'
    with open(rss_filename, 'w') as rss_file:
        rss_file.write(rss_feed_str)

    print(f"{target_day} class routines RSS feed generated successfully.")

    # Add and commit the changes using Git
    subprocess.run(["git", "add", rss_filename])
    commit_message = f"Update class routines for {target_day}"
    subprocess.run(["git", "commit", "-m", commit_message])

    print("Changes committed to Git.")
else:
    print(f"No routine available for {current_day_name}.")
