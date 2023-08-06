import arrow
import csv
import datetime
import nytid.schedules
import re
import requests

SIGNUP_SHEET_HEADER = [
  "Event", "Start", "End", "#Rooms",
  "#Needed TAs"
]
def needed_TAs(event):
  """
  Takes an event and returns the number of TAs needed
  """
  num_groups = event.description.split().count("grupp")
  if num_groups == 0:
    num_groups = event.description.split().count("group")

  num_rooms = len(event.location.split(","))

  num_TAs = max(num_rooms, num_groups)

  if "laboration" in event.name or "Laboration" in event.name:
    num_TAs = round(num_TAs * 1.5)

  return num_TAs
  
def generate_signup_sheet(course, url, needed_TAs=needed_TAs):
  """
  Input:
  - course is a string containing the file name used for output.
  - url is the URL to the ICS-formatted calendar.
  - needed_TAs is a function computing the number of needed TAs based on the 
    event. The default is the needed_TAs function in this module.

  Output:
  Returns nothing. Writes output to {course}.csv.
  """
  with open(f"{course}.csv", "w") as out:
    csvout = csv.writer(out, delimiter="\t")
    calendar = nytid.schedules.read_calendar(url)

    max_num_TAs = 0
    rows = []

    for event in calendar.timeline:
      if "Övning" in event.name or \
          "laboration" in event.name or "Laboration" in event.name:
        num_TAs = needed_TAs(event)
        if num_TAs > max_num_TAs:
          max_num_TAs = num_TAs

        rows.append([
          event.name,
          event.begin.to("local").format("YYYY-MM-DD HH:mm"),
          event.end.to("local").format("YYYY-MM-DD HH:mm"),
          len(event.location.split(",")),
          num_TAs
        ])

    csvout.writerow(SIGNUP_SHEET_HEADER +
      [f"TA username" for n in range(max_num_TAs)] +
        ["..."])

    csvout.writerows(rows)
def read_signup_sheet_from_file(filename):
  """
  Input: filename is a string containing the file name of the CSV file of the 
  sign-up sheet.

  Output: All the rows of the CSV as a Python list.
  """
  with open(filename, "r") as f:
    csvfile = csv.reader(f)
    return list(csvfile)[1:]
def read_signup_sheet_from_url(url):
  """
  Input: url is a string containing the URL of the CSV file of the sign-up 
  sheet.

  Output: All the rows of the CSV as a Python list.
  """
  response = requests.get(url)
  if response.status_code != 200:
    raise ValueError(response.text)

  response.encoding = response.apparent_encoding
  csvdata = response.text.splitlines()
  return list(csv.reader(csvdata))[1:]
def google_sheet_to_csv_url(share_url):
  """
  Input: The share URL of a Google Sheets sheet.

  Output: A URL that downloads (exports) the sheet in CSV format.
  """
  match = re.search("/edit.*$", share_url)
  if not match:
    raise ValueError(f"{share_url} doesn't seem like a Google Sheets URL.")

  url = share_url[:match.start()]
  return url + "/export?format=csv"
def get_TAs_from_csv(csv_row):
  """
  Input: takes a CSV data row as from a csv.reader.

  Output: returns the list of signed TAs.
  """
  return csv_row[len(SIGNUP_SHEET_HEADER):]
def hours_per_TA(csv_rows):
  """
  Input: Rows of CSV data as from csv.reader.

  Output: a dictionary mapping a TA to the number of hours they signed up for 
  in the sign-up sheet, {TA: hours}
  """
  TA_hours = {}

  start_index = SIGNUP_SHEET_HEADER.index("Start")
  end_index = SIGNUP_SHEET_HEADER.index("End")
  event_index = SIGNUP_SHEET_HEADER.index("Event")

  for row in csv_rows:
    time = (arrow.get(row[end_index], "YYYY-MM-DD HH:mm") - \
      arrow.get(row[start_index], "YYYY-MM-DD HH:mm"))

    time = round_time(time)
    time = add_prep_time(time, row[event_index])

    for assistant in get_TAs_from_csv(row):
      if assistant in TA_hours:
        TA_hours[assistant] += time
      else:
        TA_hours[assistant] = time

  return TA_hours
def total_hours(csv_rows):
  """
  Input: Rows of CSV data as from csv.reader.

  Output: Total number of hours spent on the course.
  """
  total = 0.0
  TA_hours = hours_per_TA(csv_rows)
  TA_hours[""] = 0

  for _, hours in TA_hours.items():
    total += float(hours)

  return total
