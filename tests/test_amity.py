import os
import sys
import unittest
from mock import patch
from app.amity import Amity
from app.person import Person, Staff, Fellow
from app.room import Room, Office, Livingspace

class TestAmity(unittest.TestCase):
    '''This class tests all the funtionality of the amity famility allocation 
    system. It has only focussed on the amity module since the class amity 
    interacts with all the other modules and performs all the logical functioning
    of the application'''
    def setUp(self):
        self.amity = Amity()

    def test_returns_error_if_input_is_nonalphabetical(self):
        self.assertEqual(self.amity.create_room(['123'],'office'), 'Invalid room name type')
        #print os.getcwd()

    def test_returns_error_given_wrong_roomtype(self):
        self.assertEqual(self.amity.create_room(['Purple'],'workspace'), 'Room type can only be office or livingspace')
        #print os.getcwd()

    def test_create_room(self):
        self.amity.create_room(["Pink"], "office")
        self.amity.create_room(['Blue'],'livingspace')
        self.assertIn("Pink", Room.rooms['office'])
        self.assertIn('Blue', Room.rooms['livingspace'])

    @patch.dict('app.room.Room.rooms', {
                    "office": {},
                    "livingspace": {}
                })
    @patch.dict('app.person.Person.people', {
                    "staff": {},
                    "fellow": {}
                })
    @patch.object(Amity, "offices", 0)
    @patch.object(Amity, "livingspaces", 0)
    def test_message(self):
        res = self.amity.create_room(["Pink"], "office")
        self.assertIn('There are 1 offices and 0 livingspaces in the system.', res)

    @patch.dict('app.room.Room.rooms', {
                    "office": {},
                    "livingspace": {}
                })
    @patch.dict('app.person.Person.people', {
                    "staff": {},
                    "fellow": {}
                })
    @patch.object(Amity, "offices", 0)
    @patch.object(Amity, "livingspaces", 0)
    def test_create_room_increments_rooms_by_one(self):
        self.assertEqual(len(Room.rooms['office']), 0)
        self.amity.create_room( ["Orange"], "office")
        self.assertEqual(len(Room.rooms['office']), 1)
            
    @patch.dict('app.room.Room.rooms', {
                    "office": {'Yellow':[]},
                    "livingspace": {}
                })
    @patch.dict('app.person.Person.people', {
                    "staff": {},
                    "fellow": {}
                })
    @patch.object(Amity, "offices", 0)
    @patch.object(Amity, "livingspaces", 0)
    def test_create_room_duplicate_rooms(self):
        self.assertEqual(self.amity.create_room(['Yellow'], 'office'), 'A room with that name exists. Select another name')
            
    '''This section tests the functionality of adding a person to the system, 
    allocation of rooms and reallocation of a person from one room to another'''

    def test_only_alphabetical_names_allowed(self):
        self.assertEqual(self.amity.add_person('1234','Menjo', 'fellow'), 'Invalid name format. Alphabets only')
        self.assertEqual(self.amity.add_person('Menjo','1234', 'fellow'), 'Invalid name format. Alphabets only')

    def test_restriction_on_job_designation(self):
        self.assertEqual(self.amity.add_person('Charlie', 'Kip', 'worker'),'Enter a valid designation' )

    def test_restriction_on_residence(self):
        self.assertEqual(self.amity.add_person('Charlie', 'Kip', 'fellow', 'R'),'Respond with Y or N for residence' )

    def test_new_person_gets_ID(self):
        self.amity.add_person('Mary','Chepkoech', 'staff')
        self.assertIn('ST01', Person.people['staff'])
        self.amity.add_person('Kevin','Leo','fellow','Y')
        self.assertIn('FE01', Person.people['fellow'])

    @patch.dict('app.room.Room.rooms', {
                    "office": {
                        'Yellow': {
                            "Room_name": 'Yellow',
                            "Max_occupants": 6,
                            "Total_occupants": 0,
                            "Occupants": []
                        }
                    },
                    "livingspace": {}
                })
    @patch.dict('app.person.Person.people', {
                    "staff": {},
                    "fellow": {}
                })
    @patch.object(Amity, "offices", 1)
    @patch.object(Amity, "livingspaces", 0)
    def test_add_person_adds_person_to_lists(self):
        self.amity.add_person('Mary', 'Chepkoech', 'staff')
        self.amity.add_person('Kevin', 'Leo', 'fellow', 'Y')
        self.assertIn('Mary Chepkoech', Person.people['staff']['ST01']['Name'])
        self.assertIn('Kevin Leo', Person.people['fellow']['FE01']['Name'])
    
    @patch.dict('app.room.Room.rooms', {
                    "office": {
                        'Brown': {
                            "Room_name": 'Brown',
                            "Max_occupants": 6,
                            "Total_occupants": 0,
                            "Occupants": []
                        }
                    },
                    "livingspace": {
                        'Beige': {
                            "Room_name": 'Beige',
                            "Max_occupants": 4,
                            "Total_occupants": 0,
                            "Occupants": []
                        }
                    }
                })
    @patch.dict('app.person.Person.people', {
                    "staff": {},
                    "fellow": {}
                })
    @patch.object(Amity, "offices", 1)
    @patch.object(Amity, "livingspaces", 1)
    def test_person_is_allocated_room_after_creation(self):
        self.amity.add_person('Sophie', 'Njeri', 'fellow', 'Y')
        self.assertIn('FE01', Room.rooms['office']['Brown']['Occupants'])
        self.assertIn('FE01', Room.rooms['livingspace']['Beige']['Occupants'])

    @patch.dict('app.room.Room.rooms', {
                    "office": {},
                    "livingspace": {}
                })
    @patch.dict('app.person.Person.people', {
                    "staff": {},
                    "fellow": {}
                })
    @patch.object(Amity, "offices", 0)
    @patch.object(Amity, "livingspaces", 0)
    def test_reallocate_person(self):
        self.amity.create_room(['Brown'],'office')
        self.amity.create_room(['Beige'], 'livingspace')
        self.amity.add_person('Sophie', 'Njeri','fellow', 'Y')
        self.amity.create_room(["Orange"], "office")
        self.amity.reallocate('FE01','Orange')
        self.assertIn('FE01', Room.rooms['office']['Orange']['Occupants'])

    @patch.dict('app.room.Room.rooms', {
                    "office": {
                        'Brown': {
                            "Room_name": 'Brown',
                            "Max_occupants": 6,
                            "Total_occupants": 0,
                            "Occupants": []
                        }
                    },
                    "livingspace": {
                        'Beige': {
                            "Room_name": 'Beige',
                            "Max_occupants": 4,
                            "Total_occupants": 0,
                            "Occupants": []
                        }
                    }
                })
    @patch.dict('app.person.Person.people', {
                    "staff": {},
                    "fellow": {}
                })
    @patch.object(Amity, "offices", 1)
    @patch.object(Amity, "livingspaces", 1) 
    def test_reallocation_to_nonexistent_room(self):
        self.amity.add_person('Sophie', 'Njeri','fellow', 'Y')
        self.assertIn('No such room exists', self.amity.reallocate('FE01','Orange'))

