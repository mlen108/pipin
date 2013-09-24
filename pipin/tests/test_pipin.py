import os
import subprocess

here = os.path.abspath(os.path.dirname(__file__))
req_file = "%s/requirements.txt" % here


# TODO: that should somehow come from pipin
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

def pr(text, color, prefix=''):
    return prefix + "\x1b[1;%dm" % (30 + color) + text + "\x1b[0m\n"


class TestPipinCommands(object):
    def test_cmd_valid(self):
        app_name = "Django==1.4.2"

        output = subprocess.check_output(["pipin", app_name, "."])
        expected_output = pr("%s (%s)" % (here.split('/')[-1].upper(), req_file), YELLOW)
        expected_output += pr("%s found" % app_name, CYAN, '- ')

        assert output == expected_output

    def test_cmd_invalid(self):
        app_name = "Flask"

        output = subprocess.check_output(["pipin", app_name, "."])
        expected_output = pr("%s (%s)" % (here.split('/')[-1].upper(), req_file), YELLOW)
        expected_output += pr("%s not found" % app_name, RED, '- ')

        assert output == expected_output
