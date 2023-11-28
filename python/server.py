# TC2008B Modelación de Sistemas Multiagentes con gráficas computacionales
# Python server to interact with Unity via POST
# Sergio Ruiz-Loza, Ph.D. March 2021

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json

from foodCollectModel import FoodModel

WIDTH = 20
HEIGHT = 20
COUNT_FOOD = 47
NUM_EXPLORERS = 3
NUM_COLLECTORS = 2
STEPS = 1500


class CustomServer(BaseHTTPRequestHandler):
           	
    def _run_simulation(self):
        model = FoodModel(
            WIDTH, HEIGHT, NUM_EXPLORERS, NUM_COLLECTORS, COUNT_FOOD)

        for i in range(STEPS):
            if model.collected_food < 47:
                model.step()
            else:
                break

        data = model.datacollector.get_model_vars_dataframe().to_dict('records')

        # floor = model.get_floor()
        # agents = model.get_agent_positions()

        for iter in range(len(data)):
            flatFloor = []
            for row in data[iter]['Floor']:
                for col in row:
                    flatFloor.append(col)
            data[iter]['Floor'] = flatFloor

            flatExplorers = []

            for row in data[iter]['AgentPositions']:
                for col in row:
                    flatExplorers.append(col)
            data[iter]['AgentPositions'] = flatExplorers

        

        return json.dumps({"steps": len(data), "data": data}).encode()



    def do_GET(self):
        if self.path == "/":
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(self._run_simulation()))


def run(server_class=HTTPServer, handler_class=CustomServer, port=8585):
    logging.basicConfig(level=logging.INFO)
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd...\n")  # HTTPD is HTTP Daemon!
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:  # CTRL+C stops the server
        pass
    httpd.server_close()
    logging.info("Stopping httpd...\n")


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()



