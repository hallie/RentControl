from collections import namedtuple
from optparse import OptionParser

Deets = namedtuple('Deets', ['sqft', 'has_window', 'occupied_by'])
Rent  = namedtuple('Rent', ['price', 'room', 'deets'])
floor_plan = """
[Floor B]                  [Floor C]
|------------------------  |------------------------
|         |    R1 |        |    R1  |   R2   |
|-----      ------         |-----------------
| R2  |     |  R3 |        |
|-----       -----         |
|BRoom                     |
|BRoom                     |BRoom       -----
|                          |BRoom      | R3  |
|Kitchen                   |
|----         ----         |Kitchen
| R4 |       | R5 |        |-----       -----
-------------------        | R4  |     | R5  |
                           -------------------
"""

B_R1 = ["Single"]
B_R2 = ["Single"]
B_R3 = ["Single"]
B_R4 = ["Double", "Double"]
B_R5 = ["Double", "Double"]
C_R1 = ["Single"]
C_R2 = ["Single"]
C_R3 = ["Single"]
C_R4 = ["Single"]
C_R5 = ["Double", "Double"]

rooms = {
    # F-R#         SqFt   Has Window   Occupied By
    "B-R1": Deets( 160.0, True,        B_R1),
    "B-R2": Deets( 160.0, False,       B_R2),
    "B-R3": Deets( 150.0, False,       B_R3),
    "B-R4": Deets( 140.0, True,        B_R4),
    "B-R5": Deets( 140.0, True,        B_R5),
    "C-R1": Deets( 190.0, True,        C_R1),
    "C-R2": Deets( 190.0, True,        C_R2),
    "C-R3": Deets( 170.0, False,       C_R3),
    "C-R4": Deets( 160.0, True,        C_R4),
    "C-R5": Deets( 160.0, True,        C_R5),
}

# Takes in a decimal representing the percent weight of the common space that
#   will factor into rent.
def calculate_common_attrs(weight=.5):
    common_space = HOUSE_SIZE - sum([room.sqft for room in rooms.values()])
    common_share = common_space/PEEPS_COUNT
    common_cost_per_sqft = RENT_SUM/HOUSE_SIZE * weight
    common_share_cost = round(common_share * common_cost_per_sqft, 2)
    return common_share_cost, common_cost_per_sqft, common_space


# If its `has_attr` its expecting to apply the fee to the group that has attr.
# Otherwise, it gets everyone who doesn't.
# returns cost, opposing_cost
def calculate_opposing_fee(attr, cost, has_attr=True):
    peeps_with_attr = sum([len(deets.occupied_by) for deets in rooms.values()
                           if getattr(deets, attr) == has_attr])
    if peeps_with_attr and peeps_with_attr != PEEPS_COUNT:
        if has_attr:
            opp_cost = (PEEPS_COUNT - peeps_with_attr) * cost
            opp_cost /= peeps_with_attr * -1
            return cost, round(opp_cost, 2)
        opp_cost = peeps_with_attr * cost
        opp_cost /= (PEEPS_COUNT - peeps_with_attr) * -1
        return cost, round(opp_cost, 2)
    return 0, 0


# Putting up here for cleanliness reasons. Makes it easier to add more later.
def apply_fees_or_discounts(deets):
    bonus_fees_or_discounts = GOOD_LIGHTING_FEE if deets.has_window \
                                                else BAD_LIGHTING_DEDUCTION
    return bonus_fees_or_discounts


def calculate_rent(deets, round_dollar=True):
    room_size, has_window, occupants = deets
    occupants = len(occupants)
    base_cost = COMMON_SHARE_COST * occupants
    room_cost = room_size * ROOM_COST_PER_SQFT
    bonus_fees_or_discounts = apply_fees_or_discounts(deets)
    rent = (base_cost + room_cost) + (bonus_fees_or_discounts * occupants)
    if round_dollar:
        return int(rent)
    return rent


# Since there's lots of division happening, it makes more sense for us to drop
#  all of the extra pennies on people paying the least.
def cheapest_room_picks_up_the_cents(rents):
    rents = sorted(rents)
    missing_money = RENT_SUM - sum([rent.price for rent in rents])
    # If the math somehow comes out to more than the cost of the house,
    #  it subtracts from the most expensive room.
    if missing_money < 0:
        rents = rents[::-1]
    has_lowest_price = len([rent for rent in rents 
                            if rent[0] == rents[0].price])
    new_price = rents[0].price + (missing_money / has_lowest_price)
    for i in range(has_lowest_price):
        rents[i] = Rent(new_price, rents[i].room, rents[i].deets)
    return rents


