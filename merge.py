#!/usr/bin/env python
import argparse
import csv
import re
import pandas as pd
from datetime import datetime

def main():
    args = init_parser().parse_args()

    original_csv = args.filePath
    predictions_csv = args.predictionsPath
    output_path = args.outputFile

    



def clean_predictions_id(pdf):
    df = pdf
    df['Row'] = df['Row'].str.replace(r'\t','').astype(int)

    return df


def init_parser():
    parser = argparse.ArgumentParser(
        prog="Data merger",        
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Merge predictions file with original csv file")

    parser.add_argument('-fp',
                        '--filePath',
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