import sys
import urllib

def decode(i=''):
    """
    decode a string to UTF-8
    Args:
        i: string to decode

    Returns: decoded string

    """
    try:
        if isinstance(i, str):
            return i.decode('utf-8')
        elif isinstance(i, unicode):
            return i
    except:
        return ''

def parseParameters():
    """Parses a parameter string starting at the first ? found in inputString
    
    Argument:
    input_string: the string to be parsed, sys.argv[2] by default
    
    Returns a dictionary with parameter names as keys and parameter values as values
    """
    input_string = ''
    if sys.argv[2]:
        input_string = sys.argv[2]

    parameters = {}
    p1 = input_string.find('?')
    if p1 >= 0:
        split_parameters = input_string[p1 + 1:].split('&')
        for name_value_pair in split_parameters:
            if (len(name_value_pair) > 0) & ("=" in name_value_pair):
                pair = name_value_pair.split('=')
                key = pair[0]
                value = decode(urllib.unquote_plus(pair[1]))
                parameters[key] = value
    return parameters