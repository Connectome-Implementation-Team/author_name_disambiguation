import os
import json

input_dir = 'input'

def load_files(input_dir):
    documents = dict()
    persons = dict()
    orgs = dict()
    for f in os.listdir(input_dir):
        if f.endswith('.json'):
            graph = json.load(open(input_dir + '/' + f, 'r'))["@graph"]
    
            for node in graph:
                if "schema:author" in node:  # if the thing has an author (includes Books, Datasets, etc.)
                    documents[node["@id"]] = node
                
                elif node["@type"] == "schema:Person":  # if the node is a person
                    persons[node["@id"]] = node

                elif node["@type"] == "schema:Organization":  # if the node is an org, used for affiliation
                    orgs[node["@id"]] = node["schema:name"]

    return documents, persons, orgs


def flatten_docs(documents, persons, orgs):
    flat_documents = dict()
    for doc in documents:
        authors = list()
        for author in documents[doc]["schema:author"]:
            author_id = author["@id"]
            a = {
                "id": author_id,
                "name": persons[author_id]["schema:name"]
            }
            if "schema:affiliation" in persons[author_id]:
                if not isinstance(persons[author_id]["schema:affiliation"], list):
                    org_id = persons[author_id]["schema:affiliation"]["@id"]
                    a["org"] = orgs[org_id]
                else:
                    a["org"] = ", ".join([orgs[affiliation["@id"]] for affiliation in persons[author_id]["schema:affiliation"]])
            authors.append(a)
        
        d = {
            "authors": authors,
            "title": documents[doc]["schema:name"]
        }
        #abstract, keywords, year, venue?
        if "schema:abstract" in documents[doc]:
            d["abstract"] = documents[doc]["schema:abstract"]

        if "schema:keywords" in documents[doc]:
            d["keywords"] = documents[doc]["schema:keywords"]
        
        if "schema:datePublished" in documents[doc]:  # publications
            d["year"] = documents[doc]["schema:datePublished"]["@value"][:4]
        elif "schema:startDate" in documents[doc]:  # projects: startDate is a good enough approximation
            d["year"] = documents[doc]["schema:startDate"]["@value"][:4]
        
        flat_documents[doc] = d

    return flat_documents
                    

if __name__ == '__main__':
    documents, persons, orgs = load_files(input_dir)
    flat_documents = flatten_docs(documents, persons, orgs)
    with open("disambiguation/data/raw_documents.json", "w") as outfile:
        json.dump(flat_documents, outfile)
