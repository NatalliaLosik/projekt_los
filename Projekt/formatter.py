from prettytable import PrettyTable, HRuleStyle
from prettytable.colortable import ColorTable, Themes
from datetime import datetime
from typing import List, Tuple



def printTableFilms(results: List[Tuple[str, str, int, float]]) -> None:
    """
    Выводит таблицу с фильмами в формате:
    Title | Description | Year | Rating

    Аргументы:
    - results: список кортежей, содержащих информацию о фильмах:
        (название, описание, год, рейтинг)

    Возвращает:
    - None
    """
    try:
        if not results:
            print("Нет фильмов для отображения.")
            return

        table = ColorTable(theme=Themes.OCEAN)
        table.field_names = ["Title", "Description", "Year", "Rating"]
        table.align["Title"] = "l"
        table.align["Description"] = "l"
        table.align["Year"] = "r"
        table.align["Rating"] = "r"
        table.max_width = 80
        table.hrules = HRuleStyle.ALL

        for res in results:
            if len(res) < 4:
                print(f"Некорректные данные: {res}")
                continue
            table.add_row([res[0], res[1], res[2], res[3]])

        print(table)

    except Exception as e:
        print(f"Ошибка при выводе таблицы фильмов: {e}")

def printStatistikCount(results_frequency5):
    table = PrettyTable()
    table.field_names = ["#", "Type", "Query", "Count"]
    table.align["Query"] = "l"
    table.align["Count"] = "r"

    for res in results_frequency5:
        if res["search_type"] == "keyword":
            query = res["keyword"]
        else:       
            query = f'{res["category"]} ({res["min_year"]}..{res["max_year"]})'
        table.add_row([res["num"], res["search_type"], query, res["count"]])

    print(table)

def printStatistikLatest(results_last):
    table = PrettyTable()
    table.field_names = ["#", "Type", "Query", "DateTime"]
    table.align["Query"] = "l"

    for res in results_last:
        if res["search_type"] == "keyword":
            query = res["keyword"]
        else:       
            query = f'{res["category"]} ({res["min_year"]}..{res["max_year"]})'
        table.add_row([res["num"], res["search_type"], query, res["timestamp"].strftime("%Y-%m-%d %H:%M:%S")])

    print(table)


