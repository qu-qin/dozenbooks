import json
import providers.vdisk as client

from google.appengine.api import taskqueue


def test(token_response):

    access_token = "7fc3146662b8C1H3PLEuh4b87uL14276"

    (queries, types) = client.build_search_query([
        {"steve": client.SearchType.NAME},
        {"mobi|txt": client.SearchType.EXTENSION}
    ])

    c = client.APIClient()
    results = c.search(access_token=access_token, query=queries, search_type=types, page_size=1)

    results = json.loads(results)
    print results

    file_name = results[0]['name'].encode("utf-8")
    print file_name

    download_link = results[0]['url']
    print download_link

    taskqueue.add(queue_name="fetch-and-email-queue",
                  url="/tasks/sender",
                  params={"file_name": file_name, "download_link": download_link})
