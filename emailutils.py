import imaplib
import smtplib
import email
import constants # server address, username, password, agency address etc. are stored here. You have to set this yourself.
import re
import strutils
import os
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(to: str, subject: str, body: str, attachment_path: str = None, **kwargs) -> None:
    '''Send an email to email address.

    Mandatory arguments:
        to: string, describes the destination email address.
        subject: string, describes the email subject.
        body: string, describes the email body.

    Optional arguments:
        attachment_path: string, optional, describes the path to an attachment. Mainly I use this to email myself the logs nightly and then delete them from disk.
        in_reply_to: string, Message-ID of the email being replied to'''

    # construct email
    msg = MIMEMultipart()
    msg["subject"] = subject
    msg["From"] = constants.USERNAME
    msg["To"] = to
    
    # kwargs
    if "in_reply_to" in kwargs:
        in_reply_to = kwargs["in_reply_to"]
        msg["In-Reply-To"] = in_reply_to
        if "references" in kwargs:
            references = kwargs["references"]
            msg["References"] = f"{references} {in_reply_to}"
        else:
            msg["References"] = in_reply_to
        
    msg.attach(MIMEText(body, "plain"))

    # in case we get an attachment set it as a MIME part
    if attachment_path and os.path.exists(attachment_path):
        # read in file
        with open(attachment_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        
        # encode attachment in base64
        encoders.encode_base64(part)

        # attachment header
        part.add_header("Content-Disposition", "attachment", filename=os.path.basename(attachment_path))

        msg.attach(part)
        print(f"Attached file at path '{attachment_path}'.")
    elif attachment_path:
        print(f"Attachment file not found at path '{attachment_path}'.")
    

    with smtplib.SMTP(constants.SMTP_SERVER, constants.SMTP_PORT) as server:
        server.starttls()
        server.login(constants.USERNAME, constants.PASSWORD)
        server.send_message(msg)
        print("Email sent.")
    return None

def email_checker():
    '''Checks email for new messages matching a specific pattern from a predefined sender. Currently only checks email subjects. Works with gmail.

    Args:
        none

    Returns:
        location: a string naming the street name of the property referred to in the email.
        subject: the entire email subject.'''
    # init
    location = None
    subject = None


    # Connect to imap server
    try:
        mail = imaplib.IMAP4_SSL(constants.IMAP_SERVER)
        mail.login(constants.USERNAME, constants.PASSWORD)
        mail.select("inbox", readonly=False) 
        success_message = "IMAP login successful."
        print(success_message)

    except Exception as e:
        error_message = f"IMAP login failed: {e}"
        print(error_message)
        strutils.write_log(False, False, False, None, False, None, False)
        return location, subject #stop the rest of the script if IMAP fails.

    # Search for unread emails
    _, messages = mail.search(None, f'(UNSEEN FROM "{constants.AGENCY_ADDRESS}")')
    message_ids = messages[0].split()

    # iterate over unread emails from the correct sender
    for mid in message_ids:
        # get raw mail and convert to EmailMessage class
        _, mdata = mail.fetch(mid, "(BODY.PEEK[])") # Note that this does not set the emails as read. We do this manually when they match the regex search later. This is in case we get multiple separate emails from the agency within a small timespan with offers.
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
        match = re.search(constants.REGSTR, subject) # currently only checking on subject as in my case the property name is in the email subject

        if match:
            # this means we have an email from the correct sender and with a matching subject. Great! Parse out the location and return it.
            mail.store(mid, '+FLAGS', '\\Seen') # mark the matched email as read
            location = match.group(1)
            match_message = f"Location found in email: {location}"
            print(match_message)
            
            # get out
            mail.close()
            mail.logout()
            return location, subject
        else:
            # this means we have an email from the correct sender but without a matching subject. we do two things: log this event and send a warning email to self
            no_match_message = "No location found in email"
            print(no_match_message)
            strutils.write_log(True, True, False, None, False, None, False)
            mail.store(mid, '+FLAGS', '\\Seen') # mark the unmatched email as read if we know a warning mail has been sent
            
            # get out
            mail.close()
            mail.logout()
            return "", subject

        
    
    mail.close()
    mail.logout()

    strutils.write_log(True, False, False, None, False, None, False)

    return None


if __name__ == "__main__":
    print("please run stayontop.py")