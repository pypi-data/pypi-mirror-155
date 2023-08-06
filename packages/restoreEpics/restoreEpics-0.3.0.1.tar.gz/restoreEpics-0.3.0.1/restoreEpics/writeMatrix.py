from epics import caput
import numpy as np
from .readMatrix import readMatrix
from time import sleep
from . import backUpVals, restoreMethods


def writeMatrix(basename, inpMat, firstRow=1, firstCol=1, suffix=None,
                tramp=3.0, bak=backUpVals):
    '''
    Write epics channels to put matrix on a EPICS channel matrix.
    '''
    curMat = readMatrix(basename=basename, rows=inpMat.shape[0],
                        cols=inpMat.shape[1], firstRow=firstRow,
                        firstCol=firstCol, suffix=suffix)
    if basename not in bak:
        bak[basename] = {'type': 'matrix', 'name': basename, 'suffix': suffix,
                         'value': curMat, 'firstRow': firstRow,
                         'firstCol': firstCol,'tramp': tramp, 'sno': len(bak)}
    # Special case, changing filter gains, can use TRAMP
    rampYourself = True
    if suffix == 'GAIN':
        try:
            curTramp = readMatrix(basename=basename, rows=inpMat.shape[0],
                                  cols=inpMat.shape[1], firstRow=firstRow,
                                  firstCol=firstCol, suffix='TRAMP')
            for ii in range(firstRow, firstRow + np.shape(inpMat)[0]):
                for jj in range(firstCol, firstCol + np.shape(inpMat)[1]):
                    chName = (basename + '_' + str(ii) + '_' + str(jj)
                              + '_TRAMP')
                    caput(chName, tramp)
            rampYourself = False
        except BaseException:
            rampYourself = True
    if rampYourself:
        rampSteps = 100
        # Get current matrix values
        stepMat = (inpMat - curMat) / rampSteps
        for tstep in range(1, rampSteps):
            for ii in range(firstRow, firstRow + np.shape(inpMat)[0]):
                for jj in range(firstCol, firstCol + np.shape(inpMat)[1]):
                    chName = basename + '_' + str(ii) + '_' + str(jj)
                    if suffix is not None:
                        chName = chName + '_' + suffix
                    matToWrite = (curMat[ii-firstRow, jj-firstCol]
                                  + tstep * stepMat[ii-firstRow, jj-firstCol])
                    caput(chName, matToWrite)
            sleep(tramp/rampSteps)
    # Finally write the required matrix
    for ii in range(firstRow, firstRow + np.shape(inpMat)[0]):
        for jj in range(firstCol, firstCol + np.shape(inpMat)[1]):
            chName = basename + '_' + str(ii) + '_' + str(jj)
            if suffix is not None:
                chName = chName + '_' + suffix
            caput(chName, inpMat[ii-firstRow, jj-firstCol])
    if not rampYourself:
        sleep(tramp + 0.5)    # Wait for ramping to end
        for ii in range(firstRow, firstRow + np.shape(inpMat)[0]):
            for jj in range(firstCol, firstCol + np.shape(inpMat)[1]):
                chName = (basename + '_' + str(ii) + '_' + str(jj)
                          + '_TRAMP')
                caput(chName, curTramp[ii-firstRow, jj-firstCol])


def restoreMatrix(bakVal):
    writeMatrix(basename=bakVal['name'], suffix=bakVal['suffix'],
                inpMat=bakVal['value'], firstCol=bakVal['firstCol'],
                firstRow=bakVal['firstRow'], tramp=10, bak=[])


restoreMethods['matrix'] = restoreMatrix
