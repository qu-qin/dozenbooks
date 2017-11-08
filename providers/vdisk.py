import urllib
import urllib2
import httplib
import json
import traceback
import logging

from google.appengine.api import urlfetch


class OAuth2Client(object):

    AUTHORIZE_URL = "https://auth.sina.com.cn/oauth2/authorize?%s"
    ACCESS_TOKEN_URL = "https://auth.sina.com.cn/oauth2/access_token"

    def __init__(self, app_key, app_secret):
        self.app_key = app_key
        self.app_secret = app_secret

    def get_authorization_url(self, response_type="code", display="default", state="", call_back_url=""):
        params = {
            "client_id": self.app_key,
            "response_type": response_type,
            "display": display,
            "redirect_uri": call_back_url
        }
        if state:
            params["state"] = state
        return OAuth2Client.AUTHORIZE_URL % urllib.urlencode(params)

    def request_access_token(self, grant_type="authorization_code", code="", refresh_token="", call_back_url=""):
        params = {
            "client_id": self.app_key,
            "client_secret": self.app_secret,
            "grant_type": grant_type
        }
        # authorization request
        if grant_type == "authorization_code":
            params["code"] = code
            params["redirect_uri"] = call_back_url
        # refresh request
        elif grant_type == "refresh_token":
            params["refresh_token"] = refresh_token
        # request token
        try:
            urlfetch.set_default_fetch_deadline(59)
            request = urllib2.Request(OAuth2Client.ACCESS_TOKEN_URL)
            response = urllib2.urlopen(request, urllib.urlencode(params))
            return (response.code, self.parse_token_response(response.read()))
        except urllib2.HTTPError as err:
            return (err.code, err.msg)
        except urllib2.URLError as err:
            return (httplib.INTERNAL_SERVER_ERROR, err.reason)

    def parse_token_response(self, token_response):
        token_info = json.loads(token_response)
        return {
            "provider": "vdisk",
            "token": token_info["access_token"],
            "expiry": token_info["expires_in"] * 1000,
            "refresh_token": token_info["refresh_token"]
        }


class APIClient(object):

    API_URL = "https://api.weipan.cn/2/"
    TIMEOUT = 30

    def __init__(self, root="basic"):
        self.root = root

    def get(self, host, api, queries=None):
        try:
            if isinstance(api, unicode):
                api = api.encode("utf-8")
            else:
                api = str(api)
            url = host.strip("/") + "/" + urllib.quote(api.strip("/"))
            queries = self.encode_queries(queries)

            urlfetch.set_default_fetch_deadline(59)
            request = urllib2.Request("%s?%s" % (url, queries))
            response = urllib2.urlopen(request)
            return (response.code, response.read())
        except urllib2.HTTPError as err:
            return (err.code, err.msg)
        except urllib2.URLError as err:
            return (httplib.INTERNAL_SERVER_ERROR, err.reason)

    def encode_queries(self, queries=None, **kwargs):
        queries = queries or {}
        queries.update(kwargs)
        args = []
        for key, value in queries.iteritems():
            if not value:
                continue
            if isinstance(value, unicode):
                normalised_value = value.encode("utf-8")
            else:
                normalised_value = str(value)
            args.append("%s=%s" % (key, urllib.quote(normalised_value)))
        return "&".join(args)

    def search(self, access_token, query, search_type=None, sort_order=None, page="1", page_size="20"):
        params = {
            "access_token": access_token,
            "query": query,
            "type": search_type,
            "sort_order": sort_order,
            "page": page,
            "page_size": page_size
        }
        (status, results) = self.get(APIClient.API_URL, "share/search", params)
        if status != httplib.OK:
            return (status, results)
        else:
            return (status, parse_search_results(results))


def build_search_query(query_type_maps):
    if not query_type_maps:
        return (None, None)
    queries = []
    types = []
    for query_type_map in query_type_maps:
        queries.extend(query_type_map.keys())
        types.extend(query_type_map.values())
    return (":".join(queries), ":".join(types))


def parse_search_results(search_results):
    results = []
    try:
        search_results = json.loads(search_results)
        for search_result in search_results:

            if search_result["is_dir"]:
                continue

            name = search_result["name"].encode("utf-8")
            size = search_result["size"]
            download_links = []

            if search_result["url"]:
                download_links.append(search_result["url"])

            if search_result["download_list"]:
                download_links += search_result["download_list"]

            if not name or not size or not download_links:
                continue

            results.append({
                "name": name,
                "size": size,
                "links": download_links
            })
    except Exception:
        logging.error(traceback.format_exc())
    return results


class SearchType(object):
    FULL_TEXT_SEARCH = "1"
    NAME = "2"
    TITLE = "3"
    DESCRIPTION = "4"
    FILE_TYPE = "5"
    EXTENSION = "6"
    GROUP = "7"


class SortOrder(object):
    SHARE_TIME = "sharetime"
    PRICE = "price"
    DEGREE = "degree"
    DOWNLOAD_COUNT = "count_download"
    SIZE = "bytes"
