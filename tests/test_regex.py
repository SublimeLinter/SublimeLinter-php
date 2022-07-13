# flake8: noqa
import unittest
import re
import importlib

import sublime

# Damn you dash separated module names!!!
LinterModule = importlib.import_module('SublimeLinter-php.linter')
Linter = LinterModule.PHP
regex = Linter.regex


class TestRegex(unittest.TestCase):

    def splitMatch(self, string):
        linter = Linter(sublime.View(0), {})
        match = re.match(regex, string)

        if match is None:
            return None

        match = linter.split_match(match)

        return {
            'error': match['error'],
            'line': match['line'],
            'message': match['message'],
            'near': match['near'],
        }


    def assertMatch(self, string, expected):
        self.assertEqual(self.splitMatch(string), expected)

    def assertNoMatch(self, string):
        self.assertIsNone(self.splitMatch(string))

    def test_no_errors(self):
        self.assertNoMatch('No syntax errors detected in - ')
        self.assertNoMatch('No syntax errors detected in - file.php')
        self.assertNoMatch('No syntax errors detected in - /path/to/file.php')
        self.assertNoMatch('No syntax errors detected in Standard input code')

    def test_errors(self):
        self.assertMatch(
            'Parse error: syntax error, unexpected \'$this\' (T_VARIABLE) on line 14', {
                'error': 'Parse',
                'line': 13,
                'message': 'syntax error, unexpected \'$this\' (T_VARIABLE)',
                'near': '$this'
                })

        self.assertMatch(
            'Parse error: syntax error, unexpected end of file in - on line 23', {
                'error': 'Parse',
                'line': 22,
                'message': 'syntax error, unexpected end of file',
                'near': None
                })

    def test_issue_29(self):
        self.assertMatch(
            'Parse error: syntax error, unexpected \'endwhile\' (T_ENDWHILE), expecting end of file in Standard input code on line 16', {
                'error': 'Parse',
                'line': 15,
                'message': 'syntax error, unexpected \'endwhile\' (T_ENDWHILE), expecting end of file',
                'near': 'endwhile'
                })

        self.assertMatch(
            'Parse error: parse error in - on line 16', {
                'error': 'Parse',
                'line': 15,
                'message': 'parse error',
                'near': None
                })
