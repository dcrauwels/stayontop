import constants
import strutils

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def find_url(location: str) -> str:
    '''Scrapes a predefined web page (in the `constants` module under `constants.AGENCY_URL`) for the `location` parsed from email. 
    Returns the `url` of the property at the `location` in question in string format.'''
    # get page data
    street_name = strutils.split_and_clean(location)[0]
    
    # set up selenium as firefox
    driver = webdriver.Firefox()
    driver.get(constants.AGENCY_URL)

    # get page
    wait = WebDriverWait(driver, 30)
    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "a.houses-url[href*='woning']")
        )
    )

    # find  url
    try:
        element = driver.find_element(By.XPATH, f"//h4[contains(text(), '{street_name}')]/parent::a")
        url = element.get_attribute("href")    
        driver.quit()
        return url
    
    except NoSuchElementException: # in case we can load the website but it doesn't have the property we think we're looking for
        print(f"{street_name} not found on {constants.AGENCY_URL}")
        strutils.write_log(True, True, True, location, False, None, False)
        driver.quit()
        return None 


def send_form(location, url) -> str:
    '''Uses the property `url` gleaned from `pageutils.find_url()` to fill out the webform on said url.'''

    # setup selenium
    driver = webdriver.Firefox()
    driver.get(url)

    # get page  
    is_text_found = WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "span.property-street"), "Herenstraat"
        )
    )

    # set up form response
    #name = constants.NAME
    #email = constants.EMAIL
    #phone = constants.PHONE
    #message = constants.MESSAGE_FIRST_HALF + location + constants.MESSAGE_SECOND_HALF + name
    name = "Henk speksnijder"
    email = "speksnaaidr22@gmail.com"
    phone = "06 387249222"
    message = "goedendag, graag wil ik "

    # find and fill out form elements
    name_field = driver.find_element(By.NAME, "name")
    name_field.send_keys(name)

    email_field = driver.find_element(By.NAME, "emailaddress")
    email_field.send_keys(email)

    phone_field = driver.find_element(By.NAME, "telephone")
    phone_field.send_keys(phone)

    message_field = driver.find_element(By.ID, "contactMessage")
    message_field.send_keys(message)

    # submit form
    submit_button = driver.find_element(By.ID, "sendBtn")

    if submit_button.is_displayed():
        #submit_button.click()

        # log and return
        strutils.write_log(True, True, True, location, True, url, True)
        driver.quit()    
        return message
    else:
        # in case things don't work out
        strutils.write_log(True, True, True, location, True, url, False)
        return None


if __name__ == "__main__":
    print("please run stayontop.py")
    