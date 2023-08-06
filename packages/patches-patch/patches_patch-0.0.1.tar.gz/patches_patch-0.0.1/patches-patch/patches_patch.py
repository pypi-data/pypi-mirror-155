
class Patch:

    def __init__(self, specification):
        self.name = specification['name']
        self.version = specification['version']
        self.pstamp = specification['pstamp']
        self.release = specification['release']
        self.author = specification['author']
        self.category = specification['category']
        self.content = specification['content']
        self.promotion_level = specification['promotion_level']
        self.requires = specification['requires']
        self.obsoletes = specification['obsoletes']
        self.description = specification['description']
        self.info = specification['info']

    def __str__(self):
        return f"{self.name}-{self.version}"

    def __repr__(self):
        return f"Patch({{'name': '{self.name}', 'version': '{self.version}', 'pstamp': '{self.pstamp}', 'release': '{self.release}','author': '{self.author}', 'category': '{self.category}', 'content': {self.content}, 'promotion_level': '{self.promotion_level}', 'requires': {self.requires}, 'obsoletes': {self.obsoletes}, 'description': '{self.description}', 'info': {self.info}}})"

    def export(self):
        print(str(self.__dict__))
