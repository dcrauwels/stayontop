import constants
import os
from datetime import datetime

# header row for csv logfile
CSV_HEADER = "Timestamp, Email_found, Location, Form_sent"


def split_and_clean(location: str) -> list: 
    '''splits string "location" by constants.SEPARATOR, strips leading / trailing whitespace'''
    if constants.SEPARATOR == '': # if your usecase does not have a relevant separator
        return [location]
    locations = location.split(',') 
    cleaned_locations = list(map(lambda x: x.strip(), locations))
    return cleaned_locations # should be of the format [street, city]

def write_log(email_found: bool, location: str, form_sent: bool) -> None:
    '''Takes a `content` string and writes it to a logfile in the current directory. Logfile is named by date at YYYY-MM-DD, log entry is timed at HH:MM:SS.'''

    # get current date, time
    now = datetime.now()
    current_date = now.date()
    current_time = now.strftime("%H:%M:%S")

    # setup log
    log_name = f"{current_date}-stayontop-log.csv"
    log_exists = os.path.exists(log_name)

    with open(log_name, 'a') as log:
        if not log_exists: # this means it's the first log of the day
            log.write(CSV_HEADER) 
        log_value = ','.join(str(arg) for arg in [current_time, email_found, location, form_sent]) # convert to strings
        log.write(f"{log_value}\n")

    return None