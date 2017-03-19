from urllib.request import FancyURLopener
import urllib.request
from bs4 import BeautifulSoup
#import simplejson as json
import numpy as np
import nltk 
from nltk.corpus import stopwords
from nltk.stem.porter import *
import re 
import json
import gensim.models.word2vec as w2v
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np

#hacks2vec = w2v.Word2Vec.load(os.path.join("trained", "hack2vec.w2v"))

stemmer = PorterStemmer()
class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
openurl = MyOpener().open

class ProjectData:
	#Constructor
    def __init__(self,url, name, hackathon, description, tags, likes):
        self.url = url
        self.name = name
        self.hackathon = hackathon
        self.description = description
        self.tags = tags
        self.likes = likes
	#Pretty Printer
    def __repr__(self):
        return '"name": "%s", "hackathon": "%s", "description": "%s", "tags": "%s", "likes": "%d"' % (self.name, self.hackathon, self.description, self.tags, self.likes)

def scrapeProject(url):
    soup = BeautifulSoup(openurl(url).read(),'lxml')
    data = []

    #name
    name2 = soup.find('h1',{'id':'app-title'}).text.strip()

    #hackathon
    hackathon2 = soup.find('div',{'class':'software-list-content'}).text.strip()

    #description
    text = soup.find(id="gallery").next_sibling.next_sibling
    paragraphs = text.find_all('p')
    description2 = ''
    for paragraph in paragraphs:
        description2 += name2 + " "
        description2 += paragraph.text.strip()

    #tags
    tags2 = []
    t = soup.find_all('span', {'class':'cp-tag'})
    for x in t:
        tags2.append(x.text.strip())


    #likes
    likes2 = soup.find('span', {'class':'like-counts'})
    likes2 = likes2.text.strip()
    a = likes2.split(' ')
    numberOfLikes2 = int(a[0])
    data.append(ProjectData(url,name2,hackathon2,description2,tags2,numberOfLikes2))
    json_data = json.dumps(data, indent=4, default=lambda o:o.__dict__)
    #print (repr(data))
    with open('myProject.json','w') as f:
        f.write(json_data)
    #json_data = json.loads(repr(data))
    print ('Success')
    '''json_data[keywords] = extractKeywords(to_words(json_data[description]))
    json_data[vector] = hackVector(json_data[description])
    print (json_data)
    return json_data'''

'''def to_words(content):
    letters_only = re.sub("[^a-zA-Z", " ", content)
    words = letters_only.lower().split()
    stopw = set(stopwords.words("english"))
    meaningful_words = [w for w in words if not w in stops]
    return (" ".join(meaningful_words))'''


stemmer = PorterStemmer()
def to_words(content):
    letters_only = re.sub("[^a-zA-Z]", " ", content)
    words = letters_only.lower().split()
    stops = set(stopwords.words("english"))
    meaningful_words = [w for w in words if not w in stops]
    array = []
    array.append(" ".join(meaningful_words))
    return array 

'''def text_preprocessing(description):
    description = re.sub("[^a-zA-Z.,]", " ", description)
    for project in range(len(description)):
        tokens = nltk.word_tokenize(description)
        singles = [stemmer.stem(token) for token in tokens]
        singles = ' '.join(singles)
        #description[project] = ''.join(singles)
    array = []
    array.append(singles)
    return array'''

def extractKeywords(description):
    #processed_text = text_preprocessing(description)
    #print ("Processed text: " + processed_text)
    vectorizer = TfidfVectorizer(analyzer='word')
    result = vectorizer.fit_transform(description)

    feature_array = np.array(vectorizer.get_feature_names())
    tfidf_sorting = np.argsort(result.toarray()).flatten()[::-1]

    n = 20

    top_keywords = feature_array[tfidf_sorting][:n]
    print (top_keywords)
    return top_keywords 



def hackVector(description):
    vector_sum = 0
    words = re.sub("[^a-zA-Z]", " ", description).lower().split()
    for word in words:
        vector_sum = vector_sum + hacks2vec[word]
        vector_sum = vector_sum.reshape(1, -1)
        normalised_vector_sum = sklearn.preprocessing.normalize(vector_sum)
        return normalised_vector_sum

scrapeProject('https://devpost.com/software/spacetrip')


dataframe = pd.read_json("myProject.json", encoding='utf-8')
dataframe['project_vector'] = hackVector(dataframe['description'][0])
dataframe['keywords'] = extractKeywords(dataframe['description'][0])

dataframe.head()