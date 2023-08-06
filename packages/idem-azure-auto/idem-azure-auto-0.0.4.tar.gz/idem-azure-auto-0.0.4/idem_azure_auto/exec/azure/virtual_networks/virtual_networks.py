import copy
from typing import Any
from typing import Dict


def update_virtual_network_payload(
    hub, existing_payload: Dict[str, Any], new_values: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Giving an existing resource state and desired state inputs, generate an updated payload, which can be used by
     PUT operation to update a resource on Azure.

    Args:
        hub: The redistributed pop central hub.
        existing_payload: An existing resource state from Azure. This is usually a GET operation response.
        new_values: A dictionary of desired state values. If any property's value is None,
         this property will be ignored. This is to match the behavior when a present() input is a None, Idem does not
         do an update.

    Returns:
        A result dict.
        result: True if no error occurs during the operation.
        ret: An updated payload that can be used to call PUT operation to update the resource. None if no update on all values.
        comment: A messages list.
    """
    result = {"result": True, "ret": None, "comment": []}
    is_updated = False
    new_payload = copy.deepcopy(existing_payload)
    if (new_values.get("tags") is not None) and (
        existing_payload.get("tags") != new_values.get("tags")
    ):
        new_payload["tags"] = new_values["tags"]
        is_updated = True
    existing_properties = existing_payload["properties"]
    if (new_values.get("address_space") is not None) and (
        set(new_values["address_space"])
        != set(existing_properties["addressSpace"]["addressPrefixes"])
    ):
        new_payload["properties"]["addressSpace"]["addressPrefixes"] = new_values[
            "address_space"
        ]
        is_updated = True
    if (new_values.get("bgp_communities") is not None) and (
        new_values["bgp_communities"] != existing_properties.get("bgpCommunities")
    ):
        new_payload["properties"]["bgpCommunities"] = new_values.get("bgp_communities")
        is_updated = True
    if (new_values.get("flow_timeout_in_minutes") is not None) and (
        new_values["flow_timeout_in_minutes"]
        != existing_properties.get("flowTimeoutInMinutes")
    ):
        new_payload["properties"]["flowTimeoutInMinutes"] = new_values.get(
            "flow_timeout_in_minutes"
        )
        is_updated = True
    if is_updated:
        result["ret"] = new_payload
    return result
