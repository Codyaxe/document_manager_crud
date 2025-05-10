from abc import ABC, abstractmethod
from auxilliary_functions import clear_console, flush_input
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

    def __init__(self, title=None, author=None, text=""):
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

    @property
    def id(self):
        return self._id

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


class Slideshow(Document):

    def __init__(self, title=None, author=None, text="", size=None):
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
        self.title = input("Enter the slideshow's title: ")
        self.author = input("Enter the slideshow's author: ")
        self.text = input("Enter the slideshow's description: ")
        while True:
            self._size = input("Enter the number of slides in the slideshow: ")
            if self._size.isdigit():
                self._size = int(self._size)
                self._slides = ["" for slide in range(self._size)]
                break
            else:
                clear_console()
                print("Please enter a valid number.")
        while True:
            choice = input(
                "Do you want to modify the slides now? Y/N: ").strip().lower()
            if choice == "y":
                clear_console()
                self.modify(onlySlides=True)
                break
            elif choice == "n":
                break
            else:
                clear_console()
                print("Please enter a valid input")

    def modify(self, onlySlides=False):
        if not onlySlides:
            options = {
                1: "title",
                2: "author",
                3: "text",
            }
            while True:
                print("Which fields do you want to modify?")
                print("Press 1 to Modify Title")
                print("Press 2 to Modify Author")
                print("Press 3 to Modify Description")
                print("Press 4 to Modify Slides")
                print("Press 5 to Exit")
                choice = input("Choose: ")
                if choice.isdigit():
                    num = int(choice)
                    if num == 4:
                        break
                    if num == 5:
                        return
                    if num in options:
                        attr_name = options[num]
                        new_value = input(f"Enter the new {attr_name}: ")
                        setattr(self, attr_name, new_value)
                        print("The Slideshow has been modified...")
                        time.sleep(1)
                        clear_console()
                    else:
                        clear_console()
                        print("Invalid choice.")
                else:
                    clear_console()
                    print("Please enter a valid number!")
        clear_console()
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
                clear_console()
                print("You chose to modify all slides. ")
                print(
                    "Use arrow keys to navigate. Press 'esc' to exit. Press 'enter' to edit the slide.")
                print(
                    f"{CLEAR}Currently at Slide {index}: {self.slides[index]}", end='\r', flush=True)
                while True:
                    if keyboard.is_pressed("left"):
                        if index > 0:
                            index -= 1
                            print(
                                f"{CLEAR}Currently at Slide {index}: {self.slides[index]}", end='\r', flush=True)
                        while keyboard.is_pressed("left"):
                            pass
                    elif keyboard.is_pressed("right"):
                        if index < self._size - 1:
                            index += 1
                            print(
                                f"{CLEAR}Currently at Slide {index}: {self.slides[index]}", end='\r', flush=True)
                        while keyboard.is_pressed("right"):
                            pass
                    elif keyboard.is_pressed("enter"):
                        print(CLEAR, end='\r', flush=True)
                        while keyboard.is_pressed("enter"):
                            pass
                        flush_input()
                        self._slides[index] = input("Enter new content: ")
                        while keyboard.is_pressed("enter"):
                            pass
                        print(
                            f"{CLEAR}Currently at Slide {index}: {self.slides[index]}", end='\r', flush=True)
                    elif keyboard.is_pressed("esc"):
                        print("You have exited editing the slideshow")
                        return

            elif "-" in choice:
                clear_console()
                parts = choice.split("-")
                if len(parts) == 2 and all(part.isdigit() for part in parts):
                    start, end = map(int, parts)
                    if start < 0 or end > self._size - 1 or start > end:
                        print(
                            f"Invalid range. Start must be <= end, and both must be between 0 and {self._size - 1}.")
                        continue
                    print(f"You chose to modify slides {start} to {end}.")
                    index = start
                    print(
                        "Use arrow keys to navigate. Press 'esc' to exit. Press 'enter' to edit the slide.")
                    print(
                        f"{CLEAR}Currently at Slide {index}: {self.slides[index]}", end='\r', flush=True)
                    while True:
                        if keyboard.is_pressed("left"):
                            if index > start:
                                index -= 1
                                print(
                                    f"{CLEAR}Currently at Slide {index}: {self.slides[index]}", end='\r', flush=True)
                            while keyboard.is_pressed("left"):
                                pass
                        elif keyboard.is_pressed("right"):
                            if index < end - 1:
                                index += 1
                                print(
                                    f"{CLEAR}Currently at Slide {index}: {self.slides[index]}", end='\r', flush=True)
                            while keyboard.is_pressed("right"):
                                pass
                        elif keyboard.is_pressed("enter"):
                            print(CLEAR, end='\r', flush=True)
                            while keyboard.is_pressed("enter"):
                                pass
                            flush_input()
                            print("Enter new content: ", end='', flush=True)
                            self._slides[index] = input()
                            while keyboard.is_pressed("enter"):
                                pass
                            print(
                                f"{CLEAR}Currently at Slide {index}: {self.slides[index]}", end='\r', flush=True)
                        elif keyboard.is_pressed("esc"):
                            print("You have exited slideshow modification")
                            return
                else:
                    clear_console()
                    print("Invalid range format. Use the form x-y (e.g., 2-5).")

            elif choice.isdigit():
                clear_console()
                slide_num = int(choice)
                print(f"You chose to modify slide {slide_num}.")
                self._slides[index] = input("Enter new content: ")
                break
            else:
                clear_console()
                print("Please input a valid option!")

    def save(self):
        for i in range(len(Document.saved_documents)):
            if Document.saved_documents[i].id == self.id:
                Document.saved_documents[i] = self
                break
        else:
            Document.saved_documents.append(self)

        with open("files/docs", "wb") as f:
            pickle.dump(Document.saved_documents, f)
        print("Your Slideshow has been saved.")

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
                    print(
                        f"{CLEAR}{self._slides[index]}", end='\r', flush=True)
                    while keyboard.is_pressed("left"):
                        pass
            elif keyboard.is_pressed("right"):
                if index < self._size - 1:
                    index += 1
                    print(
                        f"{CLEAR}{self._slides[index]}", end='\r', flush=True)
                    while keyboard.is_pressed("right"):
                        pass
            elif keyboard.is_pressed("esc"):
                print("You have exited the slideshow")
                break


