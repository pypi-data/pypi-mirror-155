#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
# Made available under the terms of the MIT License, see LICENSE.txt
# Copyright 2019-2022 Kevin Locke <kevin@kevinlocke.name>
"""Functions and classes for converting iCalendar to CSV for Todoist."""

import argparse
import csv
import logging
import os.path
import re
import sys

from datetime import date, datetime
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Iterator,
    Optional,
    Sequence,
    cast,
)
from urllib.request import urlopen
from xml.sax.saxutils import escape as html_escape  # nosec:B406

from html2text import HTML2Text
from icalendar import Calendar, Todo, vText  # type: ignore

try:
    from argcomplete import autocomplete  # type: ignore
except ImportError:
    autocomplete = None

if TYPE_CHECKING:
    import _csv

    from _typeshed import SupportsWrite

if not hasattr(argparse, 'BooleanOptionalAction'):
    # Define BooleanOptionalAction for Python < 3.8
    # Based on Lib/argparse.py in Python 3.10.5
    class BooleanOptionalAction(argparse.Action):  # noqa: D101
        # pylint: disable-next=too-many-arguments
        def __init__(  # noqa: D107
            self,
            option_strings: Iterator[str],
            dest: str,
            default: Any = None,
            # pylint: disable-next=redefined-builtin
            type: Optional[Callable[[str], Any]] = None,
            choices: Optional[Sequence[str]] = None,
            required: bool = False,
            help: Optional[str] = None,  # pylint: disable=redefined-builtin
            metavar: Optional[str] = None,
        ) -> None:  # noqa: D107

            _option_strings = []
            for option_string in option_strings:
                _option_strings.append(option_string)

                if option_string.startswith('--'):
                    option_string = '--no-' + option_string[2:]
                    _option_strings.append(option_string)

            super().__init__(
                option_strings=_option_strings,
                dest=dest,
                nargs=0,
                default=default,
                type=type,
                choices=choices,
                required=required,
                help=help,
                metavar=metavar,
            )

        def __call__(  # noqa: D102
            self,
            parser: argparse.ArgumentParser,
            namespace: argparse.Namespace,
            values: Any,
            option_string: Optional[str] = None,
        ) -> None:  # noqa: D102
            if option_string in self.option_strings:
                setattr(
                    namespace,
                    self.dest,
                    not cast(str, option_string).startswith('--no-'),
                )

        # pylint: disable-next=missing-return-doc
        def format_usage(self) -> str:  # noqa: D102
            return ' | '.join(self.option_strings)

else:
    BooleanOptionalAction = argparse.BooleanOptionalAction  # type: ignore


# Note: Must comply with https://peps.python.org/pep-0440/
__version__ = '0.1.0'

__main__ = [
    'Ics2TodoistConverter',
    'TodoistCsvRow',
    'ics_to_todoist',
    'main',
    'write_csv_header',
]

# Short license message varies by license.
# The text below is based on the GPL short text, modified for the MIT License.
# Change as appropriate.
_VERSION_MESSAGE = (
    '%(prog)s '
    + __version__
    + '''

Copyright 2019-2022 Kevin Locke <kevin@kevinlocke.name>

%(prog)s is free software; you can redistribute it and/or modify
it under the terms of the MIT License.

%(prog)s is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
the terms of the MIT License for more details.'''
)

# Match https://github.github.com/gfm/#autolinks which would match
# https://github.github.com/gfm/#extended-url-autolink without <>
_autolinkre = re.compile(
    r'''
   (?:^|(?<=[\s*_~(]))          # recognized autolinks can only...
   <                            # begin autolink
   (?P<url>                     # begin URL capture
   https?://                    # extended url autolink schemes
   (?:[a-zA-Z0-9_-]+\.)*        # valid domain segments with _
   [a-zA-Z0-9-]+\.[a-zA-Z0-9-]+ # last 2 segments
   (?![^a-zA-Z0-9_-])           # _ not allowed in last segment
   [^\0-\x20<>\x7f]*            # not ASCII whitespace, ctrl, <>
   (?<![?!.,:*_~;)])            # no ambiguous trailing punctuation
   )                            # end URL capture
   >                            # end autolink
   (?![?!.,:*_~;)]*[^\0-\x20?!.,:*_~;)<>\x7f])  # not part of path
   ''',
    re.ASCII | re.MULTILINE | re.VERBOSE,
)
_logger = logging.getLogger(__name__)


