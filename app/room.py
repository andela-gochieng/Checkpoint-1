from app.amity import Amity

class Room(object):
	offices = {}
	livingspaces = {}
	office_occupants =[]
	chamber_occupants =[]
	

class Office(Room):
	max_occupants = 6
	
	def __init__(self):
		self.current_capacity = 0

	def allocate_office(self,x):
		pass
	
	def available_slots(self):
		pass
	def get_details(self,a):
		pass


class LivingSpace(Room):
	max_occupants = 4

	def __init__(self):
		self.current_capacity = 0

	def allocate_room(self,a):
		pass
																													
	def available_slots(self):
		pass
	def get_details(self,a):
		pass