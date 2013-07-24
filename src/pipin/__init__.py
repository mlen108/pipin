import os


def _locate(filename, root=os.curdir):
    for path, dirs, files in os.walk(os.path.abspath(root)):
        if filename in files:
            yield os.path.join(path, filename)


def main():
    for x in _locate('requirements.txt'):
        print x

if __name__ == '__main__':
    main()
