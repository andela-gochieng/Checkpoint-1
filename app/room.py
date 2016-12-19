#from app.amity import Amity


class Room(object):
    ''' Class Room models the rooms in Amity. The two types of rooms, Office and
    Livingspace inherit from it.'''

    rooms = {"office": {}, "livingspace": {}}

    def __init__(self, room_name, room_type, max_occupants, current_capacity=0):
        self.room_name = room_name
        self.room_type = room_type
        self.max_occupants = max_occupants
        self.rooms[room_type][room_name] = {}
        self.rooms[room_type][room_name]['Room_name'] = room_name
        self.rooms[room_type][room_name]['Max_occupants'] = max_occupants
        self.rooms[room_type][room_name]['Occupants'] = []
        self.rooms[room_type][room_name]['Total_occupants'] = 0

    @staticmethod
    def allocate_room(ID, room_name):
        if room_name in Room.rooms['office'].keys():
            room_type = 'office'
        elif room_name in Room.rooms['livingspace'].keys():
            room_type = 'livingspace'
        Room.rooms[room_type][room_name]['Occupants'].append(ID)
        Room.rooms[room_type][room_name]['Total_occupants'] += 1


class Office(Room):
    def __init__(self, room_name=[], max_occupants=6):
        super(Office, self).__init__(room_name, 'office', max_occupants)


class Livingspace(Room):
    def __init__(self, room_name=[], max_occupants=4):
        super(Livingspace, self).__init__(
            room_name, 'livingspace', max_occupants)



