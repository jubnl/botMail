from discord_webhook import DiscordWebhook, DiscordEmbed
from re import compile
from typing import List
from textwrap import wrap
from pprint import pprint
from json import dump

from environs import Env
env = Env()
env.read_env()



MAX_LENGTH_DESCRIPTION =  2048
MAX_LENGTH_TITLE = MAX_LENGTH_AUTHOR = 256
MAX_LENGTH_EMBED = 6000


def sender(expeditor: str,
           subject: str = None,
           content: str = None,
           attachments: bool = False,
           webhook_uri: str = env("WEBHOOK_URI")):
    
    webhook = DiscordWebhook(url=webhook_uri)
    
    
    if attachments:
        with open("attachments/attachments.zip", "rb") as f:
            webhook.add_file(file=f.read(), filename="attachments.zip")

    lexpeditor = len(expeditor)
    lsubject = len(subject)
    lcontent = len(content)

    regex = compile(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+")
    email = env("BASE_URI_REDIRECT_EMAIL")+regex.findall(expeditor)[0]


    if lexpeditor > MAX_LENGTH_AUTHOR:
        expeditor = expeditor[247:]+" [...]"
        lexpeditor = len(expeditor)


    if lsubject > MAX_LENGTH_TITLE:
        subject = subject[247:]+" [...]"
        lsubject = len(subject)


    if lcontent > MAX_LENGTH_DESCRIPTION:

        contents = []
        while len(content) > 0:
            x = wrap(content, MAX_LENGTH_DESCRIPTION, break_long_words=False)
            contents.append(x[0])
            content = content[len(x[0]):]

        for n, i in enumerate(contents):
            embed = DiscordEmbed(title=f"{subject} {n+1}/{len(contents)}", description=i, color='03b2f8')
            embed.set_author(name=expeditor, url=email)
            embed.set_timestamp()
            webhook.add_embed(embed)
            response = webhook.execute()

    else:
        embed = DiscordEmbed(title=subject, description=content, color='03b2f8')
        embed.set_author(name=expeditor, url=email)
        embed.set_timestamp()
        webhook.add_embed(embed)
        response = webhook.execute()
