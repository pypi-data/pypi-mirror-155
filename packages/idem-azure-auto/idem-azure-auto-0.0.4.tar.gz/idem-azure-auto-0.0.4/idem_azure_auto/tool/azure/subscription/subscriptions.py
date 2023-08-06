from typing import Any
from typing import Dict


def convert_raw_attach_subscription_to_present(
    hub,
    resource: Dict,
    idem_resource_name: str,
    management_group_id: str,
    subscription_id: str,
    resource_id: str,
) -> Dict[str, Any]:
    """
    Giving an existing resource state and desired state inputs, generate a dict that match the format of
     present input parameters.

    Args:
        hub: The redistributed pop central hub.
        resource: An existing attached management group subscription state from Azure. This is usually a GET operation response.
        idem_resource_name: The Idem name of the management group subscription.
        management_group_id: Management Group ID.
        subscription_id: Subscription ID which needs to be attached to MG.
        resource_id: Azure Management group subscription association ID.

    Returns:
        A dict that contains the parameters that match the present function's input format.
    """
    resource_translated = {
        "name": idem_resource_name,
        "resource_id": resource_id,
        "management_group_id": management_group_id,
        "subscription_id": subscription_id,
    }
    if management_group_id is None:
        resource_translated["management_group_id"] = resource.get("tenantId")
    return resource_translated


def convert_present_to_raw_subscription(
    hub,
    billing_scope: str = None,
    display_name: str = None,
    workload: str = None,
):
    """
    Giving some present function inputs, generate a payload that can be used during PUT operation to Azure. Any None
    value input will be ignored, unless this parameter is a required input parameter.

    Args:
        hub: The redistributed pop central hub.
        billing_scope: billing scope associated with billing account id and enrollment account id to create subscription
        display_name: Display name of subscription
        workload: Workload type for subscription which can be Production/DevTest

    Returns:
        A dict in the format of an Azure PUT operation payload.
    """
    payload = {
        "properties": {
            "billingScope": billing_scope,
            "DisplayName": display_name,
            "Workload": workload,
        }
    }

    if billing_scope is not None:
        payload["properties"]["billingScope"] = billing_scope
    if display_name is not None:
        payload["properties"]["DisplayName"] = display_name
    if workload is not None:
        payload["properties"]["Workload"] = workload
    return payload


def convert_raw_subscription_to_present(
    hub,
    resource: Dict,
    idem_resource_name: str,
    resource_id: str,
    alias: None,
    display_name: None,
    subscription_id: None,
) -> Dict[str, Any]:
    """
    Giving an existing resource state and desired state inputs, generate a dict that match the format of
     present input parameters.

    Args:
        hub: The redistributed pop central hub.
        resource: An existing resource state from Azure. This is usually a GET operation response.
        idem_resource_name: The Idem name of the resource.
        alias: Alias for subscription
        display_name: Display name of subscription
        subscription_id: Unique subscription id
        resource_id: Azure subscription resource id.

    Returns:
        A dict that contains the parameters that match the present function's input format.
    """
    resource_translated = {
        "name": idem_resource_name,
        "resource_id": resource_id,
        "alias": alias,
        "display_name": display_name,
        "subscription_id": subscription_id,
    }

    if display_name is None:
        resource_translated["display_name"] = resource.get("displayName")
    if subscription_id is None:
        properties = resource.get("properties")
        if properties:
            resource_translated["subscription_id"] = properties.get("subscriptionId")
        else:
            resource_translated["subscription_id"] = resource.get("subscriptionId")
    return resource_translated
