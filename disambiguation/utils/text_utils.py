def url_safe_text(input_string):
    """
    returns a string in a URL safe alphanumeric form without spaces
    """
    return ''.join(e for e in input_string if e.isalnum()).replace(' ', '')