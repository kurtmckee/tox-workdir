tox-workdir
###########

*Put tox work directories in a cache directory by default.*

----

By default, tox will create packaging and test environments in a ``.tox/`` subdirectory
in the same directory as the project's ``tox.ini`` or ``pyproject.toml`` file.

..  code-block:: text

    .tox/
    |   +-- .pkg/
    |   +-- docs/
    |   +-- mypy/
    |   +-- py39/
    |   +-- py310/
    |   +-- py311/
    |   +-- py312/
    |   \-- py313/
    |
    \-- tox.ini

As you interact with more and more projects,
those ``.tox/`` directories will proliferate throughout your filesystem.

This default behavior makes it harder to clean up all of your cached environments
and can make backups slow (and potentially expensive).

tox-workdir changes the default work directory to point to your user cache directory,
keeping your development directories trim and sleek over time.


Installation
============

If you're using pipx, inject tox-workdir into your existing tox install:

..  code-block:: text

    pipx inject tox tox-workdir

If you're using a virtual environment, install tox-workdir as a regular package:

..  code-block:: text

    pip install tox-workdir

No configuration is needed;
installing the plugin immediately changes the default ``work_dir`` value.


Work directory paths
====================

Where tox defaults to ``.tox/``, tox-workdir defaults to your user cache directory:

=================== ===============================================================
Operating system    Base path
=================== ===============================================================
Linux               ``$XDG_CACHE_DIR/tox-workdir/``
macOS               ``/Users/{user}/Library/Caches/tox-workdir/``
Windows             ``C:\Users\{user}\AppData\Local\kurtmckee\tox-workdir\Cache\``
=================== ===============================================================

Note that ``$XDG_CACHE_DIR``, above, defaults to ``$HOME/.cache`` if unset.

A hash of the path to the tox config file is used as a subdirectory for uniqueness.

You can see the ``workdir`` value that will be used by running:

..  code-block:: text

    tox workdir


Feel-good benefits
==================

To feel good about your choice to install this plugin,
simply check how much space ``.tox/`` directories are consuming.
Then, think about how much faster your backups will process
without all of those ``.tox/`` directories!

Assuming that you have a development directory with a number of project directories,
you can run one of the following commands to see how much space is consumed
by ``.tox/`` subdirectories.

On Linux and macOS:

..  code-block:: console

    $ du -csh */.tox | tail -n 1
    10G     total

On Windows, using Powershell:

..  code-block:: console

    $ (Get-ChildItem -Recurse */.tox | Measure-Object -Property Length -Sum).Sum / 1GB
    10.00000000
