import pandas as pd
import sys
import pathlib

# To Run: `py addSentiment sentimentOutput.txt postFile.csv`
# Will save new file in same path named Sentiment_{postFile}.csv

sentiFile = sys.argv[1]
postFile = sys.argv[2]

try:
    sIn = pd.read_csv(sentiFile, sep=",", decimal="t", header=0, dtype='str')
    posts = pd.read_csv(postFile)
except:
    exit

outPath = str(pathlib.Path().absolute()) + "\Sentiment_" + postFile
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
print(posts.iloc[0:15,:])

posts.to_csv (outPath, index = False, header=True)