from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QTextEdit, QMessageBox
import sys
import json


class Book:
    def __init__(self, title, author, cost):
        self.title = title
        self.author = author
        self.cost = cost

    def getTitle(self):
        return self.title

    def getAuthor(self):
        return self.author

    def getCost(self):
        return self.cost


class Section:
    def __init__(self, title):
        self.title = title
        self.books = []

    def getTitle(self):
        return self.title

    def addBook(self, book):
        self.books.append(book)
        return

    def searchBookByTitle(self, title):
        for book in self.books:
            if book.getTitle() == title:
                return {book}

    def searchBookByAuthor(self, author):
        for book in self.books:
            if book.getAuthor() == author:
                return {book}

    def deleteBook(self, title):
        book_to_delete = None
        for book in self.books:
            if book.getTitle() == title:
                book_to_delete = book
                break
        if book_to_delete:
            self.books.remove(book_to_delete)
            return

    def showBooks(self):
        for book in self.books:
            print(f"Book Title: {book.getTitle()}\n The Author: {book.getAuthor}\n The Cost: {book.getCost}\n")
            return


class Library:
    def __init__(self, title):
        self.title = title
        self.sections = []
        self.profit = 0

    def addSection(self, section):
        self.sections.append(section)
        return

    def searchBookByTitle(self, title):
        all_books_title = []
        for section in self.sections:
            all_books_title.extend(section.searchBookByTitle(title))
        return all_books_title

    def searchBookByAuthor(self, author):
        all_books_author = []
        for section in self.sections:
            all_books_author.extend(section.searchBookByTitle(author))
        return all_books_author

    def sellaBook(self, title):
        for section in self.sections:
            for book in section.books:
                if book.title == title:
                    self.profit += book.getCost()
                    section.deleteBook(title)
                    return
    def getTotalProfit(self):
        return self.profit


def load_data_from_json(json_file):
    with open(json_file) as f:
        data = json.load(f)

    library = Library("Book Store")  # Create a new library instance

    for book_title, book_data in data.items():
        title = book_title
        author = book_data["author"]
        cost = book_data["cost"]
        section = book_data["section"]

        book = Book(title, author, cost)
        library_section = Section(section)
        library_section.addBook(book)
        library.addSection(library_section)

    return library


class MyWindow(QMainWindow):

    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200, 200, 700, 700)
        self.setWindowTitle("Book Store")
        self.library = load_data_from_json("C:/Users/Ahmed Yahya/PycharmProjects/pythonProject/books.json")

        self.init_ui()

    def init_ui(self):
        # print title in the beginning
        self.label = QtWidgets.QLabel(self)
        self.label.setText("              Welcome to Book Store")
        self.label.move(30, 30)
        # make the title bigger
        label_font = self.label.font()
        label_font.setPointSize(20)
        self.label.setFont(label_font)
        # adjust the title to the window
        self.label.adjustSize()
        # add image
        self.image_label = QtWidgets.QLabel(self)
        self.image_label.setGeometry(100, 0, 700, 700)
        image = QtGui.QPixmap("C:/Users/Ahmed Yahya/Desktop/OIP (1).jpeg")
        self.image_label.setPixmap(image)
        # create search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setGeometry(150, 400, 400, 30)
        self.search_bar.setPlaceholderText("Search in Book Store")

        # create push button

        self.search_by_title_btn = QtWidgets.QPushButton(self)
        self.search_by_title_btn.setText("Search by Title")
        self.search_by_title_btn.setGeometry(180, 450, 100, 30)
        self.search_by_title_btn.clicked.connect(self.search_by_title)

        self.search_by_author_btn = QtWidgets.QPushButton(self)
        self.search_by_author_btn.setText("Search by Author")
        self.search_by_author_btn.setGeometry(280, 450, 120, 30)
        self.search_by_author_btn.clicked.connect(self.search_by_author)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Buy a Book")
        self.b1.setGeometry(400, 450, 100, 30)
        self.b1.clicked.connect(self.buy)

    def search_by_title(self):
        title = self.search_bar.text()
        title_found = False
        for section in self.library.sections:
            for book in section.books:
                if book.title == title:
                    self.display_book_details(book, section)
                    title_found = True
        if not title_found:
            QMessageBox.warning(self, "Book Not Found", f"{title} not found in the library")

    def search_by_author(self):
        author = self.search_bar.text()
        author_found = False
        for section in self.library.sections:
            for book in section.books:
                if book.author == author:
                    self.display_book_details(book, section)
                    author_found = True
        if not author_found:
            QMessageBox.warning(self, "Author Not Found", f"{author} not found in the library")

    def display_book_details(self, book, section):
        # Display book details in a QMessageBox
        details = f"Title: {book.title}\nAuthor: {book.author}\nCost: {book.cost}\nSection: {section.title}"
        QMessageBox.information(self, "Book Details", details)

    def buy(self):
        sold_book_title = self.search_bar.text()
        for section in self.library.sections:
            for book in section.books:
                if book.title == sold_book_title:
                    self.library.sellaBook(sold_book_title)
                    QMessageBox.information(self, "Book Sold",f"{sold_book_title} successfully sold\n The Cost: {book.cost}\n The Total Price: {self.library.profit}")


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


window()