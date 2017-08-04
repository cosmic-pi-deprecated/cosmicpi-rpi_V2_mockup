import http.server
import socketserver
import threading
import os


class StaticContentServerHandler(object):
    def __init__(self, httpd):
        self._httpd = httpd

    def run(self):
        self._httpd.serve_forever()


class StaticContentServer(object):
    @staticmethod
    def async_start(port=8080, directory='web'):
        # Configure web directory
        web_dir = os.path.join(os.path.dirname(__file__), '../' + directory)
        os.chdir(web_dir)

        # Start web server
        handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(('', port), handler)
        print("Serving an application at port:", port)

        # Start serving a content
        static_content_server_handler = StaticContentServerHandler(httpd=httpd)
        thread = threading.Thread(target=static_content_server_handler.run)
        thread.start()
