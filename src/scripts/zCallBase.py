#! /usr/bin/env python

# Iain Bancarz, ib5@sanger.ac.uk, January 2013

# Define 'base' class containing useful methods for zcall scripts

from GTC import *
from BPM import *
from EGT import *

class zCallBase:

    def __init__(self, threshPath, bpmPath, egtPath):
        [self.threshPath, self.bpmPath, self.egtPath] = \
            [threshPath, bpmPath, egtPath]
        (self.thresholdsX, self.thresholdsY) = self.readThresholds(threshPath)
        self.bpm = BPM(bpmPath)
        self.egt = EGT(egtPath)

    def call(self, gtc, i):
        # re-call ith SNP in GTC file, using zcall thresholds
        # call codes: 0 - "No Call", 1 - AA, 2 - AB, 3 - BB
        normX = gtc.normXintensities[i]
        normY = gtc.normYintensities[i]
        Tx = self.thresholdsX[i]
        Ty = self.thresholdsY[i]
        call = None
        if normX < Tx and normY < Ty: ## Lower left quadrant
            call = 0
        elif normX >= Tx and normY <= Ty: ## Lower right quadrant
            call = 1
        elif normX < Tx and normY >= Ty: ## Upper left quadrant
            call = 3
        else: ## Upper right quadrant
            call = 2
        return call

    def findMAF(self, nAA, nBB, nAB):
        # find minor allele frequency
        maf = None
        if nAA > nBB:
            maf = (nAB + 2 * nBB) / float(2*(nAA + nAB + nBB))
        else:
            maf = (nAB + 2 * nAA) / float(2*(nAA + nAB + nBB))
        return maf

    def normalizeCall(self, call, nAA, nBB):
        ## Normalization:  Flip genotype call so 1 is always the common allele homozygote and 3 is the minor allele homozygote
        # enforces convention that major allele is on X intensity axis
        # allele counts taken from EGT object
        if nBB > nAA: 
            if call == 1:
                call = 3
            elif call == 3:
                call = 1
        return call

    def readThresholds(self, inPath):
        # read a thresholds.txt file; return lists of x and y thresholds
        thresholdsX = []
        thresholdsY = []
        for line in open(inPath, 'r'):
            line = line.replace("\n", "")
            if line.find("Tx") != -1:
                continue
            else:
                fields = line.split("\t")
                if fields[1] != "NA":
                    tx = float(fields[1])
                else:
                    tx = fields[1]
                if fields[2] != "NA":
                    ty = float(fields[2])
                else:
                    ty = fields[2]
                thresholdsX.append(tx)
                thresholdsY.append(ty)
        return (thresholdsX, thresholdsY)
