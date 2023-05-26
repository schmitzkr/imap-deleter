#delete messages from a folder over 30 days old
# https://stackoverflow.com/questions/3180891/imap-how-to-delete-messages

import imaplib
import config
box = imaplib.IMAP4_SSL('mail.mael.is', 993)
box.login(config.username, config.password)
box.select("INBOX.delete-after-30-days")
typ, data = box.search(None, 'ALL')
for num in data[0].split():
    box.store(num, '+FLAGS', '\\Deleted')

box.close()
box.logout()