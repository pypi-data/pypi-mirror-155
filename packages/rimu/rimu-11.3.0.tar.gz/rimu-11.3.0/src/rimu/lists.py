import re
from typing import List, Match, Optional, Pattern

from rimu import (blockattributes, delimitedblocks, expansion, io, lineblocks,
                  options, utils)
from rimu.expansion import Expand


class Def:
    match: Pattern[str]
    listOpenTag: str
    listCloseTag: str
    itemOpenTag: str
    itemCloseTag: str
    termOpenTag: str  # Definition lists only.
    termCloseTag: str  # Definition lists only.

    def __init__(self,
                 match: Pattern[str],
                 listOpenTag: str,
                 listCloseTag: str,
                 itemOpenTag: str,
                 itemCloseTag: str,
                 termOpenTag: str = '',
                 termCloseTag: str = '',
                 ):
        self.match = match
        self.listOpenTag = listOpenTag
        self.listCloseTag = listCloseTag
        self.itemOpenTag = itemOpenTag
        self.itemCloseTag = itemCloseTag
        self.termOpenTag = termOpenTag
        self.termCloseTag = termCloseTag


# Information about a matched list item element.
class ItemInfo:
    match: Match[str]
    listdef: 'Def'
    id: str  # List ID.


defs: List[Def] = [
    # Prefix match with backslash to allow escaping.

    # Unordered lists.
    # $1 is list ID $2 is item text.
    Def(
        match=re.compile(r'^\\?\s*(-|\+|\*{1,4})\s+(.*)$'),
        listOpenTag='<ul>',
        listCloseTag='</ul>',
        itemOpenTag='<li>',
        itemCloseTag='</li>'),
    # Ordered lists.
    # $1 is list ID $2 is item text.
    Def(
        match=re.compile(r'^\\?\s*(?:\d*)(\.{1,4})\s+(.*)$'),
        listOpenTag='<ol>',
        listCloseTag='</ol>',
        itemOpenTag='<li>',
        itemCloseTag='</li>'),
    # Definition lists.
    # $1 is term, $2 is list ID, $3 is definition.
    Def(
        match=re.compile(r'^\\?\s*(.*[^:])(:{2,4})(|\s+.*)$'),
        listOpenTag='<dl>',
        listCloseTag='</dl>',
        itemOpenTag='<dd>',
        itemCloseTag='</dd>',
        termOpenTag='<dt>',
        termCloseTag='</dt>'),
]

ids: List[str] = []  # Stack of open list IDs.


def render(reader: io.Reader, writer: io.Writer) -> bool:
    global ids
    if reader.eof():
        options.panic('premature eof')
    startItem: Optional[ItemInfo]
    startItem = matchItem(reader)
    if startItem is None:
        return False
    ids = []
    renderList(startItem, reader, writer)
    # ids should now be empty.
    if ids:
        options.panic('list stack failure')
    return True


def renderList(item: ItemInfo, reader: io.Reader, writer: io.Writer) -> Optional[ItemInfo]:
    global ids
    ids.append(item.id)
    writer.write(blockattributes.injectHtmlAttributes(item.listdef.listOpenTag))
    nextItem: Optional[ItemInfo]
    while True:
        nextItem = renderListItem(item, reader, writer)
        if nextItem is None or nextItem.id != item.id:
            # End of list or next item belongs to parent list.
            writer.write(item.listdef.listCloseTag)
            ids.pop()
            return nextItem
        item = nextItem


def renderListItem(item: ItemInfo, reader: io.Reader, writer: io.Writer) -> Optional[ItemInfo]:
    '''Render the current list item, return the next list item or null if there are no more items.'''
    global ids
    d = item.listdef
    match = item.match
    text: str
    if d.termOpenTag:  # => definition list.
        writer.write(blockattributes.injectHtmlAttributes(d.termOpenTag, consume=False))
        blockattributes.id=''
        text = utils.replaceInline(match[1], Expand(macros=True, spans=True))
        writer.write(text)
        writer.write(d.termCloseTag)
    writer.write(blockattributes.injectHtmlAttributes(d.itemOpenTag))
    # Process item text from first line.
    itemLines = io.Writer()
    text = match[match.re.groups]
    itemLines.write(text + '\n')
    # Process remainder of list item i.e. item text, optional attached block, optional child list.
    reader.next()
    attachedLines = io.Writer()
    blankLines: int
    attachedDone: bool = False
    nextItem: Optional[ItemInfo]
    while True:
        blankLines = consumeBlockAttributes(reader, attachedLines)
        if blankLines >= 2 or blankLines == -1:
            # EOF or two or more blank lines terminates list.
            nextItem = None
            break
        nextItem = matchItem(reader)
        if nextItem:
            if nextItem.id in ids:
                # Next item belongs to current list or a parent list.
                pass
            else:
                # Render child list.
                nextItem = renderList(nextItem, reader, attachedLines)
            break
        if attachedDone:
            break  # Multiple attached blocks are not permitted.
        if blankLines == 0:
            savedIds = ids
            ids = []
            if delimitedblocks.render(reader, attachedLines,
                                      allowed=['comment', 'code', 'division', 'html', 'quote']):
                attachedDone = True
            else:
                # Item body line.
                itemLines.write(reader.cursor + '\n')
                reader.next()
            ids = savedIds
        elif blankLines == 1:
            if delimitedblocks.render(reader, attachedLines, ['indented', 'quote-paragraph']):
                attachedDone = True
            else:
                break
    # Write item text.
    text = itemLines.toString().strip()
    text = utils.replaceInline(text, Expand(macros=True, spans=True))
    writer.write(text)
    # Write attachment and child list.
    writer.buffer.extend(attachedLines.buffer)
    # Close list item.
    writer.write(d.itemCloseTag)
    return nextItem

# Consume blank lines and Block Attributes.
# Return number of blank lines read or -1 if EOF.


def consumeBlockAttributes(reader: io.Reader, writer: io.Writer) -> int:
    blanks = 0
    while True:
        if reader.eof():
            return -1
        if lineblocks.render(reader, writer, allowed=['attributes']):
            continue
        if reader.cursor != '':
            return blanks
        blanks += 1
        reader.next()


# Check if the line at the reader cursor matches a list related element.
# Unescape escaped list items in reader.
# If it does not match a list related element return null.
def matchItem(reader: io.Reader) -> Optional[ItemInfo]:
    # Check if the line matches a List definition.
    if reader.eof():
        return None
    item = ItemInfo()  # ItemInfo factory.
    # Check if the line matches a list item.
    for d in defs:
        match = d.match.search(reader.cursor)
        if match is not None:
            if match[0][0] == '\\':
                reader.cursor = reader.cursor[1:]  # Drop backslash.
                return None
            item.match = match
            item.listdef = d
            # The second to last match group is the list ID.
            item.id = match[match.re.groups - 1]
            return item
    return None
