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


def sort_order(data):
    """Determine data sort order (ascending or descending)"""
    
    inv = '--inv' not in data
    if not inv:
        data.remove('--inv')
    
    # same as:
    # inv = True                 # descending order
    # if '--inv' in data:
    #     inv = False            # ascending order
    #     data.remove('--inv')
    
    return inv, data


def form_input_data(data):
    """Forms user input data due to requirements"""
    
    slr = {}

    for pair in data:
        name, salary = pair.split(':')
        name = name.title()      # Capital letter in name
        salary = round(float(salary),  2)

        if name in slr:          # Add salary to the list of salaries for this name
            slr[name].append(salary)
        else:                    # Add salary for this name
            slr[name] = [salary]
    
    return slr


def sort_data(slr, inv):
    """Sorts input data by names or salaries in proper order"""
    
    order = 'ascending' if not inv else 'descending'
    print(f'\nSort in {order} order by names - press 1,'
          f'\nSort in {order} order by salaries - press 2.\n')
    
    choice = ''
    while choice != '1' and choice != '2':
        choice = input('Your choice: ')
        
    if choice == '1':
        sorted_data = sorted(slr.keys(), reverse=inv)
    else:
        sorted_data = {key: slr[key] for key in sorted(slr, 
                       key=lambda x: (min(slr[x]), x), reverse=inv)}
        
        # instead of '... key=lambda x: ...' you can use '... key=salaries.get ...'
    
    return sorted_data


def data_table(slr, sorted_slr, name_len, salary_len):
    """Print sorted data in a table"""
    
    print(" " + "_" * (name_len + salary_len + 5))
    print(f"| {'Name':<{name_len}} | {'Salary':<{salary_len}} |")
    print("|-" + "-" * name_len + "-|-" + "-" * salary_len + "-|")
    for name in sorted_slr:
        salary_list = slr[name]
        if len(salary_list) > 1:
            salary_range = f"${min(salary_list)} ... ${max(salary_list)}"
        else: 
            salary_range = f"${salary_list[0]}"
        print(f"| {name:<{name_len}} | {salary_range:<{salary_len}} |")
    print("|" + "_" * (name_len +1) + "_|_" + "_" * (salary_len + 1) + "|")
    

def main(args):
    """Gets called when run as a script."""
    
    if len(args) < 2:
        exit(USAGE.format(script=args[0]))
    
    # determine data sort order
    is_inv, args = sort_order(args[1:])
    
    # user data forming
    salaries = form_input_data(args)
    
    # needed for table creation
    max_name_len = max(len(name) for name in salaries)
    max_salary_len = max(len(f"${salaries[name][0]} ... ${salaries[name][-1]}") 
                         for name in salaries)
                         
    # sort data due to criterias
    sorted_data = sort_data(salaries, is_inv)
    
    # print sorted data in a table format
    data_table(salaries, sorted_data, max_name_len, max_salary_len) 


if __name__ == '__main__':
    import sys

    main(sys.argv)

