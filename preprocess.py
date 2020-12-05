#!/usr/bin/env python
import argparse
import re
import pandas as pd
from datetime import datetime

def main():
    args = init_parser().parse_args()

    csv_file = args.filePath
    out_file = args.outputFile
    date_start = args.dateStart
    date_end = args.dateEnd
    
    df = pd.read_csv(csv_file, parse_dates=['CreationDate'])

    filtered = filter_df(df, date_start, date_end)
    cleaned = clean_df(filtered)
    df_to_csv(cleaned, out_file)


def filter_df(df, date_start = None, date_end = None):
    filtered = df

    # filter by date range if both dates are provided
    if date_start and date_end:
        filtered = df.loc[(df['CreationDate'] > pd.to_datetime(date_start)) & (df['CreationDate'] < pd.to_datetime(date_end))]

    if 'Title' in filtered.columns:
        # filter title and/or body
        filtered = filtered[['Id', 'Title', 'Body']]
        # make body and title columns into their own rows
        filtered = filtered.melt(id_vars = ['Id'], var_name = "Title", value_name = "Text")[['Text']] 
    else:
        filtered = filtered[['Body']]

    return filtered


def clean_df(df):
    regex_code = re.compile('<code>.*?</code>', flags=re.DOTALL)
    regex_html = re.compile('<[^>]+>')
    regex_newline = re.compile("\\t|\\n|\\r")

    # remove code blocks
    cleaned = df.replace(regex_code, '', regex=True)

    # remove html blocks
    cleaned = cleaned.replace(regex_html, '', regex=True)

    #remove new line
    cleaned = cleaned.replace(regex_newline, ' ', regex=True)

    return cleaned

def df_to_csv(df, output_path):
    df.to_csv(output_path, index=None, header=0)


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

    return parser

if __name__ == '__main__':
    main()