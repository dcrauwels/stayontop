import imaplib
import email
import constants
import re
from email.header import decode_header

def checkEmail() -> str:

    # Connect to imap server
    try:
        mail = imaplib.IMAP4_SSL(constants.IMAP_SERVER)
        mail.login(constants.USERNAME, constants.PASSWORD)
        mail.select("inbox", readonly=True) # NOTE that this will keep the email unread. need to set this to False later
        print("IMAP login successful.")

    except Exception as e:
        print(f"IMAP login failed: {e}")
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
        subject = decode_header(emessage["Subject"])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()

        body = ""
        if emessage.is_multipart():
            for part in emessage.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
        else:
            body = emessage.get_payload(decode=True).decode()

        # check for property name
        matchSubject = re.search("Nu Online: (\\w+, \\w+)", subject)

        if matchSubject:
            location = matchSubject.group(1)
            print(f"Location found: {location}")
        else:
            print("No location found")
        

    mail.close()
    mail.logout()


