"""

Separate in 3 parts  (classes)

  raw text --> NER extraction


  NER  --> KGraph training + embedding generation/


  KG Embedding Losses



Reason :
   make the code modular, easy to change when needed.
   make thing independant.



"""

import os, spacy, numpy as np, pandas as pd, networkx as ntx
import matplotlib.pyplot as plt
from tqdm import tqdm
from typing import Tuple
from spacy.matcher import Matcher
# from node2vec import Node2Vec as n2v

import torch

from pykeen.triples import TriplesFactory
from pykeen.pipeline import pipeline
from pykeen.models import TransE,ERModel
from torch.optim import Adam
from pykeen.training import SLCWATrainingLoop, LCWATrainingLoop
from pykeen.evaluation import RankBasedEvaluator
from pykeen.nn.representation import LabelBasedTransformerRepresentation

### pip install python-box
from box import Box
from utilmy import util_download as ud
from utilmy import log




#######################################################################################################
def test_all():
    #test1
    pass



def test1(path=""):
    """



    """
    runall()




#######################################################################################################
def runall(dirin='final_dataset_clean_v2 .tsv') :
    """
    Doc::

      cd utilmy/nlp/tttorch/kgraph/
      python knoweledge_graph.py runall --dirin  mydirdata/


    """
    df = pd.read_csv(dirin, delimiter='\t')
    grapher = knowledge_grapher(data_kgf=df,embedding_dim=10, load_spacy=True)

    data_kgf = grapher.extractTriples(-1)
    grapher.buildGraph(data_kgf)
    grapher.plot_graph()
    grapher.prepare_data(data_kgf)







#######################################################################################################
class knowledge_grapher():
    def __init__(self, data_kgf, embedding_dim:int=14, load_spacy:bool=False) -> None:
        self.data_kgf = data_kgf
        self.embedding_dim = embedding_dim

    def buildGraph(self, relation = None)->None:
        if relation:
            self.graph = ntx.from_pandas_edgelist(self.data_kgf[self.data_kgf['edge']==relation], "source", "target",
                         edge_attr=True, create_using=ntx.MultiDiGraph())
        else:
            self.graph = ntx.from_pandas_edgelist(self.data_kgf, "source", "target",
                         edge_attr=True, create_using=ntx.MultiDiGraph())

    def plot_graph(self, plotFolder)->None:
        plt.figure(figsize=(14, 14))
        posn = ntx.spring_layout(self.graph)
        ntx.draw(self.graph, with_labels=True, node_color='green', edge_cmap=plt.cm.Blues, pos = posn)
        plt.savefig(os.path.join(plotFolder,'graphPlot.jpg'))
        plt.close()

    def compute_centrality(self,)->None:
        self.centrality_dict = ntx.degree_centrality(self.graph)
        self.in_centrality_dict = ntx.in_degree_centrality(self.graph)
        self.out_centrality_dict = ntx.out_degree_centrality(self.graph)
        # self.eigenvector_centrality_dict = ntx.katz_centrality(self.graph)

    def load_data(self, path)->None:
        data_kgf = pd.read_csv(path, delimiter='\t')
        self.buildGraph(data_kgf)

    def get_centers(self, max_centers:int=5)->None:

        sorted_dict = sorted(self.centrality_dict.items(), key=lambda x: x[1])[::-1]
        in_sorted_dict = sorted(self.in_centrality_dict.items(), key=lambda x: x[1])[::-1]
        out_sorted_dict = sorted(self.out_centrality_dict.items(), key=lambda x: x[1])[::-1]

        degree_centers = sorted_dict[:max_centers]

        in_degree_centers = in_sorted_dict[:max_centers]
        out_degree_centers = out_sorted_dict[:max_centers]

        degree_adjacency = {u:self.graph[u] for u,_ in degree_centers}

        in_degree_adjacency = {u:self.graph[u] for u,_ in in_degree_centers}
        out_degree_adjacency = {u:self.graph[u] for u,_ in out_degree_centers}

        self.center_dict = {'degree':{'centers':degree_centers, 'adjacency': degree_adjacency},
                            'in_degree':{'centers':in_degree_centers, 'adjacency': in_degree_adjacency},
                            'out_degree':{'centers':out_degree_centers, 'adjacency':out_degree_adjacency},}

    def map_centers_anchors(self,embedding_df:pd.DataFrame, _type:str):

       self.embedding_df = embedding_df
       _aux = self.center_dict[_type]
       centers = _aux['centers']
       adjacency = _aux['adjacency']

       self.mean_anchor_dict = {}
       for center, _ in centers:
            center_embedding = self.embedding_df[str(center)]
            num_embeddings = len(list(adjacency[center].keys()))
            adjacency_embeddings = np.ndarray((num_embeddings, self.embedding_dim))
            for i, (node, adj_dict) in enumerate(adjacency[center].items()):
                adjacency_embeddings[i,:] = self.embedding_df[str(node)]
            self.mean_anchor_dict[center] = {'center': center_embedding.values, 'anchor':adjacency_embeddings.mean(axis = 0)}



