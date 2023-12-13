import psycopg2 as ps
import requests as rq
from bs4 import BeautifulSoup
import folium

db_params = ps.connect(
    database='postgres',
    user='postgres',
    password='psip2023',
    host='localhost',
    port=5432
)

cursor=db_params.cursor()

def add_user_to() -> None:
    """
    add object to list
    :param users_list: list - user list
    :return: None
    """
    name = input('podaj imie ?')
    posts = input('podaj liczbe postow ?')
    nick = input('podaj nick ?')
    city = input('podaj miasto ?')
    sql_query_1 = f"INSERT INTO public.psip_zadanie(city, name, nick, posts) VALUES ('{city}', '{name}', '{nick}', '{posts}');"
    cursor.execute(sql_query_1)
    db_params.commit()


def remove_user_from() -> None:
    """
    remove object from list
    :param users_list: list - user list
    :return: None
    """
    name = input('podaj imie uzytkownika do usuniecia: ')
    sql_query_1 = f"SELECT * FROM public.psip_zadanie WHERE name='{name}';"
    cursor.execute(sql_query_1)
    query_result=cursor.fetchall()
    print('Znaleziono użytkowników:')
    print('0: Usuń wszystkich znalezionych użytkowników')
    for  numerek, user_to_be_removed in enumerate(query_result):
        print(f'{numerek+1}, {user_to_be_removed}')
    numer = int(input(f'wybierz numer użytkownika do usunięcia: '))
    if numer == 0:
        sql_query_2 = f"DELETE * FROM public.psip_zadanie;"
        cursor.execute(sql_query_2)
        db_params.commit()
    else:
        sql_query_2 = f"DELETE FROM public.psip_zadanie WHERE name='{query_result[numer - 1][2]}';"
        cursor.execute(sql_query_2)
        db_params.commit()

def show_users_from()-> None:
    sql_query_1 = f"SELECT * FROM public.psip_zadanie;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    for row in query_result:
        print(f'Twoj znajomy {row[2]} opublikowal {row[4]} postow')
def update_user() -> None:
    nick_of_user = input('podaj nick uzytkownika do modyfikacji')
    sql_query_1 = f"SELECT * FROM public.psip_zadanie WHERE nick='{nick_of_user}';"
    cursor.execute(sql_query_1)
    print('Znaleziono')
    name = input('podaj nowy name: ')
    nick = input('podaj nowy nick: ')
    posts =int(input('podaj liczbe postow: '))
    city= input('podaj city: ')
    sql_query_2 = f"UPDATE public.psip_zadanie SET name='{name}',nick='{nick}', posts='{posts}', city='{city}' WHERE nick='{nick_of_user}';"
    cursor.execute(sql_query_2)
    db_params.commit()

# ==================================== MAPA
def get_coordinates(city:str)->list[float,float]:
    # pobieranie strony internetowej
    adres_url=f'https://pl.wikipedia.org/wiki/{city}'

    response=rq.get(url=adres_url) #zwraca obiekt, wywołany jest status
    response_html=BeautifulSoup(response.text, 'html.parser') #zwraca tekst kodu strony internetowej, zapisany w html

    #pobieranie współrzędnych
    response_html_lat=response_html.select('.latitude')[1].text #kropka oznacza klasę, do ID odwołujemy sie przez #
    response_html_lat=float(response_html_lat.replace(',','.'))

    response_html_long=response_html.select('.longitude')[1].text #kropka oznacza klasę, do ID odwołujemy sie przez #
    response_html_long=float(response_html_long.replace(',','.'))

    return [response_html_lat,response_html_long]
def get_map_one_user()->None:
    city=input('Podaj city uzytkownika: ')
    sql_query_1 = f"SELECT * FROM public.psip_zadanie WHERE city='{city}';"
    cursor.execute(sql_query_1)
    query_result=cursor.fetchall()
    city=get_coordinates(city)
    map = folium.Map(location=city,
                     tiles='OpenStreetMap',
                     zoom_start=14
                     )  # location to miejsce wycentrowania mapy
    for user in query_result:
        folium.Marker(location=city,
                      popup=f'Użytkownik: {user[2]}\n'
                      f'Liczba postow: {user[4]}'
                      ).add_to(map)
    map.save(f'mapaaaaaaa{query_result[0][1]}.html')
def get_map_of()->None:
    map = folium.Map(location=[52.3,21.0],
                     tiles='OpenStreetMap',
                     zoom_start=7
                     )  # location to miejsce wycentrowania mapy
    sql_query_1 = f"SELECT * FROM public.psip_zadanie;"
    cursor.execute(sql_query_1)
    query_result=cursor.fetchall()
    for user in query_result:
        folium.Marker(location=get_coordinates(city=user[1]),
                      popup=f'Użytkownik: {user[2]}\n'
                      f'Liczba postow: {user[4]}'
                      ).add_to(map)
        map.save('mapkaaaaaaaaaa.html')
#========================END OF MAP

def gui() -> None:
    while True:
        print(f'MENU: \n'
              f'0: Zakończ program \n'
              f'1: Wyświetl użytkowników \n'
              f'2: Dodaj użytkownika \n'
              f'3: Usuń użytkownika \n'
              f'4: Modyfikuj użytkownika \n'
              f'5: Wygeneruj mapę z użytkownikiem \n'
              f'6: Wygeneruj mapę z wszystkimi użytkownikami')
        menu_option = input('Podaj funkcję do wywołania')
        print(f'Wybrano funkcję {menu_option}')

        match menu_option:
            case '0':
                print('Kończę pracę')
                break
            case '1':
                print('Wyświetlenie listy użytkowników')
                show_users_from()
            case '2':
                print('Dodawanie użytkownika')
                add_user_to()
            case '3':
                print("Usuwanie użytkownika")
                remove_user_from()
            case '4':
                print('Modyfikuję użytkownika')
                update_user()
            case '5':
                print('Rysuję mapę z użytkownikiem')
                get_map_one_user()
            case '6':
                print('Rysuję mapę z wszystkimi użytkownikami')
                get_map_of()

def pogoda_z(miasto: str):
    url = f"https://danepubliczne.imgw.pl/api/data/synop/station/{miasto}"
    return rq.get(url).json()

class User:
    def __init__(self, city, name, nick, posts):
        self.city = city
        self.name = name
        self.nick = nick
        self.posts = posts
    def pogoda_z(self,miasto: str):
        URL = f'https://danepubliczne.imgw.pl/api/data/synop/station/{miasto}'
        return rq.get(URL).json()

npc_1=User(city='lublin', name='Kinga', nick='kiniaaaaa', posts=785)
npc_2=User(city='warszawa',  name='Wojtek', nick='wowo', posts=1245845)
print(npc_1.city)
print(npc_2.city)

print(npc_1.pogoda_z(npc_1.city))
print(npc_2.pogoda_z(npc_2.city))

