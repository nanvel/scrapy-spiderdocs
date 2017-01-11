from __future__ import print_function

import re

from scrapy.commands import ScrapyCommand
from scrapy.exceptions import UsageError


__all__ = ('Command',)


INDENT_RE = re.compile('^(\s+)')


def get_line_indent(line):
    matches = INDENT_RE.match(line)
    return matches and len(matches.groups()[0]) or 0


class SpiderDocsSection(object):

    _name = None
    _lines = []

    def __init__(self, name, processor=None):
        self._name = name
        self._processor = processor
        self._lines = []

    def append(self, line):
        self._lines.append(line)

    def _default_processor(self, name, content):
        return "### {name}\n\n{content}".format(
            name=name,
            content=content
        )

    def to_md(self):
        content = '\n'.join(self._lines).strip()
        return (self._processor or self._default_processor)(name=self._name, content=content)


class Command(ScrapyCommand):

    requires_project = True
    default_settings = {
        # {<module>: <destination>}
        'SPIDERDOCS_LOCATIONS': {},
        # {<section_name>: <function(name, content) -> str>}
        'SPIDERDOCS_SECTION_PROCESSORS': {},
        'LOG_ENABLED': False
    }
    SECTION_PREFIX = ';'
    SECTION_END = 'end'

    _locations = {}

    def short_desc(self):
        return "Generate spiders documentation md file for specified module."

    def add_options(self, parser):
        parser.usage = "usage: scrapy spiderdocs [<module.name>] [-o <filename.md>]"
        ScrapyCommand.add_options(self, parser)
        parser.add_option("-o", "--output", dest="output_filename", metavar="FILE", help="Output file name.")

    def process_options(self, args, opts):
        ScrapyCommand.process_options(self, args, opts)
        if args:
            self._locations[args[0]] = opts.output_filename
        else:
            locations = self.settings.get('SPIDERDOCS_LOCATIONS', None)
            if locations:
                self._locations = locations
            else:
                raise UsageError("Module name is required.", print_help=False)

    def run(self, args, opts):

        section_processors = self.settings.get('SPIDERDOCS_SECTION_PROCESSORS') or {}

        for module, location in self._locations.items():

            output = ["# {module_name} spiders".format(module_name=module)]

            spiders_count_total = 0
            spiders_count_documented = 0

            for spider_name in sorted(self.crawler_process.spider_loader.list()):
                spider = self.crawler_process.spider_loader.load(spider_name)

                spiders_count_total += 1

                if not spider.__module__.startswith(module):
                    continue

                if not spider.__doc__:
                    continue

                sections = []

                doc_lines = spider.__doc__.split('\n')

                # calculate base text indent
                indent = None
                for line in doc_lines:
                    line_indent = get_line_indent(line)
                    if line_indent > 0 and (indent is None or line_indent < indent):
                        indent = line_indent
                indent = indent or 0

                current_section = None
                for line in doc_lines:
                    line_indent = get_line_indent(line)
                    if line_indent > 0:
                        line = line[indent:]

                    if line.startswith(self.SECTION_PREFIX):
                        if current_section:
                            sections.append(current_section.to_md())

                        section_name = line[len(self.SECTION_PREFIX):].strip()
                        if section_name.lower().strip() == self.SECTION_END:
                            current_section = None
                        else:
                            current_section = SpiderDocsSection(
                                section_name,
                                processor=section_processors.get(section_name.lower())
                            )

                        continue

                    if current_section:
                        current_section.append(line)

                if current_section:
                    sections.append(current_section.to_md())

                if sections:
                    output.append(
                        "## {spider_name} ({class_name})".format(
                            spider_name=spider.name,
                            class_name=spider.__name__
                        )
                    )
                    output.extend(sections)

                    spiders_count_documented += 1

            output = '\n\n'.join(output)

            if location:
                with open(location, 'w') as f:
                    f.write(output)
                print(
                    "{module} -> {location} ({documented}/{total} spiders)".format(
                        module=module,
                        location=location,
                        total=spiders_count_total,
                        documented=spiders_count_documented
                    )
                )
            else:
                print(output)
