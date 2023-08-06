import requests
from bs4 import BeautifulSoup
import pickle
from .department import Department

class University:
    _dataFile = "univer_save.pickle"
    _univer = None


    def __init__(self, canSearchMstu):
        self.canSearchMstu = canSearchMstu
        self.departments = []
        self.loadData()
        self.saveData()

    @staticmethod
    def getUniversity(canSearchMstu = False):
        if University._univer is None:
            University._univer = University(canSearchMstu)
        return University._univer

    def loadData(self):
        try:
            with open(University._dataFile, 'rb') as f:
                data = pickle.load(f)
                if data is not None:
                    self.departments = data.departments
        except:
            if self.canSearchMstu:
                print("No saved data or invalid, loading from scratch")
                self.fillDepartments()

    def saveData(self):
        with open(University._dataFile, 'wb') as f:
            pickle.dump(self, f)

    def fillDepartments(self):
        cafsLink = 'https://www.mstu.edu.ru/structure/kafs/'
        try:
            html = requests.get(cafsLink).text
            soup = BeautifulSoup(html, features="html.parser")
            lists = soup.findAll("ul", {"class": "anker"})
            # print(lists)
            links = []
            for ul in lists:
                hrefs = ul.findAll("a")
                for h in hrefs:
                    links.append(h['href'])
            print(links)
            baseUrl = 'https://www.mstu.edu.ru'
            for link in links:
                url = baseUrl + link
                self.addDepartment(url)
        except:
            print("Could not reach MSTU website")
            return

    def addDepartment(self, link):
        dep = Department(link)
        if dep.name != "":
            self.departments.append(dep)

    def addOfflineDepartment(self, dept):
        self.departments.append(dept)

    def getDepartment(self, name):
        for dep in self.departments:
            if name == dep.name:
                return dep
        return None

    def getDepartmentNames(self):
        names = []
        for dep in self.departments:
            names.append(dep.name)
        return names

    def searchEmployees(self, name):
        names = []
        for dep in self.departments:
            names.extend(dep.searchEmployees(name))
        return names

    def searchEmployee(self, fullName):
        empls = []
        for dep in self.departments:
            empl = dep.searchEmployee(fullName)
            if empl is not None:
                empls.append(empl)
        if len(empls) != 1:
            return None
        return empls[0]

    def searchPublicationByDOI(self, doi):
        for dep in self.departments:
            publ = dep.searchPublicationByDOI(doi)
            if publ is not None:
                return publ
        return None
    
