# -*- coding: utf-8 -*-
""" Top-k retrieval vectors for Rec
Doc::



"""
import os, glob, sys, math, time, json, functools, random, yaml, gc, copy, pandas as pd, numpy as np
import datetime
from pathlib import Path; from collections import defaultdict, OrderedDict ;
from typing import List, Optional, Tuple, Union  ; from numpy import ndarray
from box import Box

import warnings ;warnings.filterwarnings("ignore")
from warnings import simplefilter  ; simplefilter(action='ignore', category=FutureWarning)
with warnings.catch_warnings():
    import matplotlib.pyplot as plt
    import mpld3
    from scipy.cluster.hierarchy import ward, dendrogram
    import sklearn

    from sklearn.cluster import KMeans
    from sklearn.manifold import MDS
    from sklearn.metrics.pairwise import cosine_similarity


from utilmy import pd_read_file, os_makedirs, pd_to_file, glob_glob


#### Optional imports
try :
    import faiss
    import diskcache as dc
except: pass



#############################################################################################
from utilmy import log, log2, os_module_name
MNAME = os_module_name(__file__)

def help():
    """function help        """
    from utilmy import help_create
    print( help_create(__file__) )



#############################################################################################
def test_all() -> None:
    """ python  $utilmy/deeplearning/util_embedding.py test_all         """
    log(MNAME)
    test1()


def test1() -> None:
    """function test1     
    """
    dirtmp ="./ztmp/"

    dd = test_create_fake_df(dirout= dirtmp)
    log(dd)



def test_create_fake_df(dirout="./ztmp/"):
    """ Creates a fake embeddingdataframe
    """
    res  =Box({})
    n = 30

    # Create fake user ids
    word_list = [ 'a' + str(i) for i in range(n)]

    emb_list = []
    for i in range(n):
        emb_list.append( ','.join([str(x) for x in np.random.random( (0,1,120)) ])  )


    ####
    df = pd.DataFrame()
    df['id']   = word_list
    df['emb']  = emb_list
    res.df = df


    #### export on disk
    res.dir_parquet =  dirout +"/emb_parquet/db_emb.parquet"
    pd_to_file(df, res.dir_parquet , show=1)

    #### Write on text:
    res.dir_text = dirout + "/word2vec_export.vec"
    log( res.dir_text )
    with open(res.dir_text, mode='w') as fp:
        fp.write("word2vec export format\n")

        for i,x in df.iterrows():
          emb  = x['emb'].replace(",", "")
          fp.write(  f"{x['id']}  {emb}\n")


    return res





########################################################################################################
######## Top-K retrieval ###############################################################################
def sim_scores_pairwise(embs:np.ndarray, word_list:list, is_symmetric=False):
    """ Pairwise Cosinus Sim scores
    Example:
        Doc::

           embs   = np.random.random((10,200))
           idlist = [str(i) for i in range(0,10)]
           df = sim_scores_fast(embs:np, idlist, is_symmetric=False)
           df[[ 'id1', 'id2', 'sim_score'  ]]

    """
    from sklearn.metrics.pairwise import cosine_similarity    
    dfsim = []
    for i in  range(0, len(word_list) - 1) :
        vi = embs[i,:]
        normi = np.sqrt(np.dot(vi,vi))
        for j in range(i+1, len(word_list)) :
            # simij = cosine_similarity( embs[i,:].reshape(1, -1) , embs[j,:].reshape(1, -1)     )
            vj = embs[j,:]
            normj = np.sqrt(np.dot(vj, vj))
            simij = np.dot( vi ,  vj  ) / (normi * normj)
            dfsim.append([ word_list[i], word_list[j],  simij   ])
            # dfsim2.append([ nwords[i], nwords[j],  simij[0][0]  ])
    
    dfsim  = pd.DataFrame(dfsim, columns= ['id1', 'id2', 'sim_score' ] )   

    if is_symmetric:
        ### Add symmetric part      
        dfsim3 = copy.deepcopy(dfsim)
        dfsim3.columns = ['id2', 'id1', 'sim_score' ] 
        dfsim          = pd.concat(( dfsim, dfsim3 ))
    return dfsim



    


