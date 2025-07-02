import re
from typing import List, Tuple, Union
import formatter as fm

def main_menu():
    menu_text = """Введите:
    1 - если поиск по ключевому слову
    2 - если поиск по жанру и диапазону годов выпуска
    3 - Посмотреть популярные или последние запросы
    -----
    0 - выход"""
    try:
        print(menu_text)
        search_type = int(input("\nВаш выбор:"))
        return search_type
    except ValueError:
        return -1

# Печать страницы результатов и запрос вывода следующей
# res - результаты поиска
# page_number - отображаемая страница
# max_page - номер последней доступной страницы
# Возвращает True для перехода к след. странице или False для прекращения вывода
def showNextResultsPage(res, page_number, max_page):
    print(f"\n--- Страница {page_number} ---")
    fm.print_table_films(res)

    if page_number >= max_page:
        print("Вы достигли последней страницы.")
        return False

    while True:
        page_next = input("Перейти на следующую страницу? (Y)es/(N)o: ").strip().upper()
        if page_next == "YES" or page_next == "Y":
            return True
        elif page_next == "NO" or page_next == "N":
            return False

def inputCategory(categories: List[Tuple[str, int, int]]) -> int:

    def printCategories(categories: List[Tuple[str, int, int]]) -> None:
        col_width = max(len(cat[0]) for cat in categories) + 6  # 6 = длина "[99] "
        for idx, cat in enumerate(categories, 1):
            entry = f"[{idx}]{cat[0]}".ljust(col_width)
            print(entry, end='')
            # Переход на новую строку каждые 4 категории
            if idx % 4 == 0:
                print()
        # Переход на новую строку, если строка была не завершена
        if len(categories) % 4 != 0:
            print()

    while True:
        try:
            print("Доступные категории: ")
            printCategories(categories)
            search_category_num = int(input("Введите номер категории или 0 для выхода: "))
        except ValueError:
            print("Ошибка ввода. Введите числовое значение.")
            continue
        if search_category_num == 0:
            return 0
        if 1 <= search_category_num <= len(categories):
            return search_category_num
        else:
            print("Неверное значение, попробуйте еще раз.")

def inputYears(range_min: int, range_max: int)-> Tuple[int, int]:
    print(f"По выбранной категории доступны годы выпуска с {range_min} по {range_max}")
    while True:
        year_input = input("Введите год или диапазон (например: 2020 или 2010-2020): ").strip()
        # Ищем двух- или однозначные года
        years = re.findall(r'\d{4}', year_input)
        try:
            if len(years) == 2:
                min_year = int(years[0])
                max_year = int(years[1])
                if min_year > max_year:
                    min_year, max_year = max_year, min_year  # автоматический обмен
            elif len(years) == 1:
                min_year = max_year = int(years[0])
            else:
                raise ValueError
            if min_year < range_min or max_year > range_max:
                raise ValueError
            return (min_year, max_year)
        except ValueError:
            print("Неверный формат года. Введите год или диапазон, например: 2015 или 2010-2020.")

