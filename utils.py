# -*- coding: utf-8 -*-

# - OWN LIBRARIES - #
import config
import sql
from sql import ex_update_user
from sql import ex_update_puzzle_user

# - TELEBOT - #
import telebot
from telebot import types

# - OTHER - #
import datetime
import pytz

###################################################################################################

bot = telebot.TeleBot(config.token)
timezone = pytz.timezone('Europe/Moscow')

keyboards = {
	"main": [["🤔 Загадки", "💰 Клад"],
			["🔎 Добыть $", "🏦 Вложить $"],
			["😈 Украсть $", "👮 Защитить $"],
			["💵 Печатать $", "💡 Поддержка"]],
	
	"puzzles": [["🔴 Клондайк", "🔵 Эльдорадо"],
				["🗃 Архив", "📖 Правила"],
				["📋 Меню"]],
	
	"puzzles_no_team": [["🗃 Архив", "📖 Правила"],
						["📋 Меню"]],
	
	"archive": [["❓ Загадка"],
				["⬆ Вернуться", "📋 Меню"]],
	
	"gain": [["🎊 Халява", "🎲 Игры", "👱 Друзья"],
			["🔠 Задания", "⌛ Конкурсы"],
			["😥 Милостыня", "📋 Меню"]],
	
	"freebie": [["🚰 Кран", "🎁 Бонус", "🔥 Промокод"],
				["⬆ Назад", "📋 Меню"]],
	
	"games": [["🎯 Редкое число", "🎰 Счастливое число"],
				["⬆ Назад", "📋 Меню"]],
	
	"tasks": [["🤖 Ботография", "📢 Каналогия"],
				["⬆ Назад", "📋 Меню"]],
	
	"botography": [["Получить", "⬆ Обратно"]],
	
	"invest": [["🆕 Вклад", "💸 Начисления"],
				["📋 Меню"]],
	
	"steal": [["🔖 Наводка", "💣 Динамит"],
				["📋 Меню"]],
	
	"protect": [["🗄 Сейф", "🔒 Усиление"],
				["🛎 Сигнализация", "📋 Меню"]],
	
	"print": [["📚 Книги", "⛏ Майнинг"],
				["📋 Меню"]],
	
	"treasures": [["📜 Карта", "🗝 Ключ", "📋 Меню"]],
	
	"support": [["📖 Инструкция", "🆘 Помощь"],
				["👱 Рефералы", "🌟 Оценить"],
				["📊 Статистика", "📋 Меню"]],
	
	"rate": [["⭐️", "⭐️ ⭐️", "⭐️ ⭐️ ⭐️"],
			["⭐️ ⭐️ ⭐️ ⭐️", "⭐️ ⭐️ ⭐️ ⭐️ ⭐️"],
			["👍 Поддержать", "Отмена"]]
	
	}

reply_buttons_list = []
for keyboard_index in keyboards:
	for buttons_row in keyboards[keyboard_index]:
		reply_buttons_list += buttons_row

miners_icons = {'M1': '📕', 'M2': '📗', 'M3': '📘', 'M4': '📙', 'M5': '📓', 'M6': '📔'}

###################################################################################################


# noinspection PyPep8Naming
class dot_dict(dict):
	"""dot.notation access to dictionary attributes"""
	__getattr__ = dict.get
	__setattr__ = dict.__setitem__
	__delattr__ = dict.__delitem__
	

def number_morphy(number, form1, form2, form3):
	word = ""
	number = str(number)
	number_buffer = ""

	if len(number) > 2:
		for i in range(-2, 0):
			number_buffer += number[i]
		number = number_buffer

	for i in range(1, 2):
		if number == str(i):
			word = form1

	for i in range(2, 5):
		if number == str(i):
			word = form2

	for i in range(5, 21):
		if number == str(i):
			word = form3

	for n in range(2, 10):
		for i in range(int(str(n) + "1"), int(str(n) + "2")):
			if number == str(i):
				word = form1

		for i in range(int(str(n) + "2"), int(str(n) + "5")):
			if number == str(i):
				word = form2

		for i in range(int(str(n) + "5"), int(str(n + 1) + "1")):
			if number == str(i):
				word = form3

	if number == "0" or number == "00":
		word = form3

	return word


