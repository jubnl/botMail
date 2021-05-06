from imap_tools.message import MailMessage
from zipfile import ZipFile
from pathlib import Path
from sender import sender
from os import remove
# from pprint import pprint

# set constant
ATT_FOLDER = "./attachments/"

def extractor(email: MailMessage=None):
    """
    :param email: MailMessage object
    
    extract infos from the mail object
    """
    print("Extracting datas from email...")
    # extract email infos
    expeditor = email.from_values['full'] if email.from_values else f"<{email.from_}>"
    subject = email.subject if email.subject else None
    content = email.text if email.text != "\r\n" else None
    attachments = [
        (att.filename, att.payload) 
        for att in email.attachments
        ] if email.attachments else None
    sender_att = False
    print("Extract finished !")
    # return if empty email
    if not subject and not content and not attachments:
        return

    # extract and zip attachments if any
    if attachments:
        print("Attachments found, zipping files...")
        sender_att = True
        for att in attachments:
            with open(ATT_FOLDER+att[0], 'wb') as f:
                f.write(att[1])
        files = [x for x in Path(ATT_FOLDER).iterdir() if x.is_file()]
        with ZipFile(ATT_FOLDER+"attachments.zip", 'w') as zip:
            for f in files:
                zip.write(f, str(f).replace("attachments/",""))
        print("Zip file created successfully !")

    # send the mail on discord via the sender
    # pprint((expeditor, subject, content, sender_att))
    sender(expeditor=expeditor, subject=subject, content=content, attachments=sender_att)
    
    # empty attachments dir
    if attachments:
        print("Detecting files in ./attachments ...")
        files = [x for x in Path(ATT_FOLDER).iterdir()]
        for f in files:
            remove(f)
        print("Attachments folder has been emptied !")
