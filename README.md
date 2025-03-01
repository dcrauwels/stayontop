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

    wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz
    tar -xvzf geckodriver-v0.33.0-linux64.tar.gz
    sudo mv geckodriver /usr/local/bin/

## Setup
### email_checker
A number of constants are used in this script which are personal to my usecase. For obvious reasons, I am not sharing the actual constants, so you have to set it up yourself. An `example_constants.py` file has been provided and the script expects a `constants.py` module. This means you need to rename `example_constants.py` to `constants.py` and fill out values yourself.
Either replace the references to the `constants` module or make one yourself, defining the following constants:
- `USERNAME`: this is your email username. Ex: `username`
- `PASSWORD`: this is your email password. Ex: `password123`. Note that I use Gmail, and if you do so as well, you will need to use an app password (Google it) if you use 2FA.
- `IMAP_SERVER`: this is the IMAP server address. For Gmail, this is `imap.gmail.com`. 
- `SMTP_SERVER`: this is the SMTP server address. For Gmail, this is `smtp.gmail.com`.
- `SMTP_PORT`: this is the port the SMTP server listens on for TLS. For Gmail, this is `587`.
- `AGENCY_ADDRESS`: this is the email address that you are scanning for emails from. Ex: `offers@realagency.com`
- `AGENCY_URL`: this is the url for the website you are going to scrape for the location taken from the email notification. Ex: `www.realagency.com`
- `REGSTR`: this is a regex string to find the location name that you are scraping the website for. Ex: `Now Available: (.+, .+)` for `Now Available: 40th. Str., NYC`
- `SEPARATOR`: this is a single character string (I hope) by which you split the resulting string. Ex `','` for `40th. Str., NYC`. Can be set to `''` if your usecase requires it and it will skip the string split.
- `CSS_

Note that the current version of this script scans the email *subject*. If you want, you can scan the body instead by editing the `match = re.search(constants.REGSTR, subject)` statement near the end of the `email_checker()` function in `emailchecker.py` to `match = re.search(constants.REGSTR, body)`.

### page_scraper
We use `Selenium` to render the page before scraping.