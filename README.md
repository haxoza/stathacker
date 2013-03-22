stathacker
==========

Installation
~~~~~~~~~~~~

::

    $ git clone git@github.com:haxoza/stathacker.git stathacker
    $ cd stathacker
    $ mkvirtualenv stathacker # (optional)
    $ pip install -r requirements.txt


Usage
~~~~~

::

    $ python runner.py


Configuration
~~~~~~~~~~~~~

::

    DOMAIN = 'coderwall.com'

    PLUGINS = ['hackernews.crawler.Hackernews']
    CALLBACKS = ['callbacks.console']


Set (``DOMAIN``) variable to domain name you would like to observe.

(``CALLBACKS``) is a list of functions that will be invoked when given plugin discover occurrence of domain.
