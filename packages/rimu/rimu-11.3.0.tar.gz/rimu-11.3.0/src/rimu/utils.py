import re
from typing import Match

from rimu import macros, options, spans
from rimu.expansion import Expand


def replaceSpecialChars(s: str) -> str:
    return s.replace('&', '&amp;').replace('>', '&gt;').replace('<', '&lt;')


def replaceMatch(match: Match, replacement: str, expand: Expand = None) -> str:
    '''Replace pattern '$1' or '$$1', '$2' or '$$2'... in `replacement` with corresponding match groups
       from `match`. If pattern starts with one '$' character add specials to `expand`,
       if it starts with two '$' characters add spans to `expand`.'''
    if expand is None:
        expand = Expand()

    def repl(m):
        # Replace $1, $2 ... with corresponding match groups.
        if m[1] == '$$':
            expand.spans = True
        else:
            expand.specials = True
        i = int(m[2])
        # match group number.
        if i > match.re.groups:
            options.errorCallback('undefined replacement group: ' + m[0])
            return ''
        result = match[i]
        # match group text.
        return replaceInline(result, expand)
    return re.sub(r'(\${1,2})(\d)', repl, replacement)


def replaceInline(text: str, expand: Expand) -> str:
    '''Replace the inline elements specified in options in text and return the result.'''
    result = text
    if expand.macros:
        result = macros.render(result)
    # Spans also expand special characters.
    if expand.spans:
        result = spans.render(result)
    elif expand.specials:
        result = replaceSpecialChars(result)
    return result
