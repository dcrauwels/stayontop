import constants
import strutils

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def find_url(location: str) -> str:
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
        strutils.write_log(True, True, location, False, None, False)
        driver.quit()
        return None 


def send_form(url) -> None:


    return


if __name__ == "__main__":
    print("please run stayontop.py")