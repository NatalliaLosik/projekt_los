import pymysql
config = { 
'host': 'ich-db.edu.itcareerhub.de',
'user': 'ich1', 
'password': 'password', 
'database': 'sakila'
}

def connect():
    connection = pymysql.connect(**config)
    return connection

#Поиск по названию
def searchFilmByTitle(connection, search_word: str, page_number: int):
    with connection.cursor() as cursor:
        offset_value = (page_number - 1) * 10
        # запрос кол-ва фильмов соответствующих типу поиска
        query_count = "select count(*) from film where title like concat('%%', %s, '%%')"
        cursor.execute(query_count, (search_word,))
        rowcount = int(cursor.fetchone()[0])
        # запрос следующих 10 фильмов соответствующих типу поиска      
        query_films = '''
	   select title,  description, release_year, rating
           from film
           where title like concat('%%', %s, '%%')
           limit 10 offset %s
        '''
        cursor.execute(query_films, (search_word, offset_value))
        res = list(cursor.fetchall())
    return (res, rowcount)

#Поиск по категории
def searchFilmByCategory(connection, search_category: str, min_year: int, max_year: int, page_number: int):
    with connection.cursor() as cursor:
        offset_value = (page_number - 1) * 10
        query_count = '''select count(*) from film
            inner join film_category as fc on fc.film_id = film.film_id
    		inner join category as c on c.category_id = fc.category_id
    		where c.name = %s and release_year between %s and %s'''
        cursor.execute(query_count, (search_category, min_year, max_year))
        rowcount = int(cursor.fetchone()[0])
        # запрос следующих 10 фильмов соответствующих типу поиска      
        query_films = '''select title,  description, release_year, rating from film
            inner join film_category as fc on fc.film_id = film.film_id
    		inner join category as c on c.category_id = fc.category_id
    		where c.name = %s and release_year between %s and %s limit 10 offset %s'''
        cursor.execute(query_films, (search_category, min_year, max_year, offset_value))
        res = list(cursor.fetchall())
    return (res, rowcount)

# Список категорий
def getCategoriesWithYears(connection):
    with connection.cursor() as cursor:
        query = '''select c.name, min(f.release_year) as min_year, max(f.release_year) as max_year
        from film f
        inner join film_category fc on fc.film_id = f.film_id
        inner join category c on c.category_id = fc.category_id
        group by c.name'''
        cursor.execute(query)
        res = list(cursor.fetchall())
    return res
