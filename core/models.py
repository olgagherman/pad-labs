'''
In this module are defined models for core entities.
'''

class Student(object):
    def __init__(self, name, group, mark):
        self.name = name
        self.academic_group = group
        self.average_mark = mark