def replace_html(text, replace_back=False):
	text = str(text)
	if replace_back is False:
		if '<' or '>' or '&' in text:
			text = text.replace('&', '&amp;')
			text = text.replace('<', '&lt;')
			text = text.replace('>', '&gt;')
	else:
		if '&lt;' or '&gt;' or '&amp;' in text:
			text = text.replace('&amp;', '&')
			text = text.replace('&lt;', '<')
			text = text.replace('&gt;', '>')
	return text


def get_bad_words():
	with open("bad_words.wpc", "r", encoding='utf-8') as file:
		return file.readlines()


def update_bad_words(word):
	with open("bad_words.wpc", "a", encoding='utf-8') as file:
		file.write("\n" + word)


def today():
	dtime = datetime.datetime.now(tz=timezone).timetuple()
	day = dtime[6]
	return str(day)


def tomorrow():
	dtime = datetime.datetime.now(tz=timezone).timetuple()
	wday = dtime[6] + 1
	if wday == 7:
		wday = 0
	return str(wday)


def yesterday():
	dtime = datetime.datetime.now(tz=timezone).timetuple()
	wday = dtime[6] - 1
	if wday == -1:
		wday = 6
	return str(wday)


def day_before_yesterday():
	dtime = datetime.datetime.now(tz=timezone).timetuple()
	wday = dtime[6] - 1
	if wday == -1:
		wday = 6
	wday -= 1
	if wday == -1:
		wday = 6
	return str(wday)


def just_now_string(minus=None, plus=None):
	dtime = datetime.datetime.now(tz=timezone).timetuple()
	hours = dtime[3]
	minutes = dtime[4]

	if minus is not None:
		minutes -= minus
		if minutes < 0:
			new_minus = -minutes
			hours -= 1
			minutes = 60 - new_minus
			if hours == -1:
				hours = 23

	elif plus is not None:
		minutes += plus
		if minutes > 60:
			minutes -= 60
			hours += 1
			if hours == 24:
				hours = 0

	the_string = '{hours}:{minutes}'.format(hours=hours, minutes=minutes)
	return the_string


def daytime_string():
	dtime = datetime.datetime.now(tz=timezone).timetuple()
	daytime = "{d}//{h}:{m}".format(d=dtime[6], h=dtime[3], m=dtime[4])
	return daytime


def today_date(zeros=True):
	dtime = datetime.datetime.now(tz=timezone).timetuple()
	day = dtime.tm_mday
	month = dtime.tm_mon
	year = dtime.tm_year
	if zeros is True:
		if day < 10:
			day = '0' + str(day)
		if month < 10:
			month = '0' + str(month)
	date_string = "{d}.{m}.{y}".format(d=day, m=month, y=year)
	
	return date_string


def date_time():
	date = today_date()
	time = just_now_string()
	own_date_time = date + '-' + time
	return own_date_time
	

def inline_kb(buttons_list):
	buttons = []
	# Converting list to buttons:
	for row in buttons_list:
		new_row = []
		
		for button in row:
			button_text = button[0]
			button_data = button[1]
			button_url = None
			if len(button) > 2:
				button_url = button[2]
				button_data = None
				
			new_row.append(types.InlineKeyboardButton(text=button_text, callback_data=button_data, url=button_url))
		
		buttons.append(new_row)
	
	keyboard = types.InlineKeyboardMarkup()
	
	for num in range(len(buttons)):
		keyboard.row(*[button for button in buttons[num]])
	
	return keyboard


def inline_button(text, data=None, url=None):
	keyboard = types.InlineKeyboardMarkup()
	keyboard.add(types.InlineKeyboardButton(text=text, callback_data=data, url=url))


def reply_kb(buttons_list):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	for row in buttons_list:
		keyboard.add(*[types.KeyboardButton(button) for button in row])
	return keyboard


def get_menu(kb):
	return reply_kb(keyboards[kb])


