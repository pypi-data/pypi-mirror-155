import re
from typing import Callable, List, Match, Optional, Pattern

from rimu import (blockattributes, delimitedblocks, expansion, io, macros,
                  options, quotes, replacements, utils)
from rimu.expansion import Expand

# Custom types.
Verify = Optional[Callable[[Match[str], io.Reader], bool]]   # Additional match verification checks.
Filter = Optional[Callable[[Match[str], io.Reader, 'Def'], str]]


class Def:
    match: Pattern[str]
    replacement: str
    name: str  # Optional unique identifier.
    verify: Verify
    filter: Filter

    def __init__(self,
                 match: Pattern[str],
                 replacement: str = '',
                 name: str = '',
                 verify: Verify = None,
                 filter: Filter = None,
                 ) -> None:
        self.match = match
        self.replacement = replacement
        self.name = name
        self.verify = verify
        self.filter = filter


def verifyMacroLine(match: Match[str], reader: io.Reader) -> bool:
    if macros.DEF_OPEN.search(match[0]):
        # Do not process macro definitions.
        return False
    # Silent because any macro expansion errors will be subsequently addressed downstream.
    value = macros.render(match[0], silent=True)
    if value.startswith(match[0]) or '\n' + match[0] in value:
        # The leading macro invocation expansion failed or contains itself.
        # This stops infinite recursion.
        return False
    # Insert the macro value into the reader just ahead of the cursor.
    pos = reader.pos+1
    reader.lines[pos:pos] = value.split('\n')
    return True


def blockDefFilter(match: Match[str], *_) -> str:
    if options.isSafeModeNz():
        return ''  # Skip if a safe mode is set.
    value = utils.replaceInline(match[2], Expand(macros=True))
    delimitedblocks.setDefinition(match[1], value)
    return ''


def quoteDefFilter(match: Match[str], *_) -> str:
    if options.isSafeModeNz():
        return ''  # Skip if a safe mode is set.
    quotes.setDefinition(quotes.Def(
        quote=match[1],
        openTag=utils.replaceInline(match[2], Expand(macros=True)),
        closeTag=utils.replaceInline(match[4], Expand(macros=True)),
        spans=match[3] == '|')
    )
    return ''


def replacementDefFilter(match: Match[str], *_) -> str:
    if options.isSafeModeNz():
        return ''  # Skip if a safe mode is set.
    pattern = match[1]
    flags = match[2]
    replacement = match[3]
    replacement = utils.replaceInline(replacement, Expand(macros=True))
    replacements.setDefinition(pattern, flags, replacement)
    return ''


def macroDefFilter(match: Match[str], *_) -> str:
    name = match[1]
    value = match[2]
    value = utils.replaceInline(value, Expand(macros=True))
    macros.setValue(name, value)
    return ''


def headerFilter(match: Match[str], _, d: Def) -> str:
    if macros.getValue('--header-ids') and blockattributes.id == '':
        blockattributes.id = blockattributes.slugify(match[2])
    result = utils.replaceMatch(match, d.replacement, Expand(macros=True))
    # Replace $1 with header number e.g. "<h###>" -> "<h3>"
    result = result.replace(match[1] + '>', str(len(match[1])) + '>')
    return result


def anchorFilter(match: Match[str], _, d: Def) -> str:
    if options.skipBlockAttributes():
        return ''
    else:
        # Default(non-filter) replacement processing.
        return utils.replaceMatch(match, d.replacement, Expand(macros=True))


def apiOptionFilter(match: Match[str], *_) -> str:
    if not options.isSafeModeNz():
        value = utils.replaceInline(match[2], Expand(macros=True))
        options.setOption(match[1], value)
    return ''


defs: List[Def] = [
    # Comment line.
    Def(
        match=re.compile(r'^\\?\/{2}(.*)$'),
    ),
    # Expand lines prefixed with a macro invocation prior to all other processing.
    # macro name = $1, macro value = $2
    Def(
        match=macros.MATCH_LINE,
        verify=verifyMacroLine,
        filter=lambda *_:'',     # Already processed in the `verify` function.
    ),
    # Delimited Block definition.
    # name = $1, definition = $2
    Def(
        match=re.compile(r"^\\?\|([\w\-]+)\|\s*=\s*'(.*)'$"),
        filter=blockDefFilter,
    ),
    # Quote definition.
    # quote = $1, openTag = $2, separator = $3, closeTag = $4
    Def(
        match=re.compile(r"^(\S{1,2})\s*=\s*'([^|]*)(\|{1,2})(.*)'$"),
        filter=quoteDefFilter,
    ),
    # Replacement definition.
    # pattern = $1, flags = $2, replacement = $3
    Def(
        match=re.compile(r"^\\?\/(.+)\/([igm]*)\s*=\s*'(.*)'$"),
        filter=replacementDefFilter,
    ),
    # Macro definition.
    # name = $1, value = $2
    Def(
        match=macros.LINE_DEF,
        filter=macroDefFilter,
    ),
    # Headers.
    # $1 is ID, $2 is header text.
    Def(
        match=re.compile(r'^\\?([#=]{1,6})\s+(.+?)(?:\s+\1)?$'),
        replacement=r'<h$1>$$2</h$1>',
        filter=headerFilter,
    ),
    # Block image: < image: src | alt >
    # src = $1, alt = $2
    Def(
        match=re.compile(r'^\\?<image:([^\s|]+)\|(.+?)>$'),
        replacement=r'<img src="$1" alt="$2">',
    ),
    # Block image: < image: src >
    # src = $1, alt = $1
    Def(
        match=re.compile(r'^\\?<image:([^\s|]+?)>$'),
        replacement=r'<img src="$1" alt="$1">',
    ),
    # DEPRECATED as of 3.4.0.
    # Block anchor: <<  # id>>
    # id = $1
    Def(
        match=re.compile(r'^\\?<<#([a-zA-Z][\w\-]*)>>$'),
        replacement=r'<div id="$1"></div>',
        filter=anchorFilter,
    ),
    # Block Attributes.
    # Syntax: .class-names  # id [html-attributes] block-options
    Def(
        name='attributes',
        # A loose match because Block Attributes can contain macro references.
        match=re.compile(r'^\\?\.[a-zA-Z#"\[+-].*$'),
        verify=lambda match, _: blockattributes.parse(match[0])
    ),
    # API Option.
    # name = $1, value = $2
    Def(
        match=re.compile(r"^\\?\.(\w+)\s*=\s*'(.*)'$"),
        filter=apiOptionFilter,
    ),
]


def render(reader: io.Reader, writer: io.Writer, allowed: List[str] = None) -> bool:
    '''If the next element in the reader is a valid line block render it
       and return True, else return false.'''
    if allowed is None:
        allowed = []
    if reader.eof():
        options.panic('premature eof')
    for d in defs:
        if allowed and d.name not in allowed:
            continue
        match = d.match.search(reader.cursor)
        if match is not None:
            if match[0][0] == '\\':
                # Drop backslash escape and continue.
                reader.cursor = reader.cursor[1:]
                continue
            if d.verify and not d.verify(match, reader):
                continue
            text: str
            if d.filter:
                text = d.filter(match, reader, d)
            else:
                text = utils.replaceMatch(match, d.replacement, Expand(macros=True)) if d.replacement else ''
            if text:
                text = blockattributes.injectHtmlAttributes(text)
                writer.write(text)
                reader.next()
                if not reader.eof():
                    writer.write('\n')  # Add a trailing '\n' if there are more lines.
            else:
                reader.next()
            return True
    return False
