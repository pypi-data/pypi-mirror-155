"""ics2todoist.cli unit tests."""

from io import StringIO
from unittest.mock import Mock, patch

import pytest

import ics2todoist


@patch('sys.stdout', new_callable=StringIO)
@patch('sys.stderr', new_callable=StringIO)
def test_main_help_prints_usage_then_exits(
    mock_stderr: Mock, mock_stdout: Mock
) -> None:
    with pytest.raises(SystemExit) as excinfo:
        ics2todoist.main(['ics2todoist', '--help'])
    stderr_content = mock_stderr.getvalue()
    stdout_content = mock_stdout.getvalue()
    assert not stderr_content
    assert '--quiet' in stdout_content
    assert '--verbose' in stdout_content
    assert excinfo.value.code == 0