# Takes in a list of Rent
def print_rents_per_room(rents):
    row_divider = "-" * 80
    row_format = "{:^15}|{:^15}|{:^15}|{:^15}|{:^15}"

    print
    print row_format.format("Room", "Rent", "SqFt", "Good Lighting",
                            "Occupants")
    print row_divider
    for rent in sorted(rents):
        print row_format.format(rent.room, ("$%.2f" % rent[0]),
                                rent.deets.sqft,str(rent.deets.has_window), 
                                ", ".join(rent.deets.occupied_by))
    print row_divider
    print "{:^15}|{:^15}|".format(
        "Total", "$%.2f" % sum([rent.price for rent in rents]))
    print


# Takes in a list of Rent objects and uses it to print out individual rents.
def print_cost_per_person(rents):
    cost_person = []
    for rent in rents:
        cost = rent.price / len(rent.deets.occupied_by)
        for person in rent.deets.occupied_by:
            cost_person.append([cost, person, rent.room])
    
    row_divider = "-" * 50
    row_format = "{:^15}|{:^15}|{:^15}"
    
    print
    print row_format.format("Name", "Room", "Rent")
    print row_divider
    for rent in sorted(cost_person):
        print row_format.format(rent[1], rent[2], "$%.2f" % rent[0])
    print row_divider
    print


RENT_SUM = 15000.00
HOUSE_SIZE = 6000.00

parser = OptionParser()
parser.add_option("--bld", "--bad_lighting_deduct", dest="bad_lighting_deduct",
                  default="100", help="Deduction for poorly lit rooms")
parser.add_option("--rd", "--round_dollar", dest="round_dollar",
                  default="True", help="Round to nearest dollar")
parser.add_option("--cw", "--common_weight", dest="common_weight",
                  default=".6", help="Weight of common space on rent price")
parser.add_option("--cs", "--calculate_singles", dest="calculate_singles",
                  default="False", help="Check pricing all rooms were singles")
parser.add_option("--rs", "--rent_sum", dest="rent_sum",
                  default=RENT_SUM, help="The total cost of combined space")
parser.add_option("--hs", "--house_size", dest="house_size",
                  default=HOUSE_SIZE, help="The total square footage of home")
    

if __name__ == '__main__':
    options, args = parser.parse_args()
    COMMON_WEIGHT = float(options.common_weight)
    ROUND_DOLLAR = options.round_dollar == "True"
    CACULATE_AS_SINGLES = options.calculate_singles == "True"
    
    HOUSE_SIZE = float(options.house_size)
    RENT_SUM = float(options.rent_sum)
    if CACULATE_AS_SINGLES:
        for room in rooms:
            deets = rooms[room]
            deets = Deets(deets.sqft, deets.has_window,
                          ["/".join(deets.occupied_by)])
            rooms[room] = deets
    PEEPS_COUNT = sum([len(room.occupied_by) for room in rooms.values()])
    
    BAD_LIGHTING_DEDUCTION, GOOD_LIGHTING_FEE = calculate_opposing_fee(
        'has_window', float(options.bad_lighting_deduct) * -1)
    
    COMMON_SHARE_COST, COMMON_COST_PER_SQFT, COMMON_SPACE = calculate_common_attrs(COMMON_WEIGHT)

    ROOM_COST_PER_SQFT = RENT_SUM - (COMMON_SHARE_COST * PEEPS_COUNT)
    ROOM_COST_PER_SQFT /= HOUSE_SIZE - COMMON_SPACE
    
    rents = []
    for room, deets in rooms.iteritems():
        rent = calculate_rent(deets, ROUND_DOLLAR)
        rents.append(Rent(rent, room, deets))
    
    rents = sorted(rents)
    if ROUND_DOLLAR:
        rents = cheapest_room_picks_up_the_cents(rents)
        
    print floor_plan
    print "People in House:", PEEPS_COUNT
    print "Total SqFt:", HOUSE_SIZE
    print "Common Space:", COMMON_SPACE
    print "Cost per Common SqFt: $%.2f (Weighted by %.2f)" % (
        COMMON_COST_PER_SQFT, COMMON_WEIGHT)
    print "Common Cost: $%.2f" % COMMON_SHARE_COST
    print "Cost per Room SqFt: $%.2f" % ROOM_COST_PER_SQFT
    print "Bad Lighting Rebate: $%.2f" % BAD_LIGHTING_DEDUCTION
    print "Good Lighting Upcharge: %.2f" % GOOD_LIGHTING_FEE
    
    print_rents_per_room(rents)
    if not CACULATE_AS_SINGLES:
        print_cost_per_person(rents)
