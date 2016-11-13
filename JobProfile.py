from collections import Counter
from bs4 import BeautifulSoup
import urllib.request


class JobProfile():

    def __init__(self, url):
        self.job_content = self.extractJobDescript(url)
        self.unigram = self.tokenator(self.job_content)
        self.word_counter = Counter(self.unigram)
        self.vocab = set(self.job_content)

    def extractJobDescript(self, url):
        r = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(r)
        letters = soup.find_all("div", {"id": "content"})
        lobby = []
        for element in letters:
            lobby.append(element.get_text())
        return(lobby[0].strip().replace("\n", ""))

    def tokenator(self, some_string):
        return nltk.word_tokenize(some_string)

    def getWordProb(self, key):
        return self.word_counter[key]/len(self.job_content)*100

    def getMatchRate(self, candidate_vocab):
        prob = 0
        for word in candidate_vocab:
            prob += self.getWordProb(word)
        return(prob)
