"""Загрузка данных библиотеки из XML-файла в объекты."""

import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path
from typing import Dict

from exceptions import LibraryDataError
from models import Author, Book, Library, Loan, Reader


def read_text(parent: ET.Element, tag_name: str) -> str:
    """Возвращает текст вложенного тега. Если тега нет — бросает LibraryDataError."""
    element = parent.find(tag_name)
    if element is None or element.text is None:
        raise LibraryDataError(f"В теге <{parent.tag}> нет обязательного поля <{tag_name}>")
    return element.text.strip()


def read_int(parent: ET.Element, tag_name: str) -> int:
    """Возвращает содержимое вложенного тега как целое число."""
    text = read_text(parent, tag_name)
    try:
        return int(text)
    except ValueError as error:
        raise LibraryDataError(f"В поле <{tag_name}> должно быть число, а не «{text}»") from error


def load_books(root: ET.Element, library: Library) -> None:
    """Читает раздел <books> и добавляет книги (вместе с авторами) в библиотеку."""
    # Один и тот же автор должен быть одним объектом, даже если у него несколько книг
    authors_by_name: Dict[str, Author] = {}

    for book_element in root.findall("books/book"):
        author_name = read_text(book_element, "author")
        if author_name not in authors_by_name:
            authors_by_name[author_name] = Author(author_name)

        book = Book(
            title=read_text(book_element, "title"),
            year=read_int(book_element, "year"),
            author=authors_by_name[author_name],
            quantity=read_int(book_element, "quantity"),
        )
        library.add_book(book)


def load_readers(root: ET.Element, library: Library) -> None:
    """Читает раздел <readers> и добавляет читателей в библиотеку."""
    for reader_element in root.findall("readers/reader"):
        reader = Reader(
            full_name=read_text(reader_element, "full_name"),
            ticket_number=read_int(reader_element, "ticket_number"),
        )
        library.add_reader(reader)


def load_loans(root: ET.Element, library: Library) -> None:
    """Читает раздел <loans>. Книги и читателей ищет среди уже загруженных."""
    for loan_element in root.findall("loans/loan"):
        book_title = read_text(loan_element, "book_title")
        ticket_number = read_int(loan_element, "reader_ticket")
        date_text = read_text(loan_element, "date_taken")

        book = library.find_book_by_title(book_title)
        if book is None:
            raise LibraryDataError(f"В выдаче указана неизвестная книга «{book_title}»")

        reader = library.find_reader_by_ticket(ticket_number)
        if reader is None:
            raise LibraryDataError(f"В выдаче указан неизвестный читатель с билетом № {ticket_number}")

        try:
            date_taken = date.fromisoformat(date_text)  # формат ГГГГ-ММ-ДД
        except ValueError as error:
            raise LibraryDataError(f"Дата «{date_text}» должна быть в формате ГГГГ-ММ-ДД") from error

        library.add_loan(Loan(book, reader, date_taken))


def load_library(file_path: Path) -> Library:
    """Главная функция: читает XML-файл и возвращает готовый объект Library."""
    try:
        tree = ET.parse(file_path)
    except FileNotFoundError as error:
        raise LibraryDataError(f"Файл {file_path} не найден") from error
    except ET.ParseError as error:
        raise LibraryDataError(f"Файл {file_path} содержит некорректный XML: {error}") from error

    root = tree.getroot()
    library = Library(name=read_text(root, "name"))

    # Порядок важен: выдачи ссылаются на книги и читателей, поэтому они грузятся последними
    load_books(root, library)
    load_readers(root, library)
    load_loans(root, library)

    return library
