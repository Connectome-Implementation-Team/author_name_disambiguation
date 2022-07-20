def single_author_split(author):
    """
    splits a string into first and last names where the name takes either
    - the form Lastname, Firstnames
    or
    - the form Firstnames Lastname
    """
    lastname_first = True if ',' in author else False

    # define parameters depending on name order
    split_char = ',' if lastname_first else ' '

    author = author.strip().split(split_char)

    if author[0] == 'and':
        author = author[1:]

    if len(author) > 2:
        # longer last name?
        if lastname_first and author[0].lower() in ['de', 'da', 'von', 'st', 'le', 'van']:
            firstname = ' '.join(author[2:])
            lastname = author[0] + ' ' + author[1]
        elif author[-2].lower() in ['de', 'da', 'von', 'st', 'le', 'van']:
            firstname = ' '.join(author[:-2])
            lastname = author[-2] + ' ' + author[-1]
        else:  # first+middle name(s)
            if lastname_first:
                firstname = ' '.join(author[1:])
                lastname = author[0]
            else:
                firstname = ' '.join(author[:-1])
                lastname = author[-1]
    elif len(author) == 2:
        if lastname_first:
            lastname = author[0]
            firstname = author[1]
        else:
            lastname = author[1]
            firstname = author[0]
    else:  # only one word name?
        lastname = author[0]
        firstname = ' '

    firstname = firstname.strip()
    lastname = lastname.strip()
    return firstname, lastname


def multiple_author_split(list_of_authors):
        if ";" in list_of_authors:
            authors = list_of_authors.split(';')
        elif "/" in list_of_authors:
            authors = list_of_authors.split('/')
        elif "&" in list_of_authors:
            authors = list_of_authors.split('&')
        else:
            if list_of_authors.strip().endswith(','):
                list_of_authors = list_of_authors.strip()[:-1]
            authors = list_of_authors.split(',')
            # if this yields len 2, we have only one author
            if len(authors) == 2:
                authors = [list_of_authors]

        split_authors = []
        for author in authors:
            author.replace('et al.', '')  # remove et al from name
            split_authors.append(author)

        return split_authors
