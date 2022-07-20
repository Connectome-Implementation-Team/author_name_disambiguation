from utils import name_utils, entity_utils


def disambiguate_authors(scholarly_article):
    """
    Takes as input an object of type ScholarlyArticle in JSON-LD format with author list in plain string format,
    and returns a list of ScholarlyArticle with authors as Person entities as well as said Person entities as JSON-LD.
    :param scholarly_article:
    :return return_graph:
    """
    # TODO: deduplication of persons with same name & IRI via lookup. Needs to receive full SNF person IRI list
    # TODO: deduplication of persons under consideration of project-publication-affiliation

    list_of_authors = name_utils.multiple_author_split(scholarly_article["schema:author"])

    # initialize author list empty
    scholarly_article["schema:author"] = []

    return_graph = []

    for author in list_of_authors:
        firstname, lastname = name_utils.single_author_split(author)
        person = entity_utils.create_person(firstname, lastname, "http://snf.ch/person/")

        scholarly_article["schema:author"].append({"@id": person["@id"]})
        return_graph.append(person)

    return_graph.append(scholarly_article)
    return return_graph

