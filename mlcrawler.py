import requests
from bs4 import BeautifulSoup
from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer
from lxml.html import fromstring

class Mutante:
    def __init__(self, url_finder):
        self.url_finder = url_finder
              
    def smartCrawler(self):
        url = self.url_finder
        re = requests.get(url)
        soup = BeautifulSoup(re.text, 'html.parser')
        needed = ['0','1','2','3','4','5','6','7','8','9',',']
        test_texts = [value 
                    for element in soup.find_all(class_=True) 
                    for value in element["class"]] 
        possible_texts = [
        "game_purchase_price",
        "price",
        "catalog-detail-price-value",
        "preco_desconto",
        "preco",
        "preco_desconto_avista-cm",
        'css-ovezyj',
        "currency-value",
        "best-price"
        ]
        negative_texts = [
        "container",
        "pop_up", 
        "menu", 
        "hr",
        "nav-menu-item"
        ]
        training_texts = possible_texts + negative_texts 
        training_labels = ["positive"] * len(negative_texts) + ["negative"] * len(possible_texts) 
        vectorizer = CountVectorizer() 
        vectorizer.fit(training_texts)
        training_vectors = vectorizer.transform(training_texts)
        testing_vectors = vectorizer.transform(test_texts) 
        classifier = tree.DecisionTreeClassifier()
        classifier.fit(training_vectors, training_labels)
        predictions = classifier.predict(testing_vectors)
        c = 0
        valuesInsideFoundit = []

        for i in predictions:
            if i == "positive":
                foundit = soup.find(class_=test_texts[c])      
                valuesInsideFoundit.append(foundit.text)       
            c+=1
        firstValuesInsideIt = []

        for k in filter(None,valuesInsideFoundit):
            cc = 0
            for y in list(k):
                if y in needed or y == "R" and list(k)[cc+1] == "$" or y == "$" and list(k)[cc-1] == "R":
                    firstValuesInsideIt.append(str(y).replace("\n", "").replace(' ', ''))
                else:
                    pass
                cc+=1
        ccc = 0
        whatWeWant = ""
        indexOf = 0

        for b in firstValuesInsideIt:    
            if b == "R" and firstValuesInsideIt[ccc+1] == "$":        
                indexOf = firstValuesInsideIt.index(str(firstValuesInsideIt[ccc]))      
                break 
            ccc+=1
        lastFormatedValues = []
        cccc = 0
        for y in firstValuesInsideIt[indexOf:]:

            lastFormatedValues.append(y)
            try:
                if lastFormatedValues[cccc-2] == ",":
                    break
            except:
                pass
            cccc+=1
        ccccc = 0
        indexOf2 = 0
        for bb in lastFormatedValues:
            if lastFormatedValues[ccccc] == "R" and lastFormatedValues[ccccc+1] == "$" and lastFormatedValues[ccccc+2] in needed: 
                indexOf2 = lastFormatedValues.index(str(lastFormatedValues[ccccc]))
            ccccc+=1
        for z in lastFormatedValues[indexOf2-8:]:  
            whatWeWant = whatWeWant + z
        treecontent = fromstring(re.content)
        productName = treecontent.findtext('.//title')


        return productName, whatWeWant
if __name__ == '__main__':
    jurest = Mutante('ooooo')
