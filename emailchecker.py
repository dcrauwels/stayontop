import imaplib
import email
from email.header import decode_header

# Gmail IMAP settings

# Connect to imap server
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(USERNAME, PASSWORD)
mail.select("inbox")

# Search for unread emails
status, messages = mail.search(None, f'(UNSEEN FROM "")')