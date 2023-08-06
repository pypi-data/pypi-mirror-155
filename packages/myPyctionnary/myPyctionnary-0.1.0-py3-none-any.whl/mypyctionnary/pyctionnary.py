import requests
from bs4 import BeautifulSoup as bs

class Pyctionnary:
    """
    Instanciate Pictionnary class
    """
    def __init__(self, *args):
        try:
            if isinstance(args[0], list):
                self.args = args[0]
            else:
                self.args = args
        except:
            self.args = args

    def synonyms(self,list_words,max_synonyms=None):
        """
        Parameters
        ----------
        list_words : List
            synonym function takes a list of words you want to find synonyms of as input
        max_synonyms: int
            Maximum number of synonms for each word. Default None
        Returns
        -------
        dictio : dictionnary
            It outputs a dictionnary, Key is the word and value list of synonyms.

        """
        dictio={}
        for word in list_words:
            URL = "https://www.synonym.com/synonyms/"+word#website with the word to search
            page = requests.get(URL)#request website HTML
            soup = bs(page.content, "html.parser")#parse html with beautifulsoup
            result =soup.find_all("ul", class_="section-list")#find the list of synonmys
            result = result[0]
            if max_synonyms!=None:
                li = result.find_all("li")[0:max_synonyms]
            else:
                li = result.find_all("li")
            synonym=[]
            for a in li:
                synonym.append(a.text)
            dictio[word]=synonym
        return dictio