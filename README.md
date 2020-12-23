# VfDM
Data mining (COMP 4710) project

## How to install dependencies

`pip install -r requirements.txt`
# preprocess.py
## How to run

`py preprocess.py -fp [FILEPATH] -ds [DATE_START | optional] -de [DATE_END | optional] -c [NUM OF CHUNKS | optional]`

- example: `py preprocess.py -fp C-Questions.csv -ds 2008-01-01 -de 2018-01-01 -c 4` 

# addSentiment.py
## How to run

`py addSentiment.py rawDataFile.csv resultsFolder #ofchunks`
- Will save new files in new folder named resultsFolder_results
- Results folder should have sentiment result files with file names - fileNumber_resultsFolder_results.csv
- example: `py addSentiment.py C-Questions.csv C-questions 9` 
- example result file: `0_C-questions_results.csv`


**5 files will be generated**
- rawDatafile with sentiment appended
- sentiment ordered raw data file
- rows with negative sentiment
- rows with positive sentiment
- rows with neutral sentimen
