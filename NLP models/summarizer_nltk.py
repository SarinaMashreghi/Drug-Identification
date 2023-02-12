import nltk
nltk.download('stopwords')
from nltk.cluster.util import cosine_distance
from nltk.corpus import stopwords
import numpy as np
import networkx as nx

def read_file(file_name):
    file = open(file_name, "r", encoding="utf8")
    filedata = file.readline()
    text = filedata.split(". ")
    # print(text)
    sentences = []
    for s in text:
        sentences.append(s.replace("[^a-zA-Z", " ").split(" "))
    sentences.pop()
    # print("from file: ", sentences)
    return sentences

def read_string(str_data):
    all_words = [w for w in str_data.split()]
    print(all_words)
    sentences = []

    i = 0

    while i<len(all_words):
        x = []
        a = True
        while a and i<len(all_words):
            x.append(all_words[i])
            if "." in all_words[i]:
                a = False
                x[-1] = x[-1][:-1]
                sentences.append(x)
            i += 1
    # print("from str: ", sentences)
    return sentences

def sentence_similarity(s1, s2, stopwords=None):
    if stopwords is None:
        stopwords = []

    s1 = [w.lower() for w in s1]
    s2 = [w.lower() for w in s2]
    all_words = list(set(s1+s2))

    v1 = [0] * len(all_words)
    v2 = [0] * len(all_words)

    for w in s1:
        if w in stopwords:
            continue
        v1[all_words.index(w)] += 1

    for w in s2:
        if w in stopwords:
            continue
        v2[all_words.index(w)] += 1

    return 1-cosine_distance(v1, v2)

def gen_sim_matrix(sentences, stopwords):
    sim_matrix = np.zeros((len(sentences), len(sentences)))

    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i == j:
                continue
            sim_matrix[i][j] = sentence_similarity(sentences[i], sentences[j], stopwords)

    return sim_matrix

def generate_file_summary(file_name, n_sent=5):
    stop_words = stopwords.words('english')
    summary = []
    sentences = read_file(file_name)
    sim_mat = gen_sim_matrix(sentences, stop_words)
    sim_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(sim_graph)
    ranked_sentences = sorted(((scores[i], s) for i,s in enumerate(sentences)), reverse=True)

    for i in range(n_sent):
        summary.append(" ".join(ranked_sentences[i][1]))

    return summary

def generate_string_summary(str_data, n_sent=5):
    stop_words = stopwords.words('english')
    summary = []
    sentences = read_string(str_data)
    sim_mat = gen_sim_matrix(sentences, stop_words)
    sim_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(sim_graph)
    ranked_sentences = sorted(((scores[i], s) for i,s in enumerate(sentences)), reverse=True)

    for i in range(n_sent):
        summary.append(" ".join(ranked_sentences[i][1]))

    return summary


print(generate_string_summary("The process is intuitively understandable. First step is tokenization, which transform sentence to tokens. Second is creating dictionary, which removes word duplication and make word set(which is called dictionary or vocabulary). Final step is counting occurrences of each words and make it Bag-of-Words model. As you can see, “likes” and “movies” show 2 as they appears two times in sample sentence.", 2))
print(generate_file_summary('test.txt', 2))










