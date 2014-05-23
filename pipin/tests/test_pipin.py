import os
import subprocess

try:
    unicode
except NameError:
    # Python 3
    basestring = unicode = str

here = os.path.abspath(os.path.dirname(__file__))

# TODO: that should somehow come from pipin
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)


def pr(text, color):
    return "\x1b[1;%dm" % (30 + color) + text + "\x1b[0m\n"


def check_output(cmd):
    return subprocess.Popen(
        cmd, stdout=subprocess.PIPE, universal_newlines=True).communicate()[0]


class TestPipin(object):
    def print_header_for(self, req_file):
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
        output = check_output(["pipin", "Django==1.4.2", "."])

        expected_output = self.hdr + pr("Django==1.4.2 found", CYAN)
        expected_output += self.print_summary(text='Django==1.4.2', found=1)

        assert output == expected_output

    def test_cmd_invalid(self):
        output = check_output(["pipin", "Flask", "."])

        expected_output = self.hdr + pr("Flask not found", RED)
        expected_output += self.print_summary(text='Flask', not_found=1)

        assert output == expected_output

    def test_regex_valid(self):
        output = check_output(["pipin", "South*=0.7", "."])

        expected_output = self.hdr + pr("South>=0.7 found", CYAN)
        expected_output += self.print_summary(text='South*=0.7', found=1)

        assert output == expected_output

    def test_regex_invalid(self):
        output = check_output(["pipin", "Django*1.6", "."])

        expected_output = self.hdr + pr("Django*1.6 not found", RED)
        expected_output += self.print_summary(text='Django*1.6', not_found=1)

        assert output == expected_output

    def test_multiple_cmd(self):
        output = check_output(["pipin", "Flask", "Django", "."])

        expected_output = self.hdr + pr("Flask not found", RED)
        expected_output += pr("Django found", CYAN)
        expected_output += self.print_summary(text='Flask', not_found=1)
        expected_output += self.print_summary(text='Django', found=1)

        assert output == expected_output


class TestPipinCustomCommands(TestPipin):
    def setup(self):
        self.hdr = self.print_header_for("dev_requirements.txt")

    def test_custom_requirements_file(self):
        output = check_output([
            "pipin", "nose", ".", "-f", "dev_requirements.txt"
        ])

        expected_output = self.hdr + pr("nose found", CYAN)
        expected_output += self.print_summary(text='nose', found=1)

        assert output == expected_output
