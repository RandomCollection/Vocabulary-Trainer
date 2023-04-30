# MODULE:       main.py
# VERSION:      0.3
# DIRECTORY:    <masked>
# DATE:         2023-02-26
# AUTHOR:       RandomCollection
# DESCRIPTION:  See https://github.com/RandomCollection/Vocabulary-Trainer.

# LIBRARIES ############################################################################################################

import os
import random
import requests
import shutil
import webbrowser

from datetime import date, datetime  # TODO: (probably add to buildozer.spec)
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import DictProperty, ObjectProperty, StringProperty
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu

if platform == "android":
	from android.permissions import Permission, request_permissions
	from android.storage import primary_external_storage_path
	request_permissions([Permission.INTERNET, Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

import cfg

from database import Database

# GLOBAL VARIABLES #####################################################################################################

db = Database()


# FUNCTIONS ############################################################################################################

def calc_statistics() -> str:
	words = db.get_number_of_words(language='ES')
	categories = len(db.get_distinct_categories_all())
	levels = chr(10).join([f'{cnt[0]:2}: {cnt[1]:,}' for cnt in db.get_count_of_words_per_level()])
	return (
		f"The vocabulary trainer contains [b]{words:,} {'word' if words == 1 else 'words'}[/b] in [b]{categories:,} "
		f"{'category' if categories == 1 else 'categories'}[/b].\n\n"
		f"The table below gives an overview about the currently existing [b]levels[/b] and corresponding [b]number of "
		f"words[/b] within. Please note that every word appears twice - once for the Spanish to German translation and "
		f"once for the German to Spanish translation.\n\n"
		f"{levels}"
	)


def choose_color(indicator: int, text: str) -> str:
	return text if indicator == 1 else f"[color=FFFFFF]{text}[/color]"


def create_home_text():
	last_date = db.get_constants(column="STATISTIC_LAST_DATE", table="STATISTICS")
	if not last_date:
		return f"{cfg.DICT_TEXT['HOME']} {cfg.DICT_TEXT['HOME_INITIAL']}"
	days = (date.today() - datetime.strptime(last_date, '%Y-%m-%d').date()).days
	if days == 0:
		return f"{cfg.DICT_TEXT['HOME']} {cfg.DICT_TEXT['HOME_DAY_0']}"
	elif days == 1:
		return f"{cfg.DICT_TEXT['HOME']} {cfg.DICT_TEXT['HOME_DAY_1'].format(days)}"
	elif days > 7:
		return f"{cfg.DICT_TEXT['HOME']} {cfg.DICT_TEXT['HOME_DAY_>7'].format(days)}"
	else:
		return f"{cfg.DICT_TEXT['HOME']} {cfg.DICT_TEXT['HOME_DAY_ELSE'].format(days)}"


def create_str_from_list(char: list) -> str:
	return "('" + "','".join(char) + "')"


def set_language(mode: str) -> (str, str):
	if mode == list(cfg.DICT_LANGUAGE.keys())[0]:
		if random.randint(a=0, b=1) == 0:
			return "ES", "DE"
		else:
			return "DE", "ES"
	elif mode == list(cfg.DICT_LANGUAGE.keys())[1]:
		return "ES", "DE"
	elif mode == list(cfg.DICT_LANGUAGE.keys())[2]:
		return "DE", "ES"
	else:
		raise ValueError(f"mode '{mode}' is not valid in function 'language_setting'")


def update_dropdown(caller: any, values: list, callback: callable) -> MDDropdownMenu:
	return MDDropdownMenu(
		caller=caller,
		items=[
			{
				"text": f"{i.capitalize() if type(i) == str else i}",
				"viewclass": "OneLineListItem",
				"height": dp(56),
				"on_release": lambda x=f"{i}": callback(x),
			} for i in values
		],
		width_mult=3,
		max_height=dp(224),
		background_color="#A7FFEB",
	)


# CLASS ################################################################################################################

class VocabularyTrainer(MDApp):
	# Properties
	# Dictionary properties
	dict_language_setting = DictProperty(defaultvalue=cfg.DICT_LANGUAGE)
	# Object properties
	in_class = ObjectProperty(defaultvalue=None)
	# String properties
	label_counter_on = StringProperty(defaultvalue="")
	label_home = StringProperty(defaultvalue="")
	label_sensitivity = StringProperty(defaultvalue="")
	label_sleeper = StringProperty(defaultvalue="")
	label_statistics = StringProperty(defaultvalue="")
	label_streak_current_text = StringProperty(defaultvalue="")
	label_streak_current_number = StringProperty(defaultvalue="")
	label_streak_best_text = StringProperty(defaultvalue="")
	label_streak_best_number = StringProperty(defaultvalue="")
	label_words_current_text = StringProperty(defaultvalue="")
	label_words_current_number = StringProperty(defaultvalue="")
	label_words_total_text = StringProperty(defaultvalue="")
	label_words_total_number = StringProperty(defaultvalue="")

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		# Theme
		self.theme_cls.primary_palette = "DeepPurple"
		self.theme_cls.primary_hue = "900"
		self.theme_cls.secondary_palette = "Teal"
		self.theme_cls.secondary_hue = "200"
		self.theme_cls.theme_style = "Light"
		# Builder
		self.screen = Builder.load_file("main.kv")
		# Variables
		self.language = list(cfg.DICT_LANGUAGE.keys())[1]
		self.language_in = "ES"
		self.language_out = "DE"
		self.words_in = None
		self.words_out = None
		self.z = None
		self.category_distinct_all = create_str_from_list(char=db.get_distinct_categories_all())
		self.level_distinct_all = create_str_from_list(char=db.get_distinct_levels_all())
		self.category_distinct = create_str_from_list(char=db.get_distinct_categories(level=self.level_distinct_all))
		self.level_distinct = create_str_from_list(char=db.get_distinct_levels(category=self.category_distinct_all))
		self.levels_in = None
		self.level_current = None
		self.status = 0
		# Settings
		self.counter_on = db.get_constants(column="SETTING_COUNTER_ON", table="SETTINGS")
		self.sensitivity = db.get_constants(column="SETTING_SENSITIVITY", table="SETTINGS")
		self.sleeper = db.get_constants(column="SETTING_SLEEPER", table="SETTINGS")
		# Statistics
		self.streak_current_number = 0
		self.streak_best_number = db.get_constants(column='STATISTIC_STREAK_BEST', table='STATISTICS')
		self.words_current_number = 0
		self.words_total_number = db.get_constants(column='STATISTIC_WORDS_TOTAL', table='STATISTICS')
		# String properties
		self.label_counter_on = f"{cfg.SETTING_COUNTER_ON_VALUES[0] if db.get_constants(column='SETTING_COUNTER_ON', table='SETTINGS') == 1 else cfg.SETTING_COUNTER_ON_VALUES[1]}"
		self.label_home = create_home_text()
		self.label_sensitivity = f"{db.get_constants(column='SETTING_SENSITIVITY', table='SETTINGS')}"
		self.label_sleeper = f"{db.get_constants(column='SETTING_SLEEPER', table='SETTINGS')}s"
		self.label_statistics = calc_statistics()
		self.label_streak_current_text = choose_color(indicator=self.counter_on, text="Current streak:")
		self.label_streak_current_number = choose_color(indicator=self.counter_on, text=f"{self.streak_current_number:,}")
		self.label_streak_best_text = choose_color(indicator=self.counter_on, text="Best streak:")
		self.label_streak_best_number = choose_color(indicator=self.counter_on, text=f"{self.streak_best_number:,}")
		self.label_words_current_text = choose_color(indicator=self.counter_on, text="Words current:")
		self.label_words_current_number = choose_color(indicator=self.counter_on, text=f"{self.words_current_number:,}")
		self.label_words_total_text = choose_color(indicator=self.counter_on, text="Words total:")
		self.label_words_total_number = choose_color(indicator=self.counter_on, text=f"{self.words_total_number:,}")
		# Dropdowns
		self.menu_category = self.menu_category = update_dropdown(
			caller=self.screen.ids.button_category,
			values=["All"] + db.get_distinct_categories(level=self.level_distinct),
			callback=self.callback_category
		)
		self.menu_counter_on = update_dropdown(
			caller=self.screen.ids.button_counter_on,
			values=cfg.SETTING_COUNTER_ON_VALUES,
			callback=self.callback_counter_on
		)
		self.menu_level = update_dropdown(
			caller=self.screen.ids.button_level,
			values=["All"] + db.get_distinct_levels(category=self.category_distinct),
			callback=self.callback_level
		)
		self.menu_sensitivity = update_dropdown(
			caller=self.screen.ids.button_sensitivity,
			values=cfg.SETTING_SENSITIVITY_VALUES,
			callback=self.callback_sensitivity
		)
		self.menu_sleeper = update_dropdown(
			caller=self.screen.ids.button_sleeper,
			values=cfg.SETTING_SLEEPER_VALUES,
			callback=self.callback_sleeper
		)

	def on_start(self):
		self.root.ids.label_how_to.text = cfg.LABEL_HOW_TO
		self.root.ids.label_settings.text = cfg.LABEL_SETTINGS
		self.root.ids.text.text = cfg.LABEL_TEXT
		self.root.ids.label_update.text = cfg.LABEL_UPDATE
		self.root.ids.label_word_in.text = cfg.LABEL_WORD_IN
		# TODO: add all static labels here

	# TODO: check if there is something like on_end and what i could put in there

	# SCREEN "START" ---------------------------------------------------------------------------------------------------

	def solve(self):
		if self.status == 0:
			self.root.ids.label_word_out.text = cfg.LABEL_START
		else:
			self.root.ids.label_word_out.text = self.words_out[self.z]

	def check(self):
		if self.status == 0:
			self.status = 1
			self.root.ids.please_translate.text = cfg.LABEL_TRANSLATE
			self.next()
			self.root.ids.label_button_check.text = cfg.LABEL_BUTTON_CHECK
		else:
			if self.root.in_class.text == "":
				self.root.ids.label_word_out.text = cfg.LABEL_ENTER_TRANSLATION
			elif self.root.in_class.text in self.words_out[self.z].split("/"):
				self.root.ids.label_word_out.text = cfg.LABEL_SOLUTION_CORRECT
				Clock.schedule_once(lambda _: self.sleeper_correct(), self.sleeper)
				db.increase_level(level=self.level_current, word=self.words_in[self.z])
				self.streak_current_number += 1
				self.streak_best_number = max(self.streak_current_number, self.streak_best_number)
			else:
				self.root.ids.label_word_out.text = cfg.LABEL_SOLUTION_INCORRECT
				db.decrease_level(level=self.level_current, word=self.words_in[self.z])
				self.streak_current_number = 0
			self.label_statistics = calc_statistics()
			# TODO: below counts words also only when 'check' is pressed but no word actually entered
			self.words_current_number += 1
			self.words_total_number += 1
			self.label_streak_current_number = choose_color(indicator=self.counter_on, text=f"{self.streak_current_number:,}")
			self.label_streak_best_number = choose_color(indicator=self.counter_on, text=f"{self.streak_best_number:,}")
			self.label_words_current_number = choose_color(indicator=self.counter_on, text=f"{self.words_current_number:,}")
			self.label_words_total_number = choose_color(indicator=self.counter_on, text=f"{self.words_total_number:,}")
			db.update_counters(streak_best=self.streak_best_number, words_total=self.words_total_number)
			db.update_constants_date(value=date.today())

	def next(self):
		if self.status == 0:
			self.root.ids.label_word_out.text = cfg.LABEL_START
			return None
		self.language_in, self.language_out = set_language(mode=self.language)
		self.words_in, self.words_out, self.levels_in = db.get_data(
				language=self.language_in,
				category=self.category_distinct,
				level=self.level_distinct
			)
		if not self.words_in and self.language == "Random":
			self.language_in, self.language_out = self.language_out, self.language_in
			self.words_in, self.words_out, self.levels_in = db.get_data(
				language=self.language_in,
				category=self.category_distinct,
				level=self.level_distinct
			)
			if not self.words_in:
				self.reset_filters()
				return None
		elif not self.words_in:
			self.reset_filters()
			return None
		weights = [self.sensitivity ** ((-1) * level) for level in self.levels_in]
		self.z = self.words_in.index(random.choices(population=self.words_in, weights=weights)[0])
		self.root.ids.label_word_in.text = self.words_in[self.z]
		self.root.in_class.text = ""
		self.root.ids.label_word_out.text = ""
		self.level_current = db.get_level(word=self.words_in[self.z])
		self.update_menus()

	# SCREEN "STATISTICS" ----------------------------------------------------------------------------------------------

	def reset_statistics(self):
		db.reset(category=self.category_distinct, level=self.level_distinct)
		self.reset()

	# SCREEN "VOCABULARY" ----------------------------------------------------------------------------------------------

	def show_vocabulary(self):
		self.columns_data = [
				("Word", dp(30)),
				("Translation", dp(80)),
				("#Level", dp(10)),
			]
		self.row_data = ["0", "0", "0"]
		self.data_tables = MDDataTable(
			pos_hint={"center_y": 0.5, "center_x": 0.5},
			size_hint=(0.9, 0.6),
			use_pagination=True,
			rows_num=10,
			column_data=self.columns_data,
			row_data=self.row_data,
		)
		self.root.ids.data_layout.add_widget(self.data_tables)
		x = db.get_data(
			language=self.language_in,
			category=self.category_distinct,
			level=self.level_distinct
		)
		self.row_data = [(f"{x[0][i]}", f"{x[1][i]}", f"{x[2][i]}") for i in range(len(x[0]))]
		self.data_tables.update_row_data(self.data_tables, self.row_data)

	# SCREEN "SETTINGS" ------------------------------------------------------------------------------------------------

	def reset_counters(self):
		self.streak_current_number = 0
		self.streak_best_number = 0
		self.words_current_number = 0
		self.words_total_number = 0
		self.label_streak_current_number = choose_color(indicator=self.counter_on, text=f"{self.streak_current_number:,}")
		self.label_streak_best_number = choose_color(indicator=self.counter_on, text=f"{self.streak_best_number:,}")
		self.label_words_current_number = choose_color(indicator=self.counter_on, text=f"{self.words_current_number:,}")
		self.label_words_total_number = choose_color(indicator=self.counter_on, text=f"{self.words_total_number:,}")
		self.root.ids.label_reset_status.text = cfg.LABEL_RESET
		db.update_counters(streak_best=self.streak_best_number, words_total=self.words_total_number)

	# SCREEN "UPDATE" --------------------------------------------------------------------------------------------------

	def import_db(self):
		try:
			r = requests.get(url=cfg.URL_DATABASE, timeout=5)
			open(cfg.NAME_DATABASE, "wb").write(r.content)
			self.root.ids.label_update_status.text = cfg.LABEL_IMPORT_1
			self.reset()
		except Exception as e:
			self.root.ids.label_update_status.text = cfg.LABEL_IMPORT_0.format(e=str(e))

	def export_db(self):
		try:
			shutil.copy(cfg.NAME_DATABASE, os.path.join(primary_external_storage_path(), "Download", cfg.NAME_DATABASE))
			self.root.ids.label_update_status.text = cfg.LABEL_IMPORT_1
		except Exception as e:
			self.root.ids.label_update_status.text = cfg.LABEL_EXPORT_0(e=str(e))

	# SCREEN "ABOUT" ---------------------------------------------------------------------------------------------------

	@staticmethod
	def open_url(url: str):
		webbrowser.open(url=url)

	# OTHER ------------------------------------------------------------------------------------------------------------

	def callback_category(self, instance):
		if instance == "All":
			self.category_distinct = create_str_from_list(char=db.get_distinct_categories_all())
		else:
			self.category_distinct = f"('{instance}')"
		self.root.ids.label_category.text = instance.capitalize()
		self.update_menus()
		self.menu_category.dismiss()

	def callback_counter_on(self, instance):
		self.counter_on = 1 if instance == "On" else 0
		self.root.ids.label_counter_on.text = instance
		db.update_constants(value=self.counter_on, column="SETTING_COUNTER_ON", table="SETTINGS")
		self.label_streak_current_text = choose_color(indicator=self.counter_on, text="Current streak:")
		self.label_streak_current_number = choose_color(indicator=self.counter_on, text=f"{self.streak_current_number:,}")
		self.label_streak_best_text = choose_color(indicator=self.counter_on, text="Best streak:")
		self.label_streak_best_number = choose_color(indicator=self.counter_on, text=f"{self.streak_best_number:,}")
		self.label_words_current_text = choose_color(indicator=self.counter_on, text="Words current:")
		self.label_words_current_number = choose_color(indicator=self.counter_on, text=f"{self.words_current_number:,}")
		self.label_words_total_text = choose_color(indicator=self.counter_on, text="Words total:")
		self.label_words_total_number = choose_color(indicator=self.counter_on, text=f"{self.words_total_number:,}")
		self.menu_counter_on.dismiss()

	def callback_language(self, instance):
		self.language = [key for key, value in cfg.DICT_LANGUAGE.items() if value == instance.icon][0]

	def callback_level(self, instance):
		if instance == "All":
			self.level_distinct = create_str_from_list(char=db.get_distinct_levels_all())
		else:
			self.level_distinct = f"({instance})"
		self.root.ids.label_level.text = instance
		self.update_menus()
		self.menu_level.dismiss()

	def callback_sensitivity(self, instance):
		self.sensitivity = int(instance)
		self.root.ids.label_sensitivity.text = instance
		db.update_constants(value=self.sensitivity, column="SETTING_SENSITIVITY", table="SETTINGS")
		self.menu_sensitivity.dismiss()

	def callback_sleeper(self, instance):
		self.sleeper = int(instance)
		self.root.ids.label_sleeper.text = f"{instance}s"
		db.update_constants(value=self.sleeper, column="SETTING_SLEEPER", table="SETTINGS")
		self.menu_sleeper.dismiss()

	def reset(self):
		self.label_statistics = calc_statistics()
		self.category_distinct = create_str_from_list(char=db.get_distinct_categories_all())
		self.level_distinct = create_str_from_list(char=db.get_distinct_levels_all())
		self.root.ids.please_translate.text = ""
		self.root.ids.label_button_check.text = "START"
		self.root.ids.label_category.text = 'All'
		self.root.ids.label_level.text = 'All'
		self.update_menus()
		self.language = "ES -> DE"
		self.status = 0

	def reset_filters(self):
		self.root.ids.label_word_in.text = cfg.DICT_TEXT["NO_WORDS"]
		self.reset()

	def sleeper_correct(self):
		self.root.ids.label_word_out.text = ""
		self.next()

	def update_menus(self):
		self.menu_level = update_dropdown(
			caller=self.screen.ids.button_level,
			values=["All"] + db.get_distinct_levels(category=self.category_distinct),
			callback=self.callback_level
		)
		self.menu_category = update_dropdown(
			caller=self.screen.ids.button_category,
			values=["All"] + db.get_distinct_categories(level=self.level_distinct),
			callback=self.callback_category
		)

	# BUILD ------------------------------------------------------------------------------------------------------------

	def build(self):
		return self.screen


if __name__ == '__main__':
	VocabularyTrainer().run()
