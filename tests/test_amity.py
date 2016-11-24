#from mock import patch
import unittest

from app.amity import Amity

class TestRooms(unittest.TestCase):

	def setUp(self):
		
		self.amity = Amity()

	#@patch.dict('app.amity.Amity.rooms', {'livingspaces': []})
	#def test_it_creates_livingspaces(self):
		#details = self.room.create_livingspace('Emerald')
		#self.assertIn('Emerald', self.rooms[livingspaces])

	def test_create_livingspace(self):
		self.amity.create_room('Yellow')
		self.assertIn('Yellow',self.amity.rooms['livingspaces'])

	def test_create_office(self):
		self.amity.create_room('Purple')
		self.assertIn('Purple',self.amity.rooms['offices'])

	def test_create_room_duplicate_rooms(self):
		creation = self.amity.create_room('Yellow')
		self.assertEqual(creation, 'A room with that name already exists')


	def test_get_details_room(self):
		details = self.amity.get_details_room('Yellow')
		self.assertEqual(details,self.amity.details)

	def test_relocate_new_room(self):
		reallocation = self.amity.reallocate(5,'Green')
		self.assertIn(5,self.amity.rooms['offices']['Green'])

	def test_add_staff(self):
		self.amity.add_person('Mary Chepkoech', 'STAFF')
		self.assertIn('Mary Chepkoech',self.amity.staff)

	def test_add_fellow(self):
		self.amity.add_person('Mark Kitavi','FELLOW','Y')
		self.assertIn('Mark Kitavi',self.amity.fellows)

	def test_get_details_person(self):
		details = self.amity.get_details_person('Mark Kitavi')
		self.assertEqual('Mark Kitavi Fellow',details)

