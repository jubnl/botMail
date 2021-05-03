from imap_tools.message import MailMessage
from zipfile import ZipFile
from pathlib import Path


ATT_FOLDER = "./attachments/"

def send_discord(email: MailMessage=None):
    expeditor = email.from_
    subject = email.subject if email.subject else None
    content = email.text if email.text != "\r\n" else None
    attachments = [
        (att.filename, att.payload) 
        for att in email.attachments
        ] if email.attachments else None
    
    if not subject and not content and not attachments:
        return
    
    if attachments:
        for att in attachments:
            with open(ATT_FOLDER+att[0], 'wb') as f:
                f.write(att[1])
        files = [x for x in Path(ATT_FOLDER).iterdir() if x.is_file()]
        with ZipFile(ATT_FOLDER+"attachments.zip", 'w') as zip:
            for f in files:
                zip.write(f)