class NERExtractor:

    def __init__(self, data:pd.DataFrame, embeddingFolder:str, load_spacy=True):

        if load_spacy:
            self.nlp = spacy.load("ro_core_news_sm")
        self.data = data
        self.embeddingFolder = embeddingFolder

    def extract_entities(self, sents)->pd.DataFrame:
        # chunk one
        enti_one = ""
        enti_two = ""
        dep_prev_token = "" # dependency tag of previous token in sentence
        txt_prev_token = "" # previous token in sentence
        prefix = ""
        modifier = ""
        for tokn in self.nlp(sents):
            # chunk two
            ## move to next token if token is punctuation
            if tokn.dep_ != "punct":
                #  check if token is compound word or not
                if tokn.dep_ == "compound":
                    prefix = tokn.text
                    # add the current word to it if the previous word is 'compound’
                    if dep_prev_token == "compound":
                        prefix = txt_prev_token + " "+ tokn.text
                # verify if token is modifier or not
                if tokn.dep_.endswith("mod") == True:
                    modifier = tokn.text
                    # add it to the current word if the previous word is 'compound'
                    if dep_prev_token == "compound":
                        modifier = txt_prev_token + " "+ tokn.text
                # chunk3
                if tokn.dep_.find("subj") == True:
                    enti_one = modifier +" "+ prefix + " "+ tokn.text
                    prefix = ""
                    modifier = ""
                    dep_prev_token = ""
                    txt_prev_token = ""
                # chunk4
                if tokn.dep_.find("obj") == True:
                    enti_two = modifier +" "+ prefix +" "+ tokn.text
                # chunk 5
                # update variable
                dep_prev_token = tokn.dep_
                txt_prev_token = tokn.text
        return [enti_one.strip(), enti_two.strip()]

    def obtain_relation(self,sent):
        doc = self.nlp(sent)
        matcher = Matcher(self.nlp.vocab)
        pattern = [{'DEP':'ROOT'},
                {'DEP':'prep','OP':"?"},
                {'DEP':'agent','OP':"?"},
                {'POS':'ADJ','OP':"?"}]
        matcher.add(key="matching_1", patterns = [pattern])
        matcher = matcher(doc)
        h = len(matcher) - 1
        try:
            assert matcher
            span = doc[matcher[h][1]:matcher[h][2]]
            return span.text
        except AssertionError:
            print('No match found for this entry!')
            return None

    def extractTriples(self, max_text:int) -> pd.DataFrame:

        pairs_of_entities = [self.extract_entities(i) for i in tqdm(self.data['paragraph'][:max_text])]
        relations = [self.obtain_relation(j) for j in tqdm(self.data['paragraph'][:max_text])]
        indexes = [x for x, z in enumerate(relations) if z is not None]
        relations = [x for x in relations if x is not None]

        # subject extraction
        source = [j[0] for j in pairs_of_entities]
        source = [source[i] for i in indexes]

        #object extraction
        target = [k[1] for k in pairs_of_entities]
        target = [target[i] for i in indexes]

        return pd.DataFrame({'source':source, 'target':target, 'edge':relations})

    def prepare_data(self, data_kgf:pd.DataFrame)->Tuple[pd.DataFrame]:

        SAMPLES = len(data_kgf.index)
        TRAIN_SPLIT = int(0.5 * SAMPLES)
        TEST_SPLIT = int(0.3 * SAMPLES)
        VALIDATION_SPLIT = int(0.2 * SAMPLES)

        train_indexes = np.random.randint(low = 0, high = len(data_kgf.index), size=TRAIN_SPLIT)
        test_indexes = np.random.randint(low = 0, high = len(data_kgf.index), size=TEST_SPLIT)
        validation_indexes = np.random.randint(low = 0, high = len(data_kgf.index), size=VALIDATION_SPLIT)

        train_df = data_kgf.iloc[train_indexes]
        test_df = data_kgf.iloc[test_indexes]
        val_df = data_kgf.iloc[validation_indexes]

        train_df.to_csv(os.path.join(self.embeddingFolder,'train_data.tsv'), sep="\t")
        test_df.to_csv(os.path.join(self.embeddingFolder,'test_data.tsv'), sep="\t")
        val_df.to_csv(os.path.join(self.embeddingFolder,'validation_data.tsv'), sep="\t")
        data_kgf.to_csv(os.path.join(self.embeddingFolder,'data_kgf.tsv'), sep="\t")

        return train_df, test_df, val_df




