# Задание 1 (ПМ.01). Разработайте классы Book (название, автор, год, isbn)
# и Library с методами add_book(), remove_book(), find_by_author().
# Используйте коллекции для хранения книг.

# Задание 2 (ПМ.02). Реализуйте модуль для импорта книг из CSV-файла и
# экспорта в CSV. Обеспечьте обработку ошибок (неверный формат,
# отсутствие файла).

# Задание 3 (Отладка). Добавьте в класс Library метод validate_isbn(), который
# проверяет корректность ISBN. Напишите юнит-тесты для этого метода (2-3
# тестовых случая).
import csv
import os

class Book:
    def __init__(self, title='', author='', year=0, isbn=''):
        self.title=title
        self.author=author
        self.year=year
        self.isbn=isbn

    def to_dict(self):
        return self.__dict__


class Library:
    def __init__(self):
        self.books=[]

    def add_book(self, book):
        if len(book.isbn)!= 13:
            raise ValueError("Invalid book data")
        self.books.append(book)

    def remove_book(self, isbn):
        self.books=[book for book in self.books if book.isbn != isbn] 
    
    def find_by_author(self, author):
        return [book for book in self.books if book.author==author]
    
    @staticmethod
    def validate_isbn(isbn):
        if len(isbn) != 13 or not isbn.isdigit():
            return False
        else:
            return True
        

class Storage:

    @staticmethod
    def import_from_csv(file_path):
        books=[]
        if not os.path.exists(file_path):
            print(f"File {file_path} not found.")
            return
        
        try:
            with open(file_path, mode='r', newline='',) as file:
                reader=csv.DictReader(file)
                books=[row for row in reader]
                return books
        except Exception as e:
            print(f"Error reading file: {e}")


    @staticmethod
    def export_to_csv(file_path, books):
        fieldnames=['title', 'author', 'year', 'isbn']
        try:
            with open(file_path, mode='w', newline='') as file:
                writer=csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                writer.writerows(books)
        except Exception as e:
            print(f"Error writing to file: {e}")
               

new_book=Book("1984", "George Orwell", 1949, "1234567890123")
new_library=Library()

new_storage=Storage()
try:
    new_library.add_book(new_book)
    new_storage.export_to_csv("books.csv", [new_book.to_dict()])
except ValueError as e:
    print(e)