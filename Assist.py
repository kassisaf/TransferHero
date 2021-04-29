import time
import random
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException

random.seed()


# Enters text at a humanly rate
def slow_type(element, text, delay_min=0.02, delay_max=0.14):
    for character in text:
        element.send_keys(character)
        time.sleep(random.uniform(delay_min, delay_max))


# Creates the Selenium web driver needed to automate assist.org
def create_driver(download_folder, headless=False):
    opts = Options()
    # opts.headless = True

    profile = FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', download_folder)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/pdf')

    driver = Firefox(options=opts, firefox_profile=profile)
    driver.get('http://assist.org')
    return driver


# Uses web automation to download the PDF for an articulation agreement between two schools
def get_agreement_pdf(driver, years, university, city_college, target_major):
    # Find the elements we need for the first form
    try:
        year = driver.find_element_by_id('academicYear')
        school = driver.find_element_by_id('fromInstitution')
        agreement = driver.find_element_by_id('agreement')
        view_button = driver.find_element_by_xpath(r'//*[@id="transfer-info-search"]/div[4]/div/button')
    except NoSuchElementException as e:
        print(f'ERROR: One or more elements not found')
        raise e
    else:
        print('Found necessary fields for initial search')

    # Fill out "Academic Year", "Institution", and "Other Institution" fields
    year.send_keys(years)
    year.send_keys(Keys.RETURN)
    school.send_keys(university)
    school.send_keys(Keys.RETURN)

    # "Other Institution" gets typed slowly because the results update in real time
    slow_type(agreement, city_college)  # replace with field from google sheet
    time.sleep(0.5)
    agreement.send_keys(Keys.RETURN)

    # "Other Institution" dropdown obscures the submit button, so if search fails we can't click it
    #  If click fails, attempt to close the dropdown and wait before retrying
    max_retries = 11
    for i in range(max_retries):
        try:
            view_button.click()
        except ElementClickInterceptedException:
            if i == max_retries:
                raise Exception('Failed to click "View Agreements" button')
            agreement.send_keys(Keys.RETURN)
            time.sleep(1)
        else:
            break

    # Find and select the correct major
    major_input = driver.find_element_by_css_selector('.filterAgreements input')
    major_input.send_keys(target_major)
    time.sleep(0.5)

    majors_list = driver.find_elements_by_css_selector('.disciplines .viewByRowColText')
    major_row = None
    for row in majors_list:
        print(row.text)
        if target_major in row.text:
            major_row = row
            break

    major_row.click()
