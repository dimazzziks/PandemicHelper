from bs4 import BeautifulSoup
import requests
html_doc = requests.get("https://www.rbc.ru/tags/?tag=%D0%BA%D0%BE%D1%80%D0%BE%D0%BD%D0%B0%D0%B2%D0%B8%D1%80%D1%83%D1%81")
soup = BeautifulSoup(html_doc.text, 'html.parser')
a = (soup.find_all("span", class_="search-item__title"))
RBCnews = []
RBClink = []
RBCImage = []
print(len(a))
for i in range(0,len(a)-1):
    RBCnews.append(a[i].contents[0])
    
a = (soup.find_all("a", class_="search-item__link"))
for i in range(0,len(a)-1):
    RBClink.append(a[i].attrs["href"])
for i in range(0,len(RBClink)-1):
    html_doc = requests.get(RBClink[i])
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    a = (soup.find_all("img", class_="article__main-image__image js-rbcslider-image"))
    if(len(a)!=0):
        RBCImage.append(a[0].attrs["src"])
    else:
        RBCImage.append("http://www.lanitnn.ru/wp-content/uploads/2017/12/95f048a4ad0654e8ec63a5a1192ea8b8-1.jpg")

import requests
html_doc = requests.get("https://lenta.ru/themes/2020/03/16/virus/")
soup = BeautifulSoup(html_doc.text, 'html.parser')
a = (soup.find_all("div", class_="titles"))
print(len(a))
LentaNews = []
LentaLinks = []
LentaImage = []

n = 0

if(len(a)>10):
    n=100
else:
    n=len(a)
    
for j in range(0,n):

    s1 = ([i.strip() for i in a[j].contents[0].text])
    s2 = ""
    for j1 in range(0,len(s1)):
        if(s1[j1]==""):
            s2+=" "
        else:
            s2+=s1[j1]
    LentaNews.append(s2)
    
    s="https://lenta.ru/"+(a[j].contents[0].contents[0].attrs["href"])
    LentaLinks.append(s)

for j in range(0,n):
    html_doc = requests.get(LentaLinks[j])
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    a = (soup.find_all("img", class_="g-picture"))
    LentaImage.append(a[0].attrs["src"])
    

import requests
html_doc = requests.get("https://www.forbes.ru/coronavirus")
soup = BeautifulSoup(html_doc.text, 'html.parser')
a = (soup.find_all("a", class_="card"))
print(len(a))
ForbesNews = []
ForbesLinks = []
ForbesImage = []

n = 0

if(len(a)>10):
    n=10
else:
    n=len(a)

for i in range(0,n-1):
    ForbesNews.append(a[i].contents[0].contents[0].contents[2].text[13:-11])
    s="https://www.forbes.ru"+a[i].attrs["href"]
    ForbesLinks.append(s)
    
for i in range(0,n-1):
    html_doc = requests.get(ForbesLinks[i])
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    a = (soup.find_all("img", class_="lazy-image"))
    if(len(a)>0):
        ForbesImage.append(a[0].attrs["data-src"])
    else:
        ForbesImage.append("https://www.ruckusmarketing.com/wp-content/uploads/2016/03/forbes-e1504186907594.jpg")

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate('D:/Key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

num = 30
ind = 0
for i in range(0,num-1):
    ind+=1
    
    matrix = tokenizer.texts_to_matrix([LentaNews[i]], mode='count')
    X = normalize(matrix)
    
    Prob =  model.predict(X)[0]
    
    doc_ref = db.collection(u'News').document(str(ind))
    doc_ref.set({
        u'corp': u'lenta',
        u'image': LentaImage[i],
        u'link': LentaLinks[i],
        u'title': LentaNews[i],
        u'prob': str(Prob[0])
    })
    ind+=1
    
    matrix = tokenizer.texts_to_matrix([RBCnews[i]], mode='count')
    X = normalize(matrix)
    
    Prob =  model.predict(X)[0]
    
    doc_ref = db.collection(u'News').document(str(ind))
    doc_ref.set({
        u'corp': u'rbc',
        u'image': RBCImage[i],
        u'link': RBClink[i],
        u'title': RBCnews[i],
        u'prob': str(Prob[0])
    })

for i in range(num,num*2-1):
    ind+=1
    
    matrix = tokenizer.texts_to_matrix([LentaNews[i]], mode='count')
    X = normalize(matrix)
    
    Prob =  model.predict(X)[0]
    
    doc_ref = db.collection(u'News').document(str(ind))
    doc_ref.set({
        u'corp': u'lenta',
        u'image': LentaImage[i],
        u'link': LentaLinks[i],
        u'title': LentaNews[i],
        u'prob': str(Prob[0])
    })
    
num = 10    
for i in range(0,num-1):
    ind+=1
    
    matrix = tokenizer.texts_to_matrix([ForbesNews[i]], mode='count')
    X = normalize(matrix)
    
    Prob =  model.predict(X)[0]
    
    doc_ref = db.collection(u'News').document(str(ind))
    doc_ref.set({
        u'corp': u'forbes',
        u'image': ForbesImage[i],
        u'link': ForbesLinks[i],
        u'title': ForbesNews[i],
        u'prob': str(Prob[0])
    })