###################################################################################################
# PUZZLE EXTRA:
def run_p():
	sql.update_setting('temp_words', None)
	try:
		puzzle_question = sql.get_puzzle()[0][1]
		sql.update_setting("puzzle_checker", "True")
		sql.update_setting("puzzle_counter", int(sql.get_setting("puzzle_counter")) + 1)
		for utc_user in sql.get_utc_users():
			sql.change_utc(uid=utc_user[1], new_tasks_value=utc_user[2] + 1)
			
		keyboard = inline_kb([[["Ответить", None, "http://t.me/TreasureHuntersBot?start=getpuzzle"]]])
		bot.send_message(chat_id=config.channel_id, text="🤔 <b>Загадка дня:</b>\n\n{p}".format(p=puzzle_question), reply_markup=keyboard, parse_mode='HTML')
	except Exception as e:
		bot.send_message(chat_id=42857380, text="Что-то произошло с загадкой. Возможно, они закончились. Проверь /p и попробуй запустить загадку вручную")
		print(e)


def end_p():
	
	sql.update_setting("puzzle_checker", "False")
	
	teams = {"Klondike": {}, "ElDorado": {}}
	stat_teams = {"Klondike": [], "ElDorado": []}
	the_other_answers = []
	bad_words = get_bad_words()
	answers_for_db = []
	puzzle_users = sql.get_puzzle_users()
	
	puzzle = sql.get_puzzle()[0]
	puzzle_id = puzzle[0]
	puzzle_question = puzzle[1]
	puzzle_answer = puzzle[2]
	puzzle_comment = puzzle[3]
	
	###############################################################################################
	# COLLECTING ANSWERS:
	if puzzle_users is not None:
		for user in puzzle_users:
			user_id = user[1]
			answers = user[2]
			coins = user[3]
			team = user[4]
			
			if answers is not None:
				answers = user[2].split(',')
				for answer in answers:
					answers_for_db.append(answer)
					if answer not in bad_words and answer not in the_other_answers:
						the_other_answers.append(answer)
			else:
				answers = []
				
			if puzzle_answer in answers:
				teams[team][user_id] = coins
				
				# STATISTIC #
				stat_teams[team].append(user_id)
			
			else:
				sql.delete_puzzle_user(user_id)
				
		if answers_for_db is not None:
			sql.update_setting('temp_words', ','.join(answers_for_db))
	
	if len(teams['Klondike']) > len(teams['ElDorado']):
		true_team = 'ElDorado'
		false_team = 'Klondike'
		first_string = "🤓 В этот раз победила команда <b>Эльдорадо</b>."
	
	elif len(teams['ElDorado']) > len(teams['Klondike']):
		true_team = 'Klondike'
		false_team = 'ElDorado'
		first_string = "🤓 В этот раз победила команда <b>Клондайк</b>."
	else:
		true_team = None
		false_team = 'Klondike;ElDorado'
		first_string = "😐 В этот раз <b>ничья</b>: ни одна из команд не смогла победить."
	
	#######################################################################################

	if true_team is not None:
		for user_id in teams[true_team]:
			new_coins_balance = teams[true_team][user_id] * 2
			ex_update_user(user_id=user_id, balance=new_coins_balance)
			ex_update_puzzle_user(user_id=user_id, answers=None, coins=new_coins_balance, team=None, has_attempts=3)

	for team in false_team.split(';'):
		for user_id in teams[team]:
			ex_update_user(user_id=user_id, balance=1)
			ex_update_puzzle_user(user_id=user_id, answers=None, coins=1, team=None, has_attempts=3)

	answers_string = ", ".join(the_other_answers)

	msg_text = "{fs}\n\n✅ Правильный ответ: <b>{p}</b>\n<i>{c}</i>\n\n" \
		"💬 Ответы, которые давали игроки:\n<b>{a}</b>".format(fs=first_string,
																	p=puzzle_answer,
																	c=puzzle_comment,
																	a=answers_string)

	while len(msg_text) >= 2998:
		msg_text = ', '.join(msg_text.split(', ')[:-1]) + ' 🙂'
	
	sql.delete_puzzle(puzzle_id=puzzle_id)
	
	keyboard = inline_kb([[["Проверить свой счёт в игре", None, "https://t.me/TreasureHuntersBot?start=getstat_puzzle"]]])
	
	sent_message = bot.send_message(config.channel_id, msg_text, parse_mode='HTML', reply_markup=keyboard)
	sql.update_setting("last_puzzle_link", "https://t.me/t_hunters/" + str(sent_message.message_id))
	
	#
	
	###############################################################################################
	# ARCHIVE:
	sql.add_archive_puzzle(question=puzzle_question, answer=puzzle_answer, comment=puzzle_comment)
	last_archive_puzzle_id = str(sql.get_archive_puzzles()[-1][0])
	
	archive_dict = {**teams['Klondike'], **teams['ElDorado']}
	
	for archive_uid in archive_dict:
		sql.update_archive_user(uid=archive_uid, plus_puzzle_id=last_archive_puzzle_id, current_puzzle_id=None)
	
	#
	
	###############################################################################################
	# STATISTIC:
	sql.create_pstat_table()
	utc_users = sql.get_utc_users()
	# stat_teams = {"Klondike" : [], "ElDorado" : []}
	
	# Collecting all of existing users tasks "days" ===============================================
	all_values_of_tasks_days = []
	for utc_user_tasks in utc_users:
		utc_user_task_value = utc_user_tasks[2]
		all_values_of_tasks_days.append(utc_user_task_value)
	
	all_values_of_tasks_days = list(set(all_values_of_tasks_days))
	all_values_of_tasks_days.sort()
	
	# Creating the library of values for statistic ================================================
	library_of_values = {}
	for ix in all_values_of_tasks_days:
		library_of_values[ix] = {'Klondike': 0, 'ElDorado': 0}
	
	# Counting values for the library =============================================================
	for k_uid in stat_teams['Klondike']:
		k_user_value = sql.get_utc_users(where="user_id", value=k_uid)[0][2]
		library_of_values[k_user_value]['Klondike'] += 1
	
	for e_uid in stat_teams['ElDorado']:
		e_user_value = sql.get_utc_users(where="user_id", value=e_uid)[0][2]
		library_of_values[e_user_value]['ElDorado'] += 1
	
	# Adding statistic to the database ============================================================
	for d in all_values_of_tasks_days:
		sql.add_pstat(puzzle_day=d, klondike=str(library_of_values[d]['Klondike']), eldorado=str(library_of_values[d]['ElDorado']))

