Scrapy spiderdocs command
=========================

Usage example
-------------

.. code-block:: bash

    pip install git+https://github.com/nanvel/scrapy-spiderdocs.git
    scrapy spiderdocs <module.name>

Example project
---------------

See ``documented`` project for example.

.. code-block:: python

    # -*- coding: utf-8 -*-
    import scrapy


    class ExampleSpider(scrapy.Spider):
        """Some text.
        Hi!

        ; Note

        Some note.

        ; output

        {
            "1": 1
        }
        """

        name = 'example'
        allowed_domains = ('example.com',)
        start_urls = ('http://example.com/',)

        def parse(self, response):
            yield {
                'body_length': len(response.body)
            }

Settings:

.. code-block:: python

    SPIDERDOCS_LOCATIONS = {
        'documented.spiders.example': "docs/example.md"
    }
    SPIDERDOCS_SECTION_PROCESSORS = {
        'output': lambda i: '```json\n{i}\n```'.format(i=i)
    }

Execute the command:

.. code-block:: bash

    scrapy spiderdocs documented.spiders

Output:

.. code-block:: md

    # documented.spiders spiders
    
    ## example [documented.spiders.example.ExampleSpider]
    
    ### Note
    
    Some note.
    
    
    ### output
    
    ```json
    Some note.
    
    
    {
        "1": 1
    }
    ```

Output options
--------------

stdout
~~~~~~

.. code-block:: bash

    scrapy spiderdocs <module.name> > somefile.md

`-o` (`--output`) option
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    scrapy spiderdocs <module.name> -o somefile.md

Settings
~~~~~~~~

.. code-block:: python

    SPIDERDOCS_LOCATIONS = {
        'module.name': "somefile.md"
    }

The setting used if no module specified.

.. code-block:: bash

    scrapy spiderdocs

Docstring syntax
----------------

Use ``;`` to create sections. For example:

.. code-block:: text

    ; Section 1

    Some text ...

    ; Section 2

    Some text ...

Use ``; end`` to close a section:

.. code-block:: text

    This text will not be added to the documentation.

    ; Section 1

    Some text ...

    ; end

    And this text also will be skipped.

Section processors
~~~~~~~~~~~~~~~~~~

An example:

.. code-block:: python

    SPIDERDOCS_SECTION_PROCESSORS = {
        'output': lambda i: '```json\n{i}\n```'.format(i=i)
    }

.. code-block:: bash

    ; Output
    
    {
        "attr": "value"
    }

will be translated into:

.. code-block:: md

    ### Output
    
    ```json
    {
        "attr": "value"
    }
    ```

Scrapy settings
---------------

``SPIDERDOCS_LOCATIONS: {<module>: <destination>}``, default: ``{}``.

``SPIDERDOCS_SECTION_PROCESSORS: {<section_name>: <function>}``, default: ``{}``.

See usage examples above.

Development
-----------

.. code-block:: bash

    git clone git@github.com:nanvel/scrapy-spiderdocs.git
    cd scrapy-spiderdocs
    virtualenv .env --no-site-packages -p /usr/local/bin/python3
    source .env/bin/activate
    pip install scrapy
    scrapy crawl example
    scrapy spiderdocs documented.spiders
    python -m unittest documented.tests

TODO
----

- unittests
