import emailutils
import pageutils
import constants
import strutils

def main() -> None:
    # step 1: parse email for location
    location = emailutils.email_checker()
    if location == "": # means email_checker() returned an empty string, which means we found a relevant email but did not manage to extract a location. Worrying.
        emailutils.send_email(constants.EMAIL, "WARNING: Stayontop cannot find location", f"Stayontop has found an email from {constants.AGENCY_ADDRESS} but no location seems to be present. Please check the email manually ASAP.")
        return None
    elif not location: # means we did not find an email matching the agency email address
        print("- result: no email found")
        return None

    
    # step 2: parse website for property url
    url = pageutils.find_url(location)
    if not url: # means find_url() returned None, which means we have a location name but could not find it on the main website.
        street_name = strutils.split_and_clean(location)[0]
        emailutils.send_email(constants.EMAIL, "WARNING: Stayontop cannot find url", f"Stayontop has found an email from {constants.AGENCY_ADDRESS} describing a property at {location}. However, it seems {street_name} cannot be found at {constants.AGENCY_URL}. Please check the website manually asap.")
        print("- result: email found but no url found")
        return None
    
    # step 3: check if property is >30 square meter
    price, size = pageutils.get_property_details_from_url(location, url)
    if not price: # this means get_property_details_from_url() returned None, so there was an issue parsing the website.
        emailutils.send_email(constants.EMAIL, "WARNING: Stayontop cannot parse website", f"Stayontop has found an email from {constants.AGENCY_ADDRESS} describing a property at {location}. A corresponding url was found at {url}. However, parsing the website at that url did not produce a workable property size or price. Please check the website manually asap.")
        print("- result: email found and url found but no price/size found")
        return None



    # step 3: fill out form on property url
    form = pageutils.send_form(location, url)
    if not form:
        emailutils.send_email(constants.EMAIL, "WARNING: Stayontop cannot fill out form",f"Stayontop has found a property url at {url} but cannot fill out the form therein. Please check the url manually ASAP.")
        print("- result: email found and url found but no form sent")
        return None
    
    print("- result: email found and url found and form sent")
    
    return None



if __name__ == "__main__":
    main()