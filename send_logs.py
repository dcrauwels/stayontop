import emailutils
from os import listdir
import pathlib
from datetime import datetime

def main() -> None:
    '''This is purely for nightly logging purposes. Set up a cronjob to run this around 1 am or something. Make sure you set the cronjob for the actual email checking, website scraping yada yada to run between like 4 am and 12 am.'''
    # get current date, time
    now = datetime.now()
    current_date = now.date()
    
    # construct email subject, body, log attachment path
    subject = f"Stayontop logs for {current_date}"
    body = ""
    logs = listdir("logs")

    # sanity check
    if len(logs) == 0:
        print("No logs found.")
        return None
    
    # shit out logs to email and delete em
    for l in logs:
        attachment_path = "logs/" + l
        # send email
        emailutils.send_email(subject, body, attachment_path)
        # delete logs
        pathlib.Path.unlink(attachment_path)

    return None

if __name__ == "__main__":
    main()