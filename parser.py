"""
Title: UFW Log Parser
Author: Darius Strasel @dariusstrasel
Description: takes an input logfile and returns all the lines as a Python dictionary.
"""

import datetime
import re
import json


def _cleanse_line(line):
    """Massages and removes unparseable elements from a log line."""
    new_line = line

    # Remove blank spaces from within bracket, to preserve structure.
    new_line = new_line.replace("[ ", "[")

    # Remove brackets
    new_line = new_line.replace("[", "")
    new_line = new_line.replace("]", "")
    # Remove newlines
    new_line = new_line.replace("\n", "")
    # Remove blank space at end of line
    new_line = new_line.strip()

    return new_line


def _tokenize_line(line):
    """Splits a line into a normalized data structure."""

    new_line = _cleanse_line(line)  # Removes impurities.

    split_line = new_line.split(' ')

    # Keys which identify the index of static flags.
    MONTH = 0
    DAY = 1
    TIME = 2
    HOSTNAME = 3
    BLOCK_TYPE = 4
    UPTIME = 5
    TYPE = (6, 7)
    REMAINDER = split_line[8:len(split_line)]

    log_map = {
        'month': split_line[MONTH],
        'day': split_line[DAY],
        'time': split_line[TIME],
        'hostname': split_line[HOSTNAME],
        'block_type': split_line[BLOCK_TYPE][:-1],  # Remove trailing ':'
        'uptime': split_line[UPTIME],
        'type': split_line[TYPE[0]] + split_line[TYPE[1]]
    }

    # Convert the remaining key-value pairs and map them to log_map.
    remainder = [_convert_to_key_value_pair(key) for key in REMAINDER]

    for key in remainder:
        _add_dict1_to_dict2(key, log_map)

    print(log_map)
    return log_map


def _add_dict1_to_dict2(dict_one, dict_two):
    """Merge one dictionary into a second dictionary."""
    if dict_one and dict_two:
        for key in dict_one:
            dict_two[key] = dict_one[key]


def _convert_to_key_value_pair(string_pair):
    """Takes input string e.g. "key=value" and converts into a Python dictionary."""
    new_string = string_pair.split("=")
    KEY = 0
    VALUE = 1

    # Single length pair indicates Null value
    if len(new_string) == 1:
        result = {new_string[KEY]: None}
    else:
        result = {new_string[KEY]: new_string[VALUE]}

    return result


def _find_illegal_keys(line):
    """Checks for patterns of text which match: SYN URGP=0"""
    regex = r"\s(\w+\s\w+=\w+)"
    matches = re.findall(regex, line)
    return matches


def _dump_to_JSON(dictionary_input):
    """Saves a Python dictionary to a JSON file."""
    with open('result.json', 'w') as fp:
        return json.dump(dictionary_input, fp)

def _get_dict_keys(parser_results):
    """Returns a list of all the keys found in the argument parser result; helps to define data model of logfile."""
    results = parser_results
    existing_keys = []
    for result in results:
        for key in list(result.keys()):
            if key not in existing_keys:
                existing_keys.append(key)
        else:
            pass
    print(existing_keys)


def process_file(file_name):
    """Main function used to starr parser. Accepts filepath of file to process."""
    result = []
    try:
        with open(file_name, 'r+') as logfile:
            print("Opening: %s" % file_name)
            start = datetime.datetime.now()
            for line in logfile:
                    result.append(_tokenize_line(line))
            end = datetime.datetime.now()
            print("Start: %s, End: %s" % (start, end))
    except IOError:
        print("File is locked.")
        raise
    return result

if __name__ == "__main__":
    process_file("./ufw.log")