class KGEmbedder:
    def __init__(self, dataFolder, graph:ntx.MultiDiGraph, embedding_dim:int)->None:

        self.dataFolder = dataFolder
        self.graph = graph
        self.embedding_dim = embedding_dim

        train_path =os.path.join(dataFolder,'train_data.tsv')
        test_path =os.path.join(dataFolder,'test_data.tsv')
        val_path =os.path.join(dataFolder,'validation_data.tsv')
        data_path = os.path.join(dataFolder,'data_kgf.tsv')


        self.training = TriplesFactory.from_path(train_path)

        self.testing = TriplesFactory.from_path(test_path,
                                            entity_to_id=self.training.entity_to_id,
                                            relation_to_id=self.training.relation_to_id)

        self.validation = TriplesFactory.from_path(val_path,
                                            entity_to_id=self.training.entity_to_id,
                                            relation_to_id=self.training.relation_to_id)


    def set_up_embeddings(self,):
        # entity_representations = LabelBasedTransformerRepresentation.from_triples_factory(training)

        if os.path.exists(os.path.join(self.dataFolder, 'trained_model.pkl')):
            self.model = torch.load(os.path.join(self.dataFolder, 'trained_model.pkl'))
        else:
            self.model = ERModel(triples_factory=self.training,
                                 interaction='distmult',
                               # entity_representations=entity_representations
                               entity_representations_kwargs = dict(embedding_dim=self.embedding_dim, dropout=0.1),
                               relation_representations_kwargs = dict(embedding_dim=self.embedding_dim, dropout=0.1)
                               )

            self.optimizer = Adam(params=self.model.get_grad_params())

            self.training_loop = LCWATrainingLoop(
                model=self.model,
                triples_factory=self.training,
                optimizer=self.optimizer,
            )


    def compute_embeddings(self, path_to_embeddings, batch_size=1024):

        self.set_up_embeddings()
        losses = self.training_loop.train(
                                triples_factory=self.training,
                                num_epochs=10,
                                checkpoint_name='myCheckpoint.pt',
                                checkpoint_frequency=5,
                                batch_size=256,
                                )

        # Pick an evaluator
        evaluator = RankBasedEvaluator()
        # Get triples to test

        mapped_triples = self.testing.mapped_triples
        # Evaluate
        results = evaluator.evaluate(
            model=self.model,
            mapped_triples=mapped_triples,
            batch_size=batch_size,
            additional_filter_triples=[
                self.training.mapped_triples,
                self.validation.mapped_triples,
            ],
        )
        torch.save(self.model, os.path.join(self.dataFolder, 'trained_model.pkl'))
        return losses, results

    def load_embeddings(self, path_to_embeddings:str):

        if os.path.exists(path_to_embeddings):
           self.embedding_df = pd.read_csv(path_to_embeddings)
           return None, None
        else:
            return self.compute_embeddings(path_to_embeddings, batch_size=1024)

    def save_embeddings(self,):
        return self.training




if __name__=="__main__":
    import fire
    fire.Fire()
    ### python  
