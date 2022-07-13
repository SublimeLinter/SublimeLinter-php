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
from SublimeLinter.lint import Linter, util


logger = logging.getLogger('SublimeLinter.plugin.php')


def _filter_message(message):
    if not message:
        message = 'parse error'
    else:
        message = message.replace('Standard input code', '')
        message = message.replace(' on ', '')
        message = message.replace(' in -', '')
        message = message.replace(' in ', '')
        message = message.strip()

    return message


class PHP(Linter):
    """Provides an interface to php -l."""

    defaults = {
        'selector': 'source.php, text.html.basic'
    }
    regex = (
        r'^(?P<error>Parse|Fatal) error:\s*'
        r'(?P<message>((?:parse|syntax) error,?)?\s*(?:unexpected \'(?P<near>[^\']+)\')?.*) '
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
            logger.warning('The setting `cmd` has been deprecated. '
                           'Use `executable` instead.')
            command = [self.settings.get('cmd')]
        else:
            command = ['php']

        command.append('-l')
        command.append('-n')
        command.append('-d')
        command.append('display_errors=On')
        command.append('-d')
        command.append('log_errors=Off')

        return command
