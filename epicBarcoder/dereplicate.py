#!/usr/bin/env python

import reads as rd

#Collapse identical reads into representative sequences to reduce the file
#size for usearch
#INPUT:  noPrimerFile is the clean 16S output of upstream primer filtering
#        outFasta is the output file where unique seqs are written along with
#            size designations for the number of identical reads
#OUTPUT: Dictionary mapping unique DNA sequence to a list of read objects that
#            contain it (from the input primer-filtered 16S file)
def getUniqueSeqs(noPrimerFile, outFasta):
    inReads = rd.importFasta(noPrimerFile)
    uniqueSeqs = {}
    uniqueReads = []
    outFile = open(outFasta, 'w')
    for read in inReads:
        if read.seq not in uniqueSeqs:
            uniqueSeqs[read.seq] = [read]
        else:
            uniqueSeqs[read.seq].append(read)
    for u in sorted(uniqueSeqs, key=lambda k: len(uniqueSeqs[k]), reverse=True):
        firstRead = uniqueSeqs[u][0]
        outFile.write(firstRead.header + ';size=' + str(len(uniqueSeqs[u])) + \
                        ';\n' + firstRead.seq + '\n')
    outFile.close()
    return uniqueSeqs

#Translate unoise2 output into headers of original reads
#INPUT:  unique dictionary created by getUniqueSeqs
#        reads imported from denoised otus
#OUTPUT: a file is written with all primer-filtered, denoised reads, plus otu
#	 information in their headers
def expandDenoised(uniqueDict, denoisedFile, outFileName):
    denoised = rd.importFasta(denoisedFile)
    outFile = open(outFileName, 'w')
    for otu in denoised:
        for read in uniqueDict[otu.seq]:
            otuID = otu.header.replace('>','').split(';')[0]
            newHeader = read.header + ';' + otuID + ';'
            outFile.write(newHeader + '\n')
            outFile.write(read.seq + '\n')
    outFile.close()

#Written specifically for uparse output
def uniqueSeqsToOTU(uparseMap):
    otuToHeaders = {}
    i = 1
    with open(uparseMap, 'r') as f:
        for line in f:
            line = line.strip().split('\t')
            if line[1] == 'OTU':
                otuToHeaders['OTU' + str(i)] = [line[0]]
                i += 1
    with open(uparseMap, 'r') as f:
        for line in f:
            line = line.strip().split('\t')
            if (line[1] == 'match') and ('top=OTU' in line[2]):
                otuID = line[2].split('top=')[1].split('(')[0].strip()
                otuToHeaders[otuID].append(line[0])
    return otuToHeaders
