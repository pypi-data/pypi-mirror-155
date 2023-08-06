import requests
from bs4 import BeautifulSoup
from .author import Author


class Department:

    def __init__(self, link):
        self.siteLink = link
        self.name = ""
        self.employees = []
        self.fillData()

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

    def getPublications(self):
        publs = set()
        for empl in self.employees:
            for pub in empl.publications:
                publs.add(pub)
        return list(publs)
        