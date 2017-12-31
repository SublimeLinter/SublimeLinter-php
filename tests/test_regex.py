# flake8: noqa
import unittest
import re
import importlib

# Damn you dash separated module names!!!
LinterModule = importlib.import_module('SublimeLinter-php.linter')
Linter = LinterModule.PHP
_filter_message = LinterModule._filter_message
regex = Linter.regex


class TestRegex(unittest.TestCase):

    def assertMatch(self, string, expected):
        match = re.match(regex, string)
        self.assertIsNotNone(match)

        # Hack to test message filtering.
        actual = match.groupdict()
        if 'message' in actual:
            actual['message'] = _filter_message(actual['message'])

        self.assertEqual(actual, expected)

    def assertNoMatch(self, string):
        self.assertIsNone(re.match(regex, string))

    def test_no_errors(self):
        self.assertNoMatch('No syntax errors detected in - ')
        self.assertNoMatch('No syntax errors detected in - file.php')
        self.assertNoMatch('No syntax errors detected in - /path/to/file.php')
        self.assertNoMatch('No syntax errors detected in Standard input code')

    def test_errors(self):
        self.assertMatch(
            'Parse error: syntax error, unexpected \'$this\' (T_VARIABLE) in - on line 14', {
                'error': 'Parse',
                'line': '14',
                'message': 'syntax error, unexpected \'$this\' (T_VARIABLE)',
                'near': '$this'
                })

        self.assertMatch(
            'Parse error: syntax error, unexpected end of file in - on line 23', {
                'error': 'Parse',
                'line': '23',
                'message': 'syntax error, unexpected end of file',
                'near': None
                })

    def test_issue_29(self):
        self.assertMatch(
            'Parse error: syntax error, unexpected \'endwhile\' (T_ENDWHILE), expecting end of file in Standard input code on line 16', {
                'error': 'Parse',
                'line': '16',
                'message': 'syntax error, unexpected \'endwhile\' (T_ENDWHILE), expecting end of file',
                'near': 'endwhile'
                })

        self.assertMatch(
            'Parse error: parse error in - on line 16', {
                'error': 'Parse',
                'line': '16',
                'message': 'parse error',
                'near': None
                })
