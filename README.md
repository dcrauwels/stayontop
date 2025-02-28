# stayontop
Automates webform fillouts in response to email triggers from a certain Dutch rental agency in Python. Was made to interact with emails sent to a Gmail address. Personal project that I threw on Github, really.

# Requirements
python3
requests 2.32+
beautifulsoup4 4.13+

# Use
## Requirements
Install selenium and beautifulsoup4:
`pip3 install selenium beautifulsoup4`
Install geckodriver:

    wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz
    tar -xvzf geckodriver-v0.33.0-linux64.tar.gz
    sudo mv geckodriver /usr/local/bin/
    
## Setup
### email_checker
Either replace the references to the `constants` module or make one yourself, defining the following constants:
- `USERNAME`: this is your email username. Ex: `username`
- `PASSWORD`: this is your email password. Ex: `password123`
- `IMAP_SERVER`: this is the imap server address. For Gmail, this is `imap.gmail.com`. 
- `AGENCY_ADDRESS`: this is the email address that you are scanning for emails from. Ex: `offers@realagency.com`
- `AGENCY_URL`: this is the url for the website you are going to scrape for the location taken from the email notification. Ex: `www.realagency.com`
- `REGSTR`: this is a regex string to find the location name that you are scraping the website for. Ex: `Now Available: (.+, .+)` for `Now Available: 40th. Str., NYC`
- `SEPARATOR`: this is a single character string (I hope) by which you split the resulting string

Note that the current version of this script scans the email *subject*. If you want, you can scan the body instead by editing the `match = re.search(constants.REGSTR, subject)` statement near the end of the `email_checker()` function in `emailchecker.py`.

### page_scraper
