import imaplib
import smtplib
import email
import constants # server address, username, password, agency address etc. are stored here. You have to set this yourself.
import re
import strutils
from email.header import decode_header
from email.mime.text import MIMEText

def email_checker() -> str:
    # Connect to imap server
    try:
        mail = imaplib.IMAP4_SSL(constants.IMAP_SERVER)
        mail.login(constants.USERNAME, constants.PASSWORD)
        mail.select("inbox", readonly=True) # NOTE that this will keep the email unread. need to set this to False later
        success_message = "IMAP login successful."
        print(success_message)

    except Exception as e:
        error_message = f"IMAP login failed: {e}"
        print(error_message)
        strutils.write_log(error_message)
        exit() #stop the rest of the script if IMAP fails.


    # Search for unread emails
    status, messages = mail.search(None, f'(UNSEEN FROM "{constants.AGENCY_ADDRESS}")')
    message_ids = messages[0].split()

    for mid in message_ids:
        # get raw mail and convert to EmailMessage class
        _, mdata = mail.fetch(mid, "(RFC822)")
        raw = mdata[0][1]
        emessage = email.message_from_bytes(raw)

        # pahse
        # subject
        subject = decode_header(emessage["Subject"])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()

        # body
        body = ""
        if emessage.is_multipart(): #unlikely but just in case
            for part in emessage.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
        else:
            body = emessage.get_payload(decode=True).decode()

        # check for property name
        match = re.search(constants.REGSTR, subject) # currently only checking on subject as in my case the 

        if match:
            location = match.group(1)
            match_message = f"Location found in email: {location}"
            print(match_message)
            strutils.write_log(match_message)
            return location
        else:
            no_match_message = "No location found in email"
            print(no_match_message)
            strutils.write_log(no_match_message)
            return None
        

    mail.close()
    mail.logout()


if __name__ == "__main__":
    print("please run stayontop.py")