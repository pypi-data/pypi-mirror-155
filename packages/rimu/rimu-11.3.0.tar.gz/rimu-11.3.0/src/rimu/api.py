from rimu import (blockattributes, delimitedblocks, io, lineblocks, lists,
                  macros, options, quotes, replacements)


def init() -> None:
    blockattributes.init()
    options.init()
    delimitedblocks.init()
    macros.init()
    quotes.init()
    replacements.init()


def render(source: str) -> str:
    reader = io.Reader(source)
    writer = io.Writer()
    while not reader.eof():
        reader.skipBlankLines()
        if reader.eof():
            break
        if lineblocks.render(reader, writer):
            continue
        if lists.render(reader, writer):
            continue
        if delimitedblocks.render(reader, writer):
            continue
        # This code should never be executed (normal paragraphs should match anything).
        options.panic('no matching delimited block found')
    return writer.toString()
