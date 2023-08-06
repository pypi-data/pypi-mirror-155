NAME_PARAMETER = {
    "default": None,
    "doc": "The identifier for this state",
    "param_type": "str",
    "required": True,
    "target": "hardcoded",
    "target_type": "arg",
}

GET_REQUEST_FORMAT = r"""
    subscription_id = ctx.acct.subscription_id
    return {{ function.hardcoded.get_function }}(
        ctx,
        url=f"{{ function.hardcoded.path }}",
        success_codes=[200],
    )
"""

LIST_REQUEST_FORMAT = r"""
    ret = dict(comment="", result=True, ret={})
    subscription_id = ctx.acct.subscription_id

    async for page_result in hub.tool.azure.request.paginate(
            ctx,
            url=f"{{ function.hardcoded.path }}",
            success_codes=[200],
    ):
        resource_list = page_result.get("value", None)
        if resource_list:
            for resource in resource_list:
                ret["ret"][resource["id"]] = resource
    return ret
"""

CREATE_REQUEST_FORMAT = r"""
    subscription_id = ctx.acct.subscription_id

    # PUT operation to create a resource
    return {{ function.hardcoded.create_function }}(
        ctx,
        url=f"{{ function.hardcoded.path }}",
        success_codes=[200, 201],
        json=parameters,
    )
"""

UPDATE_REQUEST_FORMAT = r"""
    subscription_id = ctx.acct.subscription_id

    {% if function.hardcoded.patch_parameters %}
    response_get = {{ function.hardcoded.get_function }}(
        ctx,
        url=f"{{ function.hardcoded.path }}",
        success_codes=[200],
    )

    # PATCH operation to update a resource
    patch_parameters = {{ function.hardcoded.patch_parameters }}
    existing_resource = response_get["ret"]
    new_parameters = hub.tool.azure.request.patch_json_content(patch_parameters, existing_resource, parameters)

    if force_update:
        return {{ function.hardcoded.create_function }}(
            ctx,
            url=f"{{ function.hardcoded.path }}",
            success_codes=[200, 201],
            json=new_parameters,
        )
    else:
        return {{ function.hardcoded.patch_function }}(
            ctx,
            url=f"{{ function.hardcoded.path }}",
            success_codes=[200],
            json=new_parameters,
        )

    {% else %}
    ret = dict(
        comment="No update operation on {{ function.hardcoded.resource_name }} since Azure does not have PATCH api on {{ function.hardcoded.resource_name }}",
        result=True,
        ret=None
    )

    return ret
    {% endif %}
"""

DELETE_REQUEST_FORMAT = r"""
    subscription_id = ctx.acct.subscription_id

    return {{ function.hardcoded.delete_function }}(
        ctx,
        url=f"{{ function.hardcoded.path }}",
        success_codes=[200, 202, 204],
    )
"""

PRESENT_REQUEST_FORMAT = r"""
    # TODO Please use virtual_network.py as a reference. Function input parameters need to be added manually.
    result = dict(name=name, result=True, old_state=None, new_state=None, comment=())
    subscription_id = ctx.acct.subscription_id
    if resource_id is None:
        # TODO: This resource_id is not correct and it needs to be manually fixed to the correct one
        resource_id = {{ function.hardcoded.get_function }}
    # TODO: double check if the api version here is correct or not.
    response_get = {{ function.hardcoded.get_function }}(
        ctx,
        url=f"{hub.exec.azure.URL}{resource_id}?api-version=2021-03-01",
        success_codes=[200],
    )

    if not response_get["result"]:
        if ctx.get("test", False):
            # Return a proposed state by Idem state --test
            result["new_state"] = hub.tool.azure.test_state_utils.generate_test_state(
                enforced_state={},
                # TODO Populate desired_state to match present input
                desired_state={"name": name,},
            )
            result["comment"]=("Would create azure.{{ function.hardcoded.create_ref }}",)
            return result

        if response_get["status"] == 404:
            # PUT operation to create a resource
            # TODO Populate payload, please refer to hub.tool.azure.virtual_networks.conversion_utils.convert_present_to_raw_virtual_network()
            payload = {}
            response_put = {{ function.hardcoded.create_function }}(
                ctx,
                url=f"{hub.exec.azure.URL}{resource_id}?api-version=2021-03-01",
                success_codes=[200, 201],
                json=payload,
            )

            if not response_put["result"]:
                hub.log.debug(f"Could not create {{ function.hardcoded.resource_name }} {response_put['comment']} {response_put['ret']}")
                result["comment"] = (response_put["comment"], response_put["ret"])
                result["result"] = False
                return result

            # TODO: Add conversion_util function here. Please refer to hub.tool.azure.virtual_networks.conversion_utils.convert_raw_virtual_network_to_present()
            result["new_state"] = {}
            result["comment"] = (f"Created azure.{{ function.hardcoded.create_ref }} '{name}'",)
            return result
        else:
            hub.log.debug(
                f"Could not get {{ function.hardcoded.resource_name }} {response_get['comment']} {response_get['ret']}"
            )
            result["result"] = False
            result["comment"] = (response_get["comment"], response_get["ret"]),
            return result
    else:
        existing_resource = response_get["ret"]
        # TODO: Add conversion_util function here. Please refer to hub.tool.azure.virtual_networks.conversion_utils.convert_raw_virtual_network_to_present
        result["old_state"] = {}
        # Generate a new PUT operation payload with new values
        # TODO: Add payload_update function here. Please refer to hub.exec.azure.virtual_networks.virtual_networks.update_virtual_network_payload()
        new_payload = {}
        if ctx.get("test", False):
            if new_payload["ret"] is None:
                result["new_state"] = copy.deepcopy(result["old_state"])
                result["comment"] = (f"azure.{{ function.hardcoded.create_ref }} '{name}' has no property need to be updated.",)
            else:
                # TODO: Add conversion_util function here. Please refer to hub.tool.azure.virtual_networks.conversion_utils.convert_raw_virtual_network_to_present
                result["new_state"] = {}
                result["comment"] = (f"Would update azure.{{ function.hardcoded.create_ref }} '{name}'",)
            return result
        # PUT operation to update a resource
        if new_payload["ret"] is None:
            result["new_state"] = copy.deepcopy(result["old_state"])
            result["comment"] = (
                f"azure.{{ function.hardcoded.create_ref }} '{name}' has no property need to be updated.",
            )
            return result
        result["comment"] = result["comment"] + new_payload["comment"]
        response_put = await hub.exec.request.json.put(
            ctx,
            url=f"{hub.exec.azure.URL}{resource_id}?api-version=2021-03-01",
            success_codes=[200],
            json=new_payload["ret"],
        )

        if not response_put["result"]:
            hub.log.debug(
                f"Could not update azure.{{ function.hardcoded.create_ref }} '{name}' {response_put['comment']} {response_put['ret']}"
            )
            result["result"] = False
            result["comment"] = (response_get["comment"], response_get["ret"])
            return result

        # TODO: Add conversion_util function here. Please refer to hub.tool.azure.virtual_networks.conversion_utils.convert_raw_virtual_network_to_present
        result["new_state"] = {}
        result["comment"] = (f"Updated azure.{{ function.hardcoded.create_ref }} '{name}'",)
        return result
"""

