class Person(object):

    people = {"staff":{}, "fellow": {}}

    def __init__(self, designation, firstname, surname, ID, resident):
        self.firstname = firstname
        self.surname = surname
        self.designation = designation
        self.ID = ID
        self.resident = resident
        self.people[designation][ID] = {}
        self.people[designation][ID]['Name'] = firstname + ' ' + surname
        self.people[designation][ID]['Resident'] = resident

    @staticmethod
    def get_details(ID):
        if ID not in Person.people['staff'] and ID not in Person.people['fellow']:
            return 'ID not found!'
        if ID in Person.people['staff']:
            return ID + ' -> ' + Person.people['staff'][ID]['Name']
        elif ID in Person.people['fellow']:
            return ID + ' -> ' + Person.people['fellow'][ID]['Name'] 


class Fellow(Person):
  def __init__(self, firstname,surname, ID, resident = 'N' ):
    super(Fellow, self).__init__('fellow', firstname, surname, ID, resident)


class Staff(Person):
  def __init__(self, firstname, surname, ID, resident = 'N'):
     super(Staff, self).__init__('staff', firstname, surname, ID, resident)

