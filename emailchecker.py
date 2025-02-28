import imaplib
import email
import constants
from email.header import decode_header

# Gmail IMAP settings

# Connect to imap server
try:
    mail = imaplib.IMAP4_SSL(constants.IMAP_SERVER)
    mail.login(constants.USERNAME, constants.PASSWORD)
    mail.select("inbox")
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
    if "Herenstraat" in body: # this needs to be a regex check instead
        property_name = "Herenstraat"
        print(f"found {property_name}")

mail.close()
mail.logout()


