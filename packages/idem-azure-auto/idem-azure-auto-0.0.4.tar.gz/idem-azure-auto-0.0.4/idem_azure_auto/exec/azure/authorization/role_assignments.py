from collections import OrderedDict


async def get(hub, ctx, name: str, resource_id: str):
    result = dict(comment=[], ret=None, result=True)
    if resource_id is None or name is None:
        result["result"] = False
        result["comment"].append(
            "name and resource_id cannot be None for azure.authorization.role_assignments get()"
        )
        return result
    before = await hub.exec.request.json.get(
        ctx,
        url=f"{hub.exec.azure.URL}/{resource_id}?api-version=2015-07-01",
        success_codes=[200],
    )
    if not before["result"]:
        result["comment"] = before["comment"]
        if before.get("status") == 404:
            return result
        result["result"] = False
        return result
    uri_parameters = OrderedDict({"roleAssignments": "role_assignment_name"})
    uri_parameter_values = hub.tool.azure.uri.get_parameter_value_in_dict(
        resource_id, uri_parameters
    )
    result[
        "ret"
    ] = hub.tool.azure.authorization.role_assignments.convert_raw_role_assignments_to_present(
        resource=before["ret"],
        idem_resource_name=name,
        role_assignment_name=uri_parameter_values["role_assignment_name"],
        resource_id=resource_id,
    )
    return result
