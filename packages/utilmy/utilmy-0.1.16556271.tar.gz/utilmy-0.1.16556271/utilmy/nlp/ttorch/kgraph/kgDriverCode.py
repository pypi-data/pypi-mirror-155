import pandas as pd
from knowledge_graph2 import knowledge_grapher, NERExtractor, KGEmbedder

data = pd.read_csv('final_dataset_clean_v2 .tsv', delimiter='\t')
extractor = NERExtractor(data, 'pykeen_data', load_spacy=True)
data_kgf = extractor.extractTriples(-1)
extractor.prepare_data(data_kgf)

grapher = knowledge_grapher(data_kgf=data_kgf,embedding_dim=10, load_spacy=True)
grapher.buildGraph()
grapher.plot_graph('plots')

embedder = KGEmbedder('pykeen_data', grapher.graph, embedding_dim=10)
embedder.load_embeddings('none')
factory = embedder.save_embeddings()
