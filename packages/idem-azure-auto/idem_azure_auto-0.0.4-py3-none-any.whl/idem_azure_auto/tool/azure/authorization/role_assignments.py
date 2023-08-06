from typing import Any
from typing import Dict


def convert_raw_role_assignments_to_present(
    hub,
    resource: Dict,
    idem_resource_name: str,
    role_assignment_name: str,
    resource_id: str,
) -> Dict[str, Any]:
    """
    Giving an existing resource state and desired state inputs, generate a dict that match the format of
     present input parameters.

    Args:
        hub: The redistributed pop central hub.
        resource: An existing resource state from Azure. This is usually a GET operation response.
        idem_resource_name: The Idem name of the resource.
        role_assignment_name: Azure role assignment resource name.
        resource_id: Role assignment resource id on Azure.

    Returns:
        A dict that contains the parameters that match the present function's input format.
    """
    resource_translated = {
        "name": idem_resource_name,
        "resource_id": resource_id,
        "role_assignment_name": role_assignment_name,
    }
    properties = resource.get("properties")
    if properties:
        properties_parameters = {
            "roleDefinitionId": "role_definition_id",
            "principalId": "principal_id",
            "scope": "scope",
        }
        for parameter_raw, parameter_present in properties_parameters.items():
            if parameter_raw in properties:
                resource_translated[parameter_present] = properties[parameter_raw]
    return resource_translated


def convert_present_to_raw_role_assignments(
    hub,
    role_definition_id: str = None,
    principal_id: int = None,
) -> Dict[str, Any]:
    """
    Giving some present function inputs, generate a payload that can be used during PUT operation to Azure. Any None
    value input will be ignored, unless this parameter is a required input parameter.

    Args:
        hub: The redistributed pop central hub.
        role_definition_id: The role definition ID used in the role assignment.
        principal_id: The principal ID assigned to the role. This maps to the ID inside the Active Directory. It can point to a user, service principal, or security group.

    Returns:
        A dict in the format of an Azure PUT operation payload.
    """
    payload = {
        "properties": {
            "roleDefinitionId": role_definition_id,
            "principalId": principal_id,
        }
    }
    return payload