class _TodoistHTML2Text(HTML2Text):
    """
    HTML2Text subclass with ics2todoist workarounds.

    Currently includes workarounds for:
    - https://github.com/Alir3z4/html2text/issues/383
    """

    def handle_charref(self, c: str) -> None:
        charref = self.charref(c)
        if not self.code and not self.pre:
            charref = html_escape(charref)
        self.handle_data(charref, True)

    def handle_entityref(self, c: str) -> None:
        entityref = self.entityref(c)
        if (
            not self.code
            and not self.pre
            and entityref != '&nbsp_place_holder;'
        ):
            entityref = html_escape(entityref)
        if entityref:
            self.handle_data(entityref, True)


# pylint: disable-next=too-few-public-methods,too-many-instance-attributes
class TodoistCsvRow:
    """
    A row of Todoist CSV data.

    Columns are described in `How to format your CSV file so you can import it
    into Todoist
    <https://todoist.com/help/articles/how-to-format-your-csv-file-so-you-can-import-it-into-todoist>`_.
    """

    __slots__ = (
        'type',
        'content',
        'description',
        'priority',
        'indent',
        'author',
        'responsible',
        'date',
        'date_lang',
        'timezone',
    )

    def __init__(self) -> None:
        """Initialize a task row with no additional data."""
        self.type = 'task'
        self.content: Optional[str] = None
        self.description: Optional[str] = None
        self.priority: Optional[int] = None
        self.indent: Optional[int] = None
        self.author: Optional[str] = None
        self.responsible: Optional[str] = None
        self.date: Optional[str | date | datetime] = None
        self.date_lang: Optional[str] = None
        self.timezone: Optional[str] = None

    def __iter__(self) -> Iterator[Optional[str]]:
        """
        Iterate over the columns of this row.

        :return: Iterator over column values.
        """
        yield self.type
        yield self.content
        yield self.description
        yield str(self.priority) if self.priority is not None else None
        yield str(self.indent) if self.priority is not None else None
        yield self.author
        yield self.responsible
        if isinstance(self.date, datetime):
            # Note: datetime.__str__() uses space as the date/time separator,
            # which causes Todoist not to recognize the timezone offset (and
            # perhaps depend on date_lang for parsing?).
            # Serialize to string with T separator to get reliable results.
            yield self.date.isoformat()
        else:
            yield str(self.date) if self.date is not None else None
        yield self.date_lang
        yield self.timezone


