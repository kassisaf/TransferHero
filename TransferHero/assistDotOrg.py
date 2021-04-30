import os
import random
from time import sleep
import fitz
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
# from selenium.common.exceptions import ElementNotInteractableException

random.seed()
MAX_RETRIES = 11


# Enters text at a humanly rate
def slow_type(element, text, delay_min=0.02, delay_max=0.14):
    for character in text:
        element.send_keys(character)
        sleep(random.uniform(delay_min, delay_max))


# Clears out a text field by simulating select all + delete
def clear_field(element):
    element.send_keys(Keys.CONTROL + 'a')
    element.send_keys(Keys.DELETE)


# Creates the Selenium web driver needed to automate assist.org
def create_driver(download_folder, headless=False):
    opts = Options()
    # opts.headless = True

    profile = FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', download_folder)
    profile.set_preference('browser.download.useDownloadDir', True)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/pdf')
    profile.set_preference('pdfjs.disabled', True)

    driver = Firefox(options=opts, firefox_profile=profile)
    driver.get('https://assist.org')
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

    # Fill out "Academic Year", "Institution", and "Other Institution" fields
    year.send_keys(years)
    year.send_keys(Keys.RETURN)
    school.send_keys(university)
    school.send_keys(Keys.RETURN)

    # "Other Institution" gets typed slowly because the results update in real time
    clear_field(agreement)  # Doesn't seem necessary but just to be safe
    slow_type(agreement, city_college)  # replace with field from google sheet
    sleep(0.5)
    agreement.send_keys(Keys.RETURN)

    # "Other Institution" dropdown obscures the submit button, so if search fails we can't click it
    #  If click fails, attempt to close the dropdown and wait before retrying
    for i in range(MAX_RETRIES):
        try:
            view_button.click()
        except ElementClickInterceptedException:
            if i == MAX_RETRIES:
                raise Exception('Failed to click "View Agreements" button')
            agreement.send_keys(Keys.RETURN)
            sleep(1)
        else:
            break

    # Find and select the correct major
    major_input = driver.find_element_by_css_selector('.filterAgreements input')
    clear_field(major_input)  # Clear the field before typing in it again
    major_input.send_keys(target_major)
    sleep(0.5)

    majors_list = driver.find_elements_by_css_selector('.disciplines .viewByRowColText')
    major_row = None

    # Need to make sure we always find the specified major in the list of majors else nothing to click on
    for i in range(MAX_RETRIES):
        try:
            for row in majors_list:
                if target_major in row.text:
                    major_row = row
                    break
            major_row.click()
        except AttributeError:
            sleep(1)
        else:
            break

    # If the download button isn't visible, try to click the major button and wait before trying again
    for i in range(MAX_RETRIES):
        try:
            major_row.click()
            sleep(0.5)
            download_button = driver.find_element_by_xpath('//*[@id="view-results"]/div/div[4]/button')
        except NoSuchElementException:
            sleep(1)
        else:
            download_button.click()
            break


# Looks for a school name and our target course inside a PDF file
# Returns the school name, or None if the course was not found
def parse_agreement_pdf(absolute_filename, target_course_code):
    filename = os.path.split(absolute_filename)[1]
    # Open the PDF, look for the line containing our target course and find equivalencies around it
    with fitz.open(absolute_filename) as pdf:
        text = []
        for page in pdf:
            # Looks ugly but this gets rid of all the nasty zero-width spaces that prevent us from searching easily
            text += page.get_text().encode('ascii', 'ignore').decode('unicode_escape').split('\n')

        # Get school name before we look at courses. Looks like "From: {School Name}"
        # print(f'Parsing {filename}', end='')
        for line in text:
            if "From: " in line:
                school = line.split(':')[1].strip()
                # print(f' ({school})')
                break  # Got what we came here for

        # See if our target course is listed
        #  There may be multiple equivalent courses separated by '--- And ---' or '--- Or ---' but they may not
        #  appear in natural reading order.  TODO: find a smarter way to extract all equivalent courses
        #  https://pymupdf.readthedocs.io/en/latest/faq.html#how-to-extract-text-in-natural-reading-order
        for line in text:
            if target_course_code in line:
                return school

    return None
