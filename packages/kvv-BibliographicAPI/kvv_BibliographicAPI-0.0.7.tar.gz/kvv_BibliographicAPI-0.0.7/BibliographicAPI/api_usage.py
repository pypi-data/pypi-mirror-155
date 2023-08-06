from StoredObjects import Author, Publication
from . import *


def collectAuthorApiData(author, fromDate, toDate):
    publications = []
    if author is not None:
        if author.orcID is None:
            author.orcID = orcid_api.getOrcidByName(author)
            publons_api.addAuthorIDs(author)

        publonsPubls = publons_api.getPublicationsOfAuthor(author)
        for publon in publonsPubls:
            if fromDate <= publon.publishedDate <= toDate:
                scopusPub = scopus_api.indexRetrieval(publon.doi)
                publon.enrich(scopusPub)

                if not publon.searchAuthor(author):
                    author.addPublication(publon)
                    publications.append(publon)

        crossrefPubls = crossref_api.getPublicationsByPeriod(author, fromDate, toDate)
        for cross in crossrefPubls:
            doi = cross.doi
            scopusPub = scopus_api.indexRetrieval(doi)
            cross.enrich(scopusPub)
            if scopusPub is not None:  # add only publs from Crossref existing in Scopus
                # check if this pub already is added from Publons
                publon = None
                for pub in publications:
                    if cross.doi == pub.doi:
                        publon = pub
                if publon is not None:
                    publon.enrich(cross)
                else:
                    # not exists in Publons, add new
                    author.addPublication(cross)
                    publications.append(cross)
    return publications

