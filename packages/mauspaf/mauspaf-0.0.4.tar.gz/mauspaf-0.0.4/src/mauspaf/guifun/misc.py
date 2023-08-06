import random
import string


def random_id(basestring):
    """ Generates a random id.

    In the form "`basestring`.<4randomcharacters>".

    Args:
        basestring (string): String

    Returns:
        id (string): random id.

    """
    id = basestring + '.' + ''.join(random.choices(string.ascii_lowercase
                                                   + string.digits, k=4))
    return id


def new_row(id):
    """ Generates a list with elements to initialize a new row

    In the form "`basestring`.<4randomcharacters>".

    Args:
        id (string): String

    Returns:
        list: List with default elements for new row.

    """
    new_row = ['NEW PART', id, '0', '', '', '', '', '0', '', '', '', '']
    return new_row
