def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in [x for x in dict_args if isinstance(x, dict)]:
        result.update(dictionary)
    return result