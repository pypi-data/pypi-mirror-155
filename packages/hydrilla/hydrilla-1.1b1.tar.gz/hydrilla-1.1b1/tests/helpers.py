# SPDX-License-Identifier: CC0-1.0

# Copyright (C) 2022 Wojtek Kosior <koszko@koszko.org>
#
# Available under the terms of Creative Commons Zero v1.0 Universal.

import re

variable_word_re = re.compile(r'^<(.+)>$')

def process_command(command, expected_command):
    """Validate the command line and extract its variable parts (if any)."""
    assert len(command) == len(expected_command)

    extracted = {}
    for word, expected_word in zip(command, expected_command):
        match = variable_word_re.match(expected_word)
        if match:
            extracted[match.group(1)] = word
        else:
            assert word == expected_word

    return extracted

def run_missing_executable(command, **kwargs):
    """
    Instead of running a command, raise FileNotFoundError as if its executable
    was missing.
    """
    raise FileNotFoundError('dummy')

class MockedCompletedProcess:
    """
    Object with some fields similar to those of subprocess.CompletedProcess.
    """
    def __init__(self, args, returncode=0,
                 stdout='some output', stderr='some error output',
                 text_output=True):
        """
        Initialize MockedCompletedProcess. Convert strings to bytes if needed.
        """
        self.args       = args
        self.returncode = returncode

        if type(stdout) is str and not text_output:
            stdout = stdout.encode()
        if type(stderr) is str and not text_output:
            stderr = stderr.encode()

        self.stdout = stdout
        self.stderr = stderr
