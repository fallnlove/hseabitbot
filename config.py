TOKEN = '' #здесь вставьте токен бота

download_every = 5 # частота скачивания файла в минутах
check_every = 5 # частота проверки в минутах

date_pos = (8, 2) # ряд и столбец ячейки с датой формирования таблицы, !!!!имейти в виду, что при трансформации excel в csv ячейки съезжают и ряд может поменятся
# советую вручную трансормировать файл в csv и проверить ряд и столбец ячейки там

link_list_prog = 'https://ba.hse.ru/base2022' # ссылка на сайт с конкурсными списками

url_pk = '' # ссылка на вашу политику конфиденциальности (бот собирает снилсы, тем самым подпадает под дествия закона о защите ПД)

list_prog = ['BD_Ant_Ist', 'BD_Ant_Fil', 'BD_Akter', 'BD_BI', 'BD_Vostok', 'BD_GGIGT', 'BD_GorPlan', 'BD_GMU', 'BD_Design', 'BD_Egypt', 'BD_Ek', 'BD_ZHur', 'BD_InYaz', 'BD_ITSS', 'BD_IVT', 'BD_IB', 'BD_ISTR', 'BD_Isk', 'BD_Film', 'BD_CMB', 'BD_KogNeir', 'BD_KB', 'BD_Compds', 'BD_Cultural', 'BD_Marketing', 'BD_Math', 'BD_Media', 'BD_ir', 'BD_icef', 'BD_MO', 'BD_MB', 'BD_WE', 'BD_Moda', 'BD_Political', 'BD_Pravo', 'BD_AM', 'BD_AMI', 'BD_Data', 'BD_epa', 'BD_SE', 'BD_Psy', 'BD_AD', 'BD_CPM', 'BD_Art', 'BD_Soc', 'BD_Producer', 'BD_bba', 'BD_Creative', 'BD_Logistics', 'BD_Physics', 'BD_Philology', 'BD_Phil', 'BD_Ling', 'BD_Chem', 'BD_dlawyer', 'BD_digital', 'BD_Stat', 'BD_EA', 'BD_Korea', 'BD_Asia', 'BD_NN_MBBE', 'BD_NN_BI', 'BD_NN_Design', 'BD_NN_InYaz', 'BD_NN_Math', 'BD_NN_AMI', 'BD_NN_SE', 'BD_NN_Philology', 'BD_NN_Ling', 'BD_NN_DM','BD_NN_Ur', 'BD_Perm_Design', 'BD_Perm_InYaz', 'BD_Perm_ISTR', 'BD_Perm_MBBE', 'BD_Perm_Isystems', 'BD_Perm_Ur', 'BD_SPB_MBBE', 'BD_SPB_Vostok', 'BD_SPB_Design', 'BD_SPB_ISTR', 'BD_SPB_Media', 'BD_SPB_PMP', 'BD_SPB_AMI', 'BD_SPB_PADII', 'BD_SPB_Soc', 'BD_SPB_gmu', 'BD_SPB_Physics', 'BD_SPB_Philology', 'BD_SPB_dpl', 'BD_SPB_Ur']
#список с названиями программ

msg_rs = 'dfff'

# Сообщение, которое отправляется пользователю при нажатии /add или /del
add_del_msg = f'''Отправь ссылку на конкурсные списки программы
[Ссылку можно найти на сайте ВШЭ]({link_list_prog})'''



# Сообщение для /start или /help
help_text = f'''Привет!

Этот бот покажет сколько осталось бюджетных мест, количество бви(олимпиадников) и прогнозируемый проходной балл на твоем направлении

Бот отправляет данные 5 раз в день, сразу после того как списки обновляются на сайте НИУ ВШЭ

*Доступные комманды:*
/add - добавить уведомление о программе

/del - отключить уведомление

/set - указать/изменить свой балл ЕГЭ или номер СНИЛС

/pos - узнать свою позицию в списках _(сначала нужно установить балл ЕГЭ или номер СНИЛС)_

Кстати, используя бот, вы соглашаетесь с Политикой конфиденциальности [ссылка]({url_pk})

_Данные бот берет с сайта_ [ВШЭ]({link_list_prog})'''

# Отправляется при нажатии /set
snils_text = f'''Отправь свой снилс в формате XXX-XXX-XXX XX
Если поступаешь по ЕГЭ - можешь отправить сумму баллов

Кстати, напоминаю, используя бот, вы соглашаетесь с Политикой конфиденциальности [ссылка]({url_pk})'''
