
from bs4 import BeautifulSoup
import requests
import folium
nazwy_miejscowosci = ['Opoczno', 'Lublin', 'Gdańsk']

from dane import users_list

def get_coordinates_of(city:str)->list[float,float]:
    # pobranie strony internetowej
    adres_URL = f'https://pl.wikipedia.org/wiki/{city}'
    response = requests.get(url=adres_URL)
    response_html = BeautifulSoup(response.text, 'html.parser')

    # pobranie współrzędnych z treści strony internetowej
    response_html_latitude = response_html.select('.latitude')[1].text  # . ponieważ class
    response_html_latitude = float(response_html_latitude.replace(',','.'))
    response_html_longitude = response_html.select('.longitude')[1].text  # . ponieważ class
    response_html_longitude = float(response_html_longitude.replace(',','.'))

    return [response_html_latitude, response_html_longitude]


# for item in nazwy_miejscowosci:
#     print(get_coordinates_of(item))


# zwrócić mapę z pinezką odnoszącą się do użytkownika podanego z klawiatury
def get_map_one_user(user:str)->None:
    city = get_coordinates_of(user['city'])
    map = folium.Map(
        location=city,    # gdzie mapa ma byc wycentrowana
        tiles="OpenStreetMap",
        zoom_start=15,
    )
    folium.Marker(
        location=city,
        popup=f'Tu rządzi: {user["name"]},'
              f'postów: {user["posts"]}'
    ).add_to(map)
    map.save(f'mapka_{user["name"]}.html')


### RYSOWANIE MAPY
def get_map_of(users: list[dict,dict])->None:
    map = folium.Map(
        location=[52.3, 21.0],    # gdzie mapa ma byc wycentrowana
        tiles="OpenStreetMap",
        zoom_start=7,
    )
    for user in users:
        folium.Marker(
            location=get_coordinates_of(city=user['city']),
            popup=f'Użytkownik: {user["name"]} \n'
                  f'Liczba postów: {user["posts"]}'
        ).add_to(map)
    map.save('mapka.html')
get_map_of(users_list)
# =========================================== END OF MAP ELEMENT ==============================================
def add_user_to(users_list:list) -> None:
    """
    add object to list
    :param users_list: list - user list
    :return: None
    """
    name = input('podaj imie ?')
    posts = input('podaj liczbe postow ?')
    city = input('podaj miasto ?')
    users_list.append({"name": name, "posts": posts, "city": city})


def remove_user_from(users_list: list) -> None:
    """
    remove object from list
    :param users_list: list - user list
    :return: None
    """
    tmp_list = []
    name = input('podaj imie uzytkownika do usuniecia: ')
    for user in users_list:
        if user["name"] == name:
            tmp_list.append(user)
    print('Znaleziono użytkowników:')
    print('0: Usuń wszystkich znalezionych użytkowników')
    for  numerek, user_to_be_removed in enumerate(tmp_list):
        print(f'{numerek+1}, {user_to_be_removed}')
    numer = int(input(f'wybierz numer użytkownika do usunięcia: '))
    if numer == 0:
        for user in tmp_list:
            users_list.remove(user)
    else:
        users_list.remove(tmp_list[numer-1])


def show_users_from(users_list:list)-> None:
   for user in users_list:
      print(f'Twój znajomy {user["name"]} dodał {user["posts"]}')

def update_user(users_list: list[dict,dict]) -> None:
    nick_of_user = input('podaj nick uzytkownika do modyfikacji')
    print(nick_of_user)
    for user in users_list:
        if user['nick'] == nick_of_user:
            print('Znaleziono!!')
            user['name'] = input('podaj nowe imie')
            user['nick'] = input('podaj nowa ksywke')
            user['posts'] = int(input('podaj liczbe postow: '))
            user['city'] = input('podaj miasto')

# ==================================== MAPA
import requests
from bs4 import BeautifulSoup
import folium
from dane import users_list
def get_coordinates(city:str)->list[float,float]:
    # pobieranie strony internetowej
    adres_url=f'https://pl.wikipedia.org/wiki/{city}'

    response=requests.get(url=adres_url) #zwraca obiekt, wywołany jest status
    response_html=BeautifulSoup(response.text, 'html.parser') #zwraca tekst kodu strony internetowej, zapisany w html

    #pobieranie współrzędnych
    response_html_lat=response_html.select('.latitude')[1].text #kropka oznacza klasę, do ID odwołujemy sie przez #
    response_html_lat=float(response_html_lat.replace(',','.'))

    response_html_long=response_html.select('.longitude')[1].text #kropka oznacza klasę, do ID odwołujemy sie przez #
    response_html_long=float(response_html_long.replace(',','.'))

    return [response_html_lat,response_html_long]
def get_map_one_user(user:str)->None:
    city=get_coordinates(user['city'])
    map = folium.Map(location=city,
                     tiles='OpenStreetMap',
                     zoom_start=14
                     )  # location to miejsce wycentrowania mapy
    folium.Marker(location=city,
                  popup=f'Użytkownik: {user["name"]}\n'
                  f'Liczba postow: {user['posts']}'
                  ).add_to(map)
    map.save(f'mapka_{user['name']}.html')
def get_map_of(users:list[dict,dict])->None:
    map = folium.Map(location=[52.3,21.0],
                     tiles='OpenStreetMap',
                     zoom_start=7
                     )  # location to miejsce wycentrowania mapy
    for user in users_list:
        folium.Marker(location=get_coordinates(city=user['city']),
                      popup=f'Użytkownik: {user["name"]}\n'
                      f'Liczba postow: {user['posts']}'
                      ).add_to(map)
        map.save('mapka.html')
#========================END OF MAP

def gui(users_list:list) -> None:
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
                show_users_from(users_list)
            case '2':
                print('Dodawanie użytkownika')
                add_user_to(users_list)
            case '3':
                print("Usuwanie użytkownika")
                remove_user_from(users_list)
            case '4':
                print('Modyfikuję użytkownika')
                update_user(users_list)
            case '5':
                print('Rysuję mapę z użytkownikiem')
                user = input("Podaj nazwę użytkownika do modyfikacji")
                for item in users_list:
                    if item['name'] == user:
                        get_map_one_user(item)
            case '6':
                print('Rysuję mapę z wszystkimi użytkownikami')
                get_map_of(users_list)

def pogoda_z(miasto: str):
    url = f"https://danepubliczne.imgw.pl/api/data/synop/station/{miasto}"
    return requests.get(url).json()
