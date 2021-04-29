import csv
from TransferHero import Assist
from TransferHero.Course import Course

DOWNLOAD_FOLDER = r'S:\assist'
INPUT_FILENAME = r'comp132.csv'
SCHOOL_NAME = 'CSUMB'
MAJOR_NAME = 'Computer Science'

if __name__ == '__main__':
    # Create the web driver we'll need for automation
    # driver = Assist.create_driver(download_folder=DOWNLOAD_FOLDER)

    # Open the input csv and save the info we care about to a list of Course objects
    courses = []
    with open(INPUT_FILENAME, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            courses.append(Course(row['Institution'], row['Local Dept. Name & Number'], row['Local Course Title(s)']))

    # TODO download agreement PDFs for each community college in our list
    for course in courses:
        print(course)

    # TODO parse out our PDFs to verify which classes satisfy the class we need

    # TODO Create a new spreadsheet of courses that have a transfer agreement

    # TODO Of the remaining schools, try to find links to their class schedules online
