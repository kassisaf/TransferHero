import csv
import os
import time
from re import match

import fitz  # AKA pymupdf
from TransferHero import AssistOrg
from TransferHero.Course import Course

DOWNLOAD_FOLDER = r'S:\assist'
INPUT_FILENAME = r'comp132.csv'
SCHOOL_NAME = 'CSUMB'
MAJOR_NAME = 'Computer Science'
CATALOG_YEAR = '2020-2021'
TARGET_COURSE = 'CST 238'


if __name__ == '__main__':
    # Open the input csv and save the info we care about to a list of Course objects
    courses = []
    with open(INPUT_FILENAME, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            courses.append(Course(row['Institution'], row['Local Dept. Name & Number'], row['Local Course Title(s)']))

    # Download agreement PDFs for every community college in our list
    # print('Downloading course agreements...')
    # Create the Selenium web driver we'll need for automation
    # driver = AssistOrg.create_driver(download_folder=DOWNLOAD_FOLDER)
    # for course in sorted(courses):
    #     print(f'   {course}', end='')
    #     AssistOrg.get_agreement_pdf(driver, CATALOG_YEAR, SCHOOL_NAME, course.school, MAJOR_NAME)
    #     time.sleep(5)  # Avoid hammering
    # driver.close()

    # TODO parse out our PDFs to verify which classes satisfy the class we need
    for filename in os.listdir(DOWNLOAD_FOLDER):
        absolute_filename = os.path.join(DOWNLOAD_FOLDER, filename)
        file_ext = os.path.splitext(filename)

        # Skip non-PDFs and remove duplicates
        if file_ext[1].lower() != '.pdf':
            continue
        elif match(r'\(\d{1,2}\)', file_ext[0][-3:]):
            os.remove(absolute_filename)
            continue

        # Open the PDF, look for the line containing our target course and find equivalencies around it
        with fitz.open(absolute_filename) as pdf:
            text = []
            for page in pdf:
                # Looks ugly but this gets rid of all the nasty zero-width spaces that prevent us from searching easily
                text += page.get_text().encode('ascii', 'ignore').decode('unicode_escape').split('\n')

            # Get school name before we look at courses. Looks like "From: {School Name}"
            print(f'Parsing {filename}...', end='')
            for line in text:
                if "From: " in line:
                    school = line.split(':')[1].strip()
                    print(f'({school})')
                    break

            # See if our target course is listed
            #  There may be multiple equivalent courses separated by '--- And ---' or '--- Or ---' but they may not
            #  appear in natural reading order.  TODO: find a smarter way to extract all equivalent courses
            #  https://pymupdf.readthedocs.io/en/latest/faq.html#how-to-extract-text-in-natural-reading-order
            for line in text:
                if TARGET_COURSE in line:
                    print(f'   Found {TARGET_COURSE}')
                    break

    # TODO Create a new spreadsheet of courses that have a transfer agreement

    # TODO Of the remaining schools, try to find links to their class schedules online
