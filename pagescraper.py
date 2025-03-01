import constants
import strutils
import emailchecker

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_url(location: str) -> str:
    if location:
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
        element = driver.find_element(By.XPATH, f"//h4[contains(text(), '{street_name}')]/parent::a")
        url = element.get_attribute("href")
        print(type(url))
        
        driver.quit()
        return url


def send_form(url) -> None:


    return


if __name__ == "__main__":
    location = emailchecker.email_checker()
    find_url(location)