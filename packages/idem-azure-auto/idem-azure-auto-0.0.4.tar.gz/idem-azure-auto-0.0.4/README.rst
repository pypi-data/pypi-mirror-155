===============
idem-azure-auto
===============

.. image:: https://img.shields.io/badge/made%20with-pop-teal
   :alt: Made with pop, a Python implementation of Plugin Oriented Programming
   :target: https://pop.readthedocs.io/

.. image:: https://img.shields.io/badge/made%20with-python-yellow
   :alt: Made with Python
   :target: https://www.python.org/

.. note::
    Idem plugin to manage Azure cloud resources

About
=====

Azure Cloud Provider Idem plugin

What is POP?
------------

This project is built with `pop <https://pop.readthedocs.io/>`__, a Python-based
implementation of *Plugin Oriented Programming (POP)*. POP seeks to bring
together concepts and wisdom from the history of computing in new ways to solve
modern computing problems.

For more information:

* `Intro to Plugin Oriented Programming (POP) <https://pop-book.readthedocs.io/en/latest/>`__
* `pop-awesome <https://gitlab.com/saltstack/pop/pop-awesome>`__
* `pop-create <https://gitlab.com/saltstack/pop/pop-create/>`__

Getting Started
===============

Prerequisites
-------------

* Python 3.7+
* git *(if installing from source, or contributing to the project)*

Installation
------------

.. note::

   If wanting to contribute to the project, and setup your local development
   environment, see the ``CONTRIBUTING.rst`` document in the source repository
   for this project.

If wanting to use ``idem-azure-auto``, you can do so by either
installing from PyPI or from source.

Install from PyPI
+++++++++++++++++

.. code-block:: bash

    pip install pop-release

Install from source
+++++++++++++++++++

.. code-block:: bash

   # clone repo
   git clone git@<your-project-path>/idem-azure-auto.git
   cd idem-azure-auto

   # Setup venv
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .

Usage
=====

Credentials Setup
-----------------

After installation, the Azure Idem execution and state modules will be accessible to the pop `hub`.
In order to use them, we need to set up our credentials.

Create a new file called `credentials.yaml` and populate it with credentials.
The `default` profile will be picked up automatically by `idem`.

There are multiple authentication backends for `idem-azure-auto` which each have their own unique set of parameters.
The following examples show the parameters that can be used to define credential profiles.

credentials.yaml:

..  code:: sls

    azure:
       default:
          client_id: "12345678-1234-1234-1234-aaabc1234aaa"
          secret: "76543210-4321-4321-4321-bbbb3333aaaa"
          subscription_id: "ZzxxxXXXX11xx-aaaaabbbb-k3xxxxxx"
          tenant: "bbbbbca-3333-4444-aaaa-cddddddd6666"

Next step is to encrypt the credentials file, and add the encryption key and encrypted file
path to the ENVIRONMENT.

Encrypt the credential file:

.. code:: bash

    Idem encrypt credentials.yaml

This will generate a credentials.yaml.fernet file and a command line output token::

    -AXFSEFSSEjsfdG_lb333kVhCVSCDyOFH4eABCDEFNwI=

Add these to your environment:

.. code:: bash

    export ACCT_KEY="-AXFSEFSSEjsfdG_lb333kVhCVSCDyOFH4eABCDEFNwI="
    export ACCT_FILE=$PWD/credentials.yaml.fernet


You are ready to use idem-azure-auto!!!

STATES
--------
Idem states are used to make sure resources are in a desired state.
The desired state of a resource can be specified in sls file.
In Idem-azure-auto, three states are supported: `present`, `absent`, `describe`

present state
+++++++++++++
`present` state makes sure a resource exists in a desired state. If a resource does
not exist, running `present` will create the resource on the provider. If a resource
exists, running `present` will update the resource on the provider. (Only the values
that the Azure REST api supports can be updated.)

absent state
++++++++++++
`absent` state makes sure a resource does not exist. If a resource exits, running
`absent` will delete the resource. If a resource does not exist, running `absent`
is a no-operation.

describe state
++++++++++++++
`describe` state lists all the current resources of the same resource type
under the subscription id specified in the credential profile.

States can be accessed by their relative location in `idem-azure-auto/idem_azure_auto/states`.
For example, in the state sls yaml file below, Azure resource group state can be created with the `present` function.

my_resource_group_state.sls:

.. code:: sls

    my-azure-resource-group:
      azure.resource_management.resource_groups.present:
      - resource_group_name: my-azure-resource-group
      - parameters:
        location: eastus

The state sls file can be executed with:

.. code:: bash

    idem state $PWD/my_resource_group_state.sls

Example of creating an Azure virtual network:

.. code:: sls

    my-virtual-network:
      azure.virtual_networks.virtual_networks.present:
      - resource_group_name: my-azure-resource-group
      - virtual_network_name: my-virtual-network
      - parameters:
        location: eastus
        properties:
          addressSpace:
            addressPrefixes:
            - 10.12.13.0/25
          flowTimeoutInMinutes: 10

The resource parameters in an sls yaml file follow the exact structure as
what's in the `Azure REST api doc <https://docs.microsoft.com/en-us/rest/api/azure/>`__ . URI Parameters
should be specified in snake case with "- " in front. All parameters of the api request body
should be specified in exactly the same way as what's in the Azure REST api.

Current Supported Resources states
++++++++++++++++++++++++++++++++++

authorization
"""""""""""""
role_assignments

resource_management
"""""""""""""""""""
resource_groups

policy
""""""
policy_definitions

management_groups
"""""""""""""""""""
management_groups

subscription
"""""""""""""""""""
subscription
