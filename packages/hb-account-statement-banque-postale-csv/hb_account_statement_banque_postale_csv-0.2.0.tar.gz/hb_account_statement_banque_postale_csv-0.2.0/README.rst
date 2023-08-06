#########################################
Hb Bank Statement Machine Learning Module
#########################################

This module implements the import of **banque postale**'s csv file as statement

*******
Install
*******

Dependencies for ArchLinux

.. code-block::

    sudo pacman -S cairo pkgconf gobject-introspection


Dependencies for debian


.. code-block::

    sudo apt-get install libcairo2-dev libgirepository1.0-dev


Install the package

.. code-block::

    # installs python deps
    pip install -e .
    # createdb postgresql database
    createdb banque_postale_csv
    # initialize database
    trytond-admin -c trytond-dev.conf -d banque_postale_csv --all
    # install module hb_tryton
    trytond-admin -c trytond-dev.conf -d banque_postale_csv -u hb_account_statement_banque_postale_csv --activate-dependencies


*****
Usage
*****

This module use the wexisting wizard to import statement

.. note::

    If the the module **hb_bank_statement_machine_learning** is installed then 
    the party and account will be predict form the number on the line

*********
CHANGELOG
*********

0.2.0 (2022-06-20)
------------------

* Fixed date during import
* Fixed default account, if no account is defined use the account of the journal


0.1.0 (2021-09-28)
------------------

* Implemented the import as statement
* Used the machine learning 
