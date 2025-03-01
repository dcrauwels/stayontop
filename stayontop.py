import emailutils
import pageutils
import constants
import strutils

def main() -> None:
    # step 1: parse email for location
    location = emailutils.email_checker()
    if not location:
        emailutils.send_email("WARNING: Stayontop cannot find location", f"Stayontop has found an email from {constants.AGENCY_ADDRESS} but no location seems to be present. Please check the email manually ASAP.")    
    
    # step 2: parse website for property url
    url = pageutils.find_url(location)
    if not url:
        street_name = strutils.split_and_clean(location)[0]
        emailutils.send_email("WARNING: Stayontop cannot find url", f"Stayontop has found an email from {constants.AGENCY_ADDRESS} describing a property at {location}. However, it seems {street_name} cannot be found at {constants.AGENCY_URL}. Please check the website manually asap.")

    # step 3: fill out form on property url
    form = pageutils.send_form(url)
    if not form:
        emailutils.send_email("WARNING: Stayontop cannot fill out form",f"Stayontop has found a property url at {url} but cannot fill out the form therein. Please check the url manually ASAP.")
    
    return None



if __name__ == "__main__":
    main()