ABSENT_REQUEST_FORMAT = r"""
    result = dict(comment="", old_state=None, new_state=None, name=name, result=True)
    subscription_id = ctx.acct.subscription_id
    # TODO: This resource_id is not correct and it needs to be manually fixed to the correct one
    resource_id = {{ function.hardcoded.get_function }}
    # TODO: double check if the api version here is correct or not.
    response_get = {{ function.hardcoded.get_function }}(
        ctx,
        url=f"{hub.exec.azure.URL}{resource_id}?api-version=2021-03-01",
        success_codes=[200],
    )
    if response_get["result"]:
        # TODO: Add conversion_util function here. Please refer to hub.tool.azure.virtual_networks.conversion_utils.convert_raw_virtual_network_to_present
        result["old_state"] = {}
        if ctx.get("test", False):
            result["comment"] = ("Would delete azure.{{ function.hardcoded.create_ref }} '{name}'",)
            return result
        response_delete = {{ function.hardcoded.delete_function }}(
            ctx,
            url=f"{{ function.hardcoded.path }}",
            success_codes=[200, 202, 204],
        )

        if not response_delete["result"]:
            hub.log.debug(
                f"Could not delete azure.{{ function.hardcoded.create_ref }} '{name}' {response_delete['comment']} {response_delete['ret']}"
            )
            result["result"] = False
            result["comment"] = (response_delete["comment"], response_delete["ret"])
            return result

        result["comment"] = (
            f"Deleted azure.{{ function.hardcoded.create_ref }} '{name}'",
        )
        return result
    elif response_get["status"] == 404:
        # If Azure returns 'Not Found' error, it means the resource has been absent.
        result["comment"] = (f"azure.{{ function.hardcoded.create_ref }} '{name}' already absent",)
        return result
    else:
        hub.log.debug(
            f"Could not get azure.{{ function.hardcoded.create_ref }} '{name}' {response_get['comment']} {response_get['ret']}"
        )
        result["result"] = False
        result["comment"] = (response_get["comment"], response_get["ret"])
        return result
"""

DESCRIBE_REQUEST_FORMAT = r"""
    result = {}
    subscription_id = ctx.acct.subscription_id
    uri_parameters = {{ function.hardcoded.describe_parameters }}
    async for page_result in hub.tool.azure.request.paginate(
            ctx,
            url=f"{{ function.hardcoded.path }}",
            success_codes=[200],
    ):
        resource_list = page_result.get("value")
        if resource_list:
            for resource in resource_list:
                # TODO: double check if the resource_id is populated correctly
                resource_id = resource["id"]
                uri_parameter_values = (
                    hub.tool.azure.utils.get_uri_parameter_value_from_uri(resource_id, uri_parameters)
                )
                # TODO: Add conversion_util function here. Please refer to hub.tool.azure.virtual_networks.conversion_utils.convert_raw_virtual_network_to_present
                resource_translated = {}
                result[resource["id"]] = {f"azure.{{ function.hardcoded.create_ref }}.present":
                    [{parameter_key: parameter_value} for parameter_key, parameter_value in resource_translated.items()]}
    return result
"""
