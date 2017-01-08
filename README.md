# Scrapy spiderdocs command

## Usage example

```bash
pip install git+https://github.com/nanvel/scrapy-spiderdocs.git
scrapy spiderdocs <module.name> -o <filename.md> 
```

See documented project for example.

```python
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
```

Settings:
```
SPIDERDOCS_LOCATIONS = {
    'documented.spiders.example': "docs/example.md"
}
SPIDERDOCS_SECTION_PROCESSORS = {
    'output': lambda i: '```json\n{i}\n```'.format(i=i)
}
```

Execute the command:
```bash
scrapy spiderdocs documented.spiders
```

Output:

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

Run the example spider:
```bash
scrapy crawl example
```

## TODO

- test on Python2.7
- unittests
- setup.py
- docs
