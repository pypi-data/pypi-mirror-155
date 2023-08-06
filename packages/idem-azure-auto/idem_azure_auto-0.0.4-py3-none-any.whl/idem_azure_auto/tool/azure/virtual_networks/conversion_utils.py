from typing import Any
from typing import Dict
from typing import List


def convert_raw_virtual_network_to_present(
    hub,
    resource: Dict,
    idem_resource_name: str,
    resource_group_name: str,
    virtual_network_name: str,
    resource_id: str,
) -> Dict[str, Any]:
    """
    Giving an existing resource state and desired state inputs, generate a dict that match the format of
     present input parameters.

    Args:
        hub: The redistributed pop central hub.
        resource: An existing resource state from Azure. This is usually a GET operation response.
        idem_resource_name: The Idem name of the resource.
        resource_group_name: Azure Resource Group name.
        virtual_network_name: Azure Virtual Network resource name.
        resource_id: Azure Virtual Network resource id.

    Returns:
        A dict that contains the parameters that match the present function's input format.
    """
    resource_translated = {
        "name": idem_resource_name,
        "resource_id": resource_id,
        "resource_group_name": resource_group_name,
        "virtual_network_name": virtual_network_name,
        "location": resource["location"],
    }
    if "tags" in resource:
        resource_translated["tags"] = resource["tags"]
    properties = resource.get("properties")
    if properties:
        properties_parameters = {
            "bgpCommunities": "bgp_communities",
            "flowTimeoutInMinutes": "flow_timeout_in_minutes",
            "provisioningState": "provisioning_state",
        }
        for parameter_raw, parameter_present in properties_parameters.items():
            if parameter_raw in properties:
                resource_translated[parameter_present] = properties.get(parameter_raw)
        resource_translated["address_space"] = properties["addressSpace"][
            "addressPrefixes"
        ]
    return resource_translated


def convert_present_to_raw_virtual_network(
    hub,
    address_space: List,
    location: str,
    bgp_communities: str = None,
    flow_timeout_in_minutes: int = None,
    tags: Dict = None,
):
    """
    Giving some present function inputs, generate a payload that can be used during PUT operation to Azure. Any None
    value input will be ignored, unless this parameter is a required input parameter.

    Args:
        hub: The redistributed pop central hub.
        address_space: An array of IP address ranges that can be used by subnets of the virtual network.
        location: Resource location. Update this field will result in resource re-creation.
        bgp_communities: Bgp Communities sent over ExpressRoute with each route corresponding to a prefix in this VNET.
        flow_timeout_in_minutes: The FlowTimeout value (in minutes) for the Virtual Network
        tags: Resource tags.

    Returns:
        A dict in the format of an Azure PUT operation payload.
    """
    payload = {
        "location": location,
        "properties": {"addressSpace": {"addressPrefixes": address_space}},
    }
    if tags is not None:
        payload["tags"] = tags
    if bgp_communities is not None:
        payload["properties"]["bgpCommunities"] = bgp_communities
    if flow_timeout_in_minutes is not None:
        payload["properties"]["flowTimeoutInMinutes"] = flow_timeout_in_minutes
    return payload
