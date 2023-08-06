from typing import Any
from typing import Dict
from typing import List


async def paginate(
    hub, ctx, url: str, success_codes: List = [200], headers: Dict = {}
) -> Dict[str, Any]:
    """
    Paginate items from the given azure url
    :param hub: The redistributed pop central hub.
    :param ctx: A dict with the keys/values for the execution of the Idem run located in
     `hub.idem.RUNS[ctx['run_name']]`.
    :param url: HTTP request url
    :param success_codes: List of HTTP status codes that are considered as "successful" to a request
    :param headers: HTTP request headers
    :return: Response body
    """
    while url:
        ret = await hub.exec.request.json.get(
            ctx,
            url=url,
            success_codes=success_codes,
            headers=headers,
        )
        if not ret["result"]:
            raise ValueError(
                f"Error on requesting GET {url} with status code {ret['status']}:"
                f" {ret.get('comment', '')}"
            )
        result = ret["ret"]
        yield result
        url = result.get("nextLink", None)


def _no_update(old_value, new_value) -> bool:
    """Given two value, check if there is a need to update from the old_value to new_value."""
    if isinstance(old_value, str) and isinstance(new_value, str):
        # If the two values are the same string, then no need to update.
        return old_value == new_value
    elif isinstance(old_value, dict) and isinstance(new_value, dict):
        # If the new value dictionary is a subset of the old value dictionary, then no need to update
        return new_value.items() <= old_value.items()
    else:
        return False


def patch_json_content(
    hub,
    patch_parameters: dict,
    old_values: dict,
    new_values: dict,
    force_update_parameters: dict = {"tags": "tags"},
) -> dict:
    """
    Generate a json that contains all the parameters and their values that will be sent during a PATCH operation
    :param hub: The redistributed pop central hub. This is required in
    Idem, so while not used, must appear.
    :param patch_parameters: A dictionary of patchable parameters.
    For example: {"tags": "tags", "properties": {"properties_1": "properties_1", "properties_2": "properties_2"}}
    :param old_values: A dictionary that contains the old values of parameters.
    For example: {"tags": "new-tag", "properties": {"properties_1": "value_1", "properties_2": "value_2"}}
    :param new_values: A dictionary that contains the new values of parameters. This should be the exact structure as
     what old_values have.
    For example: {"tags": "new-tag", "properties": {"properties_1": "value_1", "properties_2": "value_2"}}
    :param force_update_parameters: A dictionary that determines what parameters will be updated as long as the value is
    different, regardless if the new value is a sub-set of old value or not.
    For example: {"tags": "new-tag", "properties": {"properties_1": "value_1", "properties_2": "value_2"}}
    """
    payload = {}
    for parameter_key, parameter_fields in patch_parameters.items():
        value = new_values.get(parameter_key, None)
        if value is None:
            continue
        elif isinstance(parameter_fields, str):
            if parameter_fields in old_values:
                # If the new value is a sub-set of the old value, then we need to decide if this should be a patch
                # operation or a no-op. For example, if tags property changes from {tagA, tagB} to {tagA}, this should
                # trigger a patch operation to update tags property to remove tagB. However, for some properties,
                # seeing a property being absent doesn't mean that we want to delete that property. So to distinguish
                # these two scenarios, we use 'force_update_parameters' to decide what should be updated as long as
                # the value is different.
                if parameter_fields in force_update_parameters:
                    # If a property is in 'force_update_parameters', update the resource as long as old and new value
                    # are different
                    if old_values[parameter_fields] != value:
                        payload.update({parameter_key: value})
                else:
                    # If a property is not in 'force_update_parameters', update the resource only if old and
                    # new value are different and new value is not a sub-set of the old value
                    if old_values[parameter_fields] != value and (
                        not _no_update(old_values[parameter_fields], value)
                    ):
                        payload.update({parameter_key: value})
            else:
                payload.update({parameter_key: value})
        elif isinstance(parameter_fields, dict):
            sub_force_update = force_update_parameters.get(parameter_key, dict())
            if parameter_key in old_values:
                sub_payload = patch_json_content(
                    hub,
                    parameter_fields,
                    old_values[parameter_key],
                    value,
                    sub_force_update,
                )
            else:
                sub_payload = patch_json_content(
                    hub, parameter_fields, dict(), value, sub_force_update
                )
            if sub_payload:
                payload.update({parameter_key: sub_payload})
        else:
            continue
    return payload