class Ics2TodoistConverter:
    """Converter from iCalendar values to Todoist CSV values."""

    _bare_autolinks: bool
    _default_priority: Optional[int]
    _html2text: HTML2Text
    _include_completed: bool
    _text_is_markdown: bool
    _warn_completed: bool

    def __init__(
        self,
        *,
        bare_autolinks: bool = False,
        default_priority: Optional[int] = None,
        include_completed: Optional[bool] = None,
        text_is_markdown: bool = False,
    ) -> None:
        """Initialize a converter with given options."""
        self._bare_autolinks = bare_autolinks
        self._default_priority = default_priority
        self._html2text = _TodoistHTML2Text(bodywidth=0)
        self._include_completed = include_completed or False
        self._text_is_markdown = text_is_markdown
        self._warn_completed = include_completed is None

    def category_to_label(self, category: str) -> str:
        """
        Convert an iCalendar category to a Todoist label.

        Currently removes forbidden characters listed in the `Introduction
        to Labels <https://todoist.com/help/articles/introduction-to-labels>`.

        :param category: Category from iCalendar categories property to
                         convert.
        :return: ``category`` sanitized for use as a Todoist label.
        """
        return re.sub('[ @"()|&!]+', '_', category.strip())

    def priority_to_priority(self, prio: int) -> Optional[int]:
        """
        Convert an iCalendar priority to a Todoist priority.

        See `Introduction to: Priorities
        <https://todoist.com/hc/en-us/articles/205873321>`_.

        :param prio: iCalendar priority (0-9) to convert.
        :return: Todoist priority corresponding to ``prio``, or ``None`` if
                 ``prio`` is ``0``.
        """
        # Note: 0 is "an undefined priority"
        # https://datatracker.ietf.org/doc/html/rfc5545#section-3.8.1.9
        if prio == 0:
            return None

        if prio >= 7:
            return 4

        return (prio + 1) // 2

    def markdown_to_todoist(self, markdown: str) -> str:
        """
        Convert generic Markdown to Todoist Markdown.

        Todoist Markdown is described in `Text formatting
        <https://todoist.com/help/articles/text-formatting>`_.

        This method currently removes some superfluous whitespace and
        strips angle brackets from autolinks if requested.

        :param markdown: Markdown content to convert.
        :return: Markdown content suitable for Todoist.
        """
        # Spaces at start and end are superfluous.
        todoist = markdown.strip()
        # Spaces before newlines are superfluous.
        todoist = re.sub('[\t ]+\n', '\n', todoist)
        # More than 2 consecutive newlines are superfluous.
        todoist = re.sub('\n{3,}', '\n\n', todoist)
        # Strip angle brackets from autolinks, if requested
        if self._bare_autolinks:
            todoist = _autolinkre.sub(r'\g<url>', todoist)
        return todoist

    def html_to_todoist(self, html: str) -> str:
        """
        Convert HTML to Todoist Markdown.

        Todoist Markdown is described in `Text formatting
        <https://todoist.com/help/articles/text-formatting>`_.

        :param html: HTML content to convert.
        :return: Markdown content suitable for Todoist.
        """
        markdown = self._html2text.handle(html)
        return self.markdown_to_todoist(markdown)

    def text_to_todoist(self, text: str) -> str:
        """
        Convert text to Todoist Markdown.

        Todoist Markdown is described in `Text formatting
        <https://todoist.com/help/articles/text-formatting>`_.

        This method currently adds backslashes to escape text which would
        otherwise be interpreted as Markdown formatting.

        :param text: Text content to convert.
        :return: Markdown content suitable for Todoist.
        """
        text = text.rstrip()
        # Escape unrestricted Markdown metacharacters
        text = re.sub(r'[\\`[]', r'\\\g<0>', text)
        # Escape < when followed by an alnum
        text = re.sub(r'<(?=\w)', r'\\\g<0>', text)
        # Escape bullet list markers and blockquotes
        text = re.sub(r'^(\s*)([+*>-]\s)', r'\1\\\2', text)
        # Escape ATX headings
        text = re.sub(r'^(\s*)(#{1,6}\s)', r'\1\\\2', text)
        # Escape left-flanking runs of *
        text = re.sub(r'[*]+(?![*\s]|$)', r'\\\g<0>', text)
        # Escape _ only when not preceded by a letter or followed by space
        # since in CommonMark "intraword emphasis is disallowed for _"
        text = re.sub(r'(?<!\w)_(?!\s)', r'\\\g<0>', text)
        return text

    def vtext_to_todoist(self, vtext: vText) -> str:
        """
        Convert :class:`icalendar.prop.vText` to Todoist Markdown.

        :param vtext: iCalendar VTEXT component to convert.
        :return: Markdown content suitable for Todoist.
        """
        # Thunderbird stores HTML as a data: URI in the ALTREP parameter
        altrep = vtext.params.get('altrep', '')
        if altrep.startswith('data:text/html,'):
            # Parse data: URI with urllib: https://stackoverflow.com/a/58633199
            with urlopen(altrep) as response:  # nosec:B310
                html = response.read().decode('utf-8')
            todoist = self.html_to_todoist(html)
        elif self._text_is_markdown:
            todoist = self.markdown_to_todoist(vtext)
        else:
            todoist = self.text_to_todoist(vtext)

        # Note: Todoist exports \n in values and \r\n between rows, like Excel
        # https://stackoverflow.com/a/9512606
        # Don't convert \n to \r\n in description
        return todoist

    def todo_to_todoist(self, todo: Todo) -> TodoistCsvRow:
        """
        Convert a :class:`icalendar.cal.Todo` to Todoist CSV.

        :param todo: iCalendar VTODO component to convert.
        :return: A row of Todoist CSV data.
        """
        desc = todo.get('description')
        prio = int(todo.get('priority', 0))
        summary = todo.get('summary', '')
        categories = todo.get('categories')
        due = todo.get('due', todo.get('dtstart'))

        if todo.get('rrule') or todo.get('rdate'):
            # FIXME: Convert iCalendar recurrence rules (and recurrence dates?)
            # https://www.rfc-editor.org/rfc/rfc5545.html#section-3.8.5.3
            # to Todoist recurring due date format
            # https://todoist.com/help/articles/set-a-recurring-due-date#how-to-set-a-recurring-due-date
            # Note: Probably need to set date_lang for recurrence format used
            _logger.warning(
                'Recurring dates are not currently converted to Todoist'
            )

        # categories is [vCategory] if it appears multiple times
        if isinstance(categories, list):
            cats = [cat for vcat in categories for cat in vcat.cats]
        elif categories:
            cats = categories.cats
        else:
            cats = None

        row = TodoistCsvRow()
        if summary:
            row.content = self.vtext_to_todoist(summary)
        if cats:
            labels = ' '.join('@' + self.category_to_label(cat) for cat in cats)
            if row.content:
                row.content += ' ' + labels
            else:
                row.content = labels
        if desc is not None:
            row.description = self.vtext_to_todoist(desc)
        row.priority = self.priority_to_priority(prio) or self._default_priority
        if due is not None:
            row.date = due_dt = due.dt
            # date_lang must be non-empty for date to be imported
            row.date_lang = 'en'
            # Pass along the Time Zone Identifier, if present
            # https://www.rfc-editor.org/rfc/rfc5545.html#section-3.2.19
            tzid = due.params.get('TZID')
            if tzid:
                row.timezone = tzid
            elif isinstance(due_dt, datetime) and due_dt.tzinfo is not None:
                row.timezone = due_dt.tzinfo.tzname(due_dt)
        return row

    def calendar_to_todoist(self, cal: Calendar) -> Iterator[TodoistCsvRow]:
        """
        Convert a :class:`icalendar.cal.Calendar` to Todoist CSV rows.

        :param cal: iCalendar to convert.
        :return: Todoist CSV data for each VTODO component in ``cal``.
        """
        for todo in cal.walk('vtodo'):
            # Don't export vtodos which have been COMPLETED, since Todoist
            # does not have a way to import completed todos
            if not self._include_completed and todo.get('COMPLETED'):
                if self._warn_completed:
                    _logger.warning('Skipping completed vtodo(s).')
                    self._warn_completed = False
                continue

            # Don't export overridden instances of a recurrence set.
            # These are changes to a specific occurrence of a recurring task.
            # Often the only difference is a COMPLETED property to mark a
            # specific occurrence of a task as completed at a particular time.
            #
            # TODO: Does Todoist support overrides in recurring date strings?
            # https://todoist.com/help/articles/set-a-recurring-due-date#how-to-set-a-recurring-due-date
            if todo.get('RECURRENCE-ID'):
                continue

            yield self.todo_to_todoist(todo)

    def ical_to_todoist(self, ical: str) -> Iterator[TodoistCsvRow]:
        """
        Convert a string of iCalendar data to Todoist CSV rows.

        :param ical: iCalendar data to convert.
        :return: Todoist CSV data for each VTODO component in ``cal``.
        """
        for cal in Calendar.from_ical(ical, multiple=True):
            yield from self.calendar_to_todoist(cal)


