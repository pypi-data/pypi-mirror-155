import os
from typing import List

try:
    import bs4  # noqa
    import requests  # noqa
    import tqdm  # noqa

    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)


def __virtual__(hub):
    return HAS_LIBS


__func_alias__ = {"type_": "type"}


def parse(hub, api_url: str, rest_api: str, resources: List[str] = None):
    """
    rest_api can be one of: Azure, Kaizala, Power BI, Playfab, Azure DevOps, Operations Manager, Azure Blockchain Workbench, or Dynamic 365 Online Management
    """
    plugins = {}
    ref = rest_api

    # TODO using selenium should be the default
    # selenium is needed because the html we need is rendered after a bunch of javascript
    USING_SELENIUM = False
    if USING_SELENIUM:
        url = f"https://docs.microsoft.com/en-us/rest/api/{ref.replace(' ', '-')}"
        soup = hub.pop_create.azure.api_reference.parse_url(url, resources)
    else:
        # TODO once selenium is integrated we can remove this and the baked-in file
        if ref.lower() == "azure":
            file_path = os.path.dirname(__file__) + "/resource/azure-rest-api.html"
        else:
            hub.log.error(f"{ref} is not a supported resource.")
        soup = hub.pop_create.azure.api_reference.parse_file(file_path, resources)

    new_plugins = hub.pop_create.azure.api_reference.parse(soup, resources)

    for k, v in new_plugins.items():
        ref = f"{hub.tool.format.case.snake(ref)}.{hub.tool.format.case.snake(k)}"
        plugins[ref] = v

    return plugins
