CLI_CONFIG = {
    "rest_api": {
        "subcommands": ["azure"],
        "dyne": "pop_create",
    },
    "resources": {
        "subcommands": ["azure"],
        "dyne": "pop_create",
    },
}
CONFIG = {
    "resources": {
        "default": [],
        "nargs": "*",
        "help": "The resources to target under the rest api, defaults to all",
        "dyne": "pop_create",
    },
    "rest_api": {
        "default": "Azure",
        "help": "The Microsoft REST API to target, defaults to Azure",
        "dyne": "pop_create",
    },
}
DYNE = {
    "pop_create": ["pop_create"],
    "tool": ["tool"],
    "states": ["states"],
    "exec": ["exec"],
    "acct": ["acct"],
    "reconcile": ["reconcile"],
}
SUBCOMMANDS = {
    "azure": {
        "help": "Create idem_azure state modules by Azure REST API web",
        "dyne": "pop_create",
    },
}
