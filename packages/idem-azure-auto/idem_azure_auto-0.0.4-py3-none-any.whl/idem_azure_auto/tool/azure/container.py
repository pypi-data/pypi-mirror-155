def _is_within(parent, o, ignore: set):
    """
    Determine of an object is within a parent object.
    :param parent: The object in which o hopefully exists.
    :param o: The object to find in parent.
    :param ignore: A set of keys to ignore in parent.
    return: True if o is within parent somewhere. False otherwise.
    """
    if not isinstance(parent, type(o)):
        return False
    elif isinstance(o, dict):
        return _is_within_dict(parent, o, ignore)
    else:
        return parent == o


def _is_within_dict(parent, o, ignore: set):
    """
    Determine of an object is within a parent dict object.
    :param parent: The object in which o hopefully exists.
    :param o: The object to find in parent.
    :param ignore: A set of keys to ignore in parent.
    return: True if o is within parent somewhere. False otherwise.
    """
    ret = False
    for k, v in o.items():
        if k in ignore:
            ret = True
            break
        elif k in parent and parent[k] == v:
            ret = True
            break
    return ret


def get_from_list(hub, parent, o):
    """
    Returns the first object found in parent that contains o, None if no object is found.
    :param hub: The redistributed pop central hub. This is required in
    Idem, so while not used, must appear.
    :param parent: An iterable object to search for o.
    :param o: An object the values of which must exist in one of the iterables.

    For example:

    The subset:

    { name: "my_object" }

    exists within (and would be returned)

    [
        { name: "not_my_object", something_else: "not the other thing" }
        { name: "my_object", something_else: "some other thing"},
    ]
    """
    ret = None

    for item in parent:
        if isinstance(item, dict):
            if _is_within(item, o, set()):
                ret = item
                break
        else:
            hub.log.warning(f"Item {str(item)} should be a dict. Skipping this item.")

    return ret
