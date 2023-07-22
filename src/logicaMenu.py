import os
# Borrar consola segun S.O.


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def printMenu(menuOptions):
    for key in menuOptions.keys():
        print(key, '--', menuOptions[key])

def logicaMenu(
    nombrePrograma: str,
    opcionesMenu: 'dict[int, str]',
    opcionUna: 'function',
    opcionDos: 'function'
):
    cls()
    print(f'{nombrePrograma} de Docbook Article | Grupo 12. SSL 2023.')
    while(True):
        printMenu(opcionesMenu)
        option = ''
        try:
            option = int(input('Ingrese la opción: '))
        except:
            cls()
            print('Opción inválida. Por favor, ingrese una de las opciones disponibles...')
        cls()
        if option == 1:
            opcionUna()
        elif option == 2:
            opcionDos()
        elif (option == 3):
            print('Ejecucion finalizada.')
            exit()
        else:
            print('Opción incorrecta. Por favor, ingresar un número del 1 al 3.')
