from collections import OrderedDict
from typing import Dict


def get_parameter_value(hub, uri: str, parameters: OrderedDict) -> list:
    """
    Generate a list of pairs of uri parameter and its value. And convert uri parameters to expected key used in sls files
    For example /virtualNetworks/virtual-network-name/subnets/subnet-name} will output
    [{"virtualNetworks": "virtual-network-name"}, {"subnets": "subnet-name"}]
    :param hub: The redistributed pop central hub. This is required in Idem, so while not used, must appear.
    :param uri: the uri
    :param parameters: parameters to search through the uri.
    For example: OrderedDict({"virtualNetworks": "virtual_network_name"})
    """
    ret = []
    uri_values = uri.split("/")
    for parameter_key, parameter_value in parameters.items():
        if parameter_key in uri_values:
            uri_index = uri_values.index(parameter_key)
            # Convert parameters from camel case to snake case
            ret.append({parameter_value: uri_values[uri_index + 1]})
    return ret


def get_parameter_value_in_dict(hub, uri: str, parameters: OrderedDict) -> Dict:
    """
    Generate a list of pairs of uri parameter and its value. And convert uri parameters to expected key used in sls files
    For example /virtualNetworks/virtual-network-name/subnets/subnet-name} will output
    {"virtualNetworks": "virtual-network-name", "subnets": "subnet-name"}
    :param hub: The redistributed pop central hub. This is required in Idem, so while not used, must appear.
    :param uri: the uri
    :param parameters: parameters to search through the uri.
    For example: OrderedDict({"virtualNetworks": "virtual_network_name"})
    """
    ret = {}
    uri_values = uri.split("/")
    for parameter_key, parameter_value in parameters.items():
        if parameter_key in uri_values:
            uri_index = uri_values.index(parameter_key)
            # Convert parameters from camel case to snake case
            ret[parameter_value] = uri_values[uri_index + 1]
    return ret
