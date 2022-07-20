from utils import text_utils


def create_person(given_name, family_name, base_uri="http://connectome.ch/person/"):
    cleaned_firstname = text_utils.url_safe_text(given_name)
    cleaned_lastname = text_utils.url_safe_text(family_name)

    iri = "{}{}{}".format(base_uri, cleaned_firstname, cleaned_lastname)
    person_mapped = {
        '@id': iri,
        '@type': 'schema:Person',
        'schema:familyName': family_name,
        'schema:givenName': given_name,
        'schema:name': ' '.join([given_name, family_name])
    }
    return person_mapped