def _build_argument_parser(**kwargs: Any) -> argparse.ArgumentParser:
    """
    Build parser for command line options.

    :return: argument parser
    """
    parser = argparse.ArgumentParser(
        usage='%(prog)s [options] [ics_file...]',
        description='Convert iCalendar to Todoist CSV',
        # Use raw formatter to avoid mangling version text
        formatter_class=argparse.RawDescriptionHelpFormatter,
        **kwargs,
    )
    parser.add_argument(
        '--bare-autolinks',
        action='store_true',
        help='Remove angle brackets around autolinkable URLs',
    )
    parser.add_argument(
        '--default-priority',
        type=int,
        choices=range(1, 5),
        help='Priority of tasks without an iCalendar priority',
    )
    parser.add_argument(
        '--include-completed',
        action=BooleanOptionalAction,
        help='Include VTODOs which have been completed in CSV',
    )
    parser.add_argument(
        '-o',
        '--output',
        type=argparse.FileType('w'),
        default='-',
        help='Output file, - for stdout',
    )
    parser.add_argument(
        '-q',
        '--quiet',
        action='count',
        help='Decrease verbosity (less detailed status output)',
    )
    parser.add_argument(
        '--text-is-markdown',
        action='store_true',
        help='Treat text in iCalendar as Markdown',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        help='Increase verbosity (more detailed status output)',
    )
    parser.add_argument(
        '-V',
        '--version',
        action='version',
        help='Output version and license information',
        version=_VERSION_MESSAGE,
    )
    parser.add_argument(
        'input_files',
        default=['-'],
        nargs='*',
        metavar='ics_file...',
        help='iCalendar file(s) to convert, - for stdin',
    )
    return parser


