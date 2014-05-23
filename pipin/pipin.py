import argparse
from collections import defaultdict
import os
import re
import sys

try:
    unicode
except NameError:
    # Python 3
    basestring = unicode = str

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# todo: add ssh, sftp protocols
uri_regex = re.compile(r'^(svn|git|bzr|hg|http|https|file|ftp):(\.+)')
file_uri_regex = re.compile(
    r'^(?P<path>[^#]+)#egg=(?P<name>[^&]+)$', re.MULTILINE)
editable_uri_regex = re.compile(r'^((?P<vcs>svn|git|bzr|hg)\+)?'
                                '(?P<uri>[^#&]+)#egg=(?P<name>[^&]+)$',
                                re.MULTILINE)
vcs_uri_regex = re.compile(r'^(?P<vcs>svn|git|bzr|hg)\+'
                           '(?P<uri>[^#&]+)#egg=(?P<name>[^&]+)$',
                           re.MULTILINE)

parser = argparse.ArgumentParser()
parser.add_argument("app", nargs="+",
    help="the app(s) you wish to look up for.")
parser.add_argument("path", action="store",
    help="a directory to search in (use `.` for current directory).")
parser.add_argument("-f", "--file", action="store",
    help="name of requirements file (default to `requirements.txt`).")
args = parser.parse_args()


def is_uri(uri):
    match = re.match(uri_regex, uri.lower())
    return match is not None


def is_vcs_uri(uri):
    match = re.match(vcs_uri_regex, uri.lower())
    return match is not None


def parse(s):
    if not isinstance(s, basestring):
        s = s.read()

    excludes = (
        '#', '-r', '--requirement',
        '-f', '--find-links',
        '-i', '--index-url', '--extra-index-url', '--no-index',
        '-Z', '--always-unzip')

    for line in s.splitlines():
        line = line.strip()
        if not line:
            continue

        if [x for x in excludes if line.startswith(x)]:
            continue

        if line.startswith('file:'):
            match = re.match(file_uri_regex, line)
        # TODO: shall it check for editable apps?
        elif line.startswith('-e') or line.startswith('--editable') or \
                is_uri(line) or is_vcs_uri(line):
            if line.startswith('-e'):
                tmpstr = line[len('-e'):].strip()
                # too short requirement format
                if len(tmpstr) < 5:
                    continue
            elif line.startswith('--editable'):
                tmpstr = line[len('--editable'):].strip()
            else:
                tmpstr = line
            match = re.match(editable_uri_regex, tmpstr)
        else:
            try:
                yield line
                continue
            except ValueError:
                match = None

        if match:
            yield match.groupdict()['name']
        else:
            raise ValueError('Invalid requirement line "%s"' % line)


def _locate(root, filename):
    for path, dirs, files in os.walk(os.path.abspath(root)):
        if filename in files:
            yield path, os.path.join(path, filename)


def _out(text, color):
    sys.stdout.write("\x1b[1;%dm" % (30 + color) + text + "\x1b[0m\n")


def lets_pipin():
    cnt = defaultdict(int)
    cnt_projects = 0
    filename = args.file or 'requirements.txt'

    for path, fpath in _locate(root=args.path, filename=filename):
        cnt_projects += 1
        with open(fpath, 'r') as fopen:
            items = ' '.join(parse(fopen))
            _out(fpath.split('/')[-2].upper() + ' (' + fpath + ')', YELLOW)

            reapp = None
            for app in args.app:
                if '*' in app:
                    reapp = re.search(r'\b%s\b([\>\=\<]+)%s' % tuple(app.split('*')), items)
                    reapp = reapp.group() if reapp else None

                if reapp:
                    _out("%s found" % reapp, CYAN)
                    cnt['%s_found' % app] += 1
                elif app in items:
                    _out("%s found" % app, CYAN)
                    cnt['%s_found' % app] += 1
                else:
                    _out("%s not found" % app, RED)
                    cnt['%s_not_found' % app] += 1

    for app in args.app:
        _out("\nSearched %s projects for %s:" % (cnt_projects, app), WHITE)
        _out(" %s found" % cnt['%s_found' % app], CYAN)
        _out(" %s not found" % cnt['%s_not_found' % app], RED)

if __name__ == '__main__':
    lets_pipin()
