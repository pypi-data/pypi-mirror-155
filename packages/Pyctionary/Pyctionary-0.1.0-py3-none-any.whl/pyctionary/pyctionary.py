import requests
from bs4 import BeautifulSoup as bs
import json

class Pyctionary:
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
    def language(self,text):
        """
        Parameters
        ----------
        text : String
            String input to find its language.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        payload={
            "text":text,
            "uiLanguage":"en",
            "etnologue":True
            }
        url="https://api.translatedlabs.com/language-identifier/identify"
        result = requests.post(url,json=payload)
        result=json.loads(result.text)
        dictionnary_result={}
        dictionnary_result["language"]=result["language"]
        dictionnary_result["Language-Code"]=result["code"]
        dictionnary_result["description"]="Dedicasse FAKIRI Ismail l3chra"
        return dictionnary_result
    def definition(self,word):
        """
        Parameters
        ----------
        word : String
            Word to define, (it needs to be 1 word).

        Returns
        -------
        definitions : dictionnary
            returns a dictionnary and type of word (Noun, Verb...) as key and definition as value.

        """
        definitions={}
        if len(word.split())>1:
            print("Error: A Term must be only a single word")
            return
        page = requests.get("http://wordnetweb.princeton.edu/perl/webwn?s="+str(word))
        soup = bs(page.content, "html.parser")
        h3= soup.find_all("h3")
        ul=soup.find_all("ul")
        for e,c in zip(h3,ul):
            li = c.find("li").text
            definitions[e.text]=li
        return definitions