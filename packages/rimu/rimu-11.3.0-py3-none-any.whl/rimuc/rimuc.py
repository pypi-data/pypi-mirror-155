import io
import os
import re
import sys
from typing import List, Optional

import rimu

import rimuc

VERSION = '11.3.0'
NAME = 'rimupy'
HOME_DIR = os.path.expanduser('~')
RIMURC = os.path.join(HOME_DIR, '.rimurc')


def die(message: str = '') -> None:
    if message != '':
        sys.stderr.write(message+'\n')
    raise SystemExit(1)


def readResource(name: str) -> str:
    if name not in rimuc.resources:
        die(f'missing resource: {name}')
    return rimuc.resources[name]


def main() -> None:
    '''Process sys.argv command-line.'''
    RESOURCE_TAG = 'resource:'  # Placeholder tag for resource files.
    PREPEND_TAG = '--prepend options'    # Placeholder tag for prepend options.
    STDIN = '-'

    # Command option values.
    safe_mode: Optional[int] = None
    html_replacement: Optional[str] = None
    layout: str = ''
    no_rimurc: bool = False
    prepend_files: List[str] = []
    pass_through: bool = False

    def popArg(arg: str) -> str:
        if len(args) == 0:
            die(f'missing {arg} option value')
        return args.pop(0)

    # Parse command-line options.
    prepend: str = ''
    outfile: str = ''
    args = sys.argv[1:]  # Drop script name.
    while len(args) > 0:
        arg: str = args.pop(0)
        if arg in ['--help', '-h']:
            manpage = readResource('manpage.txt')
            manpage = re.sub(r'\brimuc\b', NAME, manpage)
            print('\n' + manpage)
            return
        elif arg in ['--version']:
            print(VERSION)
            return
        elif arg in ['--lint', '-l']:   # Deprecated in Rimu 10.0.0
            pass
        elif arg in ['--output', '-o']:
            outfile = popArg(arg)
        elif arg in ['--pass']:
            pass_through = True
        elif arg in ['--prepend', '-p']:
            prepend += popArg(arg) + '\n'
        elif arg in ['--prepend-file']:
            prepend_file: str = popArg(arg)
            prepend_files.append(prepend_file)
        elif arg in ['--no-rimurc']:
            no_rimurc = True
        elif arg in ['--safe-mode', '--safeMode']:  # --safeMode deprecated in Rimu 7.1.0
            safe_mode = int(popArg(arg))
            if safe_mode < 0 or safe_mode > 15:
                die(f'illegal --safe-mode option value: {safe_mode}')
        elif arg in ['--html-replacement', '--htmlReplacement']:  # --htmlReplacement deprecated in Rimu 7.1.0
            html_replacement = popArg(arg)
        elif arg in [  # Styling macro definitions shortcut options.
            '--highlightjs',
            '--mathjax',
            '--section-numbers',
            '--theme',
            '--title',
            '--lang',
            '--toc',             # --toc deprecated in Rimu 8.0.0
            '--no-toc',
            '--sidebar-toc',     # --sidebar-toc deprecated in Rimu 10.0.0
            '--dropdown-toc',    # --dropdown-toc deprecated in Rimu 10.0.0
            '--custom-toc',
            '--header-ids',
                '--header-links']:
            macro_value = popArg(arg) if arg in ['--lang', '--title', '--theme'] else 'true'
            prepend += f"{{{arg}}}='{macro_value}'\n"
        elif arg in ['--layout', '--styled-name']:  # --styled-name' deprecated in Rimu 10.0.0
            layout = popArg(arg)
            if layout not in ['classic', 'flex', 'plain', 'sequel', 'v8']:
                # NOTE: Imported layouts are not supported.
                die(f"illegal --layout: {layout}")
            prepend += "{--header-ids}='true'\n"
        elif arg in ['--styled', '-s']:
            prepend += "{--header-ids}='true'\n"
            prepend += "{--no-toc}='true'\n"
            layout = 'sequel'
        else:
            args.insert(0, arg)  # Contains source file names.
            break
    # process.argv contains the list of source files.
    files = list(args)
    if len(files) == 0:
        files.append(STDIN)
    elif len(files) == 1 and layout != '' and files[0] != STDIN and len(outfile) == 0:
        # Use the source file name with .html extension for the output file.
        outfile = os.path.splitext(files[0])[0] + '.html'
    if layout != '':
        # Envelope source files with header and footer.
        files.insert(0, f'{RESOURCE_TAG}{layout}-header.rmu')
        files.append(f'{RESOURCE_TAG}{layout}-footer.rmu')
    # Prepend $HOME/.rimurc file if it exists.
    if not no_rimurc and os.path.isfile(RIMURC):
        prepend_files.insert(0, RIMURC)
    if prepend:
        prepend_files.append(PREPEND_TAG)
    files = prepend_files + files
    # Convert Rimu source files to HTML.
    output = ''
    errors = 0
    options = rimu.RenderOptions()
    if html_replacement is not None:
        options.htmlReplacement = html_replacement
    for infile in files:
        source = ''
        options.safeMode = safe_mode
        ext = ''
        if infile.startswith(RESOURCE_TAG):
            infile = infile[len(RESOURCE_TAG):]
            source = readResource(infile)
            options.safeMode = 0  # Resources are trusted.
        elif infile == STDIN:
            source = sys.stdin.read()
        elif infile == PREPEND_TAG:
            source = prepend
            options.safeMode = 0  # --prepend options are trusted.
        else:
            if not os.path.isfile(infile):
                die('source file does not exist: ' + infile)
            try:
                with open(infile) as f:
                    source = f.read()
            except:
                die('source file permission denied: ' + infile)
            if infile in prepend_files:
                # Prepended and ~/.rimurc files are trusted.
                options.safeMode = 0
            ext = os.path.splitext(infile)[1]
        # Skip .html and pass-through inputs.
        if not (ext == '.html' or (pass_through and infile == STDIN)):
            def callback(message: rimu.CallbackMessage) -> None:
                nonlocal errors
                msg = f'{message.type}: {"/dev/stdin" if infile == STDIN else infile}: {message.text}'
                if len(msg) > 120:
                    msg = msg[: 117] + '...'
                sys.stderr.write(msg + '\n')
                if message.type == 'error':
                    errors += 1
            options.callback = callback
            source = rimu.render(source, options)
        source = source.strip()
        if source:
            output += source + '\n'
    output = output.strip()
    if len(outfile) == 0 or outfile == '-':
        sys.stdout.write(output)
    else:
        with open(outfile, 'w') as f:
            f.write(output)
    if errors > 0:
        die()
