#delete messages from a folder over 30 days old
# https://stackoverflow.com/questions/3180891/imap-how-to-delete-messages

#!/bin/python

import imaplib
import config
import datetime
import logging

current_date = datetime.date.today()
d = 30
datedays = (current_date-datetime.timedelta(days=d)).strftime("%d-%b-%Y")

box = imaplib.IMAP4_SSL(config.host, 993)
box.login(config.username, config.password)
box.select("INBOX.delete-after-30-days")
typ, data = box.search(None, '(BEFORE {0})'.format(datedays))

count = len(data[0].split())

logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
logging.info('%d messages deleted', count)

for num in data[0].split():
    box.store(num, '+FLAGS', '\\Deleted')

box.close()
box.logout()