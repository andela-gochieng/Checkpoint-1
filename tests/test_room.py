import unittest
from app.room import Room,Office, Livingspace

class TestRoom(unittest.TestCase):

	def setUp(self):
		self.office = Office()
		self.chamber = Livingspace()


	def test_allocate_office_to_staff(self):
		allocation = self.office.allocate_office(5)
		self.assertEqual('Successfully booked into Purple',allocation)

	def test_allocate_office_to_fellow(self):
		allocation = self.office.allocate_office(2)
		self.assertEqual('Successfully booked into Purple',allocation)

	def test_allocate_room_to_fellow(self):
		allocation = self.chamber.allocate_quarters(4)
		self.assertEqual('Successfully booked into Yellow',allocation)

	def test_allocate_room_to_staff(self):
		allocation = self.chamber.allocate_quarters(3)
		self.assertEqual('As staff you cannot be allocated living space',allocation)

	def test_allocate_room_in_fully_booked_room(self):
		allocation = self.chamber.allocate_quarters(6)
		self.assertEqual('Room Yellow is fully occupied',allocation)

	def test_capacity(self):
		self.office.allocate_office(11)
		self.office.allocate_office(12)
		self.office.allocate_office(13)
		self.chamber.allocate_room(14)
		self.chamber.allocate_room(15)
		self.assertEqual(self.office.max_occupants - self.office.current_capacity, 3)
		self.assertEqual(self.chamber.max_occupants - self.chamber.current_capacity, 2)

	def test_get_details(self):
		self.assertEqual(self.office.get_details, Room.office_occupants)
		self.assertEqual(self.chamber.get_details, Room.chamber_occupants)

	def test_get_details_nonexistent_room(self):
		self.office2 = 'office'
		self.chamber2 = 'chamber'
		self.assertIsInstance(self.office2, Office, msg='No such room exists')
		

	





		
