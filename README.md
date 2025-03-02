# stayontop
Automates webform fillouts in response to email triggers from a certain Dutch rental agency in Python. Was made to interact with emails sent to a Gmail address. Personal project that I threw on Github, really.

# Requirements
- `python3`
- `selenium` 4.29+


# Use
## Requirements
Install `Selenium`:

    pip3 install selenium

Install geckodriver:

    wget https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz
    tar -xvzf geckodriver-v0.36.0-linux64.tar.gz
    sudo mv geckodriver /usr/local/bin/

## Setup
### Constants
A number of constants are used in this script which are personal to my usecase. For obvious reasons, I am not sharing the actual constants, so you have to set it up yourself. An `example_constants.py` file has been provided and the script expects a `constants.py` module. This means you need to rename `example_constants.py` to `constants.py` and fill out values yourself:

- `USERNAME`: this is your email username. Ex: `username`
- `PASSWORD`: this is your email password. Ex: `password123`. Note that I use Gmail, and if you do so as well, you will need to use an app password (Google it) if you use 2FA.
- `IMAP_SERVER`: this is the IMAP server address. For Gmail, this is `imap.gmail.com`. 
- `SMTP_SERVER`: this is the SMTP server address. For Gmail, this is `smtp.gmail.com`.
- `SMTP_PORT`: this is the port the SMTP server listens on for TLS. For Gmail, this is `587`.
- `AGENCY_ADDRESS`: this is the email address that you are scanning for emails from. Ex: `offers@realagency.com`
- `AGENCY_URL`: this is the url for the website you are going to scrape for the location taken from the email notification. Ex: `www.realagency.com`
- `REGSTR`: this is a regex string to find the location name that you are scraping the website for. Ex: `Now Available: (.+, .+)` for `Now Available: 40th. Str., NYC`
- `SEPARATOR`: this is a single character string (I hope) by which you split the resulting string. Ex `','` for `40th. Str., NYC`. Can be set to `''` if your usecase requires it and it will skip the string split.
- `NAME`: this is your own name, to be filled out on the form.
- `EMAIL`: this is your email address, to be filled out on the form.
- `PHONE`: this is your phone number, to be filled out on the form.
- `MESSAGE_FIRST_HALF`: first half of the message to be filled out on the form. Expects to be combined with `MESSAGE_SECOND_HALF` in the following way: `MESSAGE_FIRST_HALF + location_name + MESSAGE_SECOND_HALF + NAME`. Ex: `Good day, I like the property at 40th. Str., and would like to arrange a viewing. Kind regards, John`
- `MESSAGE_SECOND_HALF`: second half of the message to be filled out on the form. See above.

Note that the current version of this script scans the email *subject*. If you want, you can scan the body instead by editing the `match = re.search(constants.REGSTR, subject)` statement near the end of the `email_checker()` function in `emailchecker.py` to `match = re.search(constants.REGSTR, body)`.

### cron
The script checks your email and scrapes the website etc. *once*. We want to execute this very frequently, let's say every five minutes. There's plenty of ways of doing so, but my solution was setting up a cron job on my Raspberry Pi. Something like this will work:

    crontab -e
    */5 * * * * /usr/bin/python3 /home/pi/stayontop.py

Obviously adjust the path to `stayontop.py` as you see fit.