import copy
import json
from typing import Any
from typing import Dict


def convert_raw_management_group_to_present(
    hub,
    resource: Dict,
    idem_resource_name: str,
    management_group_name: str,
    resource_id: str,
) -> Dict[str, Any]:
    """
    Giving an existing resource state and desired state inputs, generate a dict that match the format of
     present input parameters.

    Args:
        hub: The redistributed pop central hub.
        resource: An existing resource state from Azure. This is usually a GET operation response.
        idem_resource_name: The Idem name of the resource.
        management_group_name: Azure Resource Group name.
        resource_id: Azure Managment group resource id.

    Returns:
        A dict that contains the parameters that match the present function's input format.
    """
    resource_translated = {
        "name": idem_resource_name,
        "management_group_name": management_group_name,
        "resource_id": resource_id,
    }
    if type(resource) == str:
        resource = json.loads(resource)
    properties = resource.get("properties")
    if properties:
        if "displayName" in properties:
            resource_translated["display_name"] = properties["displayName"]
        if "details" in properties:
            resource_translated["parent_id"] = properties["details"]["parent"]["id"]

    return resource_translated


def convert_present_to_raw_management_group(hub, display_name: str, parent_id: str):
    """
    Giving some present function inputs, generate a payload that can be used during PUT operation to Azure. Any None
    value input will be ignored, unless this parameter is a required input parameter.

    Args:
        hub: The redistributed pop central hub.
        display_name: The management group name to be displayed
        parent_id: creates management group under this id

    Returns:
        A dict in the format of an Azure PUT operation payload.
    """
    payload = {}
    if display_name is not None or parent_id is not None:
        payload["properties"] = {}
    if display_name is not None:
        payload["properties"]["displayName"] = display_name
    if parent_id is not None:
        payload["properties"]["details"] = {"parent": {"id": parent_id}}

    return payload


def update_management_groups_payload(
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
        comment: A messages tuple.
    """
    result = {"result": True, "ret": None, "comment": []}
    need_update = False
    new_payload = copy.deepcopy(existing_payload)
    if (
        (new_values.get("parent_id") is not None)
        and (existing_payload.get("properties") is not None)
        and (existing_payload.get("properties").get("details") is not None)
        and (
            existing_payload.get("properties").get("details").get("parent") is not None
        )
        and (
            existing_payload.get("properties").get("details").get("parent").get("id")
            != new_values.get("parent_id")
        )
    ):
        new_payload["properties"]["details"]["parent"]["id"] = new_values["parent_id"]
        need_update = True
    if (new_values.get("display_name") is not None) and (
        existing_payload.get("properties").get("displayName")
        != new_values.get("display_name")
    ):
        new_payload["properties"]["displayName"] = new_values["display_name"]
        need_update = True

    if need_update:
        result["ret"] = new_payload
    return result
