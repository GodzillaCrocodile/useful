# 'EStroev'
import argparse
from datetime import datetime
import os

__author__ = "EStroev <jenya.stroev(at)gmail.com>"
__email__ = "jenya.stroev@gmail.com"


def main():
    parser = argparse.ArgumentParser(description='IP search in the RIPE.net database')
    parser.add_argument('-p', dest='terminal_print', action='store_true', help='Print to console')
    parser.add_argument('-f', dest='input_file', action='store', help='Input file with IP list for searching')

    args = parser.parse_args()
    outFolder = os.path.dirname(os.path.abspath(args.outFile))
    
    if not args.inPath:
        print('[-] You must specify an existing input path!')
        exit(-1)
    elif not os.path.exists(args.inPath):
        print('[-] Input path %s does not exist!' % os.path.abspath(args.inPath))
        exit(-1)
    if not args.outFolder:
        print('[-] You must specify an existing path to the output folder!')
        exit(-1)
    elif not os.path.exists(args.outFolder):
        print(f'[-] Output folder {os.path.abspath(args.outFolder)} does not exist!')
        os.makedirs(args.outFolder)
        print(f'[+] Create output folder {args.outFolder}')
    elif not os.path.exists(outFolder):
        print(f'[-] Output folder {outFolder} does not exist!')
        os.makedirs(outFolder)
        print(f'[+] Create output folder {outFolder}')
        
    startTime = datetime.now()
    print(startTime.strftime('[*] Start time: %d.%m.%Y %H:%M:%S'))

    endTime = datetime.now()
    print('[*] Total elapsed time - {0} seconds'.format((endTime - startTime).seconds))
    print(endTime.strftime('[*] End time: %d.%m.%Y %H:%M:%S'))

if __name__ == '__main__':
    main()