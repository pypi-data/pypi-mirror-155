if 'backUpVals' not in globals():
    globals()['backUpVals'] = {}
if 'restoreMethods' not in globals():
    globals()['restoreMethods'] = {}

from .readMatrix import readMatrix
from .writeMatrix import writeMatrix, restoreMatrix
from .caput import caput, restoreChannel
from .writeChannels import writeChannels
from .restoreEpics import restoreEpics
from epics import caget
