#!/usr/bin/env python3

"""Script contains a list of useful functions for work with dictionaries.

Functions:
- union, intersection, difference, symmetric difference
- sort dictionary by keys/values in different orders
- swap dictionary
"""


def dict_union(dict1, dict2):
    """Union of sets of two dictionries."""
    return dict(dict1.items() | dict2.items())


def dict_intersection(dict1, dict2):
    """Intersection of sets of two dictionries."""
    return dict(dict1.items() & dict2.items())


def dict_difference(dict1, dict2):
    """Difference of sets of two dictionries."""
    return dict(dict1.items() - dict2.items())


def dict_symm_difference(dict1, dict2):
    """Difference of sets of two dictionries."""
    return dict(dict1.items() ^ dict2.items())


def dict_sort_by_key(dictionary, order=False):
    """Sort dictionary by keys in specific order."""
    sorted_keys = sorted(dictionary.keys(), reverse=order)
    return {key: dictionary[key] for key in sorted_keys}


def dict_sort_by_values(dictionary, order=False):
    """Sort dictionary by keys in specific order."""
    sorted_values = sorted(dictionary, key=lambda key: (dictionary[key], key), reverse=order)
    return {key: dictionary[key] for key in sorted_values}


def dict_swap_with_for(dictionary):
    """Swap keys and values in dictionary."""
    try:
        # Check the uniqueness of dictionary valeus
        if len(set(dictionary.values())) != len(dictionary):
            raise ValueError('Dictionary values are not unique')
    except Exception as error:
        print('Caught this error: \033[91m' + repr(error) + '\033[0m\n')
    else:
        return {k_value: key for key, k_value in dictionary.items()}


def dict_swap_with_zip(dictionary):
    """Swap keys and values in dictionary."""
    # Check the uniqueness of dictionary valeus
    if len(set(dictionary.values())) != len(dictionary):
        raise ValueError('\033[91mDictionary values are not unique\033[0m')
    return dict(zip(dictionary.values(), dictionary.keys()))
