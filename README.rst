pytest vulture
--------------

This plugin enables you to run `vulture` (https://pypi.org/project/vulture/) alongside `pytest`,
allowing for dead code detection during your testing process.

Sample Usage
============

To integrate `vulture` with `pytest` and find dead code, use the following commands:

1. **Basic Usage**
   Run `vulture` with `pytest` to check for dead code:

   .. code-block:: shell

      pytest --vulture

2. **Custom Configuration**
   Specify a custom configuration file path:

   .. code-block:: shell

      pytest --vulture --vulture-cfg-file=/path/to/vulture.ini

   **Note:** By default, the tool looks for configuration files in the following order:

   - ``pyproject.toml``
   - ``tox.ini``
   - ``vulture.ini``

Ignoring Vulture Messages
=========================

You can ignore specific warnings from `vulture` directly in the source code. Here’s how:

- **Ignore Specific Lines:**

  .. code-block:: python

      def test_function():
          unused_variable = 42  # vulture: ignore

- **Ignore Entire Methods:**

  .. code-block:: python

      def ignored_function():  # vulture: ignore
          pass

- **Ignore Classes:**

  .. code-block:: python

      class IgnoredClass:  # vulture: ignore
          pass



Configuring with ``pyproject.toml``
===================================

Here’s an example of how to configure `vulture` using ``pyproject.toml``:

.. code-block:: toml

    [tool.vulture]
    # Exclude specific paths (e.g., test directories)
    exclude = [
        "*/test/*",
    ]

    # Ignore specific files in the `pytest` output (but they are still checked by `vulture`)
    ignore = [
        "src/some_ignored_file.py",
    ]

    # Ignore specific function or variable names
    ignore-names = [
        "deprecated_function",
    ]

    # Ignore decorators
    ignore-decorators = [
        "@app.route",
        "@celery.task",
    ]

    # Ignore specific types of messages (e.g., imports)
    ignore-types = [
        "import",
    ]

    # Define the source path
    source-path = "src"

Configuring with ``.ini`` Config Files
======================================

Here’s an example of how to configure `vulture` using an ``.ini`` file:

.. code-block:: ini

    [vulture]
    exclude =
        */test/*  # Usually exclude tests as they may cover dead code

    ignore =
        src/some_ignored_file.py

    ignore-names =
        deprecated_function

    ignore-decorators =
        @app.route
        @celery.task

    ignore-types =
        attribute
        variable


Acknowledgements
================

This code depends on
`vulture <https://pypi.org/project/vulture>`__

Development
===========

If you want to help development, there is overview documentation in DEVELOPMENT.rst.

Issues
===========

If you encounter any problems, please file an issue along with a detailed description.

Releases
========

2.2.0
~~~~~~

- Add pyproject.toml support for parameters

2.0.2
~~~~~~

- Uses vulture with pytest (tested with python 3.7 3.8 and 3.9, with vulture==2.3 and pytest 7.x)

1.0.0
~~~~~~

- stable Gatewatcher internal use only

0.x
~~~~~~

- unstable Gatewatcher internal use only