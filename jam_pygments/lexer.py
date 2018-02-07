"""
    pygments.lexer.jam
    ~~~~~~~~~~~~~~~~~~
    
    Lexer for Jam/B2 language.
    
    :copyright: Copyright 2018 Rene Rivera
    :license:
        Distributed under the Boost Software License, Version 1.0.
        (See accompanying file LICENSE.txt or http://www.boost.org/LICENSE_1_0.txt)
"""

from pygments.lexer import RegexLexer, include, bygroups, words
from pygments.token import Whitespace, Comment, Keyword, Name, Punctuation, String, Text

__all__ = ['JamLexer']

class JamLexer(RegexLexer):
    name = "Jam"
    aliases = ['jam', 'bjam', 'b2']
    filenames = ['*.jam', 'Jamfile', 'Jamroot']
    mimetypes = ['text/x-jam']
    keywords = (
        'local', 'include', 'return', 'break', 'continue', 'for', 'in',
        'switch', 'if', 'else', 'module', 'class', 'while', 'rule', 'on',
        'actions', 'case', 'bind', 'updated', 'together', 'ignore',
        'quietly', 'piecemeal', 'existing')
    builtins = (
        'Always', 'ALWAYS', 'Depends', 'DEPENDS', 'echo', 'Echo', 'ECHO', 'exit', 'Exit', 'EXIT',
        'Glob', 'GLOB', 'GLOB-RECURSIVELY', 'Includes', 'INCLUDES', 'REBUILDS',
        'SPLIT_BY_CHARACTERS', 'NoCare', 'NOCARE', 'NOTIME', 'NotFile', 'NOTFILE',
        'NoUpdate', 'NOUPDATE', 'Temporary', 'TEMPORARY', 'ISFILE', 'HdrMacro', 'HDRMACRO',
        'FAIL_EXPECTED', 'RMOLD', 'UPDATE', 'subst', 'SUBST', 'RULENAMES', 'VARNAMES',
        'DELETE_MODULE', 'IMPORT', 'EXPORT', 'CALLER_MODULE', 'BACKTRACE', 'PWD',
        'IMPORT_MODULE', 'IMPORTED_MODULES', 'INSTANCE', 'SORT', 'NORMALIZE_PATH',
        'CALC', 'NATIVE_RULE', 'HAS_NATIVE_RULE', 'USER_MODULE', 'NEAREST_USER_LOCATION',
        'PYTHON_IMPORT_RULE', 'W32_GETREG', 'W32_GETREGNAMES', 'SHELL', 'COMMAND',
        'MD5', 'FILE_OPEN', 'PAD', 'PRECIOUS', 'SELF_PATH', 'MAKEDIR', 'READLINK', 'GLOB_ARCHIVE',
        'import', 'using', 'peek', 'poke', 'record-binding',
        'project', 'use-project', 'build-project',
        'exe', 'lib', 'alias', 'obj', 'explicit', 'install', 'make', 'notfile',
        'unit-test', 'compile', 'compile-fail', 'link', 'link-fail', 'run', 'run-fail',
        'check-target-builds', 'glob', 'glob-tree', 'always',
        'constant', 'path-constant')
    whitespace_re = r'(\s+)'
    value_re = r'([^\s]+)'

    tokens = {
        'whitespace': [
            (whitespace_re, Whitespace),
            ],
        'comment': [
            (r'#[|]([\s\S]*?)[|]#', Comment.Multiline),
            (r'#.*?\n', Comment.Single),
            ],
        'root': [
            include('whitespace'),
            include('comment'),
            (r'(rule)' + whitespace_re + value_re + whitespace_re,
                bygroups(Keyword, Whitespace, Name.Function, Whitespace)),
            (r'(actions)' + whitespace_re,
                bygroups(Keyword, Whitespace), 'actions_def'),
            (r'(module)' + whitespace_re + value_re + whitespace_re + r'([{])',
                bygroups(Keyword, Whitespace, Name.Namespace, Whitespace, Punctuation)),
            (r'(class)' + whitespace_re + value_re + whitespace_re + r'([:])' + whitespace_re + value_re,
                bygroups(Keyword, Whitespace, Name.Class, Whitespace, Punctuation, Whitespace, Name.Class)),
            (r'(class)' + whitespace_re + value_re,
                bygroups(Keyword, Whitespace, Name.Class)),
            (r'([$][(])' r'([^)]+)' r'([)])' + whitespace_re,
                bygroups(String.Interpol, String.Interpol, String.Interpol, Whitespace)),
            (words(builtins, suffix=r'\b'), Name.Builtin),
            (words(keywords, suffix=r'\b'), Keyword),
            (value_re, Text)
            ],
        'actions_def': [
            include('whitespace'),
            include('comment'),
            (r'({)' r'([^}]+)' r'(})',
                bygroups(Punctuation, String.Heredoc, Punctuation), '#pop'),
            (words(
                ('updated', 'together', 'ignore', 'quietly', 'piecemeal', 'existing'),
                suffix=r'\b'), Name.Attribute),
            (value_re, Name.Function, 'actions_bind')
            ],
        'actions_bind': [
            include('whitespace'),
            include('comment'),
            (r'({)' r'([^}]+)' r'(})',
                bygroups(Punctuation, String.Heredoc, Punctuation), '#pop:2'),
            (r'(bind)' r'(\s+)',
                bygroups(Keyword, Whitespace)),
            (value_re, Name.Variable)
            ],
    }
