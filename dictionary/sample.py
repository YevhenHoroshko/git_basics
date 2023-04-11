#!/usr/bin/env python3

"""Script demonstraits some usefull functions for work with dictionaries.

Functions:
- union, intersection, difference, symmetric difference of dictionaries
- sort dictionary by keys/values in different orders
- swap dictionary
"""

from timeit import timeit

import functions as fnc

sample_dict1 = {'c': 1, 'y': 6, 'a': 5, 'x': 2, 'd': 3}
sample_dict2 = {'x': 2, 'b': 7, 't': 7, 'y': 6}

print('\nHi! I would like to demonstrate you a list of '
      'useful functions to work with dictionaries.\n'
      '\nAs input data we will use next dictionaries:'
      f'\n\tdictionary A: {sample_dict1}\n\tdictionary B: {sample_dict2}\n')

print('\033[1m' + '\033[93m' + '\nSets of dictionaries:\n\n' + '\033[0m'
      f'  Union A | B: \t\t\t{fnc.dict_union(sample_dict1, sample_dict2)}\n'
      f'  Intersection A & B: \t\t{fnc.dict_intersection(sample_dict1, sample_dict2)}\n'
      f'  Difference A - B: \t\t{fnc.dict_difference(sample_dict1, sample_dict2)}\n'
      f'  Difference B - A: \t\t{fnc.dict_difference(sample_dict2, sample_dict1)}\n'
      f'  Symmetric differrence A ^ B:  {fnc.dict_symm_difference(sample_dict1, sample_dict2)}\n')

order = True

print('\033[1m' + '\033[93m' + '\nSort dictionary:\n\n' + '\033[0m'
      '\033[96m' + '\033[93m' + '  Ascending order...\n' + '\033[0m'
      f'    Sort by keys: \t\t{fnc.dict_sort_by_key(sample_dict1)}\n'
      f'    Sort by values: \t\t{fnc.dict_sort_by_values(sample_dict1)}\n\n'
      '\033[96m' + '\033[93m' + '  Descending order...\n' + '\033[0m'
      f'    Sort by keys: \t\t{fnc.dict_sort_by_key(sample_dict1, order)}\n'
      f'    Sort by values: \t\t{fnc.dict_sort_by_values(sample_dict1, order)}\n')

dirc_swap_for = 'fnc.dict_swap_with_for(sample_dict1)'
dirc_swap_zip = 'fnc.dict_swap_with_zip(sample_dict1)'

print('\033[1m' + '\033[93m' + '\nSwap dictionary:\n\n' + '\033[0m'
      '\033[96m' + '\033[93m' + '  Dictionary with unique values...\n' + '\033[0m'
      f'    for loop:   \t\t\t{fnc.dict_swap_with_for(sample_dict1)}\n'
      f'       run time: {round(timeit(stmt=dirc_swap_for, globals=globals()), 3)} sec\n'
      f'    zip method: \t\t\t{fnc.dict_swap_with_zip(sample_dict1)}\n'
      f'       run time: {round(timeit(stmt=dirc_swap_zip, globals=globals()), 3)} sec\n')

print('\033[96m' + '\033[93m' + '  Dictionary with not unique values...\n' + '\033[0m')
print(f'    For loop:   \t\t\t{fnc.dict_swap_with_for(sample_dict2)}\n'
      f'    Zip method: \t\t\t{fnc.dict_swap_with_zip(sample_dict2)}\n')


if __name__ == '__main__':
    pass
