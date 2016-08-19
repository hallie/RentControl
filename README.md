## Mission: Control the Rent
Here's a pretty simple algorithm for determining how much rent would change when people come in and out of the house.

##How to Use
To run with defaults, simply go:
```bash
python rent_calculator.py
```

There are currently `3` optional parameters you can add:
- `--bld` or `--bad_lighting_deduct`, which is the amount off people get in rooms with bad lighting (ex. windows that don't open, or are very small/don't bring in natural lighting) (defaults to `100`)
- `--rd` or `--round_dollar`, which takes all of the extra cents lost in rounding the final numbers to dollars, and dumps them on the person/people paying the least rent. (defaults to `true`)
- `--cw` or `--common_weight`, the decicimal representing the percentage of the cost of the common space that gets taken into account when calculating overall rent. (defaults to `.5`)
- `--cas` or `--calculate_as_singles`, shows what the price would be if all rooms were singles.

Example:
```bash
python rent_calculator.py --bld=150 --rd=False --cw=.7 --cas=True
```
This would raise the bad-lighting deduction to $150, set 70% of the common area cost as a default cost per person, doesn't round the cents, and assumes there is only one person per room.