import numpy as np
def preprocess(txt):
    txt=txt.lower()
    txt=txt.replace('.',' .')
    words = txt.split(' ')
    word_to_id={}
    id_to_word={}
    for word in words:
        if word not in word_to_id:
            new_id=len(word_to_id)
            word_to_id[word]=new_id
            id_to_word[new_id]=word #최초 등장 시 각 사전에 등록
    corpus=np.array([word_to_id[w] for w in words])

    return corpus, word_to_id, id_to_word

def create_co_matrix(corpus, vocab_size, window_size=1):
    corpus_size=len(corpus)
    co_matrix=np.zeros((vocab_size,vocab_size),dtype=np.int32)

    for idx, word_id in enumerate(corpus):
        for i in range(1, window_size+1):
            left_idx=idx-i
            right_idx=idx+i

            if left_idx>=0:
                left_word_id=corpus[left_idx]
                co_matrix[word_id,left_word_id]+=1

            if right_idx<corpus_size:
                right_word_id=corpus[right_idx]
                co_matrix[word_id,right_word_id]+=1
    return co_matrix

def cos_similarity(x,y,eps=1e-8):
    nx=x/(np.sqrt(np.sum(x**2))+eps)
    ny=y/(np.sqrt(np.sum(y**2))+eps)
    return np.dot(nx,ny)

def ppmi(C,verbose=False, eps=1e-8):
    M=np.zeros_like(C,dtype=np.float32)
    N=np.sum(C)
    S=np.sum(C,axis=0)
    total=C.shape[0]*C.shape[1]
    cnt=0

    for i in range(C.shape[0]):
        for j in range(C.shape[1]):
            pmi=np.log2(C[i,j]*N/((S[j]*S[i])+eps))
            M[i,j]=max(0,pmi)

            if verbose:
                cnt+=1
                if cnt %(total//100)==0:
                    print('%.1f%% 완료' %(100*cnt/total))
    return M