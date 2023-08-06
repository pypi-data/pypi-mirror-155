import re
from typing import Callable, List, Match, Optional, Pattern

from rimu import options, utils

Filter = Optional[Callable[[Match[str], 'Def'], str]]


class Def:
    match: Pattern[str]
    replacement: str
    filter: Filter

    def __init__(self,
                 match: Pattern[str],
                 replacement: str,
                 filter: Filter = None,
                 ):
        self.match = match
        self.replacement = replacement
        self.filter = filter

    @classmethod
    def copyFrom(cls, d: 'Def') -> 'Def':
        return Def(d.match, d.replacement, d.filter)


defs: List[Def] = []  # Mutable definitions initialized by DEFAULT_DEFS.

DEFAULT_DEFS: List[Def] = [
    # Begin match with \\? to allow the replacement to be escaped.
    # Global flag must be set on match re's so that the RegExp lastIndex property is set.
    # Replacements and special characters are expanded in replacement groups($1..).
    # Replacement order is important.

    # DEPRECATED as of 3.4.0.
    # Anchor: << #id>>
    Def(
        match=re.compile(r'\\?<<#([a-zA-Z][\w\-]*)>>'),
        replacement='<span id="$1"></span>',
        filter=lambda match, d:
            '' if options.skipBlockAttributes() else utils.replaceMatch(match, d.replacement)
    ),

    # Image: <image:src|alt>
    # src= $1, alt = $2
    Def(
        match=re.compile(r'\\?<image:([^\s|]+)\|(.*?)>', re.DOTALL),
        replacement='<img src="$1" alt="$2">'),

    # Image: <image:src>
    # src= $1, alt = $1
    Def(
        match=re.compile(r'\\?<image:([^\s|]+?)>'),
        replacement='<img src="$1" alt="$1">'),

    # Image: ![alt](url)
    # alt= $1, url = $2
    Def(
        match=re.compile(r'\\?!\[([^[]*?)]\((\S+?)\)'),
        replacement='<img src="$2" alt="$1">'),

    # Email: <address|caption>
    # address= $1, caption = $2
    Def(
        match=re.compile(r'\\?<(\S+@[\w.\-]+)\|(.+?)>', re.DOTALL),
        replacement='<a href="mailto:$1">$$2</a>'),

    # Email: <address>
    # address= $1, caption = $1
    Def(
        match=re.compile(r'\\?<(\S+@[\w.\-]+)>'),
        replacement='<a href="mailto:$1">$1</a>'),

    # Open link in new window: ^[caption](url)
    # caption= $1, url = $2
    Def(
        match=re.compile(r'\\?\^\[([^[]*?)]\((\S+?)\)'),
        replacement='<a href="$2" target="_blank">$$1</a>'),

    # Link: [caption](url)
    # caption= $1, url = $2
    Def(
        match=re.compile(r'\\?\[([^[]*?)]\((\S+?)\)'),
        replacement='<a href="$2">$$1</a>'),

    # Link: <url|caption>
    # url= $1, caption = $2
    Def(
        match=re.compile(r'\\?<(\S+?)\|(.*?)>', re.DOTALL),
        replacement='<a href="$1">$$2</a>'),

    # HTML inline tags.
    # Match HTML comment or HTML tag.
    # $1= tag, $2 = tag name
    Def(
        match=re.compile(
            r'\\?(<!--(?:[^<>&]*)?-->|<\/?([a-z][a-z0-9]*)(?:\s+[^<>&]+)?>)', re.IGNORECASE),
        replacement='',
        # Matched HTML comment or inline tag.
        filter=lambda match, d: options.htmlSafeModeFilter(match[1])
    ),

    # Link: <url>
    # url= $1
    Def(match=re.compile(r'\\?<([^|\s]+?)>'),
        replacement='<a href="$1">$1</a>'),

    # Auto-encode(most) raw HTTP URLs as links.
    Def(
        match=re.compile(
            r'\\?((?:http|https):\/\/[^\s"' + r"']*[A-Za-z0-9/#])"),
        replacement='<a href="$1">$1</a>'),

    # Character entity.
    Def(
        match=re.compile(r'\\?(&[\w#][\w]+;)'),
        replacement='',
        filter=lambda match, d: match[1]  # Pass the entity through verbatim.
    ),

    # Line-break (space followed by \ at end of line).
    Def(match=re.compile(r'[\\ ]\\(\n|$)'), replacement='<br>$1'),

    # This hack ensures backslashes immediately preceding closing code quotes are rendered
    # verbatim(Markdown behaviour).
    # Works by finding escaped closing code quotes and replacing the backslash and the character
    # preceding the closing quote with itself.
    Def(match=re.compile(r'(\S\\)(?=`)'), replacement='$1'),

    # This hack ensures underscores within words rendered verbatim and are not treated as
    # underscore emphasis quotes(GFM behaviour).
    Def(match=re.compile(r'([a-zA-Z0-9]_)(?=[a-zA-Z0-9])'), replacement='$1'),
]

# Reset definitions to defaults.


def init() -> None:
    '''Reset definitions to defaults.'''
    global defs
    # Make shallow copy of DEFAULT_DEFS (list and list objects).
    defs.clear()
    for d in DEFAULT_DEFS:
        defs.append(Def.copyFrom(d))


def getDefinition(pattern: str) -> Optional[Def]:
    '''Return the replacment definition matching the regular expresssion pattern, return null if not found.'''
    for d in defs:
        if d.match.pattern == pattern:
            return d
    return None


def setDefinition(pattern: str, flags: str, replacement: str) -> None:
    '''Update existing or add new replacement definition.'''
    # Flag properties are read-only so have to create new RegExp.
    flgs = 0
    if 'i' in flags:
        flgs |= re.IGNORECASE
    if 'm' in flags:
        flgs |= re.MULTILINE
    regexp = re.compile(pattern, flgs)
    d = getDefinition(pattern)
    if d is not None:
        # Update existing definition.
        d.match = regexp
        d.replacement = replacement
    else:
        # Append new definition to end of defs list(custom definitons have lower precedence).
        defs.append(Def(match=regexp, replacement=replacement))
