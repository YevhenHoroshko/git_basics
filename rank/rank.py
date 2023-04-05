#!/usr/bin/env python3

"""Script receives pairs of name:salary values as arguments: 
./rank.py --inv john:1000.5 bob:850 klaus:1100

The main criteria for script output:
- sort data in descending order by default, or in
  ascending order if the --inv argument is passed
- names must begin with a capital letter
- if the name is repeated, the salaries are recorded
  in the form of a range (from minimum to maximum)
- table format for output, where the width of the
  name field is set by the longest name from the list
"""

USAGE = """USAGE: {script} [--inv] name_1:salary [... name_n:salary]

\t--inv - sort data in ascending order.
"""
USAGE = USAGE.strip()


def determ_sort_order(data):
    """Determine a sort order: ascending or descending"""
    
    inv = True                 # descending order
    if '--inv' in data:
        inv = False            # ascending order
        data.remove('--inv')
    return inv, data


def form_salaries(data):
    """Store names and salaries in dictionary"""
    
    salaries = {}

    for pair in data:
        name, salary = pair.split(':')
        name = name.title()    # Capital letter in name
        salary = round(float(salary),  2)

        if name in salaries:   # Add salary to the list of salaries for this name
            salaries[name].append(salary)
        else:                  # Add salary for this name
            salaries[name] = [salary]
    
    return salaries


def print_salaries_table(salaries, sorted_names, max_name_len):
    """Print salaries in a table"""
    
    print(f"{'Name':<{max_name_len}} | Salary")
    print("-" * max_name_len + "-|-------")
    for name in sorted_names:
        salary_list = salaries[name]
        if len(salary_list) > 1:
            salary_range = f"${min(salary_list)} ... ${max(salary_list)}"
        else: 
            salary_range = f"${salary_list[0]}"
        print(f"{name:<{max_name_len}} | {salary_range}")
    

def main(args):
    """Gets called when run as a script."""
    if len(args) < 2:
        exit(USAGE.format(script=args[0]))
    
    sort_order, args = determ_sort_order(args[1:])
    salaries = form_salaries(args)
    max_name_len = max(len(name) for name in salaries)
    sorted_names = sorted(salaries.keys(), reverse=sort_order)
    print_salaries_table(salaries, sorted_names, max_name_len)
 
 
if __name__ == '__main__':
    import sys

    main(sys.argv)
