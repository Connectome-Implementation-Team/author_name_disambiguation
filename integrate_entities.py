import pickle
from wikimapper import WikiMapper
import numpy as np

mapper = WikiMapper("data/index_enwiki-latest.db")
biggraph_names = json.load(open("wikidata_translation_v1_names.json", "r"))
biggraph_vectors = np.load("wikidata_translation_v1_vectors.npy")
data_path = 'new_all_entities_aminer.p'


def wikititle_to_wikidata(title):
    """
    Converts a given Wikipedia article title to its corresponding Wikidata ID (Q123)
    """
    wiki_title = etitle.replace(' ', '_')
    qid = mapper.title_to_id(wiki_title)
    return qid


def wikidata_to_embedding(uri):
    """
    for a given URI in format <http://www.wikidata.org/entity/Q123> returns the embedding in biggraph
    """
    idx = biggraph_names.index(uri)
    return biggraph_vectors[idx]


def entities_to_docembeddings(data):
    """
    iterates over input data and summarizes each document into one vector
    """
    doc_embeddings = dict()
    for key in data:
        embeddings = []
        aminer_entities_wikidata[key] = []
        for (_, etitle,_) in list(set(data[key])):
            wikidata_uri = f"<http://www.wikidata.org/entity/{wikititle_to_wikidata(etitle)}>"
            if wikidata_uri in biggraph_names:
                embeddings.append(wikidata_to_embedding(wikidata_uri))
        
        doc_embeddings[key] = np.mean(embeddings, axis=0)

    return doc_embeddings


if __name__ == '__main__':
    data = pickle.load(open(data_path, 'rb'))
    emb_per_doc = entities_to_docembeddings(data)
    pickle.dump(emb_per_doc, open('aminer_entities_doc_embeddings.p', 'wb'))
