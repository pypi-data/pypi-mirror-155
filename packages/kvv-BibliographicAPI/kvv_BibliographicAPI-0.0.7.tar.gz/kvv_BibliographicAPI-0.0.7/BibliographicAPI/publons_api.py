import requests
import json
from StoredObjects import Author, Publication
from datetime import datetime
from dateutil import parser

_token = None
_baseUrl = 'https://publons.com/api/v2/'


def setToken(token):
    # try to make a request with this token, if incorrect, TypeError will be thrown
    global _token
    _token = token
    _request('academic/0')

def hasToken():
    return _token

def _request(url):
    global _token
    if _token == None:
        print("Publons token was not provided")
        return
    headers = {'Authorization': 'Token ' + _token, 'Content-Type': 'application/json'}
    url = url.removeprefix(_baseUrl)
    r = requests.get(_baseUrl + url, headers=headers)
    r = r.json()
    if 'detail' in r:
        if r['detail'] == 'Invalid token.':
            _token = None
            raise TypeError('Некорректный токен Publons')
        if r['detail'] == 'Invalid token header. No credentials provided.':
            _token = None
            raise TypeError('Токен Publons не предоставлен')

    else:
        return r


def _getID(author: Author):
    id = author.publonsID
    if id is None:
        id = author.researcherID
    if id is None:
        id = author.orcID
    return id


def addAuthorIDs(author: Author):
    id = _getID(author)
    if id is None:
        return False
    url = 'academic/' + id
    json_obj = _request(url)
    ids = json_obj['ids']
    author.publonsID = ids['id']
    author.researcherID = ids['rid']
    author.orcid = ids['orcid']
    return True


def getPublicationsOfAuthor(author: Author):
    id = _getID(author)
    if id is None:
        return []

    url = 'academic/publication/?academic=' + str(id)
    json_obj = _request(url)
    while True:
        results = json_obj['results']
        for res in results:
            info = res['publication']

            pub = Publication()
            pub.title = info['title']
            date = info['date_published']
            if date is not None and date != "":
                pub.publishedDate = parser.parse(date).date()

            ids = info['ids']
            if ids is not None:
                pub.doi = ids['doi'].lower()
                pub.ut = ids['ut']
                pub.wosLink = f'https://gateway.webofknowledge.com/gateway/Gateway.cgi?GWVersion=2&SrcApp=Publons&SrcAuth=Publons_CEL&KeyUT=WOS:000304359700014&DestLinkType=FullRecord&DestApp=WOS_CPL'
                existingPub = author.searchPublicationByDOI(pub.doi)
                if existingPub is not None:
                    existingPub.enrich(pub)
                else:
                    author.addPublication(pub)

        url = json_obj['next']
        if url is None:
            break
        json_obj = _request(url)
    return author.publications


def getAuthorsOfUniversity():
    inst = 'Murmansk State Technical University'
    url = 'academic/?institution=' + inst
    json_obj = _request(url)
    while True:
        print(json_obj['count'])

        url = json_obj['next']
        if url is None:
            break
        json_obj = _request(url)

