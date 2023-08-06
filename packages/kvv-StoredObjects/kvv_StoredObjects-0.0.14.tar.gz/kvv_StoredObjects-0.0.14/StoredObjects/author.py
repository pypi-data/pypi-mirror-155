
class Author:

    def __init__(self, name, department=None):
        self.name = name
        self.engName = Author.translate(name)
        splitName = self.engName.split()
        self.orcidName = splitName[1] + " " + splitName[0]
        self.scopusName = (splitName[0], splitName[1][0] + '.' + splitName[2][0] + '.')
        self.crossrefName = []
        self.affiliations = []
        self.orcID = None
        self.researcherID = None
        self.publonsID = None
        self.department = department
        self.publications = []

    def __eq__(self, author):
        if (self.name == author.name): return True
        if (self.orcID and self.orcID == author.orcID): return True
        if (self.researcherID and self.researcherID == author.researcherID): return True
        if (self.publonsID and self.publonsID == author.publonsID): return True
        return False

    def searchPublicationByDOI(self, doi):
        for pub in self.publications:
            if pub.doi == doi:
                return pub
        return None

    def addPublication(self, publ):
        if not publ.searchAuthor(self):
            publ.authors.append(self)
        existing = self.searchPublicationByDOI(publ.doi)
        if existing is None:
            self.publications.append(publ)
        else:
            existing.enrich(publ)

    @staticmethod
    def translate(name):
        symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ",
                  (*list(u'abvgdee'), 'zh', *list(u'zijklmnoprstuf'), 'kh', 'z', 'ch', 'sh', 'sh', '',
                  'y', '', 'e', 'u','a', *list(u'ABVGDEE'), 'ZH', 
                  *list(u'ZIJKLMNOPRSTUF'), 'Kh', 'Z', 'Ch', 'Sh', 'Sh', '', 'Y', '', 'E', 'Yu', 'Ya', ' '))

        coding_dict = {source: dest for source, dest in zip(*symbols)}
        return ''.join([coding_dict[i] for i in name])
