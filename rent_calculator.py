import csv

from helpers import Home, Options, Rent


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


# Putting up here for cleanliness reasons. Makes it easier to add more later.
def apply_fees_or_discounts(deets, home):
    bonus_fees_or_discounts = home.good_lighting_fee if deets.has_window \
                                                else home.bad_lighting_deduction
    return bonus_fees_or_discounts


def calculate_rent(room_deets, home, round_dollar=True):
    occupants = len(room_deets.occupied_by)
    base_cost = home.common_share_cost * occupants
    room_cost = room_deets.sqft * home.room_cost_per_sqft * room_deets.percent_usable
    bonus_fees_or_discounts = apply_fees_or_discounts(room_deets, home)
    rent = (base_cost + room_cost) + (bonus_fees_or_discounts * occupants)
    if round_dollar:
        return int(rent)
    return rent


# Since there's lots of division happening, it makes more sense for us to drop
#  all of the extra pennies on people paying the least.
def cheapest_room_picks_up_the_cents(rents, home):
    missing_money = home.rent_sum - sum([rent.price for rent in rents.values()])
    num_people_with_lowest_price = sum([len(rent.deets.occupied_by) for rent in home.cheapest_rooms])
    cent_diff = missing_money / num_people_with_lowest_price
    for rent in home.cheapest_rooms:
        new_price = rent.price + (cent_diff * len(rent.deets.occupied_by))
        rents[rent.room] = Rent(new_price, rent.room, rent.deets)
    return rents


# Takes in a list of Rent
def print_rents_per_room(rents):
    row_divider = "-" * 96
    row_format = "{:^15}|{:^15}|{:^15}|{:^15}|{:^15}|{:^15}"

    print
    print row_format.format("Room", "Rent", "SqFt", "% Usable",
                             "Good Lighting", "Occupants")
    print row_divider
    for rent in sorted(rents):
        print row_format.format(rent.room, ("$%.2f" % rent[0]),
                                rent.deets.sqft,
                                "{}%".format(int(rent.deets.percent_usable * 100)),
                                str(rent.deets.has_window), 
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

    

if __name__ == '__main__':
    options, args = Options.parse_args()
    home = Home(options)
    
    home.bad_lighting_deduction, home.good_lighting_fee = home.calculate_opposing_fee(
        'has_window', float(options.bad_lighting_deduct) * -1)
    
    rents = {}
    for room, deets in home.rooms.iteritems():
        rent = calculate_rent(deets, home, home.round_dollar)
        room_rent = Rent(rent, room, deets)
        home.set_cheapest_room(room_rent)
        rents[room] = room_rent
    
    if home.round_dollar:
        rents = cheapest_room_picks_up_the_cents(rents, home)
    rents = sorted(rents.values())
        
    print floor_plan
    print "People in House:", home.peeps_count
    print "Total SqFt:", home.house_size
    print "Common Space:", home.common_space
    print "Cost per Common SqFt: $%.2f (Weighted by %.2f)" % (
        home.common_cost_per_sqft, home.common_weight)
    print "Common Cost: $%.2f" % home.common_share_cost
    print "Cost per Room SqFt: $%.2f" % home.common_cost_per_sqft
    print "Bad Lighting Rebate: $%.2f" % home.bad_lighting_deduction
    print "Good Lighting Upcharge: $%.2f" % home.good_lighting_fee
    
    print_rents_per_room(rents)
    if not home.calculate_as_singles:
        print_cost_per_person(rents)
