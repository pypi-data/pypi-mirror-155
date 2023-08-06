import re
from typing import Callable, List, Match, Optional, Pattern

from rimu import api, blockattributes, io, macros, options, utils
from rimu.expansion import Expand

MATCH_INLINE_TAG: Pattern[str] = re.compile(
    r'^(a|abbr|acronym|address|b|bdi|bdo|big|blockquote|br|cite|code|del|dfn|em|i|img|ins|kbd|mark|q|s|samp|small|span|strike|strong|sub|sup|time|tt|u|var|wbr)$',
    re.IGNORECASE)

# Custom type defintions.
Verify = Optional[Callable[[Match[str]], bool]]  # Additional match verification checks.
DelimiterFilter = Optional[Callable[[Match[str], 'Def'], str]]  # Return filtered delimiter content.
ContentFilter = Optional[Callable[[str, Match[str], Expand], str]]


class Def:
    '''Multi-line block element definition.'''
    openTag: str
    closeTag: str
    openMatch: Pattern[str]
    closeMatch: Pattern[str]  # $1 (if defined) is appended to block content.
    verify: Verify  # Additional match verification checks.
    delimiterFilter: DelimiterFilter  # Process opening delimiter. Return any delimiter content.
    contentFilter: ContentFilter
    expand: Expand
    name: str  # Optional unique identifier.

    def __init__(self,
                 openTag: str,
                 closeTag: str,
                 openMatch: Pattern[str],
                 closeMatch: Pattern[str] = None,
                 verify: Verify = None,
                 delimiterFilter: DelimiterFilter = None,
                 contentFilter: ContentFilter = None,
                 expand: Expand = None,
                 name: str = '',
                 ) -> None:
        self.openTag = openTag
        self.closeTag = closeTag
        self.openMatch = openMatch
        if closeMatch is not None:
            self.closeMatch = closeMatch
        else:
            self.closeMatch = self.openMatch
        self.verify = verify
        self.delimiterFilter = delimiterFilter
        self.contentFilter = contentFilter
        if expand is not None:
            self.expand = Expand.copyFrom(expand)
        else:
            self.expand = Expand()
        self.name = name

    @classmethod
    def copyFrom(cls, d: 'Def') -> 'Def':
        return Def(
            d.openTag,
            d.closeTag,
            d.openMatch,
            d.closeMatch,
            d.verify,
            d.delimiterFilter,
            d.contentFilter,
            d.expand,
            d.name,
        )


# Filter and Verify functions.

def htmlVerify(match: Match[str]) -> bool:
    '''Return False if the HTML tag is an inline (non-block) HTML tag.'''
    if match[2]:
        # Matched alphanumeric tag name.
        return MATCH_INLINE_TAG.search(match[2]) is None
    else:
         # Matched HTML comment or doctype tag.
        return True


def openingDelimiterFilter(match: Match[str], _) -> str:
    '''delimiterFilter that returns opening delimiter line text from match group $1.'''
    return match[1]


def classInjectionFilter(match: Match[str], d: Def) -> str:
    '''delimiterFilter for code, division and quote blocks.
       Inject $2 into block class attribute, set close delimiter to $1.'''
    p1 = match[2].strip()
    if p1:
        blockattributes.classes = p1
    d.closeMatch = re.compile('^' + re.escape(match[1]) + r'$')
    return ''


def macroDefContentFilter(text: str, match: Match[str], expand: Expand) -> str:
    '''contentFilter for multi-line macro definitions.'''
    m = re.search(r'^{([\w\-]+\??)}', match[0])  # Extract macro name from opening delimiter.
    assert m is not None
    name = m[1]
    text = re.sub(r"' *\\\n", "'\n", text)  # Unescape line-continuations.
    text = re.sub(r"(' *[\\]+)\\\n", lambda match: f'{match[1]}\n', text)  # Unescape escaped line-continuations.
    text = utils.replaceInline(text, expand)  # Expand macro invocations.
    macros.setValue(name, text)
    return ''


def indentedContentFilter(text: str, *_) -> str:
    '''Strip indent from start of each line.'''
    m = re.search(r'\S', text)
    assert m is not None
    first_indent = m.start()
    result = []
    for line in text.split('\n'):
        # Strip first line indent width or up to first non-space character.
        m = re.search(r'\S|$', line)
        assert m is not None
        indent = m.start()
        if indent > first_indent:
            indent = first_indent
        result.append(line[indent:])
    return '\n'.join(result)


