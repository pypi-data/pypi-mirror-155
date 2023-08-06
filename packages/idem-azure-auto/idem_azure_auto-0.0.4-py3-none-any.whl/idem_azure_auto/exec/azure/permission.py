__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    resource_group_name: str,
    resource_provider_namespace: str,
    parent_resource_path: str,
    resource_type: str,
    resource: str,
):
    """
    https://docs.microsoft.com/en-us/rest/api/authorization/permissions/list-for-resource
    """
    subscription_id = ctx.acct.subscription_id
    return await hub.exec.request.json.get(
        ctx,
        url=f"https://management.azure.com/subscriptions/{subscription_id}/resourcegroups/{resource_group_name}/providers/{resource_provider_namespace}/{parent_resource_path}/{resource_type}/{resource}/providers/Microsoft.Authorization/permissions",
        params={"api-version": "2015-07-01"},
        success_codes=[200],
    )


async def list_(hub, ctx, resource_group_name: str):
    """
    https://docs.microsoft.com/en-us/rest/api/authorization/permissions/list-for-resource
    """
    subscription_id = ctx.acct.subscription_id
    return await hub.exec.request.json.get(
        ctx,
        url=f"https://management.azure.com/subscriptions/{subscription_id}/resourcegroups/{resource_group_name}/providers/Microsoft.Authorization/permissions",
        params={"api-version": "2015-07-01"},
        success_codes=[200],
    )
