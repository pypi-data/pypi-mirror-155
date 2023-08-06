import os, sys
from distutils.core import setup
def findPackages(base):
    r = []
    for dir, dns, fns in os.walk(base + os.sep + 'appy'):
        r.append(dir[4:].replace(os.sep, '.'))
    return r

# Python 2 or 3 ?
base = 'py%d' % sys.version_info[0]
if base == 'py3':
    dependencies = ['zodb', 'DateTime']
    python = '>=3.6'
else:
    dependencies = []
    python = '>=2.4'

setup(name = "appy", version = "1.0.12",
      description = "The Appy framework",
      long_description = "Appy is the simpliest way to build complex webapps.",
      author = "Gaetan Delannay",
      author_email = "gaetan.delannay@geezteem.com",
      license = "GPL", platforms="all",
      url = 'https://appyframe.work',
      packages = findPackages(base),
      package_dir = {'appy': base + os.sep + 'appy'},
      package_data = {'':["*.*"]},
      install_requires = dependencies, python_requires = python)
