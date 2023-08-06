{{cookiecutter.project_name|title}}
{{ '=' * cookiecutter.project_name|length }}

{{cookiecutter.service_name}} Cloud Provider for Idem

DEVELOPMENT
===========

Clone the `{{cookiecutter.project_name}}` repository and install with pip.

.. code:: bash

    git clone git@gitlab.com:my-user/{{cookiecutter.project_name}}.git
    pip install -e {{cookiecutter.project_name}}

ACCT
====

After installation {{cookiecutter.service_name}} Idem Provider execution and state modules will be accessible to the pop `hub`.
In order to use them we need to set up our credentials.

Create a new file called `credentials.yaml` and populate it with profiles.
The `default` profile will be used automatically by `idem` unless you specify one with `--acct-profile=profile_name` on the cli.

`acct backends <https://gitlab.com/saltstack/pop/acct-backends>`_ provide alternate methods for storing profiles.

The {{cookiecutter.service_name}} provider uses the {{cookiecutter.acct_plugin}} acct plugin for authentication.
A profile needs to specify the authentication parameters for {{cookiecutter.acct_plugin}}.

credentials.yaml

..  code:: sls

    {{cookiecutter.acct_plugin}}:
      default:
        username: my_user
        password: my_good_password
        endpoint_url: https://console.{{cookiecutter.service_name}}.com/api

Now encrypt the credentials file and add the encryption key and encrypted file path to the ENVIRONMENT.

The `acct` command should be available as it is a requisite of `idem` and `{{cookiecutter.clean_name}}`.
Encrypt the the credential file.

.. code:: bash

    acct encrypt credentials.yaml

output::

    -A9ZkiCSOjWYG_lbGmmkVh4jKLFDyOFH4e4S1HNtNwI=

Add these to your environment:

.. code:: bash

    export ACCT_KEY="-A9ZkiCSOjWYG_lbGmmkVh4jKLFDyOFH4e4S1HNtNwI="
    export ACCT_FILE=$PWD/credentials.yaml.fernet


USAGE
=====
A profile can be specified for use with a specific state.
If no profile is specified, the profile called "default", if one exists, will be used:

.. code:: sls

    ensure_user_exists:
      {{cookiecutter.service_name}}.user.present:
        - acct_profile: my-staging-env
        - name: a_user_name
        - kwarg1: val1

It can also be specified from the command line when executing states.

.. code:: bash

    idem state --acct-profile my-staging-env my_state.sls

It can also be specified from the command line when calling an exec module directly.

.. code:: bash

    idem exec --acct-profile my-staging-env {{cookiecutter.service_name}}.user.list
