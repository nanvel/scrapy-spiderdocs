from __future__ import print_function

import re

from scrapy.commands import ScrapyCommand
from scrapy.exceptions import UsageError


__all__ = ('Command',)


INDENT_RE = re.compile('^(\s+)')


def get_line_indent(line):
    matches = INDENT_RE.match(line)
    return matches and len(matches.groups()[0]) or 0


class SpiderDocsSection:

    _name = None
    _lines = []

    def __init__(self, name, processor=None):
        self._name = name
        self._processor = processor

    def append(self, line):
        self._lines.append(line)

    def to_md(self):
        lines = '\n'.join(self._lines).strip()

        if self._processor:
            lines = self._processor(lines)

        return "### {name}\n\n{lines}\n".format(
            name=self._name,
            lines=lines
        )

class Command(ScrapyCommand):

    requires_project = True
    default_settings = {
        # {<module>: <destination>}
        'SPIDERDOCS_LOCATIONS': {},
        # {<section_name>: <function>}
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

            for spider_name in self.crawler_process.spider_loader.list():
                spider = self.crawler_process.spider_loader.load(spider_name)

                if not spider.__module__.startswith(module):
                    continue

                output.append("## {spider_name} [{module_name}.{class_name}]".format(
                    spider_name=spider.name,
                    module_name=spider.__module__,
                    class_name=spider.__name__
                ))

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
                            output.append(current_section.to_md())

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
                    output.append(current_section.to_md())

            output = '\n\n'.join(output)

            if location:
                with open(location, 'w') as f:
                    f.write(output)
            else:
                print(output)
