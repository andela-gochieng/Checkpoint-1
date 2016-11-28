# from room import Office, LivingSpace

class Amity(object): 

	office_max_occupants = 6
	livingspace_occupants =  4

	rooms = {"offices":{},"livingspaces": {}}
	staff = {}
	fellows = {}
	details = {}

	def __init__(self):
		print "Creating our Logistics Handler..."

	def create_room(self,name, room_type):
		if room_type =='Office':
			self.rooms['offices'] = name
		elif room_type == 'Livingspace':
			self.rooms['offices'] = name


new_room = Amity()
new_room.create_room('Yellow','Office')
print new_room.rooms['offices']



	# def create_livingspace(self,a):
	# 	pass
	
	# def add_person(self, a, b, c="N"):
	# 	pass

	# def create_office(self,a):
	# 	pass
	
	# def allocate_office(self,x,y):
	# 	pass
	
	# def allocate_room(self,a,b):
	# 	pass
	
	# def reallocate(self,a,b):
	# 	pass
	
	# def get_details_person(self,a):
	# 	pass
	
	# def get_details_room(self,a):
	# 	pass
	# 