def topk_nearest_vector(x0:np.ndarray, vector_list:list, topk=3, engine='faiss', engine_pars:dict=None) :
    """ Retrieve top k nearest vectors using FAISS, raw retrievail
    """
    if 'faiss' in engine :
        # cc = engine_pars
        import faiss  
        index = faiss.index_factory(x0.shape[1], 'Flat')
        index.add(vector_list)
        dist, indice = index.search(x0, topk)
        return dist, indice



def topk_calc( diremb="", dirout="", topk=100,  idlist=None, nexample=10, emb_dim=200, tag=None, debug=True):
    """ Get Topk vector per each element vector of dirin.
    Example:
        Doc::

           Return  pd.DataFrame( columns=[  'id', 'emb', 'topk', 'dist'  ] )
             id : id of the emb
             emb : [342,325345,343]   X0 embdding
             topk:  2,5,6,5,6
             distL 0,3423.32424.,

    
           python $utilmy/deeplearning/util_embedding.py  topk_calc   --diremb     --dirout
    

    """
    from utilmy import pd_read_file

    ##### Load emb data  ###############################################
    flist    = glob_glob(diremb)
    df       = pd_read_file(  flist , n_pool=10 )
    df.index = np.arange(0, len(df))
    log(df)

    assert len(df[['id', 'emb' ]]) > 0


    ##### Element X0 ####################################################
    vectors = np_str_to_array(df['emb'].values,  mdim= emb_dim)
    del df ; gc.collect()

    llids = idlist
    if idlist is None :    
       llids = df['id'].values    
       llids = llids[:nexample]

    dfr = [] 
    for ii in range(0, len(llids)) :        
        x0      = vectors[ii]
        xname   = llids[ii]
        log(xname)
        x0         = x0.reshape(1, -1).astype('float32')  
        dist, rank = topk_nearest_vector(x0, vectors, topk= topk) 
        
        ss_rankid = np_array_to_str( llids[ rank[0] ] )
        ss_distid = np_array_to_str( dist[0]  )

        dfr.append([  xname, x0,  ss_rankid,  ss_distid  ])   

    dfr = pd.DataFrame( dfr, columns=[  'id', 'emb', 'topk', 'dist'  ] )
    pd_read_file( dfr, dirout + f"/topk_{tag}.parquet"  )




########################################################################################################
######## Top-K retrieval Faiss #########################################################################
def faiss_create_index(df_or_path=None, col='emb', dirout=None,  db_type = "IVF4096,Flat", nfile=1000, emb_dim=200,
                       nrows=-1):
    """ 1 billion size vector Index creation
    Docs::

          python util_embedding.py   faiss_create_index    --df_or_path myemb/
    """
    import faiss

    
    dirout    =  "/".join( os.path.dirname(df_or_path).split("/")[:-1]) + "/faiss/" if dirout is None else dirout

    os.makedirs(dirout, exist_ok=True) ; 
    log( 'dirout', dirout)    
    log('dirin',   df_or_path)  ; time.sleep(10)
    
    if isinstance(df_or_path, str) :      
       flist = sorted(glob.glob(df_or_path  ))[:nfile] 
       log('Loading', df_or_path) 
       df = pd_read_file(flist, n_pool=20, verbose=False)
    else :
       df = df_or_path

    df  = df.iloc[:nrows, :]   if nrows>0  else df
    log(df)
        
    tag = f"_" + str(len(df))    
    df  = df.sort_values('id')    
    df[ 'idx' ] = np.arange(0,len(df))
    pd_to_file( df[[ 'idx', 'id' ]], 
                dirout + f"/map_idx{tag}.parquet", show=1)   #### Keeping maping faiss idx, item_tag
    

    log("#### Convert parquet to numpy   ", dirout)
    X  = np.zeros((len(df), emb_dim  ), dtype=np.float32 )    
    vv = df[col].values
    del df; gc.collect()
    for i, r in enumerate(vv) :
        try :
          vi      = [ float(v) for v in r.split(',')]        
          X[i, :] = vi
        except Exception as e:
          log(i, e)
            
    log("#### Preprocess X")
    faiss.normalize_L2(X)  ### Inplace L2 normalization
    log( X ) 
    
    nt = min(len(X), int(max(400000, len(X) *0.075 )) )
    Xt = X[ np.random.randint(len(X), size=nt),:]
    log('Nsample training', nt)

    ####################################################    
    D = emb_dim   ### actual  embedding size
    N = len(X)   #1000000

    # Param of PQ for 1 billion
    M      = 40 # 16  ###  200 / 5 = 40  The number of sub-vector. Typically this is 8, 16, 32, etc.
    nbits  = 8        ### bits per sub-vector. This is typically 8, so that each sub-vec is encoded by 1 byte    
    nlist  = 6000     ###  # Param of IVF,  Number of cells (space partition). Typical value is sqrt(N)    
    hnsw_m = 32       ###  # Param of HNSW Number of neighbors for HNSW. This is typically 32

    # Setup  distance -> similarity in uncompressed space is  dis = 2 - 2 * sim, https://github.com/facebookresearch/faiss/issues/632
    quantizer = faiss.IndexHNSWFlat(D, hnsw_m)
    index     = faiss.IndexIVFPQ(quantizer, D, nlist, M, nbits)
    
    log('###### Train indexer')
    index.train(Xt)      # Train
    
    log('###### Add vectors')
    index.add(X)        # Add

    log('###### Test values ')
    index.nprobe = 8  # Runtime param. The number of cells that are visited for search.
    dists, ids = index.search(x=X[:3], k=4 )  ## top4
    log(dists, ids)
    
    log("##### Save Index    ")
    dirout2 = dirout + f"/faiss_trained{tag}.index" 
    log( dirout2 )
    faiss.write_index(index, dirout2 )
    return dirout2
        


