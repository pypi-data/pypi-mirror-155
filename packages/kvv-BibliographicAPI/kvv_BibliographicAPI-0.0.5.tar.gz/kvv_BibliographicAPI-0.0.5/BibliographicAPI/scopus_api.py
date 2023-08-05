import requests
import json
from StoredObjects import Publication

_baseUrl = 'https://api.elsevier.com/'
_abstractUrl = _baseUrl + 'content/abstract/'


def getIndexType(index=""):
    indexType = None
    if index.startswith("SCOPUS"):
        indexType = "scopus_id/"
    if index.startswith("10."):
        indexType = "doi/"
    if index.startswith("2-s2."):
        indexType = "eid/"
    return indexType


def indexRetrieval(index=""):
    indexType = getIndexType(index)
    if indexType is None:
        return None

    finalUrl = _abstractUrl + indexType + index

    params = {'httpAccept': 'application/json'}
    response = requests.get(finalUrl, params)
    json_str = response.text

    x = json.loads(json_str)
    if 'service-error' in x.keys():
        return None

    publ = Publication()
    response = x['abstracts-retrieval-response']
    if response is None:
        return None
    data = response['coredata']
    if data is None:
        return None

    if 'dc:identifier' in data.keys():
        publ.scopusId = data['dc:identifier']
    if 'eid' in data.keys():
        publ.eid = data['eid']
    if 'pii' in data.keys():
        publ.pii = data['pii']

    return publ
