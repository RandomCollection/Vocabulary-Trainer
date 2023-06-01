# MODULE:       main.py
# VERSION:      0.4
# DIRECTORY:    <masked>
# DATE:         2023-06-04
# AUTHOR:       RandomCollection
# DESCRIPTION:  See https://github.com/RandomCollection/Vocabulary-Trainer.

# LIBRARIES ############################################################################################################

import os
import pandas as pd
import random
import shutil
import webbrowser

from datetime import date, datetime
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

def choose_color(indicator: int, text: str) -> str:
	return text if indicator == 1 else f"[color=FAFAFA]{text}[/color]"


def create_label_home() -> str:
	last_date = db.get_constants(column="STATISTIC_LAST_DATE", table="STATISTICS")
	if not last_date:
		return f"{cfg.LABEL_HOME['HOME']} {cfg.LABEL_HOME['HOME_INITIAL']}"
	days = (date.today() - datetime.strptime(last_date, '%Y-%m-%d').date()).days
	if days == 0:
		return f"{cfg.LABEL_HOME['HOME']} {cfg.LABEL_HOME['HOME_DAY_0']}"
	elif days == 1:
		return f"{cfg.LABEL_HOME['HOME']} {cfg.LABEL_HOME['HOME_DAY_1'].format(days=days)}"
	elif days > 7:
		return f"{cfg.LABEL_HOME['HOME']} {cfg.LABEL_HOME['HOME_DAY_>7'].format(days=days)}"
	else:
		return f"{cfg.LABEL_HOME['HOME']} {cfg.LABEL_HOME['HOME_DAY_ELSE'].format(days=days)}"


def create_str_from_list(char: list) -> str:
	return "('" + "','".join(char) + "')"


