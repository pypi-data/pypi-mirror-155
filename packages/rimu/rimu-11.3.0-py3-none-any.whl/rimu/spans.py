'''
 This module renders inline text containing Quote and Replacement elements.

 Quote and replacement processing involves splitting the source text into
 fragments where at the points where quotes and replacements occur then splicing fragments
 containing output markup into the breaks. A fragment is flagged as 'done' to
 exclude it from further processing.

 Once all quotes and replacements are processed fragments not yet flagged as
 'done' have special characters (&, <, >) replaced with corresponding special
 character entities. The fragments are then reassembled (defraged) into a
 resultant HTML string.
'''

import re
from typing import List, Match, Optional

from rimu import quotes, replacements, utils


class Fragment:
    text: str
    done: bool
    verbatim: str  # Replacements text rendered verbatim.

    def __init__(self,
                 text: str,
                 done: bool,
                 verbatim: str = '',
                 ):
        self.text = text
        self.done = done
        self.verbatim = verbatim


def render(source: str) -> str:
    result = preReplacements(source)
    fragments = [Fragment(text=result, done=False)]
    fragments = fragQuotes(fragments)
    fragSpecials(fragments)
    result = defrag(fragments)
    return postReplacements(result)


def defrag(fragments: List[Fragment]) -> str:
    '''Converts fragments to a string.'''
    result = ''
    for fragment in fragments:
        result += fragment.text
    return result


def fragQuotes(fragments: List[Fragment]) -> List[Fragment]:
    '''Fragment quotes in all fragments and return resulting fragments array.'''
    result: List[Fragment] = []
    for fragment in fragments:
        result.extend(fragQuote(fragment))
    # Strip backlash from escaped quotes in non-done fragments.
    for fragment in result:
        if not fragment.done:
            fragment.text = quotes.unescape(fragment.text)
    return result


def fragQuote(fragment: Fragment) -> List[Fragment]:
    '''Fragment quotes in a single fragment and return resulting fragments array.'''
    if fragment.done:
        return [fragment]
    # Find first matched quote in fragment text.
    quote: str
    match: Optional[Match[str]]
    startIndex: int = 0
    nextIndex: int = 0
    while True:
        match = quotes.quotesRe.search(fragment.text, nextIndex)
        if match is None:
            return [fragment]
        quote = match[1]
        # Check if quote is escaped.
        if match[0].startswith('\\'):
            # Restart search after escaped opening quote.
            nextIndex += match.start() + len(quote) + 1
            continue
        startIndex = match.start()
        nextIndex = match.end()
        break
    result: List[Fragment] = []
    # Arrive here if we have a matched quote.
    # The quote splits the input fragment into 5 or more output fragments:
    # Text before the quote, left quote tag, quoted text, right quote tag and text after the quote.
    qdef = quotes.getDefinition(match[1])
    assert qdef is not None
    # Check for same closing quote one character further to the right.
    quoted = match[2]
    while nextIndex < len(fragment.text) and fragment.text[nextIndex] == quote[0]:
        # Move to closing quote one character to right.
        quoted += quote[0]
        nextIndex += 1
    before = fragment.text[:startIndex]
    after = fragment.text[nextIndex:]
    result.append(Fragment(text=before, done=False))
    result.append(Fragment(text=qdef.openTag, done=True))
    if not qdef.spans:
        # Spans are disabled so render the quoted text verbatim.
        quoted = utils.replaceSpecialChars(quoted)
        quoted = quoted.replace('\u0000', '\u0001')  # Substitute verbatim replacement placeholder.
        result.append(Fragment(text=quoted, done=True))
    else:
        # Recursively process the quoted text.
        result.extend(fragQuote(Fragment(text=quoted, done=False)))
    result.append(Fragment(text=qdef.closeTag, done=True))
    # Recursively process the following text.
    result.extend(fragQuote(Fragment(text=after, done=False)))
    return result


# Stores placeholder replacement fragments saved by `preReplacements()` and restored by `postReplacements()`.
savedReplacements: List[Fragment] = []


def preReplacements(text: str) -> str:
    '''Return text with replacements replaced with a placeholder character (see `postReplacements()`):
       '\u0000' is placeholder for expanded replacement text.
       '\u0001' is placeholder for unexpanded replacement text (replacements that occur within quotes are rendered verbatim).'''
    savedReplacements.clear()
    fragments = fragReplacements([Fragment(text=text, done=False)])
    # Reassemble text with replacement placeholders.
    result = ''
    for fragment in fragments:
        if fragment.done:
            savedReplacements.append(fragment)  # Save replaced text.
            result += '\u0000'  # Placeholder for replaced text.
        else:
            result += fragment.text
    return result


def postReplacements(text: str) -> str:
    '''Replace replacements placeholders with replacements text from savedReplacements[].'''
    def func(match):
        fragment = savedReplacements.pop(0)
        return fragment.text if match[0] == '\u0000'else utils.replaceSpecialChars(fragment.verbatim)
    return re.sub(r'[\u0000\u0001]', func, text)


def fragReplacements(fragments: List[Fragment]) -> List[Fragment]:
    '''Fragment replacements in all fragments and return resulting fragments array.'''
    result = list(fragments)
    for rdef in replacements.defs:
        tmp: List[Fragment] = []
        for fragment in result:
            tmp.extend(fragReplacement(fragment, rdef))
        result = list(tmp)  # TODO: Is this necessary, why not: result=tmp?
    return result


def fragReplacement(fragment: Fragment,  rdef: replacements.Def) -> List[Fragment]:
    '''Fragment replacements in a single fragment for a single replacement definition.
       Return resulting fragments array.'''
    if fragment.done:
        return [fragment]
    match = rdef.match.search(fragment.text)
    if match is None:
        return [fragment]
    # Arrive here if we have a matched replacement.
    # The replacement splits the input fragment into 3 output fragments:
    # Text before the replacement, replaced text and text after the replacement.
    before = fragment.text[:match.start()]
    after = fragment.text[match.end():]
    result: List[Fragment] = []
    result.append(Fragment(text=before, done=False))
    replacement: str
    if match[0].startswith('\\'):
        # Remove leading backslash.
        replacement = utils.replaceSpecialChars(match[0][1:])
    else:
        if rdef.filter is None:
            replacement = utils.replaceMatch(match, rdef.replacement)
        else:
            replacement = rdef.filter(match, rdef)
    result.append(Fragment(text=replacement, done=True, verbatim=match[0]))
    # Recursively process the remaining text.
    result.extend(fragReplacement(Fragment(text=after, done=False), rdef))
    return result


def fragSpecials(fragments: List[Fragment]) -> None:
    '''Replace special characters in all non-done fragments.'''
    for fragment in filter(lambda fragment: not fragment.done, fragments):
        fragment.text = utils.replaceSpecialChars(fragment.text)
