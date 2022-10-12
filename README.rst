pytest vulture
--------------

Run vulture (https://pypi.org/project/vulture/) with pytest to find dead code.

Sample Usage
============
.. code-block:: shell

   py.test --vulture

would be the most simple usage and would run vulture for all error messages.

.. code-block:: shell

   py.test --vulture --vulture-cfg-file=/test/vulture.ini

This would use the vulture with the /test/vulture.ini config path

Ignoring vulture messages in source code
========================================

- ignoring lines :

.. code-block:: python

    def test():
        a = 2    # vulture: ignore

- ignoring methods :

.. code-block:: python

    def test():  # vulture: ignore
        pass

- ignoring classes :

.. code-block:: python

    class Test:  # vulture: ignore
        pass


Config file
============

The config file (the path can be defined by the --vulture-cfg-file option) can look like this ::

    [vulture]
    # completely exclude files for vulture
    exclude =
        */test/* # We usualy exclude tests because tests can cover dead code

    # those file are ignored by pytest, but still computed by vulture
    ignore =
        src/toto.py

    # ignoring names in code
    ignore-names =
        delimiter

    # ignoring decorators
    ignore-decorators =
      @application.errorhandler
      @application.route
      @celery_app.task
      @application.app.errorhandler

    # ignore vulture type of messages
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

2.0.2
~~~~~~

- Uses vulture with pytest (tested with python 3.7 3.8 and 3.9, with vulture==2.3 and pytest 7.x)

1.0.0
~~~~~~

- stable Gatewatcher internal use only

0.x
~~~~~~

- unstable Gatewatcher internal use only