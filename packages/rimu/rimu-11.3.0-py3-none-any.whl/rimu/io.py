import re
from typing import List, Match, Optional, Pattern


class Reader:
    '''Rimu line oriented string reader.'''
    lines: List[str]
    pos: int    # Line index of current line.

    def __init__(self, text: str):
        # Used internally by spans package.
        text = text.replace('\u0000', ' ')
        # Used internally by spans package.
        text = text.replace('\u0001', ' ')
        # Used internally by macros package.
        text = text.replace('\u0002', ' ')
        # Split self.lines on newline boundaries.
        # http:#stackoverflow.com/questions/1155678/javascript-string-newline-character
        # Split is broken on IE8 e.g. 'X\n\nX'.split(/\n/g).length) returns 2 but should return 3.
        self.lines = re.split(r'\r\n|\r|\n', text)
        self.pos = 0

    @property
    def cursor(self) -> str:
        assert not self.eof()
        return self.lines[self.pos]

    @cursor.setter
    def cursor(self, value: str) -> None:
        assert not self.eof()
        self.lines[self.pos] = value

    def eof(self) -> bool:
        '''Return true if the cursor has advanced over all input self.lines.'''
        return self.pos >= len(self.lines)

    def next(self) -> None:
        '''Move cursor to next input line.'''
        if (not self.eof()):
            self.pos += 1

    def readTo(self, regexp: Pattern[str]) -> Optional[List[str]]:
        '''Read to the first line matching the regexp.

        Return the array of self.lines preceding the match plus a line containing
        the $1 match group (if it exists).
        Return null if an self.EOF is encountered.
        Exit with the reader pointing to the line following the match.'''
        result = []
        match = None
        while (not self.eof()):
            match = regexp.search(self.cursor)
            if (match is not None):
                if (regexp.groups > 0):
                    result.append(match[1])  # $1
                self.next()
                break
            result.append(self.cursor)
            self.next()
        # Blank line matches self.EOF.
        if (match is not None or (regexp.pattern == r'^$' and self.eof())):
            return result
        else:
            return None

    def skipBlankLines(self) -> None:
        while (not self.eof() and self.cursor.strip() == ''):
            self.next()


class Writer:
    '''Rimu line oriented string writer.'''
    buffer: List[str]

    def __init__(self):
        self.buffer = []

    def write(self, line: str) -> None:
        '''Write line.'''
        self.buffer.append(line)

    def toString(self) -> str:
        '''Return string of joined lines.'''
        return ''.join(self.buffer)