def quoteParagraphContentFilter(text: str, *_) -> str:
    '''Strip leading > from start of each line and unescape escaped leading >.'''
    result = []
    for line in text.split('\n'):
        line = re.sub(r'^>', '', line)
        line = re.sub(r'^\\>', '>', line)
        result.append(line)
    return '\n'.join(result)


defs: List[Def] = []  # Mutable definitions initialized by DEFAULT_DEFS.

DEFAULT_DEFS: List[Def] = [
    # Delimited blocks cannot be escaped with a backslash.

    # Multi-line macro literal value definition.
    Def(
        openMatch=macros.DEF_OPEN,  # $1 is first line of macro.
        closeMatch=macros.DEF_CLOSE,
        openTag='',
        closeTag='',
        expand=Expand(macros=True),
        delimiterFilter=openingDelimiterFilter,
        contentFilter=macroDefContentFilter,
    ),
    # Comment block.
    Def(
        name='comment',
        openMatch=re.compile(r'^\\?\/\*+$'),
        closeMatch=re.compile(r'^\*+\/$'),
        openTag='',
        closeTag='',
        expand=Expand(
            skip=True, specials=True  # Fall-back if skip is disabled.
        ),
    ),
    # Division block.
    Def(
        name='division',
        openMatch=re.compile(
            r'^\\?(\.{2,})([\w\s-]*)$'),  # $1 is delimiter text, $2 is optional class names.
        openTag='<div>',
        closeTag='</div>',
        expand=Expand(
            container=True, specials=True  # Fall-back if container is disabled.
        ),
        delimiterFilter=classInjectionFilter,
    ),
    # Quote block.
    Def(
        name='quote',
        openMatch=re.compile(
            r'^\\?("{2,})([\w\s-]*)$'),  # $1 is delimiter text, $2 is optional class names.
        openTag='<blockquote>',
        closeTag='</blockquote>',
        expand=Expand(
            container=True, specials=True  # Fall-back if container is disabled.
        ),
        delimiterFilter=classInjectionFilter,
    ),
    # Code block.
    Def(
        name='code',
        openMatch=re.compile(
            r'^\\?(-{2,}|`{2,})([\w\s-]*)$'),  # $1 is delimiter text, $2 is optional class names.
        openTag='<pre><code>',
        closeTag='</code></pre>',
        expand=Expand(macros=False, specials=True),
        verify=lambda match:
            # The deprecated '-' delimiter does not support appended class names.
            not (match[1][0] == '-' and match[2].strip() != ''),
        delimiterFilter=classInjectionFilter,
    ),
    # HTML block.
    Def(
        name='html',
        # Block starts with HTML comment, DOCTYPE directive or block-level HTML start or end tag.
        # $1 is first line of block.
        # $2 is the alphanumeric tag name.
        openMatch=re.compile(
            r'^(<!--.*|<!DOCTYPE(?:\s.*)?|<\/?([a-z][a-z0-9]*)(?:[\s>].*)?)$',
            re.IGNORECASE),
        closeMatch=re.compile(r'^$'),  # Blank line or EOF.
        openTag='',
        closeTag='',
        expand=Expand(macros=True),
        verify=htmlVerify,
        delimiterFilter=openingDelimiterFilter,
        contentFilter=lambda text, *_: options.htmlSafeModeFilter(text),
    ),
    # Indented paragraph.
    Def(
        name='indented',
        openMatch=re.compile(r'^\\?(\s+\S.*)$'),  # $1 is first line of block.
        closeMatch=re.compile(r'^$'),  # Blank line or EOF.
        openTag='<pre><code>',
        closeTag='</code></pre>',
        expand=Expand(macros=False, specials=True),
        delimiterFilter=openingDelimiterFilter,
        contentFilter=indentedContentFilter,
    ),
    # Quote paragraph.
    Def(
        name='quote-paragraph',
        openMatch=re.compile(r'^\\?(>.*)$'),  # $1 is first line of block.
        closeMatch=re.compile(r'^$'),  # Blank line or EOF.
        openTag='<blockquote><p>',
        closeTag='</p></blockquote>',
        expand=Expand(
            macros=True,
            spans=True,
            specials=True  # Fall-back if spans is disabled.
        ),
        delimiterFilter=openingDelimiterFilter,
        contentFilter=quoteParagraphContentFilter,
    ),
    # Paragraph (lowest priority, cannot be escaped).
    Def(
        name='paragraph',
        openMatch=re.compile(r'(.*)'),  # $1 is first line of block.
        closeMatch=re.compile(r'^$'),  # Blank line or EOF.
        openTag='<p>',
        closeTag='</p>',
        expand=Expand(
            macros=True,
            spans=True,
            specials=True  # Fall-back if spans is disabled.
        ),
        delimiterFilter=openingDelimiterFilter),
]

