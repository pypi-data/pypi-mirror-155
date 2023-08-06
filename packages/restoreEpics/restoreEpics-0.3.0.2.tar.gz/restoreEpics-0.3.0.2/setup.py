from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

version = '0.3.0.2'
short_des = ('A simple package that gives wrapped caput and writeMatrix '
             + 'functions for writing EPICS channels which save previous '
             + 'values and a restoreEpics function can be used later to '
             + 'restore all values in case of error, interrupt, or as a '
             + 'final restore.')
dwnld_url = ('https://gitlab.com/anchal-physics/restoreepics/-/archive/'
             + version + '/restoreepics-' + version + '.tar.gz')
# Chose either "3 - Alpha" or "4 - Beta"
# or "5 - Production/Stable" as the current state of your package
classifiers = ['Development Status :: 4 - Beta',
               'Intended Audience :: Developers',
               'Topic :: Software Development :: Build Tools',
               'License :: OSI Approved :: MIT License',
               'Programming Language :: Python :: 3']

setup(name='restoreEpics',
      packages=['restoreEpics'],
      version=version,
      license='LICENSE',
      description=short_des,
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Anchal Gupta',
      author_email='anchal@caltech.edu',
      url='https://gitlab.com/anchal-physics/restoreepics',
      download_url=dwnld_url,
      keywords=['EPICS', 'RESTORE', 'MATRIX'],
      install_requires=['pyepics', 'argparse', 'numpy', 'PyYAML'],
      classifiers=classifiers,
      scripts=['bin/readMatrix', 'bin/writeMatrix', 'bin/caputt'])
