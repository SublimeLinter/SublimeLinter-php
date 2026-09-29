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
            'Parse error: syntax error, unexpected \'endwhile\' (T_ENDWHILE), '
            'expecting end of file in Standard input code on line 16',
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

    def test_issue_55_message_filter_only_strips_trailing_source(self):
        # " on " and " in " inside the message must survive
        self.assertMatch(
            'Fatal error: Cannot use isset() on the result of an expression '
            '(you can use "null !== expression" instead) in Standard input code on line 2',
            {
                'error': 'Fatal',
                'line': 1,
                'message': 'Cannot use isset() on the result of an expression '
                           '(you can use "null !== expression" instead)',
            },
        )

        self.assertMatch(
            "Fatal error: 'break' not in the 'loop' or 'switch' context "
            'in Standard input code on line 3',
            {
                'error': 'Fatal',
                'line': 2,
                'message': "'break' not in the 'loop' or 'switch' context",
            },
        )

        self.assertMatch(
            'Fatal error: Cannot redeclare f() (previously declared in Standard input code:2) '
            'in Standard input code on line 3',
            {
                'error': 'Fatal',
                'line': 2,
                'message': 'Cannot redeclare f() (previously declared in Standard input code:2)',
            },
        )

    def test_issue_56_php8_quoted_tokens(self):
        # PHP 8 writes `unexpected token ";"`, `unexpected identifier "bar"`, ...
        self.assertMatch(
            'Parse error: syntax error, unexpected token ";", expecting "]" '
            'in Standard input code on line 2',
            {
                'error': 'Parse',
                'line': 1,
                'message': 'syntax error, unexpected token ";", expecting "]"',
                'near': ';',
            },
        )

        self.assertMatch(
            'Parse error: syntax error, unexpected identifier "bar" in Standard input code on line 2',
            {
                'error': 'Parse',
                'line': 1,
                'message': 'syntax error, unexpected identifier "bar"',
                'near': 'bar',
            },
        )

        self.assertMatch(
            'Parse error: syntax error, unexpected variable "$y" in Standard input code on line 2',
            {'error': 'Parse', 'line': 1, 'near': '$y'},
        )

        self.assertMatch(
            'Parse error: syntax error, unexpected integer "2", expecting "," or ";" '
            'in Standard input code on line 2',
            {'error': 'Parse', 'line': 1, 'near': '2'},
        )

        self.assertMatch(
            'Parse error: syntax error, unexpected double-quoted string "def" '
            'in Standard input code on line 2',
            {'error': 'Parse', 'line': 1, 'near': 'def'},
        )

        self.assertMatch(
            'Parse error: syntax error, unexpected double-quoted string "a\'b", '
            'expecting "," or ";" in Standard input code on line 1',
            {'error': 'Parse', 'line': 0, 'near': "a'b"},
        )

        self.assertMatch(
            'Parse error: syntax error, unexpected end of file in Standard input code on line 3',
            {
                'error': 'Parse',
                'line': 2,
                'message': 'syntax error, unexpected end of file',
                'near': None,
            },
        )
