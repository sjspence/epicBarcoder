def exportFasta(reads, outFileName):
    outFile = open(outFileName, 'w')
    for read in reads:
	outFile.write(read.header + '\n')
	outFile.write(read.seq + '\n')
    outFile.close()

def exportPairedFasta(pairedReads, outFileName, outFileNameN):
    outFile = open(outFileName, 'w')
    outFileN = open(outFileNameN, 'w')
    for read in pairedReads:
	outFile.write(read.header1 + '\n')
	outFile.write(read.seq + '\n')
	outFileN.write(read.header1 + '\n')
	outFileN.write(read.seqN + '\n')
    outFile.close()
    outFileN.close()

def exportOTUtable(df, outFileName):
    outFile = open(outFileName, 'w')
    outFile.write('\t')
    outFile.write('\t'.join(df.columns.values) + '\n')
    for row in df.iterrows():
        index, data = row    
        outFile.write(index + '\t')
        outFile.write('\t'.join(map(str, data.tolist())) + '\t')
        outFile.write('\t'.join(tax2[index]) + '\n')
