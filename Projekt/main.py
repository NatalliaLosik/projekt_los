import ui
import mysql_connector as cn
import log_writer as log
import log_sstats as st
import settings

def doSearchByKeyword(conn, collection) -> None:
    ''' 
    Поиск по ключевому слову
    return: постраничный список фильмов
    '''
    try:
        search_word = input("Ключевое слово:")  
        page_number = 1  # начальная страница
    
        res = cn.searchFilmByTitle(conn, search_word, page_number)
        if res:
            films, rescount = res
            max_page = (rescount - 1) // 10 + 1

            try:
                log.logRequestKeyword(collection, search_word, rescount)
            except Exception as log_error:
                print(f"Ошибка логгирования запроса: {log_error}")

            print(f'Найдено фильмов: {rescount}') #на {max_page} страницах')

            while ui.showNextResultsPage(res[0], page_number, max_page):
                page_number += 1
                res = cn.searchFilmByTitle(conn, search_word, page_number)  # обновляем результаты для новой страницы
        else:
            print("Фильмов по запросу не найдено")
    except Exception as e:
        print(f"Произошла ошибка при поиске по ключевому слову: {e}")


def doSearchByCategory(conn, collection) -> None:
    ''' 
    Поиск по категории и годам выпуска
    return: постраничный список фильмов
    '''
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
            log.logRequestCategory(collection, search_category, min_year, max_year, rescount)
            print(f'Найдено фильмов: {rescount} на {max_page} страницах')
            while ui.showNextResultsPage(res[0], page_number, max_page):
                page_number += 1
                res = cn.searchFilmByCategory(conn, search_category, min_year, max_year, page_number)
        else:
            print("Фильмов по запросу не найдено")
    except Exception as e:
        print(f"Ошибка при поиске по категории: {e}")

# статистика
def statistik(collection) -> None:
    '''
    Отображает статистику запросов:
    - Топ-5 самых частых ключевых слов
    - Топ-5 последних ключевых слов
    '''
    try:
        results_frequency5 = st.getFrequencyTop5(collection)
        results_last = st.getLatestTop5(collection)
        ui.showStatistik(results_frequency5, results_last)
    except Exception as e:
        print(f"Ошибка при отображении статистики: {e}")

def menu(conn, collection) -> None:
    '''
    Главное меню приложения. Обрабатывает выбор пользователя
    Возвращает:
    - None
    '''
    try:
        while (search_type := ui.mainMenu()) != 0:    
            if search_type == 1:
                doSearchByKeyword(conn, collection)
            elif search_type == 2:
                doSearchByCategory(conn, collection)
            elif search_type == 3:
                statistik(collection)
            else:
                print("Неверный выбор, пожалуйста повторите")
    except Exception as e:
        print(f"Критическая ошибка в главном меню: {e}")
def main():
    try:
        conn = cn.connect(settings.DATABASE_MYSQL_W)
        collection = log.collection(settings.DATABASE_MONGO_W) 
        menu(conn, collection)
        conn.close()
    except Exception as error:
        print('Произошла ошибка. ', error)


if __name__ == '__main__':
    main()