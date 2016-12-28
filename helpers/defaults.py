import csv

class Defaults:
    BAD_LIGHTING_DEDUCT = 'bad_lighting_deduct'
    ROUND_DOLLAR = 'round_dollar'
    COMMON_WEIGHT = 'common_weight'
    CALCULATE_AS_SINGLES = 'calculate_singles'
    RENT_SUM = 'rent_sum'
    HOUSE_SIZE = 'house_size'
    FILE = 'file'
    
    def __init__(self, file_name='csv/defaults.csv'):
        self.file_name = file_name
        self.get_default_args()
        
    def get_default_args(self):
        with open(self.file_name) as csvfile:
            reader = csv.DictReader(csvfile)
            data = next(reader)
            self.bad_lighting_deduct = data.get(self.BAD_LIGHTING_DEDUCT)
            self.round_dollar = data.get(self.ROUND_DOLLAR)
            self.common_weight = data.get(self.COMMON_WEIGHT)
            self.calculate_singles = data.get(self.CALCULATE_AS_SINGLES)
            self.rent_sum = data.get(self.RENT_SUM)
            self.house_size = data.get(self.HOUSE_SIZE)
            self.rooms_file = data.get(self.FILE)