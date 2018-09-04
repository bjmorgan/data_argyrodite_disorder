#! /usr/bin/env python3

import platform
import pip
import sys

def pip_freeze():
    try:
        from pip._internal.operations import freeze
    except ImportError:  # pip < 10.0
        from pip.operations import freeze
    return freeze.freeze()

def print_sys_info():
    print('# Platform\n')
    print('platform :', platform.platform())
    print('system   :', platform.system())
    print('node     :', platform.node())
    print('release  :', platform.release())
    print('version  :', platform.version())
    print('machine  :', platform.machine())
    print('processor:', platform.processor())
    print()
    print('# Python Interpreter\n')
    print('Python Version :', platform.python_version())
    print('Compiler       :', platform.python_compiler())
    print('Build          :', platform.python_build())
    print()

def main( output='stdout' ):
    if output is not 'stdout':
        sys.stdout = open(output, 'w')
    print_sys_info()
    print( '# Frozen Python Modules\n' )
    for p in pip_freeze():
        print( p )

if __name__ == '__main__':
    main()

