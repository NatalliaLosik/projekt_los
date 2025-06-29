import mysql_connector as cn
import log_writer as log
import log_sstats as st
import re

def doSearchByKeyword():
    search_word = input("Ключевое слово:")  
    page_number = 1  # начальная страница

    res = cn.searchFilmByTitle(search_word, page_number)
    if res:
        rescount = res[1]
        max_page = (rescount - 1) // 10 + 1
        log.log_request_keyword(search_word, rescount)
        print(f'Найдено фильмов: {rescount} на {max_page} страницах')
    
        while True:
            print(f"\n--- Страница {page_number} ---")
            for row in res[0]:
                print(row[0])
    
            if page_number >= max_page:
                print("Вы достигли последней страницы.")
                break
    
            page_next = input("Перейти на следующую страницу? YES/NO: ").strip().upper()
            if page_next != "YES":
                break
    
            page_number += 1
            res = cn.searchFilmByTitle(search_word, page_number)  # обновляем результаты для новой страницы
    else:
        print("Фильмов по запросу не найдено")

def printCategories(categories):
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

def inputCategory(categories):
    while True:
        try:
            print("Доступные категории: ")
            printCategories(categories)
            search_category_num = int(input("Введите номер категории или 0 для выхода: "))
        except:
            search_category_num = -1
        if search_category_num == 0:
            return 0
        if search_category_num < 1 or search_category_num > len(categories):
            print("Неверное значение, попробуйте еще раз.")
        else:
            break
    return search_category_num
    
def inputYears(range_min, range_max):
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
            break
        except ValueError:
            print("Неверный формат года. Введите год или диапазон, например: 2015 или 2010-2020.")
    return (min_year, max_year)

def doSearchByCategory():
    categories = cn.getCategoriesWithYears()
    category_num = inputCategory(categories)
    if category_num == 0:
        return
    selected_category = categories[category_num-1]
    search_category = selected_category[0]
    print(f"Выбрана категория: {search_category}")

    (min_year, max_year) = inputYears(selected_category[1], selected_category[2])

    page_number = 1  # начальная страница

    res = cn.searchFilmByCategory(search_category, min_year, max_year, page_number)
    if res:
        rescount = res[1]
        max_page = (rescount - 1) // 10 + 1
        log.log_request_category(search_category, min_year, max_year, rescount)
        print(f'Найдено фильмов: {rescount} на {max_page} страницах')
    
        while True:
            print(f"\n--- Страница {page_number} ---")
            for row in res[0]:
                print(row[0])
    
            if page_number >= max_page:
                print("Вы достигли последней страницы.")
                break
    
            page_next = input("Перейти на следующую страницу? YES/NO: ").strip().upper()
            if page_next != "YES":
                break
    
            page_number += 1
            res = cn.searchFilmByCategory(search_category, min_year, max_year, page_number)
    else:
        print("Фильмов по запросу не найдено")
# статистика
def statistik():
    results_frequency5 = st.getFrequencyTop5()
    print("\nТоп-5 по частоте:")
    for res in results_frequency5:
        if res["search_type"] == "keyword":
            print(f'{res["num"]}. keyword: {res["keyword"]} — {res["count"]} раз(а)')
        else:       
            print(f'{res["num"]}. category: {res["category"]} ({res["min_year"]}..{res["max_year"]}) — {res["count"]} раз(а)')

    results_last = st.getLatestTop5()
    print("\nТоп-5 по последним поискам:")
    for res in results_last:
        if res["search_type"] == "keyword":
            print(f'{res["num"]}. keyword: {res["keyword"]} — {res["timestamp"]}')
        else:       
            print(f'{res["num"]}. category: {res["category"]} ({res["min_year"]}..{res["max_year"]}) — {res["timestamp"]}')

while True:
    search_type = int(input("Введите:\n 1 - если поиск по ключевому слову\n 2 - если поиск по жанру и диапазону годов выпуска\n 3 - Посмотреть популярные или последние запросы \n-----\n 0 - выход\nВаш выбор:"))
    if search_type == 1:
        doSearchByKeyword()
    elif search_type == 2:
        doSearchByCategory()
    elif search_type == 3:
        statistik()
    elif search_type == 0:
        break;
    else:
        print("Неверный выбор, пожалуйста повторите")
        