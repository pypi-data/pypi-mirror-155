# __main__.py

import sys
import argparse
import os
from arxiv_rename.arxiv_detect import detect_arxiv

from arxiv_rename.arxiv_rename import arxivRename
from arxiv_rename.arxiv_watcher import scheduleWatcher

def main():
    prog_parser = argparse.ArgumentParser(
        prog='arxiv_rename',
        description='Rename PDFs downloaded from arXiv.org',

    )

    prog_parser.add_argument('path', metavar='PATH', type=str, help="path to arXiv PDF or a folder of arXiv PDFs")

    prog_parser.add_argument('-w', '--watch', action='store_true', help="watch for new files in the folder specified by PATH")

    args = prog_parser.parse_args()

    input_path = args.path
    to_watch = args.watch

    if not os.path.exists(input_path):
        print('The path specified does not exist')
        sys.exit()

    if to_watch and os.path.isfile(input_path):
        print('Can only watch a directory for changes\nPATH specified is a file')
        sys.exit()

    # print(detect_arxiv("sample_pdfs/others/misc/1206.0049.pdf"))

    if to_watch:
        scheduleWatcher(input_path)
    else:
        if os.path.isfile(input_path):
            arxivRename(input_path)
        else:
            for root, subdirs, files in os.walk(input_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # print(file_path)
                    arxivRename(file_path)

                    

    

if __name__=="__main__":
    main()