import json
import webapp2


class APIHandler(webapp2.RequestHandler):

    def send(self, response=None, status=200):
        self.response.headers["Content-Type"] = "application/json"
        self.response.status_int = status
        self.response.write(json.dumps(response or {}))
