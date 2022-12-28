import sqlite3

from flask import jsonify


def get_result(query: str):
    """
    Принимает SQL запрос и возвращает результат запроса
    :param query: SQL запрос
    :return: Результат SQL запроса
    """
    with sqlite3.connect('netflix.db') as conn:
        conn.row_factory = sqlite3.Row
        result = []

        for item in conn.execute(query).fetchall():
            s = dict(item)

            result.append(s)

        return result


def get_one(query: str):
    """
    Принимает SQL запрос и возвращает результат запроса в единичном виде
    :param query: SQL запрос
    :return: Результат SQL запроса
    """
    with sqlite3.connect('netflix.db') as conn:
        conn.row_factory = sqlite3.Row
        res = conn.execute(query).fetchone()

        if res is None:
            return None
        else:
            return dict(res)


def get_by_cast(name1: str, name2: str):
    """
    Принимает в качестве аргумента имена двух актеров, сохраняет всех актеров из колонки cast
    и возвращает список тех, кто играет с ними в паре больше 2 раз.
    :param name1: Имя первого актера.
    :param name2: Имя второго актера.
    :return: Список актеров, которые играют с искомыми актерами в паре более двух раз
    """

    query = f"""
            SELECT *
            FROM netflix
        """

    cast = []

    result = get_result(query)

    for items in result:
        if name1 in items['cast'] and name2 in items['cast']:

            cast.append(items['cast'])

    cast_actor = ''

    for item in cast:
        cast_actor += f'{item}, '

    cast_partner = cast_actor.split(', ')
    cast_more_than_twice = []

    for item in cast_partner:
        if cast_partner.count(item) > 2:
            if item not in cast_more_than_twice and item != name1 and item != name2:
                cast_more_than_twice.append(item)

    return cast_more_than_twice

# Для проверки 5 шага.
# a = get_by_cast('Jack Black', 'Dustin Hoffman')
# print(a)


def get_by_search(type_src: str, year_src: str, listed_in_src: str):
    """
    Принимает тип картины (фильм или сериал), год выпуска и ее жанр
    и возвращает список названий картин с их описаниями в JSON.
    :param type_src: тип картины.
    :param year_src: год релиза.
    :param listed_in_src: жанр.
    :return: JSON объект со списком найденных картин: название и описание.
    """

    query = f"""
                SELECT *
                FROM netflix
                WHERE type LIKE '{type_src}'
                AND release_year LIKE '{year_src}'
                AND listed_in LIKE '%{listed_in_src}%'
                LIMIT 10
            """

    result = []

    for item in get_result(query):
        result.append(
            {
                "title": item['title'],
                "description": item['description'],
            }
        )

    return jsonify(result)
    # Для проверки 6 шага.
    # return result


# s = get_by_search('Movie', '2001', 'Dramas')
# print(s)
