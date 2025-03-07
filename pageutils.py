import constants
import strutils
import re

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


def get_property_details_from_url(location, url):
    '''Returns the monthly rent in euros and property size in square meters. Both are returned as int values.'''
    # setup selenium
    driver = webdriver.Firefox()
    driver.get(url)

    price, size = str(None), str(None)

    # scrape  
    try:
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "span.property-street"), location
            )
        )

        # dump to html for debugging
        with open("generated/url_selenium.html", 'w') as f:
            f.write(driver.page_source)

        # property price
        price = driver.find_element(By.CLASS_NAME, "property-price").text
        
        # property size
        # 1. iterate over li elements to find the one with the Oppervlakte span
        li_elements = driver.find_elements(By.CSS_SELECTOR, "ul.information-block li")
                
        for li in li_elements:

            # 2. iterate over spans per li element
            spans = li.find_elements(By.TAG_NAME, "span")
                        
            for i, span in enumerate(spans):
               
               # 3. check for Oppervlakte
               if "Oppervlakte" in span.text or "Oppervlakte" in span.get_attribute('innerHTML'):
                        
                    # 4. Try to get the value span
                    if i+1 < len(spans):
                        value_span = spans[i+1]
                        size = value_span.get_attribute('innerHTML')
                        
                    # If no next span in this list, look for a sibling span
                    elif i == 0 and len(spans) == 1:
                        try:
                            # Try to find the value span using XPath sibling
                            parent_div = span.find_element(By.XPATH, "./..")
                            parent_li = parent_div.find_element(By.XPATH, "./..")
                            value_span = parent_li.find_element(By.CSS_SELECTOR, "span:not(div span)")
                            print(f"    Value: '{value_span.text}'")
                            print(f"    Value HTML: '{value_span.get_attribute('innerHTML')}'")
                        except Exception as e:
                            print(f"    Error finding sibling: {e}")

               
    except TimeoutException:
        print(f"Timed out waiting for element with text '{location}' to appear.")
        strutils.write_log(True,True,True,location,True,url,False)

    finally:
        driver.quit()

        # log an error if needed
        if not price: # means we didnt retrieve a value
            strutils.write_log(True, True, True, location, True, url, False)

        # parse the scraped content a bit so we get some cleaner values
        price_match = re.search("(€ *)(\\d+)", price)
        if price_match:
            price = int(price_match.group(2))

        size_match = re.search("(\\d+)(m<sup>)", size)
        if size_match:
            size = int(size_match.group(1))
        
        return price, size


    

def send_form(location, url) -> str:
    '''Uses the property `url` gleaned from `pageutils.find_url()` to fill out the webform on said url.'''

    # setup selenium
    driver = webdriver.Firefox()
    driver.get(url)

    # get page  
    is_text_found = WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "span.property-street"), location
        )
    )

    # if page didnt load properly
    if not is_text_found:
        strutils.write_log(True,True,True,location,True,url,False)
        driver.quit()
        return None

    # set up form response
    name = constants.NAME
    email = constants.EMAIL
    phone = constants.PHONE
    message = constants.MESSAGE_FIRST_HALF + location + constants.MESSAGE_SECOND_HALF + name

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
        driver.quit()
        return None


if __name__ == "__main__":
    print("please run stayontop.py")
    