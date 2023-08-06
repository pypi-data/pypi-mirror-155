"""Ics2TodoistConverter unit tests."""

from datetime import date, datetime, timedelta, timezone
from typing import Optional
from urllib.parse import quote
from uuid import uuid4

import pytest

from ics2todoist import Ics2TodoistConverter

_DATE_LANGS = [
    'da',
    'de',
    'en',
    'es',
    'fi',
    'fr',
    'it',
    'ja',
    'ko',
    'nb',
    'nl',
    'pl',
    'pt_BR',
    'ru',
    'sv',
    'zh_CN',
]


def _wrap_vtodo(ical: str) -> str:
    """
    Wrap a string of VTODO props with required VTODO and VCALENDAR props.

    :param ical: String of VTODO properties.
    :return: String of iCalendar data with VTODO section including ical.
    """
    return f'''BEGIN:VCALENDAR\r
VERSION:2.0\r
PRODID:ics2todoist tests\r
BEGIN:VTODO\r
UID:{uuid4()}\r
DTSTAMP:20220101T000000Z\r
{ical}\r
END:VTODO\r
END:VCALENDAR\r
'''


def test_type_task() -> None:
    converter = Ics2TodoistConverter()
    ical = _wrap_vtodo('')
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.type == 'task'


def test_summary_to_content() -> None:
    converter = Ics2TodoistConverter()
    summary = 'An example summary'
    ical = _wrap_vtodo(f'SUMMARY:{summary}')
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.content == summary


def test_html_summary_to_summary() -> None:
    converter = Ics2TodoistConverter()
    hsummary = '<body>\nA <b>bold</b> example.</body>'
    msummary = 'A **bold** example.'
    tsummary = 'A bold example.'
    ical = _wrap_vtodo(
        f'SUMMARY;ALTREP="data:text/html,{quote(hsummary)}":{tsummary}'
    )
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.content == msummary


def test_markdown_summary_to_summary() -> None:
    converter = Ics2TodoistConverter(text_is_markdown=True)
    msummary = 'A **bold** example.'
    ical = _wrap_vtodo(f'SUMMARY:{msummary}')
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.content == msummary


def test_description_to_description() -> None:
    converter = Ics2TodoistConverter()
    description = 'An example description.'
    ical = _wrap_vtodo(f'DESCRIPTION:{description}')
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.description == description


def test_html_description_to_description() -> None:
    converter = Ics2TodoistConverter()
    hdesc = '<body>\nA <b>bold</b> example.</body>'
    mdesc = 'A **bold** example.'
    tdesc = 'A bold example.'
    ical = _wrap_vtodo(
        f'DESCRIPTION;ALTREP="data:text/html,{quote(hdesc)}":{tdesc}'
    )
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.description == mdesc


def test_markdown_description_to_description() -> None:
    converter = Ics2TodoistConverter(text_is_markdown=True)
    mdesc = 'A **bold** example.'
    ical = _wrap_vtodo(f'DESCRIPTION:{mdesc}')
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.description == mdesc


@pytest.mark.parametrize(
    'text,markdown',
    [
        ('An [example]', r'An \[example]'),
        ('An `example`', r'An \`example\`'),
        ('An exam\\ple', r'An exam\\ple'),
        ('An <example>', r'An \<example>'),
        ('1 < 2', r'1 < 2'),
        ('* Item 1', r'\* Item 1'),
        (' * Item 1', r' \* Item 1'),
        ('- Item 1', r'\- Item 1'),
        (' - Item 1', r' \- Item 1'),
        ('+ Item 1', r'\+ Item 1'),
        (' + Item 1', r' \+ Item 1'),
        ('> Quoted', r'\> Quoted'),
        (' > Quoted', r' \> Quoted'),
        ('# Heading', r'\# Heading'),
        (' # Heading', r' \# Heading'),
        ('## Heading 2', r'\## Heading 2'),
        (' ## Heading 2', r' \## Heading 2'),
        ('Not end *emphasized*', r'Not end \*emphasized*'),
        ('Not *emphasized* mid', r'Not \*emphasized* mid'),
        ('Not end _emphasized_', r'Not end \_emphasized_'),
        ('Not _emphasized_ mid', r'Not \_emphasized_ mid'),
        ('Not my_word', r'Not my_word'),
        ('Not end **strong**', r'Not end \**strong**'),
        ('Not **strong** mid', r'Not \**strong** mid'),
    ],
)
def test_text_to_markdown(text: str, markdown: str) -> None:
    converter = Ics2TodoistConverter()
    ical = _wrap_vtodo(f'''SUMMARY:{text}\r\nDESCRIPTION:{text}''')
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.description == markdown
    assert todoist.content == markdown


