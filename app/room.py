
class Room(object):
    ''' Class Room models the rooms in Amity. The two types of rooms, Office and
    Livingspace inherit from it.'''

    rooms = {"office": {}, "livingspace": {}}

    def __init__(self):
        pass

    @staticmethod
    def allocate_room(ID, room_name):
        if room_name in Room.rooms['office'].keys():
            room_type = 'office'
        elif room_name in Room.rooms['livingspace'].keys():
            room_type = 'livingspace'
        Room.rooms[room_type][room_name]['Occupants'].append(ID)
        Room.rooms[room_type][room_name]['Total_occupants'] += 1


class Office(Room):
    def __init__(self, room_name=[], max_occupants=6, Total_occupants = 0):
        self.room_name = room_name
        self.max_occupants = max_occupants
        self.rooms['office'][room_name] = {}
        self.rooms['office'][room_name]['Room_name'] = room_name
        self.rooms['office'][room_name]['Max_occupants'] = max_occupants
        self.rooms['office'][room_name]['Occupants'] = []
        self.rooms['office'][room_name]['Total_occupants'] = 0


class Livingspace(Room):
    def __init__(self, room_name=[], max_occupants=4, Total_occupants = 0):
        self.room_name = room_name
        self.max_occupants = max_occupants
        self.rooms['livingspace'][room_name] = {}
        self.rooms['livingspace'][room_name]['Room_name'] = room_name
        self.rooms['livingspace'][room_name]['Max_occupants'] = max_occupants
        self.rooms['livingspace'][room_name]['Occupants'] = []
        self.rooms['livingspace'][room_name]['Total_occupants'] = 0


