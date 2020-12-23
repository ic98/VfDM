import argparse
import csv
import re
import pandas as pd
import numpy as np
import sys
import pathlib
import os

# To Run: `py addSentiment.py rawDataFile.csv resultsFolder #ofchunks`
# Will save new files in new folder named resultsFolder_results
# 5 files will be generated
# - rawDatafile with sentiment appended
# - sentiment ordered raw data file
# - rows with negative sentiment
# - rows with positive sentiment
# - rows with neutral sentiment

def main():
    if len(sys.argv) == 4:
        rawFile = sys.argv[1]
        resultsFolder = sys.argv[2]
        chunks = int(sys.argv[3])
    else:
        print(len(sys.argv))
        print("Please add more arguments (rawFileName, sentimentFileFolder, number of chunks")
        exit

    if chunks == 1:
        try:
            sIn = pd.read_csv(resultsFolder, sep=",", decimal="t", header=0, dtype='str')
            posts = pd.read_csv(rawFile)
            outPath = str(pathlib.Path().absolute()) + "\\"+ resultsFolder + "_results\Sentiment_" + resultsFolder + ".csv"
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
            input_split = np.array_split(rawFile, chunks)
            
            for i in range(chunks):
                resultsFile = resultsFolder + "/" + str(i) + "_" + resultsFolder + "_results.csv"
                sIn = pd.read_csv(resultsFile, sep=",", decimal="t", header=0, dtype='str')
                tempSplit = input_split[i]
                tempSplit.reset_index(inplace=True, drop=True)
                currentSplit = appendSentiment(sIn, tempSplit)
                if i > 0:
                    currentSplit.to_csv(outPath + ".csv", mode = "a", header = False)
                else:
                    currentSplit.to_csv(outPath + ".csv")

            newFile = pd.read_csv(outPath+ ".csv")
            newFile.dropna(how="all", inplace=True)
            newFile.to_csv(outPath+ ".csv")
            newFile = newFile.sort_values(by=['Sentiment'])
            newFile.to_csv(outPath + "_sorted.csv")
            print(newFile.shape[0]) #total number of rows
            
            tempFile = newFile[newFile['Sentiment'] == 'negative']
            print(tempFile.shape[0]) #number of negative sentiment rows
            tempFile.to_csv(outPath +"_negative.csv")
            
            tempFile = newFile[newFile['Sentiment'] == 'neutral']
            print(tempFile.shape[0]) #number of neutral sentiment rows
            tempFile.to_csv(outPath +"_neutral.csv")
            
            tempFile = newFile[newFile['Sentiment'] == 'positive']
            print(tempFile.shape[0]) #number of positive sentiment rows
            tempFile.to_csv(outPath +"_positive.csv")

            print("done")
            
            exit
        except:
            print("Evan messed up")            
            exit

def appendSentiment(sIn, posts):
    sIn.columns = ["tID", "Sentiment"]
    sIn['index'] = sIn['tID'].str.slice(1)
    sIn['index'] = sIn['index'].astype(int)
    sIn.set_index('index', inplace=True, verify_integrity=True) # return false if duplacite tID's in ssentiFile

    posts = posts.join(sIn["Sentiment"])
    
    return posts

if __name__ == '__main__':
    main()