import argparse
import os
import re
import sys
from pkg_resources import Requirement

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

parser = argparse.ArgumentParser(version="Pipin {0}".format('0.1'))
parser.add_argument("apps", nargs="+",
    help="the apps you wish to look up for.")
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

        if filter(lambda x: line.startswith(x), excludes):
            continue

        if line.startswith('file:'):
            match = re.match(file_uri_regex, line)
        # TODO: shall it check for editable apps?
        elif line.startswith('-e') or line.startswith('--editable') or \
                is_uri(line) or is_vcs_uri(line):
            if line.startswith('-e'):
                tmpstr = line[len('-e'):].strip()
            elif line.startswith('--editable'):
                tmpstr = line[len('--editable'):].strip()
            else:
                tmpstr = line
            match = re.match(editable_uri_regex, tmpstr)
        else:
            try:
                yield line
                # yield Requirement.parse(line)
                continue
            except ValueError:
                match = None

        if match:
            yield match.groupdict()
        else:
            raise ValueError('Invalid requirement line "%s"' % line)


def _locate(root, filename):
    for path, dirs, files in os.walk(os.path.abspath(root)):
        if filename in files:
            yield path, os.path.join(path, filename)


def pr(text, color):
    sys.stdout.write("\x1b[1;%dm" % (30 + color) + text + "\x1b[0m\n")


def main():
    filename = args.file or 'requirements.txt'
    for path, fpath in _locate(root=args.path, filename=filename):
        with open(fpath, 'r') as fopen:
            items = parse(fopen)
            items = ''.join(items)
            pr(fpath.split('/')[-2].upper() + ' (' + fpath + ')', MAGENTA)
            for app in args.apps:
                # TODO: regex for versions comparison (or perhaps use pip's __contains__)
                if app in items:
                    pr("%s found" % app, BLUE)
                else:
                    pr("%s not found" % app, RED)

if __name__ == '__main__':
    main()
