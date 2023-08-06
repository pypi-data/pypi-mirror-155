# SPDX-License-Identifier: CC0-1.0

# Copyright (C) 2022 Wojtek Kosior <koszko@koszko.org>
#
# Available under the terms of Creative Commons Zero v1.0 Universal.

import sys
from pathlib import Path

import pytest
import pkgutil
import importlib
import functools
from tempfile import TemporaryDirectory
from typing import Iterable

here = Path(__file__).resolve().parent
sys.path.insert(0, str(here / 'src'))

@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """Remove requests.sessions.Session.request for all tests."""
    if importlib.util.find_spec("requests") is not None:
        monkeypatch.delattr('requests.sessions.Session.request')

def _mock_subprocess_run(monkeypatch, where, mocked_run):
    """Temporarily replace subprocess.run() with the given function."""
    class MockedSubprocess:
        """Minimal mocked version of the subprocess module."""
        run = mocked_run

    monkeypatch.setattr(where, 'subprocess', MockedSubprocess)

@pytest.fixture
def mock_subprocess_run(monkeypatch, request):
    """
    Facilitate temporarily replacing subprocess.run() with a different function.

    If the 'subprocess_run' pytest marker has been used, perform the replacement
    for the module-function pair supplied through it.

    Return a function that can be called to perform the same replacement in
    another fixture or from inside a test function.
    """
    mocker = functools.partial(_mock_subprocess_run, monkeypatch)

    marker = request.node.get_closest_marker('subprocess_run')
    if marker:
        where, mocked_run = marker.args
        mocker(where, mocked_run)

    return mocker

@pytest.fixture(autouse=True)
def no_gettext(monkeypatch, request):
    """
    Make gettext return all strings untranslated unless we request otherwise.
    """
    if request.node.get_closest_marker('enable_gettext'):
        return

    import hydrilla
    modules_to_process = [hydrilla]

    def add_child_modules(parent):
        """
        Recursuvely collect all modules descending from 'parent' into an array.
        """
        try:
            load_paths = parent.__path__
        except AttributeError:
            return

        for module_info in pkgutil.iter_modules(load_paths):
            if module_info.name != '__main__':
                __import__(f'{parent.__name__}.{module_info.name}')
                modules_to_process.append(getattr(parent, module_info.name))
                add_child_modules(getattr(parent, module_info.name))

    add_child_modules(hydrilla)

    for module in modules_to_process:
        if hasattr(module, '_'):
            monkeypatch.setattr(module, '_', lambda message: message)

@pytest.fixture
def tmpdir() -> Iterable[Path]:
    """
    Provide test case with a temporary directory that will be automatically
    deleted after the test.
    """
    with TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)