def test_category_without_summary() -> None:
    converter = Ics2TodoistConverter()
    category = 'Test'
    ical = _wrap_vtodo(f'CATEGORIES:{category}')
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.content == f'@{category}'


# https://github.com/Alir3z4/html2text/issues/383
def test_preserves_html_charref() -> None:
    converter = Ics2TodoistConverter()
    hdesc = '<body>\nAdd &lt;hr&gt; to page.</body>'
    mdesc = 'Add &lt;hr&gt; to page.'
    tdesc = 'Add <hr> to page.'
    ical = _wrap_vtodo(
        f'DESCRIPTION;ALTREP="data:text/html,{quote(hdesc)}":{tdesc}'
    )
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.description == mdesc


def test_html_charref_in_code() -> None:
    converter = Ics2TodoistConverter()
    hdesc = '<body>\nAdd <code>&lt;hr&gt;</code> to page.</body>'
    mdesc = 'Add `<hr>` to page.'
    tdesc = 'Add <hr> to page.'
    ical = _wrap_vtodo(
        f'DESCRIPTION;ALTREP="data:text/html,{quote(hdesc)}":{tdesc}'
    )
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.description == mdesc


# iCalendar priority 1-9 maps to Todoist 1-4.
# iCalendar "0 specifies an undefined priority"
# https://datatracker.ietf.org/doc/html/rfc5545#section-3.8.1.9
@pytest.mark.parametrize(
    'iprio,tprio',
    [
        (None, None),
        (0, None),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 2),
        (5, 3),
        (6, 3),
        (7, 4),
        (8, 4),
        (9, 4),
    ],
)
def test_priority_to_priority(
    iprio: Optional[int],
    tprio: Optional[int],
) -> None:
    converter = Ics2TodoistConverter()
    ical = _wrap_vtodo(
        f'PRIORITY:{iprio}' if iprio is not None else '',
    )
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.priority == tprio


def test_due_date_to_date() -> None:
    converter = Ics2TodoistConverter()
    tdate = date(2022, 5, 20)
    ical = _wrap_vtodo('DUE:20220520')
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.date == tdate
    assert todoist.date_lang in _DATE_LANGS
    assert todoist.timezone is None


def test_due_date_to_datetime_utc() -> None:
    converter = Ics2TodoistConverter()
    tdate = datetime(2022, 5, 20, 8, 4, 11, tzinfo=timezone.utc)
    ical = _wrap_vtodo('DUE:20220520T080411Z')
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.date == tdate
    assert todoist.date_lang in _DATE_LANGS
    assert todoist.timezone == 'UTC'


def test_due_date_to_datetime_notz() -> None:
    converter = Ics2TodoistConverter()
    tdate = datetime(2022, 5, 20, 8, 4, 11)
    ical = _wrap_vtodo('DUE:20220520T080411')
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.date == tdate
    assert todoist.date_lang in _DATE_LANGS
    assert todoist.timezone is None


def test_due_date_to_datetime_tzid() -> None:
    converter = Ics2TodoistConverter()
    tdate = datetime(2022, 5, 20, 8, 4, 11)
    ical = _wrap_vtodo('DUE;TZID=America/New_York:20220520T080411')
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    # icalendar currently returns tzinfo from pytz.timezone()
    # test that tzinfo has expected offset, not specific pytz implementation
    actual_date = todoist.date
    assert isinstance(actual_date, datetime)
    assert actual_date.replace(tzinfo=None) == tdate
    assert actual_date.utcoffset() == timedelta(hours=-4)
    assert todoist.date_lang in _DATE_LANGS
    assert todoist.timezone == 'America/New_York'