def max_hours(csv_rows):
  """
  Input: takes the rows of CSV as output from csv.reader.

  Output: returns the maximum number of hours (using maximum TAs needed).
  """
  start_index = SIGNUP_SHEET_HEADER.index("Start")
  end_index = SIGNUP_SHEET_HEADER.index("End")
  event_index = SIGNUP_SHEET_HEADER.index("Event")
  needed_TAs_index = SIGNUP_SHEET_HEADER.index("#Needed TAs")

  max_hours = datetime.timedelta()

  for row in csv_rows:
    time = (arrow.get(row[end_index], "YYYY-MM-DD HH:mm") - \
      arrow.get(row[start_index], "YYYY-MM-DD HH:mm"))

    time = round_time(time)
    time = add_prep_time(time, row[event_index])

    max_num_TAs = int(row[needed_TAs_index])

    max_hours += time * max_num_TAs

  return max_hours
def round_time(time):
  """
  Input: a datetime.timedelta object time.

  Output: the time object rounded according to KTH rules.
  """
  HOUR = 60*60
  QUARTER = 15*60

  total_seconds = time.total_seconds()
  full_hours = (total_seconds // HOUR) * HOUR
  part_hour = total_seconds % HOUR

  if part_hour >= 3*QUARTER:
    return datetime.timedelta(seconds=full_hours+HOUR)
  elif part_hour > 2*QUARTER:
    return datetime.timedelta(seconds=full_hours+2*QUARTER)
  elif part_hour >= QUARTER:
    return datetime.timedelta(seconds=full_hours+2*QUARTER)

  return datetime.timedelta(seconds=full_hours)
def add_prep_time(time, event_type):
  """
  Input: a datetime.timedelta object time,
    a string containing the title of the event.

  Output: the time object rounded according to KTH rules.
  """
  if "laboration" in event_type or "Laboration" in event_type:
    time *= 1.33
  elif "Övning" in event_type:
    time *= 2

  return time
def compute_amanuensis_data(csv_rows, low_percentage=0.1):
  """
  Input:
    - csv_rows, the CSV rows as output from csv.reader.
    - low_percentage, the lowest acceptable percentage of employment.

  Output: a dictionary {TA: (start, end, hours)} mapping the TA username to a 
  tuple (start, end, hours) with the start and end time and the total number of 
  hours.
  """
  start_index = SIGNUP_SHEET_HEADER.index("Start")
  end_index = SIGNUP_SHEET_HEADER.index("End")
  event_index = SIGNUP_SHEET_HEADER.index("Event")
  needed_TAs_index = SIGNUP_SHEET_HEADER.index("#Needed TAs")

  ta_hours = hours_per_TA(csv_rows)
  ta_data = {}

  for ta in ta_hours.keys():
    earliest_date = arrow.get(csv_rows[0][start_index], "YYYY-MM-DD")
    latest_date = arrow.get(csv_rows[0][end_index], "YYYY-MM-DD")

    for row in csv_rows:
      start_date = arrow.get(row[start_index], "YYYY-MM-DD")
      end_date = arrow.get(row[end_index], "YYYY-MM-DD")

      if start_date < earliest_date:
        earliest_date = start_date
      if end_date > latest_date:
        latest_date = end_date

    hours = ta_hours[ta].total_seconds()/60/60

    earliest_month = arrow.get(
      f"{earliest_date.year}-{earliest_date.month:02d}-01",
      "YYYY-MM-DD")
    latest_month = arrow.get(
      f"{latest_date.year}-{latest_date.month:02d}-01",
      "YYYY-MM-DD").shift(months=1, seconds=-1)

    if compute_percentage(earliest_month, latest_month, hours) >= low_percentage:
      earliest_date = earliest_month
      latest_date = latest_month
    elif compute_percentage(earliest_date, latest_month, hours) >= low_percentage:
      latest_date = latest_month

    ta_data[ta] = (earliest_date, latest_date, hours)

  return ta_data
def compute_percentage(start, end, hours):
  """
  Input: start and end as arrow.arrow.Arrow or datetime.date objects,
    hours as a float.

  Output: a float in the interval [0, 1], which is the percentage of full time.
  """
  days = (end - start).total_seconds()/60/60/24
  full_time = 40 * days / 7
  return hours / full_time

def main():
  COURSES = {
    "DD1310": 
    "https://cloud.timeedit.net/kth/web/public01/ri.ics?sid=7&p=0.w%2C12.n&objects=453080.10&e=220609&enol=t&ku=29&k=1B9F3AD696BCA5C434C68950EFD376DD",
    "DD1317": 
    "https://cloud.timeedit.net/kth/web/public01/ri.ics?sid=7&p=0.w%2C12.n&objects=455995.10&e=220609&enol=t&ku=29&k=BA4400E3C003685549BC65AD9EAD3DC58E"
  }

  for course, url in COURSES.items():
    generate_signup_sheet(course, url)

if __name__ == "__main__":
    main()
