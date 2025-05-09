from abc import ABC, abstractmethod
import os
import pickle
import textwrap
import datetime
import keyboard
import uuid
import time

CLEAR = "\033[K"

class Document(ABC):

    saved_documents = []

    def __init__(self, title= None, author= None, text= ""):
        self._title = title
        self._author = author
        self._text = textwrap.fill(text, width=100)
        self._id = str(uuid.uuid4())

    def __eq__(self, other):
        if not isinstance(other, Document):
            return False
        return self._id == other._id  

    @property
    def title(self):
        return self._title
    
    @property
    def author(self):
        return self._author
    
    @property
    def text(self):
        return self._text

    @title.setter
    def title(self, title):
        self._title = title

    @author.setter
    def author(self, author):
        self._author = author

    @text.setter
    def text(self, text):
        self._text = text
        
    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def modify(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def print(self):
        pass

    @abstractmethod
    def share(self):
        pass

class SlideShow(Document):

    def __init__(self, title = None, author = None, text = "", size = None):
        super().__init__(title, author, text)
        self._size = size
        if size:
            self._slides = ["" for slide in range(size)]

    @property
    def slides(self):
        return self._slides
    
    @slides.setter
    def slides(self, content):
        if len(content) != self._size:
            raise ValueError(f"Content must be a list of {self._size} slides.")
        for i in range(self._size):
            if content[i] is not None:
                self._slides[i] = content[i]

    def create(self):
        self.title = input("Enter the spreadsheet title: ")
        self.author = input("Enter the spreadsheet author: ")
        self.text = input("Enter the spreadsheet description: ")
        while True:
            self._size = input("Enter the number of slides in the slideshow: ")
            if self._size.isdigit():
                self._size = int(self._size)
                self._slides = ["" for slide in range(self._size)]
                break
            else:
                print("Please enter a valid number.")
        while True:
            choice = input("Do you want to modify the slides now? Y/N")
            if choice == "Y" or choice == "y":
                self.modify(onlySlides = True)
                break
            elif choice == "N" or choice == "n":
                break
            else:
                print("Please enter a valid input")

    def modify(self, onlySlides = False):
        if not onlySlides:
            options = {
                1: "title",
                2: "author",
                3: "text",
            }
            print("Which fields do you want to modify?")
            print("Press 1 to Modify Title")
            print("Press 2 to Modify Author")
            print("Press 3 to Modify Description")
            print("Press 4 to Modify Slides")
            print("Press 5 to Exit")
            while True:
                try:
                    choice = int(input("Choose: "))
                    if choice == 4:
                        break
                    if choice == 5:
                        return
                    if choice in options:
                        attr_name = options[choice]
                        new_value = input(f"Enter the new {attr_name}: ")
                        setattr(self, attr_name, new_value)
                        break
                    else:
                        print("Invalid choice.")
                except ValueError:
                    print("Please enter a valid number.")
        print("Modifying slides...")
        time.sleep(1)
        index = 0
        while True:
            choice = input(
                "Which slides would you like to modify? "
                "You may input a range via 'x-y' (e.g., 0-3), "
                "one slide via x, or all using 'a': "
            )
            if choice == "a":
                print("You chose to modify all slides. Press the arrow keys to navigate. Press 'esc' to exit.")
                while True:
                    print(f"You are in slide {index}:")
                    self._slides[index] = input("Enter new content: ")
                    print("Slide is saved! Press the arrow keys to navigate.")
                    while True:
                        if keyboard.is_pressed("left"):
                            if index > 0:
                                index -= 1
                                break  
                            while keyboard.is_pressed("left"):
                                pass
                        elif keyboard.is_pressed("right"):
                            if index < self._size - 1:
                                index += 1
                                break
                            while keyboard.is_pressed("right"):
                                pass
                        elif keyboard.is_pressed("esc"):
                            print("You have exited editing the slideshow")
                            return  

            elif "-" in choice:
                parts = choice.split("-")
                if len(parts) == 2 and all(part.isdigit() for part in parts):
                    start, end = map(int, parts)
                    if start < 0 or end > self._size or start > end:
                        print(f"Invalid range. Start must be <= end, and both must be between 0 and {self._size - 1}.")
                        continue
                    print(f"You chose to modify slides {start} to {end}.")
                    index = start
                    while True:
                        print(f"You are in slide {index}:")
                        self._slides[index] = input("Enter new content: ")
                        print("Slide is saved! Press the arrow keys to navigate.")
                        while True:
                            if keyboard.is_pressed("left"):
                                if index > start:
                                    index -= 1
                                    break
                                while keyboard.is_pressed("left"):
                                    pass
                            elif keyboard.is_pressed("right"):
                                if index < end - 1:
                                    index += 1
                                    break
                                while keyboard.is_pressed("right"):
                                    pass
                            elif keyboard.is_pressed("esc"):
                                print("You have exited editing the slideshow")
                                return  
                else:
                    print("Invalid range format. Use the form x-y (e.g., 2-5).")

            elif choice.isdigit():
                slide_num = int(choice)
                print(f"You chose to modify slide {slide_num}.")
                self._slides[index] = input("Enter new content: ")
                break
            else:
                print("Please input a valid option!")
            
    def save(self):
        Document.saved_documents.append(self)

        with open("files/docs", "wb") as f:
            pickle.dump(Document.saved_documents, f)
        print("Your Powerpoint Presentation has been saved.")

    def print(self):
        index = 0
        print(
            f"{self.title.title()}\n"
            f"{self.author}\n\n"
            f"{self.text}\n"
        )
        print(f"{self._slides[index]}", end='\r', flush=True)
        while True:
            if keyboard.is_pressed("left"):
                if index > 0:
                    index -= 1
                    print(f"{CLEAR}{self._slides[index]}", end='\r', flush=True)
                    while keyboard.is_pressed("left"): 
                        pass
            elif keyboard.is_pressed("right"):
                if index < self._size - 1:
                    index += 1
                    print(f"{CLEAR}{self._slides[index]}", end='\r', flush=True)
                    while keyboard.is_pressed("right"): 
                        pass
            elif keyboard.is_pressed("esc"):
                print("You have exited the slideshow")
                break
            
    def share(self):
        print("Your SlideShow has been shared.")

class Spreadsheet(Document):
    
    def __init__(self, title = None, author = None, text = "", size= None):
        super().__init__(title, author, text)
        self._size = size
        if size:
            self._table = [["" for col in range(size)] for row in range(size)]
    
    @property
    def table(self):
        return self._table
    
    @table.setter
    def table(self, content):
        if len(content) != self._size:
            raise ValueError(f"Content must be a list of {self._size}x{self._size} table.")
        for i in range(self._size):
            if content[i] is not None:
                self._table[i] = content[i]
    
    def create(self):
        self.title = input("Enter the spreadsheet title: ")
        self.author = input("Enter the spreadsheet author: ")
        self.text = input("Enter the spreadsheet text: ")
        while True:
            self._size = input("Enter the size of the table: ")
            if self._size.isdigit():
                self._size = int(self._size)
                self._table = [["" for col in range(self._size)] for row in range(self._size)]
                break
            else:
                print("Please enter a valid number.")
        while True:
            choice = input("Do you want to modify the table now? Y/N")
            if choice == "Y" or choice == "y":
                self.modify(onlyTable = True)
                break
            elif choice == "N" or choice == "n":
                break
            else:
                print("Please enter a valid input")

    def modify(self, onlyTable = False):
        #will be implemented next day
        pass

    def save(self):
        Document.saved_documents.append(self)

        with open("files/docs", "wb") as f:
            pickle.dump(Document.saved_documents, f)
        print("Your Spreadsheet has been saved.")

    def print(self):
        print(
            f"{self.title.title()}\n"
            f"{self.author}\n\n"
            f"{self.text}\n\n"
        )

        for row in range(self._size):
            for column in range(self._size):
                cell = self._table[row][column]
                if len(cell) > 10: 
                    short = textwrap.shorten(cell, width=10, placeholder="...")
                    print(f"|{short:<10}|", end=" ")
                else:
                    print(f"|{cell:<10}|", end="")
            print()

    def share(self):
        print("Your Spreadsheet has been shared.")

#Should I make a subclass of Reports?
class Report(Document):

    def __init__(self):
        pass

    def create(self):
        pass

    def modify(self):
        pass

    def save(self):
        pass

    def print(self):
        pass

    def share(self):
        pass

class Email(Document):

    def __init__(self, title = None, author= None, s_from= None, r_to= None, text= "", subject= None, recipient= None, cc= None):
        super().__init__(title, author, text)
        self._s_from = s_from
        self._r_to = r_to
        self._subject = subject
        self._recipient = recipient
        self._cc = cc

    def create(self):
        self.title = input("Enter the email title: ")
        self.author = input("Enter the email author: ")
        self.text = input("Enter the email text: ")
        self._s_from = input("Enter the sender's email: ")
        self._r_to = input("Enter the recipient's email: ")
        self._subject = input("Enter the email subject: ")
        self._recipient = input("Enter the recipient's name: ")
        self._cc = input("Enter the CC (optional): ")


    def modify(self):
        pass
    
    def save(self):
        Document.saved_documents.append(self)

        with open("files/docs", "wb") as f:
            pickle.dump(Document.saved_documents, f)
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
        print("Your Email has been shared.")


class Letter(Document):

    def __init__(self, title = None, author = None, s_address = None, r_address = None, text = "", subject = None, recipient = None, includeDate = False):
        super().__init__(title, author, text)
        self._s_address = s_address
        if includeDate:
            self._date = datetime.date.today()
        self._r_address = r_address
        self._subject = subject
        self._recipient = recipient

    def create(self):
        self.title = input("Enter the letter title: ")
        self.author = input("Enter the letter author: ")
        self.text = input("Enter the letter text: ")
        self._s_address = input("Enter the sender's address: ")
        self._r_address = input("Enter the recipient's address: ")
        self._subject = input("Enter the subject of the letter: ")
        self._recipient = input("Enter the recipient's name: ")
        self._date = datetime.date.today()

    def modify(self):
        pass

    def save(self):
        Document.saved_documents.append(self)

        with open("files/docs", "wb") as f:
            pickle.dump(Document.saved_documents, f)
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
    print("Creating a Document...")

def share_document():
    pass

def edit_document():
    pass

def remove_document():
    pass

def read_document():
    pass

def init():
    if not os.path.exists("files"):
        os.makedirs("files")
    
    if os.path.exists("files/docs"):
        with open("files/docs", "rb") as f:
            try:
                Document.saved_documents = pickle.load(f)
                print("Documents loaded successfully.")
            except EOFError:
                print("No data to load.")

def handle_choice(choice):
    actions = {
        0: read_document,
        1: create_document,
        2: share_document,
        3: edit_document,
        4: remove_document
    }

    action = actions.get(choice)
    if action:
        action()
    elif choice == 5:
        return False
    else:
        print("Invalid Choice!")

    return True

# email_one = Letter("Random Title", 
#                   "Codyaxe", "Batangas City", "Alangilan",
#                   "I am testing if I can make a long line " 
#                   "that would violate the principles of programming " 
#                   "making programmers have to scroll horizontally to "
#                   "read the entire text", "A Message to a Classmate", "Aleckxa")
# email_one.print()
init()
# email_one.save()

# print(Document.saved_documents)
# print("Test 1:")
# Document.saved_documents[0].print()

#For Implementing A Menu Option
if __name__ == "__main__":
    print("Welcome to the Document Manager. What do you want to do today?")
    while True:
        choice = int(input("Enter your choice: "))
        if not handle_choice(choice):
            break