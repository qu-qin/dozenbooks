import logging
import httplib
import traceback

from endpoints.api import APIHandler
from appengine_config import APP_CONFIG as config

import providers.vdisk as client

VDISK_CONFIG = config["PROVIDERS"]["VDISK"]
OAUTH_CLIENT = client.OAuth2Client(VDISK_CONFIG["APP_KEY"], VDISK_CONFIG["APP_SECRET"])
API_CLIENT = client.APIClient()

DEFAULT_PAGE_SIZE = config["PAGE_SIZE"]


class SearchHandler(APIHandler):

    def get(self):

        auth_provider = self.request.headers.get("x-auth-provider")
        auth_token = self.request.headers.get("x-auth-token")
        refresh_token = self.request.headers.get("x-auth-refresh-token")
        query = self.request.get("query")
        page = self.request.get("page") or "1"
        page_size = self.request.get("page_size") or DEFAULT_PAGE_SIZE

        if not auth_provider and not auth_token and not refresh_token:
            self.send(status=httplib.UNAUTHORIZED)
            return

        if not query:
            self.send(response=[])
            return

        logging.info("[Search] auth provider: %s, auth token: %s, refresh token: %s",
                     auth_provider,
                     auth_token,
                     refresh_token)

        response = {}

        # fresh token means the auth token is exchanged from refresh token, if the auth token
        # is obtained from client request, it's not a fresh token
        fresh_token = False

        # if we don't have auth token, use refresh token to get the auth token first
        if not auth_token:
            logging.info("[Search] no auth token, try to get auth token from refresh token")
            try:
                token_response = self.get_auth_token(refresh_token)
                logging.info("[Search] got auth token %s", token_response)
                auth_token = token_response["token"]
                fresh_token = True
                response["renew_token"] = token_response
            except ValueError:
                logging.error(traceback.format_exc())
                self.send(status=httplib.UNAUTHORIZED)
                return

        # first attempt
        (status, results) = self.search(query, auth_token, page, page_size)

        # if we are using old auth token and server responses with unauthorized
        # let's try to get the token from refresh token and search again
        if status == httplib.UNAUTHORIZED and not fresh_token:
            logging.info("[Search] got 401 from first attempt search, try to get auth token from refresh token")
            try:
                token_response = self.get_auth_token(refresh_token)
                logging.info("[Search] got auth token %s", token_response)
                auth_token = token_response["token"]
                response["renew_token"] = token_response
                # second attempt
                logging.info("[Search] second attempt search")
                (status, results) = self.search(query, auth_token, page, page_size)
            except ValueError:
                logging.error(traceback.format_exc())
                self.send(status=httplib.UNAUTHORIZED)
                return

        response["results"] = results

        if "renew_token" in response:
            response["renew_token"]["provider"] = auth_provider

        self.send(status=status, response=response)

    def get_auth_token(self, refresh_token):
        (status, token_response) = OAUTH_CLIENT.request_access_token(grant_type="refresh_token",
                                                                     refresh_token=refresh_token,
                                                                     call_back_url=self.request.path_url)
        if status != httplib.OK:
            raise ValueError("Failed to get auth token from refresh token")

        return token_response

    def search(self, keyword, auth_token, page, page_size):

        (queries, types) = client.build_search_query([
            {keyword: client.SearchType.NAME},
            {"mobi|txt|epub": client.SearchType.EXTENSION}
        ])

        return API_CLIENT.search(access_token=auth_token,
                                 query=queries,
                                 search_type=types,
                                 page=page,
                                 page_size=page_size)
