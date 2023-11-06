def add_user_to(users_list:list) -> None:
    """
    add object to list
    :param users_list: list - user list
    :return: None
    """
    name = input('podaj imie ?')
    posts = input('podaj liczbe postow ?')
    users_list.append({"name": name, "posts": posts})


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


def gui(users_list:list) -> None:
    while True:
        print(f'MENU: \n'
              f'0: Zakończ program \n'
              f'1: Wyświetl użytkowników \n'
              f'2: Dodaj użytkownika \n'
              f'3: Usuń użytkownika \n'
              f'4: Modyfikuj użytkownika \n'
              )
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
                print('to będzie zrobione')  # TODO add this function to my_functions