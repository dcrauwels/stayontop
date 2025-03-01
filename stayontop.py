import emailutils
import pagescraper

def main() -> None:
    location = emailutils.email_checker()
    if location:
        url = pagescraper.find_url(location)
    else:
        pass

    return



if __name__ == "__main__":
    main()