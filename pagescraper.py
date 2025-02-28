import constants
import strutils
import time
import emailchecker

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def page_scraper(location: str):
    if location:
        # get page data
        street_name = strutils.split_and_clean(location)[0]
        
        # set up selenium as firefox
        driver = webdriver.Firefox()
        driver.get(constants.AGENCY_URL)

        # get page and write to output.html        
        '''wait = WebDriverWait(driver, 30)
        wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "div.media:nth-child(3) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1) > h4:nth-child(1)"), 
                "Joubertstraat"
            )
        )'''
        time.sleep(10)
        with open('output.html', 'w') as dumpfile: # get me a copy man
            dumpfile.write(driver.page_source)

        print("mission accomplished")
        driver.quit()
        return

        soup = BeautifulSoup(response.text, "html.parser")

        # Find link based on street name
        property_link = None
        
        # iterate over all <a> tags in html
        for link in soup.find_all("a", href = True):
            print(link)
            if street_name in link.text:
                property_link = link["href"]
                break

        if property_link:
            # check if absolute link or relative
            if not property_link.startswith("http"):
                full_url = constants.AGENCY_URL + property_link
            else:
                full_url = property_link

            print(f"Property URL: {full_url}")
        else:
            print(f"Property with name {street_name} not found on page {constants.AGENCY_URL}.")

        driver.close()



if __name__ == "__main__":
    location = emailchecker.email_checker()
    page_scraper(location)