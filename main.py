# MODULE:       main.py
# VERSION:      1.0
# DIRECTORY:    <masked>
# DATE:         2022-11-27
# AUTHOR:       RandomCollection
# DESCRIPTION:  See https://github.com/RandomCollection/Vocabulary-Trainer.

# LIBRARIES ############################################################################################################

import os
import random
import requests
import shutil
import webbrowser

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu

if platform == "android":
	from android.permissions import Permission, request_permissions
	request_permissions([Permission.INTERNET, Permission.ACCESS_NETWORK_STATE, Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
	from android.storage import primary_external_storage_path

from database import Database

# CONSTANTS ############################################################################################################

DICT_LANGUAGE = {
	"Random": "arrow-left-right",
	"ES -> DE": "arrow-right",
	"ES <- DE": "arrow-left",
}

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


def create_str_from_list(char: list) -> str:
	return "('" + "','".join(char) + "')"


def set_language(mode: str) -> (str, str):
	if mode == list(DICT_LANGUAGE.keys())[0]:
		if random.randint(a=0, b=1) == 0:
			return "ES", "DE"
		else:
			return "DE", "ES"
	elif mode == list(DICT_LANGUAGE.keys())[1]:
		return "ES", "DE"
	elif mode == list(DICT_LANGUAGE.keys())[2]:
		return "DE", "ES"
	else:
		raise ValueError(f"mode '{mode}' is not valid in function 'language_setting'")


# CLASS ################################################################################################################

class VocabularyTrainer(MDApp):

	in_class = ObjectProperty(None)
	dict_language_setting = DICT_LANGUAGE.copy()

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
		self.language = list(DICT_LANGUAGE.keys())[1]
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
		self.sensitivity = 2
		# Dropdowns
		self.menu_level = self.update_level()
		self.menu_category = self.update_category()
		self.menu_sensitivity = self.update_sensitivity()

	# SCREEN "START" ---------------------------------------------------------------------------------------------------

	def check(self):
		try:
			word_out_used = self.words_out[self.z]
		except TypeError:
			self.root.ids.label_word_out.text = "Please click the [i]NEXT[/i] button to start"
		else:
			if self.root.in_class.text == "":
				self.root.ids.label_word_out.text = "Please enter a translation into the text field"
			elif self.root.in_class.text == word_out_used:
				self.root.ids.label_word_out.text = "[color=238823]Correct =)[/color]"
				db.increase_level(level=self.level_current, word=self.words_in[self.z])
			else:
				self.root.ids.label_word_out.text = "[color=D2222D]Incorrect =([/color]"
				db.decrease_level(level=self.level_current, word=self.words_in[self.z])
			self.label_statistics = calc_statistics()

	def next(self):
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

	def solve(self):
		try:
			self.root.ids.label_word_out.text = self.words_out[self.z]
		except (IndexError, TypeError):
			self.root.ids.label_word_out.text = "Please click the [i]NEXT[/i] button to start"

	def callback_category(self, instance):
		if instance == "All":
			self.category_distinct = create_str_from_list(char=db.get_distinct_categories_all())
		else:
			self.category_distinct = f"('{instance.upper()}')"
		self.root.ids.label_category.text = instance.capitalize()
		self.update_menus()
		self.menu_category.dismiss()

	def callback_language(self, instance):
		self.language = [key for key, value in DICT_LANGUAGE.items() if value == instance.icon][0]

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
		self.menu_sensitivity.dismiss()

	def reset_filters(self):
		self.root.ids.label_word_in.text = (
			"There are no more words with the current configuration. Back to [i]All[/i] and [i]ES -> DE[/i]."
		)
		self.category_distinct = create_str_from_list(char=db.get_distinct_categories_all())
		self.root.ids.label_category.text = 'All'
		self.level_distinct = create_str_from_list(char=db.get_distinct_levels_all())
		self.root.ids.label_level.text = 'All'
		self.language_in = "ES"
		self.language_out = "DE"
		self.update_menus()

	# SCREEN "STATISTICS" ----------------------------------------------------------------------------------------------

	label_statistics = StringProperty(defaultvalue=calc_statistics())

	def reset_statistics(self):
		db.reset(category=self.category_distinct, level=self.level_distinct)
		self.update_menus()
		self.label_statistics = calc_statistics()
		self.category_distinct = create_str_from_list(char=db.get_distinct_categories_all())
		self.level_distinct = create_str_from_list(char=db.get_distinct_levels_all())
		self.root.ids.label_category.text = 'All'
		self.root.ids.label_level.text = 'All'

	# SCREEN "UPDATE" --------------------------------------------------------------------------------------------------

	def import_db(self):
		try:
			url = r"https://dl.dropbox.com/s/shwv4bhspcu3cbe/data.db?dl=1"
			r = requests.get(url, verify=False, timeout=5)
			open('data.db', 'wb').write(r.content)
			# shutil.copy(os.path.join(primary_external_storage_path(), "Documents", "data.db"), "data.db")
			# self.root.ids.label_update_status.text = "import successful"
		except Exception as e:
			self.root.ids.label_update_status.text = str(e)

	def export_db(self):
		try:
			shutil.copy("data.db", os.path.join(primary_external_storage_path(), "Documents", "data.db"))
			self.root.ids.label_update_status.text = "export successful"
		except Exception as e:
			self.root.ids.label_update_status.text = str(e)

	# SCREEN "ABOUT" ---------------------------------------------------------------------------------------------------

	@staticmethod
	def open_link(link: str):
		webbrowser.open(url=link)

	# OTHER ------------------------------------------------------------------------------------------------------------

	def update_category(self) -> MDDropdownMenu:
		return MDDropdownMenu(
			caller=self.screen.ids.button_category,
			items=[
				{
					"text": f"{category.capitalize()}",
					"viewclass": "OneLineListItem",
					"height": dp(56),
					"on_release": lambda x=f"{category}": self.callback_category(x),
				} for category in ["All"] + db.get_distinct_categories(level=self.level_distinct)
			],
			width_mult=3,
			max_height=dp(224),
			background_color="#A7FFEB",
		)

	def update_level(self) -> MDDropdownMenu:
		return MDDropdownMenu(
			caller=self.screen.ids.button_level,
			items=[
				{
					"text": f"{level}",
					"viewclass": "OneLineListItem",
					"height": dp(56),
					"on_release": lambda x=f"{level}": self.callback_level(x),
				} for level in ["All"] + db.get_distinct_levels(category=self.category_distinct)
			],
			width_mult=3,
			max_height=dp(224),
			background_color="#A7FFEB",
		)

	def update_sensitivity(self) -> MDDropdownMenu:
		return MDDropdownMenu(
			caller=self.screen.ids.button_sensitivity,
			items=[
				{
					"text": f"{sensitivity}",
					"viewclass": "OneLineListItem",
					"height": dp(56),
					"on_release": lambda x=f"{sensitivity}": self.callback_sensitivity(x),
				} for sensitivity in [1, 2, 3, 4, 5, 10, 20]
			],
			width_mult=3,
			max_height=dp(224),
			background_color="#A7FFEB",
		)

	def update_menus(self):
		self.menu_level = self.update_level()
		self.menu_category = self.update_category()

	# BUILD ------------------------------------------------------------------------------------------------------------

	def build(self):
		return self.screen


VocabularyTrainer().run()
