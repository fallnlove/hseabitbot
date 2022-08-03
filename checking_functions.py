import pandas

import bothse, config, db_functions

async def checking():
    list_upd = []
    for program in config.list_prog:
        sheet = pandas.read_csv(f'csvfiles/{program}.csv')
        info = await db_functions.get_program_info(program)
        if info[1] != sheet.iat[config.date_pos]: # Ячейка config.date_pos хранит дату сформаированного файла
            # и елси она не совпадает с последней сохраненной датой
            # то мы добавляем программу в список на обновление
            list_upd.append(program)
    await db_functions.update(list_upd)
    await bothse.sending(list_upd)

async def issnils(snils):
    try:
        snils = snils.strip()
        list = snils.replace('-', '').replace(' ', '')
        return len(snils) == 14 and list[0].isdigit()
    except:
        return False