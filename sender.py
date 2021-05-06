from discord_webhook import DiscordWebhook, DiscordEmbed
from re import compile
from textwrap import wrap
# from pprint import pprint

# set env vars
from environs import Env
env = Env()
env.read_env()


# Define constants
MAX_LENGTH_DESCRIPTION =  2048
MAX_LENGTH_TITLE = MAX_LENGTH_AUTHOR = 256


def sender(expeditor: str,
           subject: str = None,
           content: str = None,
           attachments: bool = False,
           webhook_uri: str = env("WEBHOOK_URI")) -> None:
    """
    :param expeditor: str that contain the expeditor of the mail
    :param subject: (optional) str that contain the subject of the mail
    :param content: (optional) str The body of the mail
    :param attachments: (optional, default False) bool that indicate if there is some attachments
    :param webhook_uri: str that contain a Discord webhook URL
    :return None:
    """
    print("Datas received, trying to send datas to Discord...")
    # instantiate DiscordWebHook
    webhook = DiscordWebhook(url=webhook_uri)
    
    # set attachments if any
    if attachments:
        print("Getting zip file...")
        with open("attachments/attachments.zip", "rb") as f:
            webhook.add_file(file=f.read(), filename="attachments.zip")
        print("Zip file added to webhook !")

    # get length of every field
    lexpeditor = len(expeditor)
    lsubject = len(subject) if subject else 0
    lcontent = len(content) if content else 0
    

    # extract email from expeditor string
    regex = compile(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+")
    email = env("BASE_URI_REDIRECT_EMAIL")+regex.findall(expeditor)[0]

    # if expeditor string is bigger than 256 chars, shorter the expeditor
    if lexpeditor > MAX_LENGTH_AUTHOR:
        expeditor = expeditor[247:]+" [...]"
        lexpeditor = len(expeditor)

    # if subject string is bigger than 256 chars, shorter the subject
    if lsubject > MAX_LENGTH_TITLE:
        subject = subject[247:]+" [...]"
        lsubject = len(subject)

    # check if we need one or more embeds
    if lcontent > MAX_LENGTH_DESCRIPTION:
        print("Multiple embeds needed...")
        # separate content in strings of 2048 chars max
        # contents = List[str]
        contents = []
        while len(content) > 0:
            x = wrap(content, MAX_LENGTH_DESCRIPTION, break_long_words=False)
            contents.append(x[0])
            content = content[len(x[0]):]

        # send embeds
        print("Constructing embeds...")
        for n, i in enumerate(contents):
            # pprint((subject, content, expeditor, email))
            embed = DiscordEmbed(title=f"{subject} {n+1}/{len(contents)}", description=i, color='03b2f8')
            embed.set_author(name=expeditor, url=email)
            embed.set_timestamp()
            webhook.add_embed(embed)
            response = webhook.execute()
        print("Embeds have been sent !")

    # send embed
    else:
        print("Constructing embed...")
        # pprint((subject, content, expeditor, email))
        embed = DiscordEmbed(title=subject, description=content, color='03b2f8')
        embed.set_author(name=expeditor, url=email)
        embed.set_timestamp()
        webhook.add_embed(embed)
        response = webhook.execute()
        print("Embed has been sent !")
