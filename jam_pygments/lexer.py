"""
    pygments.lexer.jam
    ~~~~~~~~~~~~~~~~~~
    
    Lexer for Jam/B2 language.
    
    :copyright: Copyright 2018-2019 Rene Rivera
    :license:
        Distributed under the Boost Software License, Version 1.0.
        (See accompanying file LICENSE.txt or http://www.boost.org/LICENSE_1_0.txt)
"""

from pygments.lexer import RegexLexer, include, bygroups, words, default
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
        'MATCH', 'ARGV',
        'import', 'using', 'peek', 'poke', 'record-binding',
        'project', 'use-project', 'build-project',
        'exe', 'lib', 'alias', 'obj', 'explicit', 'install', 'make', 'notfile',
        'unit-test', 'compile', 'compile-fail', 'link', 'link-fail', 'run', 'run-fail',
        'check-target-builds', 'glob', 'glob-tree', 'always',
        'constant', 'path-constant')
    whitespace_re = r'(\s+)'
    value_re = r'([^\s{}]+)'

    tokens = {
        'root': [
            include('^whitespace'),
            include('^comment'),
            include('^actions'),
            include('^rule'),
            include('^variable_exp'),
            (r'(module)' + whitespace_re + value_re + whitespace_re + r'([{])',
                bygroups(Keyword, Whitespace, Name.Namespace, Whitespace, Punctuation)),
            (r'(class)' + whitespace_re + value_re + whitespace_re + r'([:])' + whitespace_re + value_re,
                bygroups(Keyword, Whitespace, Name.Class, Whitespace, Punctuation, Whitespace, Name.Class)),
            (r'(class)' + whitespace_re + value_re,
                bygroups(Keyword, Whitespace, Name.Class)),
            (words(builtins, suffix=r'\b'), Name.Builtin),
            (words(keywords, suffix=r'\b'), Keyword),
            include('^value'),
            ],

        '^whitespace': [
            (whitespace_re, Whitespace),
            ],
        '^comment': [
            (r'#[|][\s\S]*?[|]#', Comment.Multiline),
            (r'#.*?\n', Comment.Single),
            ],

        # Value
        '^value': [
            (r'(?=[^\s])', Text, ('#pop', '@value'))
            ],
        '@value': [
            include('^variable_exp'),
            (r'(?=<)', Text, '@value_grist'),
            (r'[^\s]', Text)
            ],
        '@value_grist': [
            (r'<', Name.Attribute, '#push'),
            include('^variable_exp'),
            (r'[^\s>]+', Name.Attribute),
            (r'>', Name.Attribute, '#pop:2'),
            ],

        # Variable expansion
        '^variable_exp': [
            (r'[$][(]', String.Interpol, '@variable_exp')
            ],
        '@variable_exp': [
            (r'[$][(]', String.Interpol, '#push'),
            (r'[\][$]', String.Interpol),
            (r'[^)]+', String.Interpol),
            (r'[)]', String.Interpol, '#pop'),
            ],

        # Rule definition
        '^rule': [
            (r'(rule)' + whitespace_re,
                bygroups(Keyword, Whitespace), ('@rule_def')),
            ],
        '@rule_def': [
            include('^whitespace'),
            include('^comment'),
            (value_re + whitespace_re, bygroups(Name.Function, Whitespace), ('#pop', '@rule_args')),
        ],
        '@rule_args': [
            include('^whitespace'),
            include('^comment'),
            (r'[(]', Punctuation),
            (r'([^\s:*+?)]+)', Name.Variable),
            (r'[)]', Punctuation, '#pop')
        ],

        # Actions definition
        '^actions': [
            (r'(actions)' + whitespace_re,
                bygroups(Keyword, Whitespace), ('@actions_def')),
            ],
        '@actions_def': [
            include('^whitespace'),
            include('^comment'),
            (words(('updated', 'together', 'ignore', 'quietly', 'piecemeal', 'existing'), suffix=r'\b'), Name.Attribute),
            (value_re + whitespace_re, bygroups(Name.Function, Whitespace), ('#pop', '@actions_bind')),
            ],
        '@actions_bind': [
            (r'{', Text, ('#pop', '@actions_body')),
            include('^whitespace'),
            include('^comment'),
            (r'(bind)' + whitespace_re, bygroups(Keyword, Whitespace)),
            (value_re, Name.Variable)
            ],
        '@actions_body': [
            include('^variable_exp'),
            (whitespace_re + r'(})', bygroups(String.Heredoc, Punctuation), '#pop'),
            (r'[^{}]', String.Heredoc),
            (r'{', String.Heredoc, '#push'),
            (r'}', String.Heredoc, '#pop'),
            ],
    }
