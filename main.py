"""Точка входа: загружает данные из XML и выводит их в консоль."""

from pathlib import Path

from exceptions import LibraryDataError
from xml_loader import load_library

XML_FILE_PATH = Path(__file__).parent / "data" / "library.xml"


def main() -> None:
    try:
        library = load_library(XML_FILE_PATH)
    except LibraryDataError as error:
        # Программа не падает, а сообщает пользователю, что не так
        print(f"Не удалось загрузить данные: {error}")
        return

    print(f"Библиотека: {library.name}")

    print("\nКниги:")
    for book in library.books:
        print(f"  {book}")

    print("\nЧитатели:")
    for reader in library.readers:
        print(f"  {reader}")

    print("\nВыдачи:")
    for loan in library.loans:
        print(f"  {loan}")


if __name__ == "__main__":
    main()