#Tests the print_room functionality
    def test_print_room_nonexistent_room(self):
        self.assertIn('No such room exists', self.amity.print_room('Orange'))

    def test_print_room_with_no_occupants(self):
        self.amity.create_room(['Brown'], 'office')
        self.assertEqual(self.amity.print_room('Brown'), 'No occupants.')

    @patch.dict('app.room.Room.rooms', {
                    "office": {},
                    "livingspace": {}
                })
    @patch.dict('app.person.Person.people', {
                    "staff": {},
                    "fellow": {}
                })
    @patch.object(Amity, "offices", 0)
    @patch.object(Amity, "livingspaces", 0) 
    def test_print_room_with_occupants(self):
        self.amity.create_room(['Brown'],'office')
        self.amity.add_person('Sophie', 'Njeri','fellow')
        self.assertIn('FE01 -> Sophie Njeri', self.amity.print_room('Brown'))

        
    # Tests the printing of unallocated persons
    @patch.dict('app.room.Room.rooms', {
                    "office": {},
                    "livingspace": {}
                })
    @patch.dict('app.person.Person.people', {
                    "staff": {},
                    "fellow": {}
                })
    @patch.object(Amity, "offices", 0)
    @patch.object(Amity, "livingspaces", 0)
    @patch.object(Amity, "unallocated_people", [])
    def test_empty_unallocated(self):
        self.assertEqual(self.amity.print_unallocated(), 'There are no unallocated people')

    @patch.dict('app.room.Room.rooms', {
                    "office": {},
                    "livingspace": {}
                })
    @patch.dict('app.person.Person.people', {
                    "staff": {},
                    "fellow": {}
                })
    @patch.object(Amity, "offices", 0)
    @patch.object(Amity, "livingspaces", 0)
    def test_unallocated_with_entries(self):
        self.amity.add_person('Sophie', 'Njeri', 'fellow')
        self.assertIn('Sophie Njeri', self.amity.print_unallocated())

    #Tests for the print allocations begin here
    @patch.dict('app.room.Room.rooms', {
                    "office": {},
                    "livingspace": {}
                })
    @patch.dict('app.person.Person.people', {
                    "staff": {},
                    "fellow": {}
                })
    @patch.object(Amity, "offices", 0)
    @patch.object(Amity, "livingspaces", 0)
    def test_print_allocations_with_no_rooms(self):
        self.assertEqual(self.amity.print_allocations(), 'There are no rooms in the system at the moment.')


    @patch.dict('app.room.Room.rooms', {
                    "office": {},
                    "livingspace": {}
                })
    @patch.dict('app.person.Person.people', {
                    "staff": {},
                    "fellow": {}
                })
    @patch.object(Amity, "offices", 0)
    @patch.object(Amity, "livingspaces", 0)

    @patch.dict('app.room.Room.rooms', {
                    "office": {
                        'Brown': {
                            "Room_name": 'Brown',
                            "Max_occupants": 6,
                            "Total_occupants": 0,
                            "Occupants": ['ST01']
                        }
                    },
                    "livingspace": {}
                })
    @patch.dict('app.person.Person.people', {
                "staff": {
                    'ST01': {
                        'Name':'Mary Chepkoech',
                        'Resident': 'N'
                        }
                    },
                    "fellow": {}
                })
    @patch.object(Amity, "offices", 1)
    @patch.object(Amity, "livingspaces", 0)
    def test_print_allocations_with_occupants_in_rooms(self):
        res = self.amity.print_allocations()
        self.assertIn('ST01 -> Mary Chepkoech', res['off_occupants'])

    # Tests for the load people method begins here

    @patch.dict('app.person.Person.people', {
                "staff": {},
                "fellow": {}
                })
    def test_load_people(self):
        if os.path.exists('app'):
            os.chdir('app')
        self.amity.load_people('test.txt')
        assert (Person.people['staff'] > 1)

    # Tests for the database
    def test_save_state(self):
        if os.path.exists('app'):
            os.chdir('app')
        self.assertEqual(self.amity.save_state('savefile.db'),
                         'The current data has been saved to the database.')

    @patch.object(Room, "rooms", {"office": {}, "livingspace": {}})
    @patch.object(Person, "people", {"staff": {}, "fellow": {}})
    @patch.object(Amity, "offices", 0)
    @patch.object(Amity, "livingspaces", 0)
    @patch.object(Amity, "available_rooms", [])
    @patch.object(Amity, "unallocated_people", [])
    def test_load_state(self):
        if os.path.exists('app'):
            os.chdir('app')
        self.assertEqual(
            self.amity.load_state('infile.db'),
            "Data has been successfully loaded from the database."
        )










