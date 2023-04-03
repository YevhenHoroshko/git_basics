#!/usr/bin/env python3

"""Calculate deposit percent yield based on time period.

Imagine your friend wants to put money on a deposit.
He has got many offers from different banks:
- First bank declares +A% each day;
- Second bank promises +B% each month;
- Third bank offers +C% by the end of the year;
- The 4th bank promotes +D% in a 10-year term;
- ... and so on ...

Your friend gets a terrible headache calculating all this stuff,
and asks you to help checking everything. You quickly realize
it is a common task and having a simple script is a great idea.

Let's implement this.

A simplified task:
Given the SUM amount of money, and PERCENT yield promised in a
FIXED_PERIOD of time, calculate the TOTAL equivalent of money
in a SET_PERIOD of time.

Math formula:
p = PERCENT / 100
TOTAL = SUM * ((1 + p) ** (SET_PERIOD / FIXED_PERIOD))
"""


# TODO: add lines to calculate yields for some common periods
#       of time (e.g. 1 month, 1 year, 5 years, 10 years)
# TODO: change the script to output the 1-year percent yield
#       as well
# TODO: (extra) Output only percents if the initial SUM is
#       not known at the moment the script is run


USAGE = """USAGE: {script} initial_sum percent fixed_period set_period

\tCalculate deposit yield. See script source for more details.
"""
USAGE = USAGE.strip()

MONTH = 30.44
YEAR = 365.24
FIVE_YEAR = 1826.21
TEN_YEAR = 3652.42


def deposit(percent, fixed_period, set_period, initial_sum = None):
    """Calculate deposit yield."""
    per = percent / 100
    growth = [(1 + per) ** (set_period / fixed_period),
    	      (1 + per) ** (MONTH / fixed_period),
    	      (1 + per) ** (YEAR / fixed_period),
              (1 + per) ** (FIVE_YEAR / fixed_period),
    	      (1 + per) ** (TEN_YEAR / fixed_period)]
    return [initial_sum * g for g in growth] if initial_sum else growth


def main(args):
    """Gets called when run as a script."""
    if len(args) != 4 + 1:
        if len(args) == 4:
            percent, fixed_period, set_period = map(float, args[1:])
            res = deposit(percent, fixed_period, set_period)
            print(f'Percent for setted period: {res[0]}\nOne year percent: {res[2]}\n')
            exit()
        exit(USAGE.format(script=args[0]))

    args = args[1:]
    percent, fixed_period, set_period, initial_sum = map(float, args)

    # same as
    # initial_sum = float(args[0])
    # percent = float(args[1])
    # ...

    res = deposit(percent, fixed_period, set_period, initial_sum)
    print(f'Percent yield for setted period: {res[0]}\nOne year percent yield: {res[2]}\n')


if __name__ == '__main__':
    import sys

    main(sys.argv)
