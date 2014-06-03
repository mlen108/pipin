from cStringIO import StringIO
import contextlib
import os
import sys

try:
    unicode
except NameError:
    # Python 3
    basestring = unicode = str

import pipin

# TODO: that should somehow come from pipin
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)


class Data(object):
    pass


@contextlib.contextmanager
def capture():
    old = sys.stdout
    capturer = StringIO()
    sys.stdout = capturer
    data = Data()
    yield data
    sys.stdout = old
    data.result = capturer.getvalue()


def pr(text, color):
    return "\x1b[1;%dm" % (30 + color) + text + "\x1b[0m\n"


class TestPipin(object):
    def print_header_for(self, req_file):
        here = os.path.join(os.path.dirname(__file__), 'test_project')
        project = here.split('/')[-1].upper()
        req_file = "%s/%s" % (here, req_file)
        return pr("%s (%s)" % (project, req_file), YELLOW)

    def print_summary(self, text, found=0, not_found=0):
        s = pr("\nSearched 1 projects for %s:" % (text), WHITE)
        s += pr(" %s found" % found, CYAN)
        s += pr(" %s not found" % not_found, RED)
        return s


class TestPipinCommands(TestPipin):
    def setup(self):
        self.hdr = self.print_header_for("requirements.txt")

    def test_cmd_valid(self):
        with capture() as output:
            pipin.lets_pipin(['Django==1.4.2'], '.')

        expected_output = self.hdr + pr("Django==1.4.2 found", CYAN)
        expected_output += self.print_summary(text='Django==1.4.2', found=1)

        assert output.result == expected_output

    def test_cmd_invalid(self):
        with capture() as output:
            pipin.lets_pipin(["Flask"], '.')

        expected_output = self.hdr + pr("Flask not found", RED)
        expected_output += self.print_summary(text='Flask', not_found=1)

        assert output.result == expected_output

    def test_regex_valid(self):
        with capture() as output:
            pipin.lets_pipin(["South*=0.7"], '.')

        expected_output = self.hdr + pr("South>=0.7 found", CYAN)
        expected_output += self.print_summary(text='South*=0.7', found=1)

        assert output.result == expected_output

    def test_regex_invalid(self):
        with capture() as output:
            pipin.lets_pipin(["Django*1.6"], '.')

        expected_output = self.hdr + pr("Django*1.6 not found", RED)
        expected_output += self.print_summary(text='Django*1.6', not_found=1)

        assert output.result == expected_output

    def test_multiple_cmd(self):
        with capture() as output:
            pipin.lets_pipin(["Flask", "Django"], '.')

        expected_output = self.hdr + pr("Flask not found", RED)
        expected_output += pr("Django found", CYAN)
        expected_output += self.print_summary(text='Flask', not_found=1)
        expected_output += self.print_summary(text='Django', found=1)

        assert output.result == expected_output


class TestPipinCustomCommands(TestPipin):
    def setup(self):
        self.hdr = self.print_header_for("test_requirements.txt")

    def test_custom_requirements_file(self):
        with capture() as output:
            pipin.lets_pipin(['nose'], '.', 'test_requirements.txt')

        expected_output = self.hdr + pr("nose not found", RED)
        expected_output += self.print_summary(text='nose', not_found=1)

        assert output.result == expected_output
