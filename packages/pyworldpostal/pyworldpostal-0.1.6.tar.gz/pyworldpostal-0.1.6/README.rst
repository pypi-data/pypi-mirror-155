pyworldpostal
=============

|PyPI version| |License| |Python Versions| |Build Status| |Requirements Status|

:Author: Dalwinder singh

.. contents::
    :backlinks: none

.. sectnum::

What is it?
-----------

Extract meta data like

-  ``postal_code``
-  ``coutry_code``
-  ``state_code``
-  ``state_name``
-  ``admin_name2``
-  ``admin_name3``
-  ``place_name``



-  Appropriate boundaries for that area

by just using the ``postal_code`` and `Country code <https://github.com/dalwindr/inferzipcode/tree/main/pyworldpostal/country_files/*.py>`__

Features
--------

-  Written in uncomplicated ``python``
-  Supports all the Country codes specified in the ISO specification i.e
   all **264 countries** where they have a pin code.

   You can find a list of all the country codes at `the Wiki page <https://github.com/dalwindr/inferzipcode/tree/main/pyworldpostal/country_files/*.py>`__
-  Gives ouput in a ``dict`` form or a ``JSON`` format
-  Fast and easy to use


Installation
------------

Option 1: installing through `pip <https://pypi.python.org/pypi/inferzipcode>`__ (Suggested way)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`pypi package link <https://pypi.python.org/pypi/pyzipcode-cli>`__

``$ pip install inferzipcode``

If you are behind a proxy

``$ pip --proxy [username:password@]domain_name:port install inferzipcode``

**Note:** If you get ``command not found`` then
``$ sudo apt-get install python-pip`` should fix that

Option 2: Installing from source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ git clone https://github.com/dalwindr/inferzipcode.git
    $ cd inferzipcode/
    $ pip install -r requirements.txt
    $ python setup.py install

Usage
-----

``bulkget()``
~~~~~~~~~
