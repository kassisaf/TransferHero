import csv
import os
from re import match
from time import sleep
from TransferHero import assistDotOrg
from TransferHero.spreadsheet import Spreadsheet
from TransferHero.search import feeling_ducky
from TransferHero.course import Course


HAMMER_DELAY = 3
# TODO tkinter dialog to prompt for download folder
# DOWNLOAD_FOLDER = r'S:\assist'
DOWNLOAD_FOLDER = r'C:\Users\akassisx\OneDrive - Intel Corporation\Documents\Personal and School\TransferHero'
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

    # Start a new spreadsheet for our output
    sheet_title = f'{TARGET_COURSE} agreements'
    header_row = ['School', 'Class', 'Description', 'Offered', 'Online', 'Synchronous', 'Notes']
    spreadsheet = Spreadsheet(sheet_title, header_row)
    for course in sorted(courses):
        spreadsheet.add_row(course.to_list())
        # Try to find and add a link to the school's class schedule
        # TODO use existing link if we've already looked at this school for another course
        search_terms = f'{course.school} california class schedule search summer 2021'
        schedule_link = feeling_ducky(search_terms)
        spreadsheet.add_hyperlink(spreadsheet.workbook.active.max_row, 1, schedule_link)

    # TODO run PDF downloads asynchronously
    # Download agreement PDFs for every community college in our list
    # print('Downloading course agreements...')
    # # Create the Selenium web driver we'll need for automation
    # driver = assistDotOrg.create_driver(download_folder=DOWNLOAD_FOLDER)
    # for course in sorted(courses):
    #     print(f'   {course}')
    #     assistDotOrg.get_agreement_pdf(driver, CATALOG_YEAR, SCHOOL_NAME, course.school, MAJOR_NAME)
    #     sleep(HAMMER_DELAY)  # Avoid hammering assist.org
    # driver.close()

    # # Parse out our PDFs to verify which classes satisfy the class we need
    # for filename in os.listdir(DOWNLOAD_FOLDER):
    #     absolute_filename = os.path.join(DOWNLOAD_FOLDER, filename)
    #     file_ext = os.path.splitext(filename)
    #
    #     # Delete duplicate PDFs (i.e. identical catalogs from the same school)
    #     if match(r'\(\d{1,2}\)', file_ext[0][-3:]):
    #         os.remove(absolute_filename)
    #         continue
    #
    #     # Parse the PDF and look for our target course
    #     if file_ext[1].lower() == '.pdf':
    #         school = assistDotOrg.parse_agreement_pdf(absolute_filename, TARGET_COURSE)
    #         if school:  # Target course was found in this school's agreement so the name was returned
    #             # Since we can't accurately parse the course name from the PDF, try to look it up using the list we
    #             #  created from our csv file
    #             this_course = Course(school, 'Unknown', 'Unknown')
    #             for course in courses:
    #                 if school == course.school:
    #                     this_course = course
    #
    #             # Add the class to the spreadsheet
    #             new_row = [this_course.school, this_course.course_code, this_course.description]
    #             spreadsheet.add_row(new_row)
    #
    #             # Try to find and add a link to the school's class schedule
    #             schedule_link = find_class_schedule_link(school)
    #             spreadsheet.add_hyperlink(spreadsheet.workbook.active.max_row, 1, schedule_link)

    # Save the spreadsheet
    output_filename = os.path.join(DOWNLOAD_FOLDER, f'{SCHOOL_NAME} {TARGET_COURSE} agreements.xlsx')
    spreadsheet.save(output_filename)
