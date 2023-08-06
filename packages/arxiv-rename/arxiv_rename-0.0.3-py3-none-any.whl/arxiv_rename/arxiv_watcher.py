import re
import sys
import time
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler
from arxiv_rename.arxiv_detect import detect_arxiv
from arxiv_rename.arxiv_rename import arxivRename

class MyHandler(RegexMatchingEventHandler):
    def on_moved(self, event):
        if not detect_arxiv(event.dest_path):
            return
        arxivRename(event.dest_path)
        return

    def on_created(self, event):
        if not detect_arxiv(event.src_path):
            return
        arxivRename(event.src_path)
        return


def scheduleWatcher(dir=None):

    path = dir if dir is not None else '.'
    event_handler = MyHandler(ignore_directories=True, case_sensitive=False)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    print(f'Watching for file changes in {path}')
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main():
    scheduleWatcher(sys.argv[1])

if __name__ == 'main':
    main()