def write_csv_header(csvwriter: '_csv._writer') -> None:
    """
    Write the CSV header line to a given CSV writer.

    :param csvwriter: CSV writer to which the header will be written.
    """
    csvwriter.writerow(s.upper() for s in TodoistCsvRow.__slots__)


def ics_to_todoist(
    icspaths: Iterator[str],
    todoist: 'SupportsWrite[str]',
    *,
    bare_autolinks: bool = False,
    default_priority: Optional[int] = None,
    include_completed: Optional[bool] = False,
    text_is_markdown: bool = False,
) -> None:
    """
    Convert iCalendar files to Todoist CSV.

    :param icspaths: Paths of iCalendar files to convert.
    :param todoist: Writable file for Todoist CSV data.
    :param bare_autolinks: Don't surround URLs with angle brackets if Todoist
                           will recognize them as links automatically.
    :param default_priority: Priority of Todoist tasks when not specified by
                             iCalendar data.
    :param include_completed: Include VTODOs which have been completed in CSV.
    :param text_is_markdown: Treat iCalendar text as being in Markdown format.
    """
    # Write a UTF byte-order-mark to match Todoist export (and Excel)
    todoist.write('\ufeff')
    todoistcsv = csv.writer(todoist)
    write_csv_header(todoistcsv)
    converter = Ics2TodoistConverter(
        bare_autolinks=bare_autolinks,
        default_priority=default_priority,
        include_completed=include_completed,
        text_is_markdown=text_is_markdown,
    )
    for icspath in icspaths:
        # Inform users about reading from a TTY, which can be surprising
        if icspath == '-' and sys.stdin.isatty():
            _logger.info('Reading iCalendar data from stdin...')

        # Note: iCalendar must be UTF-8 or US-ASCII:
        # https://datatracker.ietf.org/doc/html/rfc5545#section-6
        with open(
            icspath, encoding='utf-8'
        ) if icspath != '-' else sys.stdin as icsfile:
            cal = icsfile.read()

        wroterow = False
        for row in converter.ical_to_todoist(cal):
            todoistcsv.writerow(row)
            wroterow = True

        if not wroterow:
            _logger.warning('No VTODO components in %s', icspath)


# pylint: disable-next=dangerous-default-value
def main(argv: Sequence[str] = sys.argv) -> int:
    """
    Entry point for packagename command-line tool.

    :param argv: command-line arguments

    :return: exit code
    """
    parser = _build_argument_parser(
        prog=os.path.basename(argv[0]),
    )

    if autocomplete:
        exit_code = None

        def exit_method(code: int = 0) -> None:
            nonlocal exit_code
            exit_code = code

        autocomplete(parser, exit_method=exit_method)
        if exit_code is not None:
            return exit_code

    args = parser.parse_args(args=argv[1:])

    # Set log level based on verbosity requested (default of INFO)
    verbosity = (args.quiet or 0) - (args.verbose or 0)
    logging.basicConfig(
        format='%(levelname)s:%(message)s',
        level=logging.INFO + verbosity * 10,
    )

    # Log version to aid debugging
    _logger.debug('ics2todoist %s', __version__)

    try:
        ics_to_todoist(
            args.input_files,
            args.output,
            bare_autolinks=args.bare_autolinks,
            default_priority=args.default_priority,
            include_completed=args.include_completed,
            text_is_markdown=args.text_is_markdown,
        )
    except Exception as exc:  # pylint: disable=broad-except
        _logger.error('Unhandled Error: %s', exc, exc_info=True)
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
