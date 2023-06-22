import imaplib
import datetime
import logging
import logging.handlers
import smtplib
from email.mime.text import MIMEText

import config

current_date = datetime.date.today()
d = 30
datedays = (current_date - datetime.timedelta(days=d)).strftime("%d-%b-%Y")

# Configure the root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create a SMTP handler
smtp_handler = logging.handlers.SMTPHandler(
    mailhost=(config.host, config.port),
    fromaddr=config.from_address,
    toaddrs=[config.to_address],
    credentials=config.send_creds,
    subject='[delete after 30 days] logging Output',
    secure=()
)
smtp_handler.setLevel(logging.DEBUG)

# Add the SMTP handler to the root logger
logger.addHandler(smtp_handler)

def process_account(account):
    box = imaplib.IMAP4_SSL(config.host, 993)
    box.login(account[0], account[1])
    box.select("INBOX.delete-after-30-days")
    typ, data = box.search(None, '(BEFORE {0})'.format(datedays))

    count = len(data[0].split())

    # Log your messages
    logger.info('connected to %s, %d messages deleted', account[0], count)

    for num in data[0].split():
        box.store(num, '+FLAGS', '\\Deleted')

    box.expunge()
    box.close()
    box.logout()

if __name__ == "__main__":
    # Connect to each account and process the email data
    for account in config.creds:
        process_account(account)
