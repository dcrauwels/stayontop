import emailutils
import pageutils
import constants
import strutils

def main() -> None:
    # step 1: parse email for location
    location, subject, message_id, references = emailutils.email_checker()
    if location == "": # means email_checker() returned an empty string, which means we found a relevant email but did not manage to extract a location. Worrying.
        emailutils.send_email(constants.EMAIL, "WARNING: Stayontop cannot find location", f"Stayontop has found an email from {constants.AGENCY_ADDRESS} but no location seems to be present. Please check the email manually ASAP.")
        return None
    elif not location: # means we did not find an email matching the agency email address
        print("- result: no email found")
        return None

    print(f"  Email found for location: {location}.")
    
    # step 2: parse website for property url
    url = pageutils.find_url(location)
    street_name = strutils.split_and_clean(location)[0]
    if not url: # means find_url() returned None, which means we have a location name but could not find it on the main website.
        emailutils.send_email(constants.EMAIL, "WARNING: Stayontop cannot find url", f"Stayontop has found an email from {constants.AGENCY_ADDRESS} describing a property at {location}. However, it seems {street_name} cannot be found at {constants.AGENCY_URL}. Please check the website manually asap.")
        print("- result: email found but no url found")
        return None
    
    print(f"  Url found at: {url}")
    
    # step 3: check if property is >30 square meter
    price, size = pageutils.get_property_details_from_url(street_name, url)
    if price is None: # this means get_property_details_from_url() returned None, so there was an issue parsing the website.
        emailutils.send_email(constants.EMAIL, "WARNING: Stayontop cannot parse website", f"Stayontop has found an email from {constants.AGENCY_ADDRESS} describing a property at {location}. A corresponding url was found at {url}. However, parsing the website at that url did not produce a workable property size or price. Please check the website manually asap.")
        print("- result: email found and url found but no price/size found")
        return None
    if size <= 30:
        emailutils.send_email(constants.EMAIL, "WARNING: Stayontop found a small property", f"Stayontop has found an email from {constants.AGENCY_ADDRESS} describing a property at {location}. A corresponding url was found at {url}. The website describes the property as costing € {price} per month for {size} square meters, which is less than 30. The realtor has not been contacted. You can consider the property yourself if you so wish.")
        print("- result: email fround and url found and price/size found but size too small")
        return None
    
    print(f"  Property seems to be over 30 square meters in size - sending email!")

    # step 4: return email
    name = constants.NAME
    agency_address = constants.AGENCY_ADDRESS
    message = constants.MESSAGE_FIRST_HALF + street_name + constants.MESSAGE_SECOND_HALF + name
    reply_subject = "Re: " + subject
    
    emailutils.send_email(agency_address, reply_subject, message, None, in_reply_to = message_id, references = references) #NOTE that this replies to self right now, not to 
    
    print("- result: email found and url found and reply sent")
    
    return None



if __name__ == "__main__":
    main()