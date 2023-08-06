import copy
from typing import Any
from typing import Dict


def update_policy_definition_payload(
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
    existing_properties = existing_payload["properties"]
    if (new_values.get("display_name") is not None) and (
        new_values["display_name"] != existing_properties.get("displayName")
    ):
        new_payload["properties"]["displayName"] = new_values.get("display_name")
        need_update = True
    if (new_values.get("description") is not None) and (
        new_values["description"] != existing_properties.get("description")
    ):
        new_payload["properties"]["description"] = new_values.get("description")
        need_update = True
    if (new_values.get("mode") is not None) and (
        new_values["mode"] != existing_properties.get("mode")
    ):
        new_payload["properties"]["mode"] = new_values.get("mode")
        need_update = True
    if (new_values.get("policy_rule") is not None) and (
        new_values["policy_rule"] != existing_properties.get("policyRule")
    ):
        new_payload["properties"]["policyRule"] = new_values.get("policy_rule")
        need_update = True
    if (new_values.get("metadata") is not None) and (
        new_values["metadata"] != existing_properties.get("metadata")
    ):
        new_payload["properties"]["metadata"] = new_values.get("metadata")
        need_update = True
    # ToDo: to use DeepDiff to compare two Dict once NamespaceDict can be converted to Dict
    if (new_values.get("parameters") is not None) and (
        new_values["parameters"] != existing_properties.get("parameters")
    ):
        new_payload["properties"]["parameters"] = new_values.get("parameters")
        need_update = True
    if need_update:
        result["ret"] = new_payload
    return result


def convert_raw_policy_definition_to_present(
    hub,
    resource: Dict,
    idem_resource_name: str,
    policy_definition_name: str,
    resource_id: str,
) -> Dict[str, Any]:
    """
    Giving an existing resource state and desired state inputs, generate a dict that match the format of
     present input parameters.

    Args:
        hub: The redistributed pop central hub.
        resource: An existing resource state from Azure. This is usually a GET operation response.
        idem_resource_name: The Idem name of the resource.
        policy_definition_name: Azure Policy Definition name.
        resource_id: Azure Policy Definition resource id.

    Returns:
        A dict that contains the parameters that match the present function's input format.
    """
    resource_translated = {
        "name": idem_resource_name,
        "resource_id": resource_id,
        "policy_definition_name": policy_definition_name,
    }
    properties = resource.get("properties")
    if properties:
        properties_parameters = {
            "description": "description",
            "displayName": "display_name",
            "metadata": "metadata",
            "mode": "mode",
            "policyRule": "policy_rule",
            "policyType": "policy_type",
            "parameters": "parameters",
        }
        for parameter_raw, parameter_present in properties_parameters.items():
            if parameter_raw in properties:
                resource_translated[parameter_present] = properties.get(parameter_raw)
    return resource_translated


def convert_present_to_raw_policy_definition(
    hub,
    policy_type: str,
    description: str,
    display_name: str,
    mode: str,
    metadata: Dict = None,
    policy_rule: Dict = None,
    parameters: Dict = None,
):
    """
    Giving some present function inputs, generate a payload that can be used during PUT operation to Azure. Any None
    value input will be ignored, unless this parameter is a required input parameter.

    Args:
        hub: The redistributed pop central hub.
        policy_type: The policy type. Possible values are BuiltIn, Custom and NotSpecified.
        description: The description of the policy definition.
        display_name: The display name of the policy definition.
        mode: The policy mode that allows you to specify which resource types will be evaluated. Some examples are All, Indexed, Microsoft.KeyVault.Data.
        metadata: The metadata for the policy definition.
        policy_rule: The policy rule for the policy definition.
        parameters: Parameters for the policy definition.
    Returns:
        A dict in the format of an Azure PUT operation payload.
    """
    payload = {
        "properties": {"displayName": display_name, "policyType": policy_type},
    }
    if description is not None:
        payload["properties"]["description"] = description
    if metadata is not None:
        payload["properties"]["metadata"] = metadata
    if mode is not None:
        payload["properties"]["mode"] = mode
    if policy_rule is not None:
        payload["properties"]["policyRule"] = policy_rule
    if parameters is not None:
        payload["properties"]["parameters"] = {}
        payload["properties"]["parameters"] = parameters
    return payload
