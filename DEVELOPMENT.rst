pytest vulture
-------------

How it works
============

At the start of pytest execution (pytest_sessionstart),
it parses the configuration file if it exists (otherwise it takes the default values),
and then run vulture.

When a file is manages by pytest (pytest_collect_file), it looks for vulture outputs related to this file
and add it to the pytest output of the file.
Vulture outputs are ignored if they are an entrypoint or if they are ignored by the vulture configuration file.
If no vulture outputs are found for this file, it is skipped.

Development Environment Suggestion
==================================

Use `pyenv <https://github.com/pyenv/pyenv>`_, and install all the versions supported by the plugin.

.. code-block:: shell

    pyenv install 3.7.7

    pyenv install 3.8.2

    pyenv install 3.9.13

    pyenv install 3.10.6


Set the installed versions as global, that will allow tox to find all of them.

.. code-block:: shell

    pyenv global 3.10.6 3.9.13 3.8.2 3.7.7

In your virtualenv, install tox and the tests dependencies, and run tox :

.. code-block:: shell

    pip install tox

    pip install .[test]

    tox

The development environment is complete.