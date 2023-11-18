import http.server
import threading
import socketserver
import subprocess
import sys

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from _logger import get_logger

logger = get_logger(__name__)

class ReloadHandler(PatternMatchingEventHandler):
    """ 
    Regenerate the site when a change occurs on the patterns specified
    on super.__init__(patterns=[<patterns>])
    """
    def __init__(self):
      super(ReloadHandler, self).__init__(
        ignore_patterns=["__pycache__/*", "__pycache__", "*.swp"],
        patterns=["_templates/*", "_posts/*"]
    )

    def process(self, event):
        logger.info("Regenerating site")
        run = subprocess.run(["python3", "_p.py"], capture_output=True)
        if run.returncode == 0:
            logger.info("Site regenerated")
            return True
        print(run.stderr.decode("utf-8"))
        logger.info("Unable to regenerate site")
        return False

    def on_modified(self, event):
        logger.info("file modified " + event.src_path)
        self.process(event)


def server():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("127.0.0.1", 8000), handler) as httpd:
        print("Serving at port 8000")
        httpd.serve_forever()


def main():
    path = '.'
    event_handler = ReloadHandler()
    # Server start
    server_daemon = threading.Thread(target=server)
    server_daemon.daemon = True
    server_daemon.start()
    # Observer start
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        exit(0)
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    main()   
