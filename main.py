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
        
        M = IMAP4_SSL(IMAP_SERVER)
        M.login(EMAIL, PASSWORD)
        
        M.select("INBOX")
        
        idler = Idler(M)
        idler.start()

        while True:
            sleep(1739) # IMAP4_SSL.Idle_timout - 1s
            raise Exception

    except Exception as e:
        print(e)
        idler.stop()
        idler.join()
        M.close()
        M.logout()
        
        print(f"[{datetime.now().strftime('%d %m %Y %H:%M:%S')}] : Bot has restarted")
        exit()