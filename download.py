import pandas
import asyncio
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import config, db_functions

async def download_files():
    for prg in config.list_prog:
        info = await db_functions.get_program_info(prg)
        url = info[3]
        file_obj = requests.get(url) # здесь скрипт скачивает файл по ссылке
        # Предполагается, что списки будут excel-файлами, если это не так
        # то вам нужно будет изменить следующие две строки
        sheet = pandas.read_excel(file_obj.content, 'TDSheet')
        sheet.to_csv(f'files/{prg}.csv', encoding='utf-8', index=False)

if __name__ == '__main__':
    sched = AsyncIOScheduler()
    sched.add_job(download_files, 'cron', minute = f'0-59/{config.download_every}')
    sched.start()
    asyncio.get_event_loop().run_forever()