class Spreadsheet(Document):

    def __init__(self, title=None, author=None, text="", size=None):
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
            raise ValueError(
                f"Content must be a list of {self._size}x{self._size} table.")
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
                self._table = [["" for col in range(
                    self._size)] for row in range(self._size)]
                break
            else:
                print("Please enter a valid number.")
        while True:
            choice = input(
                "Do you want to modify the table now? Y/N: ").strip().lower()
            if choice == "y":
                self.modify(onlyTable=True)
                break
            elif choice == "n":
                break
            else:
                clear_console()
                print("Please enter a valid input")

    def modify(self, onlyTable=False):
        if not onlyTable:
            options = {
                1: "title",
                2: "author",
                3: "text",
            }
            while True:
                print("Which fields do you want to modify?")
                print("Press 1 to Modify Title")
                print("Press 2 to Modify Author")
                print("Press 3 to Modify Description")
                print("Press 4 to Modify Table")
                print("Press 5 to Exit")
                choice = input("Choose: ")
                if choice.isdigit():
                    num = int(choice)
                    if num == 4:
                        break
                    if num == 5:
                        return
                    if num in options:
                        attr_name = options[num]
                        new_value = input(f"Enter the new {attr_name}: ")
                        setattr(self, attr_name, new_value)
                        print("The Spreadsheet has been modified...")
                        time.sleep(1)
                        clear_console()
                    else:
                        clear_console()
                        print("Invalid choice.")
                else:
                    clear_console()
                    print("Please enter a valid number.")

        print("Modifying table...")
        time.sleep(1)
        row, col = 0, 0
        print(
            "Use arrow keys to navigate. Press 'esc' to exit. Press 'enter' to edit cell.")
        print(
            f"{CLEAR}Currently at cell ({row}, {col}): {self._table[row][col]}", end='\r', flush=True)
        while True:
            if keyboard.is_pressed("left"):
                if col > 0:
                    col -= 1
                    print(
                        f"{CLEAR}Currently at cell ({row}, {col}): {self._table[row][col]}", end='\r', flush=True)
                while keyboard.is_pressed("left"):
                    pass
            elif keyboard.is_pressed("right"):
                if col < self._size - 1:
                    col += 1
                    print(
                        f"{CLEAR}Currently at cell ({row}, {col}): {self._table[row][col]}", end='\r', flush=True)
                while keyboard.is_pressed("right"):
                    pass
            elif keyboard.is_pressed("up"):
                if row > 0:
                    row -= 1
                    print(
                        f"{CLEAR}Currently at cell ({row}, {col}): {self._table[row][col]}", end='\r', flush=True)
                while keyboard.is_pressed("up"):
                    pass
            elif keyboard.is_pressed("down"):
                if row < self._size - 1:
                    row += 1
                    print(
                        f"{CLEAR}Currently at cell ({row}, {col}): {self._table[row][col]}", end='\r', flush=True)
                while keyboard.is_pressed("down"):
                    pass
            elif keyboard.is_pressed("enter"):
                print(CLEAR, end='\r', flush=True)
                while keyboard.is_pressed("enter"):
                    pass
                flush_input()
                new_content = input(
                    f"Enter new content for cell ({row}, {col}): ")
                while keyboard.is_pressed("enter"):
                    pass
                self._table[row][col] = new_content
                print(
                    f"{CLEAR}Currently at cell ({row}, {col}): {self._table[row][col]}", end='\r', flush=True)
                flush_input()
            elif keyboard.is_pressed("esc"):
                print("You have exited table modification.")
                break

    def save(self):
        for i in range(len(Document.saved_documents)):
            if Document.saved_documents[i].id == self.id:
                Document.saved_documents[i] = self
                break
        else:
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

        while True:
            choice = input(
                "Do you want to navigate the cells? Y/N: ").strip().lower()
            if choice == "y":
                break
            elif choice == "n":
                return
            else:
                clear_console()
                print("Please enter a valid input")

        print("Use arrow keys to navigate. Press 'esc' to exit.")
        row, col = 0, 0
        print(f"Currently at cell ({row}, {col}): {self._table[row][col]}")
        while True:
            if keyboard.is_pressed("left"):
                if col > 0:
                    col -= 1
                    print(
                        f"{CLEAR}Currently at cell ({row}, {col}): {self._table[row][col]}", end='\r', flush=True)
                while keyboard.is_pressed("left"):
                    pass
            elif keyboard.is_pressed("right"):
                if col < self._size - 1:
                    col += 1
                    print(
                        f"{CLEAR}Currently at cell ({row}, {col}): {self._table[row][col]}", end='\r', flush=True)
                while keyboard.is_pressed("right"):
                    pass
            elif keyboard.is_pressed("up"):
                if row > 0:
                    row -= 1
                    print(
                        f"{CLEAR}Currently at cell ({row}, {col}): {self._table[row][col]}", end='\r', flush=True)
                while keyboard.is_pressed("up"):
                    pass
            elif keyboard.is_pressed("down"):
                if row < self._size - 1:
                    row += 1
                    print(
                        f"{CLEAR}Currently at cell ({row}, {col}): {self._table[row][col]}", end='\r', flush=True)
                while keyboard.is_pressed("down"):
                    pass
            elif keyboard.is_pressed("esc"):
                print("You have exited cell navigation.")
                break


