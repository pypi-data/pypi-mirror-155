import re
from typing import List

from rimu import options, utils
from rimu.expansion import Expand

classes: str  # Space separated HTML class names.
id: str  # HTML element id.
css: str  # HTML CSS styles.
attributes: str  # Other HTML element attributes.
opts: Expand

ids: List[str] = []  # List of allocated HTML ids.


def init() -> None:
    global classes, id, css, attributes, opts, ids
    classes = ''
    id = ''
    css = ''
    attributes = ''
    opts = Expand()
    ids.clear()


def parse(attrs: str) -> bool:
    '''Parse Block Attributes line:
       .class-names #id "css-properties" [html-attributes] block-options
    '''
    global classes, id, css, attributes, opts, ids
    if options.skipBlockAttributes():
        return True
    text = attrs
    text = utils.replaceInline(text, Expand(macros=True))

    # Kludge: The regexp is split in two to fix a catastrophic backtracking issue (without
    # this split the match was taking around 5 seconds!).
    # See https://unix.stackexchange.com/questions/419545/why-is-regular-expression-matching-so-slow
    # Split re after this asterisk     * <-- split regexp here.
    # r'^\\?\.((?:\s*[a-zA-Z][\w\-]*)+)*(?:\s*)?(#[a-zA-Z][\w\-]*\s*)?(?:\s*)?(?:"(.+?)")?(?:\s*)?(\[.+])?(?:\s*)?([+-][ \w+-]+)?$'
    # class-names = $1, id = $2, css-properties = $3, html-attributes = $4, block-options = $5'''
    r1 = re.compile(r'^\\?\.((?:\s*[a-zA-Z][\w\-]*)+)*')
    m1 = r1.match(text)
    if m1 is None:
        return False
    # Prefixed empty placeholder group () to maintain group match indexes in m2.
    r2 = re.compile(r'()(?:\s*)?(#[a-zA-Z][\w\-]*\s*)?(?:\s*)?(?:"(.+?)")?(?:\s*)?(\[.+])?(?:\s*)?([+-][ \w+-]+)?$')
    m2 = r2.match(text[m1.end():])
    if m2 is None:
        return False
    if m1[1]:
        # HTML element class names.
        classes += f' {m1[1].strip()}'
        classes = classes.strip()
    if m2[2]:
        # HTML element id.
        id = m2[2].strip()[1:]
    if m2[3]:
        # CSS properties.
        if css and not css.endswith(';'):
            css += ';'
        css += ' ' + m2[3].strip()
        css = css.strip()
    if m2[4] and not options.isSafeModeNz():
        # HTML attributes.
        attributes += ' ' + m2[4][1:- 1].strip()
        attributes = attributes.strip()
    if m2[5]:
        opts.parse(m2[5])
    return True


def injectHtmlAttributes(tag: str, consume: bool=True) -> str:
    '''Inject HTML attributes into the HTML `tag` and return result.
       Consume HTML attributes unless the 'tag' argument is blank.'''
    global classes, id, css, attributes, opts, ids
    if not tag:
        return tag
    result = tag
    attrs = ''
    if classes:
        match = re.compile(r'^(<[^>]*class=")(.*?)"', re.IGNORECASE).search(result)
        if match:
            # Inject class names into existing class attribute in first tag.
            result = result.replace(match[0], f'{match[1]}{classes} {match[2]}"', 1)
        else:
            attrs = f'class="{classes}"'
    if id:
        id = id.lower()
        has_id = re.compile(r'^<[^<]*id=".*?"', re.IGNORECASE).search(result)
        if has_id or id in ids:
            options.errorCallback(f"duplicate 'id' attribute: {id}")
        else:
            ids.insert(0, id)
        if not has_id:
            attrs += f' id="{id}"'
    if css:
        match = re.compile(r'^(<[^>]*style=")(.*?)"', re.IGNORECASE).search(result)
        if match:
            # Inject CSS styles into first style attribute in first tag.
            group2 = match[2].strip()
            if not group2.endswith(';'):
                group2 += ';'
            result = result.replace(match[0], f'{match[1]}{group2} {css}"', 1)
        else:
            attrs += f' style="{css}"'
    if attributes:
        attrs += f' {attributes}'
    attrs = attrs.strip()
    if attrs:
        match = re.compile(r'^<([a-z]+|h[1-6])(?=[ >])', re.IGNORECASE).search(result)
        if match:
            # Inject attributes after tag name.
            before = result[:len(match[0])]
            after = result[len(match[0]):]
            result = before + ' ' + attrs + after
    if consume:
        # Consume the attributes.
        classes = ''
        id = ''
        css = ''
        attributes = ''
    return result


def slugify(text: str) -> str:
    slug = re.sub(r'\W+', '-', text)  # Replace non-alphanumeric characters with dashes.
    slug = re.sub(r'-+', '-', slug)  # Replace multiple dashes with single dash.
    slug = re.sub(r'(^-)|(-$)', '', slug)  # Trim leading and trailing dashes.
    slug = slug.lower()
    if not slug:
        slug = 'x'
    if slug in ids:
        # Another element already has that id.
        i = 2
        while f'{slug}-{i}' in ids:
            i += 1
        slug += f'-{i}'
    return slug
