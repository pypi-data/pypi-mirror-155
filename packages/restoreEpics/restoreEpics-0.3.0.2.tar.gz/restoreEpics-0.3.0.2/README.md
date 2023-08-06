# restoreEpics

A simple package that gives wrapped caput and writeMatrix functions for writing EPICS channels which save previous values and a restoreEpics function can be used later to restore all values in case of error, interrupt, or as a final restore.

## Usage

### Restoring channels

```python
from restoreEpics import restoreEpics, caput, caget

try:
    # do some work that uses caget or caput as usual
except BaseException:
    # Handle error cases
finally:
    restoreEpics()  # Will restore all changes to previous values
```

### Writing to matrices with form basename_ii_jj_suffix

```python
from restoreEpics import restoreEpics, writeMatrix

try:
    writeMatrix(basename, mat, suffix=suffix, tramp=10)
except BaseException:
    # Handle error cases
finally:
    restoreEpics()  # Will restore all changes to previous values
```

### Writing multiple channels with option of ramping together

```python
from restoreEpics import restoreEpics, writeChannels

try:
    chanInfo = {'channels': {'C1:FIRST_CH': {'value': 5},
                             'C1:SECON_CH': {'value': 10}},
                'tramp': 4}
    writeChannels(chanInfo)
except BaseException:
    # Handle error cases
finally:
    restoreEpics()  # Will restore all changes to previous values
```

### Make your own restoring methods

```python
from restoreEpics import restoreEpics, backUpVals, restoreMethods
from awg import Sine

def exciteSine(ch, freq, ampl, duration=10, ramptime=1, bak=backUpVals):
    exc = Sine(ch, freq, ampl, duration=duration)
    exc.start(ramptime=ramptime)
    if ch in bak:
        bak[ch] = {'type': 'excSine', # Store the exc object wth a type defined.
                   'name': ch, # Values
                   'exc': exc, # Values
                   'sno': len(bak)} # Assign a serial number like this



def restoreExc(bakVal):
    bakVal['exc'].stop()  # Restoring method for excitation.

# Add the restoring method to restoreMethods dictionary with type defined above as key
restoreMethods['excSine'] = restoreExc

try:
    exciteSine('blah', 0.5, 10)
except BaseException:
    # Handle error cases
finally:
    restoreEpics()  # Will restore all changes to previous values
```

## Command line tools
The readMatrix and writeMatrix functions are available as command line tools on installation through pip. Usage:
```bash
$ readMatrix -h
usage: readMatrix [-h] [--firstRow FIRSTROW] [--firstCol FIRSTCOL] [-s SUFFIX]
                  basename inMatFile rows cols

This reads matrix coefficients from EPICS channels to a text file to. Note
that all indices start from 1 by convention for EPICS channels.

positional arguments:
  basename              Matrix EPICS base name
  inMatFile             Input Matrix file name
  rows                  Number of rows to read. Default None(all)
  cols                  Number of columns to read. Default None(all)

optional arguments:
  -h, --help            show this help message and exit
  --firstRow FIRSTROW   First index of output. Default 1
  --firstCol FIRSTCOL   First index of input. Default 1
  -s SUFFIX, --suffix SUFFIX
                        Any suffix after the matrix indices in channel names.
                        Default is None.
```
```bash
$ writeMatrix -h
usage: writeMatrix [-h] [-r ROWS] [-c COLS] [--firstRow FIRSTROW]
                   [--firstCol FIRSTCOL] [--fileRowInd FILEROWIND]
                   [--fileColInd FILECOLIND] [-t TRAMP] [-s SUFFIX]
                   inMatFile basename

This writes matrix coefficients from a text file to EPICS channels. Note that
all indices start from 1 by convention for EPICS channels.

positional arguments:
  inMatFile             Input Matrix file name
  basename              Matrix EPICS base name

optional arguments:
  -h, --help            show this help message and exit
  -r ROWS, --rows ROWS  Number of rows to write. Default None(all)
  -c COLS, --cols COLS  Number of columns to write. Default None(all)
  --firstRow FIRSTROW   First index of output. Default 1
  --firstCol FIRSTCOL   First index of input. Default 1
  --fileRowInd FILEROWIND
                        First row index in file. Default 1
  --fileColInd FILECOLIND
                        First col index in file. Default 1
  -t TRAMP, --tramp TRAMP
                        Ramping time when chaning values. Default 3
  -s SUFFIX, --suffix SUFFIX
                        Any suffix after the matrix indices in channel names.
                        Default is None.
```
```bash
$ caputt -h
usage: caputt [-h] [-t TRAMP] [-w] [-o TIMEOUT] [chanInfo [chanInfo ...]]

This script is a version of nominal caput command with added functionality of
setting a tramp and reading a set of channels from yaml files if they need to
be set all together or ramped all together to new values.

positional arguments:
  chanInfo              Channel name and value pairs sepaated by space or name
                        of the yaml file containing them.

optional arguments:
  -h, --help            show this help message and exit
  -t TRAMP, --tramp TRAMP
                        Global ramping time in seconds.
  -w, --wait            Whether to wait until the processing has completed.
                        Global and would override any other value from
                        paramter file.
  -o TIMEOUT, --timeout TIMEOUT
                        how long to wait (in seconds) for put to complete
                        before giving up. Global and would override any other
                        value from paramter file.

Example use:
caputt C1:FIRST_CH 8.0
caputt C1:FIRST_CH 8.0 -t 5
caputt C1:FIRST_CH 8.0 C1:SECOND_CH 5.6 -t 6 -w -o 60
caputt channelsFile.yml
```
Example of channelsFile.yml
```yaml
channels:
  C1:FIRST_CH:
    value: 10
  C1:SECOND_CH:
    value: 20
  C1:THIRD_CH:
    value: 30
    tramp: 5   # Individual tramp, will get overridden by global tramp if present.
  C1:FOURTH_CH:
    value: 40
    timeout: 60  # Time after which the process will call it failed attempt.
    wait: True   # Will wait for the process to end
tramp: 5    # GLobal tramp, overrides individual tramp
```
