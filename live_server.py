import http.server
import socketserver
import webbrowser
import threading
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and (event.src_path.endswith('.html') or 
                                       event.src_path.endswith('.css') or 
                                       event.src_path.endswith('.js')):
            print(f'Reloading browser due to changes in {event.src_path}')
            # 在這裡可以添加瀏覽器重新整理的邏輯

def start_server():
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        print(f'Serving at http://localhost:{PORT}')
        httpd.serve_forever()

def start_file_watcher():
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    return observer

def open_browser():
    webbrowser.open(f'http://localhost:{PORT}')

def main():
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    file_watcher = start_file_watcher()
    open_browser()

    try:
        file_watcher.join()
    except KeyboardInterrupt:
        file_watcher.stop()
    file_watcher.join()

if __name__ == '__main__':
    main()
