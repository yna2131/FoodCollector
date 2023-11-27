# TC2008B Modelación de Sistemas Multiagentes con gráficas computacionales
# Python server to interact with Unity via POST
# Sergio Ruiz-Loza, Ph.D. March 2021

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json

from foodCollectModel import FoodModel

# # Model parameters
# WIDTH = 20
# HEIGHT = 20
# COUNT_FOOD = 47
# NUM_EXPLORERS = 3
# NUM_COLLECTORS = 2
# STEPS = 1500

class Server(BaseHTTPRequestHandler):
    
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_GET(self):
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        position = {
            "x" : 1,
            "y" : 2,
            "z" : 3
        }

        self._set_response()
        self.wfile.write(str(position).encode('utf-8'))

"""
    class Server(BaseHTTPRequestHandler):

    @property
    def api_response(self):
        model = FoodModel(GRID_WIDTH, GRID_HEIGH,
                             N_EXPLORERS, N_COLELCTORS, MAX_FOOD)

        for _ in range(MAX_STEPS):
            model.step()
            if not model.running:
                break
        data = model.datacollector.get_model_vars_dataframe().get("Data")
        data = list(data)

        return json.dumps({"steps": len(data), "data": data}).encode()

    def do_GET(self):
        if self.path == '/':
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(self.api_response))

"""


def run(server_class=HTTPServer, handler_class=Server, port=8585):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd...\n") # HTTPD is HTTP Daemon!
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:   # CTRL+C stops the server
        pass
    httpd.server_close()
    logging.info("Stopping httpd...\n")

if __name__ == '__main__':
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()



