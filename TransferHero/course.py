class Course:
    def __init__(self, school, course_code, description):
        self.school = school
        self.course_code = course_code
        self.description = description

    def __str__(self):
        return f'{self.school}: {self.course_code}'

    def __lt__(self, other):
        return self.school[0] < other.school[0]

    def to_list(self):
        return [self.school, self.course_code, self.description]
