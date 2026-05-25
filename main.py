import json
import os
from datetime import datetime
from typing import List, Dict

BOOKS_FILE = "books.json"

def load_books() -> List[Dict]:
    """Загружает список книг из JSON-файла"""
    if not os.path.exists(BOOKS_FILE):
        return []
    
    try:
        with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_books(books: List[Dict]) -> None:
    """Сохраняет список книг в JSON-файл"""
    with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

def is_duplicate(books: List[Dict], author: str, title: str) -> bool:
    """Проверяет, существует ли уже книга с таким автором и названием"""
    return any(book['author'].lower() == author.lower() 
               and book['title'].lower() == title.lower() 
               for book in books)

def add_book(books: List[Dict]) -> List[Dict]:
    """Добавляет новую книгу"""
    print("\n--- Добавление книги ---")
    
    author = input("Введите автора: ").strip()
    if not author:
        print("Ошибка: автор не может быть пустым")
        return books
    
    title = input("Введите название: ").strip()
    if not title:
        print("Ошибка: название не может быть пустым")
        return books
    
    # Проверка на дубликаты
    if is_duplicate(books, author, title):
        print("Ошибка: такая книга уже существует!")
        return books
    
    try:
        rating = int(input("Введите оценку (1-5): "))
        if rating < 1 or rating > 5:
            print("Ошибка: оценка должна быть от 1 до 5")
            return books
    except ValueError:
        print("Ошибка: введите целое число")
        return books
    
    date_read = input("Введите дату прочтения (ГГГГ-ММ-ДД): ").strip()
    try:
        datetime.strptime(date_read, "%Y-%m-%d")
    except ValueError:
        print("Ошибка: неверный формат даты")
        return books
    
    book = {
        "author": author,
        "title": title,
        "rating": rating,
        "date_read": date_read
    }
    
    books.append(book)
    save_books(books)
    print(f"Книга '{title}' успешно добавлена!")
    
    return books

def show_all_books(books: List[Dict]) -> None:
    """Показывает все книги"""
    print("\n--- Список всех книг ---")
    
    if not books:
        print("Библиотека пуста.")
        return
    
    for idx, book in enumerate(books, 1):
        print(f"\n{idx}. {book['title']}")
        print(f"   Автор: {book['author']}")
        print(f"   Оценка: {book['rating']}/5")
        print(f"   Дата: {book['date_read']}")

def show_average_rating(books: List[Dict]) -> None:
    """Показывает среднюю оценку"""
    print("\n--- Средняя оценка ---")
    
    if not books:
        print("Нет книг для статистики.")
        return
    
    total = sum(book['rating'] for book in books)
    average = total / len(books)
    print(f"Средняя оценка: {average:.2f}/5")
    print(f"Всего книг: {len(books)}")

def show_author_stats(books: List[Dict]) -> None:
    """Статистика по авторам"""
    print("\n--- Статистика по авторам ---")
    
    if not books:
        print("Нет книг для статистики.")
        return
    
    author_stats = {}
    for book in books:
        author = book['author']
        if author not in author_stats:
            author_stats[author] = {'count': 0, 'total': 0}
        author_stats[author]['count'] += 1
        author_stats[author]['total'] += book['rating']
    
    for author, stats in sorted(author_stats.items()):
        avg = stats['total'] / stats['count']
        print(f"\n{author}:")
        print(f"   Книг: {stats['count']}, Средняя оценка: {avg:.2f}/5")

def delete_book(books: List[Dict]) -> List[Dict]:
    """Удаляет книгу"""
    print("\n--- Удаление книги ---")
    
    if not books:
        print("Библиотека пуста.")
        return books
    
    for idx, book in enumerate(books, 1):
        print(f"{idx}. {book['title']} - {book['author']}")
    
    try:
        choice = int(input("\nНомер книги для удаления: "))
        if 1 <= choice <= len(books):
            deleted = books.pop(choice - 1)
            save_books(books)
            print(f"Книга '{deleted['title']}' удалена!")
        else:
            print("Неверный номер")
    except ValueError:
        print("Ошибка: введите число")
    
    return books

def main():
    books = load_books()
    
    while True:
        print("\n=== Трекер прочитанных книг ===")
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Показать среднюю оценку")
        print("4. Статистика по авторам")
        print("5. Удалить книгу")
        print("6. Выход")
        
        choice = input("\nВыберите действие: ").strip()
        
        if choice == '1':
            books = add_book(books)
        elif choice == '2':
            show_all_books(books)
        elif choice == '3':
            show_average_rating(books)
        elif choice == '4':
            show_author_stats(books)
        elif choice == '5':
            books = delete_book(books)
        elif choice == '6':
            print("До свидания!")
            break
        else:
            print("Неверный выбор!")

if __name__ == "__main__":
    main()
