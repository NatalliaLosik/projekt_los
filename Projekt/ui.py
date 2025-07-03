import re
from typing import List, Tuple, Union
import formatter as fm

def mainMenu() -> int:
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

def showNextResultsPage(res: list, page_number: int, max_page: int) -> bool:
    """
    Показывает текущую страницу с результатами и спрашивает у пользователя, хочет ли он перейти к следующей.

    Аргументы:
    - res (list): Список фильмов или результатов, которые нужно отобразить на текущей странице.
    - page_number (int): Номер текущей страницы.
    - max_page (int): Общее количество доступных страниц.

    Возвращает:
    - bool: True, если пользователь хочет перейти к следующей странице, иначе False.
    """
    if not res:
        return False
    print(f"\n--- Страница {page_number} из {max_page} ---")
    fm.printTableFilms(res)

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

def inputYears(range_min: int, range_max: int) -> Tuple[int, int]:
    print(f"По выбранной категории доступны годы выпуска с {range_min} по {range_max}")
    while True:
        print("Укажите год или диапазон (например: 2020 или 2010-2020)")
        print("ENTER - выбрать весь доступный диапазон")
        year_input = input("Ваш выбор: ").strip()
        if not year_input:
            year_input = f'{range_min}-{range_max}'
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
            print(f'Вы выбрали годы {min_year}-{max_year}')
            return (min_year, max_year)
        except ValueError:
            print("Неверный формат года. Введите год или диапазон, например: 2015 или 2010-2020.")

def showStatistik(results_frequency5: list, results_last: list) -> None:
    """
    Отображает статистику:
    - Топ-5 популярных запросов
    - Топ-5 последних запросов
    Аргументы:
    - results_frequency5: список популярных запросов.
    - results_last: список последних запросов.

    Возвращает:
    - None
    """
    try:
        print("\nТоп-5 популярных запросов:")
        if results_frequency5:
            fm.printStatistikCount(results_frequency5)
        else:
            print("Нет данных по популярным запросам.")

        print("\nТоп-5 последних запросов:")
        if results_last:
            fm.printStatistikLatest(results_last)
        else:
            print("Нет данных по последним запросам.")

    except Exception as e:
        print(f"Ошибка при отображении статистики: {e}")

