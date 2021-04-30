import csv
import os
from re import match
from time import sleep
from TransferHero import AssistOrg
from TransferHero import Google
from TransferHero.Course import Course

HAMMER_DELAY = 3
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
    #     sleep(HAMMER_DELAY)  # Avoid hammering
    # driver.close()

    # Parse out our PDFs to verify which classes satisfy the class we need
    potential_schools = []
    for filename in os.listdir(DOWNLOAD_FOLDER):
        absolute_filename = os.path.join(DOWNLOAD_FOLDER, filename)
        file_ext = os.path.splitext(filename)

        # Delete duplicate PDFs (i.e. from multiple downloads during testing)
        if match(r'\(\d{1,2}\)', file_ext[0][-3:]):
            os.remove(absolute_filename)
            continue

        if file_ext[1].lower() == '.pdf':
            school = AssistOrg.parse_agreement_pdf(absolute_filename, TARGET_COURSE)
            if school:
                # print(f'{school} offers a {TARGET_COURSE} equivalent')
                potential_schools.append(school)

    # TODO Create a new spreadsheet of courses that have a transfer agreement

    # TODO Try to find links to class schedules for schools that offer what we need
    for school in potential_schools:
        Google.find_class_schedule_page(school)


