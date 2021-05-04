from imaplib2 import IMAP4_SSL
from time import sleep
from datetime import datetime
from sys import exit
from idler import (
    IMAP_SERVER,
    PASSWORD,
    EMAIL,
    Idler
)

if __name__ == '__main__':

    try:
        # Create IMAP_SSL instance
        M = IMAP4_SSL(IMAP_SERVER)
        M.login(EMAIL, PASSWORD)
        
        # needed to get rid of the Auth state
        M.select("INBOX")
        
        # start Idler
        idler = Idler(M)
        idler.start()

        # every 28 min and 59 seconds, reboot to prevent the bot to get out of his idle state
        while True:
            print(f"[{datetime.now().strftime('%d %m %Y %H:%M:%S')}] : Bot online")
            sleep(1739) # IMAP4_SSL.Idle_timout - 1s
            raise Exception

    except Exception as e:
        print(e)
        
        # close threads
        idler.stop()
        idler.join()
        
        # close IMAP instance and logout (DON'T FORGET TO LOGOUT)
        M.close()
        M.logout()

        # log when the bot disconnect (I use an external logger that catch print())
        print(f"[{datetime.now().strftime('%d %m %Y %H:%M:%S')}] : Bot offline")
        # handled by pm2, automatically restart main.py when it exits
        exit()