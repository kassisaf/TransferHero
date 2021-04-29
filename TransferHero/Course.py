class Course:
    def __init__(self, school, course_code, description, has_agreement=False):
        self.school = school
        self.name_number = course_code
        self.description = description
        self.has_agreement = has_agreement

    def __str__(self):
        return f'{self.school}: {self.name_number}'

    def __lt__(self, other):
        return self.school[0] < other.school[0]
