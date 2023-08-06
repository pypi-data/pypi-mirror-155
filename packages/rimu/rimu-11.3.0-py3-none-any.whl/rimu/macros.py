import re
from typing import List, Optional

from rimu import options, spans

# Matches a line starting with a macro invocation. $1 = macro invocation.
MATCH_LINE = re.compile(r'^({(?:[\w\-]+)(?:[!=|?](?:|.*?[^\\]))?}).*$')
# Match single-line macro definition. $1 = name, $2 = delimiter, $3 = value.
LINE_DEF = re.compile(r"^\\?{([\w\-]+\??)}\s*=\s*'(.*)'$")
# Match multi-line macro definition literal value open delimiter. $1 is first line of macro.
DEF_OPEN = re.compile(r"^\\?{[\w\-]+\??}\s*=\s*'(.*)$")
DEF_CLOSE = re.compile(r"^(.*)'$")


class Macro:
    name: str
    value: str

    def __init__(self, name: str, value: str = '') -> None:
        self.name = name
        self.value = value


defs: List[Macro] = []


def init() -> None:
    '''Reset definitions to defaults.'''
    # Initialize predefined macros.
    defs.clear()
    defs.append(Macro('--'))
    defs.append(Macro('--header-ids'))


def getValue(name: str) -> Optional[str]:
    '''Return named macro value or null if it doesn't exist.'''
    for mdef in defs:
        if mdef.name == name:
            return mdef.value
    return None


def setValue(name: str, value: str) -> None:
    '''Set named macro value or add it if it doesn't exist.
       If the name ends with '?' then don't set the macro if it already exists.
       `quote` is a single character: ' if a literal value, ` if an expression value.'''
    if options.skipMacroDefs():
        return  # Skip if a safe mode is set.
    existential = False
    if name.endswith('?'):
        name = name[:-1]  # Strip trailing '?'.
        existential = True
    if name == '--' and value != '':
        options.errorCallback('the predefined blank \'--\' macro cannot be redefined')
        return
    for mdef in defs:
        if mdef.name == name:
            if not existential:
                mdef.value = value
            return
    defs.append(Macro(name, value))


def render(text: str, silent: bool = False) -> str:
    '''Render macro invocations in text string.
        Render Simple invocations first, followed by Parametized, Inclusion and Exclusion invocations.'''
    MATCH_COMPLEX = re.compile(r'\\?{([\w\-]+)([!=|?](?:|.*?[^\\]))}',
                               re.DOTALL)  # Parametrized, Inclusion and Exclusion invocations.
    MATCH_SIMPLE = re.compile(r'\\?{([\w\-]+)()}')  # Simple macro invocation.
    result = text
    for find in [MATCH_SIMPLE, MATCH_COMPLEX]:
        def repl(match):
            if match[0].startswith('\\'):
                return match[0][1:]
            params = match[2]
            if params.startswith('?'):
                # DEPRECATED: Existential macro invocation.
                if not silent:
                    options.errorCallback(f'existential macro invocations are deprecated: {match[0]}')
                return match[0]
            name = match[1]
            value = getValue(name)  # Macro value is null if macro is undefined.
            if value is None:
                if not silent:
                    options.errorCallback(f'undefined macro: {match[0]}: {text}')
                return match[0]
            if find is MATCH_SIMPLE:
                return value
            params = params.replace(r'\}', '}')  # Unescape escaped} characters.
            if params[0] in '|':
                paramsList = params[1:].split('|')
                # Substitute macro parameters.
                # Matches macro definition formal parameters[$]$< param-number > [[\]: < default-param-value >$]
                # 1st group: [$]$
                # 2nd group: < param-number > (1, 2..)
                # 3rd group: [\]: < default-param-value >$
                # 4th group: < default-param-value >
                PARAM_RE = re.compile(r'\\?(\$\$?)(\d+)(\\?:(|.*?[^\\])\$)?', re.DOTALL)

                def repl(mr):
                    if mr[0].startswith('\\'):
                        # Unescape escaped macro parameters.
                        return mr[0][1:]
                    p1 = mr[1]
                    p2 = int(mr[2])
                    p3 = mr[3] or ''
                    p4 = mr[4] or ''
                    if p2 == 0:
                        return mr[0]  # $0 is not a valid parameter name.
                    # Unassigned parameters are replaced with a blank string.
                    param = '' if len(paramsList) < p2 else paramsList[p2 - 1]
                    if p3 != '':
                        if p3.startswith('\\'):
                            # Unescape escaped default parameter.
                            param += p3[1:]
                        elif param == '':
                            # Assign default parameter value.
                            param = p4
                            # Unescape escaped $ characters in the default value.
                            param = param.replace(r'\$', r'$')
                    if p1 == r'$$':
                        param = spans.render(param)
                    return param
                value = PARAM_RE.sub(repl, value)
                return value
            elif params[0] in '!=':  # Exclusion and inclusion macros.
                pattern = params[1:]
                skip: bool
                try:
                    skip = re.match(f'^{pattern}$', value) is None
                except:
                    if not silent:
                        options.errorCallback(f'illegal macro regular expression: {pattern}: {text}')
                    return match[0]
                if params[0] == '!':
                    skip = not skip
                return '\u0002' if skip else ''  # Flag line for deletion.
            else:
                options.errorCallback(f'illegal macro syntax: {match[0]}')
                return ''
        result = find.sub(repl, result)
    if '\u0002' in result:
        # Delete lines flagged by Inclusion/Exclusion macros.
        result = '\n'.join(filter(lambda line: '\u0002' not in line, result.split('\n')))
    return result
