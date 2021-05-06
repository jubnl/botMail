from imaplib2 import IMAP4_SSL
from time import sleep
from datetime import datetime
from pytz import timezone
from pathlib import Path
from os import remove
from sys import exit
# from pprint import pprint
from idler import (
    IMAP_SERVER,
    PASSWORD,
    EMAIL,
    TIMEZONE,
    Idler
)

if __name__ == '__main__':

    try:
        # check in attachments dir is empty, if not : will empty the dir
        print("STARTUP : getting files in ./attachments if any...")
        files = [x for x in Path("./attachments/").iterdir()]
        # pprint(files)
        if files:
            print(f"STARTUP : {len(files)} file(s) found in ./attachments")
            removed = []
            for f in files:
                try:
                    remove(f)
                    removed.append(f)
                except Exception:
                    pass
            if len(removed) == len(files):
                print(f"STARTUP : {len(files)} file(s) removed !")
            else:
                print(f"STARTUP : {len(removed)} file(s) removed !")
                print(f"STARTUP : {len(files)-len(removed)} file(s) remaining...")
                print(f for f in removed)
        else:
            print("STARTUP : No files have been found")
        
        
        print("STARTUP : Trying to start application...")
        
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
            print(f"[{datetime.now(timezone(TIMEZONE)).strftime('%d/%m/%Y %H:%M:%S')}] : App online !")
            sleep(1739) # IMAP4_SSL.Idle_timout - 1s
            raise Exception

    except Exception as e:
        # print(e)
        print("Closing threads and logging out...")
        # close threads
        idler.stop()
        idler.join()

        # close IMAP instance and logout (DON'T FORGET TO LOGOUT)
        M.close()
        M.logout()
        print("Disconnected !")
        # log when the bot disconnect (I use an external logger that catch print())
        print(f"[{datetime.now(timezone(TIMEZONE)).strftime('%d/%m/%Y %H:%M:%S')}] : App offline")
        # handled by pm2, automatically restart main.py when it exits
        exit()
