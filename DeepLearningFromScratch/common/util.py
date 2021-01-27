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