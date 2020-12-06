#!/usr/bin/env python
import argparse
import csv
import re
import pandas as pd
import numpy as np
from datetime import datetime

# disable chained assignments
pd.options.mode.chained_assignment = None 

def main():
    args = init_parser().parse_args()

    csv_file = args.filePath
    out_file = args.outputFile
    date_start = args.dateStart
    date_end = args.dateEnd
    num_of_chunks = args.chunks
    
    df = pd.read_csv(csv_file, parse_dates=['CreationDate'])

    filtered = filter_df(df, date_start, date_end)
    cleaned = clean_df(filtered)
    df_to_csv(cleaned, num_of_chunks, out_file)


def filter_df(df, date_start = None, date_end = None):
    filtered = df

    # filter by date range if both dates are provided
    if date_start and date_end:
        filtered = df.loc[(df['CreationDate'] > pd.to_datetime(date_start)) & (df['CreationDate'] < pd.to_datetime(date_end))]

    if 'Title' in filtered.columns:
        # filter title and/or body
        filtered = filtered[['rownum', 'Title', 'Body']]
        filtered['Body'] = filtered['Title'].astype(str) + " " + df['Body']

    filtered = filtered[['rownum', 'Body']]

    # rename rownum so that it matches predictions Row
    filtered.rename(columns = {'rownum': 'Row'}, inplace = True)

    return filtered

def clean_df(df):
    cleaned = df

    regex_code = re.compile('<code>.*?</code>', flags=re.DOTALL)
    regex_hyperlink = re.compile('<a.*?</a>', flags=re.DOTALL)
    regex_html = re.compile('<[^>]+>')
    regex_newline = re.compile("\\t|\\n|\\r")

    # remove code blocks
    cleaned = cleaned.replace(regex_code, '', regex=True)
    
    #remove new line
    cleaned = cleaned.replace(regex_hyperlink, ' ', regex=True)

    # remove html blocks
    cleaned = cleaned.replace(regex_html, '', regex=True)

    #remove new line
    cleaned = cleaned.replace(regex_newline, '', regex=True)

    return cleaned

def df_to_csv(df, chunks, output_path):
    if chunks > 1:
        df_split = np.array_split(df, chunks)
        for i in range(len(df_split)):
            df_split[i].to_csv(str(i) + "_" + output_path, index=None)
    else:
        df.to_csv(output_path, index=None)

def init_parser():
    parser = argparse.ArgumentParser(
        prog="Data pre-processor",        
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Pre-process data for Senti4SD")

    parser.add_argument('-fp',
                        '--filePath',
                        required=True,
                        help="Path to file")
                        
    parser.add_argument('-o',
                        '--outputFile',
                        default="./output.csv",
                        help="Specific output name")
    
    parser.add_argument('-ds',
                        '--dateStart',
                        type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(),
                        help="Date start (DD-MM-YYYY")

    parser.add_argument('-de',
                        '--dateEnd',
                        type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(),
                        help="Date end (DD-MM-YYYY)")

    parser.add_argument('-c',
                        '--chunks',
                        default=1,
                        type=int, choices=range(1, 10),
                        help="Number of chunks to split file into (1-10)")

    return parser

if __name__ == '__main__':
    main()