# Reset definitions to defaults.


def init() -> None:
    '''Reset definitions to defaults.'''
    global defs
    # Make shallow of DEFAULT_DEFS (list and list objects).
    defs.clear()
    for d in DEFAULT_DEFS:
        defs.append(Def.copyFrom(d))


# If the next element in the reader is a valid delimited block render it
# and return True, else return False.
def render(reader: io.Reader, writer: io.Writer, allowed: List[str] = None) -> bool:
    global defs
    if allowed is None:
        allowed = []
    if reader.eof():
        options.panic('premature eof')
    for d in defs:
        if allowed and d.name not in allowed:
            continue
        match = d.openMatch.search(reader.cursor)
        if not match:
            continue
        # Escape non-paragraphs.
        if match[0][0] == '\\' and d.name != 'paragraph':
            # Drop backslash escape and continue.
            reader.cursor = reader.cursor[1:]
            continue
        if d.verify and not d.verify(match):
            continue
        # Process opening delimiter.
        delimiterText = d.delimiterFilter(match, d) if d.delimiterFilter else ''
        # Read block content into lines.
        lines: List[str] = []
        if delimiterText:
            lines.append(delimiterText)
        # Read content up to the closing delimiter.
        reader.next()
        content = reader.readTo(d.closeMatch or d.openMatch)
        if content is None:
            options.errorCallback('unterminated delimited block: ' + match[0])
        else:
            lines.extend(content)
        # Calculate block expansion options.
        expand = Expand.copyFrom(d.expand)
        expand.merge(blockattributes.opts)
        # Translate block.
        if expand.skip is not True:
            text = '\n'.join(lines)
            if d.contentFilter:
                text = d.contentFilter(text, match, expand)
            opentag = d.openTag
            if d.name == 'html':
                text = blockattributes.injectHtmlAttributes(text)
            else:
                opentag = blockattributes.injectHtmlAttributes(opentag)
            if expand.container:
                blockattributes.opts.container = None  # Consume before recursion.
                text = api.render(text)
            else:
                text = utils.replaceInline(text, expand)
            closetag = d.closeTag
            if d.name == 'division' and opentag == '<div>':
                # Drop div tags if the opening div has no attributes.
                opentag = ''
                closetag = ''
            writer.write(opentag)
            writer.write(text)
            writer.write(closetag)
            if not reader.eof() and (opentag + text + closetag):
                # Add a trailing '\n' if we've written a non-blank line and there are more source lines left.
                writer.write('\n')
        # Reset consumed Block Attributes expansion options.
        blockattributes.opts = Expand()
        return True
    return False  # No matching delimited block found.


def getDefinition(name: str) -> Optional[Def]:
    '''Return block definition or null if not found.'''
    for d in defs:
        if d.name == name:
            return d
    return None


def setDefinition(name: str, value: str) -> None:
    '''Update existing named definition.
       Value syntax: <open-tag>|<close-tag> block-options'''
    d = getDefinition(name)
    if not d:
        options.errorCallback(f"illegal delimited block name: {name}: |{name}|='{value}'")
        return
    match = re.search(r'^(?:(<[a-zA-Z].*>)\|(<[a-zA-Z/].*>))?(?:\s*)?([+-][ \w+-]+)?$', value.strip())
    if not match:
        options.errorCallback(f"illegal delimited block definition: |{name}|='{value}'")
        return
    if match[1] is not None:
        # Open and close tags are defined.
        d.openTag = match[1]
        d.closeTag = match[2]
    if match[3] is not None:
        d.expand.parse(match[3])
