"""
Util objects
"""
import os
from string import Formatter

str_formater = Formatter()


def field_names_of_format_string(format_string):
    return list(
        dict.fromkeys(
            fname for _, fname, _, _ in str_formater.parse(format_string) if fname
        )
    )


# TODO: Replace with subprocess (need to change string into list for that!)
def execute_command(command_string):
    stream = os.popen(command_string)
    output = stream.read()
    return output
