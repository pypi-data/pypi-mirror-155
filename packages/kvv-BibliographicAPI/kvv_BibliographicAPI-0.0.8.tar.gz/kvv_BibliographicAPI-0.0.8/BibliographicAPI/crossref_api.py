import requests
import json
from datetime import datetime
from dateutil.parser import parse as parseDate

from crossref.restful import Works
from StoredObjects import University, Publication
_baseUrl = 'https://api.crossref.org/'

def getPublicationByDOI(doi):
    works = Works()
    work = works.doi(doi)
    if work is None:
        return None
    publ = Publication()
    publ.title = work['title']
    publ.type = work['type']
    publ.doi = work['DOI'].lower()
    if 'ISSN' in work:
        publ.issn = work['ISSN']
    publ.citations = work['is-referenced-by-count']
    publ.publisher = work['publisher']
    publishedDate = "-".join(str(part) for part in work['published']['date-parts'][0])
    indexedDate = "-".join(str(part) for part in work['indexed']['date-parts'][0])
    publ.publishedDate = parseDate(publishedDate).date()
    publ.indexedDate = parseDate(indexedDate).date()
    publ.containerTitle = work['container-title']

    authors = work['author']

    return publ


def getPublicationsByPeriod(author, fromDate, toDate):
    splitName = author.engName.split(' ')
    family = splitName[0]
    given = splitName[1]
    queryName = given + ' ' + family
    dateFormat = '%Y-%m-%d'
    fromFormat = 'from-created-date:' + fromDate.strftime(dateFormat)
    toFormat = 'until-created-date:' + toDate.strftime(dateFormat)

    query = _baseUrl + 'works?query.author=' + queryName + '&filter=' + fromFormat + ',' + toFormat

    
    response = requests.get(query)
    json_str = response.text
    x = json.loads(json_str)

    publications = []

    message = x['message']
    if message is None:
        return []
    items = message['items']
    if items is None:
        return []
    for item in items:
        correctAuthor = False
        authors = item['author']
        for au in authors:
            if 'given' not in au.keys():  # в авторах может быть универ
                continue

            if au['given'].startswith(given) and au['family'] == family \
                    or au['family'].startswith(given) and au['given'] == family:  # имя и фамилия могут быть изменены местами
                secondName = ''
                if len(splitName) > 2:
                    secondName = splitName[2][0] + '.'

                if au['given'] == given or au['given'] == given + ' ' + secondName:
                    correctAuthor = True

        if correctAuthor:
            doi = item['DOI']
            publ = getPublicationByDOI(doi)
            if publ is None:
                continue
            publications.append(publ)


    return publications
