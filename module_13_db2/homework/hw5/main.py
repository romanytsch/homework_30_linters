import sqlite3
import random


def generate_test_data(cursor: sqlite3.Cursor, number_of_groups: int) -> None:
    if not 4 <= number_of_groups <= 16:
        return

    # Полная очистка
    cursor.execute('DELETE FROM uefa_draw')
    cursor.execute('DELETE FROM uefa_commands')

    # Расширенные списки команд
    strong = [('Реал', 'Испания'), ('Бавария', 'Германия'), ('Сити', 'Англия'),
              ('ПСЖ', 'Франция'), ('Ливерпуль', 'Англия'), ('Барса', 'Испания'),
              ('Челси', 'Англия'), ('Юве', 'Италия')]

    medium = [('Рома', 'Италия'), ('Севилья', 'Испания'), ('Аякс', 'Голландия'),
              ('Лейпциг', 'Германия'), ('Тотт', 'Англия'), ('Лион', 'Франция'),
              ('Аталанта', 'Италия'), ('Вильярреал', 'Испания'), ('Шахтер', 'Украина'),
              ('Зенит', 'Россия'), ('Ференц', 'Венгрия'), ('Лудогорец', 'Болгария'),
              ('Загреб', 'Хорватия'), ('Славия', 'Чехия'), ('Партизан', 'Сербия'),
              ('Мольде', 'Норвегия'), ('Копенгаген', 'Дания')]

    weak = [('Янг Бойз', 'Швейцария'), ('Олимпиакос', 'Греция'), ('Рубин', 'Россия'),
            ('Краснодар', 'Россия'), ('Селтик', 'Шотландия'), ('Брюгге', 'Бельгия'),
            ('Монако', 'Франция'), ('Антверпен', 'Бельгия')]

    # Берем столько команд, сколько доступно
    s_teams = random.sample(strong, min(number_of_groups, len(strong)))
    m_teams = random.sample(medium, min(number_of_groups * 2, len(medium)))
    w_teams = random.sample(weak, min(number_of_groups, len(weak)))

    # Заполняем команды с правильной нумерацией
    commands_data = []
    team_num = 1

    for name, country in s_teams:
        commands_data.append((team_num, name, country, 'сильная'))
        team_num += 1

    for name, country in m_teams:
        commands_data.append((team_num, name, country, 'средняя'))
        team_num += 1

    for name, country in w_teams:
        commands_data.append((team_num, name, country, 'слабая'))
        team_num += 1

    cursor.executemany(
        'INSERT INTO uefa_commands (command_number, command_name, command_country, command_level) VALUES (?, ?, ?, ?)',
        commands_data
    )

    # Жеребьевка - используем реальное количество команд
    total_strong = len(s_teams)
    total_medium = len(m_teams)
    total_weak = len(w_teams)

    draw_data = []

    for group in range(1, number_of_groups + 1):
        # Сильная команда (если есть)
        if group <= total_strong:
            draw_data.append((group, group))

        # Средние команды (по 2 на группу, сколько хватает)
        m_start = total_strong
        m1 = m_start + (group - 1) * 2 + 1
        m2 = m_start + (group - 1) * 2 + 2
        if m1 <= total_strong + total_medium:
            draw_data.append((m1, group))
        if m2 <= total_strong + total_medium:
            draw_data.append((m2, group))

        # Слабая команда (если есть)
        w_start = total_strong + total_medium
        if group <= total_weak:
            w_num = w_start + (group - 1)
            draw_data.append((w_num, group))

    cursor.executemany(
        'INSERT OR IGNORE INTO uefa_draw (command_number, group_number) VALUES (?, ?)',
        draw_data
    )



if __name__ == '__main__':
    number_of_groups: int = int(input('Введите количество групп (от 4 до 16): '))
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        generate_test_data(cursor, number_of_groups)
        conn.commit()
