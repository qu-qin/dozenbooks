import httplib

from endpoints.api import APIHandler
from appengine_config import APP_CONFIG as config

from google.appengine.api import taskqueue

QUEUE_CONFIG = config["FETCH_AND_EMAIL_QUEUE"]


class SendHandler(APIHandler):

    def put(self):

        body = self.request.body

        if body:
            taskqueue.add(queue_name=QUEUE_CONFIG["NAME"],
                          url=QUEUE_CONFIG["URL"],
                          params={"job": body})

        self.send(status=httplib.OK)
