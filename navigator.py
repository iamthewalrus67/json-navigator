#!/usr/bin/env python3

'''
Module for navigating through JSON files.
https://github.com/iamthewalrus67/json-navigator
'''


import sys
import json
import numbers
from termcolor import colored


def read_json_from_file(path):
    '''
    Read JSON from file.
    '''
    with open(path, 'r') as json_file:
        return json.load(json_file)


def print_options(options):
    '''
    Print possible options.
    '''
    if isinstance(options, dict):
        for key, value in options.items():
            if isinstance(value, bool):
                print(colored(key, 'yellow'), value)
            elif isinstance(value, dict):
                print(colored(key, 'red'))
            elif isinstance(value, numbers.Number):
                print(colored(key, 'blue'), value)
            elif isinstance(value, str):
                print(colored(key, 'green'), value)
            elif isinstance(value, list):
                print(colored(key, 'magenta'))
            else:
                print(colored(key, 'white'))
    elif isinstance(options, list):
        for i, value in enumerate(options):
            if isinstance(value, bool):
                print(colored(i, 'yellow'), value)
            elif isinstance(value, dict):
                print(colored(i, 'red'))
            elif isinstance(value, numbers.Number):
                print(colored(i, 'blue'), value)
            elif isinstance(value, str):
                print(colored(i, 'green'), value)
            elif isinstance(value, list):
                print(colored(i, 'magenta'))
            else:
                print(colored(i, 'white'))
        #     print(i, end='  ')
        # print()


def get_current_directory(json_dict: dict, path: str) -> tuple:
    '''
    Get current directory.

    >>> get_current_directory({"json": {"deeper_json": {"even_deeper_json": "something"}}}, "json/deeper_json")
    ({'even_deeper_json': 'something'}, 'json/deeper_json')
    '''
    current_dir = json_dict

    splitted_path = path.split('/') if not isinstance(path, int) else [path]
    splitted_path = [i for i in splitted_path if i != '']
    for i, _ in enumerate(splitted_path):
        if splitted_path[i].isnumeric():
            splitted_path[i] = int(splitted_path[i])

    for index, i in enumerate(splitted_path):
        if i == '..':
            splitted_path = [str(i) for i in splitted_path]
            dir_and_path = get_current_directory(json_dict,
                                                 '/'.join(splitted_path[:index-1]))
            current_dir = dir_and_path[0]
            splitted_path = dir_and_path[1].split('/')
            break
        try:
            current_dir = current_dir[i]
        except (TypeError, IndexError):
            raise KeyError

    splitted_path = [str(i) for i in splitted_path]
    return current_dir, '/'.join(splitted_path)


if __name__ == '__main__':
    # Get argument
    path_to_json = str(sys.argv[-1])
    json_data = read_json_from_file(path_to_json)
    current_dir = json_data
    current_path = ''

    # Main loop
    while True:
        user_input = input(current_path + '> ').split()

        if len(user_input) > 2:
            print('Wrong format')

        command = user_input[0]

        # Chow items in current directory
        if command in ('ls', 'dir'):
            print_options(current_dir)

        # Open new directory
        if command == 'cd':
            if not len(user_input) < 2:
                argument = int(
                    user_input[1]) if user_input[1].isnumeric() else user_input[1]
            else:
                argument = ''
            try:
                if str(argument).startswith('/'):
                    dir_and_path = get_current_directory(json_data, argument)
                    current_dir = dir_and_path[0]
                    current_path = dir_and_path[1]
                elif argument in ('', '/'):
                    current_dir = json_data
                    current_path = ''
                else:
                    dir_and_path = get_current_directory(
                        json_data, '/'.join([current_path, str(argument)]))
                    current_dir = dir_and_path[0]
                    current_path = dir_and_path[1]
            except KeyError:
                print('Chosen element is not a dictionary or a list')

        # Exit from program
        if command in ('exit', 'quit'):
            break
