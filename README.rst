time tracker
============

Set up local environment
------------------------

Requirements to run the project VM are:

- Vagrant
- VitrualBox

.. code:: sh

   vagrant up
   vagrant ssh

The VM comes with aliases:

-  ``dj`` - shortcut to ``django-admin``
-  ``djrun`` - shortcut to ``django-admin runserver 0:8000``

Create database and superuser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: sh

   vagrant ssh
   dj migrate
   dj createsuperuser

Start the development server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: sh

   vagrant ssh
   djrun

The application should be available at http://localhost:8000/.


Run tests
~~~~~~~~

.. code:: sh

    vagrant ssh
    make lint
    make test
