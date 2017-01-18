import os
import urllib
import urlparse

import posixpath

import boto.cloudsearch

conn = boto.connect_cloudsearch2(region="us-east-1",
                aws_access_key_id='AKIAIWCSSPJXIVZTN4KA',
                aws_secret_access_key='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')

directory = os.path.dirname(os.path.realpath(__file__)) + '/RunningShoes'

if not os.path.exists(directory):
    os.makedirs(directory)

domain = conn.lookup('refresh-12-28')

page_index = 0

size = 100

search_service = domain.get_search_service()

results = search_service.search(q="(prefix field='brandcard_category_ids' 'Running Road Shoes')", parser="structured", size=size)

total_pages = results.num_pages_needed

while page_index < total_pages - 1:

    for doc in results.docs:
        url = doc['fields']['images'][0]
        path = urlparse.urlsplit(url).path
        filename = posixpath.basename(path)

        urllib.urlretrieve(url, directory +  '/' + filename)

    page_index += 1

    results = search_service.search(q="(prefix field='brandcard_category_ids' 'Running Road Shoes')", parser="structured", start=(page_index*size) + 1)