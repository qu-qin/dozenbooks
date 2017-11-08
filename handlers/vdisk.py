import logging

from handlers.base import BaseHandler
from appengine_config import APP_CONFIG as config

import providers.vdisk as client


VDISK_CONFIG = config["PROVIDERS"]["VDISK"]
OAUTH_CLIENT = client.OAuth2Client(VDISK_CONFIG["APP_KEY"], VDISK_CONFIG["APP_SECRET"])


class VdiskHandler(BaseHandler):

    def get(self):
        code = self.request.get("code")
        # not callback request, redirect to authorize page
        if not code:
            self._authorize_redirect()
            return
        logging.debug("[vdisk] authorize code %s", code)
        # request access token
        (_, response) = OAUTH_CLIENT.request_access_token(code=code, call_back_url=self.request.path_url)
        # sample response
        # {"access_token":"f578ca6662b8C1H3PLEuh4b87uLcae4a","expires_in":1424899107,"time_left":86400,"uid":"1996858161","refresh_token":"4ec6de6662b8C1H3PLEuh4b87uLde4ca"}
        self.render_template("auth/token.html", token=response)


    def _authorize_redirect(self):
        authorize_url = OAUTH_CLIENT.get_authorization_url(call_back_url=self.request.path_url)
        logging.debug("[vdisk] authorize url %s", authorize_url)
        self.redirect(authorize_url)