def create_table_statistics() -> str:
	return chr(10).join([f'{cnt[0]:2}: {cnt[1]:,}' for cnt in db.get_count_of_words_per_level()])


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
	# PROPERTIES -------------------------------------------------------------------------------------------------------

	# Dictionary properties
	dict_language = DictProperty(defaultvalue=cfg.DICT_LANGUAGE)
	# Object properties
	input = ObjectProperty(defaultvalue=None)
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
	table_statistics = StringProperty(defaultvalue="")

	# INIT -------------------------------------------------------------------------------------------------------------

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
		self.distinct_category_all = create_str_from_list(char=db.get_distinct_categories_all())
		self.distinct_level_all = create_str_from_list(char=db.get_distinct_levels_all())
		self.distinct_category = create_str_from_list(char=db.get_distinct_categories(level=self.distinct_level_all))
		self.distinct_level = create_str_from_list(char=db.get_distinct_levels(category=self.distinct_category_all))
		self.language = list(cfg.DICT_LANGUAGE.keys())[1]
		self.language_in = "ES"
		self.language_out = "DE"
		self.level_current = None
		self.levels_in = None
		self.status = 0
		self.words_in = None
		self.words_out = None
		self.z = None
		# Settings
		self.setting_counter_on = db.get_constants(column="SETTING_COUNTER_ON", table="SETTINGS")
		self.setting_sensitivity = db.get_constants(column="SETTING_SENSITIVITY", table="SETTINGS")
		self.setting_sleeper = db.get_constants(column="SETTING_SLEEPER", table="SETTINGS")
		# Statistics
		self.statistic_number_of_words = db.get_number_of_words(language='ES')
		self.statistic_number_of_categories = len(db.get_distinct_categories_all())
		self.statistic_streak_current = 0
		self.statistic_streak_best = db.get_constants(column='STATISTIC_STREAK_BEST', table='STATISTICS')
		self.statistic_words_current = 0
		self.statistic_words_total = db.get_constants(column='STATISTIC_WORDS_TOTAL', table='STATISTICS')
		# String properties
		self.label_counter_on = (
			cfg.SETTING_COUNTER_ON_VALUES[0] if db.get_constants(column='SETTING_COUNTER_ON', table='SETTINGS') == 1
			else cfg.SETTING_COUNTER_ON_VALUES[1]
		)
		self.label_home = create_label_home()
		self.label_sensitivity = str(db.get_constants(column='SETTING_SENSITIVITY', table='SETTINGS'))
		self.label_sleeper = f"{db.get_constants(column='SETTING_SLEEPER', table='SETTINGS')}s"
		self.label_statistics = cfg.LABEL_STATISTICS.format(
			words=f"{self.statistic_number_of_words:,}",
			words_adj=f"{'word' if self.statistic_number_of_words == 1 else 'words'}",
			categories=f"{self.statistic_number_of_categories:,}",
			categories_adj=f"{'category' if self.statistic_number_of_categories == 1 else 'categories'}"
		)
		self.choose_color_wrapper_text()
		self.choose_color_wrapper_number()
		self.table_statistics = create_table_statistics()
		# Datatables
		self.columns_data = [("Word", dp(30)), ("Translation", dp(80)), ("Level", dp(10))]
		self.row_data = ["0", "0", "0"] * 40
		self.data_tables = MDDataTable(
			pos_hint={"center_y": 0.5, "center_x": 0.5},
			size_hint=(0.9, 0.6),
			use_pagination=True,
			pagination_menu_pos="auto",
			rows_num=10,
			column_data=self.columns_data,
			row_data=self.row_data,
		)
		# Dropdowns
		self.dropdown_category = update_dropdown(
			caller=self.screen.ids.button_category,
			values=["All"] + db.get_distinct_categories(level=self.distinct_level),
			callback=self.callback_category
		)
		self.dropdown_counter_on = update_dropdown(
			caller=self.screen.ids.button_counter_on,
			values=cfg.SETTING_COUNTER_ON_VALUES,
			callback=self.callback_counter_on
		)
		self.dropdown_level = update_dropdown(
			caller=self.screen.ids.button_level,
			values=["All"] + db.get_distinct_levels(category=self.distinct_category),
			callback=self.callback_level
		)
		self.dropdown_sensitivity = update_dropdown(
			caller=self.screen.ids.button_sensitivity,
			values=cfg.SETTING_SENSITIVITY_VALUES,
			callback=self.callback_sensitivity
		)
		self.dropdown_sleeper = update_dropdown(
			caller=self.screen.ids.button_sleeper,
			values=cfg.SETTING_SLEEPER_VALUES,
			callback=self.callback_sleeper
		)

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
			if self.root.input.text == "":
				self.root.ids.label_word_out.text = cfg.LABEL_ENTER_TRANSLATION
			elif self.root.input.text in self.words_out[self.z].split("/"):
				self.root.ids.label_word_out.text = cfg.LABEL_SOLUTION_CORRECT
				Clock.schedule_once(lambda _: self.sleeper_correct(), self.setting_sleeper)
				db.increase_level(level=self.level_current, word=self.words_in[self.z])
				self.statistic_streak_current += 1
				self.statistic_streak_best = max(self.statistic_streak_current, self.statistic_streak_best)
				self.update_statistics()
			else:
				self.root.ids.label_word_out.text = cfg.LABEL_SOLUTION_INCORRECT
				db.decrease_level(level=self.level_current, word=self.words_in[self.z])
				self.statistic_streak_current = 0
				self.update_statistics()

	def next(self):
		if self.status == 0:
			self.root.ids.label_word_out.text = cfg.LABEL_START
			return None
		self.language_in, self.language_out = set_language(mode=self.language)
		self.words_in, self.words_out, self.levels_in = db.get_data(
				language=self.language_in,
				category=self.distinct_category,
				level=self.distinct_level
			)
		if not self.words_in and self.language == "Random":
			self.language_in, self.language_out = self.language_out, self.language_in
			self.words_in, self.words_out, self.levels_in = db.get_data(
				language=self.language_in,
				category=self.distinct_category,
				level=self.distinct_level
			)
			if not self.words_in:
				self.reset_filters()
				return None
		elif not self.words_in:
			self.reset_filters()
			return None
		weights = [self.setting_sensitivity ** ((-1) * level) for level in self.levels_in]
		self.z = self.words_in.index(random.choices(population=self.words_in, weights=weights)[0])
		self.root.ids.label_word_in.text = self.words_in[self.z]
		self.root.input.text = ""
		self.root.ids.label_word_out.text = ""
		self.level_current = db.get_level(word=self.words_in[self.z])
		self.update_dropdowns()

	# SCREEN "STATISTICS" ----------------------------------------------------------------------------------------------

	def reset_statistics(self):
		db.reset(category=self.distinct_category, level=self.distinct_level)
		self.reset()

	# SCREEN "VOCABULARY" ----------------------------------------------------------------------------------------------

	def show_vocabulary(self):
		data = db.get_data(
			language=self.language_in,
			category=self.distinct_category,
			level=self.distinct_level
		)
		self.row_data = [(f"{data[0][i]}", f"{data[1][i]}", f"{data[2][i]}") for i in range(len(data[0]))]
		self.data_tables.update_row_data(self.data_tables, self.row_data)

	# SCREEN "SETTINGS" ------------------------------------------------------------------------------------------------

	def reset_counters(self):
		self.statistic_streak_current = 0
		self.statistic_streak_best = 0
		self.statistic_words_current = 0
		self.statistic_words_total = 0
		self.choose_color_wrapper_number()
		self.root.ids.label_reset_status.text = cfg.LABEL_RESET
		db.update_counters(streak_best=self.statistic_streak_best, words_total=self.statistic_words_total)

	# SCREEN "UPDATE" --------------------------------------------------------------------------------------------------

	def import_db(self):
		self.root.ids.label_update_status.text = cfg.LABEL_IMPORT_START
		try:
			(
				pd.read_excel(io=cfg.URL_DATABASE)
				.merge(
					right=pd.read_sql(sql="SELECT * FROM VOCABULARY", con=db.con),
					how="left",
					on="WORD",
					suffixes=("_NEW", "_OLD")
				)
				.filter(items=["WORD", "TRANSLATION_NEW", "CATEGORY_NEW", "LANGUAGE_NEW", "LEVEL_OLD"])
				.rename(columns=lambda x: x.split("_")[0])
				.assign(LEVEL=lambda df: df["LEVEL"].fillna(0).astype(int))
				.to_sql(name="VOCABULARY", con=db.con, if_exists="replace", index=False)
			)
			db.con.commit()
			self.reset()
			self.root.ids.label_update_status.text = cfg.LABEL_IMPORT_1
		except Exception as e:
			self.root.ids.label_update_status.text = cfg.LABEL_IMPORT_0.format(e=str(e))

	def export_db(self):
		self.root.ids.label_update_status.text = cfg.LABEL_EXPORT_START
		try:
			shutil.copy(cfg.NAME_DATABASE, os.path.join(primary_external_storage_path(), "Download", cfg.NAME_DATABASE))
			self.root.ids.label_update_status.text = cfg.LABEL_EXPORT_1
		except Exception as e:
			self.root.ids.label_update_status.text = cfg.LABEL_EXPORT_0(e=str(e))

	# SCREEN "ABOUT" ---------------------------------------------------------------------------------------------------

	@staticmethod
	def open_url(url: str):
		webbrowser.open(url=url)

	# OTHER ------------------------------------------------------------------------------------------------------------

	def callback_category(self, instance):
		if instance == "All":
			self.distinct_category = create_str_from_list(char=db.get_distinct_categories_all())
		else:
			self.distinct_category = f"('{instance}')"
		self.root.ids.label_category.text = instance.capitalize()
		self.update_dropdowns()
		self.dropdown_category.dismiss()

	def callback_counter_on(self, instance):
		self.setting_counter_on = 1 if instance == "On" else 0
		self.root.ids.label_counter_on.text = instance
		db.update_constants(value=self.setting_counter_on, column="SETTING_COUNTER_ON", table="SETTINGS")
		self.choose_color_wrapper_text()
		self.choose_color_wrapper_number()
		self.dropdown_counter_on.dismiss()

	def callback_language(self, instance):
		self.language = [key for key, value in cfg.DICT_LANGUAGE.items() if value == instance.icon][0]

	def callback_level(self, instance):
		if instance == "All":
			self.distinct_level = create_str_from_list(char=db.get_distinct_levels_all())
		else:
			self.distinct_level = f"({instance})"
		self.root.ids.label_level.text = instance
		self.update_dropdowns()
		self.dropdown_level.dismiss()

	def callback_sensitivity(self, instance):
		self.setting_sensitivity = int(instance)
		self.root.ids.label_sensitivity.text = instance
		db.update_constants(value=self.setting_sensitivity, column="SETTING_SENSITIVITY", table="SETTINGS")
		self.dropdown_sensitivity.dismiss()

	def callback_sleeper(self, instance):
		self.setting_sleeper = int(instance)
		self.root.ids.label_sleeper.text = f"{instance}s"
		db.update_constants(value=self.setting_sleeper, column="SETTING_SLEEPER", table="SETTINGS")
		self.dropdown_sleeper.dismiss()

	def choose_color_wrapper_number(self):
		self.label_streak_current_number = choose_color(
			indicator=self.setting_counter_on, text=f"{self.statistic_streak_current:,}"
		)
		self.label_streak_best_number = choose_color(
			indicator=self.setting_counter_on, text=f"{self.statistic_streak_best:,}"
		)
		self.label_words_current_number = choose_color(
			indicator=self.setting_counter_on, text=f"{self.statistic_words_current:,}"
		)
		self.label_words_total_number = choose_color(
			indicator=self.setting_counter_on, text=f"{self.statistic_words_total:,}"
		)

	def choose_color_wrapper_text(self):
		self.label_streak_current_text = choose_color(
			indicator=self.setting_counter_on, text=cfg.LABEL_COUNTER_STREAK_CURRENT
		)
		self.label_streak_best_text = choose_color(
			indicator=self.setting_counter_on, text=cfg.LABEL_COUNTER_STREAK_BEST
		)
		self.label_words_current_text = choose_color(
			indicator=self.setting_counter_on, text=cfg.LABEL_COUNTER_WORDS_CURRENT
		)
		self.label_words_total_text = choose_color(
			indicator=self.setting_counter_on, text=cfg.LABEL_COUNTER_WORDS_TOTAL
		)

	def on_start(self):
		# Labels in 'main.kv' with 'text: ""' that should show text not equal to "" on start
		self.root.ids.label_word_in.text = cfg.LABEL_START
		self.root.ids.text.text = cfg.LABEL_TEXT
		self.root.ids.label_settings.text = cfg.LABEL_SETTINGS
		self.root.ids.label_how_to.text = cfg.LABEL_HOW_TO
		self.root.ids.label_update.text = cfg.LABEL_UPDATE
		self.root.ids.label_about.text = cfg.LABEL_ABOUT
		# MDDataTable
		self.root.ids.data_layout.add_widget(self.data_tables)

	def reset(self):
		self.distinct_category = create_str_from_list(char=db.get_distinct_categories_all())
		self.distinct_level = create_str_from_list(char=db.get_distinct_levels_all())
		self.root.ids.please_translate.text = ""
		self.root.ids.label_word_in.text = cfg.LABEL_START
		self.root.ids.label_word_out.text = ""
		self.root.ids.label_button_check.text = "START"
		self.root.ids.label_category.text = 'All'
		self.root.ids.label_level.text = 'All'
		self.update_dropdowns()
		self.language = "ES -> DE"
		self.status = 0
		self.table_statistics = create_table_statistics()

	def reset_filters(self):
		self.root.ids.label_word_in.text = cfg.LABEL_NO_WORDS
		self.reset()

	def sleeper_correct(self):
		self.root.ids.label_word_out.text = ""
		self.next()

	def update_dropdowns(self):
		self.dropdown_level = update_dropdown(
			caller=self.screen.ids.button_level,
			values=["All"] + db.get_distinct_levels(category=self.distinct_category),
			callback=self.callback_level
		)
		self.dropdown_category = update_dropdown(
			caller=self.screen.ids.button_category,
			values=["All"] + db.get_distinct_categories(level=self.distinct_level),
			callback=self.callback_category
		)

	def update_statistics(self):
		self.table_statistics = create_table_statistics()
		self.statistic_words_current += 1
		self.statistic_words_total += 1
		self.choose_color_wrapper_number()
		db.update_counters(streak_best=self.statistic_streak_best, words_total=self.statistic_words_total)  # TODO: could this go to 'on_end'?
		db.update_constants_date(value=date.today())  # TODO: could this go to 'on_end'?

	# BUILD ------------------------------------------------------------------------------------------------------------

	def build(self):
		return self.screen


# MAIN #################################################################################################################

if __name__ == '__main__':
	VocabularyTrainer().run()

# END ##################################################################################################################
