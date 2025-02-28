import requests
import constants
import strutils
import emailchecker
from bs4 import BeautifulSoup

def page_scraper(location: str):
    if location:
        # get page data
        street_name = strutils.split_and_clean(location)[0]
        

        # pretend I'm a real boy
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/'
        }
        response = requests.get(constants.AGENCY_URL, headers=headers)
        with open('output.html', 'w') as dumpfile: # get me a copy man
            dumpfile.write(response.text)

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



if __name__ == "__main__":
    location = emailchecker.email_checker()
    page_scraper(location)