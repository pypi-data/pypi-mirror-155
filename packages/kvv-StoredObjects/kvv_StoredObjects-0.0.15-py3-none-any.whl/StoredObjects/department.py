import requests
from bs4 import BeautifulSoup
from .author import Author


class Department:

    def __init__(self, link=None):
        self.siteLink = link
        self.name = ""
        self.employees = []
        if link is not None:
            self.fillData()

    def addEmployee(self, name):
        empl = Author(name, self)
        self.employees.append(empl)

    def deleteEmployee(self, name):
        empl = self.searchEmployee(name)
        if empl is not None:
            self.employees.remove(empl)

    def fillData(self):
        r = requests.get(self.siteLink)
        soup = BeautifulSoup(r.text, features="html.parser")
        title = soup.find("h1")
        if title.text == "Ботанический сад": # не является кафедрой, другой интерфейс
            return

        self.name = title.text
        r = requests.get(self.siteLink + "prepods/")
        soup = BeautifulSoup(r.text, features="html.parser")
        table = soup.find("table")
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            name = cols[0].text
            author = Author(name, self)
            self.employees.append(author)

    def searchEmployees(self, name):
        names = []
        for empl in self.employees:
            if name.lower() in empl.name.lower():
                names.append(empl.name)
        return names

    def searchEmployee(self, name):
        empls = []
        for empl in self.employees:
            if name.lower() in empl.name.lower():
                empls.append(empl)
        if len(empls) != 1:
            return None
        return empls[0]

    def searchPublicationByDOI(self, doi):
        for empl in self.employees:
            publ = empl.searchPublicationByDOI(doi)
            if publ is not None:
                return publ
        return None

    def getPublications(self, fromDate, toDate):
        publs = []
        for empl in self.employees:
            for pub in empl.publications:
                publs.append(pub)
        self.mergePublications(publs)

        publs = []
        for empl in self.employees:
            for pub in empl.publications:
                if pub not in publs:
                    if fromDate <= pub.publishedDate <= toDate:
                        publs.append(pub)
        return publs

    def mergePublications(self, publications):
        for pub in publications:
            for pub2 in publications:
                if pub2 is pub:
                    continue
                if pub == pub2:
                    for au in pub.authors:
                        au.addPublication(pub2)
                    for au in pub2.authors:
                        au.addPublication(pub)
