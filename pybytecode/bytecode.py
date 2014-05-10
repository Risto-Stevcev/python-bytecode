#!/usr/bin/env python
import marshal
import struct
import time
import imp
import sys
import os


class Compiler(object):
    def __init__(self, path):
        with open(path, 'r') as f:
            self.data = f.read()
        self.filename = os.path.basename(path)
        self.dirname = os.path.dirname(os.path.abspath(path))

        self.magic_number = imp.get_magic()
        self.modification_date = struct.pack('i', int(time.time()))
        self.padding = b'A\x00\x00\x00'

        self.code = compile(self.data, self.filename, 'exec')
        self.bytes_code = marshal.dumps(self.code)


    def compile(self):
        with open(os.path.join(self.dirname, self.filename + 'c'), 'wb') as f:
            f.write(self.magic_number)
            f.write(self.modification_date)
            if sys.version_info.major == 3:
                f.write(self.padding)
            f.write(self.bytes_code)


def main():
    if len(sys.argv) != 2:
        print('Usage: %s [python file]' % sys.argv[0])
        sys.exit(1)

    compiler = Compiler(sys.argv[1])
    compiler.compile()


if __name__ == '__main__':
    main()