class Email(Document):

    def __init__(self, title=None, author=None, s_from=None, r_to=None, text="", subject=None, recipient=None, cc=None):
        super().__init__(title, author, text)
        self._s_from = s_from
        self._r_to = r_to
        self._subject = subject
        self._recipient = recipient
        self._cc = cc

    def create(self):
        self.title = input("Enter the email's title: ")
        self.author = input("Enter the email's author: ")
        self.text = input("Enter the email's content: ")
        self._s_from = input("Enter the sender's email: ")
        self._r_to = input("Enter the recipient's email: ")
        self._subject = input("Enter the email's subject: ")
        self._recipient = input("Enter the recipient's name: ")
        self._cc = input("Enter the CC (optional): ")

    def modify(self):
        fields = {
            1: ("title", "Enter the email's title: "),
            2: ("author", "Enter the email's author: "),
            3: ("text", "Enter the email's content: "),
            4: ("_s_from", "Enter the sender's email: "),
            5: ("_r_to", "Enter the recipient's email: "),
            6: ("_subject", "Enter the email's subject: "),
            7: ("_recipient", "Enter the recipient's name: "),
            8: ("_cc", "Enter the CC (optional): ")
        }
        while True:
            print("Which fields do you want to modify?")
            print("Enter 1 to change email's title")
            print("Enter 2 to change email's author")
            print("Enter 3 to change email's content")
            print("Enter 4 to change sender's email")
            print("Enter 5 to change recipient's email")
            print("Enter 6 to change email's subject")
            print("Enter 7 to change recipient's name")
            print("Enter 8 to change CC")
            print("Enter 9 to exit")
            choice = input("Choose: ")
            if choice.isdigit():
                num = int(choice)
                if num == 9:
                    break
                elif num in fields:
                    attr, prompt = fields[num]
                    setattr(self, attr, input(prompt))
                    print("The Email has been modified...")
                    time.sleep(1)
                    clear_console()
                else:
                    clear_console()
                    print("Invalid choice.")
            else:
                clear_console()
                print("Please enter a valid number.")

    def save(self):
        for i in range(len(Document.saved_documents)):
            if Document.saved_documents[i].id == self.id:
                Document.saved_documents[i] = self
                break
        else:
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
        print("Press 'esc' to exit.")
        while True:
            if keyboard.is_pressed("esc"):
                while keyboard.is_pressed("left"):
                    pass
                break


