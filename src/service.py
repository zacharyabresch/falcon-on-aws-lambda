import awsgi
import falcon
import json

from wsgiref.simple_server import make_server

DEGS = [
    {"breed": "Pitbull"},
    {"breed": "Collie"},
    {"breed": "Bulldog"},
    {"breed": "Husky"},
]


class DogsResource:
    def on_get(self, request, response):
        """Handles GET requests and returns dogs"""
        response.status = falcon.HTTP_200  # alternatively, HTTP_OK
        response.media = DEGS


app = falcon.App()
dogs = DogsResource()
app.add_route("/degs", dogs)


def handler(event, context):
    """Lambda handler function (i.e. `service.handler`)"""
    return awsgi.response(app, event, context)


if __name__ == "__main__":
    with make_server("", 8000, app) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()
