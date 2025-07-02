import ui
import mysql_connector as cn
import log_writer as log
import log_sstats as st
import formatter as fm

def doSearchByKeyword(conn) -> None:
    ''' 
    Поиск по ключевому слову
    return: постраничный список фильмов
    '''
    try:
        search_word = input("Ключевое слово:")  
        page_number = 1  # начальная страница
    
        res = cn.searchFilmByTitle(conn, search_word, page_number)
        if res:
            rescount = res[1]
            max_page = (rescount - 1) // 10 + 1
            log.log_request_keyword(search_word, rescount)
            print(f'Найдено фильмов: {rescount} на {max_page} страницах')

            while ui.showNextResultsPage(res[0], page_number, max_page):
                page_number += 1
                res = cn.searchFilmByTitle(conn, search_word, page_number)  # обновляем результаты для новой страницы
        else:
            print("Фильмов по запросу не найдено")
    except Exception as e:
        print(f"Произошла ошибка при поиске по ключевому слову: {e}")


def doSearchByCategory(conn) -> None:
    try:
        categories = cn.getCategoriesWithYears(conn)
        if (category_num := ui.inputCategory(categories)) == 0:
            return
        selected_category = categories[category_num-1]
        search_category = selected_category[0]
        print(f"Выбрана категория: {search_category}")
    
        (min_year, max_year) = ui.inputYears(selected_category[1], selected_category[2])
    
        page_number = 1  # начальная страница
    
        res = cn.searchFilmByCategory(conn, search_category, min_year, max_year, page_number)
        if res:
            rescount = res[1]
            max_page = (rescount - 1) // 10 + 1
            log.log_request_category(search_category, min_year, max_year, rescount)
            print(f'Найдено фильмов: {rescount} на {max_page} страницах')
            while ui.printNextResultsPage(res[0], page_number, max_page):
                page_number += 1
                res = cn.searchFilmByCategory(conn, search_category, min_year, max_year, page_number)
        else:
            print("Фильмов по запросу не найдено")
    except Exception as e:
        print(f"Ошибка при поиске по категории: {e}")

# статистика
def statistik():
    results_frequency5 = st.getFrequencyTop5()
    print("\nТоп-5 по частоте:")
    fm.print_statistik_count(results_frequency5)

    results_last = st.getLatestTop5()
    print("\nТоп-5 по последним поискам:")
    fm.print_statistik_latest(results_last)

def menu(conn):
    while (search_type := ui.main_menu()) != 0:    
        if search_type == 1:
            doSearchByKeyword(conn)
        elif search_type == 2:
            doSearchByCategory(conn)
        elif search_type == 3:
            statistik()
        else:
            print("Неверный выбор, пожалуйста повторите")

def main():
    try:
        conn = cn.connect()
        menu(conn)
        conn.close()
    except Exception as error:
        print('Произошла ошибка. ', error)


if __name__ == '__main__':
    main()