class Letter(Document):

    def __init__(self, title=None, author=None, s_address=None, r_address=None, text="", subject=None, recipient=None, includeDate=False):
        super().__init__(title, author, text)
        self._s_address = s_address
        if includeDate:
            self._date = datetime.date.today()
        self._r_address = r_address
        self._subject = subject
        self._recipient = recipient

    def create(self):
        self.title = input("Enter the letter's title: ")
        self.author = input("Enter the letter's author: ")
        self.text = input("Enter the letter's content: ")
        self._s_address = input("Enter the sender's address: ")
        self._r_address = input("Enter the recipient's address: ")
        self._subject = input("Enter the letter's subject: ")
        self._recipient = input("Enter the recipient's name: ")
        self._date = datetime.date.today()

    def modify(self):
        fields = {
            1: ("title", "Enter the letter's title: "),
            2: ("author", "Enter the letter's author: "),
            3: ("text", "Enter the letter's content: "),
            4: ("_s_address", "Enter the sender's address: "),
            5: ("_r_address", "Enter the recipient's address: "),
            6: ("_subject", "Enter the letter's subject: "),
            7: ("_recipient", "Enter the recipient's name: "),
        }
        while True:
            print("Which fields do you want to modify?")
            print("Enter 1 to change letter's title")
            print("Enter 2 to change letter's author")
            print("Enter 3 to change letter's content")
            print("Enter 4 to change sender's address")
            print("Enter 5 to change recipient's address")
            print("Enter 6 to change letter's subject")
            print("Enter 7 to change recipient's name")
            print("Enter 8 to exit")
            choice = input("Choose: ")
            if choice.isdigit():
                num = int(choice)
                if num == 8:
                    break
                elif num in fields:
                    attr, prompt = fields[num]
                    setattr(self, attr, input(prompt))
                    print("The Letter has been modified...")
                    time.sleep(1)
                    clear_console()
                else:
                    clear_console()
                    print("Invalid choice.")
            else:
                clear_console()
                print("Please enter a valid number.")

    def save(self):
        for i in range(len(Document.saved_documents)):
            if Document.saved_documents[i].id == self.id:
                Document.saved_documents[i] = self
                break
        else:
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
        print("Press 'esc' to exit.")
        while True:
            if keyboard.is_pressed("esc"):
                while keyboard.is_pressed("left"):
                    pass
                break


