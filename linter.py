#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Ryan Hileman, Aparajita Fishman and Anthony Pidden
# Copyright (c) 2013 Ryan Hileman, Aparajita Fishman and Anthony Pidden
#
# License: MIT
#

"""This module exports the PHP plugin class."""

import logging
import re
from SublimeLinter.lint import Linter, util


logger = logging.getLogger('SublimeLinter.plugin.php')

# PHP appends where it read the code from, e.g. `... in Standard input code`
# or `... in -`. Only that trailing part is noise; ` in ` and ` on ` inside the
# message itself (`Cannot use isset() on the result of an expression`) are not.
TRAILING_SOURCE_RE = re.compile(r'\s+in\s+(?:Standard input code|-)\s*$')


def _filter_message(message):
    if not message:
        message = 'parse error'
    else:
        message = TRAILING_SOURCE_RE.sub('', message).strip()

    return message


class PHP(Linter):
    """Provides an interface to php -l."""

    defaults = {
        'selector': 'embedding.php, source.php'
    }
    regex = (
        r'^(?P<error>Parse|Fatal) error:\s*'
        # PHP 7 quotes the token with single quotes (`unexpected 'foo'`), PHP 8
        # with double quotes and a description (`unexpected token ";"`,
        # `unexpected identifier "foo"`).
        r'(?P<message>((?:parse|syntax) error,?)?\s*'
        r'(?:unexpected (?:[a-z-]+(?: [a-z-]+)* )?(?P<quote>["\'])(?P<near>.+?)(?P=quote))?.*) '
        r'(?:in - )?on line (?P<line>\d+)'
    )
    error_stream = util.STREAM_STDOUT

    def split_match(self, match):
        """Return the components of the error."""
        result = super().split_match(match)
        result['message'] = _filter_message(result.message)

        return result

    def cmd(self):
        """Read cmd from inline settings."""
        if 'cmd' in self.settings:
            logger.warning(
                'The setting `cmd` has been removed. '
                'Use `executable` instead. '
            )
            return None

        return ('php', '-l', '-n', '-d', 'display_errors=On', '-d', 'log_errors=Off')
