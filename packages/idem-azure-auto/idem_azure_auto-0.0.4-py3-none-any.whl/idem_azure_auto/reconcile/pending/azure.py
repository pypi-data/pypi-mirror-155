def is_pending(hub, ret: dict):
    # The azure resource contains provisioningState. the optional values are:
    # CANCELED, CREATING, DELETING, FAILED, SUCCEEDED, UNKNOWN and UPDATING
    # provisioningState 'Succeeded' can be return when a new absent or present/update
    # request has not yet started. Therefore require 'Succeeded' without changes.
    hub.log.debug("Azure is_pending()")

    new_state = ret.get("new_state", None)
    status = None
    if new_state:
        status = _search_value(new_state, "provisioningState")

    if status and isinstance(status, str):
        hub.log.debug(f"Azure is_pending() status {status}")
        if status.casefold() == "failed" or status.casefold() == "canceled":
            hub.log.debug(
                f"No need to reconcile new state {new_state} with status {status}"
            )
            return False
        if (
            status.casefold() == "creating"
            or status.casefold() == "updating"
            or status.casefold() == "deleting"
        ):
            hub.log.debug(
                f"Need to reconcile new state {new_state} with status {status}"
            )
            return True

    # Reconcile for 'False' result or if there are changes
    return not ret["result"] is True or bool(ret["changes"])


def _search_value(obj, key):
    """Return a value corresponding to the specified key in the (possibly
    nested) dictionary d. If there is no item with that key, return
    default.
    """
    if key in obj:
        return obj[key]
    for k, v in obj.items():
        if isinstance(v, dict):
            item = _search_value(v, key)
            if item is not None:
                return item
