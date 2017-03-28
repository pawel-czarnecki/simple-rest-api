from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from database import Database
import json
import threading


class RestApiData(Database):
    def __init__(self):
        super(RestApiData, self).__init__()

    def get_server_response(self):
        """
        :return: All server responses stored in database
        """
        return self.select('SELECT * FROM server_response')


class RestApiHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Rest API handler used to return suitable endpoint data formatted in JSON."""
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/api/responseList':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            data = RestApiData()
            response_list = []
            for time, code in data.get_server_response():
                response_list.append({'time': time, 'code': code})

            self.wfile.write(bytes(json.dumps({'responseList': response_list}), "utf8"))
        else:
            self.send_response(503)

        return


class RestApiHTTPServer(HTTPServer):
    def run(self):
        """Start Rest API server"""
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.server_close()


class RestApi:
    """Implementation of Rest API server."""
    def __init__(self, address='127.0.0.1', port=8000):
        self.__rest_api = RestApiHTTPServer((address, port), RestApiHTTPRequestHandler)
        self.__thread = threading.Thread()
        self.is_running = False

    def start(self):
        """
        :return: New thread of Rest API server
        """
        self.__thread = threading.Thread(None, self.__rest_api.run)
        self.__thread.start()
        self.is_running = True
        return self.__thread

    def stop(self):
        """Shutdown Rest API server."""
        self.__rest_api.shutdown()
        self.__thread.join()
        self.is_running = False
