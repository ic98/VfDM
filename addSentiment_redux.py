import argparse
import csv
import re
import pandas as pd
import numpy as np
import sys
import pathlib
import os

# To Run: `py addSentiment sentimentOutput.txt postFile.csv`
# Will save new file in same path named Sentiment_{postFile}.csv
def main():
    if len(sys.argv) == 4:
        rawFile = sys.argv[1]
        resultsFolder = sys.argv[2]
        chunks = int(sys.argv[3])
    else:
        print(len(sys.argv))
        print("Please add more arguments (inputFileName, sentimentFileFolder, number of chunks")
        exit

    if chunks == 1:
        try:
            sIn = pd.read_csv(resultsFolder, sep=",", decimal="t", header=0, dtype='str')
            posts = pd.read_csv(rawFile)
            outPath = str(pathlib.Path().absolute()) + "\\"+ resultsFolder + "_results\Sentiment_" + resultsFolder + ".csv"
            #print(outPath)
            posts = appendSentiment(sIn, posts)
            posts.to_csv (outPath, index = False, header=True)
            exit
        except:
            print("File reading went wrong")
            exit
    else:
        try:
            rawFile = pd.read_csv(rawFile)
            if not os.path.exists(resultsFolder+"_results"):
                os.makedirs(resultsFolder+"_results")
            outPath = str(pathlib.Path().absolute()) + "\\"+ resultsFolder + "_results\Sentiment_" + resultsFolder
            print(outPath)
            input_split = np.array_split(rawFile, chunks)
            
            for i in range(chunks):
                resultsFile = resultsFolder + "/" + str(i) + "_" + resultsFolder + "_results.csv"
                sIn = pd.read_csv(resultsFile, sep=",", decimal="t", header=0, dtype='str')
                tempSplit = input_split[i]
                tempSplit.reset_index(inplace=True, drop=True)
                currentSplit = appendSentiment(sIn, tempSplit)
                currentSplit.to_csv(outPath + ".csv")

            newFile = pd.read_csv(outPath+ ".csv")
            newFile = newFile.sort_values(by=['Sentiment'])
            newFile.to_csv(outPath + "_sorted.csv")
            
            tempFile = newFile[newFile['Sentiment'] == 'negative']
            tempFile.to_csv(outPath +"_negative.csv")
            
            tempFile = newFile[newFile['Sentiment'] == 'neutral']
            tempFile.to_csv(outPath +"_neutral.csv")
            
            tempFile = newFile[newFile['Sentiment'] == 'positive']
            tempFile.to_csv(outPath +"_positive.csv")
            
            exit
        except:
            print("Evan messed up")            
            exit

def appendSentiment(sIn, posts):
#print(outPath)
    sIn.columns = ["tID", "Sentiment"]
    sIn['index'] = sIn['tID'].str.slice(1)
    sIn['index'] = sIn['index'].astype(int)
    sIn.set_index('index', inplace=True, verify_integrity=True) # return false if duplacite tID's in ssentiFile

    # Sorting below should be unneccesary - can be useful for cheking debug output though
    # sIn.sort_values('index', inplace=True, ascending=True)
    # print(sIn)

    posts = posts.join(sIn["Sentiment"])

    # DEBUG (Can Remove): Print first 15 rows to preview data
    #print(posts.iloc[0:15,:])
    
    return posts

if __name__ == '__main__':
    main()