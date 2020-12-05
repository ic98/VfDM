#!/usr/bin/env python
import argparse
import re
from datetime import datetime
from bs4 import BeautifulSoup

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
                        default="output.csv",
                        help="Specific output name")
    
    parser.add_argument('-ds',
                        '--dateStart',
                        help="Date start (DD-MM-YYYY")

    parser.add_argument('-de',
                        '--dateEnd',
                        help="Date end (DD-MM-YYYY)")

    return parser

def access_file(file_path):
    text = ''

    with open(file_path, 'rb') as file:
        text = file.read().decode()
        file.close()
    
    return text


def write_file(text, file_path):

    new_file = open(file_path, "w", encoding='utf-8')
    new_file.write(text)
    new_file.close()


def clean_text(text):
    soup = BeautifulSoup(text)
    clean = soup.get_text()
    clean = re.sub('<code>.*?</code>','', text, flags=re.DOTALL)
    
    return clean


if __name__ == '__main__':
    args = init_parser().parse_args()

    csv_file = args.filePath
    out_file = args.outputFile
    date_start = args.dateStart
    date_end = args.dateEnd

    print(csv_file)
    print(out_file)
    print(date_start)
    print(date_end)

    file = access_file(csv_file)

    cleaned = clean_text(file)

    write_file(cleaned, out_file)






