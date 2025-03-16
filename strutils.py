import constants
import os
import google.generativeai as genai
from datetime import datetime

# header row for csv logfile
CSV_HEADER = "Timestamp,Login_succeeded,Email_found,Location_found,Location,URL_found,URL,Form_sent\n"


def split_and_clean(location: str) -> list: 
    '''splits string "location" by constants.SEPARATOR, strips leading / trailing whitespace'''
    if constants.SEPARATOR == '': # if your usecase does not have a relevant separator
        return [location]
    locations = location.split(',') 
    cleaned_locations = list(map(lambda x: x.strip(), locations))
    return cleaned_locations # should be of the format [street, city]

def write_log(login_succeeded: bool, email_found: bool, location_found: bool, location: str, url_found: bool, url: str, form_sent: bool) -> None:
    '''Takes a six value status report and writes it to a logfile in the current directory. Logfile is named by date at YYYY-MM-DD, log entry is timed at HH:MM:SS.
    
    - `login_succeeded`: boolean, describes if email login via IMAP succeeded or not.
    - `email_found`: boolean, describes if an email matching the desired pattern is found unread in the inbox.
    - `location_found`: boolean, describes if a usable location was able to be parsed from the email.
    - `location`: string, describes the actual location of the property.
    - `url_found`: boolean, describes if a url was found matching the location name on the agency's website.
    - `url`: string, describes the url of the property on the agency's website.
    - `form_sent`: boolean, describes if a webform on the relevant url was found and sent.'''

    # get current date, time
    now = datetime.now()
    current_date = now.date()
    current_time = now.strftime("%H:%M:%S")

    # setup log
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(script_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    log_name = os.path.join(logs_dir, f"{current_date}-stayontop-log.csv")
    log_exists = os.path.exists(log_name)

    with open(log_name, 'a') as log:
        if not log_exists: # this means it's the first log of the day
            log.write(CSV_HEADER) 
        log_value = ','.join(str(arg) for arg in [current_time, login_succeeded, email_found, location_found, location, url_found, url, form_sent]) # convert to strings
        log.write(f"{log_value}\n")
        print(f"written to log on {current_date} at {current_time}")

    return None

def rewrite_email(original_email: str):
    '''Rewrites an email using Google Gemini API. 
    
    Args:
    
        original_email (str): The default email to be rewritten.
        
    Returns:
    
        str: Rewritten email'''
    
    try:
        # config for apikey
        genai.configure(api_key = constants.LLM_API_KEY)

        # get datetime
        current_date = datetime.now().strftime("%B %d, %Y")

        # create propmpt
        prompt = f"""
        Today is {current_date}.

        Please rewrite the following email in the same language it was written in. The goal when rewriting is to make it sound slightly different while keeping the same meaning, tone and important information.
        You can make changes to sentence structure and especially word choice to make it unique. However, names must be preserved no matter what.

        Original email:
        {original_email}

        Rewritten email:
        """

        # initialize model
        model = genai.GenerativeModel('models/gemini-2.0-flash-lite')

        # call gemin API
        response = model.generate_content(
            contents=[
                {"role": "user", "parts": [{"text": prompt}]}
            ],
            generation_config={
                "temperature": 0.8,
                "max_output_tokens": 1000        
            }
        )

        return response.text.strip()

    except Exception as e:
        print(f"Error: {e}")
        return f"Error rewriting email: {str(e)}"

if __name__ == "__main__":
    print("please run stayontop.py")