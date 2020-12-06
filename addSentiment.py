import pandas as pd
import sys
import pathlib

# To Run: `py addSentiment sentimentOutput.txt postFile.csv`
# Will save new file in same path named Sentiment_{postFile}.csv

sentiFile = sys.argv[1]
postFile = sys.argv[2]

try:
    sIn = pd.read_csv(sentiFile, sep=",", header=0)
    posts = pd.read_csv(postFile)
except:
    exit

outPath = str(pathlib.Path().absolute()) + "\Sentiment_" + postFile

print(outPath)
sIn.columns = ["tID", "Sentiment"]
sIn = sIn.sort_values('tID', ascending=True)
posts = posts.join(sIn["Sentiment"])

# DEBUG (Can Remove): Print first 15 rows to preview data
print(posts.iloc[0:15,:])

posts.to_csv (outPath, index = False, header=True)