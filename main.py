import csv
import time
from TransferHero import AssistOrg
from TransferHero.Course import Course

DOWNLOAD_FOLDER = r'S:\assist'
INPUT_FILENAME = r'comp132.csv'
SCHOOL_NAME = 'CSUMB'
MAJOR_NAME = 'Computer Science'
CATALOG_YEAR = '2020-2021'

if __name__ == '__main__':
    # Open the input csv and save the info we care about to a list of Course objects
    courses = []
    with open(INPUT_FILENAME, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            courses.append(Course(row['Institution'], row['Local Dept. Name & Number'], row['Local Course Title(s)']))

    # Download agreement PDFs for every community college in our list
    print('Downloading course agreements...')

    # Create the web driver we'll need for automation
    driver = AssistOrg.create_driver(download_folder=DOWNLOAD_FOLDER)
    for course in sorted(courses):
        print(f'   {course}', end='')
        AssistOrg.get_agreement_pdf(driver, CATALOG_YEAR, SCHOOL_NAME, course.school, MAJOR_NAME)
        time.sleep(5)  # Avoid hammering
    driver.close()

    # TODO parse out our PDFs to verify which classes satisfy the class we need

    # TODO Create a new spreadsheet of courses that have a transfer agreement

    # TODO Of the remaining schools, try to find links to their class schedules online
