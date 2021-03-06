# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\Exslt\RegularExpressions.py
# Compiled at: 2006-12-26 13:39:48
__doc__ = '\nEXSLT 2.0 - Regular Expressions (http://www.exslt.org/regexp/index.html)\nWWW: http://4suite.org/XSLT        e-mail: support@4suite.org\n\nCopyright (c) 2001 Fourthought Inc, USA.   All Rights Reserved.\nSee  http://4suite.org/COPYRIGHT  for license and copyright information\n'
import re
from Ft.Lib import boolean
from Ft.Xml.XPath import Conversions
EXSL_REGEXP_NS = 'http://exslt.org/regular-expressions'

def Match(context, source, pattern, flags=''):
    """
    The regexp:match function lets you get hold of the substrings of the
    string passed as the first argument that match the captured parts of
    the regular expression passed as the second argument.

    The second argument is a regular expression that follows the Javascript
    regular expression syntax.

    The third argument is a string consisting of character flags to be used
    by the match. If a character is present then that flag is true. The
    flags are:
      g: global match - the submatches from all the matches in the string
                        are returned. If this character is not present, then
                        only the submatches from the first match in the
                        string are returned.
      i: case insensitive - the regular expression is treated as case
                            insensitive. If this character is not present,
                            then the regular expression is case sensitive.

    The regexp:match function returns a node set of 'match' elements, each of
    whose string value is equal to a portion of the first argument string
    that was captured by the regular expression. If the match is not global,
    the first match element has a value equal to the portion of the string
    matched by the entire regular expression.
    """
    source = Conversions.StringValue(source)
    pattern = Conversions.StringValue(pattern)
    flags = flags and Conversions.StringValue(flags)
    regexp = re.compile(pattern, 'i' in flags and re.IGNORECASE or 0)
    match = regexp.search(source)
    if match is None:
        return []
    processor = context.processor
    processor.pushResultTree(context.currentInstruction.baseUri)
    try:
        if 'g' in flags:
            while match:
                processor.writer.startElement('match')
                processor.writer.text(match.group())
                processor.writer.endElement('match')
                match = regexp.search(source, match.end())

        all = [match.group()]
        groups = match.groups()
        groups and all.extend(list(groups))
        for match in all:
            processor.writer.startElement('match')
            match and processor.writer.text(match)
            processor.writer.endElement('match')

    finally:
        rtf = processor.popResult()
    return rtf.childNodes
    return


def Replace(context, source, pattern, flags, repl):
    """
    The regexp:replace function replaces the parts of a string that match
    a regular expression with another string.

    The first argument is the string to be matched and replaced. The second
    argument is a regular expression that follows the Javascript regular
    expression syntax. The fourth argument is the string to replace the
    matched parts of the string.

    The third argument is a string consisting of character flags to be used
    by the match. If a character is present then that flag is true. The flags
    are:
      g: global replace - all occurrences of the regular expression in the
                          string are replaced. If this character is not
                          present, then only the first occurrence of the
                          regular expression is replaced.
      i: case insensitive - the regular expression is treated as case
                            insensitive. If this character is not present,
                            then the regular expression is case sensitive.
    """
    source = Conversions.StringValue(source)
    pattern = Conversions.StringValue(pattern)
    flags = Conversions.StringValue(flags)
    repl = Conversions.StringValue(repl)
    regexp = re.compile(pattern, 'i' in flags and re.IGNORECASE or 0)
    return regexp.sub(repl, source, 'g' not in flags)


def Test(context, source, pattern, flags=''):
    """
    The regexp:test function returns true if the string given as the first
    argument matches the regular expression given as the second argument.

    The second argument is a regular expression that follows the Javascript
    regular expression syntax.

    The third argument is a string consisting of flags to be used by the test.
    If a character is present then that flag is true. The flags are:
      g: global test - has no effect on this function, but is retained for
                       consistency with regexp:match and regexp:replace.
      i: case insensitive - the regular expression is treated as case
                            insensitive. If this character is not present,
                            then the regular expression is case sensitive.
    """
    source = Conversions.StringValue(source)
    pattern = Conversions.StringValue(pattern)
    flags = flags and Conversions.StringValue(flags)
    regexp = re.compile(pattern, 'i' in flags and re.IGNORECASE or 0)
    return regexp.search(source) and boolean.true or boolean.false


ExtNamespaces = {EXSL_REGEXP_NS: 'regexp'}
ExtFunctions = {(EXSL_REGEXP_NS, 'match'): Match, (EXSL_REGEXP_NS, 'replace'): Replace, (EXSL_REGEXP_NS, 'test'): Test}
ExtElements = {}