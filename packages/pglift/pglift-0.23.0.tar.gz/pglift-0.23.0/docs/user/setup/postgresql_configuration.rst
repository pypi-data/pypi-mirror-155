.. _`postgresql-site-configuration`:

PostgreSQL configuration
========================

Instances created by pglift have their configuration managed. This is handled
by writing these configuration items into specific files located in the
``conf.pglift.d`` directory within instance's data directory. An include
directive is then inserted on top of main ``postgresql.conf`` file.

For instance, given a ``13/main`` instance, we'll have the following
configuration tree:

.. code-block:: bash

    $prefix/srv/pgsql/13/main/data/
    ├── conf.pglift.d
    │   ├── pgbackrest.conf
    │   ├── site.conf
    │   └── user.conf
    ├── postgresql.auto.conf
    └── postgresql.conf

Head of ``postgresql.conf`` contains:

.. code-block::
   :caption: postgresql.conf

    include_dir = 'conf.pglift.d'

    # -----------------------------
    # PostgreSQL configuration file
    # -----------------------------
    #


File ``conf.pglift.d/pgbackrest.conf`` contains configuration items needed for
pgBackRest to operate. Any other satellite service needing to override
PostgreSQL configuration would have its file there.

File ``conf.pglift.d/user.conf`` contains configuration items defined by the
user at instance creation or update.

File ``conf.pglift.d/site.conf`` contains site-wise configuration items, if
any. The content of this file, or a template, might be defined on site by
writing to ``$XDG_CONFIG_HOME/pglift/postgresql/site.conf`` [#xdgconfighome]_
or ``/etc/pglift/postgresql/site.conf`` (by order of precedence). The default
``site.conf`` file contains:

.. literalinclude:: ../../../src/pglift/data/postgresql/site.conf
   :caption: site.conf

Since the include directive is located on top of ``postgresql.conf`` file, any
setting defined in that file (and kept after the include directive) will take
precedence over the managed configuration.

.. seealso:: The ``pgconf`` command to manage :ref:`PostgreSQL configuration <pgconf>`.

.. [#xdgconfighome]
   Where ``$XDG_CONFIG_DIR`` would be ``$HOME/.config`` unless configured
   differently.
