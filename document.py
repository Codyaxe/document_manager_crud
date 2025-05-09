from abc import ABC, abstractmethod
import pickle
import textwrap
import datetime

class Document(ABC):

    saved_documents = []

    def __init__(self, title, author, text):
        self._title = title
        self._author = author
        self._text = textwrap.fill(text, width=100)

    @property
    def title(self):
        return self._title
    
    @property
    def author(self):
        return self._author
    
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, text):
        self._text = text

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
    """ We could create an actual implementation of PDF.
    Kaso, that would be tedious. We might have to use third
    party libraries."""

    def save(self):
        pass

    def print(self):
        pass

    def share(self):
        pass

class Word(Document):
    """ We could create an actual implementation of Word.
    Kaso, that would be tedious. We might have to use third
    party libraries."""

    def save(self):
        pass

    def print(self):
        pass

    def share(self):
        pass

class JSON(Document):
    """ We could create an actual implementation of JSON.
    We might have to use third party libraries."""
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

class Email(Document):

    def __init__(self, title, author, s_from, r_to, text, subject, recipient, cc = None):
        super().__init__(title, author, text)
        self._s_from = s_from
        self._r_to = r_to
        self._subject = subject
        self._recipient = recipient
        self._cc = cc
    

    def save(self):
        Document.saved_documents.append(self)
        print("Your Email has been saved.")

    def print(self):
        print(
            f"From: {self._s_from}\n"
            f"To: {self._r_to}\n"
            f"{'CC: ' + self._cc if self._cc else ''}\n"
            f"Subject: {self._subject}\n\n"
            f"{self.title.title()}\n\n"
            f"Dear {self._recipient},\n\n"
            f"{self.text}\n\n"
            f"{'Sincerely,':>100}\n"
            f"{self.author:>100}"
        )

    def share(self):
        pass


class Letter(Document):

    def __init__(self, title, author, s_address, r_address, text, subject, recipient):
        super().__init__(title, author, text)
        self._s_address = s_address
        self._date = datetime.date.today()
        self._r_address = r_address
        self._subject = subject
        self._recipient = recipient

    #We will use Pickle for this.
    def save(self):
        Document.saved_documents.append(self)
        print("Your Letter has been saved.")

    def print(self):
        print(
            f"{self._s_address}\n"
            f"{self._date}\n"
            f"{self._r_address}\n\n"
            f"{self.title.title()}\n"
            f"Subject: {self._subject}\n\n"
            f"Dear {self._recipient},\n\n"
            f"{self.text}\n\n"
            f"{'Yours truly,':>100}\n"
            f"{self.author:>100}"
        )

    def share(self):
        print("Your Letter has been shared.")

def create_document():
    pass

def share_document():
    pass

def edit_document():
    pass

def remove_document():
    pass

def read_document():
    pass
    
print()

email_one = Letter("Random Title", 
                  "Codyaxe", "Batangas City", "Alangilan",
                  "I am testing if I can make a long line " 
                  "that would violate the principles of programming " 
                  "making programmers have to scroll horizontally to "
                  "read the entire text", "A Message to a Classmate", "Aleckxa")
email_one.print()

email_one.save()

print(Document.saved_documents)
print("Test 1:")
Document.saved_documents[0].print()

""" For Implementing A Menu Option"""
if __name__ == "__main__":
    print("Welcome to the Document Manager. What do you want to do today?")
    while(True):
        choice = int(input("Press 0 to Read a Document, Press 1 to Create a Document, Press 2 to Share a Document, Press 3 to Edit a Document, Press 4 to Remove a Document, Press 5 to Exit the Program\n"))
        if choice == 0:
            read_document()
        elif choice == 1:
            create_document()
        elif choice == 2:
            share_document()
        elif choice == 3:
            edit_document()
        elif choice == 4:
            remove_document()
        elif choice == 5:
            break
        else:
            print("Invalid Choice!")
            continue