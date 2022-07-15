import unittest
import importlib

import sublime


LinterModule = importlib.import_module('SublimeLinter-php.linter')
Linter = LinterModule.PHP


class TestRegex(unittest.TestCase):
    def assertMatch(self, string, expected):
        linter = Linter(sublime.View(0), {})
        actual = list(linter.find_errors(string))[0]
        # `find_errors` fills out more information we don't want to write down
        # in the examples
        self.assertEqual({k: actual[k] for k in expected.keys()}, expected)

    def assertNoMatch(self, string):
        linter = Linter(sublime.View(0), {})
        actual = list(linter.find_errors(string))
        self.assertFalse(actual)

    def test_no_errors(self):
        self.assertNoMatch('No syntax errors detected in - ')
        self.assertNoMatch('No syntax errors detected in - file.php')
        self.assertNoMatch('No syntax errors detected in - /path/to/file.php')
        self.assertNoMatch('No syntax errors detected in Standard input code')

    def test_errors(self):
        self.assertMatch(
            'Parse error: syntax error, unexpected \'$this\' (T_VARIABLE) on line 14',
            {
                'error': 'Parse',
                'line': 13,
                'message': 'syntax error, unexpected \'$this\' (T_VARIABLE)',
                'near': '$this',
            },
        )

        self.assertMatch(
            'Parse error: syntax error, unexpected end of file in - on line 23',
            {
                'error': 'Parse',
                'line': 22,
                'message': 'syntax error, unexpected end of file',
                'near': None,
            },
        )

    def test_issue_29(self):
        self.assertMatch(
            'Parse error: syntax error, unexpected \'endwhile\' (T_ENDWHILE), expecting end of file in Standard input code on line 16',
            {
                'error': 'Parse',
                'line': 15,
                'message': 'syntax error, unexpected \'endwhile\' (T_ENDWHILE), expecting end of file',
                'near': 'endwhile',
            },
        )

        self.assertMatch(
            'Parse error: parse error in - on line 16',
            {
                'error': 'Parse',
                'line': 15,
                'message': 'parse error',
                'near': None,
            },
        )
