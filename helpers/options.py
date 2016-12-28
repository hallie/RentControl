from optparse import OptionParser
from helpers import Defaults

defaults = Defaults()
parser = OptionParser()
parser.add_option(
    "--bld",
    "--bad_lighting_deduct",
    dest="bad_lighting_deduct",
    default=defaults.bad_lighting_deduct,
    help="Deduction for poorly lit rooms"
)
parser.add_option(
    "--rd",
    "--round_dollar",
    dest="round_dollar",
    default=defaults.round_dollar,
    help="Round to nearest dollar"
)
parser.add_option(
    "--cw",
    "--common_weight",
    dest="common_weight",              
    default=defaults.common_weight,
    help="Weight of common space on rent price"
)
parser.add_option(
    "--cs",
    "--calculate_singles",
    dest="calculate_singles",              
    default=defaults.calculate_singles, 
    help="Check pricing all rooms were singles"
)
parser.add_option(
    "--rs",
    "--rent_sum",
    dest="rent_sum",
    default=defaults.rent_sum,
    help="The total cost of combined space")
parser.add_option(
    "--hs",
    "--house_size",
    dest="house_size",
    default=defaults.house_size,
    help="The total square footage of home"
)
parser.add_option(
    "--f",
    "--file",
    dest="file_name",
    default=defaults.rooms_file,
    help="Name of csv file containing deets"
)