###################################################################################################


def try_send_message(chat_id, text, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None, parse_mode=None, disable_notification=None):
	try:
		bot.send_message(chat_id, text, disable_web_page_preview, reply_to_message_id, reply_markup, parse_mode, disable_notification)
	except telebot.apihelper.ApiException:
		pass


def delete_reply_markup(cid, mid):
	try:
		bot.edit_message_reply_markup(chat_id=cid, message_id=mid, reply_markup=None)
	except telebot.apihelper.ApiException:
		pass
	
	
def delete_message(cid, mid, action='edit_text', text='Сообщение недоступно.'):
	try:
		bot.delete_message(chat_id=cid, message_id=mid)
	except telebot.apihelper.ApiException:
		try:
			if action == 'edit_text':
				bot.edit_message_text(text=text, chat_id=cid, message_id=mid)
			elif action == 'delete_keyboard':
				bot.edit_message_reply_markup(chat_id=cid, message_id=mid, reply_markup=None)
		except telebot.apihelper.ApiException:
			pass


def chunks(the_list, n):
	# For item i in a range that is a length of list
	for i in range(0, len(the_list), n):
		yield the_list[i:i+n]


def make_chunks(the_list, n):
	return list(chunks(the_list, n))


def send_rate_message(cid):
	msg_text = "👍 Надеемся, тебе нравится наша игра. Пожалуйста, поддержи нас и помоги нам сделать ее популярнее!"
	bot.send_message(cid, msg_text, reply_markup=get_menu("rate"))


def error_notification(text):
	bot.send_message(config.errors_cid, text)


# NUMBER MORPHY WORDS:
def coins_word(coins):
	return number_morphy(coins, 'монету', 'монеты', 'монет')
