# MODULE:       main.py
# VERSION:      0.4
# DIRECTORY:    <masked>
# DATE:         2023-06-04
# AUTHOR:       RandomCollection
# DESCRIPTION:  See https://github.com/RandomCollection/Vocabulary-Trainer.

# LIBRARIES ############################################################################################################
#
import os
# import pandas as pd
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
		pass

	def check(self):
		pass

	def next(self):
		pass

	# SCREEN "STATISTICS" ----------------------------------------------------------------------------------------------

	def reset_statistics(self):
		pass

	# SCREEN "VOCABULARY" ----------------------------------------------------------------------------------------------

	def show_vocabulary(self):
		pass

	# SCREEN "SETTINGS" ------------------------------------------------------------------------------------------------

	def reset_counters(self):
		pass

	# SCREEN "UPDATE" --------------------------------------------------------------------------------------------------

	def import_db(self):
		pass

	def export_db(self):
		pass

	# SCREEN "ABOUT" ---------------------------------------------------------------------------------------------------

	@staticmethod
	def open_url(url: str):
		pass

	# OTHER ------------------------------------------------------------------------------------------------------------

	def callback_category(self, instance):
		pass

	def callback_counter_on(self, instance):
		pass

	def callback_language(self, instance):
		pass

	def callback_level(self, instance):
		pass

	def callback_sensitivity(self, instance):
		pass

	def callback_sleeper(self, instance):
		pass

	def choose_color_wrapper_number(self):
		pass

	def choose_color_wrapper_text(self):
		pass

	def on_start(self):
		pass

	def reset(self):
		pass

	def reset_filters(self):
		pass
	
	def sleeper_correct(self):
		pass

	def update_dropdowns(self):
		pass

	def update_statistics(self):
		pass

	# BUILD ------------------------------------------------------------------------------------------------------------

	def build(self):
		return self.screen


# MAIN #################################################################################################################

if __name__ == '__main__':
	VocabularyTrainer().run()

# END ##################################################################################################################