def create_document():
    clear_console()
    print("Creating a Document...")
    time.sleep(1)

    # None are placeholder objects
    docs = {1: Spreadsheet,
            2: Slideshow,
            3: Email,
            4: Letter,
            5: None,
            6: None,
            7: None
            }
    instance = None
    while True:
        print("Which type of documents do you want create?")
        print("Enter 1 to create Spreadsheet")
        print("Enter 2 to create Slideshow")
        print("Enter 3 to create Email")
        print("Enter 4 to create Letter")
        print("Enter 5 to create _____")
        print("Enter 6 to create _____")
        print("Enter 7 to create _____")
        print("Enter 8 to exit")
        choice = input("Choose: ")
        if choice.isdigit():
            num = int(choice)
            if num == 8:
                break
            elif num in docs and docs[num] is not None:
                instance = docs[num]()
                clear_console()
                instance.create()
                clear_console()
                instance.save()
                break
            else:
                clear_console()
                print("Invalid choice.")
        else:
            clear_console()
            print("Please enter a valid number.")


def edit_document():
    clear_console()
    print("Editing a Document...")
    time.sleep(1)
    size = len(Document.saved_documents)
    index = 0

    if size == 0:
        print("You have no documents to edit")
        return

    print("Choose a document to edit.")
    print("Use arrow keys to navigate. Press 'esc' to exit. Press 'enter' to edit document.")
    print(
        f"{CLEAR}Currently at Document {index}: {Document.saved_documents[index].title} Type: {type(Document.saved_documents[index]).__name__}", end='\r', flush=True)
    while True:
        if keyboard.is_pressed("left"):
            if index > 0:
                index -= 1
                print(
                    f"{CLEAR}Currently at Document {index}: {Document.saved_documents[index].title} Type: {type(Document.saved_documents[index]).__name__}", end='\r', flush=True)
                while keyboard.is_pressed("left"):
                    pass
        elif keyboard.is_pressed("right"):
            if index < size - 1:
                index += 1
                print(
                    f"{CLEAR}Currently at Document {index}: {Document.saved_documents[index].title} Type: {type(Document.saved_documents[index]).__name__}", end='\r', flush=True)
                while keyboard.is_pressed("right"):
                    pass
        elif keyboard.is_pressed("enter"):
            print(CLEAR, end='\r', flush=True)
            while keyboard.is_pressed("enter"):
                pass
            flush_input()
            clear_console()
            Document.saved_documents[index].modify()
            while keyboard.is_pressed("enter"):
                pass
            flush_input()
            clear_console()
            Document.saved_documents[index].save()
            print(
                f"{CLEAR}Currently at Document {index}: {Document.saved_documents[index].title} Type: {type(Document.saved_documents[index]).__name__}", end='\r', flush=True)
        elif keyboard.is_pressed("esc"):
            return


