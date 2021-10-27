from re import sub
import json


def jprint(dictionary):
    print(json.dumps(dictionary, indent=2))


def camel_case(string: str) -> str:
    """
    Return camelCase of a given string

    :param string: the string to be converted
    :return: the string in camelCase
    :rtype: str
    """
    string = sub(r"(_|-)+", " ", string).title().replace(" ", "")
    return ''.join([string[0].lower(), string[1:]])
