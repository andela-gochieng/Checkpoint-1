import unittest
from app.person import Person,Fellow, Staff

class TestPerson(unittest.TestCase):

	def setUp(self):
		self.fellow = Fellow()
		self.staff = Staff()
	def test_get_details(self):
		pass