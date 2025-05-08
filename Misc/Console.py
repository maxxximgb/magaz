import datetime
import logging
import os
import sys
import time
import types

import werkzeug.security
from flask import Flask

import Database.Engine.Engine as engine
from Database.Classes.Admin import Admin

engine.global_init()
session = engine.create_session()
clear_console = lambda: os.system('cls' if os.name == 'nt' else 'clear')
running = False
main_app = Flask


def parse_args(args: str):
    cmd_args = args.split()
    pos_args = []
    kwargs = {}
    i = 0
    while i < len(cmd_args):
        if cmd_args[i].startswith("--"):
            key = cmd_args[i][2:]
            if i + 1 < len(cmd_args) and not cmd_args[i + 1].startswith("--"):
                kwargs[key] = cmd_args[i + 1]
                i += 1
            else:
                kwargs[key] = True
        else:
            pos_args.append(cmd_args[i])
        i += 1
    return pos_args, kwargs


def verifyPassword(password: str):
    error = list()
    if len(password) < 8:
        error.append('Длина пароля меньше восьми, пожалуйста, придумайте пароль понадежнее.')
    if password.isdigit():
        error.append('В пароле находятся только цифры, пожалуйста, придумайте пароль понадежнее.')
    elif password.isalpha():
        error.append('В пароле находятся только буквы, пожалуйста, придумайте пароль понадежнее.')

    if error:
        print(*error, sep='\n')
        raise AssertionError('Введенный пароль ненадежен.')
    return password


def consoleHelp(*args):
    print('Доступные команды:')
    for (key, (_, title)) in cmds.items():
        print(f'{key}: {title}')


def consoleRegister(*args):
    if not args:
        raise ValueError('Должность пользователя не указана.')

    position = args[0].lower().capitalize()

    if not hasattr(sys.modules[__name__], position):
        raise AssertionError('Указанной вами должности не существует в системе.')

    new = getattr(sys.modules[__name__], position)()
    new.login = input('Введите логин нового пользователя: ')
    new.hashed_password = werkzeug.security.generate_password_hash(
        verifyPassword(input('Введите пароль нового пользователя: ')))
    new.name = input('Введите имя нового пользователя: ')
    new.surname = input('Введите Фамилию нового пользователя: ')
    clear_console()
    session.add(new)
    session.commit()

    print(f'Пользователь {new.name} {new.surname} успешно зарегистрирован.')


def consoleView(*args):
    if not args:
        raise ValueError('Должность пользователя не передана в аргументы.')

    position = args[0].lower().capitalize()
    if not hasattr(sys.modules[__name__], position):
        raise AssertionError(f'Должности {position} не существует в системе.')

    objects = session.query(getattr(sys.modules[__name__], position)).all()
    if not objects:
        raise AssertionError(
            f'Нет пользователей должности {position}. Вы можете зарегистрировать их с помощью команды: "register {position}"')

    for obj in objects:
        print(f'***************************\n'
              f'Пользователь {position} с ID {obj.id}:\n'
              f'Имя - {obj.name}\n'
              f'Фамилия - {obj.surname}\n'
              f'Логин - {obj.login}\n'
              f'***************************')


def shutdown():
    main_app.shutting_down = True
    now = datetime.datetime.now()
    while main_app.requests:
        if main_app.requests:
            print(
                f'Ожидание выполнения активных запросов: {main_app.requests}. Времени прошло: {datetime.datetime.now() - now}')
        time.sleep(1)
    print('Завершение работы.')
    os.abort()


def consoleLook(*args, **kwargs):
    if not args:
        raise ValueError('Должность пользователя не передана в аргументы.')

    position = args[0].lower().capitalize()
    if not hasattr(sys.modules[__name__], position):
        raise AssertionError(f'Должности {position} не существует в системе.')

    objects = session.query(getattr(sys.modules[__name__], position)).all()
    if not objects:
        raise AssertionError(
            f'Нет пользователей должности {position}. Вы можете зарегистрировать их с помощью команды: "register {position}"')

    matches = {}
    for obj in objects:
        for key in kwargs:
            if hasattr(obj, key) and getattr(obj, key).lower() == kwargs[key].lower():
                matches[key] = kwargs[key]

        if matches:
            print("****************************************************************")
            print(f"Пользователь с ID {obj.id}:")

            for key, value in matches.items():
                print(f"{key}: {value} (совпадение)")

            print('\nПолные данные:')
            print(f'Логин: {obj.login}')
            print(f'Имя: {obj.name}')
            print(f'Фамилия: {obj.surname}')
            print("****************************************************************")

    if not matches:
        raise AssertionError('Совпадения не найдены')


cmds = {
    "help": (consoleHelp, "Выводит информацию о доступных командах."),
    "register": (consoleRegister,
                 "Регистрирует пользователя в системе. Принимает должность пользователя в аргументы. Пример: 'register Admin' "),
    "view": (
        consoleView, "Выводит список пользователей должности, которая передается в аргументах. Пример: 'view Admin'"),
    "look": (consoleLook,
             "Ищет пользователя должности, которая передается в аргументах по именнованым аргументам. Пример: 'look Admin --login maximg --name Максим --surname Габисов'"),
    "exit": (shutdown, "Завершает работу приложения"),
    "clear": (clear_console, "Очищает консоль.")
}


def runHook(app, *args, **kwargs):
    global running
    logger = logging.getLogger('werkzeug')
    for handler in logger.handlers:
        logger.removeHandler(handler)
    if not os.path.exists('Logs'):
        os.mkdir('Logs')
    fh = logging.FileHandler('Logs/server.log', encoding='UTF-8')
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
    running = True
    app._run(*args, **kwargs)


def setHook(app: Flask):
    app._run = app.run
    app.requests = 0
    app.shutting_down = False
    app.run = types.MethodType(runHook, app)
    global main_app
    main_app = app


def ConsoleWorker():
    while not running:
        time.sleep(0.1)
    print('Введите help для просмотра доступных команд')
    while True:
        cmd = input('> ')
        args, kwargs = parse_args(cmd)
        if args[0] not in cmds:
            print('Команда не найдена')
            continue
        try:
            cmds[args[0]][0](*args[1:], **kwargs)
        except Exception as e:
            print(f'Ошибка {e.__class__.__name__}:', *e.args)
