from epics import caget
import numpy as np


def readMatrix(basename, rows, cols, firstRow=1, firstCol=1, suffix=None):
    '''
    Reads epics channels to put matrix on a EPICS channel matrix.
    '''
    inpMat = np.zeros((rows, cols))
    for ii in range(firstRow, firstRow + rows):
        for jj in range(firstCol, firstCol + cols):
            chName = basename + '_' + str(ii) + '_' + str(jj)
            if suffix is not None:
                chName = chName + '_' + suffix
            inpMat[ii - firstRow, jj-firstCol] = caget(chName)
    return inpMat
