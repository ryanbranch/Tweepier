import math

#The file path to the text used to build every corpus
CORPORA_FILE = "corpora.txt"
CORPUS_OUT_PREFIX = "corpus_"
CORPUS_OUT_SUFFIX = ".txt"
FILENAMES_FILE = "corpus_filenames.txt"

#The target number of lines from CORPORA_FILE to include in a single corpus
#Assuming that CORPORA_FILE is consists of at least TARGET_CORPUS_SIZE lines,
#Every corpus file generated will be this many lines until the last, which will
#be anywhere from (0.5 * TARGET_CORPUS_SIZE lines) to TARGET_CORPUS_SIZE lines.
TARGET_CORPUS_SIZE = 500

def splitCorpora():
    fileNum = 0
    newFile = False

    #counts the number of lines in CORPORA_FILE
    numLines = -1
    with open(CORPORA_FILE, 'rb') as corpora:
        for numLines, line in enumerate(corpora):
            pass
    numLines += 1
    corpora.close()

    linesRemaining = numLines
    numFilesOut = int(math.ceil(float(numLines) / TARGET_CORPUS_SIZE))
    linesFileOut = numLines / numFilesOut

    fileNames = []

    print(str(numFilesOut - 1))
    with open(CORPORA_FILE, 'rb') as corpora:
        for i in range(numFilesOut):
            outFileName = CORPUS_OUT_PREFIX + str(i) + CORPUS_OUT_SUFFIX
            fileNames.append(outFileName)
            outFile = open(outFileName, 'wb')
            if (i != numFilesOut - 1):
                for j in range(linesFileOut):
                    outFile.write(corpora.readline())
                outFile.close()

            #If we're dealing with the last file out
            else:
                for j in range(linesFileOut + (numLines % linesFileOut)):
                    outFile.write(corpora.readline())
                outFile.close()
    corpora.close()

    outFile = open(FILENAMES_FILE, 'wb')
    for name in fileNames:
        outFile.write(name)
        outFile.write("\n")
    outFile.close()

splitCorpora()