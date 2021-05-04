# Email replicating on discord server via webhook

First of all, thank you [Thomas Wieland](https://github.com/thomaswieland) for your [gist](https://gist.github.com/thomaswieland/3cac92843896040b11c4635f7bf61cfb)!

## Only works on Linux (debian like distrib) !

1. Clone this repo
2. Rename [.env.sample](.env.sample) to `.env`
3. Complete your .env file
4. Put the email folder in your website (require PHP on your web server) according to your redirect URI inside the .env file
5. In your command prompt, run `pip3 install -r requirements.txt`
6. In your command prompt, run `sudo apt install python3-imaplib2`
7. In the same dir as [main.py](main.py), create an `attachments` directory
8. Then you can run [mail.py](main.py)

You can simply use [pm2](https://pm2.keymetrics.io/) (`pm2 start main.py --interpreter python3 --name mailBot`).

To install [pm2](https://pm2.keymetrics.io/) you can use [npm](https://www.npmjs.com/) : `npm install pm2 -g`

To install [npm](https://www.npmjs.com/) use this command : `sudo apt install nodejs npm`