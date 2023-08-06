import datetime
from prettytable import PrettyTable


class Publication:
    defaultDate = datetime.date(1970, 1, 1)

    def __init__(self):
        self.title = ""
        self.description = ""
        self.authors = []
        self.type = ""
        self.issn = ""
        self.doi = ""
        self.scopusLink = ""
        self.eid = "" # scopus
        self.scopusId = ""
        self.pii = ""
        self.ut = ""  # wos
        self.wosLink = ""
        self.publishedDate = Publication.defaultDate
        self.indexedDate = Publication.defaultDate
        self.citations = 0
        self.publisher = ""
        self.containerTitle = []
        # self.pages = "" # для статьи в журнале
    
    def __eq__(self, other):
        if isinstance(other, Publication):
            return self.doi == other.doi
        return False

    def searchAuthor(self, author):
        for au in self.authors:
            if au == author:
                return au
        return None

    def enrich(self, anotherPubl):
        if anotherPubl is None:
            return
        if not self.title:
            self.title = anotherPubl.title
        if not self.description:
            self.description = anotherPubl.description
        if not self.issn:
            self.issn = anotherPubl.issn 
        if not self.doi:
            self.doi = anotherPubl.doi
        if not self.eid:
            self.eid = anotherPubl.eid
        if not self.scopusLink:
            self.scopusLink = anotherPubl.scopusLink
        if not self.scopusId:
            self.scopusId = anotherPubl.scopusId
        if not self.pii:
            self.pii = anotherPubl.pii
        if not self.ut:
            self.ut = anotherPubl.ut
        if not self.wosLink:
            self.wosLink = anotherPubl.wosLink
        if not self.citations:
            self.citations = anotherPubl.citations
        
        for au in anotherPubl.authors:
            same = False
            if au not in self.authors:
                self.authors.append(au)


    def __str__(self):
        table = PrettyTable()
        table.header = False
        table._max_width = {"Field 1": 20, "Field 2": 70}

        table.add_row(["Название", self.title[0]])
        table.add_row(["ISSN", self.issn])
        table.add_row(["DOI", self.doi])
        table.add_row(["EID", self.eid])
        table.add_row(["Scopus ID", self.scopusId])
        table.add_row(["PII", self.pii])
        table.add_row(["UT", self.ut])
        table.add_row(["Дата публикации", str(self.publishedDate)])
        table.add_row(["Дата индексирования", str(self.indexedDate)])
        table.add_row(["Число цитирований", self.citations])
        table.add_row(["Издатель", self.publisher])
        table.add_row(["Источник", self.containerTitle])
        return table.get_string()

