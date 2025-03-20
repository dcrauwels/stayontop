import imaplib
import smtplib
import email
import constants # server address, username, password, agency address etc. are stored here. You have to set this yourself.
import re
import strutils
import os
import pathlib

from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(
        to: str, 
        subject: str, 
        body: str, 
        rewrite: bool = False, 
        attachment_path: str = None, 
        **kwargs
        ) -> None:
    '''Send an email to email address.

    Mandatory arguments:
        to: string, describes the destination email address.
        subject: string, describes the email subject.
        body: string, describes the email body.

    Optional arguments:
        rewrite: bool, optional, describes whether to rewrite the email using OpenAI API as executed with `strutils.rewrite_email()`.
        attachment_path: string, optional, describes the path to an attachment. Mainly I use this to email myself the logs nightly and then delete them from disk.
        in_reply_to: string, Message-ID of the email being replied to. emailutils.email_checker() returns this.
        references: string, References header of the email being replied to. emailutils.email_checker() returns this.
        original_message: string, body content of original email.
        original_sender: string, email address of sender of original email.
        original_date: string, date of the original email.
        
    Returns:
        None.'''

    # construct email
    msg = MIMEMultipart()
    msg["subject"] = subject
    msg["From"] = constants.USERNAME
    msg["To"] = to
    complete_message = body
    
    # kwargs
    if "in_reply_to" in kwargs:
        in_reply_to = kwargs["in_reply_to"]
        msg["In-Reply-To"] = in_reply_to
        if "references" in kwargs:
            references = kwargs["references"]
            msg["References"] = f"{references} {in_reply_to}"
        else:
            msg["References"] = in_reply_to

        quoted_original = "\n".join([f"> {line}" for line in kwargs["original_message"].split("\n")])
        complete_message = f"""{body}

On {kwargs["original_date"]}, {kwargs["original_sender"]} wrote:
{quoted_original}
"""

        
    msg.attach(MIMEText(complete_message, "plain"))

    # rewrite?
    if rewrite:
        body = strutils.rewrite_email(body)

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
    
    # send email
    with smtplib.SMTP(constants.SMTP_SERVER, constants.SMTP_PORT) as server:
        server.starttls()
        server.login(constants.USERNAME, constants.PASSWORD)
        server.send_message(msg)
    return None

def email_checker():
    '''Checks email for new messages matching a specific pattern from a predefined sender. Currently only checks email subjects. Works with gmail. Heavily reliant on constants.py file.

    Args:
        none

    Returns:
        location: a string naming the street name of the property referred to in the email.
        subject: the email subject.
        message-id: the email message-ID. Useful for the send_email() function, in particular the in_reply_to keyword argument.
        references: the email references. Useful for the send_email() function, in particular the references keyword argument.
        original_message: the body of the original email. Useful for the send_email() function, in particular the original_message kwarg.
        original_sender: the sender of the original email. Useful for the send_email() function, in particular the original_sender kwarg.
        original_date: the date of the matching email, if any. Useful for the send_email() function, in particular the original_date kwarg.'''
    # init
    location = None
    subject = None
    message_id = None
    references = None
    body = None
    sender = None
    date = None


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
        return location, subject, message_id, references, body, sender, date #stop the rest of the script if IMAP fails.

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

        # sender & date
        sender = emessage.get('From')
        date = emessage.get('Date')

        # body
        body = ""
        if emessage.is_multipart(): 
            for part in emessage.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
        else:
            body = emessage.get_payload(decode=True).decode()

        #message-id and references
        message_id = emessage.get("message-id")
        references = emessage.get("references")

        # check for property name
        match = re.search(constants.REGSTR, subject) # currently only checking on subject as in my case the property name is in the email subject

        if match:
            # this means we have an email from the correct sender and with a matching subject. Great! Parse out the location and return it.
            mail.store(mid, '+FLAGS', '\\Seen') # mark the matched email as read
            location = match.group(1)
            
            # get out
            mail.close()
            mail.logout()
            return location, subject, message_id, references, body, sender, date
        else:
            # this means we have an email from the correct sender but without a matching subject. we do two things: log this event and send a warning email to self
            no_match_message = "No location found in email"
            print(no_match_message)
            strutils.write_log(True, True, False, None, False, None, False)
            mail.store(mid, '+FLAGS', '\\Seen') # mark the unmatched email as read if we know a warning mail has been sent
            
            # get out
            mail.close()
            mail.logout()
            return "", subject, message_id, references, body, sender, date

        
    
    mail.close()
    mail.logout()

    strutils.write_log(True, False, False, None, False, None, False)

    return location, subject, message_id, references

def main():
    '''Send an email with the largest log file. Recommend putting this in a nightly cron job at 1 AM.
    Keep in mind that logfiles are separated automatically by date so if you send it before midnight you will have a spare file containing that day's activity from 
    the logging point until midnight which a single daily cron job will not solve.'''
    # init
    largest_path = None
    largest_size = 0

    # get logs folder
    script_dir = os.path.dirname(os.path.abspath(__file__)) # logs folder is relative to script location but not to where you're calling python3 if through cron
    logs_dir = os.path.join(script_dir, "logs")

    #simply iterate over files to identify largest file in directory. very straightforward
    for filename in os.listdir(logs_dir):
        filepath = os.path.join(logs_dir, filename)
        if os.path.isfile(filepath):
            file_size = os.path.getsize(filepath)
            if file_size > largest_size:
                largest_size = file_size
                largest_path = filepath

    # send email for largest one
    send_email(constants.EMAIL, f"Stayontop logs", "", False, largest_path)
    if largest_path:
        pathlib.Path.unlink(largest_path)
    return


if __name__ == "__main__":
    main()