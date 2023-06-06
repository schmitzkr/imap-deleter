#!/bin/python

import imaplib
import config
import datetime
import logging
import sys

current_date = datetime.date.today()
d = 30
datedays = (current_date-datetime.timedelta(days=d)).strftime("%d-%b-%Y")

def match_and_return_variables(input_value):
    for tpl in config.creds:
        if tpl[0] == input_value:
            first_element, second_element = tpl
            return first_element, second_element
#test
    return None

if len(sys.argv) > 1:
    # Get the command-line parameter
    user_input = sys.argv[1]

matching_tuple = match_and_return_variables(user_input)

box = imaplib.IMAP4_SSL(config.host, 993)
box.login(matching_tuple[0], matching_tuple[1])
box.select("INBOX.delete-after-30-days")
typ, data = box.search(None, '(BEFORE {0})'.format(datedays))

count = len(data[0].split())

logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
##logging.basicConfig(level=logging.DEBUG, filename="/home/grigory/logfile", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
logging.info('connected to %a', matching_tuple[0])
logging.info('%d messages deleted', count)

for num in data[0].split():
    box.store(num, '+FLAGS', '\\Deleted')

box.expunge()
box.close()
box.logout()