def test_dtstart_date_to_date() -> None:
    converter = Ics2TodoistConverter()
    tdate = date(2022, 5, 20)
    ical = _wrap_vtodo('DTSTART:20220520')
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.date == tdate
    assert todoist.date_lang in _DATE_LANGS
    assert todoist.timezone is None


def test_dtstart_date_to_datetime_utc() -> None:
    converter = Ics2TodoistConverter()
    tdate = datetime(2022, 5, 20, 8, 4, 11, tzinfo=timezone.utc)
    ical = _wrap_vtodo('DTSTART:20220520T080411Z')
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.date == tdate
    assert todoist.date_lang in _DATE_LANGS
    assert todoist.timezone == 'UTC'


def test_prefer_dtstart_due_to_date() -> None:
    converter = Ics2TodoistConverter()
    tdate = date(2022, 5, 21)
    ical = _wrap_vtodo('DTSTART:20220520\r\nDUE:20220521')
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.date == tdate
    assert todoist.date_lang in _DATE_LANGS
    assert todoist.timezone is None


def test_prefer_due_dtstart_to_date() -> None:
    converter = Ics2TodoistConverter()
    tdate = date(2022, 5, 20)
    ical = _wrap_vtodo('DUE:20220520\r\nDTSTART:20220521')
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.date == tdate
    assert todoist.date_lang in _DATE_LANGS
    assert todoist.timezone is None


def test_category_appended_to_content() -> None:
    converter = Ics2TodoistConverter()
    summary = 'Example summary'
    category = 'Test'
    ical = _wrap_vtodo(f'SUMMARY:{summary}\r\nCATEGORIES:{category}')
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.content == f'{summary} @{category}'


def test_category_invalid_char_to_underscore() -> None:
    converter = Ics2TodoistConverter()
    summary = 'Example summary'
    category = 'Test Stuff'
    label = 'Test_Stuff'
    ical = _wrap_vtodo(f'SUMMARY:{summary}\r\nCATEGORIES:{category}')
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.content == f'{summary} @{label}'


def test_category_invalid_chars_to_one_underscore() -> None:
    converter = Ics2TodoistConverter()
    summary = 'Example summary'
    category = 'Test & Stuff'
    label = 'Test_Stuff'
    ical = _wrap_vtodo(f'SUMMARY:{summary}\r\nCATEGORIES:{category}')
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.content == f'{summary} @{label}'


def test_combined_categories_appended_to_content() -> None:
    converter = Ics2TodoistConverter()
    summary = 'Example summary'
    category1 = 'Test1'
    category2 = 'Test2'
    ical = _wrap_vtodo(
        f'SUMMARY:{summary}\r\nCATEGORIES:{category1},{category2}'
    )
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.content == f'{summary} @{category1} @{category2}'


def test_separate_categories_appended_to_content() -> None:
    converter = Ics2TodoistConverter()
    summary = 'Example summary'
    category1 = 'Test1'
    category2 = 'Test2'
    ical = _wrap_vtodo(
        f'SUMMARY:{summary}\r\nCATEGORIES:{category1}\r\nCATEGORIES:{category2}'
    )
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.content == f'{summary} @{category1} @{category2}'


def test_bare_autolinks_default() -> None:
    converter = Ics2TodoistConverter()
    hdesc = (
        '<body>\nCheck'
        + ' <a href="https://example.com">https://example.com</a>'
        + ' for HTTPS.</body>'
    )
    mdesc = 'Check <https://example.com> for HTTPS.'
    tdesc = 'Check https://example.com for HTTPS.'
    ical = _wrap_vtodo(
        f'DESCRIPTION;ALTREP="data:text/html,{quote(hdesc)}":{tdesc}'
    )
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.description == mdesc


