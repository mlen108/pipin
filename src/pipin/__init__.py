import os
import re
from pkg_resources import Requirement

try:
    unicode
except NameError:
    # Python 3
    basestring = unicode = str

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

def is_uri(uri):
    match = re.match(uri_regex, uri.lower())
    return match is not None


def is_vcs_uri(uri):
    match = re.match(vcs_uri_regex, uri.lower())
    return match is not None


def parse(s):
    if not isinstance(s, basestring):
        s = s.read()

    exclude_lines = (
        '#', '-r', '--requirement',
        '-f', '--find-links',
        '-i', '--index-url', '--extra-index-url', '--no-index',
        '-Z', '--always-unzip')

    for line in s.splitlines():
        line = line.strip()
        if not line:
            continue

        for x in exclude_lines:
            if line.startswith(x):
                continue

        if line.startswith('file:'):
            match = re.match(file_uri_regex, line)
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
                yield Requirement.parse(line)
                continue
            except ValueError:
                match = None

        if match:
            yield match.groupdict()
        else:
            raise ValueError('Invalid requirement line "%s"' % line)


def _locate(filename, root=os.curdir):
    for path, dirs, files in os.walk(os.path.abspath(root)):
        if filename in files:
            yield os.path.join(path, filename)


def main():
    for x in _locate('requirements.txt'):
        with open(x, 'r') as f:
            for t in parse(f):
                print t.key, t.specs

if __name__ == '__main__':
    main()
