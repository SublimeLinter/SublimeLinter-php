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

from SublimeLinter.lint import Linter, util


class PHP(Linter):
    """Provides an interface to php -l."""

    syntax = ('php', 'html')
    regex = (
        r'^(?:Parse|Fatal) (?P<error>error):(\s*(?P<type>parse|syntax) error,?)?\s*'
        r'(?P<message>(?:unexpected \'(?P<near>[^\']+)\')?.*) (?:in - )?on line (?P<line>\d+)'
    )
    executable = 'php'
    error_stream = util.STREAM_STDOUT

    def split_match(self, match):
        """Return the components of the error."""
        match, line, col, error, warning, message, near = super().split_match(match)

        # message might be empty, we have to supply a value
        if match and match.group('type') == 'parse' and not message:
            message = 'parse error'

        return match, line, col, error, warning, message, near

    def cmd(self):
        """Read cmd from inline settings."""
        settings = Linter.get_view_settings(self)

        if 'cmd' in settings:
            command = [settings.get('cmd')]
        else:
            command = [self.executable_path]

        command.append('-l')
        command.append('-n')
        command.append('-d')
        command.append('display_errors=On')
        command.append('-d')
        command.append('log_errors=Off')

        return command
