import sqlite3
import pandas

async def update(list_upd):
    for program in list_upd:
        sheet = pandas.read_csv(f'csvfiles/{program}.csv')
        await update_program_info(program, sheet.iat[8, 2]) # Сохраняем последнюю дату обновления
        info = await get_program_info(program)
        i = 16
        counter_bvi = 0
        counter_cel = 0
        counter_ldnr = 0
        counter_os = 0
        counter_sogl_bvi = 0
        last_bud = '-'
        delta = int(info[7])
        while i != sheet.shape[0]:
            if sheet.iat[i, 22 + delta] == 'К' or sheet.iat[i, 32 + delta] == 'Да':
                i += 1
                continue
            if sheet.iat[i, 4] == 'Да':
                counter_bvi += 1
                if sheet.iat[i, 26 + delta] == 'Да':
                    counter_sogl_bvi += 1
            elif sheet.iat[i, 6] == 'Да':
                counter_os += 1
            elif sheet.iat[i, 10] == 'Да':
                counter_ldnr += 1
            elif sheet.iat[i, 8] == 'Да':
                counter_cel += 1
            i += 1
        mest_bud = int(sheet.iat[5, 10])
        mest_bud -= min(int(info[5]), counter_cel) + min(int(info[4]), counter_os) + min(int(info[6]), counter_ldnr) + counter_bvi
        mest_bud = max(mest_bud, int(0.25 * int(sheet.iat[5, 10])))
        mest_bud += int(sheet.iat[6, 10])
        i = 16
        counter_bud = 0
        while i != sheet.shape[0] and counter_bud != mest_bud:
            if sheet.iat[i, 22 + delta] == 'К' or sheet.iat[i, 32 + delta] == 'Да':
                i += 1
                continue
            if sheet.iat[i, 4] == 'Нет' and sheet.iat[i, 6] == 'Нет' and sheet.iat[i, 8] == 'Нет' and sheet.iat[i, 10] == 'Нет':
                last_bud = sheet.iat[i, 20 + delta]
                counter_bud += 1
            i += 1
        if last_bud == None:
            last_bud = 'минимальный балл'
        name_prog = sheet.iat[0, 2]
        name_prog += f' {info[8]}'
        msg_text = f'''*{name_prog}*
_{sheet.iat[8, 2]}_
_Бюджетных мест:_ *{sheet.iat[5, 10]}*
_Квазибюджетных мест:_ *{sheet.iat[6, 10]}*
_Подано заявлений БВИ:_ *{counter_bvi}* (подали согласие: *{counter_sogl_bvi}*)
_Подано заявлений по особой квоте(не более {info[4]}):_ *{counter_os}*
_Подано заявлений по специальной квоте(не более {info[6]}):_ *{counter_ldnr}*
_Подано заявлений по целевой квоте(не более {info[5]}):_ *{counter_cel}*
_Проходной балл на бюджет/квазибюджет:_ *{last_bud}*'''
        conn = sqlite3.connect('programs.db')
        cursor = conn.cursor()
        cursor.execute('Update prog set msg = ? where name = ?', (msg_text, program, ))
        conn.commit()
        cursor.close()

async def get_pos(id, prog):
    try:
        info = await get_program_info(prog)
        i = 16
        conn = sqlite3.connect('users_id.db')
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM main_table WHERE id= ?', (str(id),))
        snils = cursor.fetchall()[0][1]
        cursor.close()
        sheet = pandas.read_csv(f'csvfiles/{prog}.csv')
        delta = int(info[7])
        while i != sheet.shape[0]:
            if sheet.iat[i, 22 + delta] == 'К' or sheet.iat[i, 32 + delta] == 'Да':
                i += 1
                continue
            if sheet.iat[i, 2] == snils or (str(sheet.iat[i, 20 + delta]) == snils and sheet.iat[i, 4] == 'Нет' and sheet.iat[i, 6] == 'Нет' and sheet.iat[i, 8] == 'Нет' and sheet.iat[i, 10] == 'Нет'):
                return i - 15
            i += 1
    except:
        return None

async def add_user(program, id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    conn1 = sqlite3.connect('programs.db')
    cursor1 = conn1.cursor()
    cursor.execute(f"INSERT INTO {program} (id) VALUES (?)", (str(id),))
    cursor1.execute('SELECT * from prog where name = ?', (program,))
    conn.commit()
    cursor.close()
    msg = cursor1.fetchall()[0][2]
    cursor1.close()
    pos = await get_pos(id, program)
    if pos is None:
        return msg
    else:
        return f'{msg}\n_Место в списке:_ *{pos}*\n'

async def del_user(program, id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE from {program} where id = {id}")
    conn.commit()
    cursor.close()

async def get_users_by_program(program):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"""SELECT * from {program}""")
    info = cursor.fetchall()
    cursor.close()
    return info

async def get_program_info(program):
    conn = sqlite3.connect('programs.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * from prog where name = ?', (program,))
    info = cursor.fetchall()[0]
    cursor.close()
    return info

#функция получает на вход ссылку и передает всю информацию о программе, если вы добавляете программу другим способом, то нужно изменить эту функцию
async def get_program_info_by_url(url):
    conn = sqlite3.connect('programs.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * from prog where url = ?', (url,))
    info = cursor.fetchall()[0]
    cursor.close()
    return info

async def get_snils(id):
    conn = sqlite3.connect('users_id.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM main_table WHERE id= ?', (str(id),))
    info = cursor.fetchall()
    cursor.close()
    return info

async def add_snils(number, id):
    conn = sqlite3.connect('users_id.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO main_table (id, snils) VALUES (?, ?)", (str(id), number,))
    except:
        cursor.execute("UPDATE main_table set snils = ? where id = ?", (number, str(id),))
    conn.commit()
    cursor.close()

async def update_program_info(prog, text):
    conn = sqlite3.connect('programs.db')
    cursor = conn.cursor()
    cursor.execute(f'Update prog set last_update = ? where name = "{prog}"', (text,))
    conn.commit()
    cursor.close()