class Course:
    def __init__(self, school, name_number, description):
        self.school = school
        self.name_number = name_number
        self.description = description

    def __repr__(self):
        return f'{self.school}: {self.name_number}'
