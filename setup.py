#!/usr/bin/env python3

import sys, os, re, subprocess as sp
try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

if sys.version_info < (3,3):
    sys.exit("Python 3.3+ is required; you are using %s" % sys.version)

########################################

# Based on this recipe, adapted for Python 3, Git 2.8.x, and PEP-440 version identifiers
#   https://web.archive.org/web/20180119150411/http://blogs.nopcode.org/brainstorm/2013/05/20/pragmatic-python-versioning-via-setuptools-and-git-tags/
#   https://www.python.org/dev/peps/pep-0440/#version-scheme

# Fetch version from git tags, and write to version.py.
# Also, when git is not available (PyPi package), use stored version.py.
version_py = os.path.join(os.path.dirname(__file__), 'vpn_slice', 'version.py')

try:
    version_git = sp.check_output(["git", "describe", "--tags", "--dirty=_dirty"]).strip().decode('ascii')
    final, dev, blob, dirty = re.match(r'v?((?:\d+\.)*\d+)(?:-(\d+)-(g[a-z0-9]+))?(_dirty)?', version_git).groups()
    version_pep = final+('.dev%s+%s'%(dev,blob) if dev else '')+(dirty if dirty else '')
except:
    d = {}
    with open(version_py, 'r') as fh:
        exec(fh.read(), d)
        version_pep = d['__version__']
else:
    with open(version_py, 'w') as fh:
        print("# Do not edit this file; versioning is governed by git tags", file=fh)
        print('__version__="%s"' % version_pep, file=fh)

########################################

setup(name="vpn_slice",
      version="0.1",
      description=("vpnc-script replacement for easy split-tunnel VPN setup"),
      long_description=open('README.md').read(),
      author="Daniel Lenski",
      author_email="dlenski@gmail.com",
      install_requires=[],
      license='GPL v3 or later',
      url="https://github.com/dlenski/vpn-slice",
      packages=["vpn_slice"],
      include_package_data = True,
      entry_points={ 'console_scripts': [ 'vpn-slice=vpn_slice.main:main' ] }
      )
