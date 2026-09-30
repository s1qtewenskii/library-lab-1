"""Классы предметной области «Библиотека».

Здесь только хранение данных: бизнес-логики (выдача, возврат книг) нет.
"""

from datetime import date
from typing import List, Optional

from exceptions import LibraryDataError


class Author:
    """Автор книги."""

    def __init__(self, full_name: str) -> None:
        self.full_name = full_name

    def __str__(self) -> str:
        return self.full_name


class Book:
    """Книга, которая есть в библиотеке."""

    def __init__(self, title: str, year: int, author: Author, quantity: int) -> None:
        # Проверяем данные сразу при создании объекта
        if year <= 0:
            raise LibraryDataError(f"Год издания книги «{title}» должен быть положительным")
        if quantity < 0:
            raise LibraryDataError(f"Количество экземпляров книги «{title}» не может быть отрицательным")

        self.title = title
        self.year = year
        self.author = author
        self.quantity = quantity  # сколько экземпляров лежит в библиотеке

    def __str__(self) -> str:
        return f"«{self.title}», {self.author}, {self.year} г., экземпляров: {self.quantity}"


class Reader:
    """Читатель библиотеки."""

    def __init__(self, full_name: str, ticket_number: int) -> None:
        self.full_name = full_name
        self.ticket_number = ticket_number  # номер читательского билета

    def __str__(self) -> str:
        return f"{self.full_name} (билет № {self.ticket_number})"


class Loan:
    """Выдача: какой читатель взял какую книгу и когда."""

    def __init__(self, book: Book, reader: Reader, date_taken: date) -> None:
        self.book = book
        self.reader = reader
        self.date_taken = date_taken

    def __str__(self) -> str:
        return f"{self.reader.full_name} взял(а) «{self.book.title}» {self.date_taken}"


class Library:
    """Библиотека: хранит списки книг, читателей и выдач."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.books: List[Book] = []
        self.readers: List[Reader] = []
        self.loans: List[Loan] = []

    def add_book(self, book: Book) -> None:
        self.books.append(book)

    def add_reader(self, reader: Reader) -> None:
        self.readers.append(reader)

    def add_loan(self, loan: Loan) -> None:
        self.loans.append(loan)

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """Возвращает книгу с таким названием или None, если её нет."""
        for book in self.books:
            if book.title == title:
                return book
        return None

    def find_reader_by_ticket(self, ticket_number: int) -> Optional[Reader]:
        """Возвращает читателя с таким номером билета или None, если его нет."""
        for reader in self.readers:
            if reader.ticket_number == ticket_number:
                return reader
        return None
