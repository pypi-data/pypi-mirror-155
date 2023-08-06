from typing import Any
from typing import Dict


def convert_raw_resource_group_to_present(
    hub,
    resource: Dict,
    idem_resource_name: str,
    resource_group_name: str,
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
        resource_id: Azure Resource Group id.

    Returns:
        A dict that contains the parameters that match the present function's input format.
    """
    resource_translated = {
        "name": idem_resource_name,
        "resource_id": resource_id,
        "resource_group_name": resource_group_name,
        "location": resource["location"],
    }
    if "tags" in resource:
        resource_translated["tags"] = resource["tags"]
    return resource_translated


def convert_present_to_raw_resource_group(
    hub,
    location: str,
    tags: Dict = None,
):
    """
    Giving some present function inputs, generate a payload that can be used during PUT operation to Azure. Any None
    value input will be ignored, unless this parameter is a required input parameter.

    Args:
        hub: The redistributed pop central hub.
        location: Resource location.
        tags: Resource tags.

    Returns:
        A dict in the format of an Azure PUT operation payload.
    """
    payload = {"location": location}
    if tags is not None:
        payload["tags"] = tags
    return payload