def test_bare_autolinks_true() -> None:
    converter = Ics2TodoistConverter(bare_autolinks=True)
    hdesc = (
        '<body>\nCheck'
        + ' <a href="https://example.com">https://example.com</a>'
        + ' for HTTPS.</body>'
    )
    mdesc = 'Check https://example.com for HTTPS.'
    tdesc = 'Check https://example.com for HTTPS.'
    ical = _wrap_vtodo(
        f'DESCRIPTION;ALTREP="data:text/html,{quote(hdesc)}":{tdesc}'
    )
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.description == mdesc


def test_default_priority() -> None:
    defprio = 3
    converter = Ics2TodoistConverter(default_priority=defprio)
    ical = _wrap_vtodo('')
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.priority == defprio


def test_default_priority_zero() -> None:
    defprio = 3
    converter = Ics2TodoistConverter(default_priority=defprio)
    ical = _wrap_vtodo('PRIORITY:0')
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.priority == defprio


def test_multiple_icalendars() -> None:
    converter = Ics2TodoistConverter()
    summary1 = 'Task 1'
    ical1 = _wrap_vtodo(f'SUMMARY:{summary1}')
    summary2 = 'Task 2'
    ical2 = _wrap_vtodo(f'SUMMARY:{summary2}')
    todoists = list(converter.ical_to_todoist(ical1 + ical2))
    assert len(todoists) == 2
    assert todoists[0].content == summary1
    assert todoists[1].content == summary2


def test_include_completed_default() -> None:
    converter = Ics2TodoistConverter()
    summary1 = 'Task 1'
    ical1 = _wrap_vtodo(f'SUMMARY:{summary1}\r\nCOMPLETED:20220520T080411Z')
    summary2 = 'Task 2'
    ical2 = _wrap_vtodo(f'SUMMARY:{summary2}')
    todoists = list(converter.ical_to_todoist(ical1 + ical2))
    assert len(todoists) == 1
    assert todoists[0].content == summary2


def test_include_completed_false() -> None:
    converter = Ics2TodoistConverter(include_completed=False)
    summary1 = 'Task 1'
    ical1 = _wrap_vtodo(f'SUMMARY:{summary1}')
    summary2 = 'Task 2'
    ical2 = _wrap_vtodo(f'SUMMARY:{summary2}\r\nCOMPLETED:20220520T080411Z')
    todoists = list(converter.ical_to_todoist(ical1 + ical2))
    assert len(todoists) == 1
    assert todoists[0].content == summary1


def test_include_completed_true() -> None:
    converter = Ics2TodoistConverter(include_completed=True)
    summary1 = 'Task 1'
    ical1 = _wrap_vtodo(f'SUMMARY:{summary1}\r\nCOMPLETED:20220520T080411Z')
    summary2 = 'Task 2'
    ical2 = _wrap_vtodo(f'SUMMARY:{summary2}')
    todoists = list(converter.ical_to_todoist(ical1 + ical2))
    assert len(todoists) == 2
    assert todoists[0].content == summary1
    assert todoists[1].content == summary2


def test_recurrence_master_only() -> None:
    converter = Ics2TodoistConverter()
    summary = 'Prepare for weekly Tuesday meeting'
    uuid = uuid4()
    tdate = datetime(2022, 1, 4, 9, 30, 0, tzinfo=timezone.utc)
    ical = f'''BEGIN:VCALENDAR\r
VERSION:2.0\r
PRODID:ics2todoist tests\r
BEGIN:VTODO\r
UID:{uuid}\r
DTSTAMP:20220101T000000Z\r
DTSTART:20220104T093000Z\r
RRULE:FREQ=WEEKLY\r
SUMMARY:{summary}\r
END:VTODO\r
BEGIN:VTODO\r
UID:{uuid}\r
DTSTAMP:20220104T094515Z\r
DTSTART:20220112T093000Z\r
RECURRENCE-ID:20220111T093000Z\r
SUMMARY:{summary}\r
DESCRIPTION:Moved to Wednesday this week\r
END:VTODO\r
END:VCALENDAR\r'''
    todoists = list(converter.ical_to_todoist(ical))
    assert len(todoists) == 1
    todoist = todoists[0]
    assert todoist.content == summary
    assert todoist.date == tdate
    assert todoist.date_lang in _DATE_LANGS
    assert todoist.timezone == 'UTC'
