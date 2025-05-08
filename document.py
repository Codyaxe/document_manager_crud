from abc import ABC, abstractmethod

class Document(ABC):

    saved_documents = []

    def __init__(self, title, author, text):
        self._title = title
        self._author = author
        self._text = text

    @property
    def title(self):
        return self._title
    
    @property
    def author(self):
        return self._author
    
    @property
    def text(self):
        return self._text

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def print(self):
        pass

    @abstractmethod
    def share(self):
        pass

    def access(self):
        pass

class PDF(Document):

    def save(self):
        pass

    def print(self):
        pass

    def share(self):
        pass

class Word(Document):

    def save(self):
        pass

    def print(self):
        pass

    def share(self):
        pass

class JSON(Document):

    def save(self):
        pass

    def print(self):
        pass

    def share(self):
        pass

class Report(Document):

    def save(self):
        pass

    def print(self):
        pass

    def share(self):
        pass

class Letter(Document):

    def save(self):
        pass

    def print(self):
        pass

    def share(self):
        pass


class Email(Document):

    def save(self):
        Document.saved_documents.append(self)
        print("Your Email has been saved.")

    def print(self):
        pass

    def share(self):
        pass