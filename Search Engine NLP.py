
import re,string,requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer


def retrieve_docs_and_clean():
    r = requests.get('https://bola.kompas.com/')
    
    soup = BeautifulSoup(r.content, 'html.parser')

    link = []
    for i in soup.find('div', {'class':'most__wrap'}).find_all('a'):
        i['href'] = i['href'] + '?page=all'
        link.append(i['href'])
    
    print(f'Number of links is ({len(link)})')
    print(f'second link is \n')
    print(link[1])
    print('===============================')
    documents = []
    for i in link:
        r = requests.get(i)
        soup = BeautifulSoup(r.content, 'html.parser')

        sen = []
        for i in soup.find('div', {'class':'read__content'}).find_all('p'):
            sen.append(i.text)
        print(f'number of sentences is {len(sen)} and first sentence is ({sen[0]})')
        documents.append(' '.join(sen))
    print('===============================')
    documents_clean = []
    for d in documents:
        document_test = re.sub(r'[^\x00-\x7F]+', ' ', d)
        document_test = re.sub(r'@\w+', '', document_test)
        document_test = document_test.lower()
        document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)
        document_test = re.sub(r'[0-9]', '', document_test)
        document_test = re.sub(r'\s{2,}', ' ', document_test)
        documents_clean.append(document_test)

    print(documents_clean)
    return documents_clean


def get_similar_articles(q, df):
    print("query:", q)
    print("Article with the highest cosine similarity value: ")
    q = [q]
    q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0],)
    print(f'QVec shape is ({q_vec.shape})')
    sim = {}
    for i in range(10):
        sim[i] = np.dot(df.loc[:, i].values, q_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)
  
    print(sim)
    sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)

    for k, v in sim_sorted:
        if v != 0.0:
            print("Similarity Value:", v)
            print(docs[k])
            print()
            
            
            
            
docs = retrieve_docs_and_clean()           
            
            

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(docs)
X.shape



df = pd.DataFrame(X.T.toarray(), index=vectorizer.get_feature_names())
print(df.shape)
df.head(20)

df.tail(20)

q = 'windy'
get_similar_articles(q, df)



q = 'adalah'
get_similar_articles(q, df)



            