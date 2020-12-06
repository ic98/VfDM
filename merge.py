#!/usr/bin/env python
import argparse
import csv
import re
import pandas as pd
from datetime import datetime

def main():
    args = init_parser().parse_args()

    merge_type = args.type
    original_csv = args.origFilePath
    predictions_csv = args.predictionsPath
    output_path = args.outputFile

    odf = pd.read_csv(original_csv)
    
    starting_id = odf['rownum'][0]

    print(starting_id)


    odf.rename(columns = {'rownum': 'Row'}, inplace = True)

    print(odf)


    pdf = pd.read_csv(predictions_csv)
    pdf = clean_predictions_id(pdf)

    pdf['Row'] += starting_id

    print(pdf)

    df = pd.merge(odf, pdf, on="Row", how="outer")

    print(df)
    df.to_csv(output_path, index=None)


def clean_predictions_id(pdf):
    df = pdf
    df['Row'] = df['Row'].str.replace(r't','').astype(int)

    return df


def init_parser():
    parser = argparse.ArgumentParser(
        prog="Data merger",        
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Merge predictions file with original csv file")

    parser.add_argument('-t',
                        '--type',
                        required=True,
                        help="Type of file to merge (q - questions | a - answers")

    parser.add_argument('-ofp',
                        '--origFilePath',
                        required=True,
                        help="Path to original file")
                        
    parser.add_argument('-pp',
                        '--predictionsPath',
                        required=True,
                        help="Path to file")
                        
    parser.add_argument('-o',
                        '--outputFile',
                        default="./merged.csv",
                        help="Specific output name")

    return parser

if __name__ == '__main__':
    main()