import pathlib

import tqdm
from dict_tools.data import NamespaceDict

try:
    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)


def __virtual__(hub):
    return HAS_LIBS


def context(hub, ctx, directory: pathlib.Path):
    ctx = hub.pop_create.idem_cloud.init.context(ctx, directory)

    ctx.servers = [
        "https://management.azure.com/",
        "https://management.core.windows.net/",
    ]

    # We already have an acct plugin
    ctx.has_acct_plugin = False
    ctx.service_name = ctx.service_name or "azure_auto"
    docs_api = "https://docs.microsoft.com"
    resources = hub.pop_create.azure.resource.parse(
        docs_api, rest_api=ctx.rest_api, resources=ctx.resources
    )

    # Initialize cloud spec
    if ctx.create_plugin == "auto_states":
        request_format = {
            "get": hub.pop_create.azure.template.GET_REQUEST_FORMAT,
            "list": hub.pop_create.azure.template.LIST_REQUEST_FORMAT,
            "create": hub.pop_create.azure.template.CREATE_REQUEST_FORMAT,
            "update": hub.pop_create.azure.template.UPDATE_REQUEST_FORMAT,
            "delete": hub.pop_create.azure.template.DELETE_REQUEST_FORMAT,
        }
    elif ctx.create_plugin == "state_modules":
        request_format = {
            "present": hub.pop_create.azure.template.PRESENT_REQUEST_FORMAT,
            "absent": hub.pop_create.azure.template.ABSENT_REQUEST_FORMAT,
            "describe": hub.pop_create.azure.template.DESCRIBE_REQUEST_FORMAT,
        }

    ctx.cloud_spec = NamespaceDict(
        project_name=ctx.project_name,
        service_name=ctx.service_name,
        request_format=request_format,
        plugins={},
    )

    for ref, resource in tqdm.tqdm(resources.items()):
        try:
            plugins = hub.pop_create.azure.init.plugin(ctx, resource=resource)
            if plugins:
                ctx.cloud_spec.plugins = plugins
                hub.cloudspec.init.run(
                    ctx,
                    directory,
                    create_plugins=[ctx.create_plugin],
                )
        except Exception as e:
            hub.log.error(f"Error when generating {ref}: {e.__class__.__name__}: {e}")

    hub.pop_create.init.run(
        directory=directory,
        subparsers=["cicd"],
        **ctx,
    )

    ctx.cloud_spec.plugins = {}
    return ctx


def plugin(hub, ctx, resource):
    plugins = dict()
    for service_name, resources in resource.items():
        service_name_formatted = (
            service_name.lower().strip().replace(" ", "_").replace("-", "_")
        )
        for r in resources:
            resource_name_formatted = (
                r.get("resource").lower().strip().replace(" ", "_").replace("-", "_")
            )
            if not resource_name_formatted:
                continue
            plugin_key = f"{service_name_formatted}.{resource_name_formatted}"

            path = pathlib.Path(ctx.target_directory).absolute() / ctx.clean_name
            skip_existing = not ctx.overwrite_existing
            if skip_existing:
                if ctx.create_plugin == "auto_states":
                    path = path / "exec" / ctx.service_name
                elif ctx.create_plugin == "state_modules":
                    path = path / "states" / ctx.service_name
                elif ctx.create_plugin == "tests":
                    path = path / "tests" / "integration" / "states"

                path = path / service_name_formatted / f"{resource_name_formatted}.py"
                if path.exists():
                    hub.log.info(
                        f"Plugin already exists at '{path}', use `--overwrite` modify"
                    )
                    continue

            shared_function_data = {
                "get_function": f"await hub.exec.request.json.get",
                "create_function": f"await hub.exec.request.json.put",
                "list_function": f"await hub.exec.request.json.get",
                "delete_function": f"await hub.exec.request.raw.delete",
                "patch_function": f"await hub.exec.request.json.patch",
                "resource_name": resource.get("resource"),
                "create_ref": plugin_key,
            }
            try:
                resource_plugin = hub.pop_create.azure.plugin.parse(
                    ctx, r, shared_function_data
                )
            except Exception as e:
                hub.log.error(
                    f"Could not parse {plugin_key}: {e.__class__.__name__}: {e}"
                )
                continue
            plugins[plugin_key] = resource_plugin
    return plugins