def remove_document():
    clear_console()
    print("Removing a Document...")
    time.sleep(1)
    size = len(Document.saved_documents)
    index = 0

    if size == 0:
        print("You have no documents to remove")
        return

    print("Choose a document to remove.")
    print("Use arrow keys to navigate. Press 'esc' to exit. Press 'enter' to remove document.")
    print(
        f"{CLEAR}Currently at Document {index}: {Document.saved_documents[index].title} Type: {type(Document.saved_documents[index]).__name__}", end='\r', flush=True)
    while True:
        size = len(Document.saved_documents)

        if keyboard.is_pressed("left"):
            if index > 0:
                index -= 1
                print(
                    f"{CLEAR}Currently at Document {index}: {Document.saved_documents[index].title} Type: {type(Document.saved_documents[index]).__name__}", end='\r', flush=True)
                while keyboard.is_pressed("left"):
                    pass
        elif keyboard.is_pressed("right"):
            if index < size - 1:
                index += 1
                print(
                    f"{CLEAR}Currently at Document {index}: {Document.saved_documents[index].title} Type: {type(Document.saved_documents[index]).__name__}", end='\r', flush=True)
                while keyboard.is_pressed("right"):
                    pass
        elif keyboard.is_pressed("enter"):
            print(CLEAR, end='\r', flush=True)
            while keyboard.is_pressed("enter"):
                pass
            flush_input()
            clear_console()
            removed_document = Document.saved_documents.pop(index)
            print(f"{CLEAR}Removed Document: {removed_document.title} Type: {type(removed_document).__name__}", end='\r', flush=True)
            time.sleep(1)
            with open("files/docs", "wb") as f:
                pickle.dump(Document.saved_documents, f)
            while keyboard.is_pressed("enter"):
                pass
            flush_input()
            clear_console()
            index -= 1
            if len(Document.saved_documents) > 0:
                print(
                    f"{CLEAR}Currently at Document {index}: {Document.saved_documents[index].title} Type: {type(Document.saved_documents[index]).__name__}", end='\r', flush=True)
            else:
                print("You have no documents")
                return
        elif keyboard.is_pressed("esc"):
            return


def read_document():
    clear_console()
    print("Reading a Document...")
    time.sleep(1)
    size = len(Document.saved_documents)
    index = 0

    if size == 0:
        print("You have no documents to read")
        return

    print("Choose a document to read.")
    print("Use arrow keys to navigate. Press 'esc' to exit. Press 'enter' to read document.")
    print(
        f"{CLEAR}Currently at Document {index}: {Document.saved_documents[index].title} Type: {type(Document.saved_documents[index]).__name__}", end='\r', flush=True)
    while True:
        if keyboard.is_pressed("left"):
            if index > 0:
                index -= 1
                print(
                    f"{CLEAR}Currently at Document {index}: {Document.saved_documents[index].title} Type: {type(Document.saved_documents[index]).__name__}", end='\r', flush=True)
                while keyboard.is_pressed("left"):
                    pass
        elif keyboard.is_pressed("right"):
            if index < size - 1:
                index += 1
                print(
                    f"{CLEAR}Currently at Document {index}: {Document.saved_documents[index].title} Type: {type(Document.saved_documents[index]).__name__}", end='\r', flush=True)
                while keyboard.is_pressed("right"):
                    pass
        elif keyboard.is_pressed("enter"):
            print(CLEAR, end='\r', flush=True)
            while keyboard.is_pressed("enter"):
                pass
            flush_input()
            clear_console()
            Document.saved_documents[index].print()
            while keyboard.is_pressed("enter"):
                pass
            flush_input()
            clear_console()
            print(
                f"{CLEAR}Currently at Document {index}: {Document.saved_documents[index].title} Type: {type(Document.saved_documents[index]).__name__}", end='\r', flush=True)
        elif keyboard.is_pressed("esc"):
            return


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
        1: read_document,
        2: create_document,
        3: edit_document,
        4: remove_document
    }

    action = actions.get(choice)
    if action:
        action()
    elif choice == 5:
        return False
    else:
        clear_console()
        print("Invalid Choice!")

    return True

# email_one = Letter("Random Title",
#                   "Codyaxe", "Batangas City", "Alangilan",
#                   "I am testing if I can make a long line "
#                   "that would violate the principles of programming "
#                   "making programmers have to scroll horizontally to "
#                   "read the entire text", "A Message to a Classmate", "Aleckxa")
# email_one.print()

# email_one.save()

# print(Document.saved_documents)
# print("Test 1:")
# Document.saved_documents[0].print()


# For Implementing A Menu Option
if __name__ == "__main__":
    init()
    while True:
        print("Welcome to the Document Manager. What do you want to do today?")
        print("Enter 1 to Read Documents")
        print("Enter 2 to Create Documents")
        print("Enter 3 to Modify Documents")
        print("Enter 4 to Remove Documents")
        print("Enter 5 to Exit")
        choice = int(input("Enter your choice: "))
        if not handle_choice(choice):
            break
