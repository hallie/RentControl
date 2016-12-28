import csv

from helpers import Deets

class Home:
    rooms = {}
    cheapest_rooms = []
    cheapest_room_must_be_single = True
    
    def __init__(self, options):
        self.file_name = options.file_name
        self.fill_house()
        self.common_weight = float(options.common_weight)
        self.round_dollar = (options.round_dollar == 'True')
        self.calculate_as_singles = (options.calculate_singles == 'True')
        if self.calculate_as_singles:
            self.change_to_singles()
        self.peeps_count = sum([len(room.occupied_by) for room in self.rooms.values()])
        self.house_size = float(options.house_size)
        self.rent_sum = float(options.rent_sum)
        
        self.calculate_common_attrs()
        self.calculate_room_sqft_costs()
    
    def set_cheapest_room(self, rent):
        if self.cheapest_room_must_be_single and (len(rent.deets.occupied_by) != 1):
            return
        if not self.cheapest_rooms:
            self.cheapest_rooms.append(rent)
        else:
            r = rent.price / len(rent.deets.occupied_by)
            print self.cheapest_rooms
            cr = self.cheapest_rooms[0].price / len(self.cheapest_rooms[0].deets.occupied_by)
            if cr > r:
                self.cheapest_rooms = [rent]
            elif cr == r:
                self.cheapest_rooms.append(rent)
        
    def change_to_singles(self):
        for room_id in self.rooms:
            occupants = self.rooms[room_id].occupied_by
            self.rooms[room_id].occupied_by = '/'.join(occupants)
            
    # If its `has_attr` its expecting to apply the fee to the group that has attr.
    # Otherwise, it gets everyone who doesn't.
    # returns cost, opposing_cost
    def calculate_opposing_fee(self, attr, cost, has_attr=True):
        peeps_with_attr = sum([len(deets.occupied_by) for deets in self.rooms.values()
                               if getattr(deets, attr) == has_attr])
        if peeps_with_attr and peeps_with_attr != self.peeps_count:
            if has_attr:
                opp_cost = (self.peeps_count - peeps_with_attr) * cost
                opp_cost /= peeps_with_attr * -1
                return cost, round(opp_cost, 2)
            opp_cost = peeps_with_attr * cost
            opp_cost /= (self.peeps_count - peeps_with_attr) * -1
            return cost, round(opp_cost, 2)
        return 0, 0
    
    # Takes in a decimal representing the percent weight of the common space that
    #   will factor into rent.
    def calculate_common_attrs(self):
        self.common_space = self.house_size - sum([room.sqft for room in self.rooms.values()])
        common_share = self.common_space/self.peeps_count
        self.common_cost_per_sqft = self.rent_sum/self.house_size * self.common_weight
        self.common_share_cost = round(common_share * self.common_cost_per_sqft, 2)
        
    def calculate_room_sqft_costs(self):
        self.room_cost_per_sqft = self.rent_sum - (self.common_share_cost * self.peeps_count)
        self.room_cost_per_sqft /= self.house_size - self.common_space
            
    def fill_house(self):
        with open(self.file_name, 'r') as csvfile:
            rooms_deets = csv.DictReader(csvfile)
            for room in rooms_deets:
                deets = Deets(room)
                self.rooms[deets.id] = deets