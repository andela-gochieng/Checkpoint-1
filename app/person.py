class Person(object):

    people = {"staff": {}, "fellow": {}}

    def __init__(self):
        pass

    @staticmethod
    def get_details(ID):
        if ID not in Person.people['staff'] and ID not in Person.people['fellow']:
            return 'ID not found!'
        if ID in Person.people['staff']:
            return ID + ' ' + Person.people['staff'][ID]['Name']
        elif ID in Person.people['fellow']:
            return ID + ' ' + Person.people['fellow'][ID]['Name']


class Fellow(Person):
    def __init__(self, firstname, surname, ID, resident='N'):
        self.firstname = firstname
        self.surname = surname
        self.designation = 'fellow'
        self.ID = ID
        self.resident = resident
        self.people['fellow'][ID] = {}
        self.people['fellow'][ID]['Name'] = firstname + ' ' + surname
        self.people['fellow'][ID]['Resident'] = resident


class Staff(Person):
    def __init__(self, firstname, surname, ID, resident='N'):
        self.firstname = firstname
        self.surname = surname
        self.designation = 'staff'
        self.ID = ID
        self.resident = resident
        self.people['staff'][ID] = {}
        self.people['staff'][ID]['Name'] = firstname + ' ' + surname
        self.people['staff'][ID]['Resident'] = resident

