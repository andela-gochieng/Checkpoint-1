import os
import sqlite3 as db
import colorama
from termcolor import *
from random import choice
from room import Room, Office, Livingspace
from person import Person, Staff, Fellow


def yellow(string):
    return colored(string, 'yellow')


def cyan(string):
    return colored(string, 'cyan')


def green(string):
    return colored(string, 'green')


def blue(string):
    return colored(string, 'blue')


def red(string):
    return colored(string, 'red')


class Amity(object):

    office_max_occupants = 6
    livingspace_occupants = 4
    available_rooms = []
    unallocated_people = []
    offices = 0
    livingspaces = 0

    def __init__(self):
        pass

    def create_room(self, room_names, room_type='office'):
        ''' This method creates either an office or livingspace by
        instantiating the Office and Livingspace classes respectively. It
        receives the desired room name and the room type to create the rooms.
        The room name is a list to allow the creation of several rooms at once.
        '''

        for room_name in room_names:
            if room_name.isalpha() is False:
                return red(room_name + ' is an invalid room name type!')
            if room_name in Room.rooms['office'] or room_name in Room.rooms['livingspace']:
                return red('A room with that name exists. Select another name')
            if room_type == 'office':
                Office(room_name)
                Amity.offices += 1
            elif room_type == 'livingspace':
                Livingspace(room_name)
                Amity.livingspaces += 1
        return (green('There are ' + str(Amity.offices) + ' offices and ' + str(Amity.livingspaces) + ' livingspaces in the system.'))

    def add_person(self, firstname, surname, designation, resident="N"):
        '''This method creates an entity, person, in the system by
        instantiating the Staff and Fellow classes. Person can either be a
        staff or fellow. If fellow, person is given a chance to be given
        accomodation. It receives a firstname and surname. A unique ID is
        generated for each person for easy referencing '''

        if not firstname.isalpha() or not surname.isalpha():
            return red('Invalid name format. Alphabets only')
        if resident != 'N' and resident != 'Y':
            return red('Respond with Y or N for residence')
        if designation != 'staff' and designation != 'fellow':
            return red('Enter a valid designation')
        if designation == 'staff' and resident == 'Y':
            return red('Staff cannot be allocated livingspaces.')
        elif designation == 'staff':
            ID = 'ST0' + str(len(Person.people['staff'].keys()) + 1)
            Staff(firstname, surname, ID)
            return (cyan(str(firstname) + ' ' + str(surname) + ' has been created as a staff') + " " + self.allocate_room(ID, 'office'))
        elif designation == 'fellow':
            ID = 'FE0' + str(len(Person.people['fellow'].keys()) + 1)
            Fellow(firstname, surname, ID, resident)
            msg = str(firstname) + ' ' + str(surname) + ' has been added as a fellow'
            msg += " " + self.allocate_room(ID, 'office')
            if resident == 'Y':
                msg += " " + self.allocate_room(ID, 'livingspace')
            return cyan(msg)

    def allocate_room(self, ID, room_type):
        '''Allocate room adds a person to a room once a person has been
        created. It adds both fellows and staff to randomly selected offices in
        the system. It also adds fellows who want accomodation to the available
        livingspaces. It passes the person's ID and room name to the
        allocate_room method in the Room class.  '''

        room_list = Room.rooms[room_type].keys()
        for room in room_list:
            if Room.rooms[room_type][room]['Total_occupants'] < Room.rooms[room_type][room]['Max_occupants']:
                Amity.available_rooms.append(room)
        if len(Amity.available_rooms) == 0:
            Amity.unallocated_people.append(ID)
            Amity.available_rooms = []
            return (red('\nThere are no available %s' % room_type + 's for allocation.'))
        elif len(Amity.available_rooms) >= 1:
            random_room = choice(Amity.available_rooms)
            Room.allocate_room(ID, random_room)
            Amity.available_rooms = []
            return (cyan('and has been allocated space in ' + str(random_room)))

    def reallocate(self, ID, room_name):
        ''' This method provides the option of reallocating a person to a
        different room once the system has allocated them to the randomly
        selected room. It also passes the person's ID and room name to the
        Room's reallocate method'''

        if room_name not in Room.rooms['office'] and room_name not in Room.rooms['livingspace']:
            return (red('No such room exists'))
        if ID not in Person.people['staff'] and ID not in Person.people['fellow']:
            return (red('No person with that ID. ID is case sensitive.'))
        if room_name in Room.rooms['office']:
            if Room.rooms['office'][room_name]['Total_occupants'] == 6:
                return(red('The office %s is full to capacity.' % room_name))
            else:
                for key in Room.rooms['office']:
                    if ID in Room.rooms['office'][key]['Occupants']:
                        Room.rooms['office'][key]['Occupants'].remove(ID)
                        Room.rooms['office'][key]['Total_occupants'] -= 1
        if room_name in Room.rooms['livingspace']:
            if Room.rooms['livingspace'][room_name]['Total_occupants'] == 4:
                return (red('The livingspace %s is full to capacity.' % room_name))
            else:
                for key in Room.rooms['livingspace']:
                    if ID in Room.rooms['livingspace'][key]['Occupants']:
                        Room.rooms['livingspace'][key]['Occupants'].remove(ID)
                        Room.rooms['livingspace'][key]['Total_occupants'] -= 1
        if ID in Person.people['staff'] and room_name in Room.rooms['livingspace']:
            print (red('As staff you cannot be allocated living space'))
            return(red('As staff you cannot be allocated living space'))
        if room_name in Room.rooms['office']:
            room_type = 'office'
        else:
            room_type = 'livingspace'
        Room.rooms[room_type][room_name]['Occupants'].append(ID)
        Room.rooms[room_type][room_name]['Total_occupants'] += 1
        return str(Person.get_details(ID)) + ' has been rellocated to {}'.format(room_name)

    def print_allocations(self, filename=None):
        '''This method displays the all the allocations in the system by
        showing each room name and its corresponding occupants.There is an
        option of printing out this information on a text file'''

        if filename is not None and type(filename) is str:
            try:
                os.remove(filename)
            except OSError:
                pass
        off_occupants = []
        liv_occupants = []
        allocations = {}

        if not Room.rooms['office'] and not Room.rooms['livingspace']:
            print (red('There are no rooms in the system at the moment.'))
            return ('There are no rooms in the system at the moment.')
        elif Room.rooms['office'] or Room.rooms['livingspace']:
            print (cyan('\n\t Office Allocations'))
            print '*' * 40
            for key in Room.rooms['office']:
                if len(Room.rooms['office'][key]['Occupants']) == 0:
                    print (yellow('\n\t' + key))
                    print '-' * 40
                    print (red('No occupants'))
                elif len(Room.rooms['office'][key]['Occupants']) != 0:
                    print (yellow('\n\t' + key))
                    print '-' * 40
                    for ID in Room.rooms['office'][key]['Occupants']:
                        off_occupants.append(Person.get_details(ID))
                        if Room.rooms['office'][key]['Occupants'][-1] == ID:
                            print Person.get_details(ID) 
                        else:
                            print Person.get_details(ID) + ', ',
                    if filename is not None and type(filename) is str:
                        with open(filename, 'a') as f:
                            output = '\n\t' + key
                            output += '\n----------------------------\n'
                            output += ', '.join(off_occupants) + '\n'
                            f.write(output)
            print (cyan('\n\t Livingspace Allocations'))
            print '*' * 40
            for key in Room.rooms['livingspace']:
                if len(Room.rooms['livingspace'][key]['Occupants']) == 0:
                    print yellow('\n\t' + key)
                    print '\n----------------------------\n'
                    print (red('No occupants'))
                elif len(Room.rooms['livingspace'][key]['Occupants']) != 0:
                    print yellow('\n\t' + key)
                    print '\n----------------------------\n'
                    for ID in Room.rooms['livingspace'][key]['Occupants']:
                        liv_occupants.append(Person.get_details(ID))
                        if Room.rooms['livingspace'][key]['Occupants'][-1] == ID:
                            print Person.get_details(ID)
                        else:
                            print Person.get_details(ID) + ', ',
                    if filename is not None and type(filename) is str:
                        with open(filename, 'a') as f:
                            output = '\t' + key
                            output += '\n----------------------------\n'
                            output += ', '.join(liv_occupants) + '\n'
                            f.write(output)
                    print green('Allocations printed. Check file.')
        allocations['off_occupants'] = off_occupants
        allocations['liv_occupants'] = liv_occupants
        return allocations

    def print_unallocated(self, filename=None):
        '''This method displays the people in the system who have no room
        allocations yet. It shows the names, role and whether they require
        accomodation if they are fellows'''
        if len(Amity.unallocated_people) == 0:
            print (red('There are no unallocated people'))
            return 'There are no unallocated people'

        if filename is None:
            print (cyan('\nUnallocated people'))
            print '----------------------\n'
            for ID in Amity.unallocated_people:
                print Person.get_details(ID)
            return Person.get_details(ID)
        if filename is not None and type(filename) is str:
            try:
                os.remove(filename)
            except:
                with open(filename, 'a') as f:
                    output = '\n\tUnallocated people\n'
                    output += '------------------------\n'
                    for ID in Amity.unallocated_people:
                        output += Person.get_details(ID) + '\n'
                    f.write(output)
                    print green('Unallocated people printed. Check file.')

    def print_room(self, room_name):
        if not room_name in Room.rooms['office'] and room_name not in Room.rooms['livingspace']:
            print (red('No such room exists'))
            return (red('No such room exists'))
        else:
            if room_name in Room.rooms['office']:
                if len(Room.rooms['office'][room_name]['Occupants']) == 0:
                    print (red('No occupants.'))
                    return 'No occupants.'
                else:
                    all_occupants = []
                    print (yellow('\nOccupants of ' + room_name + ':\n'))
                    for ID in Room.rooms['office'][room_name]['Occupants']:
                        print Person.get_details(ID)
                        all_occupants.append(Person.get_details(ID))
                    return all_occupants
            elif room_name in Room.rooms['livingspace']:
                if len(Room.rooms['livingspace'][room_name]['Occupants']) == 0:
                    print (red('No occupants.'))
                    return 'No occupants'
                else:
                    print (yellow('\nOccupants of ' + room_name + ':\n'))
                    for ID in Room.rooms['livingspace'][room_name]['Occupants']:
                        all_occupants = []
                        print Person.get_details(ID)
                        all_occupants.append(Person.get_details(ID))
                    return all_occupants

    def load_people(self, filename):
        if filename:
            try:
                with open(filename, 'r') as file:
                    people = file.readlines()
                    for person in people:
                        data_list = person.split()
                        firstname = data_list[0].capitalize()
                        surname = data_list[1].capitalize()
                        designation = data_list[2].lower()
                        if len(data_list) > 3:
                            resident = data_list[3]
                        else:
                            resident = 'N'
                        self.add_person(firstname, surname, designation, resident)
                    return green('Success! Data added to the system')
            except:
                return (red('No such file exists!'))

    def save_state(self, savefile):
        """
        This method saves the current data to a database. This ensures the
        storage of the current data which can then be accessed later. It takes
        in the parameter savefile which is a file to which the database is to
        be saved to.
        """

        def db_loader(items, variety):
            for item in items:
                i = items[item]
                if variety == "office" or variety == "livingspace":
                    cursor.execute('''INSERT INTO Rooms
                                   (Name, Room_type, Max_occupants,
                                   Total_occupants, Occupants)
                                   VALUES(?, ?, ?, ?, ?)''',
                                   (i['Room_name'], variety,
                                    i['Max_occupants'], i['Total_occupants'],
                                    ', '.join(i['Occupants'])))
                elif variety == "fellow" or variety == "staff":
                    cursor.execute('''INSERT INTO People (ID, Name, Designation,
                     Resident) VALUES(?, ?, ?, ?)''', (item, i[
                                   'Name'], variety, i['Resident']))

        self.dbError = False
        connect = db.connect(savefile)
        with connect:
            cursor = connect.cursor()
            cursor.executescript('''
                    DROP TABLE IF EXISTS Rooms;
                    DROP TABLE IF EXISTS People;
                    CREATE TABLE Rooms(Name TEXT PRIMARY KEY NOT NULL,
                    Room_type TEXT NOT NULL, Max_occupants INT NOT NULL,
                    Total_occupants INT NOT NULL, Occupants TEXT);
                    CREATE TABLE People(ID TEXT PRIMARY KEY NOT NULL,
                    Name TEXT NOT NULL, Designation TEXT NOT NULL,
                    Resident TEXT NOT NULL);
                    ''')
            print 'The database is now setup'
            rooms = Room.rooms
            people = Person.people
            db_loader(rooms["office"], 'office')
            db_loader(rooms["livingspace"], 'livingspace')
            db_loader(people["fellow"], 'fellow')
            db_loader(people["staff"], 'staff')
            if not self.dbError:
                return 'The current data has been saved to the database.'

    def load_state(self, loadfile):
        """
        This method retrieves the data that was saved to the database
        in the previous session. This ensures that the application can pick up
        where it left from. It takes a parameter loadfile which specifies
        which file to load the data from.
        """
        def db_loader(table, variety):
            result = []
            final_dict = {}
            final_dict[variety] = {}
            cursor.execute("SELECT * from " + table)
            all_entries = cursor.fetchall()
            for entry in all_entries:
                if str(entry[1]) == variety and table == "Rooms":
                    final_dict[variety][str(entry[0])] = {}
                    final_dict[variety][str(entry[0])][
                        'Room_name'] = str(entry[0])
                    final_dict[variety][str(entry[0])][
                        'Max_occupants'] = str(entry[2])
                    final_dict[variety][str(entry[0])][
                        'Total_occupants'] = str(entry[3])
                    if len(entry[4]) != 0:
                        final_dict[variety][str(entry[0])][
                            'Occupants'] = str(entry[4]).split(', ')
                    else:
                        final_dict[variety][str(entry[0])]['Occupants'] = []
                    result.append(final_dict)
                elif str(entry[2]) == variety and table == "People":
                    final_dict[variety][str(entry[0])] = {}
                    final_dict[variety][str(entry[0])]['Name'] = str(entry[1])
                    final_dict[variety][str(entry[0])][
                        'Resident'] = str(entry[3])
            return final_dict

        self.dbError = False
        try:
            connect = db.connect(loadfile)
            with connect:
                cursor = connect.cursor()
                office = db_loader('Rooms', 'office')
                livingspace = db_loader('Rooms', 'livingspace')
                fellow = db_loader('People', 'fellow')
                staff = db_loader('People', 'staff')
                rooms = dict(office, **livingspace)
                people = dict(fellow, **staff)
                Room.rooms = rooms
                Person.people = people
                if not self.dbError:
                    return "Data has been successfully loaded from the database."
        except:
            return 'Error accessing that database!'
