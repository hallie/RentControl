import csv

class Deets:
    ID = 'room_id'
    SQFT = 'sqft'
    HAS_WINDOW = 'has_window'
    OCCUPIED_BY = 'occupied_by'
    PERCENT_USABLE = 'percent_usable'
    
    def __init__(self, deets_dict):
        self.id = deets_dict[self.ID]
        self.sqft = float(deets_dict[self.SQFT])
        self.has_window = (deets_dict[self.HAS_WINDOW] == 'True')
        self.occupied_by = deets_dict[self.OCCUPIED_BY].split(',')
        self.percent_usable = float(deets_dict[self.PERCENT_USABLE])
