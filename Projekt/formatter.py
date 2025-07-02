from prettytable import PrettyTable, HRuleStyle
from prettytable.colortable import ColorTable, Themes
from datetime import datetime

def print_table_films(results):
    table = ColorTable(theme=Themes.OCEAN)
    table.field_names = ["Title", "Description", "Year", "Rating"]
    table.align["Title"] = "l"
    table.align["Description"] = "l"
    table.align["Year"] = "r"
    table.align["Rating"] = "r"
    table.max_width = 80
    table.hrules = HRuleStyle.ALL

    for res in results:
        table.add_row([res[0], res[1], res[2], res[3]])

    print(table)

def print_statistik_count(results_frequency5):
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

def print_statistik_latest(results_last):
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


