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


def pr(text, color, prefix=''):
    return prefix + "\x1b[1;%dm" % (30 + color) + text + "\x1b[0m\n"


class TestPipin(object):
    def _prepare(self, req_file):
        project = here.split('/')[-1].upper()
        req_file = "%s/%s" % (here, req_file)
        return pr("%s (%s)" % (project, req_file), YELLOW)


class TestPipinCommands(TestPipin):
    def setup(self):
        self.hdr = self._prepare("requirements.txt")

    def test_cmd_valid(self):
        app_name = "Django==1.4.2"

        output = subprocess.check_output(["pipin", app_name, "."])
        output = output.decode(encoding='UTF-8')
        expected_output = self.hdr + pr("%s found" % app_name, CYAN, '- ')

        assert output == expected_output

    def test_cmd_invalid(self):
        app_name = "Flask"

        output = subprocess.check_output(["pipin", app_name, "."])
        output = output.decode(encoding='UTF-8')
        expected_output = self.hdr + pr("%s not found" % app_name, RED, '- ')

        assert output == expected_output

    def test_multiple_cmd(self):
        app_name1 = "Flask"
        app_name2 = "Django"

        output = subprocess.check_output(["pipin", app_name1, app_name2, "."])
        output = output.decode(encoding='UTF-8')
        expected_output = self.hdr + pr("%s not found" % app_name1, RED, '- ') + pr("%s found" % app_name2, CYAN, '- ')

        assert output == expected_output


class TestPipinMultipleCommands(TestPipin):
    def setup(self):
        self.hdr = self._prepare("dev_requirements.txt")

    def test_custom_requirements_file(self):
        app_name = "nose"

        output = subprocess.check_output(["pipin", app_name, ".", "-f",
            "dev_requirements.txt"])
        output = output.decode(encoding='UTF-8')
        expected_output = self.hdr + pr("%s found" % app_name, CYAN, '- ')

        assert output == expected_output