def faiss_load_index(faiss_index_path=""):
    return None



def faiss_topk_calc(df=None, root=None, colid='id', colemb='emb',
                    faiss_index:str="", topk=200, npool=1, nrows=10**7, nfile=1000,
                    return_simscore=False

                    ) :
   """#
   Doc::

       df : path or DF


       return on disk
         id  :     word id
         id_list : topk from word id
         dist_list, sim_list:



       https://github.com/facebookresearch/faiss/issues/632
       dis = 2 - 2 * sim
  
   """
   # nfile  = 1000      ; nrows= 10**7
   # topk   = 500 
 
   if faiss_index is None : 
      faiss_index = ""

   log('Faiss Index: ', faiss_index)
   if isinstance(faiss_index, str) :
        faiss_path  = faiss_index
        faiss_index = faiss_load_index(db_path=faiss_index) 
   faiss_index.nprobe = 12  # Runtime param. The number of cells that are visited for search.
        
   ########################################################################
   if isinstance(df, list):    ### Multi processing part
        if len(df) < 1 : return 1
        flist = df[0]
        root     = os.path.abspath( os.path.dirname( flist[0] + "/../../") )  ### bug in multipro
        dirin    = root + "/df/"
        dir_out  = root + "/topk/"

   elif df is None : ## Default
        root    = "emb/emb/i_1000000000/"
        dirin   = root + "/df/*.parquet"        
        dir_out = root + "/topk/"
        flist = sorted(glob.glob(dirin))
                
   else : ### df == string path
        root    = os.path.abspath( os.path.dirname(df)  + "/../") 
        log(root)
        dirin   = root + "/df/*.parquet"
        dir_out = root + "/topk/"  
        flist   = sorted(glob.glob(dirin))
        
   log('dir_in',  dirin)
   log('dir_out', dir_out) ; time.sleep(2)     
   flist = flist[:nfile]
   if len(flist) < 1: return 1 
   log('Nfile', len(flist), flist )


   ####### Parallel Mode ################################################
   if npool > 1 and len(flist) > npool :
        log('Parallel mode')
        from utilmy.parallel  import multiproc_run, multiproc_tochunk
        ll_list = multiproc_tochunk(flist, npool = npool)
        multiproc_run(faiss_topk_calc,  ll_list,  npool, verbose=True, start_delay= 5,
                      input_fixed = { 'faiss_index': faiss_path }, )      
        return 1


   ####### Single Mode #################################################
   dirmap       = faiss_path.replace("faiss_trained", "map_idx").replace(".index", '.parquet')  
   map_idx_dict = db_load_dict(dirmap,  colkey = 'idx', colval = 'item_tag_vran' )

   chunk  = 200000       
   kk     = 0
   os.makedirs(dir_out, exist_ok=True)    
   dirout2 = dir_out 
   flist = [ t for t in flist if len(t)> 8 ]
   log('\n\nN Files', len(flist), str(flist)[-100:]  ) 
   for fi in flist :
       if os.path.isfile( dir_out + "/" + fi.split("/")[-1] ) : continue
       # nrows= 5000
       df = pd_read_file( fi, n_pool=1  ) 
       df = df.iloc[:nrows, :]
       log(fi, df.shape)
       df = df.sort_values('id') 

       dfall  = pd.DataFrame()   ;    nchunk = int(len(df) // chunk)    
       for i in range(0, nchunk+1):
           if i*chunk >= len(df) : break         
           i2 = i+1 if i < nchunk else 3*(i+1)
        
           x0 = np_str_to_array( df[colemb].iloc[ i*chunk:(i2*chunk)].values   , l2_norm=True ) 
           log('X topk') 
           topk_dist, topk_idx = faiss_index.search(x0, topk)            
           log('X', topk_idx.shape) 
                
           dfi                   = df.iloc[i*chunk:(i2*chunk), :][[ colid ]]
           dfi[ f'{colid}_list'] = np_matrix_to_str2( topk_idx, map_idx_dict)  ### to actual id
           # dfi[ f'dist_list']  = np_matrix_to_str( topk_dist )
           if return_simscore: dfi[ f'sim_list']     = np_matrix_to_str_sim( topk_dist )
        
           dfall = pd.concat((dfall, dfi))

       dirout2 = dir_out + "/" + fi.split("/")[-1]      
       # log(dfall['id_list'])
       pd_to_file(dfall, dirout2, show=1)  
       kk    = kk + 1
       if kk == 1 : dfall.iloc[:100,:].to_csv( dirout2.replace(".parquet", ".csv")  , sep="\t" )
             
   log('All finished')    
   return os.path.dirname( dirout2 )



###############################################################################################################

#########################################################################################################
############## Loader of embeddings #####################################################################
def embedding_torchtensor_to_parquet(tensor_list,
                                     id_list:list, label_list, dirout=None, tag="",  nmax=10 ** 8 ):
    """ List ofTorch tensor to embedding stored in parquet
    Doc::

        yemb = model.encode(X)
        id_list = np.arange(0, len(yemb))
        ylabel = ytrue
        embedding_torchtensor_to_parquet(tensor_list= yemb,
                                     id_list=id_list, label_list=ylabel,
                                     dirout="./ztmp/", tag="v01"  )


    """
    n          =  len(tensor_list)
    id_list    = np.arange(0, n) if id_list is None else id_list
    label_list = [0]*n if label_list is None else id_list

    assert len(id_list) == len(tensor_list)

    df = []
    for idi, vecti, labeli in zip(id_list,tensor_list, label_list):
        ss = np_array_to_str(vecti.tonumpy())
        df.append([ idi, ss, labeli    ])

    df = pd.DataFrame(df, columns= ['id', 'emb', 'label'])


    if dirout is not None :
      log(dirout) ; os_makedirs(dirout)  ; time.sleep(4)
      dirout2 = dirout + f"/df_emb_{tag}.parquet"
      pd_to_file(df, dirout2, show=1 )
    return df


def embedding_rawtext_to_parquet(dirin=None, dirout=None, skip=0, nmax=10 ** 8,
                                 is_linevalid_fun=None):   ##   python emb.py   embedding_to_parquet  &
    #### FastText/ Word2Vec to parquet files    9808032 for purhase
    log(dirout) ; os_makedirs(dirout)  ; time.sleep(4)

    if is_linevalid_fun is None : #### Validate line
        def is_linevalid_fun(w):
            return len(w)> 5  ### not too small tag

    i = 0; kk=-1; words =[]; embs= []; ntot=0
    with open(dirin, mode='r') as fp:
        while i < nmax+1  :
            i  = i + 1
            ss = fp.readline()
            if not ss  : break
            if i < skip: continue

            ss = ss.strip().split(" ")
            if not is_linevalid_fun(ss[0]): continue

            words.append(ss[0])
            embs.append( ",".join(ss[1:]) )

            if i % 200000 == 0 :
              kk = kk + 1
              df = pd.DataFrame({ 'id' : words, 'emb' : embs }  )
              log(df.shape, ntot)
              if i < 2: log(df)
              pd_to_file(df, dirout + f"/df_emb_{kk}.parquet", show=0)
              ntot += len(df)
              words, embs = [], []

    kk      = kk + 1
    df      = pd.DataFrame({ 'id' : words, 'emb' : embs }  )
    ntot   += len(df)
    dirout2 = dirout + f"/df_emb_{kk}.parquet"
    pd_to_file(df, dirout2, show=1 )
    log('ntotal', ntot, dirout2 )
    return os.path.dirname(dirout2)



def embedding_load_parquet(dirin="df.parquet",  colid= 'id', col_embed= 'emb',  nmax= 500):
    """  Required columns : id, emb (string , separated)

    """
    log('loading', dirin)
    flist = list( glob.glob(dirin) )

    df  = pd_read_file( flist, npool= max(1, int( len(flist) / 4) ) )
    nmax    = nmax if nmax > 0 else  len(df)   ### 5000
    df  = df.iloc[:nmax, :]
    df  = df.rename(columns={ col_embed: 'emb'})

    df  = df[ df['emb'].apply( lambda x: len(x)> 10  ) ]  ### Filter small vector
    log(df.head(5).T, df.columns, df.shape)
    log(df, df.dtypes)


    ###########################################################################
    ###### Split embed numpy array, id_map list,  #############################
    embs    = np_str_to_array(df['emb'].values,  l2_norm=True,     mdim = 200)
    id_map  = { name: i for i,name in enumerate(df[colid].values) }
    log(",", str(embs)[:50], ",", str(id_map)[:50] )

    #####  Keep only label infos  ####
    del df['emb']
    return embs, id_map, df



def embedding_load_word2vec(dirin=None, skip=0, nmax=10 ** 8,
                                 is_linevalid_fun=None):
    """  Parse FastText/ Word2Vec to parquet files.
    Doc::

       dirin: .parquet files with cols:
       embs: 2D np.array, id_map: Dict, dflabel: pd.DataFrame


    """
    if is_linevalid_fun is None : #### Validate line
        def is_linevalid_fun(w):
            return len(w)> 5  ### not too small tag

    i = 0; kk=-1; words =[]; embs= []; ntot=0
    with open(dirin, mode='r') as fp:
        while i < nmax+1  :
            i  = i + 1
            ss = fp.readline()
            if not ss  : break
            if i < skip: continue

            ss = ss.strip().split(" ")
            if not is_linevalid_fun(ss[0]): continue

            words.append(ss[0])
            embs.append( ",".join(ss[1:]) )


    kk      = kk + 1
    df      = pd.DataFrame({ 'id' : words, 'emb' : embs }  )
    ntot   += len(df)


    embs   =  np_str_to_array( df['emb'].values  )  ### 2D numpy array
    id_map = { i : idi for i, idi in enumerate(df['id'].values)  }
    dflabel      = pd.DataFrame({ 'id' : words }  )
    dflabel['label1'] = 0

    return  embs, id_map, dflabel



def embedding_load_pickle(dirin=None, skip=0, nmax=10 ** 8,
                                 is_linevalid_fun=None):   ##   python emb.py   embedding_to_parquet  &
    """
       Load pickle from disk into embs, id_map, dflabel
    """
    import pickle

    embs = None
    flist =  glob_glob(dirin)
    for fi in flist :
        arr = pickle.load(fi)
        embs = np.concatenate((embs, arr)) if embs is not None else arr


    id_map  = {i: i for i in  range(0, len(embs))}
    dflabel = pd.DataFrame({'id': [] })
    return embs, id_map, dflabel




def embedding_extract_fromtransformer(model,Xinput:list):
    """ Transformder require Pooling layer to extract word level embedding.
    Doc::

        https://github.com/Riccorl/transformers-embedder
        import transformers_embedder as tre

        tokenizer = tre.Tokenizer("bert-base-cased")

        model = tre.TransformersEmbedder(
            "bert-base-cased", subword_pooling_strategy="sparse", layer_pooling_strategy="mean"
        )

        example = "This is a sample sentence"
        inputs = tokenizer(example, return_tensors=True)


        class TransformersEmbedder(torch.nn.Module):
                model: Union[str, tr.PreTrainedModel],
                subword_pooling_strategy: str = "sparse",
                layer_pooling_strategy: str = "last",
                output_layers: Tuple[int] = (-4, -3, -2, -1),
                fine_tune: bool = True,
                return_all: bool = True,
            )


    """
    import transformers_embedder as tre

    tokenizer = tre.Tokenizer("bert-base-cased")

    model = tre.TransformersEmbedder(
        "bert-base-cased", subword_pooling_strategy="sparse", layer_pooling_strategy="mean"
    )

    # X = "This is a sample sentence"
    X2 = tokenizer(Xinput, return_tensors=True)
    yout = model(X2)
    emb  = yout.word_embeddings.shape[1:-1]       # remove [CLS] and [SEP]
    # torch.Size([1, 5, 768])
    # len(example)
    return yout









if 'utils_vector':
    def db_load_dict(df, colkey='ranid', colval='item_tag', naval='0', colkey_type='str', colval_type='str', npool=5, nrows=900900900, verbose=True):
        ### load Pandas into dict
        if isinstance(df, str):
           dirin = df
           log('loading', dirin)
           flist = glob_glob( dirin , 1000)
           log(  colkey, colval )
           df    = pd_read_file(flist, cols=[ colkey, colval  ], nrows=nrows,  n_pool=npool, verbose=True)

        log( df.columns )
        df = df.drop_duplicates(colkey)
        df = df.fillna(naval)
        log(df.shape)

        df[colkey] = df[colkey].astype(colkey_type)
        df[colval] = df[colval].astype(colval_type)


        df = df.set_index(colkey)
        df = df[[ colval ]].to_dict()
        df = df[colval] ### dict
        if verbose: log('Dict Loaded', len(df), str(df)[:100])
        return df


    def np_array_to_str(vv, ):
        """ array/list into  "," delimited string """
        vv= np.array(vv, dtype='float32')
        vv= [ str(x) for x in vv]
        return ",".join(vv)


    def np_str_to_array(vv,  l2_norm=True,     mdim = 200):
        """ Convert list of string into numpy 2D Array
        Docs::
             
             np_str_to_array(vv=[ '3,4,5', '7,8,9'],  l2_norm=True,     mdim = 3)    

        """
        from sklearn import preprocessing
        import faiss
        X = np.zeros(( len(vv) , mdim  ), dtype='float32')
        for i, r in enumerate(vv) :
            try :
              vi      = [ float(v) for v in r.split(',')]
              X[i, :] = vi
            except Exception as e:
              log(i, e)

        if l2_norm:
            # preprocessing.normalize(X, norm='l2', copy=False)
            faiss.normalize_L2(X)  ### Inplace L2 normalization
            log("Normalized X")
        return X


    def np_matrix_to_str2(m, map_dict:dict):
        """ 2D numpy into list of string and apply map_dict.
        
        Doc::
            map_dict = { 4:'four', 3: 'three' }
            m= [[ 0,3,4  ], [2,4,5]]
            np_matrix_to_str2(m, map_dict)

        """
        res = []
        for v in m:
            ss = ""
            for xi in v:
                ss += str(map_dict.get(xi, "")) + ","
            res.append(ss[:-1])
        return res    


    def np_matrix_to_str(m):
        res = []
        for v in m:
            ss = ""
            for xi in v:
                ss += str(xi) + ","
            res.append(ss[:-1])
        return res            
                
    
    def np_matrix_to_str_sim(m):   ### Simcore = 1 - 0.5 * dist**2
        res = []
        for v in m:
            ss = ""
            for di in v:
                ss += str(1-0.5*di) + ","
            res.append(ss[:-1])
        return res   


    def os_unzip(dirin, dirout):
        # !/usr/bin/env python3
        import sys
        import zipfile
        with zipfile.ZipFile(dirin, 'r') as zip_ref:
            zip_ref.extractall(dirout)




if 'custom_code':
    def pd_add_onehot_encoding(dfref, img_dir, labels_col):
        """
           id, uri, cat1, cat2, .... , cat1_onehot

        """
        import glob
        fpaths = glob.glob(img_dir)
        fpaths = [fi for fi in fpaths if "." in fi.split("/")[-1]]
        log(str(fpaths)[:100])

        df = pd.DataFrame(fpaths, columns=['uri'])
        log(df.head(1).T)
        df['id'] = df['uri'].apply(lambda x: x.split("/")[-1].split(".")[0])
        df['id'] = df['id'].apply(lambda x: int(x))
        df = df.merge(dfref, on='id', how='left')

        # labels_col = [  'gender', 'masterCategory', 'subCategory', 'articleType' ]

        for ci in labels_col:
            dfi_1hot = pd.get_dummies(df, columns=[ci])  ### OneHot
            dfi_1hot = dfi_1hot[[t for t in dfi_1hot.columns if ci in t]]  ## keep only OneHot
            df[ci + "_onehot"] = dfi_1hot.apply(lambda x: ','.join([str(t) for t in x]), axis=1)
            #####  0,0,1,0 format   log(dfi_1hot)

        return df



    def topk_custom(topk=100, dirin=None, pattern="df_*", filter1=None):
        """  python prepro.py  topk    |& tee -a  /data/worpoch_261/topk/zzlog.py


        """
        from utilmy import pd_read_file
        import cv2

        filter1 = "all"    #### "article"

        dirout  = dirin + "/topk/"
        os.makedirs(dirout, exist_ok=True)
        log(dirin)

        #### Load emb data  ###############################################
        df        = pd_read_file(  dirin + f"/{pattern}.parquet", n_pool=10 )
        log(df)
        df['id1'] = df['id'].apply(lambda x : x.split(".")[0])


        #### Element X0 ######################################################
        colsx = [  'masterCategory', 'subCategory', 'articleType' ]  # 'gender', , 'baseColour' ]
        df0   = df.drop_duplicates( colsx )
        log('Reference images', df0)
        llids = list(df0.sample(frac=1.0)['id'].values)


        for idr1 in llids :
            log(idr1)
            #### Elements  ####################################################
            ll = [  (  idr1,  'all'     ),
                    # (  idr1,  'article' ),
                    (  idr1,  'color'   )
            ]


            for (idr, filter1) in ll :
                dfi     = df[ df['id'] == idr ]
                log(dfi)
                if len(dfi) < 1: continue
                x0      = np.array(dfi['pred_emb'].values[0])
                xname   = dfi['id'].values[0]
                log(xname)

                #### 'gender',  'masterCategory', 'subCategory',  'articleType',  'baseColour',
                g1 = dfi['gender'].values[0]
                g2 = dfi['masterCategory'].values[0]
                g3 = dfi['subCategory'].values[0]
                g4 = dfi['articleType'].values[0]
                g5 = dfi['baseColour'].values[0]
                log(g1, g2, g3, g4, g5)

                xname = f"{g1}_{g4}_{g5}_{xname}".replace("/", "-")

                if filter1 == 'article' :
                    df1 = df[ (df.articleType == g4) ]

                if filter1 == 'color' :
                    df1 = df[ (df.gender == g1) & (df.subCategory == g3) & (df.articleType == g4) & (df.baseColour == g5)  ]
                else :
                    df1 = copy.deepcopy(df)
                    #log(df)

                ##### Setup Faiss queey ########################################
                x0      = x0.reshape(1, -1).astype('float32')
                vectors = np.array( list(df1['pred_emb'].values) )
                log(x0.shape, vectors.shape)

                dist, rank = topk_nearest_vector(x0, vectors, topk= topk)
                # print(dist)
                df1              = df1.iloc[rank[0], :]
                df1['topk_dist'] = dist[0]
                df1['topk_rank'] = np.arange(0, len(df1))
                log( df1 )
                df1.to_csv( dirout + f"/topk_{xname}_{filter1}.csv"  )

                img_list = df1['id'].values
                log(str(img_list)[:30])

                log('### Writing images on disk  ###########################################')
                import diskcache as dc
                db_path = "/dev/shm/train_npz/small//img_tean_nobg_256_256-1000000.cache"
                cache   = dc.Cache(db_path)
                print('Nimages', len(cache) )

                dir_check = dirout + f"/{xname}_{filter1}/"
                os.makedirs(dir_check, exist_ok=True)
                for i, key in enumerate(img_list) :
                    if i > 15: break
                    img  = cache[key]
                    img  = img[:, :, ::-1]
                    key2 = key.split("/")[-1]
                    cv2.imwrite( dir_check + f"/{i}_{key2}"  , img)
                log( dir_check )


    
    

################################################################################################################




    
 
    
###############################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()



    
