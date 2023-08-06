import re
from typing import List, Optional, Pattern


class Def:
    quote: str
    opentTag: str
    closeTag: str
    spans: bool

    def __init__(self,
                 quote: str,
                 openTag: str,
                 closeTag: str,
                 spans: bool,
                 ) -> None:
        self.quote = quote
        self.openTag = openTag
        self.closeTag = closeTag
        self.spans = spans

    @classmethod
    def copyFrom(cls, d: 'Def') -> 'Def':
        return Def(d.quote, d.openTag, d.closeTag, d.spans)


defs: List[Def] = []  # Mutable definitions initialized by DEFAULT_DEFS.

DEFAULT_DEFS: List[Def] = [
    Def(quote='**', openTag='<strong>', closeTag='</strong>', spans=True),
    Def(quote='*', openTag='<em>', closeTag='</em>', spans=True),
    Def(quote='__', openTag='<strong>', closeTag='</strong>', spans=True),
    Def(quote='_', openTag='<em>', closeTag='</em>', spans=True),
    Def(quote='``', openTag='<code>', closeTag='</code>', spans=False),
    Def(quote='`', openTag='<code>', closeTag='</code>', spans=False),
    Def(quote='~~', openTag='<del>', closeTag='</del>', spans=True),
]

quotesRe: Pattern[str]      # Searches for quoted text.
unescapeRe: Pattern[str]    # Searches for escaped quotes.


def init() -> None:
    '''Reset definitions to defaults.'''
    global defs
    # Make shallow copy of DEFAULT_DEFS (list and list objects).
    defs.clear()
    defs.extend(map(lambda d: Def.copyFrom(d), DEFAULT_DEFS))
    initializeRegExps()


def initializeRegExps() -> None:
    '''Synthesise re's to find and unescape quotes.'''
    global quotesRe, unescapeRe
    quotes = list(map(lambda d: re.escape(d.quote), defs))
    # $1 is quote character(s), $2 is quoted text.
    # Quoted text cannot begin or end with whitespace.
    # Quoted can span multiple lines.
    # Quoted text cannot end with a backslash.
    quotesRe = re.compile(
        r'\\?(' + '|'.join(quotes) + r')([^\s\\]|\S[\s\S]*?[^\s\\])\1')
    # $1 is quote character(s).
    unescapeRe = re.compile(r'\\(' + '|'.join(quotes) + ')')


def getDefinition(quote: str) -> Optional[Def]:
    '''Return the quote definition corresponding to 'quote' character, return null if not found.'''
    for d in defs:
        if d.quote == quote:
            return d
    return None


def setDefinition(qdef: Def) -> None:
    '''Update existing or add new quote definition.'''
    d = getDefinition(qdef.quote)
    if d is not None:
        # Update existing definition.
        d.openTag = qdef.openTag
        d.closeTag = qdef.closeTag
        d.spans = qdef.spans
    else:
        # Double-quote definitions are prepended to the array so they are matched
        # before single-quote definitions(which are appended to the array).
        if len(qdef.quote) == 2:
            defs.insert(0, qdef)
        else:
            defs.append(qdef)
        initializeRegExps()


def unescape(s: str) -> str:
    '''Strip backslashes from quote characters.'''
    return unescapeRe.sub(lambda m: m[1], s)
